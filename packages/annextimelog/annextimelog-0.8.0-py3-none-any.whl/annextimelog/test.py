# system modules
import logging
import itertools
import unittest
import shlex
from datetime import timedelta as td, timedelta
from unittest import TestCase

# internal modules
from annextimelog.event import Event
from annextimelog.token import *
from annextimelog.utils import datetime, datetime as dt

logger = logging.getLogger(__name__)


def today(**kwargs):
    return dt.now().replace(
        **{**dict(hour=0, minute=0, second=0, microsecond=0), **kwargs}
    )


def days(n):
    return timedelta(days=n)


class DatetimeTest(TestCase):
    WEEKDAYS: Dict[Union[int, str], Union[int, str]] = dict(
        zip("Mon Tue Wed Thu Fri Sat Sun".split(), itertools.count(0))
    )
    WEEKDAYS.update({v: k for k, v in WEEKDAYS.items()})

    def test_this(self):
        for parts in [
            "2023-12-04T10:30  hour 2023-12-04T09:00 2023-12-04T10:00 2023-12-04T11:00",
            "2024-01-01T00:15   day 2023-12-31T00:00 2024-01-01T00:00 2024-01-02T00:00",
            "2025-02-15T15:34  week 2025-02-03T00:00 2025-02-10T00:00 2025-02-17T00:00",
            "2024-05-18T22:52 month 2024-04-01T00:00 2024-05-01T00:00 2024-06-01T00:00",
            "2024-05-18T22:52  year 2023-01-01T00:00 2024-01-01T00:00 2025-01-01T00:00",
        ]:
            d, u, p, t, n = parts.split()
            d = dt.fromisoformat(d)
            for m, s in dict(prev=p, this=t, next=n).items():
                with self.subTest(desc := f"{d!r}.{m}({u!r})"):
                    self.assertEqual(
                        (r := getattr(d, m)(u)),
                        dt.fromisoformat(s),
                        f"{desc} should be {s}, but is {r}",
                    )
                if u in {"week"}:
                    for weekstartssunday in {True, False}:
                        with self.subTest(
                            desc := f"{d!r}.{m}({u!r},{weekstartssunday = })"
                        ):
                            self.assertEqual(
                                (
                                    r := d.this(
                                        u, weekstartssunday=weekstartssunday
                                    ).weekday()
                                ),
                                self.WEEKDAYS[
                                    day := "Sun" if weekstartssunday else "Mon"
                                ],
                                f"{desc} should be a {day} but is a {self.WEEKDAYS[r]}",
                            )


class TokenTest(TestCase):
    def test_fieldmodifier(self):
        for s, r in {
            "a": AddToField("", "tag", {"a"}),
            "tag+=until": AddToField("", "tag", {"until"}),
            "tag+=a,b,c": AddToField("", "tag", {"a", "b", "c"}),
            "tags+=a,b,c": AddToField("", "tag", {"a", "b", "c"}),
            "tags-=a,b,c": RemoveFromField("", "tag", {"a", "b", "c"}),
            "tags=a,b,c": SetField("", "tag", {"a", "b", "c"}),
            "tags=": UnsetField("", "tag"),
            "field=": UnsetField("", "field"),
            "@home": SetField("", "location", {"home"}),
            "id=bla": Noop(""),
            "id-=bla": Noop(""),
            "id+=bla": Noop(""),
            "id=": Noop(""),
        }.items():
            with self.subTest(string=s):
                self.assertEqual(Token.from_str(s), r)

    def test_fieldmodifier_multiple(self):
        self.assertNotEqual(
            SetField.from_str(str(t := SetField("", "f", set(SetField.SEPARATORS)))),
            t,
            msg="when values contain all separators, stringification shouldn't round-trip, but here it does!?",
        )

    def test_duration(self):
        for s, kw in {
            "10m": dict(minutes=10),
            "10m+2h": dict(minutes=10, hours=2),
            "2h 10m": dict(minutes=10, hours=2),
            "2h30m": dict(hours=2, minutes=30),
            "   1   w   2  days 3 hour  4 min 5 sec": dict(
                weeks=1, days=2, hours=3, minutes=4, seconds=5
            ),
        }.items():
            with self.subTest(string=s):
                self.assertEqual(
                    Token.from_str(s), Duration(string=s, duration=timedelta(**kw))
                )

    def test_from_string_roundtrip(self):
        for s in [
            "10:00",
            "until",
            "bla",
            "10min",
            "10m2h",
            "field=value",
            "field+=value",
            "field=",
            "field-=value",
            "tag+=until",
            "tag+=until,bla",
            "field+;=10:00;yesterday",
            "start=10:00",
            "end=10:00",
            "[;]",
            "[10:00;]",
            "[;10:30]",
            "[8;10]",
            "",
        ]:
            with self.subTest(string=s):
                token = Token.from_str(s)
                self.assertEqual(token.roundtrip, token)

    def test_from_strings(self):
        for input, (start, end) in {
            "10min ago": (dt.now() - td(minutes=10), None),
            "y10:00 - now": (today(hour=10) - days(1), dt.now()),
            "y10:00 until now": (today(hour=10) - days(1), dt.now()),
            "til 5min ago": (None, dt.now() - td(minutes=5)),
            "y10:00 until 10min ago": (
                today(hour=10) - days(1),
                dt.now() - td(minutes=10),
            ),
            "2h ago - now": (dt.now() - td(hours=2), dt.now()),
            "2h ago til 1h ago": (dt.now() - td(hours=2), dt.now() - td(hours=1)),
            "1h since 10:00": (t := today(hour=10), today(hour=11)),
            "1h until 10:00": (t := today(hour=9), today(hour=10)),
            "1h since 2h ago": (dt.now() - td(hours=2), dt.now() - td(hours=1)),
            "1h until 2h ago": (dt.now() - td(hours=3), dt.now() - td(hours=2)),
            "15min": (dt.now() - td(minutes=15), dt.now()),
            "this day": (today(), today() + days(1)),
        }.items():
            with self.subTest(input=input):
                tokens = Token.from_strings(shlex.split(input), simplify=True)
                token = next((t for t in tokens if isinstance(t, TimeFrame)), None)
                self.assertEqual(
                    bool(a := getattr(token, "start", None)),
                    bool(b := start),
                    msg=f"start should be {b} but is {a}",
                )
                self.assertEqual(
                    bool(a := getattr(token, "end", None)),
                    bool(b := end),
                    msg=f"end should be {b} but is {a}",
                )
                if start:
                    self.assertTrue(
                        abs(token.start - start).total_seconds() < 5,
                        msg=f"start should be {start} but is {token.start}",
                    )
                if end:
                    self.assertTrue(
                        abs(token.end - end).total_seconds() < 5,
                        msg=f"end should be {end} but is {token.end}",
                    )


class EventTest(TestCase):
    def test_parse_date(self):
        for string, shouldbe in {
            "0": today(hour=0),
            "00": today(hour=0),
            "000": today(hour=0),
            "0000": today(hour=0),
            "100": today(hour=1),
            "8": today(hour=8),
            "y1500": today(hour=15) - days(1),
            "t100": today(hour=1) + days(1),
            "yt100": today(hour=1),
            "yytt14:00": today(hour=14),
            "ytt00": today(hour=0) + days(1),
            (s := "2023-01-01T13:00"): dt.fromisoformat(s),
            "2023-01-01 1300": dt(2023, 1, 1, 13),
        }.items():
            with self.subTest(string=string, shouldbe=shouldbe):
                self.assertEqual(
                    (d := Event.parse_date(string)),
                    shouldbe,
                    msg=f"\nEvent.parse_date({string!r}) should be {shouldbe} but is instead {d}",
                )

    def test_parse_date_now(self):
        self.assertLess(Event.parse_date("now") - dt.now(), timedelta(seconds=10))

    def test_to_from_cli_idempotent(self):
        for cmdline in (
            "person=me work",
            "[10:20]",
            "10:00 until 12:00 work @home",
            "10min",
            "10min ago",
            "10min ago until now",
            "10min since now",
            "10min since 30min ago work @home",
            "[10;20] since 30min ago work @home",  # double time frame
        ):
            with self.subTest(cmdline=cmdline):
                e1 = Event.from_cli(shlex.split(cmdline))
                e2 = Event.from_cli(e1.to_cli())
                self.assertEqual(e1, e2)

    def test_equality(self):
        def test(method, e1, e2):
            method(e1, e2)
            method(e2, e1)

        test(self.assertEqual, Event(), Event())
        test(self.assertNotEqual, Event(), Event(fields=dict(bla=set(["blubb"]))))
        test(
            self.assertEqual,
            Event(fields=dict(bla=set(["blubb"]))),
            Event.from_cli(["bla=blubb"]),
        )

    def test_matches(self):
        for evcli, query, match in [
            ("@home", "@home", True),
            ("today", "this hour", True),
            ("with=me", "with=you", False),
            ("with=me with=you", "with=you", True),
        ]:
            with self.subTest(
                f"{evcli!r} {'should' if match else 'should not'} match query {query!r}"
            ):
                event = Event.from_cli(shlex.split(evcli))
                querytokens = Token.from_strings(shlex.split(query))
                self.assertEqual(event.matches(querytokens), match)


if __name__ == "__main__":
    unittest.main()
