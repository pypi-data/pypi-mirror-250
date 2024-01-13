# system modules
import logging
import itertools
import unittest
import shlex
from unittest import TestCase
from unittest.mock import patch

# internal modules
from annextimelog.repo import Event
from annextimelog.token import *
from annextimelog.datetime import datetime, datetime as dt, timedelta as td, timedelta

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

    def test_this_weekday_stays_that_weekday(self):
        for t, method, (day, nth_day) in itertools.product(
            "2023-01-04 2024-06-18 2025-08-31".split(),
            "prev this next".split(),
            self.WEEKDAYS.items(),
        ):
            if not isinstance(day, str):
                continue
            t = dt.fromisoformat(t)
            with self.subTest(call := f"{t}.{method}({day!r})"):
                self.assertEqual(
                    (r := getattr(t, method)(day)).weekday(),
                    nth_day,
                    msg=f"{call} ({r}) should be a {day}, but is a {self.WEEKDAYS[nth_day]}",
                )
                match method:
                    case "prev":
                        self.assertLess(r, t, msg=f"{call} ({r}) should be before {t}")
                    case "this":
                        self.assertLessEqual(
                            abs(r - t),
                            timedelta(days=(dd := 7)),
                            msg=f"{call} ({r}) shouldn't be more than {dd} days away from {t}",
                        )
                    case "next":
                        self.assertGreater(
                            r, t, msg=f"{call} ({r}) should be after than {t}"
                        )


class TokenTest(TestCase):
    def test_fieldmodifier(self):
        for s, r in {
            "a": AddToField("tag", {"a"}),
            "tag+=until": AddToField("tag", {"until"}),
            "tag+=a,b,c": AddToField("tag", {"a", "b", "c"}),
            "tags+=a,b,c": AddToField("tag", {"a", "b", "c"}),
            "tags-=a,b,c": RemoveFromField("tag", {"a", "b", "c"}),
            "tags=a,b,c": SetField("tag", {"a", "b", "c"}),
            "tags=": UnsetField("tag"),
            "field=": UnsetField("field"),
            "@home": AddToField("location", {"home"}),
            "at=home": SetField("location", {"home"}),
            "in=Berlin,Germany": SetField("location", {"Berlin", "Germany"}),
            "where+=in town": AddToField("location", {"in town"}),
            "id=bla": SetField("id", {"bla"}),
            "id-=bla": RemoveFromField("id", {"bla"}),
            "id+=bla": AddToField("id", {"bla"}),
            "id=": UnsetField("id"),
        }.items():
            with self.subTest(string=s):
                self.assertEqual(Token.from_str(s), r)

    def test_fieldmodifier_multiple(self):
        self.assertNotEqual(
            SetField.from_str(str(t := SetField("f", set(SetField.SEPARATORS)))),
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

    @staticmethod
    def strip_microseconds(tokens):
        for token in tokens:
            match token:
                case Time(time=time):
                    yield token.evolve(time=time.replace(microsecond=0))
                case TimeFrame(start=t1, end=t2):
                    yield t.evolve(
                        start=t1.replace(microsecond=0),
                        end=t2.replace(microsecond=0),
                    )
                case _:
                    yield token

    def test_from_strings(self):
        now = dt.now()
        for input, shouldbe in {
            "10min ago": [Time(now - td(minutes=10))],
            "in 2h": [Time(now + td(hours=2))],
            "10:00": [Time(today(hour=10))],
            "bla blubb": [AddToField("tag", {"bla"}), AddToField("tag", {"blubb"})],
        }.items():
            with self.subTest(f"Token.from_strings({input!r}) should be {shouldbe}"):
                tokens = Token.from_strings(
                    shlex.split(input), reduce=True, **(kw := dict(is_condition=True))
                )
                shouldbe = [t.evolve(**kw) for t in shouldbe]
                shouldbe = list(self.strip_microseconds(shouldbe))
                tokens = list(self.strip_microseconds(tokens))
                self.assertSequenceEqual(
                    tokens,
                    shouldbe,
                    f"Token.from_strings({input!r}) should be {shouldbe} but is {tokens}",
                )

    def test_timeframe_from_strings(self):
        now = dt.now()
        for input, (start, end) in {
            "y10:00 - now": (today(hour=10) - days(1), now),
            "y10:00 until now": (today(hour=10) - days(1), now),
            "til 5min ago": (None, now - td(minutes=5)),
            "y10:00 until 10min ago": (
                today(hour=10) - days(1),
                now - td(minutes=10),
            ),
            "2h ago - now": (now - td(hours=2), now),
            "2h ago til 1h ago": (now - td(hours=2), now - td(hours=1)),
            "1h since 10:00": (t := today(hour=10), today(hour=11)),
            "1h until 10:00": (t := today(hour=9), today(hour=10)),
            "1h since 2h ago": (now - td(hours=2), now - td(hours=1)),
            "1h until 2h ago": (now - td(hours=3), now - td(hours=2)),
            "15min": (now - td(minutes=15), now),
            "this day": (today(), today() + days(1)),
            "until this day": (None, today() + days(1)),
            "since this hour": (now.this("hour"), None),
            "since yesterday": (today() - days(1), None),
            "until today": (None, today() + days(1)),
            "until tomorrow": (None, today() + days(2)),
        }.items():
            with self.subTest(input=input):
                tokens = Token.from_strings(
                    shlex.split(input), reduce=True, is_condition=True
                )
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

    def test_from_strings_actions_conditions(self):
        for cmdline, (actions, conditions) in {
            # "bla": ({AddToField("tag", {"bla"})}, set()),
            "set @home if thistag": (
                {AddToField("location", {"home"})},
                {AddToField("tag", {"thistag"})},
            ),
            "when id=asdf tag1 update @home": (
                {AddToField("location", {"home"})},
                {SetField("id", {"asdf"}), AddToField("tag", {"tag1"})},
            ),
            # "a b c ": (3, 0),
            "if a b c": (0, 3),
            "set if a b c": (0, 3),
            "if a b c set": (0, 3),
            "set tag1 until now": (2, 0),
            "until now set end=yesterday": (1, 1),
            "since yesterday @guz update myfield+=value @home": (2, 2),
            "today note=this mod location=home": (1, 2),
        }.items():
            with self.subTest(
                f"{cmdline!r} should yield {len(actions) if hasattr(actions,'__len__') else actions} actions "
                f"and {len(conditions) if hasattr(conditions,'__len__') else conditions} conditions"
            ):
                tokens = Token.from_strings(shlex.split(cmdline))
                unhandled, actions_, conditions_ = set(), set(), set()
                for token in tokens:
                    match token:
                        case Token(is_condition=True):
                            conditions_.add(token)
                        case Token(is_condition=False):
                            actions_.add(token)
                        case _:
                            unhandled.add(token)
                self.assertFalse(
                    unhandled,
                    msg=f"from_strings({cmdline!r}) shouldn't return unhandled tokens, but did: {unhandled}",
                )
                for name, (result, shouldbe, is_condition) in dict(
                    actions=(actions_, actions, False),
                    conditions=(conditions_, conditions, True),
                ).items():
                    match shouldbe:
                        case int():
                            self.assertEqual(
                                len(result),
                                shouldbe,
                                f"\n\nfrom_strings({cmdline!r}) should return {shouldbe} {name}, but instead returned {len(result)}",
                            )
                        case set():
                            shouldbe = {
                                t.evolve(is_condition=is_condition) for t in result
                            }
                            self.assertSetEqual(
                                result,
                                shouldbe,
                                f"\n\nfrom_strings({cmdline!r}) should return {name}\n{shouldbe}\nbut instead returned\n{result}",
                            )
                        case _:
                            self.fail(
                                f"wtf is {shouldbe!r} ({type(shouldbe)})? Should be int (how many {name}?) or set (the actual {name})"
                            )

    def test_from_strings_invalid_raises(self):
        for cmdline, kwargs in {
            "set bla": dict(is_condition=True),
            "if bla": dict(is_condition=False),
            "id=1 if @home": dict(is_condition=False),
            "id=1 set @home": dict(is_condition=True),
            "@home set bla": dict(is_condition=False),
            "@home set bla": dict(is_condition=True),
        }.items():
            with self.assertRaises(
                ValueError,
                msg=f"from_strings({cmdline!r}) should raise an exception but didn't!",
            ):
                Token.from_strings(shlex.split(cmdline), **kwargs)


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
                querytokens = Token.from_strings(shlex.split(query), is_condition=True)
                self.assertEqual(event.matches(querytokens), match)


if __name__ == "__main__":
    unittest.main()
