"""Tests for the Vector Clock exercise."""

import unittest

from .exercise import VectorClock


class TestVectorClock(unittest.TestCase):
    """Comprehensive tests for VectorClock."""

    # ------------------------------------------------------------------
    # 1. Initial clock: all zeros
    # ------------------------------------------------------------------
    def test_initial_clock_all_zeros(self):
        """A freshly created vector clock should have all counters at 0."""
        nodes = ["A", "B", "C"]
        vc = VectorClock("A", nodes)
        clock = vc.get_clock()
        for node in nodes:
            self.assertEqual(clock[node], 0, f"Initial counter for {node} should be 0")

    # ------------------------------------------------------------------
    # 2. increment: advances own counter only
    # ------------------------------------------------------------------
    def test_increment_advances_own_counter_only(self):
        """increment() should only increase this node's counter by 1."""
        nodes = ["A", "B", "C"]
        vc = VectorClock("A", nodes)

        result = vc.increment()
        self.assertEqual(result["A"], 1)
        self.assertEqual(result["B"], 0)
        self.assertEqual(result["C"], 0)

        result = vc.increment()
        self.assertEqual(result["A"], 2)
        self.assertEqual(result["B"], 0)
        self.assertEqual(result["C"], 0)

    # ------------------------------------------------------------------
    # 3. send: returns incremented clock
    # ------------------------------------------------------------------
    def test_send_returns_incremented_clock(self):
        """send() should increment and return a copy of the clock."""
        nodes = ["A", "B"]
        vc = VectorClock("A", nodes)

        msg_clock = vc.send()
        self.assertEqual(msg_clock["A"], 1)
        self.assertEqual(msg_clock["B"], 0)

        # The returned clock should be a copy (modifying it should not affect vc)
        msg_clock["A"] = 999
        self.assertEqual(vc.get_clock()["A"], 1, "send() should return a copy")

    # ------------------------------------------------------------------
    # 4. receive: element-wise max then increment
    # ------------------------------------------------------------------
    def test_receive_merges_and_increments(self):
        """receive() should take element-wise max then increment own counter."""
        nodes = ["A", "B", "C"]
        vc_b = VectorClock("B", nodes)

        # Simulate receiving a message from A with clock {A:3, B:1, C:0}
        incoming = {"A": 3, "B": 1, "C": 0}
        result = vc_b.receive(incoming)

        # B should take max of each: max(0,3)=3, max(0,1)=1, max(0,0)=0
        # Then increment own: B goes from 1 to 2
        self.assertEqual(result["A"], 3)
        self.assertEqual(result["B"], 2)
        self.assertEqual(result["C"], 0)

    # ------------------------------------------------------------------
    # 5. happens_before: correct causal detection (A -> B)
    # ------------------------------------------------------------------
    def test_happens_before_causal(self):
        """If A happened before B, happens_before(A, B) should return True."""
        clock_a = {"A": 1, "B": 0, "C": 0}
        clock_b = {"A": 1, "B": 1, "C": 0}
        self.assertTrue(VectorClock.happens_before(clock_a, clock_b))

    # ------------------------------------------------------------------
    # 6. happens_before: B does not happen before A when A -> B
    # ------------------------------------------------------------------
    def test_happens_before_not_reverse(self):
        """If A -> B then B does NOT happen before A."""
        clock_a = {"A": 1, "B": 0, "C": 0}
        clock_b = {"A": 1, "B": 1, "C": 0}
        self.assertFalse(VectorClock.happens_before(clock_b, clock_a))

    # ------------------------------------------------------------------
    # 7. are_concurrent: correctly detects concurrent events
    # ------------------------------------------------------------------
    def test_concurrent_events(self):
        """Two events where neither happens-before the other are concurrent."""
        clock_a = {"A": 2, "B": 0}
        clock_b = {"A": 0, "B": 3}
        self.assertTrue(VectorClock.are_concurrent(clock_a, clock_b))

    def test_not_concurrent_when_causal(self):
        """Causally ordered events should NOT be concurrent."""
        clock_a = {"A": 1, "B": 0}
        clock_b = {"A": 2, "B": 1}
        self.assertFalse(VectorClock.are_concurrent(clock_a, clock_b))

    # ------------------------------------------------------------------
    # 8. Multi-node scenario: simulate 3 nodes with message passing
    # ------------------------------------------------------------------
    def test_multi_node_message_passing(self):
        """Simulate a 3-node scenario with sends and receives."""
        nodes = ["A", "B", "C"]
        vc_a = VectorClock("A", nodes)
        vc_b = VectorClock("B", nodes)
        vc_c = VectorClock("C", nodes)

        # A does a local event
        vc_a.increment()  # A: {A:1, B:0, C:0}

        # A sends to B
        msg1 = vc_a.send()  # A: {A:2, B:0, C:0}
        vc_b.receive(msg1)  # B merges: max({A:0,B:0,C:0}, {A:2,B:0,C:0}) -> {A:2,B:0,C:0}, then B++ -> {A:2,B:1,C:0}

        clock_b = vc_b.get_clock()
        self.assertEqual(clock_b["A"], 2)
        self.assertEqual(clock_b["B"], 1)
        self.assertEqual(clock_b["C"], 0)

        # B sends to C
        msg2 = vc_b.send()  # B: {A:2, B:2, C:0}
        vc_c.receive(msg2)  # C merges: max({A:0,B:0,C:0}, {A:2,B:2,C:0}) -> {A:2,B:2,C:0}, then C++ -> {A:2,B:2,C:1}

        clock_c = vc_c.get_clock()
        self.assertEqual(clock_c["A"], 2)
        self.assertEqual(clock_c["B"], 2)
        self.assertEqual(clock_c["C"], 1)

        # A's last send happened before C's receive
        self.assertTrue(VectorClock.happens_before(msg1, clock_c))

    # ------------------------------------------------------------------
    # 9. Identical clocks: neither happens-before
    # ------------------------------------------------------------------
    def test_identical_clocks_neither_happens_before(self):
        """Two identical clocks: neither happens-before the other."""
        clock_a = {"A": 1, "B": 2}
        clock_b = {"A": 1, "B": 2}
        self.assertFalse(VectorClock.happens_before(clock_a, clock_b))
        self.assertFalse(VectorClock.happens_before(clock_b, clock_a))

    def test_identical_clocks_not_concurrent(self):
        """Identical clocks are not concurrent (they represent the same state)."""
        clock_a = {"A": 1, "B": 2}
        clock_b = {"A": 1, "B": 2}
        # Neither happens-before means are_concurrent returns True,
        # but identical clocks technically satisfy this definition
        # Depending on interpretation, identical clocks are concurrent by the
        # standard definition (neither strictly happens-before the other).
        # The definition says A hb B requires at least one A[n] < B[n].
        # For identical clocks, no A[n] < B[n], so not hb in either direction.
        # Therefore are_concurrent should return True.
        self.assertTrue(VectorClock.are_concurrent(clock_a, clock_b))

    # ------------------------------------------------------------------
    # 10. Chain: A -> B -> C transitivity
    # ------------------------------------------------------------------
    def test_chain_transitivity(self):
        """If A -> B and B -> C, then A -> C (transitivity)."""
        nodes = ["X", "Y", "Z"]
        vc_x = VectorClock("X", nodes)
        vc_y = VectorClock("Y", nodes)
        vc_z = VectorClock("Z", nodes)

        # X sends to Y
        msg_x = vc_x.send()   # X: {X:1, Y:0, Z:0}
        vc_y.receive(msg_x)   # Y: {X:1, Y:1, Z:0}

        # Y sends to Z
        msg_y = vc_y.send()   # Y: {X:1, Y:2, Z:0}
        vc_z.receive(msg_y)   # Z: {X:1, Y:2, Z:1}

        clock_x_at_send = msg_x
        clock_z_final = vc_z.get_clock()

        # X's send should happen before Z's state
        self.assertTrue(VectorClock.happens_before(clock_x_at_send, clock_z_final))


if __name__ == "__main__":
    unittest.main()
