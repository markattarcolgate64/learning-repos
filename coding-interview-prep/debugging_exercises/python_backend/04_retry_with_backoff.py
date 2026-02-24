# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Retry with Exponential Backoff
===============================

This module implements a retry decorator that retries failed function calls
with exponential backoff. It's commonly used for network requests, database
connections, and other operations that may experience transient failures.

Configuration:
    - max_retries: Maximum number of retry attempts (not counting the initial call)
    - base_delay: Initial delay in seconds before the first retry
    - backoff_factor: Multiplier applied to the delay after each retry
    - retryable_exceptions: Tuple of exception types that should trigger a retry

For example, with max_retries=3, the function should be called up to 4 times
total (1 initial + 3 retries). The delays should be:
    - After 1st failure: base_delay
    - After 2nd failure: base_delay * backoff_factor
    - After 3rd failure: base_delay * backoff_factor^2

SYMPTOMS:
    Tests are failing because the decorated function is being called fewer
    times than expected. A function configured with max_retries=3 that always
    fails should be called 4 times total (initial + 3 retries), but it is
    being called only 3 times. Functions that succeed on the 3rd attempt
    (with max_retries=3) are raising exceptions instead of returning the
    successful result.
"""

import unittest
from unittest.mock import patch, MagicMock
from functools import wraps


class MaxRetriesExceededError(Exception):
    """Raised when all retry attempts have been exhausted."""

    def __init__(self, func_name: str, attempts: int, last_exception: Exception):
        self.func_name = func_name
        self.attempts = attempts
        self.last_exception = last_exception
        super().__init__(
            f"Function '{func_name}' failed after {attempts} attempts. "
            f"Last error: {last_exception}"
        )


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
    retryable_exceptions: tuple = (Exception,),
):
    """
    Decorator that retries a function with exponential backoff.

    Args:
        max_retries: Number of retries after the initial attempt.
        base_delay: Delay before the first retry (in seconds).
        backoff_factor: Multiply delay by this factor after each retry.
        retryable_exceptions: Exception types that trigger a retry.

    Returns:
        Decorated function with retry logic.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exception = None

            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        import time
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        break

            raise MaxRetriesExceededError(
                func_name=func.__name__,
                attempts=max_retries,
                last_exception=last_exception,
            )

        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Example usage: a flaky service client
# ---------------------------------------------------------------------------

class TransientError(Exception):
    """Simulates a transient/retryable error."""
    pass


class PermanentError(Exception):
    """Simulates a permanent/non-retryable error."""
    pass


class FlakyServiceClient:
    """A service client that may experience transient failures."""

    def __init__(self, fail_times: int = 0):
        self._fail_times = fail_times
        self._call_count = 0

    @retry_with_backoff(
        max_retries=3,
        base_delay=0.01,
        backoff_factor=2.0,
        retryable_exceptions=(TransientError,),
    )
    def call_service(self, request: str) -> str:
        self._call_count += 1
        if self._call_count <= self._fail_times:
            raise TransientError(f"Transient failure on attempt {self._call_count}")
        return f"Success: {request}"

    @property
    def call_count(self) -> int:
        return self._call_count


# ---------------------------------------------------------------------------
# Test Suite
# ---------------------------------------------------------------------------

class TestRetryWithBackoff(unittest.TestCase):
    """Tests for retry_with_backoff. These tests FAIL due to the bug."""

    @patch("time.sleep")
    def test_succeeds_immediately_no_retry(self, mock_sleep):
        """If the function succeeds on first call, no retries should happen."""
        client = FlakyServiceClient(fail_times=0)
        result = client.call_service("hello")
        self.assertEqual(result, "Success: hello")
        self.assertEqual(client.call_count, 1)
        mock_sleep.assert_not_called()

    @patch("time.sleep")
    def test_retries_on_transient_error(self, mock_sleep):
        """Function should retry on transient errors and succeed."""
        client = FlakyServiceClient(fail_times=2)
        result = client.call_service("hello")
        self.assertEqual(result, "Success: hello")
        self.assertEqual(client.call_count, 3)

    @patch("time.sleep")
    def test_max_retries_exhausted(self, mock_sleep):
        """After max_retries retries, should raise MaxRetriesExceededError."""
        client = FlakyServiceClient(fail_times=999)

        with self.assertRaises(MaxRetriesExceededError) as ctx:
            client.call_service("hello")

        # With max_retries=3, total attempts should be 4 (initial + 3 retries)
        self.assertEqual(client.call_count, 4,
                         "Expected 4 total attempts: 1 initial + 3 retries")
        self.assertEqual(ctx.exception.attempts, 4)

    @patch("time.sleep")
    def test_succeeds_on_last_retry(self, mock_sleep):
        """Function that succeeds on the final retry attempt should return success."""
        # With max_retries=3, there are 4 total attempts.
        # fail_times=3 means it fails 3 times, then succeeds on attempt 4.
        client = FlakyServiceClient(fail_times=3)
        result = client.call_service("hello")
        self.assertEqual(result, "Success: hello")
        self.assertEqual(client.call_count, 4)

    @patch("time.sleep")
    def test_non_retryable_exception_not_retried(self, mock_sleep):
        """Exceptions not in retryable_exceptions should propagate immediately."""
        call_count = 0

        @retry_with_backoff(
            max_retries=3,
            base_delay=0.01,
            retryable_exceptions=(TransientError,),
        )
        def always_permanent_fail():
            nonlocal call_count
            call_count += 1
            raise PermanentError("This is permanent")

        with self.assertRaises(PermanentError):
            always_permanent_fail()

        self.assertEqual(call_count, 1, "Non-retryable exception should not cause retries")

    @patch("time.sleep")
    def test_backoff_delays(self, mock_sleep):
        """Verify that exponential backoff delays are applied correctly."""
        client = FlakyServiceClient(fail_times=999)

        with self.assertRaises(MaxRetriesExceededError):
            client.call_service("hello")

        # With base_delay=0.01 and backoff_factor=2.0 and 3 retries:
        # Retry 1: sleep(0.01)
        # Retry 2: sleep(0.02)
        # Retry 3: sleep(0.04)
        expected_delays = [0.01, 0.02, 0.04]
        actual_delays = [call.args[0] for call in mock_sleep.call_args_list]
        self.assertEqual(len(actual_delays), 3)
        for expected, actual in zip(expected_delays, actual_delays):
            self.assertAlmostEqual(actual, expected, places=5)

    @patch("time.sleep")
    def test_preserves_function_metadata(self, mock_sleep):
        """The decorated function should preserve the original function's name."""
        @retry_with_backoff()
        def my_special_function():
            return 42

        self.assertEqual(my_special_function.__name__, "my_special_function")


if __name__ == "__main__":
    unittest.main()
