"""
Tests for Pub/Sub Message Broker.

Run with:
    python -m unittest 11_pub_sub_broker.test_exercise -v
"""

import unittest
from .exercise import PubSubBroker, Message


class TestPubSubBroker(unittest.TestCase):
    """Comprehensive tests for the in-memory pub/sub message broker."""

    # ------------------------------------------------------------------
    # 1. Basic pub/sub: publish to topic, subscriber receives
    # ------------------------------------------------------------------

    def test_basic_publish_subscribe(self):
        """A subscriber should receive messages published to a matching topic."""
        broker = PubSubBroker()
        broker.create_topic("news")
        broker.subscribe("sub1", "news")
        broker.publish("news", {"headline": "hello"})

        messages = broker.poll("sub1")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].topic, "news")
        self.assertEqual(messages[0].payload, {"headline": "hello"})

    # ------------------------------------------------------------------
    # 2. Multiple subscribers all receive the message
    # ------------------------------------------------------------------

    def test_multiple_subscribers(self):
        """All subscribers matching a topic should receive the message."""
        broker = PubSubBroker()
        broker.create_topic("alerts")
        broker.subscribe("sub1", "alerts")
        broker.subscribe("sub2", "alerts")
        broker.publish("alerts", {"level": "critical"})

        msgs1 = broker.poll("sub1")
        msgs2 = broker.poll("sub2")
        self.assertEqual(len(msgs1), 1)
        self.assertEqual(len(msgs2), 1)
        self.assertEqual(msgs1[0].payload, {"level": "critical"})
        self.assertEqual(msgs2[0].payload, {"level": "critical"})

    # ------------------------------------------------------------------
    # 3. Wildcard pattern: 'events.*' matches 'events.click'
    # ------------------------------------------------------------------

    def test_wildcard_matches_single_segment(self):
        """'events.*' should match 'events.click'."""
        broker = PubSubBroker()
        broker.create_topic("events.click")
        broker.subscribe("sub1", "events.*")
        broker.publish("events.click", {"x": 100})

        messages = broker.poll("sub1")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].topic, "events.click")

    # ------------------------------------------------------------------
    # 4. Wildcard pattern: 'events.*' does NOT match 'events.click.button'
    # ------------------------------------------------------------------

    def test_wildcard_does_not_match_deep_segment(self):
        """'events.*' should NOT match 'events.click.button' (too many segments)."""
        broker = PubSubBroker()
        broker.create_topic("events.click.button")
        broker.subscribe("sub1", "events.*")
        broker.publish("events.click.button", {"detail": "deep"})

        messages = broker.poll("sub1")
        self.assertEqual(len(messages), 0)

    # ------------------------------------------------------------------
    # 5. Exact pattern: 'events.click' matches 'events.click'
    # ------------------------------------------------------------------

    def test_exact_pattern_match(self):
        """An exact pattern should match the identical topic."""
        broker = PubSubBroker()
        broker.create_topic("events.click")
        broker.subscribe("sub1", "events.click")
        broker.publish("events.click", {"type": "exact"})

        messages = broker.poll("sub1")
        self.assertEqual(len(messages), 1)

    # ------------------------------------------------------------------
    # 6. Message ordering: messages received in publish order
    # ------------------------------------------------------------------

    def test_message_ordering(self):
        """Messages should be delivered in the order they were published."""
        broker = PubSubBroker()
        broker.create_topic("log")
        broker.subscribe("sub1", "log")

        for i in range(5):
            broker.publish("log", {"seq": i})

        messages = broker.poll("sub1", max_messages=10)
        self.assertEqual(len(messages), 5)
        for i, msg in enumerate(messages):
            self.assertEqual(msg.payload["seq"], i)

    # ------------------------------------------------------------------
    # 7. Ack removes message from pending
    # ------------------------------------------------------------------

    def test_ack_removes_from_pending(self):
        """Acknowledged messages should not appear in subsequent polls."""
        broker = PubSubBroker()
        broker.create_topic("tasks")
        broker.subscribe("sub1", "tasks")

        broker.publish("tasks", {"item": "a"})
        broker.publish("tasks", {"item": "b"})

        messages = broker.poll("sub1")
        self.assertEqual(len(messages), 2)

        # Ack the first message
        broker.ack("sub1", messages[0].message_id)

        # Poll again -- only the un-acked message should remain
        remaining = broker.poll("sub1")
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].payload["item"], "b")

    # ------------------------------------------------------------------
    # 8. get_pending_count accurate
    # ------------------------------------------------------------------

    def test_get_pending_count(self):
        """get_pending_count should reflect the number of unacknowledged messages."""
        broker = PubSubBroker()
        broker.create_topic("data")
        broker.subscribe("sub1", "data")

        self.assertEqual(broker.get_pending_count("sub1"), 0)

        broker.publish("data", {"v": 1})
        broker.publish("data", {"v": 2})
        broker.publish("data", {"v": 3})
        self.assertEqual(broker.get_pending_count("sub1"), 3)

        messages = broker.poll("sub1")
        broker.ack("sub1", messages[0].message_id)
        self.assertEqual(broker.get_pending_count("sub1"), 2)

    # ------------------------------------------------------------------
    # 9. Unsubscribe: no longer receives messages
    # ------------------------------------------------------------------

    def test_unsubscribe(self):
        """After unsubscribing, a subscriber should not receive new messages."""
        broker = PubSubBroker()
        broker.create_topic("updates")
        broker.subscribe("sub1", "updates")

        broker.publish("updates", {"v": 1})
        self.assertEqual(len(broker.poll("sub1")), 1)

        broker.unsubscribe("sub1", "updates")
        broker.publish("updates", {"v": 2})

        # Ack the first message so only truly new messages would show
        msgs = broker.poll("sub1")
        # The subscriber should not have received the second message
        new_payloads = [m.payload for m in msgs if m.payload.get("v") == 2]
        self.assertEqual(len(new_payloads), 0,
                         "Unsubscribed subscriber still received new messages.")

    # ------------------------------------------------------------------
    # 10. Duplicate topic creation raises ValueError
    # ------------------------------------------------------------------

    def test_duplicate_topic_raises(self):
        """Creating the same topic twice should raise ValueError."""
        broker = PubSubBroker()
        broker.create_topic("unique")
        with self.assertRaises(ValueError):
            broker.create_topic("unique")

    # ------------------------------------------------------------------
    # 11. poll respects max_messages limit
    # ------------------------------------------------------------------

    def test_poll_max_messages(self):
        """poll(max_messages=N) should return at most N messages."""
        broker = PubSubBroker()
        broker.create_topic("stream")
        broker.subscribe("sub1", "stream")

        for i in range(10):
            broker.publish("stream", {"i": i})

        messages = broker.poll("sub1", max_messages=3)
        self.assertEqual(len(messages), 3)

    # ------------------------------------------------------------------
    # 12. Publishing with no subscribers doesn't error
    # ------------------------------------------------------------------

    def test_publish_no_subscribers(self):
        """Publishing to a topic with no subscribers should not raise."""
        broker = PubSubBroker()
        broker.create_topic("lonely")
        # Should not raise
        msg_id = broker.publish("lonely", {"data": "ignored"})
        self.assertIsInstance(msg_id, str)
        self.assertGreater(len(msg_id), 0)


if __name__ == "__main__":
    unittest.main()
