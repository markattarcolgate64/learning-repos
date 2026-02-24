"""
Vector Clock - Solution

Vector clocks for tracking causality in distributed systems.
Each node maintains a vector of logical timestamps, one per node.
"""

from typing import Dict, List


class VectorClock:
    def __init__(self, node_id: str, all_nodes: List[str]):
        """
        Initialize a vector clock for a node.

        Args:
            node_id: Identifier for this node.
            all_nodes: List of all node identifiers in the system.
        """
        self.node_id = node_id
        self.clock = {n: 0 for n in all_nodes}

    def increment(self) -> Dict[str, int]:
        """
        Increment this node's own entry in the vector clock.

        Returns:
            A copy of the updated clock.
        """
        self.clock[self.node_id] += 1
        return dict(self.clock)

    def send(self) -> Dict[str, int]:
        """
        Prepare the clock for a send event. Increments own counter
        and returns the clock to be sent with the message.

        Returns:
            A copy of the clock to include with the outgoing message.
        """
        return self.increment()

    def receive(self, other_clock: Dict[str, int]) -> Dict[str, int]:
        """
        Process a received clock from another node. Merges by taking
        the element-wise maximum, then increments own counter.

        Args:
            other_clock: The vector clock received from another node.

        Returns:
            A copy of the updated clock after merging and incrementing.
        """
        for node in self.clock:
            if node in other_clock:
                self.clock[node] = max(self.clock[node], other_clock[node])
        self.clock[self.node_id] += 1
        return dict(self.clock)

    def get_clock(self) -> Dict[str, int]:
        """
        Return a copy of the current vector clock state.

        Returns:
            A dictionary mapping node IDs to their logical timestamps.
        """
        return dict(self.clock)

    @staticmethod
    def happens_before(a: Dict[str, int], b: Dict[str, int]) -> bool:
        """
        Determine if event a causally happened before event b.
        a happens-before b iff all a[n] <= b[n] and at least one a[n] < b[n].

        Args:
            a: Vector clock of event a.
            b: Vector clock of event b.

        Returns:
            True if a happened before b.
        """
        all_keys = set(a.keys()) | set(b.keys())
        at_least_one_less = False
        for key in all_keys:
            val_a = a.get(key, 0)
            val_b = b.get(key, 0)
            if val_a > val_b:
                return False
            if val_a < val_b:
                at_least_one_less = True
        return at_least_one_less

    @staticmethod
    def are_concurrent(a: Dict[str, int], b: Dict[str, int]) -> bool:
        """
        Determine if events a and b are concurrent (neither happened before the other).

        Args:
            a: Vector clock of event a.
            b: Vector clock of event b.

        Returns:
            True if a and b are concurrent.
        """
        return not VectorClock.happens_before(a, b) and not VectorClock.happens_before(b, a)
