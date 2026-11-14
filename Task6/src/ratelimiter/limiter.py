import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, Dict, Optional


@dataclass(frozen=True)
class LimitResult:
    allowed: bool
    remaining: int      # сколько запросов осталось в текущем окне
    retry_after: float  # через сколько секунд можно повторить (0, если allowed)


class RateLimiter:
    """Не более `limit` запросов на ключ за `window` секунд."""

    def __init__(self, limit: int, window: float,
                 clock: Callable[[], float] = time.monotonic):
        if limit <= 0:
            raise ValueError("limit must be positive")
        if window <= 0:
            raise ValueError("window must be positive")
        self.limit = limit
        self.window = window
        self._clock = clock
        self._hits: Dict[str, Deque[float]] = {}
        self._lock = threading.Lock()

    def allow(self, key: str) -> LimitResult:
        now = self._clock()
        with self._lock:
            hits = self._hits.setdefault(key, deque())
            while hits and hits[0] <= now - self.window:
                hits.popleft()

            if len(hits) < self.limit:
                hits.append(now)
                return LimitResult(True, self.limit - len(hits), 0.0)

            retry_after = hits[0] + self.window - now
            return LimitResult(False, 0, retry_after)

    def reset(self, key: Optional[str] = None) -> None:
        """Сбросить счётчик одного ключа или всех."""
        with self._lock:
            if key is None:
                self._hits.clear()
            else:
                self._hits.pop(key, None)
