"""Модель данных: один конкретный рейс"""
from dataclasses import dataclass
from datetime import datetime


def is_aware(value: datetime) -> bool:
    """True, если у datetime есть часовой пояс (aware), False — если «наивный»"""
    return value.tzinfo is not None and value.utcoffset() is not None


@dataclass(frozen=True) 
class Trip:
    route: str
    transport_type: str
    destination: str 
    departs_at: datetime
    def __post_init__(self) -> None:
        if not is_aware(self.departs_at):
            raise ValueError("departs_at должен быть timezone-aware (с часовым поясом)")
