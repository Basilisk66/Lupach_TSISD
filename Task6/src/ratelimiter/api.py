import json
import math
from typing import Dict, Tuple

from .limiter import RateLimiter


def load_config(path: str) -> Dict:
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    for field in ("limit", "window_seconds"):
        if field not in cfg:
            raise ValueError(f"config: missing field '{field}'")
    return cfg


def handle_request(limiter: RateLimiter, api_key: str) -> Tuple[int, Dict[str, str], str]:
    """Возвращает (status, headers, body)."""
    if not api_key:
        return 401, {}, "API key required"

    res = limiter.allow(api_key)
    headers = {
        "X-RateLimit-Limit": str(limiter.limit),
        "X-RateLimit-Remaining": str(res.remaining),
    }
    if res.allowed:
        return 200, headers, "OK"
    headers["Retry-After"] = str(math.ceil(res.retry_after))
    return 429, headers, "Too Many Requests"
