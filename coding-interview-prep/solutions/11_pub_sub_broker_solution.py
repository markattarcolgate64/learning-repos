"""
Pub/Sub Message Broker - Solution

An in-memory publish/subscribe message broker with topic management,
wildcard subscriptions (using '*' for single-segment matching), and
message acknowledgement for at-least-once delivery semantics.
"""

from collections import defaultdict
from dataclasses import dataclass, field
import time
import re
import uuid


@dataclass
class Message:
    """A single message published to a topic.

    Attributes:
        topic: The topic this message was published to.
        payload: Arbitrary dict containing the message data.
        message_id: Unique identifier, auto-generated if not provided.
        timestamp: Unix timestamp when the message was created.
    """

    topic: str
    payload: dict
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)


class PubSubBroker:
    """An in-memory pub/sub message broker with wildcard subscriptions and
    message acknowledgement.

    Publishers send messages to topics. Subscribers register interest via
    patterns (which may contain '*' wildcards) and receive copies of all
    matching messages in their personal queues.
    """

    def __init__(self) -> None:
        """Initialise the broker."""
        self.topics = set()
        self.subscriptions = defaultdict(list)
        self.queues = defaultdict(list)
        self.acked = defaultdict(set)

    def create_topic(self, topic: str) -> None:
        """Register a new topic.

        Args:
            topic: The name of the topic to create.

        Raises:
            ValueError: If the topic already exists.
        """
        if topic in self.topics:
            raise ValueError(f"Topic '{topic}' already exists")
        self.topics.add(topic)

    def subscribe(self, subscriber_id: str, topic_pattern: str) -> None:
        """Subscribe to a topic pattern.

        The pattern may contain '*' as a wildcard matching exactly one
        segment (e.g. 'events.*' matches 'events.click' but not
        'events.click.button').

        Args:
            subscriber_id: Unique identifier for the subscriber.
            topic_pattern: A topic name or wildcard pattern to subscribe to.
        """
        self.subscriptions[subscriber_id].append(topic_pattern)

    def unsubscribe(self, subscriber_id: str, topic_pattern: str) -> None:
        """Remove a subscription.

        Args:
            subscriber_id: The subscriber to unsubscribe.
            topic_pattern: The exact pattern string to remove.
        """
        if subscriber_id in self.subscriptions:
            self.subscriptions[subscriber_id].remove(topic_pattern)

    def _matches(self, topic: str, pattern: str) -> bool:
        """Test whether a topic name matches a subscription pattern.

        The '*' wildcard in a pattern matches exactly one dot-separated
        segment.

        Args:
            topic: The actual topic name (e.g. 'events.click').
            pattern: The subscription pattern (e.g. 'events.*').

        Returns:
            True if the topic matches the pattern, False otherwise.
        """
        regex = '^' + re.escape(pattern).replace(r'\*', '[^.]+') + '$'
        return re.fullmatch(regex, topic) is not None

    def publish(self, topic: str, payload: dict) -> str:
        """Publish a message to a topic.

        Creates a Message and delivers it to the pending queue of every
        subscriber whose pattern matches the topic.

        Args:
            topic: The topic to publish to.
            payload: The message data.

        Returns:
            The auto-generated message_id of the published message.
        """
        message = Message(topic=topic, payload=payload)

        for subscriber_id, patterns in self.subscriptions.items():
            if any(self._matches(topic, pattern) for pattern in patterns):
                self.queues[subscriber_id].append(message)

        return message.message_id

    def poll(self, subscriber_id: str, max_messages: int = 10) -> list:
        """Retrieve pending (unacknowledged) messages for a subscriber.

        Args:
            subscriber_id: The subscriber whose queue to read.
            max_messages: Maximum number of messages to return.

        Returns:
            A list of Message objects that have not yet been acknowledged,
            oldest first, up to max_messages.
        """
        acked_ids = self.acked[subscriber_id]
        pending = [
            msg for msg in self.queues[subscriber_id]
            if msg.message_id not in acked_ids
        ]
        return pending[:max_messages]

    def ack(self, subscriber_id: str, message_id: str) -> None:
        """Acknowledge a message, marking it as processed.

        Args:
            subscriber_id: The subscriber acknowledging the message.
            message_id: The ID of the message to acknowledge.
        """
        self.acked[subscriber_id].add(message_id)

    def get_pending_count(self, subscriber_id: str) -> int:
        """Return the number of unacknowledged messages for a subscriber.

        Args:
            subscriber_id: The subscriber to check.

        Returns:
            The count of pending (unacknowledged) messages.
        """
        acked_ids = self.acked[subscriber_id]
        return sum(
            1 for msg in self.queues[subscriber_id]
            if msg.message_id not in acked_ids
        )
