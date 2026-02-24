"""
Vector Clock
=============
Category   : Distributed Systems
Difficulty : ** (2/5)

Problem
-------
Implement vector clocks for establishing causal ordering of events across nodes
in a distributed system.

Each node maintains a vector (dictionary) of counters, one per node.  A node
increments its own counter on every local event.  When sending a message it
attaches its current clock.  When receiving a message it merges the incoming
clock with its own by taking the element-wise maximum, then increments its own
counter.

Two events can be compared:
  - A *happens-before* B  iff  all A[n] <= B[n] and there exists at least one
    n where A[n] < B[n].
  - A and B are *concurrent* iff neither happens-before the other.

Real-world motivation
---------------------
Vector clocks (and their lighter-weight cousins, version vectors) are used in
systems like Amazon DynamoDB, Riak, and distributed version-control systems to
detect conflicting writes without a centralised clock.  Understanding causal
ordering is foundational to any distributed-systems interview.

Hints
-----
1. `increment` only touches self.clock[self.node_id].
2. `send` is just increment + return a copy of the clock.
3. `receive` merges element-wise max, *then* increments own counter.
4. For `happens_before`, iterate over *all* keys present in either clock.
5. Two clocks are concurrent when neither happens-before the other.

Run command
-----------
    pytest 04_vector_clock/test_exercise.py -v
"""


class VectorClock:
    """A vector clock for a single node in a distributed system.

    Maintains a dictionary mapping every known node ID to a logical counter.
    Provides operations for local events, sending, receiving, and comparing
    causal order between clocks.
    """

    def __init__(self, node_id: str, all_nodes: list) -> None:
        """Initialise the vector clock.

        Args:
            node_id: The identifier of the node that owns this clock.
            all_nodes: A list of all node identifiers in the system.
        """
        # TODO: Store node_id.
        # TODO: Initialise self.clock as a dict mapping each node in
        #       all_nodes to 0.
        # Hint: self.clock = {node: 0 for node in all_nodes}
        pass

    def increment(self) -> dict:
        """Record a local event by incrementing this node's own counter.

        Returns:
            A copy of the updated clock dictionary.
        """
        # TODO: Increment self.clock[self.node_id] by 1.
        # TODO: Return a copy of self.clock.
        pass

    def send(self) -> dict:
        """Prepare a clock to attach to an outgoing message.

        Increments the local counter (a send is a local event) and returns a
        copy of the clock to be included with the message.

        Returns:
            A copy of the clock dictionary after incrementing.
        """
        # TODO: Call increment() and return the result.
        # Hint: Sending is just a local event whose clock is attached to the
        #       message.
        pass

    def receive(self, other_clock: dict) -> dict:
        """Merge an incoming clock with the local clock.

        For every node, takes the element-wise maximum of the local and
        incoming counters.  Then increments this node's own counter (receiving
        is also a local event).

        Args:
            other_clock: The clock dictionary received from another node.

        Returns:
            A copy of the updated clock dictionary after merging and
            incrementing.
        """
        # TODO: For each node in self.clock, set the value to
        #       max(self.clock[node], other_clock.get(node, 0)).
        # TODO: Then increment self.clock[self.node_id] by 1.
        # TODO: Return a copy of self.clock.
        pass

    def get_clock(self) -> dict:
        """Return a copy of the current clock state.

        Returns:
            A dictionary mapping node IDs to their current counter values.
        """
        # TODO: Return a copy of self.clock.
        # Hint: return dict(self.clock)
        pass

    @staticmethod
    def happens_before(clock_a: dict, clock_b: dict) -> bool:
        """Determine whether clock_a causally happens before clock_b.

        A happens-before B iff for every node n, A[n] <= B[n], **and** there
        exists at least one node n where A[n] < B[n].

        Args:
            clock_a: The first clock dictionary.
            clock_b: The second clock dictionary.

        Returns:
            True if clock_a causally precedes clock_b, False otherwise.
        """
        # TODO: Collect all keys from both clocks.
        # TODO: Check that every A[n] <= B[n].
        # TODO: Check that at least one A[n] < B[n].
        # Hint: Use clock_a.get(node, 0) and clock_b.get(node, 0) for safe
        #       lookups.
        pass

    @staticmethod
    def are_concurrent(clock_a: dict, clock_b: dict) -> bool:
        """Determine whether two clocks are concurrent (causally unordered).

        Two events are concurrent iff neither happens-before the other.

        Args:
            clock_a: The first clock dictionary.
            clock_b: The second clock dictionary.

        Returns:
            True if the two clocks are concurrent, False otherwise.
        """
        # TODO: Return True iff not happens_before(A, B) and not
        #       happens_before(B, A).
        pass
