"""
Token Bucket Rate Limiter
=========================
Category   : Distributed Systems
Difficulty : * (1/5)

Problem
-------
Implement a token bucket rate limiter. The bucket starts at full capacity and
refills at a fixed rate (tokens per second). Each incoming request consumes one
token. If there are no tokens available the request is rejected.

This is the most common algorithm used at companies like Stripe, Cloudflare, and
AWS API Gateway to protect services from being overwhelmed by too many requests.

Real-world motivation
---------------------
Without rate limiting, a single misbehaving client can monopolise server
resources or trigger cascading failures.  The token bucket algorithm is favoured
because it naturally allows short bursts (up to the bucket capacity) while
enforcing a steady-state average rate.

Hints
-----
1. Track the *last refill time* so you can compute how many tokens to add when
   the next request arrives (lazy refill).
2. Use min(capacity, current_tokens + elapsed * refill_rate) to cap at capacity.
3. Consume exactly one token per allowed request.

Run command
-----------
    python -m unittest 01_token_bucket_rate_limiter.test_exercise -v
"""

import time
class TokenBucketRateLimiter:
    """A token bucket rate limiter.

    The bucket starts full (at *capacity* tokens) and refills continuously at
    *refill_rate* tokens per second.  Each allowed request consumes one token.
    """

    def __init__(self, capacity: int, refill_rate: float) -> None:
        """Initialise the rate limiter.

        Args:
            capacity: Maximum number of tokens the bucket can hold.
            refill_rate: Rate at which tokens are added (tokens per second).
        """
        # TODO: Store capacity, refill_rate, initial token count, and last
        #       refill timestamp.
        # Hint: Start with tokens = capacity and last_refill_time = 0.0
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = 0.0


    def _refill(self, current_time: float) -> None:
        """Add tokens to the bucket based on elapsed time since last refill.

        The number of new tokens is proportional to the elapsed time and the
        refill rate.  The token count must never exceed the bucket capacity.

        Args:
            current_time: The current timestamp in seconds.
        """
        # TODO: Calculate elapsed time since last refill.
        elapsed = current_time - self.last_refill
        if elapsed > 0:
            add_tokens = elapsed * self.refill_rate 
            if add_tokens + self.tokens > self.capacity:
                self.tokens = self.capacity
            else:
                self.tokens += add_tokens

            self.last_refill = current_time

    def allow_request(self, current_time: float) -> bool:
        """Determine whether a request should be allowed.

        Refills the bucket first, then checks whether at least one token is
        available.  If so, consumes one token and returns True; otherwise
        returns False.

        Args:
            current_time: The current timestamp in seconds.

        Returns:
            True if the request is allowed, False if it should be rejected.
        """
        # TODO: Call _refill, then check if tokens >= 1.
        print("\nTime", current_time)
        print("Tokens prerefill", self.tokens)


        self._refill(current_time)

        print("Tokens post refill", self.tokens)

        if self.tokens >= 1: 
            self.tokens -= 1 
            print("Req good")
            return True
        else:
            print("Req fail")
            return False 

    def get_tokens(self) -> float:
        """Return the current number of tokens in the bucket.

        Returns:
            The current token count (may be fractional between refills).
        """


        return int(self.tokens)
