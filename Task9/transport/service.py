from datetime import datetime
from typing import Iterable
from .models import Trip, is_aware

def nearest_departures(
    trips: Iterable[Trip],
    now: datetime,
    limit: int = 5,
    route: str | None = None,
) -> list[Trip]:
    """Возвращает до `limit` ближайших рейсов, отсортированных по времени отправления.
    Правила:
      * рейсы в прошлом (departs_at < now) НЕ попадают в результат;
      * рейс, отправляющийся ровно в `now`, ещё считается доступным (>=);
      * `now` обязан быть timezone-aware, иначе ValueError;
      * `route` (необязательно) — фильтр по маршруту без учёта регистра
    """
    if not is_aware(now):
        raise ValueError("now должен быть timezone-aware (с часовым поясом)")
    if limit < 1:
        raise ValueError("limit должен быть >= 1")
    wanted = route.strip().casefold() if route else None
    upcoming = [
        trip
        for trip in trips
        if trip.departs_at >= now
        and (wanted is None or trip.route.casefold() == wanted)
    ]
    upcoming.sort(key=lambda t: (t.departs_at, t.route))
    return upcoming[:limit]
