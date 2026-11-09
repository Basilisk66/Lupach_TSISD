import unittest
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from transport.models import Trip
from transport.service import nearest_departures

MSK = ZoneInfo("Europe/Moscow")


def trip(hhmm: str, route: str = "12", day: int = 9) -> Trip:
    h, m = map(int, hhmm.split(":"))
    return Trip(route, "bus", "Центр", datetime(2026, 11, day, h, m, tzinfo=MSK))

NOW = datetime(2026, 11, 9, 8, 0, tzinfo=MSK)

class NearestDeparturesTests(unittest.TestCase):
    def test_past_trip_is_excluded(self):
        trips = [trip("07:59"), trip("08:01")]
        result = nearest_departures(trips, NOW)
        self.assertEqual([t.departs_at.strftime("%H:%M") for t in result], ["08:01"])

    def test_trip_exactly_now_is_included(self):
        result = nearest_departures([trip("08:00")], NOW)
        self.assertEqual(len(result), 1)

    def test_one_minute_ago_is_excluded(self):
        self.assertEqual(nearest_departures([trip("07:59")], NOW), [])

    def test_sorted_by_departure_time_even_if_input_unsorted(self):
        trips = [trip("12:00"), trip("08:30"), trip("10:15")]
        result = nearest_departures(trips, NOW)
        self.assertEqual(
            [t.departs_at.strftime("%H:%M") for t in result],
            ["08:30", "10:15", "12:00"],
        )

    def test_same_time_ordered_by_route_deterministically(self):
        trips = [trip("09:00", route="M1"), trip("09:00", route="12")]
        result = nearest_departures(trips, NOW)
        self.assertEqual([t.route for t in result], ["12", "M1"])

    def test_limit_cuts_result(self):
        trips = [trip(f"{h:02d}:00") for h in range(9, 15)]
        self.assertEqual(len(nearest_departures(trips, NOW, limit=3)), 3)

    def test_limit_must_be_positive(self):
        with self.assertRaises(ValueError):
            nearest_departures([trip("09:00")], NOW, limit=0)

    def test_route_filter_case_insensitive(self):
        trips = [trip("09:00", route="M1"), trip("09:05", route="12")]
        result = nearest_departures(trips, NOW, route="m1")
        self.assertEqual([t.route for t in result], ["M1"])

    def test_empty_when_everything_in_past(self):
        self.assertEqual(nearest_departures([trip("06:00"), trip("07:00")], NOW), [])

    def test_empty_input(self):
        self.assertEqual(nearest_departures([], NOW), [])

    def test_naive_now_is_rejected(self):
        with self.assertRaises(ValueError):
            nearest_departures([trip("09:00")], datetime(2026, 11, 9, 8, 0))

    def test_naive_trip_is_rejected(self):
        with self.assertRaises(ValueError):
            Trip("12", "bus", "Центр", datetime(2026, 11, 9, 9, 0))

    def test_now_in_other_timezone_compared_correctly(self):
        now_utc = datetime(2026, 11, 9, 5, 0, tzinfo=UTC)
        result = nearest_departures([trip("07:59"), trip("08:01")], now_utc)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].departs_at.strftime("%H:%M"), "08:01")

    def test_does_not_mutate_input(self):
        trips = [trip("12:00"), trip("09:00")]
        snapshot = list(trips)
        nearest_departures(trips, NOW)
        self.assertEqual(trips, snapshot)

if __name__ == "__main__":
    unittest.main()
