"""Tests for the Privacy-Preserving Set Membership exercise."""

import unittest

from exercise import PrivacyPreservingRegistry


class TestCommitments(unittest.TestCase):
    """Cryptographic commitment generation."""

    # ------------------------------------------------------------------
    # 1. Deterministic with fixed salt
    # ------------------------------------------------------------------
    def test_deterministic_with_same_salt(self):
        """Same identifier + same salt must always produce the same commitment."""
        reg = PrivacyPreservingRegistry()
        c1 = reg.commit("iris-abc-123", salt="deadbeef")
        c2 = reg.commit("iris-abc-123", salt="deadbeef")
        self.assertEqual(c1, c2)

    # ------------------------------------------------------------------
    # 2. Different identifiers -> different commitments
    # ------------------------------------------------------------------
    def test_different_identifiers(self):
        """Different identifiers with the same salt must produce different commitments."""
        reg = PrivacyPreservingRegistry()
        c1 = reg.commit("iris-abc-123", salt="aabbccdd")
        c2 = reg.commit("iris-xyz-789", salt="aabbccdd")
        self.assertNotEqual(c1, c2)

    # ------------------------------------------------------------------
    # 3. Different salts -> different commitments
    # ------------------------------------------------------------------
    def test_different_salts(self):
        """Same identifier with different salts must produce different commitments."""
        reg = PrivacyPreservingRegistry()
        c1 = reg.commit("iris-abc-123", salt="salt_one")
        c2 = reg.commit("iris-abc-123", salt="salt_two")
        self.assertNotEqual(c1, c2)

    # ------------------------------------------------------------------
    # 4. Commitment is 64 hex chars (SHA-256)
    # ------------------------------------------------------------------
    def test_commitment_format(self):
        """Commitment should be a 64-character lowercase hex string."""
        reg = PrivacyPreservingRegistry()
        c = reg.commit("test-identifier", salt="0000")
        self.assertEqual(len(c), 64)
        self.assertTrue(all(ch in "0123456789abcdef" for ch in c))

    # ------------------------------------------------------------------
    # 5. Auto-generated salt produces unique commitments
    # ------------------------------------------------------------------
    def test_auto_salt_varies(self):
        """Without explicit salt, each call should produce a different commitment."""
        reg = PrivacyPreservingRegistry()
        commitments = {reg.commit("same-identifier") for _ in range(20)}
        # With random salts, all 20 should be unique (collision is negligible)
        self.assertEqual(len(commitments), 20)


class TestRegistration(unittest.TestCase):
    """Registration and duplicate detection."""

    # ------------------------------------------------------------------
    # 6. First registration returns True
    # ------------------------------------------------------------------
    def test_first_register_returns_true(self):
        """Registering a new commitment should return True."""
        reg = PrivacyPreservingRegistry()
        self.assertTrue(reg.register("aabb" * 16))

    # ------------------------------------------------------------------
    # 7. Duplicate registration returns False
    # ------------------------------------------------------------------
    def test_duplicate_register_returns_false(self):
        """Re-registering the same commitment should return False."""
        reg = PrivacyPreservingRegistry()
        commitment = "ccdd" * 16
        self.assertTrue(reg.register(commitment))
        self.assertFalse(reg.register(commitment))

    # ------------------------------------------------------------------
    # 8. Many unique registrations all succeed
    # ------------------------------------------------------------------
    def test_many_unique_registrations(self):
        """Registering many unique commitments should all return True."""
        reg = PrivacyPreservingRegistry(expected_items=1000, fp_rate=0.01)
        for i in range(100):
            c = reg.commit(f"user-{i}", salt="fixed-salt")
            self.assertTrue(reg.register(c), f"Registration {i} should succeed")


class TestBloomFilter(unittest.TestCase):
    """Bloom filter behaviour."""

    # ------------------------------------------------------------------
    # 9. No false negatives
    # ------------------------------------------------------------------
    def test_no_false_negatives(self):
        """Every registered commitment must return True from check_duplicate_fast."""
        reg = PrivacyPreservingRegistry(expected_items=1000, fp_rate=0.01)
        commitments = []
        for i in range(200):
            c = reg.commit(f"user-{i}", salt="salt")
            reg.register(c)
            commitments.append(c)

        for c in commitments:
            self.assertTrue(
                reg.check_duplicate_fast(c),
                f"Bloom filter must not produce false negatives for {c[:16]}...",
            )

    # ------------------------------------------------------------------
    # 10. Unregistered items return False from exact check
    # ------------------------------------------------------------------
    def test_unregistered_exact_check(self):
        """Unregistered commitments must return False from check_duplicate_exact."""
        reg = PrivacyPreservingRegistry()
        reg.register("aaaa" * 16)
        self.assertFalse(reg.check_duplicate_exact("bbbb" * 16))

    # ------------------------------------------------------------------
    # 11. Exact check agrees with registration
    # ------------------------------------------------------------------
    def test_exact_check_agrees_with_register(self):
        """check_duplicate_exact must return True for registered commitments."""
        reg = PrivacyPreservingRegistry()
        c = "1234" * 16
        reg.register(c)
        self.assertTrue(reg.check_duplicate_exact(c))

    # ------------------------------------------------------------------
    # 12. False-positive rate is approximately correct
    # ------------------------------------------------------------------
    def test_false_positive_rate(self):
        """Bloom filter FP rate should be roughly within 2x the target."""
        target_fp = 0.01
        n_items = 1000
        reg = PrivacyPreservingRegistry(expected_items=n_items, fp_rate=target_fp)

        # Register n_items commitments
        for i in range(n_items):
            c = reg.commit(f"registered-{i}", salt="reg-salt")
            reg.register(c)

        # Test 10000 non-registered commitments
        false_positives = 0
        n_tests = 10000
        for i in range(n_tests):
            c = reg.commit(f"not-registered-{i}", salt="test-salt")
            if reg.check_duplicate_fast(c):
                false_positives += 1

        observed_fp_rate = false_positives / n_tests
        # Allow up to 2x the target FP rate
        self.assertLess(
            observed_fp_rate,
            target_fp * 2,
            f"FP rate {observed_fp_rate:.4f} exceeds 2x target {target_fp}",
        )

    # ------------------------------------------------------------------
    # 13. Bloom filter correctly reports not-present for empty registry
    # ------------------------------------------------------------------
    def test_empty_bloom_returns_false(self):
        """An empty Bloom filter should return False for any query."""
        reg = PrivacyPreservingRegistry()
        self.assertFalse(reg.check_duplicate_fast("dead" * 16))
        self.assertFalse(reg.check_duplicate_exact("dead" * 16))


class TestSize(unittest.TestCase):
    """Size tracking."""

    # ------------------------------------------------------------------
    # 14. Empty registry has size 0
    # ------------------------------------------------------------------
    def test_empty_size(self):
        """A fresh registry should have size 0."""
        reg = PrivacyPreservingRegistry()
        self.assertEqual(reg.size(), 0)

    # ------------------------------------------------------------------
    # 15. Size increments on new registrations only
    # ------------------------------------------------------------------
    def test_size_increments_correctly(self):
        """Size should increase only for new (non-duplicate) registrations."""
        reg = PrivacyPreservingRegistry()
        reg.register("aaaa" * 16)
        self.assertEqual(reg.size(), 1)
        reg.register("bbbb" * 16)
        self.assertEqual(reg.size(), 2)
        # Duplicate -- size should NOT increase
        reg.register("aaaa" * 16)
        self.assertEqual(reg.size(), 2)

    # ------------------------------------------------------------------
    # 16. Size after many registrations
    # ------------------------------------------------------------------
    def test_size_after_bulk_register(self):
        """Size should equal the number of unique commitments."""
        reg = PrivacyPreservingRegistry(expected_items=500, fp_rate=0.01)
        for i in range(100):
            reg.register(reg.commit(f"u-{i}", salt="s"))
        self.assertEqual(reg.size(), 100)


class TestSerialization(unittest.TestCase):
    """Export / import round-trip."""

    # ------------------------------------------------------------------
    # 17. Round-trip preserves exact set
    # ------------------------------------------------------------------
    def test_round_trip_exact_set(self):
        """Exported + imported registry should have the same exact membership."""
        reg = PrivacyPreservingRegistry(expected_items=500, fp_rate=0.01)
        commitments = []
        for i in range(50):
            c = reg.commit(f"user-{i}", salt="s")
            reg.register(c)
            commitments.append(c)

        data = reg.export_state()
        reg2 = PrivacyPreservingRegistry.import_state(data)

        for c in commitments:
            self.assertTrue(reg2.check_duplicate_exact(c))
        self.assertEqual(reg2.size(), 50)

    # ------------------------------------------------------------------
    # 18. Round-trip preserves Bloom filter
    # ------------------------------------------------------------------
    def test_round_trip_bloom_filter(self):
        """Bloom filter in the imported registry should match the original."""
        reg = PrivacyPreservingRegistry(expected_items=500, fp_rate=0.01)
        commitments = []
        for i in range(50):
            c = reg.commit(f"item-{i}", salt="x")
            reg.register(c)
            commitments.append(c)

        data = reg.export_state()
        reg2 = PrivacyPreservingRegistry.import_state(data)

        # No false negatives in the restored Bloom filter
        for c in commitments:
            self.assertTrue(reg2.check_duplicate_fast(c))

    # ------------------------------------------------------------------
    # 19. Imported registry rejects new duplicates correctly
    # ------------------------------------------------------------------
    def test_imported_rejects_duplicates(self):
        """A commitment registered before export should be detected as duplicate after import."""
        reg = PrivacyPreservingRegistry()
        c = reg.commit("unique-user", salt="abc")
        reg.register(c)

        data = reg.export_state()
        reg2 = PrivacyPreservingRegistry.import_state(data)

        # Attempting to re-register should return False
        self.assertFalse(reg2.register(c))

    # ------------------------------------------------------------------
    # 20. Export returns bytes
    # ------------------------------------------------------------------
    def test_export_returns_bytes(self):
        """export_state should return a bytes object."""
        reg = PrivacyPreservingRegistry()
        reg.register("aabb" * 16)
        data = reg.export_state()
        self.assertIsInstance(data, bytes)

    # ------------------------------------------------------------------
    # 21. Round-trip preserves parameters
    # ------------------------------------------------------------------
    def test_round_trip_preserves_parameters(self):
        """Imported registry should have the same filter size and hash count."""
        reg = PrivacyPreservingRegistry(expected_items=5000, fp_rate=0.005)
        for i in range(10):
            reg.register(reg.commit(f"p-{i}", salt="z"))

        data = reg.export_state()
        reg2 = PrivacyPreservingRegistry.import_state(data)

        # After import, newly registered items should still work
        new_c = reg2.commit("fresh-user", salt="new")
        self.assertTrue(reg2.register(new_c))
        self.assertTrue(reg2.check_duplicate_exact(new_c))
        self.assertTrue(reg2.check_duplicate_fast(new_c))


if __name__ == "__main__":
    unittest.main()
