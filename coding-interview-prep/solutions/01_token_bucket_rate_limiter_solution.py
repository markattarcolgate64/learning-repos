"""
Token Bucket Rate Limiter - Solution

A rate limiter that uses the token bucket algorithm. Tokens are added at a
constant refill rate up to a maximum capacity. Each request consumes one token.
"""


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize the token bucket rate limiter.

        Args:
            capacity: Maximum number of tokens the bucket can hold.
            refill_rate: Number of tokens added per second.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = 0.0

    def _refill(self, current_time: float) -> None:
        """
        Refill tokens based on elapsed time since last refill.

        Args:
            current_time: The current timestamp in seconds.
        """
        elapsed = current_time - self.last_refill_time
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill_time = current_time

    def allow_request(self, current_time: float) -> bool:
        """
        Check if a request is allowed and consume a token if so.

        Args:
            current_time: The current timestamp in seconds.

        Returns:
            True if the request is allowed, False otherwise.
        """
        self._refill(current_time)
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def get_tokens(self) -> float:
        """
        Return the current number of available tokens.

        Returns:
            The current token count as a float.
        """
        return self.tokens
