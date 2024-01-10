# system modules
import time
from fnmatch import fnmatchcase
import warnings
import unittest
import itertools
import glob
import collections
import uuid
import os
import json
import re
import textwrap
import sys
import shlex
import logging
import subprocess
import argparse
from datetime import timedelta
from collections import defaultdict
from typing import List, Dict, Set
from pathlib import Path
import importlib.metadata

# internal modules
from annextimelog.event import Event
from annextimelog.log import stdout, stderr, setup_logging
from annextimelog.run import run, get_repo_root
from annextimelog.config import ANNEXTIMELOG_CONFIG_KEYS
from annextimelog.token import Token, TimeFrame
from annextimelog import utils
from annextimelog.utils import datetime, datetime as dt

# external modules
import rich
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.pretty import Pretty
from rich.text import Text
from rich import box

logger = logging.getLogger(__name__)


def test_cmd_handler(args, other_args):
    loader = unittest.TestLoader()
    logger.debug(f"🧪 Importing test suite")
    import annextimelog.test

    logger.info(f"🚀 Running test suite")
    testsuite = loader.loadTestsFromModule(annextimelog.test)
    result = unittest.TextTestRunner(
        verbosity=args.test_verbosity, buffer=args.test_verbosity <= 2
    ).run(testsuite)
    logger.debug(f"{result = }")
    if result.wasSuccessful():
        logger.info(f"✅ Test suite completed successfully")
    else:
        logger.error(f"💥 There were problems during testing.")
        sys.exit(1)


def git_cmd_handler(args, other_args):
    result = run(subprocess.Popen, ["git", "-C", str(args.repo)] + other_args)
    result.wait()
    sys.exit(result.returncode)


def config_cmd_handler(args: argparse.Namespace, other_args: List[str]):
    git_config_args = [
        (
            re.sub(r"^(annextimelog\.)?", "annextimelog.", a)
            if a in ANNEXTIMELOG_CONFIG_KEYS
            else a
        )
        for a in other_args
    ]
    result = run(
        subprocess.Popen, ["git", "-C", str(args.repo), "config"] + git_config_args
    )
    result.wait()
    sys.exit(result.returncode)


def sync_cmd_handler(args, other_args):
    if logger.getEffectiveLevel() < logging.DEBUG:
        with run(
            subprocess.Popen, ["git", "-C", args.repo, "annex", "assist"]
        ) as process:
            process.wait()
            sys.exit(process.returncode)
    else:
        with stderr.status("Syncing..."):
            result = run(
                subprocess.run, ["git", "-C", args.repo, "annex", "assist"] + other_args
            )
    if result.returncode or result.stderr:
        if result.returncode:
            logger.error(f"Syncing failed according to git annex.")
        if result.stderr:
            logger.warning(
                f"git annex returned some STDERR messages. "
                f"This might be harmless, maybe try again (a couple of times)."
            )
        sys.exit(1)
    else:
        logger.info(f"✅ Syncing finished")
    sys.exit(result.returncode)


def track_cmd_handler(args, other_args):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    if not args.metadata:
        trackparser.print_help()
        sys.exit(2)
    event = Event.from_cli(args.metadata, args=args)
    if not (event.start and event.end):
        stderr.log(event.to_rich())
        logger.critical(
            f"Currently, 'annextimelog track' can only record events with exactly two given time bounds "
            "(e.g. '3h', '10 - 12', '10min until now', etc., see 'atl -h' for more examples). "
            f"This limitation will probably be removed in the future. "
            f"You can debug this by rerunning with some -vvvv."
        )
        sys.exit(1)
    if logger.getEffectiveLevel() < logging.DEBUG:
        logger.debug(f"Event before saving:")
        stderr.print(event.to_rich())
    if not args.dry_run:
        event.id = event.id or event.random_id()
    event.output(args)
    if args.dry_run:
        logger.info(f"--dry-run was given, so this new event is not stored.")
        return
    event.store()
    cmd = ["git", "-C", args.repo, "annex", "metadata", "--key", event.key]
    for field, values in event.fields.items():
        for value in values:
            if hasattr(value, "strftime"):
                value = Event.timeformat(value)
            cmd.extend(["--set", f"{field}+={value}"])
    if run(subprocess.run, cmd).returncode:
        logger.error(
            f"Something went wrong setting annex metadata on event {event.id} key {event.key!r}"
        )
    if logger.getEffectiveLevel() <= logging.DEBUG and args.output_format not in (
        "rich",
        "console",
    ):
        logger.debug(f"Event after saving:")
        stderr.print(event.to_rich())


def summary_cmd_handler(args: argparse.Namespace, other_args: List[str]):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    # TODO: parse tokens
    if not (
        tokens := Token.from_strings(
            getattr(
                args,
                "query",
                (default := [] if getattr(args, "all", None) else ["today"]),
            )
        )
    ):
        logger.debug(f"No query tokens, using current day as constraint")
        tokens = Token.from_strings(default)
    logger.debug(f"atl ls: {tokens = }")
    start = datetime.min
    end = datetime.max
    # keep intersection of all time frames as query frame
    for token in tokens:
        match token:
            case TimeFrame():
                start = max(start, token.start or datetime.min)
                end = min(end, token.end or datetime.max)
    logger.debug(f"{start = }, {end = }")
    with logger.console.status(f"Querying metadata..."):  # type: ignore[attr-defined]
        # TODO: don't query all events but only paths that make sense
        # would be more elegant to use something like 'findkeys' which wouldn't output
        # duplicates, but then we'd have to use 'whereused' to find out the repo paths
        # and also 'findkeys' only lists existing non-missing annex keys, so meh...
        cmd = ["git", "-C", args.repo, "annex", "metadata", "--json"]
        cmd.extend(
            L := Event.git_annex_args_timerange(
                start=None if start == datetime.min else start,
                end=None if end == datetime.max else end,
            )
        )
        logger.debug(f"git annex matching args: {L = }")
        result = run(subprocess.run, cmd)
    counter = itertools.count(counter_start := 1)
    events: List[Event] = []

    def statusmsg(n):
        return f"🔎 Searched {n} events, {len(events)} matched"

    with logger.console.status(msg := statusmsg(0)) as status:  # type: ignore[attr-defined]
        for n, event in enumerate(
            Event.multiple_from_metadata(
                utils.from_jsonlines(result.stdout), args=args
            ),
            start=1,
        ):
            event_matches = event.matches(tokens, match=getattr(args, "match", "all"))
            logger.debug(
                f"Event {event.id} {'matches' if event_matches else 'does not match'} query {shlex.join(t.string for t in tokens)!r}"  # type: ignore
            )
            if event_matches:
                events.append(event)
            status.update(msg := statusmsg(n))
    for event in events:
        if getattr(args, "id_only", None):
            stdout.out(event.id)
        else:
            event.output(args)
    logger.info(msg)


def delete_cmd_handler(args: argparse.Namespace, other_args: List[str]):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    paths: Dict[str, Set[Path]] = defaultdict(set)
    for givenpattern in args.patterns:
        pattern = f"*{givenpattern}*.ev"
        result = run(
            subprocess.run,
            ["git", "-C", args.repo, "ls-files", f"*/{pattern}"],
        )
        gitpaths = set(Path(p) for p in result.stdout.splitlines())
        logger.debug(
            f"git finds {len(gitpaths)} paths for {pattern!r}: {' '.join(map(str,gitpaths))}"
        )
        globpaths = set(
            p.relative_to(args.repo)
            for p in args.repo.glob(f"**/{pattern}")
            if p != (g := args.repo / ".git") and g not in p.parents
        )
        logger.debug(
            f"globbing for {pattern!r} finds {len(globpaths)} paths: {' '.join(map(str,globpaths))}"
        )
        paths[pattern].update(gitpaths)
        paths[pattern].update(globpaths)
        # really only keep event matches (git and glob() sometimes match weird stuff...)
        realmatches = set(p for p in paths[pattern] if fnmatchcase(p.name, pattern))
        if mismatches := paths[pattern] - realmatches:
            logger.debug(
                f"{len(mismatches)} of those matches don't actually match: {' '.join(map(str,mismatches))}"
            )
            paths[pattern] = realmatches
    counter = itertools.count(0)
    for pattern, foundpaths in paths.items():
        ids = set(p.stem for p in foundpaths)
        if len(ids) > 1 and not args.force:
            logger.warning(f"Found {len(ids)} IDs matching {pattern!r}: {ids}")
            next(counter)
    if next(counter) and not args.force:
        logger.warning(f"Use --force to delete all above matches.")
        sys.exit(1)
    allpaths: Set[Path] = set(itertools.chain.from_iterable(paths.values()))
    allids: Set[str] = set(p.stem for p in allpaths)
    if not allpaths:
        logger.error(
            f"🤷 No events found for id patterns {args.patterns}. "
            "(Remember patterns are case-sensitive!)"
        )
        sys.exit(1)
    logger.debug(f"Matched paths:\n{chr(10).join(map(str,allpaths))}")
    if args.dry_run:
        logger.info(
            f"--dry-run: Would now delete {len(allpaths)} paths for {len(allids)} events {allids}"
        )
        return
    result = run(
        subprocess.run, ["git", "-C", args.repo, "rm", "-rf"] + sorted(allpaths)
    )
    success = not (result.returncode or result.stderr)
    if args.config.get("annextimelog.commit", "true") == "true":
        result = run(
            subprocess.run,
            [
                "git",
                "-C",
                args.repo,
                "commit",
                "-m",
                f"🗑️ Remove event{'' if len(allids) == 1 else 's'} {' '.join(allids)}",
            ],
        )
        success |= not (result.returncode or result.stderr)
    if success:
        logger.info(f"🗑️ Removed {len(allpaths)} paths for events {allids}")
    else:
        logger.error(f"Couldn't remove events {allids}")
        sys.exit(1)


def key2value(x):
    if m := utils.GIT_CONFIG_REGEX.fullmatch(x):
        return m.groups()
    else:
        raise argparse.ArgumentTypeError(f"{x!r} is not a key=value pair")


def add_common_arguments(parser):
    # TODO return/yield new groups?
    datagroup = parser.add_argument_group(title="Data")
    datagroup.add_argument(
        "--repo",
        type=Path,
        default=(
            default := Path(
                os.environ.get("ANNEXTIMELOGREPO")
                or os.environ.get("ANNEXTIMELOG_REPO")
                or Path(
                    os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
                )
                / "annextimelog"
            )
        ),
        help=f"Backend repository to use. "
        f"Defaults to $ANNEXTIMELOGREPO, $ANNEXTIMELOG_REPO or $XDG_DATA_HOME/annextimelog (currently: {str(default)})",
    )
    datagroup.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="don't actually store, modify or delete events in the repo. "
        "Useful for testing what exactly commands would do."
        "Note that the automatic repo creation is still performed.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Just do it. Ignore potential data loss.",
    )
    outputgroup = parser.add_argument_group(
        title="Output", description="Options changing output behaviour"
    )
    outputgroup.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="verbose output. More -v ⮕ more output",
    )
    outputgroup.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="less output. More -q ⮕ less output",
    )
    outputgroup.add_argument(
        "-O",
        "--output-format",
        choices={"rich", "console", "json", "timeclock", "cli"},
        default=(default := "console"),  # type: ignore
        help=f"Select output format. Defaults to {default!r}.",
    )


parser = argparse.ArgumentParser(
    description="⏱️ Time tracker based on Git Annex",
    epilog=textwrap.dedent(
        """
🛠️ Usage

Logging events:

> atl tr work for 4h @home with client=smallcorp on project=topsecret
> atl tr 10 - 11 @doctor
> atl tr y22:00 - 30min ago sleep @home quality=meh
> atl -vvv tr ... # debug problems

    Note: Common prepositions like 'with', 'about', etc. are ignored. See the full list with
    > python -c 'from annextimelog.token import Noop;print(Noop.FILLERWORDS)'

Listing events:

> atl
> atl ls week
> atl -O json ls -a  # dump all data as JSON
> atl -O timeclock ls -a | hledger -f timeclock:- bal --daily   # analyse with hledger

Removing events by ID:

> atl rm O3YzvZ4m

Syncing:

# add a git remote of your choice
> atl git remote add git@gitlab.com:you/yourrepo
# sync up
> atl sync

Configuration

> atl -c emojis=false ls # no emojis for this one invocation
> atl config emojis false # permanently no emojis
> atl config weekstartssunday true # week begin
> atl config commit false # don't always commit. more speed, but less backup
> atl config fast true # leave out some operations

    """.strip()
    ),
    prog="annextimelog",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "--no-config",
    action="store_true",
    help="Ignore config from git",
)
parser.add_argument(
    "-c",
    dest="extra_config",
    action="append",
    metavar="key=value",
    type=key2value,
    help="Set a temporary config key=value. "
    "If not present, 'annextimelog.' will be prepended to the key.",
    default=[],
)
add_common_arguments(parser)
versiongroup = parser.add_mutually_exclusive_group()
versiongroup.add_argument(
    "--version",
    action="store_true",
    help="show version information and exit",
)
versiongroup.add_argument(
    "--version-only",
    action="store_true",
    help="show only version and exit",
)


subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")
testparser = subparsers.add_parser(
    "test",
    help="run test suite",
    description="Run the test suite",
    formatter_class=argparse.RawTextHelpFormatter,
)
testparser.add_argument(
    "-v",
    "--verbose",
    dest="test_verbosity",
    help="Increase verbosity of test runner. "
    "-v: show test names, "
    "-vv: show raw debug output in all tests, not just failed tests. "
    "(Note that to set the debug level of annextimelog itself, you need to specify 'atl -vvvvv text -vv') ",
    action="count",
    default=1,
)
testparser.set_defaults(func=test_cmd_handler)
gitparser = subparsers.add_parser(
    "git",
    help="Access the underlying git repository",
    add_help=False,
    formatter_class=argparse.RawTextHelpFormatter,
)
gitparser.set_defaults(func=git_cmd_handler)
configparser = subparsers.add_parser(
    "config",
    help="Convenience wrapper around 'atl git config [annextimelog.]key [value], "
    "e.g. 'atl config emojis false' will set the annextimelog.emojis config to false.",
    add_help=False,
    formatter_class=argparse.RawTextHelpFormatter,
)
configparser.set_defaults(func=config_cmd_handler)
syncparser = subparsers.add_parser(
    "sync",
    help="sync data",
    description=textwrap.dedent(
        """
    Sync data with configured remotes by running 'git annex assist'.
    """
    ).strip(),
    aliases=["sy"],
)
add_common_arguments(syncparser)
syncparser.set_defaults(func=sync_cmd_handler)
trackparser = subparsers.add_parser(
    "track",
    help="record a time period",
    description=textwrap.dedent(
        """
    Record a time with metadata.

    Example:

    > atl tr y22  800 work python @GUZ ="annextimelog dev" :"working on cli etc." project=herz project+=co2

    """
    ).strip(),
    aliases=["tr"],
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(trackparser)
trackparser.add_argument(
    "metadata",
    nargs="*",
    help=textwrap.dedent(
        """
    Examples:

        10:00                   10:00 today
        y15:00                  15:00 yesterday
        yy15:00                 15:00 the day before yesterday
        t20:00                  20:00 tomorrow
        tt20:00                 20:00 the day after tomorrow
        2023-12-04T
        justaword               adds tag 'justaword'
        "with space"            (shell-quoted) adds tag "with space"
        field=value             sets metadata field 'field' to (only) 'value'
        field+=value            adds 'value' to metadata field
"""
    ).strip(),
)
trackparser.set_defaults(func=track_cmd_handler)
deleteparser = subparsers.add_parser(
    "delete",
    help="delete an event",
    description=textwrap.dedent(
        """
    Delete an event.

    Example:

    # the following commands would delete event 3QicA4G4
    > atl del 3QicA4G4
    > atl del 3Qi
    > atl del A4

    """
    ).strip(),
    aliases=["del", "rm", "remove"],
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(deleteparser)
deleteparser.add_argument(
    "patterns",
    nargs="+",
    metavar="ID",
    help="case-sensitive glob patterns matching the IDs to delete. "
    "Use 'atl su ...' to find the IDs. "
    "Use 'atl --force del ...' to delete multiple matching events.",
)
deleteparser.set_defaults(func=delete_cmd_handler)
summaryparser = subparsers.add_parser(
    "summary",
    help="show a summary of tracked periods",
    description=textwrap.dedent(
        """
    List a summary of tracked periods

    The format matches the 'atl tr' syntax, e.g.:

    atl ls today # (the default)
    atl ls week
    atl ls month
    atl ls since 10min ago
    atl ls field=REGEX   # field has value matching a regular expression
    atl ls field=REGEX,REGEX,REGEX   # field has value matching any of the given regex
    atl ls @home last week
    ...
    """
    ).strip(),
    aliases=["su", "ls", "list", "find", "search"],
    formatter_class=argparse.RawTextHelpFormatter,
)
add_common_arguments(summaryparser)
summaryparser.add_argument(
    "-a",
    "--all",
    action="store_true",
    help="list all events (unless another time period is given)",
)
summaryparser.add_argument("--match", choices="all any".split(), default="all")
listgroup = summaryparser.add_mutually_exclusive_group()
listgroup.add_argument(
    "--id",
    "--id-only",
    dest="id_only",
    action="store_true",
    help="only print IDs of matched events",
)
listgroup.add_argument("-l", "--long", action="store_true", help="more details")
summaryparser.add_argument("query", nargs="*")
summaryparser.set_defaults(func=summary_cmd_handler)


def cli(args=None):
    args, other_args = parser.parse_known_args(args=args)

    setup_logging(level=logging.INFO - (args.verbose - args.quiet) * 5)

    if not sys.stdin.isatty():
        logger.warning(
            f"annextimelog's cli is not yet stable, be careful relying on it in scripts."
        )

    logger.debug(f"{args = }")
    logger.debug(f"{other_args = }")

    if args.version or args.version_only:
        version = importlib.metadata.version(package := "annextimelog")
        urls = dict(
            re.split(r"\s*,\s*", s, maxsplit=1)
            for s in importlib.metadata.metadata("annextimelog").get_all("project-url")
        )
        author = importlib.metadata.metadata("annextimelog")["Author"]
        logger.warning(
            f"The displayed version {version!r} does not (yet) reflect development commits made after the release, "
            f"if you installed {package} from {urls['Repository']}."
        )
        if args.version_only:
            stdout.out(version)
            sys.exit(0)
        stdout.print(
            textwrap.dedent(
                f"""
                {package} v[b]{version}[/b] - A cli time tracker based on Git Annex
                by [b]{author}[/b] ({urls['Author on Mastodon']})
                Source code: {urls['Repository']}
                Changelog: {urls['Changelog']}
            """
            ).strip("\r\n")
        )
        sys.exit(0)

    if args.repo.exists() and not args.repo.is_dir():
        logger.critical(f"{args.repo} exists but is not a directory.")
        sys.exit(1)

    if args.repo.exists():
        logger.debug(f"{args.repo} exists")
        if repo_root := get_repo_root(args.repo):
            if repo_root.resolve() != args.repo.resolve():
                logger.critical(
                    f"There's something funny with {args.repo}: git says the repo root is {repo_root}. "
                )
                sys.exit(1)
        else:
            logger.critical(f"{args.repo} exists but is no git repository. 🤔")
            sys.exit(1)
    else:
        if not args.repo.parent.exists():
            logger.info(f"📁 Creating {args.repo.parent}")
            args.repo.parent.mkdir(parent=True, exist_ok=True)
        logger.info(f"Making a git repository at {args.repo}")
        result = run(
            subprocess.run, ["git", "init", str(args.repo)], capture_output=True
        )
        if result.returncode:
            logger.error(f"Couldn't make git repository at {args.repo}")
            sys.exit(1)

    # ✅ at this point, args.repo is a git repository

    logger.debug(f"Reading config from repo {args.repo}")
    result = run(subprocess.run, ["git", "-C", args.repo, "config", "--list"])
    args.config = dict()
    for line in result.stdout.splitlines():
        if m := utils.GIT_CONFIG_REGEX.fullmatch(line):
            args.config[m.group("key")] = m.group("value")
    if logger.getEffectiveLevel() < logging.DEBUG - 5:
        logger.debug(f"Read git config:\n{args.config}")
    if args.no_config:
        args.config = {k: v for k, v in args.config.items() if k in ["annex.uuid"]}
    args.config.update(
        {
            re.sub(r"^(annextimelog\.)?", "annextimelog.", k): v
            for k, v in args.extra_config
        }
    )
    if logger.getEffectiveLevel() < logging.DEBUG - 5:
        logger.debug(f"Config:\n{args.config}")

    logger.debug(f"Making sure {args.repo} is a git annex repository")
    if not args.config.get("annex.uuid"):
        logger.debug(f"{args.repo} is not a git annex repository")
        if not (
            result := run(
                subprocess.run,
                ["git", "-C", args.repo, "annex", "init"],
                title=f"add an annex to {args.repo}",
            )
        ).returncode:
            logger.info(f"Added an annex to {args.repo}")
        else:
            logger.critical(f"Couldn't add an annex to {args.repo}")
            sys.exit(1)

    # ✅ at this point, args.repo is a git annex repository

    if args.config.get("annextimelog.commit", "true") == "true":
        if args.subcommand not in ["git"]:
            result = run(
                subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"]
            )
            if result.returncode or result.stdout or result.stderr:
                logger.warning(
                    f"🐛 The repo {args.repo} is not clean. "
                    f"This should not happen. Committing away the following changes:"
                )
                result = run(subprocess.Popen, ["git", "-C", args.repo, "status"])
                with logger.console.status("Committing..."):  # type: ignore[attr-defined]
                    result = run(
                        subprocess.run, ["git", "-C", args.repo, "annex", "add"]
                    )
                    result = run(subprocess.run, ["git", "-C", args.repo, "add", "-A"])
                    result = run(
                        subprocess.run,
                        ["git", "-C", args.repo, "commit", "-m", "🧹 Leftover changes"],
                    )
                result = run(
                    subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"]
                )
                if not (result.returncode or result.stderr):
                    logger.info(f"✅ Repo is now clean")
                else:
                    logger.warning(f"Commiting leftover changes didn't work.")

    # handle the subcommand
    # (when a subcommand is specified, the 'func' default is set to a callback function)
    if not getattr(args, "func", None):
        # default to 'atl summary'
        args.func = summary_cmd_handler
    try:
        args.func(args, other_args)
    finally:
        if (
            args.subcommand not in ["git"]
            and args.config.get("annextimelog.commit", "true") == "true"
        ):
            result = run(
                subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"]
            )
            if result.returncode or result.stdout or result.stderr:
                logger.warning(
                    f"🐛 This command left the repo {args.repo} in an unclean state. "
                    f"This should not happen. Consider investigating. "
                    f"The next time you run any 'annextimelog' command, these changes will be committed."
                )
                result = run(subprocess.Popen, ["git", "-C", args.repo, "status"])


if __name__ == "__main__":
    cli()
