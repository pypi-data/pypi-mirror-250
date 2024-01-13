from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
import os
import warnings
import re
import sys
import json
import time
from argparse import Namespace
import functools
import copy
import shlex
import subprocess
import locale
import logging
import textwrap
from collections import defaultdict
import string
import random
from datetime import date
from pathlib import Path
from dataclasses import dataclass, asdict, fields, field
from typing import (
    cast,
    Any,
    Optional,
    Set,
    Dict,
    Union,
    List,
    Tuple,
    DefaultDict,
    ClassVar,
    Mapping,
    Sequence,
    Literal,
)

# internal modules
from annextimelog.run import run
from annextimelog.log import stdout, stderr
from annextimelog.datetime import datetime, datetime as dt, timedelta
from annextimelog import utils
from annextimelog.token import *

# external modules
from rich.table import Table
from rich.text import Text
from rich.console import Console, RenderableType
from rich.highlighter import ReprHighlighter, ISO8601Highlighter
from rich import box

logger = logging.getLogger(__name__)


@dataclass
class AnnextimelogRepo:
    DEFAULT_PATH: ClassVar = Path(
        os.environ.get("ANNEXTIMELOGREPO")
        or os.environ.get("ANNEXTIMELOG_REPO")
        or Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        / "annextimelog"
    )
    GIT_CONFIG_REGEX: ClassVar = re.compile(
        r"^(?P<key>[^\s=]+)=(?P<value>.*)$", flags=re.IGNORECASE
    )
    ANNEXTIMELOG_CONFIG_KEYS: ClassVar = {
        "emojis": "whether emojis should be shown in pretty-formated event output",
        "commit": "whether events should be committed upon modification. "
        "Setting this to false can improve performance but will reduce granularity to undo changes. ",
        "fast": "setting this to false will cause annextimelog be be more sloppy "
        "(and possible faster) by leaving out some non-critical cleanup steps. ",
        "weekstartssunday": "whether the week should start on Sunday instead of Monday (the default)",
        "longlist": "equivalent of specifying --long (e.g. atl ls -l)",
        "listall": "equivalent of specifying --all (e.g. atl ls -a)",
        "matchconditions": "equivalent of atl ls --match (set to 'all' or 'any')",
        "outputformat": "equivalent of -O / --output-format",
        "dryrun": "equivalent of -n / --dry-run",
        "slowdown": "a float value like 0.1 (ms) to make finding events *even* slower 😅 (for debugging purposes)",
    }

    path: Path = Path(DEFAULT_PATH)
    config: Dict[str, str] = field(default_factory=dict, compare=False, repr=False)

    def __getattr__(self, attr: str):
        @dataclass(repr=False)
        class RepoEvent(Event):  # Event class knowing it belongs to this repo
            repo: AnnextimelogRepo = field(default_factory=lambda: self)

        if attr.lower() in {"event"}:
            return RepoEvent
        raise AttributeError(f"{self.__class__.__name__} has no attribute {attr!r}")

    @property
    def dirty(self):
        result = self.run_git(
            subprocess.run,
            ["status", "--porcelain"],
            title="Checking if repo {self.path} is dirty",
        )
        return result.returncode or result.stdout or result.stderr

    @staticmethod
    def get_repo_root(path: Path) -> Union[Path, None]:
        logger.debug(f"🔎 Finding where the containing git repo root is for path {path}")
        result = run(
            subprocess.run,
            ["git", "-C", Path(path), "rev-parse", "--show-toplevel"],
            title=f"find git repo root for {path}",
        )
        if result.returncode:
            return None
        return Path(result.stdout.rstrip("\n").rstrip("\r"))

    @property
    def root(self) -> Union[Path, None]:
        return self.get_repo_root(self.path)

    def run_git(self, runner, gitargs: Union[str | Sequence[str]], **kwargs):
        if isinstance(gitargs, str):
            gitargs = shlex.split(gitargs)
        return run(runner, ["git", "-C", str(self.path)] + list(gitargs), **kwargs)

    def ensure_git(self) -> bool:
        """
        Ensure this is a properly useable git repo
        """
        if self.path.exists() and not self.path.is_dir():
            logger.critical(f"{self.path} exists but is not a directory.")
            return False

        if self.path.exists():
            logger.debug(f"{self.path} exists")
            if repo_root := self.root:
                if repo_root.resolve() != self.path.resolve():
                    logger.critical(
                        f"There's something funny with {self.path}: git says the repo root is {repo_root}. "
                    )
                    return False
            else:
                logger.critical(f"{self.path} exists but is no git repository. 🤔")
                return False
        else:
            if not self.path.parent.exists():
                logger.info(f"📁 Creating {self.path.parent}")
                self.path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Making a git repository at {self.path}")
            result = run(
                subprocess.run, ["git", "init", str(self.path)], capture_output=True
            )
            if result.returncode:
                logger.error(f"Couldn't make git repository at {self.path}")
                return False
        return True

    def ensure_git_annex(self) -> bool:
        """
        Ensure this is a git annex repo
        """
        logger.debug(f"Making sure {self.path} is a git annex repository")
        annex_uuid = None
        if not self.config:
            if not (
                result := self.run_git(
                    subprocess.run,
                    ["config", "annex.uuid"],
                    title=f"get (only) git annex repo uuid",
                )
            ).returncode:
                self.config["annex.uuid"] = result.stdout.strip()
        if not self.config.get("annex.uuid"):
            logger.debug(f"{self.path} is not a git annex repository")
            if not (
                result := self.run_git(
                    subprocess.run,
                    ["annex", "init"],
                    title=f"add an annex to {self.path}",
                )
            ).returncode:
                logger.info(f"Added an annex to {self.path}")
            else:
                logger.critical(f"Couldn't add an annex to {self.path}")
                return False
        return True

    def read_config(self):
        logger.debug(f"Reading config from repo {self.path}")
        result = self.run_git(subprocess.run, ["config", "--list"])
        for line in result.stdout.splitlines():
            if m := self.GIT_CONFIG_REGEX.fullmatch(line):
                self.config[m.group("key")] = m.group("value")
        if logger.getEffectiveLevel() < logging.DEBUG - 5:
            logger.debug(f"Read git config:\n{self.config}")
        if logger.getEffectiveLevel() < logging.DEBUG - 5:
            logger.debug(f"Config:\n{self.config}")

    def sync(self, args: Optional[Sequence[str]] = None) -> bool:
        """Sync with git annex"""
        if logger.getEffectiveLevel() < logging.DEBUG:
            with self.run_git(subprocess.Popen, ["annex", "assist"]) as process:
                process.wait()
                return process.returncode == 0
        else:
            with stdout.status("Syncing..."):
                result = self.run_git(
                    subprocess.run, ["annex", "assist"] + list(args or [])
                )
        if result.returncode or result.stderr:
            if result.returncode:
                logger.error(f"Syncing failed according to git annex.")
            if result.stderr:
                logger.warning(
                    f"git annex returned some STDERR messages. "
                    f"This might be harmless, maybe try again (a couple of times)."
                )
            return False
        else:
            logger.info(f"✅ Syncing finished")
        return True

    def store(self, event: Event):
        """Store an event"""
        if not event.id:
            event.id = event.random_id()
        event.clean()
        # TODO: Better handling of this, see https://gitlab.com/nobodyinperson/annextimelog/-/issues/9
        if event.end and event.start and event.end < event.start:
            logger.info(
                f"↔️  event {event.id!r}: Swapping start and end (they're backwards)"
            )
            event.start, event.end = event.end, event.start

        def folders():
            start, end = event.start, event.end
            start = date(start.year, start.month, start.day)
            end = date(end.year, end.month, end.day)
            day = start
            lastweekpath = None
            while day <= end:
                path = Path()
                for p in "%Y %m %d".split():
                    path /= day.strftime(p)
                yield path
                weekpath = Path()
                for p in "%Y W %W".split():
                    weekpath /= day.strftime(p)
                if weekpath != lastweekpath:
                    yield weekpath
                lastweekpath = weekpath
                day += timedelta(days=1)

        paths: Set[Path] = set()
        # TODO: It's a bit overkill to remove and remake symlinks, but it works
        for folder in folders():
            if not (folder_ := self.path / folder).exists():
                logger.debug(f"📁 Creating new folder {folder}")
                folder_.mkdir(parents=True)
            file = (folder_ / event.id).with_suffix(event.SUFFIX)
            if (file.exists() or file.is_symlink()) and not (event.paths or event.key):
                logger.warning(
                    f"🐛 {file} exists although this event {event.id} is new (it has no paths or key attached). "
                    f"This is either a bug 🐛 or you just witnessed a collision. 💥"
                    f"🗑️ Removing {file}."
                )
                file.unlink()
            if file.is_symlink() and not os.access(str(file), os.W_OK):
                logger.debug(f"🗑️ Removing existing read-only symlink {file}")
                file.unlink()
            file_existed = file.exists()
            with file.open("w") as fh:
                logger.debug(
                    f"🧾 {'Overwriting' if file_existed else 'Creating'} {file} with content {event.id!r}"
                )
                fh.write(event.id)
            try:
                paths.add(file.relative_to(self.path))
            except ValueError:
                paths.add(file)
        logger.debug(
            f"new paths for event {event.id}: {paths = }, current paths: {event.paths}"
        )
        if obsolete_paths := event.paths - paths:
            logger.debug(
                f"{len(obsolete_paths)} paths for event {event.id!r} are now obsolete:"
                f"\n{chr(10).join(map(str,obsolete_paths))}"
            )
            result = self.run_git(
                subprocess.run,
                ["rm", "-rf"] + sorted(obsolete_paths),  # type: ignore[arg-type]
            )
        event.paths = paths
        with stdout.status(f"Adding {len(event.paths)} paths..."):
            result = self.run_git(
                subprocess.run,
                ["annex", "add", "--json"] + sorted(event.paths),  # type: ignore[arg-type]
                output_lexer="json",
                title=f"Adding {len(event.paths)} paths for event {event.id!r}",
            )
            keys = set()
            for info in utils.from_jsonlines(result.stdout):
                if key := info.get("key"):
                    keys.add(key)
            if len(keys) != 1:
                logger.warning(
                    f"🐛 Adding {len(event.paths)} paths for event {event.id!r} resulted in {len(keys)} keys {keys}. "
                    f"That should be exactly 1. This is probably a bug."
                )
            if keys:
                event.key = next(iter(keys), None)
                logger.debug(f"🔑 key for event {event.id!r} is {event.key!r}")
        assert event.key, "Key is not set, this should not happen"
        # TODO: do all the below git actions in parallel for speed
        if event.config.get("annextimelog.fast", "false") != "true":
            with stdout.status(f"Force-dropping {keys = }..."):
                result = self.run_git(
                    subprocess.run,
                    [
                        "annex",
                        "drop",
                        "--force",
                        "--key",
                    ]
                    + list(keys),
                    title=f"Force-dropping {keys = } for event {event.id!r}",
                )
        if (is_new := self.dirty) and event.config.get(
            "annextimelog.commit", "true"
        ) == "true":
            with stdout.status(
                status := f"Committing addition of event {event.id!r}..."
            ):
                result = self.run_git(
                    subprocess.run,
                    [
                        "commit",
                        "-m",
                        f"➕ Add {event.id}"
                        + (f" {event.title!r}" if event.title else ""),
                    ],
                    title=status,
                )
                if not result.returncode:
                    logger.info(f"✅ Committed addition of event {event.id!r}")
        if not is_new:
            # reset metadata
            logger.debug(f"Removing all metadata for event {event.id}")
            logger.debug(
                f"Yup, this (full removal, then full back-addition) is how it's done currently "
                f"😅 It will probably be optimized at some point."
            )
            if self.run_git(
                subprocess.run,
                shlex.split("annex metadata --remove-all --key") + [event.key],
            ).returncode:
                logger.error(
                    f"Something went wrong purging annex metadata on event {event.id} key {event.key!r}"
                )
        # add metadata
        cmd = ["annex", "metadata", "--key", event.key]
        for field, values in event.fields.items():
            for value in values:
                if hasattr(value, "timeformat"):
                    value = value.timeformat()
                cmd.extend(["--set", f"{field}+={value}"])
        logger.debug(f"Setting all current metadata for event {event.id}")
        if self.run_git(subprocess.run, cmd).returncode:
            logger.error(
                f"Something went wrong setting annex metadata on event {event.id} key {event.key!r}"
            )
        if logger.getEffectiveLevel() <= logging.DEBUG and self.config.get(
            "annextimelog.outputformat"
        ) not in (
            "rich",
            "console",
        ):
            logger.debug(f"Event after saving:")
            stderr.print(event.to_rich())

    def delete(self, events: Union[Event, Sequence[Event]]) -> bool:
        if isinstance(events, Event):
            events = [events]
        events = list(events)
        allpaths: Set[Path] = set()
        for event in events:
            allpaths.update(event.paths)
        if not allpaths:
            logger.info(f"No matching events to delete")
            return False
        with stdout.status(
            f"Deleting {len(allpaths)} paths for {len(events)} event{'s' if len(events)>1 else ''}"
        ) as status:
            result = self.run_git(
                subprocess.run, ["rm", "-rf"] + sorted(map(str, allpaths))
            )
            success = not (result.returncode or result.stderr)
            status.update(f"Committing deletion of {len(events)} events")
            if self.config.get("annextimelog.commit", "true") == "true":
                result = self.run_git(
                    subprocess.run,
                    [
                        "commit",
                        "-m",
                        f"🗑️ Remove event{'' if len(events) == 1 else 's'} {' '.join(map(str,(ev.id for ev in events)))}",
                    ],
                )
                success |= not (result.returncode or result.stderr)
        if success:
            logger.info(
                f"✅ Deleted {len(events)} {' '.join(sorted(map(str,(ev.id for ev in events))))}"
            )
        return success

    def find_events(
        self, query: Union[Sequence[Token] | Sequence[str] | str]
    ) -> Iterator[Event]:
        match query:
            case [*strings] if all(isinstance(s, str) for s in strings):
                query = Token.from_strings(strings, is_condition=True)  # type: ignore
            case str() as s:
                query = Token.from_strings(s, is_condition=True)  # type: ignore
        query = cast(Sequence[Token], query)  # make mypy happy
        if logger.getEffectiveLevel() < logging.DEBUG:
            logger.debug(f"Finding events matching these tokens: 👇")
            stderr.log(query)
        start = datetime.min
        end = datetime.max
        # keep intersection of all time frames as query frame
        for token in query:
            if not token.is_condition:
                logger.warning(f"Ignoring non-condition {token.string!r}")
                continue
            match token:
                case TimeFrame():
                    start = max(start, token.start or datetime.min)
                    end = min(end, token.end or datetime.max)
        logger.debug(f"{start = }, {end = }")
        with stdout.status(f"Querying metadata..."):
            # TODO: don't query all events but only paths that make sense
            # would be more elegant to use something like 'findkeys' which wouldn't output
            # duplicates, but then we'd have to use 'whereused' to find out the repo paths
            # and also 'findkeys' only lists existing non-missing annex keys, so meh...
            cmd = ["annex", "metadata", "--json"]
            cmd.extend(
                L := Event.git_annex_args_timerange(
                    start=None if start == datetime.min else start,
                    end=None if end == datetime.max else end,
                )
            )
            logger.debug(f"git annex matching args: {L = }")
            result = self.run_git(subprocess.run, cmd)
        counter = itertools.count(counter_start := 1)
        events: List[Event] = []

        def statusmsg(n):
            return f"🔎 Searched {n} events, {len(events)} matched"

        try:
            slowdown = float(v := self.config.get("annextimelog.slowdown", "0"))
        except Exception as e:
            slowdown = 0.1
            logger.warning(
                f"Weird value {v}!r for slowdown config: {e!r}. Using {slowdown}."
            )
        with stdout.status(msg := statusmsg(0)) as status:
            for n, event in enumerate(
                self.Event.multiple_from_metadata(utils.from_jsonlines(result.stdout)),
                start=1,
            ):
                time.sleep(slowdown)
                event_matches = event.matches(
                    query, match=self.config.get("annextimelog.matchcondition", "all")
                )
                logger.debug(
                    f"Event {event.id} {'matches' if event_matches else 'does not match'} query {shlex.join(t.string for t in query)!r}"  # type: ignore
                )
                if event_matches:
                    events.append(event)
                    yield event
                status.update(msg := statusmsg(n))
        logger.info(msg)


@dataclass(repr=False)
class Event:
    repo: Optional[AnnextimelogRepo] = None
    id: Optional[str] = None
    paths: Set[Path] = field(default_factory=set)
    key: Optional[str] = None
    fields: Dict[str, Set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )  # type: ignore

    SUFFIX: ClassVar = ".ev"
    RESERVED_FIELDS: ClassVar = "start end tag location title note id".split()

    @property
    def start(self) -> Union[datetime, None]:
        if "start" not in self.fields:
            self.fields["start"] = set()
        if not (start := self.fields["start"]):
            return None
        elif len(start) > 1:
            try:
                earliest = min(
                    d.astimezone() for d in (self.parse_date(s) for s in start) if d
                )
            except Exception as e:
                logger.error(
                    f"There are {len(start)} start times for event {self.id!r}, but I can't determine the earliest: {e!r}"
                )
                self.fields["start"].clear()
                return None
            logger.warning(
                f"There were {len(start)} start times for event {self.id!r}. Using the earlier one {earliest}."
            )
            self.fields["start"].clear()
            self.fields["start"].add(earliest.timeformat())
        return self.parse_date(next(iter(self.fields["start"]), None))

    @start.setter
    def start(self, value: Union[datetime, str, None]):
        if value is None:
            self.fields["start"].clear()
            return
        if d := self.parse_date(value):
            self.fields["start"].clear()
            self.fields["start"].add(d.timeformat())
        else:
            logger.error(f"Couldn't interpret {value!r} as time.")
            self.fields["start"].clear()

    @property
    def end(self) -> Union[datetime, None]:
        if "end" not in self.fields:
            self.fields["end"] = set()
        if not (end := self.fields["end"]):
            return None
        elif len(end) > 1:
            try:
                latest = min(
                    d.astimezone() for d in (self.parse_date(s) for s in end) if d
                )
            except Exception as e:
                logger.error(
                    f"There are {len(end)} end times for event {self.id!r}, but I can't determine the latest: {e!r}"
                )
                self.fields["end"].clear()
                return None
            logger.warning(
                f"There were {len(end)} end times for event {self.id!r}. Using the later one {latest}."
            )
            self.fields["end"].clear()
            self.fields["end"].add(latest.timeformat())
        return self.parse_date(next(iter(self.fields["end"]), None))

    @end.setter
    def end(self, value: Union[datetime, str, None]):
        if value is None:
            self.fields["end"].clear()
            return
        if d := self.parse_date(value):
            self.fields["end"].clear()
            self.fields["end"].add(d.timeformat())
        else:
            logger.error(f"Couldn't interpret {value!r} as time.")
            self.fields["end"].clear()

    @property
    def note(self):
        if len(note := self.fields.get("note", set())) > 1:
            note = "\n".join(self.fields["note"])
            self.fields["note"].clear()
            self.fields["note"].add(note)
        return "\n".join(self.fields.get("note", set()))

    @note.setter
    def note(self, value):
        self.fields["note"].clear()
        self.fields["note"].add(value)

    @property
    def title(self):
        if len(title := self.fields.get("title", set())) > 1 or any(
            re.search(r"[\r\n]", t) for t in title
        ):
            title = " ".join(re.sub(r"[\r\n]+", " ", t) for t in self.fields["title"])
            self.fields["title"].clear()
            self.fields["title"].add(title)
        return "\n".join(self.fields.get("title", set()))

    @title.setter
    def title(self, value):
        value = re.sub(r"[\r\n]+", " ", str(value))
        self.fields["title"].clear()
        self.fields["title"].add(value)

    @property
    def tags(self):
        if "tag" not in self.fields:
            self.fields["tag"] = set()
        return self.fields["tag"]

    @property
    def config(self) -> Dict[str, str]:
        return getattr(self.repo, "config", dict())

    @classmethod
    def classconfig(cls) -> Dict[str, str]:
        repo = None
        if repofield := next((f for f in fields(cls) if f.name == "repo"), None):
            try:
                repo = repofield.default_factory()  # type: ignore[misc]
            except Exception as e:
                repo = repofield.default
        return getattr(repo, "config", dict())

    @classmethod
    def multiple_from_metadata(
        cls, metadatalines: Sequence[Dict[str, Any]], **init_kwargs
    ) -> Iterator[Event]:
        keys: Dict[str, Dict[str, Any]] = defaultdict(lambda: defaultdict(set))
        for i, data in enumerate(metadatalines, start=1):
            if logger.getEffectiveLevel() < logging.DEBUG - 5:
                logger.debug(f"parsed git annex metadata line #{i}:\n{data}")
            if key := data.get("key"):
                keys[key]["data"] = data
            if p := next(iter(data.get("input", [])), None):
                keys[key]["paths"].add(p)
        for key, info in keys.items():
            if not (d := info.get("data")):
                continue
            event = cls.from_metadata(d, paths=info["paths"], **init_kwargs)
            if logger.getEffectiveLevel() < logging.DEBUG - 5:
                logger.debug(f"parsed Event from metadata line #{i}:\n{event}")
            yield event

    def clean(self):
        """
        Remove inconsistencies in this event.
        """
        properties = [
            attr
            for attr in dir(self)
            if isinstance(getattr(type(self), attr, None), property)
        ]
        # Call all properties - they do their own cleanup
        for p in properties:
            getattr(self, p)
        # remove empty fields
        for field in (empty_fields := [f for f, v in self.fields.items() if not v]):
            del self.fields[field]
        # ensure paths are Path
        self.paths = set(Path(p) for p in self.paths)

    @staticmethod
    def random_id():
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))

    @staticmethod
    def parse_date(s) -> Union[datetime, None]:
        if isinstance(s, datetime):
            return s
        if t := Time.from_str(s):
            return t.time
        return None

    @classmethod
    def git_annex_args_timerange(cls, start=None, end=None):
        """
        Construct a git-annex matching expression suitable for use as arguments with :any:$(subprocess.run) to only match data files containing data in a given period of time based on the unix timestamp in the 'start' and 'end' metadata
        """
        data_starts_before_end_or_data_ends_after_start = shlex.split(
            "-( --metadata start<{end} --or --metadata end>{start} -)"
        )
        data_not_only_before_start = shlex.split(
            "--not -( --metadata start<{start} --and --metadata end<{start} -)"
        )
        data_not_only_after_end = shlex.split(
            "--not -( --metadata start>{end} --and --metadata end>{end} -)"
        )
        condition = []
        info = dict()
        start = cls.parse_date(start)
        end = cls.parse_date(end)
        if start is not None:
            condition += data_not_only_before_start
            info["start"] = start.timeformat()
        if end is not None:
            condition += data_not_only_after_end
            info["end"] = end.timeformat()
        if all(x is not None for x in (start, end)):
            condition += data_starts_before_end_or_data_ends_after_start
        return [p.format(**info) for p in condition]

    @staticmethod
    def timeformat(**kwargs) -> str:
        return datetime.timeformat(**kwargs)

    def apply(self, tokens: Sequence[Token]):
        unhandled: List[Token] = []
        for token in tokens:
            match token:
                case TimeStart(time=t):
                    self.start = t
                case TimeEnd(time=t):
                    self.end = t
                case TimeFrame(start=start, end=end):
                    self.start, self.end = start, end
                case FieldModifier(field="id"):
                    logger.warning(
                        f"Ignoring {token.string!r}: the id field is reserved"
                    )
                case SetField(field=field, values=values):
                    old = self.fields.get(field, set())
                    if old and old != values:
                        logger.warning(f"Overwriting previous {field!r} values {old}")
                    self.fields[field] = set(values)
                case AddToField(field=field, values=values):
                    if field not in self.fields:
                        self.fields[field] = set()
                    for value in values:
                        self.fields[field].add(value)
                case RemoveFromField(field=field, values=values):
                    if field in self.fields:
                        for value in values:
                            if value in self.fields[field]:
                                self.fields[field].remove(value)
                case UnsetField(field=field):
                    if field in self.fields:
                        del self.fields[field]
                case Noop():  # ignore noops, don't consider it unhandled
                    pass
                case _:
                    unhandled.append(token)
        if unhandled:
            logger.warning(
                f"Ignored {len(unhandled)} tokens {shlex.join(t.string for t in unhandled)!r} ({'·'.join(t.__class__.__name__ for t in unhandled)})"
            )

    def matches(
        self,
        tokens: Union[Token, Sequence[Token]],
        match: Union[Literal["all", "any"]] = "all",
    ) -> Union[bool, None]:
        if isinstance(tokens, Token):  # only one token given
            token = tokens  # mypy doesn't see walrus-style here, so old school 🤷
            if token.is_condition is False:
                logger.warning(
                    f"{token} is not a condition token, still using it to match, but this shouldn't happend"
                )
            match token:
                case TimeStart() | TimeEnd() | TimeFrame():
                    # TODO: This below abomination of a code block is quite
                    # inelegant but necessary as the extremes (dt.min and dt.max)
                    # can't be safely astimezone()d or timestamp()ed (exceeds limits)
                    inputtimes = dict(
                        start=getattr(token, "time", getattr(token, "start", None)),
                        end=getattr(token, "time", getattr(token, "end", None)),
                        estart=self.start,
                        eend=self.end,
                    )

                    def to_float(k: str, v: Union[datetime, None]) -> float:
                        match v:
                            case datetime():
                                return v.timestamp()
                            case x if x in (dt.min, dt.ensure(dt.min)):
                                return float("-inf")
                            case x if x in (dt.max, dt.ensure(dt.max)):
                                return float("inf")
                            case None if "start" in k:
                                return float("-inf")
                            case None if "end" in k:
                                return float("inf")
                        raise ValueError(f"{k!r} = {v!r} is a weird time")

                    times = {k: to_float(k, v) for k, v in inputtimes.items()}
                    start = times["start"]
                    end = times["end"]
                    estart = times["estart"]
                    eend = times["eend"]
                    conditions = [
                        # event_starts_before_end_or_event_ends_after_start
                        estart <= end or eend >= start,
                        # event_not_only_before_start
                        not (estart <= start and end <= start),
                        # event_not_only_after_end
                        not (estart >= end and eend >= end),
                    ]
                    return all(conditions)
                # field contains given values
                case FieldValueModifier(field=field, values=patterns):
                    present_values = (
                        set([self.id or ""])  # id field special case
                        if field.lower() == "id"
                        else self.fields.get(field, set())
                    )
                    for pattern in patterns:
                        try:
                            regex = re.compile(pattern, flags=re.IGNORECASE)
                        except Exception as e:
                            logger.error(
                                f"{pattern!r} from {shlex.quote(token.string)} is not a valid regular expression: {e!r}. Skipping."
                            )
                            continue
                        matches = set(v for v in present_values if regex.search(v))
                        if logger.getEffectiveLevel() < logging.DEBUG - 5:
                            logger.debug(
                                f"{pattern = !r} matches {len(matches)} values {matches} in {field!r} field {present_values} of event {self.id}"
                            )
                        match token:
                            case RemoveFromField():
                                return not matches
                            case _ if not matches:
                                return False
                    return True
                # field is empty
                case UnsetField(field=field):
                    logger.debug(f"{self.fields.get(field,set()) = }")
                    return not self.fields.get(field, set())
                case Noop():  # ignore noops, don't consider it unhandled
                    pass
                case _:
                    return None
        else:  # multiple tokens given
            handled: List[Token] = []
            unhandled: List[Token] = []
            results: List[bool] = []
            for token in tokens:
                match result := self.matches(token):
                    case None:
                        unhandled.append(token)
                    case _:
                        results.append(result)
                        handled.append(token)
            if unhandled:
                logger.warning(
                    f"Ignored {len(unhandled)} tokens {shlex.join(t.string for t in unhandled)!r} ({'·'.join(t.__class__.__name__ for t in unhandled)})"
                )
            if logger.getEffectiveLevel() < logging.DEBUG:
                for token, result in zip(handled, results):
                    logger.debug(
                        f"Event {self.id} {'matches' if result else 'does not match'} token {token!r}"
                    )
            match match:
                case "all":
                    return all(results)
                case "any":
                    return any(results)
                case _:
                    warnings.warn(f"weird {match = } argument. Using 'all'")
                    return all(results)
        return False

    @staticmethod
    def delegate_to_repo(decorated_fun):
        @functools.wraps(decorated_fun)
        def wrapper(self, *args, **kwargs):
            methodname = decorated_fun.__name__
            if not self.repo:
                raise ValueError(
                    f"Cannot {self.__class__.__name__}{methodname}() without knowing what repo it belongs to."
                )
            if not (f := getattr(self.repo, methodname, None)):
                raise ValueError(f"{self.repo} has no method {methodname}")
            return f(self)

        return wrapper

    @delegate_to_repo
    def store(self):
        pass

    @delegate_to_repo
    def delete(self):
        pass

    #################
    ### 📥  Input ###
    #################
    @classmethod
    def from_metadata(cls, data: Dict[str, Any], **init_kwargs) -> Event:
        """
        Create an event from a parsed output line of ``git annex metadata --json``.
        """
        path = Path(data.get("input", [None])[0])
        fields = data.get("fields", dict())
        kwargs = init_kwargs.copy()
        kwargs.setdefault("paths", set())
        kwargs["paths"].add(path)
        kwargs.update(
            dict(
                id=path.stem,
                key=data.get("key"),
                fields={
                    k: set(v)
                    for k, v in fields.items()
                    if not (k.endswith("-lastchanged") or k in ["lastchanged"])
                },
            )
        )
        return cls(**kwargs)

    @classmethod
    def parse_timerange(cls, parts) -> slice:
        start, end = datetime.min, datetime.max
        match parts:
            case [datetime() as t] | [
                "since" | "starting" | "from",
                datetime() as t,
            ]:
                start = t
            case ["-", datetime() as t] | [
                "until" | "to" | "-",
                datetime() as t,
            ]:
                end = t
            case [datetime() as t1, datetime() as t2]:
                start, end = t1, t2
            case _:
                raise ValueError(f"Unknown time range specification {parts}")
        return slice(
            None if start == datetime.min else start,
            None if end == datetime.max else end,
        )

    @classmethod
    def from_tokens(cls, tokens: Sequence[Token], **kwargs) -> Event:
        event = cls(**kwargs)
        event.apply(tokens)
        event.clean()
        return event

    @classmethod
    def from_cli(cls, cliargs: Sequence[str], **kwargs) -> Event:
        """
        Create a new event from command-line arguments such as given to 'atl track'
        """
        logger.debug(f"Creating event from {cliargs = }")
        for i, token in enumerate(
            tokens := Token.from_strings(
                cliargs, config=cls.classconfig(), is_condition=False
            ),
            start=1,
        ):
            logger.debug(f"arg #{i:2d}: {token!r}")
        return cls.from_tokens([t for t in tokens if t is not None], **kwargs)

    ##################
    ### 📢  Output ###
    ##################
    def to_rich(self, long=None) -> RenderableType:
        table = Table(title=self.title, padding=0, box=box.ROUNDED, show_header=False)
        emojis = self.config.get("annextimelog.emojis", "true") == "true"
        if not any(self.to_dict().values()):
            table.add_column("")
            table.add_row("empty event")
            return table
        table.add_column("", justify="left", width=None if emojis else -1)
        table.add_column("Field", justify="right", style="cyan")
        table.add_column("Value", justify="left")
        longlist = (
            self.config.get("annextimelog.longlist", "false") == "true" or long is True
        )
        if self.id:
            table.add_row("💳", "id", f"[b]{self.id}[/b]")
        if self.paths and (longlist):
            table.add_row(
                "🧾",
                "paths",
                ReprHighlighter()(Text("\n".join(str(p) for p in self.paths))),
            )
        if self.paths and longlist:
            table.add_row("🔑", "key", self.key)
        timehighlighter = ISO8601Highlighter()
        if start := self.start:
            table.add_row("🚀", "start", start.astimezone().strftime("%c%Z"))
        if end := self.end:
            table.add_row("⏱️", "end", end.astimezone().strftime("%c%Z"))
        if start and end and abs(end - start).total_seconds() > 0:
            table.add_row("⌛", "duration", td.ensure(end - start).pretty_duration)
        if location := self.fields.get("location", set()):
            table.add_row(
                "📍",
                "location",
                " ".join([f"{'📍 ' if emojis else '·'}{t}" for t in sorted(location)]),
            )
        if self.tags:
            table.add_row(
                "🏷️",
                "tags",
                " ".join([f"{'🏷️ ' if emojis else '·'}{t}" for t in sorted(self.tags)]),
            )
        for field, values in self.fields.items():
            if field in self.RESERVED_FIELDS:
                continue
            table.add_row(
                "",
                field,
                " ".join(f"·{value}" for value in values),
            )
        if self.note:
            table.add_row("📝", "note", self.note)
        return table

    def to_dict(self):
        if sys.version_info < (3, 12):
            # https://github.com/python/cpython/pull/32056
            # dataclasses.asdict() doesn't like defaultdict
            e = copy.copy(self)
            e.fields = dict(self.fields)  # turn defaultdict into plain dict
        else:
            e = self
        return asdict(
            e, dict_factory=lambda x: {k: v for k, v in x if k not in {"args"}}
        )

    def to_json(self) -> str:
        def default(x):
            if hasattr(x, "timeformat"):
                return x.timeformat()
            if not isinstance(x, str):
                try:
                    iter(x)
                    return tuple(x)
                except TypeError:
                    pass
            return str(x)

        return json.dumps(self.to_dict(), default=default)

    def to_timeclock(self):
        def sanitize(s):
            s = re.sub(r"[,:;]", r"⁏", s)  # replace separation chars
            s = re.sub(r"[\r\n]+", r" ", s)  # no newlines
            return s

        hledger_tags = {
            k: " ⁏ ".join(map(sanitize, v))
            for k, v in self.fields.items()
            if k not in "start end".split()
        }
        for tag in sorted(self.tags):
            hledger_tags[tag] = ""
        hledger_tags = [f"{t}: {v}" for t, v in hledger_tags.items()]
        hledger_comment = f";  {', '.join(hledger_tags)}" if hledger_tags else ""
        info = [
            ":".join(self.fields.get("account", self.tags)),
            self.title,
            hledger_comment,
        ]
        return textwrap.dedent(
            f"""
        i {self.start.strftime('%Y-%m-%d %H:%M:%S%z')} {'  '.join(filter(bool,info))}
        o {self.end.strftime('%Y-%m-%d %H:%M:%S%z')}
        """
        ).strip()

    def to_cli(self) -> List[str]:
        args = []
        fields = self.fields.copy() if self.fields else dict()
        if start := self.start:
            fields.pop("start", None)
            args.append(start.timeformat(timezone=None))
        if end := self.end:
            fields.pop("end", None)
            args.append(end.timeformat(timezone=None))
        if tags := fields.pop("tag", None):
            args.extend(tags)
        for field, values in fields.items():
            for value in values:
                if hasattr(value, "timeformat"):
                    value = value.timeformat(timezone=None)
                args.append(f"{field}+={value}")
        return args

    def output(self, args: Namespace):
        printer = {
            "timeclock": print,
            "json": print,
            "cli": lambda args: print(shlex.join(["atl", "tr"] + self.to_cli())),
        }.get(args.output_format, stdout.print)
        printer(getattr(self, f"to_{args.output_format}", self.to_rich)())  # type: ignore[operator]

    def __repr__(self) -> str:
        if hasattr(sys, "ps1"):
            with (c := Console(force_terminal=False)).capture() as capture:
                c.print(self.to_rich(long=True))
            return capture.get()
        else:
            args = ", ".join(f"{f.name}={getattr(self,f.name)!r}" for f in fields(self))
            return f"{self.__class__.__name__}({args})"

    def __eq__(self, other):
        """
        Two events are considered equal if their fields match sensibly
        """

        def sanitize(fields):
            # ensure values are set
            fields = {
                k: (set([v]) if isinstance(v, str) else set(v))
                for k, v in fields.items()
                if v
            }
            # convert to common timezone
            fields = {
                field: {
                    (
                        v.astimezone(ZoneInfo("UTC")).replace(microsecond=0)
                        if hasattr(v, "astimezone")
                        else v
                    )
                    for v in values
                }
                for field, values in fields.items()
            }
            return fields

        fields = sanitize(self.fields)
        otherfields = sanitize(other.fields)
        for field, values in fields.items():
            othervalues = otherfields.pop(field, None)
            if not (values or othervalues):  # both empty
                continue
            if values != othervalues:
                if logger.getEffectiveLevel() < logging.DEBUG - 5:
                    logger.debug(
                        f"events aren't equal because {field!r} values {values} != {othervalues}"
                    )
                return False
        if any(otherfields.values()):
            if logger.getEffectiveLevel() < logging.DEBUG - 5:
                logger.debug(
                    f"events aren't equal there are values {set(otherfields.values)} left"
                )
            return False
        return True
