import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

from transport.cli import main
from transport.service import nearest_departures
from transport.timetable import (
    Timetable,
    TimetableEntry,
    expand_timetable,
    load_timetable,
    parse_time,
)

MSK = ZoneInfo("Europe/Moscow")


def make_timetable() -> Timetable:
    entry = TimetableEntry("12", "bus", "Центр", (time(23, 50), time(0, 10)))
    return Timetable(tz=MSK, entries=(entry,))


class ParseTimeTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_time("08:05"), time(8, 5))

    def test_invalid_values(self):
        for bad in ("25:00", "8-05", "", "12:60", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_time(bad)


class ExpandTimetableTests(unittest.TestCase):
    def test_expands_two_days(self):
        trips = expand_timetable(make_timetable(), date(2026, 11, 9), days=2)
        self.assertEqual(len(trips), 4)

    def test_after_midnight_next_day_trip_is_found(self):
        now = datetime(2026, 11, 9, 23, 55, tzinfo=MSK)
        trips = expand_timetable(make_timetable(), now.date(), days=2)
        result = nearest_departures(trips, now, limit=1)
        self.assertEqual(
            result[0].departs_at, datetime(2026, 11, 10, 0, 10, tzinfo=MSK)
        )

    def test_days_must_be_positive(self):
        with self.assertRaises(ValueError):
            expand_timetable(make_timetable(), date(2026, 11, 9), days=0)


class LoadTimetableTests(unittest.TestCase):
    def _write(self, payload) -> Path:
        tmp = tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(payload, tmp, ensure_ascii=False)
        tmp.close()
        self.addCleanup(Path(tmp.name).unlink)
        return Path(tmp.name)

    def test_load_ok(self):
        path = self._write(
            {
                "timezone": "Europe/Moscow",
                "routes": [
                    {"route": 12, "type": "bus", "destination": "A", "times": ["08:00"]}
                ],
            }
        )
        tt = load_timetable(path)
        self.assertEqual(tt.entries[0].route, "12")

    def test_bad_time_in_file(self):
        path = self._write(
            {
                "timezone": "Europe/Moscow",
                "routes": [
                    {
                        "route": "1",
                        "type": "bus",
                        "destination": "A",
                        "times": ["99:99"],
                    }
                ],
            }
        )
        with self.assertRaises(ValueError):
            load_timetable(path)


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_demo_output_has_no_past_trips(self):
        code, out, _ = self.run_cli("--now", "2026-11-09T08:10", "--limit", "3")
        self.assertEqual(code, 0)
        self.assertNotIn("08:00", out)
        self.assertNotIn("08:05", out)
        first_trip_line = out.splitlines()[1]
        self.assertIn("09:30", first_trip_line)

    def test_route_filter(self):
        code, out, _ = self.run_cli("--now", "2026-11-09T08:10", "--route", "M1")
        self.assertEqual(code, 0)
        self.assertIn("M1", out)
        self.assertNotIn("Вокзал", out)

    def test_invalid_limit_returns_error_code(self):
        code, _, err = self.run_cli("--now", "2026-11-09T08:10", "--limit", "0")
        self.assertEqual(code, 2)
        self.assertIn("limit", err)

    def test_after_last_trip_shows_tomorrow(self):
        code, out, _ = self.run_cli("--now", "2026-11-09T23:55", "--limit", "1")
        self.assertEqual(code, 0)
        self.assertIn("10.11 00:10", out)


if __name__ == "__main__":
    unittest.main()
