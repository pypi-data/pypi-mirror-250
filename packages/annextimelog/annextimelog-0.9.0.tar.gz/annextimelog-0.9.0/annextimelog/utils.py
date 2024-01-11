from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
import math
import re
import json
import logging
from typing import Dict, Union, Literal, Sequence, Optional, Any, Iterator, Tuple


# external modules
from rich.text import Text


logger = logging.getLogger(__name__)


def make_it_n(items: Sequence, n: int, filler: Optional[Any] = None) -> Iterator:
    it = iter(items)
    for i in range(n):
        yield next(it, filler)


def make_it_two(items: Sequence, filler: Optional[Any] = None) -> Tuple[Any, Any]:
    it = iter(items)
    return next(it, filler), next(it, filler)


def sign(x: Union[float, int]) -> Union[Literal[-1, 1]]:
    return 1 if x >= 0 else -1


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
