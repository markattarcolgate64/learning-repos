"""Tests for the Token Bucket Rate Limiter exercise."""

import unittest

from exercise import TokenBucketRateLimiter


class TestTokenBucketRateLimiter(unittest.TestCase):
    """Comprehensive tests for TokenBucketRateLimiter."""

    # ------------------------------------------------------------------
    # 1. Fresh bucket allows requests up to capacity
    # ------------------------------------------------------------------
    def test_fresh_bucket_allows_requests_up_to_capacity(self):
        """A brand-new bucket should allow exactly `capacity` requests."""
        capacity = 5
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=1.0)
        for i in range(capacity):
            self.assertTrue(
                limiter.allow_request(current_time=0.0),
                f"Request {i + 1} of {capacity} should be allowed",
            )

    # ------------------------------------------------------------------
    # 2. Depleted bucket rejects requests
    # ------------------------------------------------------------------
    def test_depleted_bucket_rejects_requests(self):
        """After all tokens are consumed, subsequent requests are rejected."""
        capacity = 3
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=1.0)
        # Exhaust all tokens
        for _ in range(capacity):
            limiter.allow_request(current_time=0.0)
        # Next request should be rejected
        self.assertFalse(limiter.allow_request(current_time=0.0))
        self.assertFalse(limiter.allow_request(current_time=0.0))

    # ------------------------------------------------------------------
    # 3. Tokens refill over time correctly
    # ------------------------------------------------------------------
    def test_tokens_refill_over_time(self):
        """After depleting the bucket, waiting should refill tokens."""
        capacity = 5
        refill_rate = 2.0  # 2 tokens per second
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)

        # Exhaust all tokens at t=0
        for _ in range(capacity):
            limiter.allow_request(current_time=0.0)
        self.assertFalse(limiter.allow_request(current_time=0.0))

        # At t=1.0, 2 tokens should have refilled (2 tokens/sec * 1 sec)
        self.assertTrue(limiter.allow_request(current_time=1.0))
        self.assertTrue(limiter.allow_request(current_time=1.0))
        # Third request at same time should fail (only 2 refilled)
        self.assertFalse(limiter.allow_request(current_time=1.0))

    # ------------------------------------------------------------------
    # 4. Capacity cap: tokens never exceed capacity after long idle
    # ------------------------------------------------------------------
    def test_tokens_never_exceed_capacity(self):
        """Even after a long idle period, tokens are capped at capacity."""
        capacity = 5
        refill_rate = 10.0
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)

        # Exhaust all tokens
        for _ in range(capacity):
            limiter.allow_request(current_time=0.0)

        # Wait a very long time (1000 seconds at 10 tokens/sec = 10000 tokens,
        # but should be capped at 5)
        allowed_count = 0
        for i in range(10):
            if limiter.allow_request(current_time=1000.0):
                allowed_count += 1
        self.assertEqual(allowed_count, capacity)

    # ------------------------------------------------------------------
    # 5. Burst: rapid requests deplete tokens
    # ------------------------------------------------------------------
    def test_burst_depletes_tokens(self):
        """Rapid sequential requests at the same timestamp deplete tokens."""
        capacity = 10
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=1.0)

        allowed = 0
        rejected = 0
        for _ in range(15):
            if limiter.allow_request(current_time=0.0):
                allowed += 1
            else:
                rejected += 1

        self.assertEqual(allowed, capacity)
        self.assertEqual(rejected, 5)

    # ------------------------------------------------------------------
    # 6. Partial refill: fractional tokens accumulate correctly
    # ------------------------------------------------------------------
    def test_partial_refill_fractional_tokens(self):
        """Fractional token accumulation works correctly."""
        capacity = 5
        refill_rate = 1.0  # 1 token per second
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)

        # Use all tokens at t=0
        for _ in range(capacity):
            limiter.allow_request(current_time=0.0)

        # At t=0.5, only 0.5 tokens refilled -- not enough for a request
        self.assertFalse(limiter.allow_request(current_time=0.5))

        # At t=1.5 since last refill was at 0.5, another 1.0 tokens added.
        # Total accumulated since full depletion: ~1.5 - 0.5 consumed attempt
        # Actually: after the failed request at 0.5 the internal time updated,
        # so at t=1.5 we get (1.5-0.5)*1.0 = 1.0 tokens added.
        self.assertTrue(limiter.allow_request(current_time=1.5))
        # Only 1 token was available, so next should fail
        self.assertFalse(limiter.allow_request(current_time=1.5))

    #------------------------------------------------------------------
    # 7. get_tokens returns correct count
    # ------------------------------------------------------------------
    def test_get_tokens_returns_correct_count(self):
        """get_tokens should reflect the current token count."""
        capacity = 5
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=1.0)

        # Initially full
        self.assertEqual(limiter.get_tokens(), capacity)

        # After one request
        limiter.allow_request(current_time=0.0)
        self.assertEqual(limiter.get_tokens(), capacity - 1)

        # After exhausting
        for _ in range(capacity - 1):
            limiter.allow_request(current_time=0.0)
        self.assertEqual(limiter.get_tokens(), 0)

    # ------------------------------------------------------------------
    # 8. Edge: zero capacity means all requests rejected
    # ------------------------------------------------------------------
    def test_zero_capacity_rejects_all(self):
        """A bucket with zero capacity should reject every request."""
        limiter = TokenBucketRateLimiter(capacity=0, refill_rate=10.0)
        self.assertFalse(limiter.allow_request(current_time=0.0))
        self.assertFalse(limiter.allow_request(current_time=100.0))
        self.assertEqual(limiter.get_tokens(), 0)


if __name__ == "__main__":
    unittest.main()
