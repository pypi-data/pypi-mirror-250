from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
import math
import re
import json
import logging
from datetime import datetime as datetime_, timedelta
from typing import Dict

# external modules
from rich.text import Text


logger = logging.getLogger(__name__)


GIT_CONFIG_REGEX = re.compile(r"^(?P<key>[^\s=]+)=(?P<value>.*)$", flags=re.IGNORECASE)


class datetime(datetime_):
    FIELDS = "year month day hour minute second microsecond".split()

    def this(self, unit: str, offset: int = 0) -> datetime:
        kwargs: Dict[str, int] = {}
        for field in self.FIELDS[::-1]:
            if field == unit:
                break
            kwargs[field] = 1 if field in {"day", "month"} else 0
        result = self.replace(**kwargs)  # type: ignore[arg-type]
        try:
            span = timedelta(**{f"{unit}s": 1})
        except TypeError:
            if unit in self.FIELDS:
                raise NotImplementedError(f"this({unit!r}) is not yet implemented")
            else:
                raise ValueError(f"{unit!r} is an invalid unit")
        if offset:
            result += offset * span + span / 2
            return result.replace(**kwargs)  # type: ignore[arg-type]
        return result

    def next(self, unit: str, offset: int = 1) -> datetime:
        return self.this(unit, offset=offset)

    def prev(self, unit: str, offset: int = -1) -> datetime:
        return self.this(unit, offset=offset)


def pretty_duration(seconds):
    parts = dict()
    for unit, s in dict(d=24 * 60 * 60, h=60 * 60, m=60, s=1).items():
        parts[unit] = math.floor(seconds / s)
        seconds %= s
    colors = dict(d="green", h="blue", m="red", s="yellow")
    text = Text()
    for u, n in parts.items():
        if n:
            text.append(f"{n:2}").append(u, style=colors[u])
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
