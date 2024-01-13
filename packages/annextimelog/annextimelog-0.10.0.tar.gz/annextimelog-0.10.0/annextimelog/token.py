from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
import re
import inspect
import itertools
import warnings
import functools
import shlex
import logging
from abc import ABC, abstractmethod
import dataclasses
from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import (
    cast,
    Optional,
    Set,
    Dict,
    Union,
    List,
    Tuple,
    Iterator,
    ClassVar,
    FrozenSet,
)

# internal modules
from annextimelog.datetime import datetime, datetime as dt, timedelta, timedelta as td
from annextimelog.log import stderr


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Token(ABC):
    string: str = field(compare=False, default="", kw_only=True)
    is_condition: Optional[bool] = field(default=None, kw_only=True)

    @property
    def pretty(self) -> str:
        return str(self)

    @property
    def roundtrip(self) -> Union[Token | None]:
        for f in (
            lambda: type(self).from_str(str(self)),
            lambda: Token.from_str(str(self)),
        ):
            if t := f():
                return t
        return None

    @classmethod
    def recursive_subclasses(cls):
        yield cls
        for subcls in cls.__subclasses__():
            yield from subcls.recursive_subclasses()

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[Token, None]:
        """
        Recurse into subclasses and try their from_str() constructors.
        This exact method is inherited if it'string not overwritten (classmethods can't be abstractmethods...)
        """
        for subcls in cls.__subclasses__():
            if from_str := getattr(subcls, "from_str", None):
                try:
                    if token := from_str(string, **kwargs):
                        return token
                except Exception as e:
                    logger.error(
                        f"Calling {from_str}({string!r}) didn't work: {e.__class__.__name__} {e!r}"
                    )
        if cls is Token or str(cls) == str(Token):  # dirty hack: only in base class
            # fall back to just setting a tag
            return AddToField(
                string=string, field="tag", values=frozenset([string]), **kwargs
            )
        return None

    @staticmethod
    def join(tokens: Sequence[Token]) -> str:
        return shlex.join(t.string for t in tokens)

    @classmethod
    def reduce(
        cls,
        tokens: Sequence[Union[Token | None]],
        config: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Iterator[Token]:
        """
        Given a sequence of tokens, reduce it down by iteratively/recursively
        translate parts of it and dropping irrelevant elements.

        Args:
            tokens: the tokens
            config: the annextimelog git config dict
            **kwargs: further target attributes for Tokens, e.g. is_condition=...

        Steps:
            - sort into conditions and actions, recurse into those
            - sort into time-related tokens and the rest
            - recurse into time-related tokens to reduce into a single TimeFrame
        """
        config = config or dict()
        conf = dict(config=config)
        is_condition = kwargs.get("is_condition", None)
        cond = dict(is_condition=is_condition)

        ### Preparation: consume all tokens into list and irrelevant ones ###
        tokens_: List[Token] = []
        for token in tokens:
            match token:
                case None | Noop():
                    logger.debug(f"Ignoring token {token!r}")
                case _:
                    tokens_.append(token)
        tokens = tokens_
        tokenstr = shlex.join(t.string for t in tokens)

        if not tokens:
            logger.debug(f"No tokens left, we're done.")
            return

        if logger.getEffectiveLevel() < logging.DEBUG:
            frame = inspect.currentframe()
            recursion_level = (
                len(
                    [f for f in inspect.getouterframes(frame) if f.function == "reduce"]
                )
                - 1
            )
            logger.debug(
                f"Attempting reduce({is_condition=}) ({recursion_level=}) of {len(tokens)} tokens {tokenstr!r} 👇"
            )
            stderr.log(tokens)

        def reduce_fail_msg(tokens=tokens):
            return (
                f"Don't know how to interpret or reduce time-related tokens {shlex.join(t.string for t in tokens)!r} ({'·'.join(t.__class__.__name__ for t in tokens)}). "
                f"If you think this combination does makes sense, consider opening an issue (https://gitlab.com/nobodyinperson/annextimelog/-/issues/new) to discuss."
            )

        ### Step 1: Separate actions from conditions ###
        if None in (conds := set(t.is_condition for t in tokens)) or len(conds) > 1:
            next_is_condition: Optional[bool] = is_condition
            if next_is_condition is not None:
                logger.debug(
                    f"Because {is_condition=}, the following will be {'conditions' if is_condition else 'actions'}"
                )
            actions: List[Token] = []
            conditions: List[Token] = []
            unknown: List[Token] = []
            for token in tokens:
                match token:
                    case ActionFollowingKeyword() | ConditionFollowingKeyword():
                        match token:
                            case ActionFollowingKeyword():
                                logger.debug(
                                    f"{token.string!r} means the following are actions"
                                )
                                next_is_condition_ = False
                            case ConditionFollowingKeyword():
                                logger.debug(
                                    f"{token.string!r} means the following are conditions"
                                )
                                next_is_condition_ = True
                        if next_is_condition == next_is_condition_:
                            logger.debug(
                                f"superfluous {token.string!r} (in {tokenstr!r}): "
                                f"already in {'condition' if is_condition else 'action'}"
                            )
                        next_is_condition = next_is_condition_
                        if (
                            is_condition is not None
                            and is_condition != next_is_condition
                        ):
                            raise ValueError(
                                f"Can't have {str(token)!r} (in {tokenstr!r}) "
                                f"when reducing to {'condition' if is_condition else 'action'}"
                            )
                        continue
                token = token.evolve(is_condition=next_is_condition)
                match next_is_condition:
                    case True:
                        logger.debug(f"{token.string!r} is a condition")
                        conditions.append(token)
                    case False:
                        logger.debug(f"{token.string!r} is an action")
                        actions.append(token)
                    case _:
                        logger.debug(
                            f"Don't know (yet) whether {token.string!r} is action or condition"
                        )
                        unknown.append(token)
            if unknown:
                match bool(actions), bool(conditions):
                    case True, False:
                        logger.debug(
                            f"These previously unknown tokens {unknown} are conditions"
                        )
                        conditions.extend(t.evolve(is_condition=True) for t in unknown)
                    case False, True:
                        logger.debug(
                            f"These previously unknown tokens {unknown} are actions"
                        )
                        actions.extend(t.evolve(is_condition=False) for t in unknown)
                    case _ if is_condition is True:
                        logger.debug(
                            f"Assuming the unknown tokens {unknown} to be conditions, because {is_condition=}"
                        )
                        conditions.extend(t.evolve(is_condition=False) for t in unknown)
                    case _ if is_condition is False:
                        logger.debug(
                            f"Assuming the unknown tokens {unknown} to be actions, because {is_condition=}"
                        )
                        actions.extend(t.evolve(is_condition=False) for t in unknown)
                    case _:
                        raise ValueError(
                            f"Don't know whether unknown tokens {unknown} are actions or conditions. "
                            "Specify is_condition=True|False."
                        )
            logger.debug(
                f"Found {len(conditions)} {conditions = } and {len(actions)} {actions = }"
            )
            if actions:
                logger.debug(
                    f"Reducing {len(actions)} actions {shlex.join(t.string for t in actions)!r}"
                )
                yield from cls.reduce(actions, **conf, is_condition=False)
            if conditions:
                logger.debug(
                    f"Reducing {len(conditions)} conditions {shlex.join(t.string for t in conditions)!r}"
                )
                yield from cls.reduce(conditions, **conf, is_condition=True)
            return

        ### no token is time-related, nothing more to do here
        if not any(isinstance(t, TimeToken) for t in tokens):
            logger.debug(
                f"None of the {len(tokens)} tokens {tokenstr!r} are time-related, so we're done!"
            )
            yield from tokens
            return

        ### all tokens are time-related, convert them to a TimeFrame
        if all(isinstance(t, TimeToken) for t in tokens):
            logger.debug(
                f"All {len(tokens)} tokens are time-related, converting them to a TimeFrame"
            )
            ss = dict(string=(s := tokenstr), **kwargs)
            now = dt.now()
            wss = dict(
                weekstartssunday=config.get(
                    "annextimelog.weekstartssunday", "false"
                ).lower()
                == "true"
            )
            # interpret the time-related tokens
            match tokens:  # this is where the magic happens 🪄
                # these can't be simplified
                case [TimeFrame()] | [Time()]:
                    yield from tokens
                case [  # DURATION ago
                    Duration() as d,
                    TimeKeyword(name="ago"),
                ]:
                    yield Time(now - d.duration, **ss)
                case [  # in DURATION
                    TimeKeyword(name="in"),
                    Duration() as d,
                ]:
                    yield Time(now + d.duration, **ss)
                case [  # since TIME
                    TimeKeywordSince(),
                    Time() as t,
                ] | [  # TIME until
                    Time() as t,
                    TimeKeywordUntil(),
                ]:
                    yield TimeFrame(start=t.time, **ss)
                case [  # until TIME
                    TimeKeywordUntil(),
                    Time() as t,
                ]:
                    yield TimeFrame(end=t.time, **ss)
                case [Time() as t1, Time() as t2] | [  # TIME TIME
                    # TIME until TIME
                    Time() as t1,
                    TimeKeywordUntil(),
                    Time() as t2,
                ] | [
                    # since TIME until TIME
                    TimeKeywordSince(),
                    Time() as t1,
                    TimeKeywordUntil(),
                    Time() as t2,
                ]:
                    yield TimeFrame(start=t1.time, end=t2.time, **ss)
                case [  # since DURATION ago
                    TimeKeywordSince(),
                    Duration() as d,
                    TimeKeyword(name="ago"),
                ]:
                    yield TimeFrame(start=now - d.duration, **ss)
                case [  # last 2h, next 10min
                    TimeKeywordIter() as w,
                    Duration() as d,
                ]:
                    yield TimeFrame(
                        start=now + w.n * d.duration,
                        end=now + (w.n + 1) * d.duration,
                        **ss,
                    )
                case [  # until today
                    TimeKeywordUntil(),
                    TimeKeywordPeriod() as p,
                ]:  # until today
                    # TODO: or p.start? what does 'until tomorrow' mean? including tomorrow?
                    yield TimeFrame(end=p.end, **ss)
                case [  # since yesterday
                    TimeKeywordSince(),
                    TimeKeywordPeriod() as p,
                ]:  # until today
                    yield TimeFrame(start=p.start, **ss)
                case [  # until last week
                    TimeKeywordUntil(),
                    TimeKeywordIter() as w,
                    TimeKeywordUnit() as u,
                ]:
                    # TODO: +1 or not? Does 'until this week' include this week?
                    yield TimeFrame(end=now.this(u.name, offset=w.n + 1, **wss), **ss)
                case [  # since this week
                    TimeKeywordSince(),
                    TimeKeywordIter() as w,
                    TimeKeywordUnit() as u,
                ]:
                    yield TimeFrame(start=now.this(u.name, offset=w.n, **wss), **ss)
                case [  # month, week, hour, etc...
                    TimeKeywordUnit()
                ] | [  # last month, this week, next hour, etc.
                    TimeKeywordIter(),
                    TimeKeywordUnit(),
                ]:
                    match tokens:
                        case [TimeKeywordUnit() as u]:
                            unit, n = u, 0
                        case [TimeKeywordIter() as w, TimeKeywordUnit() as u]:
                            unit, n = u, w.n
                    yield TimeFrame(
                        start=now.this(unit.name, n, **wss),
                        end=now.this(unit.name, n + 1, **wss),
                        **ss,
                    )
                case [  # until DURATION ago
                    TimeKeywordUntil(),
                    Duration() as d,
                    TimeKeyword(name="ago"),
                ]:
                    yield TimeFrame(end=now - d.duration, **ss)
                case [  # TIME until DURATION ago
                    Time() as t,
                    TimeKeywordUntil(),
                    Duration() as d,
                    TimeKeyword(name="ago"),
                ]:
                    yield TimeFrame(start=t.time, end=now - d.duration, **ss)
                case [
                    # DURATION ago until TIME
                    Duration() as d,
                    TimeKeyword(name="ago"),
                    TimeKeywordUntil(),
                    Time() as t,
                ]:
                    yield TimeFrame(start=now - d.duration, end=t.time, **ss)
                case [
                    # DURATION ago until DURATION ago
                    Duration() as d1,
                    TimeKeyword(name="ago"),
                    TimeKeywordUntil(),
                    Duration() as d2,
                    TimeKeyword(name="ago"),
                ]:
                    yield TimeFrame(
                        start=now - d1.duration, end=now - d2.duration, **ss
                    )
                case [Duration() as d] | [  # DURATION
                    # since DURATION
                    TimeKeywordSince() | TimeKeyword(name="for"),
                    Duration() as d,
                ]:
                    now = now  # mypy doesn't like walrus below 🤷
                    yield TimeFrame(end=now, start=now - d.duration, **ss)
                case [  # DURATION since TIME
                    Duration() as d,
                    TimeKeywordSince(),
                    Time() as t,
                ]:
                    yield TimeFrame(start=t.time, end=t.time + d.duration, **ss)
                case [  # DURATION until TIME
                    Duration() as d,
                    TimeKeywordUntil(),
                    Time() as t,
                ]:
                    yield TimeFrame(start=t.time - d.duration, end=t.time, **ss)
                case [  # DURATION since DURATION ago
                    Duration() as d1,
                    TimeKeywordSince(),
                    Duration() as d2,
                    TimeKeyword(name="ago"),
                ]:
                    yield TimeFrame(
                        start=(t_ := now - d2.duration), end=t_ + d1.duration, **ss
                    )
                case [  # DURATION until DURATION ago
                    Duration() as d1,
                    TimeKeywordUntil(),
                    Duration() as d2,
                    TimeKeyword(name="ago"),
                ]:
                    yield TimeFrame(
                        end=(t_ := now - d2.duration), start=t_ - d1.duration, **ss
                    )
                case [  # this Monday
                    TimeKeywordIter() as i,
                    TimeKeywordDay() as day,
                ]:
                    yield TimeFrame(
                        start=now.this(day.name, offset=i.n, **wss),
                        end=now.this(day.name, offset=i.n, **wss) + td(days=1),
                        **ss,
                    )
                case [TimeKeywordSince(), TimeKeywordDay() as day]:  # since Monday
                    t_ = day.start(**wss)
                    if t_ > now:
                        t_ -= timedelta(days=7)
                    yield TimeFrame(start=t_, **ss)
                case [TimeKeywordUntil(), TimeKeywordDay() as day]:  # until Monday
                    t_ = day.end(**wss)
                    if t_ < now:
                        t_ += timedelta(days=7)
                    yield TimeFrame(end=t_, **ss)
                case [  # since last Monday
                    TimeKeywordSince(),
                    TimeKeywordIter() as i,
                    TimeKeywordDay() as day,
                ]:
                    yield TimeFrame(string=s, start=day.start(offset=i.n, **wss))
                case [  # until next Friday
                    TimeKeywordUntil(),
                    TimeKeywordIter() as i,
                    TimeKeywordDay() as day,
                ]:
                    yield TimeFrame(end=day.end(offset=i.n, **wss), **ss)
                case [
                    TimeKeywordDay() as d1,
                    TimeKeywordDay() as d2,
                ] | [
                    TimeKeywordDay() as d1,
                    TimeKeywordUntil(),
                    TimeKeywordDay() as d2,
                ]:  # Mo - Fr
                    t1_, t2_ = d1.start(**wss), d2.end(**wss)
                    if t2_ <= t1_:
                        t2_ += timedelta(days=7)
                    if t1_ > now and t2_ > now:
                        t1_ -= timedelta(days=7)
                        t2_ -= timedelta(days=7)
                    yield TimeFrame(start=t1_, end=t2_, **ss)
                # TODO: last Tuesday until next Friday
                case [TimeKeywordDay() as day]:  # Monday Tueday Wed Fri ...
                    yield TimeFrame(start=day.start(**wss), end=day.end(**wss), **ss)
                case [TimeKeywordPeriod() as w]:
                    yield TimeFrame(start=w.start, end=w.end, **ss)
                case _:
                    logger.debug(msg := reduce_fail_msg(tokens))
                    raise ValueError(msg)
            return
        else:  ### separation into time-related tokens and other tokens needed ###
            timetokens: List[TimeToken] = []
            othertokens: List[Token] = []
            # sort out the time-related tokens
            for token in tokens:
                match token:
                    case TimeToken():
                        if logger.getEffectiveLevel() < logging.DEBUG:
                            logger.debug(f"{token!r} is a TimeToken")
                        timetokens.append(token)
                    case _:
                        if logger.getEffectiveLevel() < logging.DEBUG:
                            logger.debug(f"{token!r} is NOT a TimeToken")
                        othertokens.append(token)
            logger.debug(
                f"{tokenstr!r} is split into {len(timetokens)} time-related tokens {timetokens} "
                f"and {len(othertokens)} other tokens {othertokens}"
            )
            if timetokens:
                yield from cls.reduce(timetokens, **conf, **kwargs)
            yield from othertokens

    @classmethod
    def from_strings(
        cls,
        strings: Union[str | Sequence[str]],
        reduce: bool = True,
        config: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Sequence[Union[Token | None]]:
        match strings:
            case str():
                strings = (s := shlex.split(strings))
                logger.debug(f"from_strings({strings!r}): split into {strings}")
        tokens = [cls.from_str(s) for s in strings]
        if reduce:
            tokens = list(cls.reduce(tokens, config=config, **kwargs))
        elif kwargs:
            warnings.warn("from_strings(): unused {kwargs = } with {reduce = }")
        return tokens

    def evolve(self, **kwargs) -> Token:
        return dataclasses.replace(self, **kwargs)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @staticmethod
    def recurse_into_subclasses(decorated_fun):
        @classmethod
        @functools.wraps(decorated_fun)
        def wrapper(cls, *args, **kwargs):
            for subcls in cls.__subclasses__():
                if method := getattr(subcls, decorated_fun.__name__, None):
                    if token := method(*args, **kwargs):
                        return token
            return decorated_fun(cls, *args, **kwargs)

        return wrapper


@dataclass(frozen=True)
class Noop(Token):
    FILLERWORDS = set(
        sorted(
            """
        the about beside near to above between of towards across beyond off under after by
        on underneath against despite onto unlike along down opposite among
        during out up around except outside upon as over via at from past with before
        round within behind inside without below into than beneath like through
        """.split()
        )
    )

    @property
    def pretty(self) -> str:
        return f"{self.string!r}: do nothing"

    @Token.recurse_into_subclasses
    def from_str(cls, string: str, **kwargs) -> Union[Token, None]:
        if re.fullmatch(r"\s*", string) or string.lower() in cls.FILLERWORDS:
            return cls(string=string, **kwargs)  # type: ignore[operator]
        return None

    def __str__(self) -> str:
        return ""


@dataclass(frozen=True)
class ConditionCombinationKeyword(Noop):
    KEYWORDS = "and or not".split()

    @classmethod
    def from_str(
        cls, string: str, **kwargs
    ) -> Union[ConditionCombinationKeyword, None]:
        if string.lower() in cls.KEYWORDS:
            logger.warning(
                f"{string!r} does not actually alter how conditions are met or actions are performed (yet! Maybe it will in a future release...)"
            )
            return cls(string=string, **kwargs)
        return None

    def __str__(self) -> str:
        return self.string


@dataclass(frozen=True)
class ConditionFollowingKeyword(Token):
    KEYWORDS = "where while if but although despite when given".split()

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[ConditionFollowingKeyword, None]:
        if string.lower() in cls.KEYWORDS:
            return cls(string=string, **kwargs)
        return None

    def __str__(self) -> str:
        return self.string


@dataclass(frozen=True)
class ActionFollowingKeyword(Token):
    KEYWORDS = "do then set change modify mod edit update".split()

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[ActionFollowingKeyword, None]:
        if string.lower() in cls.KEYWORDS:
            return cls(string=string, **kwargs)
        return None

    def __str__(self) -> str:
        return self.string


@dataclass(frozen=True)
class TimeToken(Token):
    pass


@dataclass(frozen=True)
class TimeKeyword(TimeToken):
    name: str
    KEYWORDS: ClassVar = set("ago for in".split())

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeKeyword, None]:
        for subcls in cls.__subclasses__():
            if token := subcls.from_str(string, **kwargs):
                return token
        if string.lower() in cls.KEYWORDS:
            return cls(string=string, name=string, **kwargs)
        return None

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class TimeKeywordIter(TimeKeyword):
    KEYWORDS: ClassVar = {
        "this": 0,
        "next": 1,
        "coming": 1,
        "following": 1,
        "last": -1,
        "prev": -1,
        "previous": -1,
    }

    @property
    def n(self) -> int:
        return self.KEYWORDS.get(self.name, 0)


@dataclass(frozen=True)
class TimeKeywordUnit(TimeKeyword):
    KEYWORDS: ClassVar = set("second minute hour day week month year".split())

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeKeywordUnit, None]:
        for kw in cls.KEYWORDS:
            if string.lower() in {kw, f"{kw}s"} or (
                kw in "second minute month"
                and len(string) >= 3
                and kw.startswith(string)
            ):
                return cls(string=string, name=kw, **kwargs)
        return None


@dataclass(frozen=True)
class TimeKeywordPeriod(TimeKeyword):
    KEYWORDS: ClassVar = {"today": 0, "yesterday": -1, "tomorrow": 1}

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeKeywordPeriod, None]:
        for kw in cls.KEYWORDS:
            if string.lower() == kw or (
                len(string) >= 3 and kw.startswith(string.lower())
            ):
                return cls(string=string, name=kw, **kwargs)
        return None

    @property
    def n(self) -> int:
        return self.KEYWORDS.get(self.name, 0)

    @property
    def start(self) -> datetime:
        return dt.now().this("day", offset=self.KEYWORDS.get(self.name, 0))

    @property
    def end(self) -> datetime:
        return dt.now().this("day", offset=self.KEYWORDS.get(self.name, 0) + 1)


@dataclass(frozen=True)
class TimeKeywordDay(TimeKeyword):
    # TODO: Can't use datetime.WEEKDAYS for some reason!?
    KEYWORDS: ClassVar = (
        "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
    )

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeKeywordDay, None]:
        for kw in cls.KEYWORDS:
            if (
                string.lower() == kw.lower()  # monday tuesday wednesday ...
                # mon tues thursd fr ...
                or (len(string) >= 2 and kw.lower().startswith(string.lower()))
            ):
                return cls(string=string, name=kw, **kwargs)
        return None

    def start(self, **kwargs) -> datetime:
        return dt.now().this(self.name, **kwargs)

    def end(self, **kwargs) -> datetime:
        return self.start(**kwargs) + timedelta(days=1)


@dataclass(frozen=True)
class TimeKeywordUntil(TimeKeyword):
    KEYWORDS = set("until til till to -".split())


@dataclass(frozen=True)
class TimeKeywordSince(TimeKeyword):
    KEYWORDS = set("since starting from".split())


@dataclass(frozen=True)
class Time(TimeToken):
    """
    A specification of a point in time, such as:

        10     # 10:00 today
        y10    # yesterday 10:00
        yy10   # day before yesterday 10:00
        t10    # tomorrow 10:00
        tt10   # day after tomorrow 10:00
        1500   # 15:00 today
        2023-12-30T13:13:40+0200    # full ISO format
        13:13:40 # partial full ISO format
        ...
    """

    time: datetime

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[Time, None]:
        if string is None:
            return None
        offset = timedelta(days=0)
        if m := re.search(r"^(?P<prefix>[yt]+)(?P<rest>.*)$", string):
            offset = timedelta(
                days=sum(dict(y=-1, t=1).get(c, 0) for c in m.group("prefix"))
            )
            if string := m.group("rest"):
                pass
                # logger.debug(
                #     f"{string!r} starts with {m.group('prefix')!r}, so thats as an {offset = }"
                # )
            else:
                logger.debug(f"{string!r} means an {offset = } from today")
                return cls(
                    string=string,
                    time=dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    + offset,
                    **kwargs,
                )
        if re.fullmatch(r"\d{3}", string):
            # prepend zero to '100', otherwise interpreted as 10:00
            string = f"0{string}"
        result = None
        todaystr = dt.now().strftime(todayfmt := "%Y-%m-%d")
        for i, f in enumerate(
            (
                lambda s: dt.now() if s == "now" else None,
                dt.fromisoformat,
                lambda s: dt.strptime(s, "%Y-%m"),
                lambda s: dt.strptime(s, "%Y/%m"),
                lambda s: dt.fromisoformat(f"{todaystr} {s}"),
                # Python<3.11 fromisoformat is limited, we implement the basic formats here
                # so we need to do it manually...
                lambda s: dt.strptime(s, "%Y-%m-%d %H:%M:%S"),
                lambda s: dt.strptime(s, "%Y-%m-%dT%H:%M:%S"),
                lambda s: dt.strptime(s, "%Y-%m-%dT%H:%M:%S%z"),
                lambda s: dt.strptime(s, "%Y-%m-%d %H:%M:%S%z"),
                lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H%M"),
                lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H"),
                lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H:%M"),
                lambda s: dt.strptime(s, "%Y-%m-%d %H%M"),
            )
        ):
            try:
                if result := f(string):
                    break
            except Exception as e:
                pass
        if not result:
            return None
        result += offset
        return Time(string=string, time=result)

    def __str__(self) -> str:
        return self.time.strftime("%Y-%m-%dT%H:%M:%S%z")


@dataclass(frozen=True)
class TimeStart(Time):
    def __str__(self):
        return f"start={self.time.isoformat()}"


@dataclass(frozen=True)
class TimeEnd(Time):
    def __str__(self):
        return f"end={self.time.isoformat()}"


@dataclass(frozen=True)
class TimeFrame(TimeToken):
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[TimeFrame, None]:
        if m := re.fullmatch(r"[({\[](?P<start>.*);(?P<end>.*)[)}\]]", string.strip()):
            if not (start := Time.from_str(s := m.group("start"))) and s:
                return None
            if not (end := Time.from_str(s := m.group("end"))) and s:
                return None
            return cls(
                string=string,
                start=getattr(start, "time", None),
                end=getattr(end, "time", None),
                **kwargs,
            )
        return None

    def __str__(self):
        return f"[{';'.join((t.isoformat() if t else '') for t in (self.start, self.end))}]"


@dataclass(frozen=True)
class Duration(TimeToken):
    """
    A duration specified in the following format:

        10min
        2h30m
        1week2days3hours4minutes5seconds
        1w2d3h4m5s
        ...
    """

    duration: timedelta

    UNITS = ["weeks", "days", "hours", "minutes", "seconds"]

    @classmethod
    def from_str(cls, string: str, **kwargs) -> Union[Duration, None]:
        durations: List[timedelta] = []
        matches: int = 0
        s = string
        while s:
            if m := re.match(
                rf"[^\da-z]*(?P<number>\d+)[^\da-z]*(?P<unit>[a-z]+)[^\da-z]*",
                s,
                flags=re.IGNORECASE,
            ):
                number, unit = m.groups()
                if kwarg := next(
                    (u for u in cls.UNITS if u.startswith(unit.lower())), None
                ):
                    durations.append(timedelta(**{kwarg: int(number)}))
                s = s[m.span()[-1] :]  # drop this match and go on
                continue
            else:
                return None
        if not durations:
            return None
        return cls(string=string, duration=sum(durations, start=timedelta(0)), **kwargs)

    def __str__(self) -> str:
        parts: List[Tuple[int, str]] = []
        duration = self.duration
        for unit in sorted(self.UNITS, key=lambda u: timedelta(**{u: 1}), reverse=True):
            unitdelta = timedelta(**{unit: 1})
            if abs(duration) < abs(unitdelta):
                continue
            unitblocks = duration // unitdelta
            parts.append((unitblocks, unit))
            duration -= unitblocks * unitdelta  # type: ignore[assignment]
        return "".join(f"{n}{u[0]}" for n, u in parts if n)


@dataclass(frozen=True)
class FieldModifier(Token):
    """
    A metadata field modifier such as:

        field=value          # set 'field' to (only) 'value'
        field+=value         # add 'value' to 'field'
        field=bla,bli,blubb  # set 'field' to given three values
        field+=bla,bli,blubb # add multiple values to 'field'
        field-=value         # remove 'value' from 'field'
        field-=bla,bli,blubb # remove multiple values from 'field'
        field+/=a,b,c/d,e,f  # different separator (this adds 'a,b,c' and 'd,e,f' to 'field')
    """

    field: str

    # don't want to put too many in here, syntax might be needed later
    SEPARATORS = ",;:"

    @classmethod
    def from_str(
        cls, string: str, **kwargs
    ) -> Union[FieldModifier, TimeStart, TimeEnd, Noop, None]:
        # short form
        if m := re.search(r"^(?P<symbol>[@:=])(?P<value>.*)$", string.strip()):
            field = {"@": "location", ":": "note", "=": "title"}.get(
                m.group("symbol"), ""
            )
            kwargs = dict(
                string=string, field=field, values=set([m.group("value")]), **kwargs
            )
            match field:
                case "location":
                    return AddToField(**kwargs)
                case _:
                    return SetField(**kwargs)
        # long form
        if m := re.search(
            rf"(?P<field>\S+?)(?P<operator>[+-]?)(?P<sep>[{cls.SEPARATORS}]?)=(?P<values>.*)",
            string,
        ):
            field, operator, sep, values = m.groups()
            sep = sep or ","
            cast(List[str], values)  # make mypy happy
            values = list(filter(bool, re.split(rf"(?:{re.escape(sep)})+", values)))
            match field.lower():
                case "start" | "end" as field_:
                    # start='in 10min', separated by whitespace, not comma like other fields
                    values = shlex.split(m.group("values"))
                    if operator in "-+".split():
                        logger.warning(
                            f"Ignoring {operator = !r} in {string} (start and end field are special)"
                        )
                        operator = ""
                    try:
                        timetokens: List[TimeToken] = []
                        othertokens: List[Token] = []
                        logger.debug(
                            f"{string!r}: Determining what {field_} time {shlex.join(values)!r} means"
                        )
                        for token in Token.from_strings(
                            list(values), is_condition=False
                        ):
                            match token:
                                case TimeToken():
                                    timetokens.append(token)
                                case t if t:
                                    othertokens.append(token)
                                    logger.warning(
                                        f"While parsing {values} (from {string!r}): Ignoring {token.string!r} as it is not time-related"
                                    )
                    except ValueError as e:
                        raise ValueError(
                            f"While parsing {values} (from {string!r}): {e}"
                        )
                    time: Optional[datetime] = None
                    match timetokens:
                        case [Time(time=time_)]:
                            time = time_
                        case [TimeFrame(start=start, end=end)]:
                            match field_:
                                case "start":
                                    time = start or end
                                case "end":
                                    time = end or start
                    if not time:
                        raise ValueError(
                            f"{values} (from {string!r}) doesn't parse to an interpretable time "
                            f"(but to {timetokens} and ignored elements {othertokens})"
                        )
                    match field_:
                        case "start":
                            return TimeStart(string=string, time=time)
                        case "end":
                            return TimeEnd(string=string, time=time)
                case "tags":  # git annex uses field 'tag' for tags, for convenience adjust it here
                    field = "tag"
                # aliases for the location field
                case str() as f if "location".startswith(
                    f
                ) or f in "at in where".split():
                    field = "location"
            values = cast(FrozenSet[str], frozenset(values))
            match operator:
                case "+":
                    return AddToField(string=string, field=field, values=values)
                case "-":
                    return RemoveFromField(string=string, field=field, values=values)
                case _ if values:
                    return SetField(string=string, field=field, values=values)
                case _:
                    return UnsetField(string=string, field=field)
        return None


@dataclass(frozen=True)
class FieldValueModifier(FieldModifier):
    values: FrozenSet[str]

    def __post_init__(self):
        object.__setattr__(self, "values", frozenset(self.values))

    @property
    def separator(self) -> Union[str, None]:
        for sep in self.SEPARATORS:
            if not any(sep in v for v in self.values):
                return sep
        return None

    @property
    def values_joined(self) -> Tuple[str, str]:
        if sep := self.separator:
            return sep, sep.join(map(str.strip, self.values))
        else:
            it = iter(self.SEPARATORS)
            sep, repl = (next(it, "") for i in range(2))
            logger.warning(
                f"Don't know what separator to use for the values in {self!r}. "
                f"None of {self.SEPARATORS!r} is safe to use they're all present in the values and we don't have an escaping mechanism. "
                f"Falling back to {sep!r} and replacing all its occurrences with {repl!r}."
            )
            return sep, sep.join(v.replace(sep, repl).strip() for v in self.values)


@dataclass(frozen=True)
class UnsetField(FieldModifier):
    def __str__(self) -> str:
        return f"{self.field}="


@dataclass(frozen=True)
class SetField(FieldValueModifier):
    def __str__(self) -> str:
        sep, joined = self.values_joined
        return f"{self.field}{sep if sep != ',' else ''}={joined}"


@dataclass(frozen=True)
class AddToField(FieldValueModifier):
    def __str__(self):
        if (
            len(self.values) == 1
            and self.field.lower() in ["tag", "tags"]
            and isinstance(Token.from_str(value := next(iter(self.values))), AddToField)
        ):
            # shortcut for tags that are not interpreted as another token
            return f"{value}"
        else:
            sep, joined = self.values_joined
            return f"{self.field}+{sep if sep != ',' else ''}={joined}"


@dataclass(frozen=True)
class RemoveFromField(FieldValueModifier):
    def __str__(self) -> str:
        sep, joined = self.values_joined
        return f"{self.field}-{sep if sep != ',' else ''}={joined}"
