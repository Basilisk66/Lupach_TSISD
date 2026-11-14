import os
import sys
import threading
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ratelimiter import RateLimiter  # noqa: E402


class FakeClock:
    """Управляемые часы — тесты не зависят от реального времени."""

    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t

    def advance(self, seconds):
        self.t += seconds


class RateLimiterTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()

    def test_allows_up_to_limit(self):
        rl = RateLimiter(3, 10, self.clock)
        results = [rl.allow("a") for _ in range(3)]
        self.assertTrue(all(r.allowed for r in results))
        self.assertEqual([r.remaining for r in results], [2, 1, 1])

    def test_blocks_over_limit(self):
        rl = RateLimiter(2, 10, self.clock)
        rl.allow("a")
        rl.allow("a")
        res = rl.allow("a")
        self.assertFalse(res.allowed)
        self.assertEqual(res.remaining, 0)
        self.assertAlmostEqual(res.retry_after, 10)

    def test_window_expires(self):
        rl = RateLimiter(2, 10, self.clock)
        rl.allow("a")
        rl.allow("a")
        self.assertFalse(rl.allow("a").allowed)
        self.clock.advance(10.01)
        self.assertTrue(rl.allow("a").allowed)

    def test_sliding_window_partial_release(self):
        rl = RateLimiter(2, 10, self.clock)
        rl.allow("a")
        self.clock.advance(6)
        rl.allow("a")         
        self.clock.advance(5) 
        self.assertTrue(rl.allow("a").allowed)
        self.assertFalse(rl.allow("a").allowed)

    def test_retry_after_value(self):
        rl = RateLimiter(1, 10, self.clock)
        rl.allow("a")
        self.clock.advance(4)
        self.assertAlmostEqual(rl.allow("a").retry_after, 6)

    def test_keys_are_independent(self):
        rl = RateLimiter(1, 10, self.clock)
        self.assertTrue(rl.allow("a").allowed)
        self.assertFalse(rl.allow("a").allowed)
        self.assertTrue(rl.allow("b").allowed)

    def test_reset_single_and_all(self):
        rl = RateLimiter(1, 10, self.clock)
        rl.allow("a")
        rl.allow("b")
        rl.reset("a")
        self.assertTrue(rl.allow("a").allowed)
        self.assertFalse(rl.allow("b").allowed)
        rl.reset()
        self.assertTrue(rl.allow("b").allowed)

    def test_invalid_params(self):
        for limit, window in [(0, 10), (-1, 10), (5, 0), (5, -3)]:
            with self.subTest(limit=limit, window=window):
                with self.assertRaises(ValueError):
                    RateLimiter(limit, window)

    def test_thread_safety(self):
        rl = RateLimiter(50, 60)
        allowed = []

        def worker():
            for _ in range(20):
                allowed.append(rl.allow("shared").allowed)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(sum(allowed), 50) 


if __name__ == "__main__":
    unittest.main()
