from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
from functools import cached_property
import math
import re
import json
import logging
from datetime import datetime as datetime_, timedelta as timedelta_  # type: ignore[assignment]
from typing import Dict, Union, Literal
from zoneinfo import ZoneInfo

# internal modules
from annextimelog.utils import sign

# external modules
from rich.text import Text


class timedelta(timedelta_):
    @cached_property
    def pretty_duration(self) -> Text:
        seconds = self.total_seconds()
        parts = dict()
        for unit, s in dict(d=24 * 60 * 60, h=60 * 60, m=60, s=1).items():
            parts[unit] = math.floor(seconds / s)
            seconds %= s
        colors = dict(d="green", h="blue", m="red", s="yellow")
        text = Text()
        for u, n in parts.items():
            if n:
                text.append(f"{n}").append(u, style=colors[u])
        return text

    @classmethod
    def ensure(cls, d) -> timedelta:
        return d if isinstance(d, cls) else cls(seconds=d.total_seconds())


class datetime(datetime_):
    FIELDS = "year month day hour minute second microsecond".split()
    WEEKDAYS = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()

    @classmethod
    def ensure(cls, d) -> datetime:
        return (
            d if isinstance(d, cls) else cls(**{f: getattr(d, f) for f in cls.FIELDS})
        )

    def this(self, unit: str, offset: int = 0, weekstartssunday=False) -> datetime:
        match unit:
            case "year":
                span = timedelta(days=367)
                result = self.this("month").replace(month=1)
                for i in range(abs(offset)):
                    result += sign(offset) * span + span / 2
                    result = result.this("month").replace(month=1)
            case "month":
                span = timedelta(days=32)
                result = self.this("day").replace(day=1)
                for i in range(abs(offset)):
                    result += sign(offset) * span + span / 2
                    result = result.this("day").replace(day=1)
            case "week":
                today = self.this("day")
                result = today - timedelta(days=today.weekday())
                if weekstartssunday:
                    result -= timedelta(days=1)
                result += offset * timedelta(days=7)
            case str() as s if s in self.FIELDS:
                kwargs: Dict[str, int] = {}
                for field in self.FIELDS[::-1]:
                    if field == unit:
                        break
                    kwargs[field] = 1 if field in {"day"} else 0
                result = self.replace(**kwargs)  # type: ignore[arg-type]
                span = timedelta(**{f"{unit}s": 1})
                if offset:
                    result += offset * span + span / 2
                    result = result.replace(**kwargs)  # type: ignore[arg-type]
            case str() as given if (
                nth_weekday := next(
                    (
                        i
                        for i, weekday in enumerate(self.WEEKDAYS)
                        if weekday.lower().startswith(given.lower())
                    ),
                    None,
                )
            ) is not None:
                result = self.this("day")
                result += timedelta(days=nth_weekday - self.weekday())
                if weekstartssunday and nth_weekday == 6:
                    result -= timedelta(days=7)
                result += offset * timedelta(days=7)
            case _:
                raise ValueError(f"{unit!r} is an invalid unit")
        return result

    def next(self, unit: str, offset=1, **kwargs) -> datetime:
        offset = abs(offset)
        kwargs["offset"] = offset
        return self.this(unit, **kwargs)

    def prev(self, unit: str, offset=-1, **kwargs) -> datetime:
        offset = -abs(offset)
        kwargs["offset"] = offset
        return self.this(unit, **kwargs)

    def timeformat(self, timezone=ZoneInfo("UTC")) -> str:
        return self.astimezone(timezone).strftime("%Y-%m-%dT%H:%M:%S%z")


# we must override the min and max constants, which are still from the base class otherwise
datetime.min = datetime.ensure(datetime_.min)
datetime.max = datetime.ensure(datetime_.max)
