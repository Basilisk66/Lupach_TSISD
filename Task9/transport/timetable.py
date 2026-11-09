"""Загрузка расписания из JSON и разворачивание его в конкретные рейсы по датам

ДОПУЩЕНИЕ О ЧАСОВЫХ ПОЯСАХ:
  * Расписание в файле хранится как «время на табло» (HH:MM) и считается
    локальным временем ОДНОГО часового пояса — он указан в поле "timezone" файла.
  * Расписание действует ежедневно (без выходных/праздников).
  * «Сейчас» всегда сравнивается как aware-datetime, поэтому пользователь
    может находиться в другом поясе — сравнение всё равно будет верным
"""
import json
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from .models import Trip


@dataclass(frozen=True)
class TimetableEntry:
    """Строка расписания: маршрут + список времён отправления в течение суток"""
    route: str
    transport_type: str
    destination: str
    times: tuple[time, ...]


@dataclass(frozen=True)
class Timetable:
    tz: ZoneInfo
    entries: tuple[TimetableEntry, ...]

def parse_time(value: str) -> time:
    """Разбирает строку 'HH:MM'. Некорректный формат выкидывает ValueError с понятным текстом"""
    try:
        return datetime.strptime(value, "%H:%M").time()
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Некорректное время {value!r}, ожидается HH:MM") from exc

def load_timetable(path: str | Path) -> Timetable:
    """Читает JSON-файл расписания и валидирует его."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    tz = ZoneInfo(data["timezone"]) 
    entries = []
    for item in data["routes"]:
        times = tuple(parse_time(t) for t in item["times"])
        entries.append(
            TimetableEntry(
                route=str(item["route"]),
                transport_type=item["type"],
                destination=item["destination"],
                times=times,
            )
        )
    return Timetable(tz=tz, entries=tuple(entries))


def expand_timetable(timetable: Timetable, start: date, days: int = 2) -> list[Trip]:
    """Превращает «ежедневное расписание» в конкретные рейсы на `days` суток с даты `start`."""
    if days < 1:
        raise ValueError("days должен быть >= 1")
    trips: list[Trip] = []
    for offset in range(days):
        day = start + timedelta(days=offset)
        for entry in timetable.entries:
            for t in entry.times:
                trips.append(
                    Trip(
                        route=entry.route,
                        transport_type=entry.transport_type,
                        destination=entry.destination,
                        departs_at=datetime.combine(day, t, tzinfo=timetable.tz),
                    )
                )
    return trips
