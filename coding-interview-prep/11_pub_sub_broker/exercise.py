"""
Pub/Sub Message Broker
======================
Category   : Full-Stack / Systems
Difficulty : ** (2/5)

Problem
-------
Implement an in-memory publish/subscribe message broker with:

1. **Topic management** -- create named topics that publishers can send
   messages to.
2. **Wildcard subscriptions** -- subscribers can register patterns using '*'
   as a wildcard segment (e.g. 'events.*' matches 'events.click' and
   'events.scroll').
3. **Message acknowledgement** -- delivered messages stay pending until the
   subscriber explicitly acknowledges them, enabling at-least-once delivery
   semantics.

Real-world motivation
---------------------
Pub/sub messaging is a core pattern in modern distributed systems:
  - Google Cloud Pub/Sub, AWS SNS/SQS, and Apache Kafka all implement
    topic-based publish/subscribe with varying delivery guarantees.
  - Wildcard subscriptions allow flexible routing (e.g. MQTT uses '+' and
    '#' wildcards for IoT device communication).
  - Acknowledgement-based delivery ensures no messages are silently lost
    when a consumer crashes mid-processing.

Building a pub/sub broker from scratch teaches you about decoupled
communication, fan-out patterns, and reliable message delivery.

Hints
-----
1. Store topics in a set or dict to enforce uniqueness.
2. For wildcard matching, convert the pattern 'events.*' into a regex like
   '^events\\.[^.]+$' and test topics against it.
3. Each subscriber needs its own message queue (a list or deque) so that
   messages are independently tracked per subscriber.
4. Separate pending (unacknowledged) messages from acknowledged ones so
   that poll() only returns messages not yet acknowledged.

Run command
-----------
    pytest 11_pub_sub_broker/test_exercise.py -v
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

    Publishers send messages to topics.  Subscribers register interest via
    patterns (which may contain '*' wildcards) and receive copies of all
    matching messages in their personal queues.
    """

    def __init__(self) -> None:
        """Initialise the broker.

        Sets up data structures for topics, subscriber patterns, and
        per-subscriber message queues.
        """
        # TODO: Create a set (or dict) of known topics.
        # TODO: Create a mapping from subscriber_id -> list of topic patterns.
        # TODO: Create per-subscriber message queues for pending messages.
        # TODO: Create per-subscriber sets for acknowledged message IDs.
        # Hint: defaultdict is handy for the queues and subscription lists.
        pass

    def create_topic(self, topic: str) -> None:
        """Register a new topic.

        Args:
            topic: The name of the topic to create.

        Raises:
            ValueError: If the topic already exists.
        """
        # TODO: Check if topic already exists; raise ValueError if so.
        # TODO: Add the topic to the topics set.
        pass

    def subscribe(self, subscriber_id: str, topic_pattern: str) -> None:
        """Subscribe to a topic pattern.

        The pattern may contain '*' as a wildcard matching exactly one
        segment (e.g. 'events.*' matches 'events.click' but not
        'events.click.button').

        Args:
            subscriber_id: Unique identifier for the subscriber.
            topic_pattern: A topic name or wildcard pattern to subscribe to.
        """
        # TODO: Store the topic_pattern for the subscriber.
        # Hint: Maintain a list of patterns per subscriber_id.
        pass

    def unsubscribe(self, subscriber_id: str, topic_pattern: str) -> None:
        """Remove a subscription.

        Args:
            subscriber_id: The subscriber to unsubscribe.
            topic_pattern: The exact pattern string to remove.
        """
        # TODO: Remove the topic_pattern from the subscriber's pattern list.
        pass

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
        # TODO: Convert the pattern to a regex and test the topic.
        # Hint: Replace '*' with '[^.]+' and anchor with ^ and $.
        #       re.fullmatch(regex, topic) is convenient here.
        pass

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
        # TODO: Create a Message with the topic and payload.
        # TODO: For each subscriber, check each of their patterns against
        #       the topic.  If any pattern matches, add the message to the
        #       subscriber's pending queue.
        # TODO: Return the message_id.
        # Hint: A subscriber should receive at most one copy even if
        #       multiple patterns match.
        pass

    def poll(self, subscriber_id: str, max_messages: int = 10) -> list:
        """Retrieve pending (unacknowledged) messages for a subscriber.

        Args:
            subscriber_id: The subscriber whose queue to read.
            max_messages: Maximum number of messages to return.

        Returns:
            A list of Message objects that have not yet been acknowledged,
            oldest first, up to max_messages.
        """
        # TODO: Return up to max_messages from the subscriber's pending
        #       queue that have not been acknowledged.
        # Hint: Filter out messages whose message_id is in the acked set.
        pass

    def ack(self, subscriber_id: str, message_id: str) -> None:
        """Acknowledge a message, marking it as processed.

        Once acknowledged, the message will no longer appear in poll()
        results for this subscriber.

        Args:
            subscriber_id: The subscriber acknowledging the message.
            message_id: The ID of the message to acknowledge.
        """
        # TODO: Add the message_id to the subscriber's acknowledged set.
        pass

    def get_pending_count(self, subscriber_id: str) -> int:
        """Return the number of unacknowledged messages for a subscriber.

        Args:
            subscriber_id: The subscriber to check.

        Returns:
            The count of pending (unacknowledged) messages.
        """
        # TODO: Count messages in the subscriber's queue that have not
        #       been acknowledged.
        pass
