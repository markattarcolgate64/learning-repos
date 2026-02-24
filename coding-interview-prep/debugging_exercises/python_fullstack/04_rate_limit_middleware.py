# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Sliding Window Rate Limiter
============================

System:
    A sliding-window rate limiter for API endpoints. Each client (identified
    by a key, typically an API key or user ID) is allowed a maximum number of
    requests within a rolling time window. Old request timestamps outside the
    window are pruned on each check.

    The middleware provides:
        - is_allowed(client_key) -> bool : check if a request is allowed
        - remaining(client_key) -> int   : how many requests remain in the window
        - reset_time(client_key) -> float : when the window fully resets

Expected behavior:
    - A client can make up to `max_requests` within any `window_seconds` period.
    - After exceeding the limit, requests are denied until old timestamps
      fall outside the window.
    - Different clients have independent limits.

Symptoms:
    Tests are failing because different users seem to share the same rate limit
    bucket. When user A makes requests, user B's remaining count goes down too.
    The per-user isolation is broken.
"""

import time
import unittest
from unittest.mock import patch


class RateLimiter:
    """Sliding window rate limiter."""

    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._default_bucket = []
        self._timestamps = {}

    def _get_bucket(self, client_key):
        """Get or create the timestamp bucket for a client."""
        if client_key not in self._timestamps:
            self._timestamps[client_key] = self._default_bucket
        return self._timestamps[client_key]

    def _prune(self, client_key, now):
        """Remove timestamps outside the current window."""
        bucket = self._get_bucket(client_key)
        cutoff = now - self.window_seconds
        # Remove expired entries in place
        expired = [ts for ts in bucket if ts <= cutoff]
        for ts in expired:
            bucket.remove(ts)

    def is_allowed(self, client_key):
        """
        Check if a request from `client_key` is allowed.
        If allowed, record the timestamp and return True.
        If rate-limited, return False.
        """
        now = time.time()
        self._prune(client_key, now)

        bucket = self._get_bucket(client_key)
        if len(bucket) >= self.max_requests:
            return False

        bucket.append(now)
        return True

    def remaining(self, client_key):
        """Return how many requests the client can still make in this window."""
        now = time.time()
        self._prune(client_key, now)
        bucket = self._get_bucket(client_key)
        return max(0, self.max_requests - len(bucket))

    def reset_time(self, client_key):
        """
        Return the epoch time when the client's oldest request will fall off,
        freeing up a slot. Returns 0 if there are no recorded requests.
        """
        bucket = self._get_bucket(client_key)
        if not bucket:
            return 0
        oldest = min(bucket)
        return oldest + self.window_seconds


# ---------------------------------------------------------------------------
# Tests -- these should PASS once the bug is fixed
# ---------------------------------------------------------------------------

class TestRateLimiter(unittest.TestCase):

    def test_allows_within_limit(self):
        """Requests within the limit should be allowed."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        for _ in range(5):
            self.assertTrue(limiter.is_allowed("user_1"))

    def test_blocks_over_limit(self):
        """The request that exceeds the limit should be denied."""
        limiter = RateLimiter(max_requests=3, window_seconds=60)
        for _ in range(3):
            self.assertTrue(limiter.is_allowed("user_1"))
        self.assertFalse(limiter.is_allowed("user_1"))

    def test_remaining_count(self):
        """remaining() should decrement as requests are made."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        self.assertEqual(limiter.remaining("user_1"), 5)
        limiter.is_allowed("user_1")
        self.assertEqual(limiter.remaining("user_1"), 4)
        limiter.is_allowed("user_1")
        self.assertEqual(limiter.remaining("user_1"), 3)

    def test_window_slides(self):
        """After the window slides past old requests, new ones are allowed."""
        limiter = RateLimiter(max_requests=2, window_seconds=10)

        base = time.time()
        with patch("time.time", return_value=base):
            self.assertTrue(limiter.is_allowed("user_1"))
            self.assertTrue(limiter.is_allowed("user_1"))
            self.assertFalse(limiter.is_allowed("user_1"))

        # Advance time past the window
        with patch("time.time", return_value=base + 11):
            self.assertTrue(
                limiter.is_allowed("user_1"),
                "Old timestamps should have expired; request should be allowed",
            )

    def test_users_are_independent(self):
        """
        Different users must have completely independent rate limits.
        User A's requests must not affect User B's remaining count.
        """
        limiter = RateLimiter(max_requests=3, window_seconds=60)

        # User A uses all requests
        for _ in range(3):
            limiter.is_allowed("user_A")

        # User B should still have a full quota
        self.assertEqual(
            limiter.remaining("user_B"),
            3,
            "User B's limit should be unaffected by User A's requests",
        )
        self.assertTrue(
            limiter.is_allowed("user_B"),
            "User B should be allowed since they haven't made any requests",
        )

    def test_reset_time(self):
        """reset_time should return when the oldest request expires."""
        limiter = RateLimiter(max_requests=3, window_seconds=60)
        base = time.time()
        with patch("time.time", return_value=base):
            limiter.is_allowed("user_1")
        expected_reset = base + 60
        self.assertAlmostEqual(limiter.reset_time("user_1"), expected_reset, places=2)

    def test_no_requests_gives_zero_reset(self):
        """reset_time for a client with no requests should return 0."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        self.assertEqual(limiter.reset_time("unknown_user"), 0)


if __name__ == "__main__":
    unittest.main()
