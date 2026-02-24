# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Webhook Dispatcher with Retry Logic
=====================================

System:
    A webhook dispatcher that sends event payloads to registered subscriber
    URLs via HTTP POST. If delivery fails (non-2xx status or exception), the
    dispatcher retries with exponential backoff up to a configurable maximum
    number of retries.

    The dispatcher provides:
        - register(url)         : add a subscriber URL
        - dispatch(event_type, payload) : send an event to all subscribers
        - delivery_log          : a list of DeliveryRecord objects for inspection

    A pluggable `send_func` is used instead of real HTTP for testability.

Expected behavior:
    - Successful deliveries (2xx) are recorded and not retried.
    - Failed deliveries are retried with exponential backoff up to max_retries.
    - After exhausting all retries, the delivery is marked as permanently failed.
    - The backoff between retries should double each time: delay, delay*2, delay*4...

Symptoms:
    Tests are failing because the dispatcher appears to give up too early --
    it retries fewer times than expected. Webhooks that should succeed after
    a few transient failures are being marked as permanently failed, and the
    total attempt count is off by one.
"""

import unittest
from dataclasses import dataclass, field
from typing import Callable, List, Optional


@dataclass
class DeliveryRecord:
    """Record of a single delivery attempt chain."""
    url: str
    event_type: str
    payload: dict
    attempts: int = 0
    succeeded: bool = False
    last_status: Optional[int] = None
    last_error: Optional[str] = None


@dataclass
class DeliveryResult:
    """Result from a single send attempt."""
    status_code: int
    error: Optional[str] = None


class WebhookDispatcher:
    """Dispatches events to registered webhook URLs with retry logic."""

    def __init__(
        self,
        send_func: Callable,
        max_retries: int = 3,
        base_delay: float = 1.0,
        sleep_func: Callable = None,
    ):
        """
        Args:
            send_func:  callable(url, event_type, payload) -> DeliveryResult
            max_retries: max number of retry attempts after the initial try
            base_delay:  initial backoff delay in seconds
            sleep_func:  callable(seconds) for backoff; defaults to no-op in tests
        """
        self.send_func = send_func
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.sleep_func = sleep_func or (lambda s: None)
        self._subscribers: List[str] = []
        self.delivery_log: List[DeliveryRecord] = []

    def register(self, url: str):
        """Register a subscriber URL."""
        if url not in self._subscribers:
            self._subscribers.append(url)

    def unregister(self, url: str):
        """Remove a subscriber URL."""
        self._subscribers = [u for u in self._subscribers if u != url]

    def dispatch(self, event_type: str, payload: dict):
        """Send an event to all registered subscribers with retry logic."""
        for url in self._subscribers:
            record = DeliveryRecord(url=url, event_type=event_type, payload=payload)
            self._deliver_with_retries(record)
            self.delivery_log.append(record)

    def _deliver_with_retries(self, record: DeliveryRecord):
        """Attempt delivery with exponential backoff retries."""
        for attempt in range(1 + self.max_retries):
            record.attempts += 1
            failed = False

            try:
                result = self.send_func(record.url, record.event_type, record.payload)
                record.last_status = result.status_code

                if 200 <= result.status_code < 300:
                    record.succeeded = True
                    return

                record.last_error = f"HTTP {result.status_code}"
                failed = True

            except Exception as e:
                record.last_error = str(e)
                failed = True

            # If delivery failed, decide whether to retry
            if failed:
                if record.attempts >= self.max_retries:
                    return  # exhausted retries

                delay = self.base_delay * (2 ** attempt)
                self.sleep_func(delay)


# ---------------------------------------------------------------------------
# Tests -- these should PASS once the bug is fixed
# ---------------------------------------------------------------------------

class TestWebhookDispatcher(unittest.TestCase):

    def test_successful_first_try(self):
        """A webhook that succeeds on the first attempt."""
        def send_ok(url, event_type, payload):
            return DeliveryResult(status_code=200)

        dispatcher = WebhookDispatcher(send_func=send_ok, max_retries=3)
        dispatcher.register("https://hooks.example.com/a")
        dispatcher.dispatch("order.created", {"order_id": 1})

        self.assertEqual(len(dispatcher.delivery_log), 1)
        record = dispatcher.delivery_log[0]
        self.assertTrue(record.succeeded)
        self.assertEqual(record.attempts, 1)
        self.assertEqual(record.last_status, 200)

    def test_succeeds_after_transient_failures(self):
        """
        A webhook that fails twice then succeeds on the third attempt.
        The dispatcher should retry and ultimately record success.
        """
        call_count = 0

        def send_flaky(url, event_type, payload):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return DeliveryResult(status_code=500, error="Internal Server Error")
            return DeliveryResult(status_code=200)

        dispatcher = WebhookDispatcher(send_func=send_flaky, max_retries=3)
        dispatcher.register("https://hooks.example.com/b")
        dispatcher.dispatch("order.shipped", {"order_id": 2})

        record = dispatcher.delivery_log[0]
        self.assertTrue(
            record.succeeded,
            f"Expected success after transient failures, but got: "
            f"succeeded={record.succeeded}, attempts={record.attempts}, "
            f"last_error={record.last_error}",
        )
        self.assertEqual(record.attempts, 3, "Should have taken 3 attempts total")

    def test_gives_up_after_max_retries(self):
        """
        A webhook that always fails should be marked as failed after
        1 initial attempt + max_retries retries.
        """
        def send_fail(url, event_type, payload):
            return DeliveryResult(status_code=503)

        dispatcher = WebhookDispatcher(send_func=send_fail, max_retries=3)
        dispatcher.register("https://hooks.example.com/c")
        dispatcher.dispatch("order.cancelled", {"order_id": 3})

        record = dispatcher.delivery_log[0]
        self.assertFalse(record.succeeded)
        self.assertEqual(
            record.attempts,
            4,
            "Should have attempted 1 initial + 3 retries = 4 total",
        )

    def test_backoff_delays(self):
        """Backoff delays should double: base, base*2, base*4, ..."""
        delays = []

        def send_fail(url, event_type, payload):
            return DeliveryResult(status_code=500)

        def mock_sleep(seconds):
            delays.append(seconds)

        dispatcher = WebhookDispatcher(
            send_func=send_fail,
            max_retries=3,
            base_delay=1.0,
            sleep_func=mock_sleep,
        )
        dispatcher.register("https://hooks.example.com/d")
        dispatcher.dispatch("test.event", {})

        # 3 retries -> 3 sleeps: 1*2^0=1, 1*2^1=2, 1*2^2=4
        self.assertEqual(delays, [1.0, 2.0, 4.0])

    def test_exception_triggers_retry(self):
        """Network exceptions should be caught and trigger retries."""
        call_count = 0

        def send_exception_then_ok(url, event_type, payload):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ConnectionError("Connection refused")
            return DeliveryResult(status_code=200)

        dispatcher = WebhookDispatcher(send_func=send_exception_then_ok, max_retries=3)
        dispatcher.register("https://hooks.example.com/e")
        dispatcher.dispatch("test.retry", {})

        record = dispatcher.delivery_log[0]
        self.assertTrue(record.succeeded)
        self.assertEqual(record.attempts, 2)

    def test_multiple_subscribers(self):
        """Each subscriber gets its own delivery attempt."""
        results = {}

        def send_track(url, event_type, payload):
            results.setdefault(url, 0)
            results[url] += 1
            return DeliveryResult(status_code=200)

        dispatcher = WebhookDispatcher(send_func=send_track, max_retries=2)
        dispatcher.register("https://hooks.example.com/x")
        dispatcher.register("https://hooks.example.com/y")
        dispatcher.dispatch("multi.test", {"data": "test"})

        self.assertEqual(len(dispatcher.delivery_log), 2)
        self.assertEqual(results["https://hooks.example.com/x"], 1)
        self.assertEqual(results["https://hooks.example.com/y"], 1)


if __name__ == "__main__":
    unittest.main()
