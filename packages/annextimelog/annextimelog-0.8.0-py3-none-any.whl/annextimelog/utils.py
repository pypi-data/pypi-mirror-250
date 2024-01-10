from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
import math
import re
import json
import logging
from datetime import datetime as datetime_, timedelta
from typing import Dict, Union, Literal

# external modules
from rich.text import Text


logger = logging.getLogger(__name__)


GIT_CONFIG_REGEX = re.compile(r"^(?P<key>[^\s=]+)=(?P<value>.*)$", flags=re.IGNORECASE)


def sign(x: Union[float, int]) -> Union[Literal[-1, 1]]:
    return 1 if x >= 0 else -1


class datetime(datetime_):
    FIELDS = "year month day hour minute second microsecond".split()

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


def pretty_duration(seconds):
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


def from_jsonlines(string):
    if hasattr(string, "decode"):
        string = string.decode(errors="ignore")
    string = str(string or "")
    for i, line in enumerate(string.splitlines(), start=1):
        try:
            yield json.loads(line)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.warning(f"line #{i} ({line!r}) is invalid JSON: {e!r}")
            continue
