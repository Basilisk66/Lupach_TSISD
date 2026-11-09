"""Консольное демо"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

from .service import nearest_departures
from .timetable import expand_timetable, load_timetable

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data" / "schedule.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ближайшие рейсы транспорта")
    parser.add_argument("--data", default=str(DEFAULT_DATA), help="путь к schedule.json")
    parser.add_argument("--now", help="ISO-время вместо текущего, напр. 2026-11-09T08:10")
    parser.add_argument("--limit", type=int, default=5, help="сколько рейсов показать")
    parser.add_argument("--route", help="показать только этот маршрут")
    args = parser.parse_args(argv)
    timetable = load_timetable(args.data)
    now = datetime.fromisoformat(args.now) if args.now else datetime.now(timetable.tz)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timetable.tz)
    today = now.astimezone(timetable.tz).date()
    trips = expand_timetable(timetable, start=today, days=2)
    try:
        result = nearest_departures(trips, now, limit=args.limit, route=args.route)
    except ValueError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2

    print(f"Сейчас: {now.astimezone(timetable.tz):%Y-%m-%d %H:%M} ({timetable.tz.key})")
    if not result:
        print("Ближайших рейсов не найдено")
        return 0
    for trip in result:
        local = trip.departs_at.astimezone(timetable.tz)
        minutes = int((trip.departs_at - now).total_seconds() // 60)
        print(f"{local:%d.%m %H:%M}  {trip.transport_type:<5} №{trip.route:<4} -> "
              f"{trip.destination}  (через {minutes} мин)")
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
