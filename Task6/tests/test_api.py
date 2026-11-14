import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ratelimiter import RateLimiter, handle_request, load_config  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")


class ApiTests(unittest.TestCase):
    def test_ok_response_has_headers(self):
        status, headers, _ = handle_request(RateLimiter(2, 60), "key1")
        self.assertEqual(status, 200)
        self.assertEqual(headers["X-RateLimit-Limit"], "2")
        self.assertEqual(headers["X-RateLimit-Remaining"], "1")

    def test_429_with_retry_after(self):
        rl = RateLimiter(1, 60)
        handle_request(rl, "key1")
        status, headers, _ = handle_request(rl, "key1")
        self.assertEqual(status, 429)
        self.assertGreaterEqual(int(headers["Retry-After"]), 1)

    def test_missing_key_is_401(self):
        self.assertEqual(handle_request(RateLimiter(1, 60), "")[0], 401)

    def test_real_config_is_valid(self):
        cfg = load_config(os.path.join(ROOT, "config", "limits.json"))
        self.assertGreater(cfg["limit"], 0)
        self.assertGreater(cfg["window_seconds"], 0)

    def test_config_missing_field(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "bad.json")
            with open(p, "w") as f:
                json.dump({"limit": 5}, f)
            with self.assertRaises(ValueError):
                load_config(p)


if __name__ == "__main__":
    unittest.main()
