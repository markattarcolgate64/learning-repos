"""Tests for the Secure Audit Log exercise."""

import json
import unittest

from exercise import AuditLog, GENESIS_HASH, LogEntry, compute_hash


class TestAuditLog(unittest.TestCase):
    """Comprehensive tests for the AuditLog hash-chain."""

    # ------------------------------------------------------------------
    # 1. Append creates correct hash chain
    # ------------------------------------------------------------------
    def test_append_chain_linkage(self):
        """Each entry's previous_hash equals the prior entry's entry_hash."""
        log = AuditLog()
        e0 = log.append("event-0", timestamp=1.0)
        e1 = log.append("event-1", timestamp=2.0)
        e2 = log.append("event-2", timestamp=3.0)

        self.assertEqual(e0.previous_hash, GENESIS_HASH)
        self.assertEqual(e1.previous_hash, e0.entry_hash)
        self.assertEqual(e2.previous_hash, e1.entry_hash)

    def test_append_computes_correct_hash(self):
        """Entry hash is SHA-256 of the canonical input string."""
        log = AuditLog()
        entry = log.append("hello", timestamp=42.0)

        expected = compute_hash(GENESIS_HASH, 0, 42.0, "hello")
        self.assertEqual(entry.entry_hash, expected)

    # ------------------------------------------------------------------
    # 2. Genesis entry
    # ------------------------------------------------------------------
    def test_genesis_previous_hash(self):
        """The first entry's previous_hash is GENESIS_HASH (64 zeros)."""
        log = AuditLog()
        entry = log.append("genesis-event", timestamp=0.0)
        self.assertEqual(entry.previous_hash, "0" * 64)
        self.assertEqual(entry.index, 0)

    # ------------------------------------------------------------------
    # 3. verify_integrity on untampered log
    # ------------------------------------------------------------------
    def test_verify_integrity_valid(self):
        """An untampered log passes integrity verification."""
        log = AuditLog()
        for i in range(20):
            log.append(f"event-{i}", timestamp=float(i))

        self.assertTrue(log.verify_integrity())

    def test_verify_integrity_empty_log(self):
        """An empty log is trivially valid."""
        log = AuditLog()
        self.assertTrue(log.verify_integrity())

    # ------------------------------------------------------------------
    # 4. verify_integrity detects tampered event_data
    # ------------------------------------------------------------------
    def test_verify_integrity_tampered_event_data(self):
        """Modifying event_data breaks the chain."""
        log = AuditLog()
        for i in range(5):
            log.append(f"event-{i}", timestamp=float(i))

        # Tamper with the middle entry's data
        log.get(2).event_data = "TAMPERED"

        self.assertFalse(log.verify_integrity())

    # ------------------------------------------------------------------
    # 5. verify_integrity detects tampered hash
    # ------------------------------------------------------------------
    def test_verify_integrity_tampered_hash(self):
        """Directly modifying an entry's hash breaks the chain."""
        log = AuditLog()
        for i in range(5):
            log.append(f"event-{i}", timestamp=float(i))

        # Tamper with entry 1's hash
        log.get(1).entry_hash = "deadbeef" * 8

        self.assertFalse(log.verify_integrity())

    # ------------------------------------------------------------------
    # 6. verify_range
    # ------------------------------------------------------------------
    def test_verify_range_valid_subrange(self):
        """A valid sub-range passes verification."""
        log = AuditLog()
        for i in range(10):
            log.append(f"event-{i}", timestamp=float(i))

        self.assertTrue(log.verify_range(3, 7))

    def test_verify_range_detects_tampering(self):
        """Tampering within the range is detected."""
        log = AuditLog()
        for i in range(10):
            log.append(f"event-{i}", timestamp=float(i))

        log.get(5).event_data = "TAMPERED"

        self.assertFalse(log.verify_range(4, 8))

    def test_verify_range_full_log(self):
        """Verifying range [0, len) is equivalent to full verification."""
        log = AuditLog()
        for i in range(10):
            log.append(f"event-{i}", timestamp=float(i))

        self.assertTrue(log.verify_range(0, len(log)))

    # ------------------------------------------------------------------
    # 7. get_proof and verify_proof round-trip
    # ------------------------------------------------------------------
    def test_proof_roundtrip(self):
        """A proof generated from a valid log verifies successfully."""
        log = AuditLog()
        for i in range(10):
            log.append(f"event-{i}", timestamp=float(i))

        proof = log.get_proof(3)
        self.assertIsNotNone(proof)
        self.assertEqual(proof.entry.index, 3)
        # chain_to_head should go from index 3 to index 9 (7 entries)
        self.assertEqual(len(proof.chain_to_head), 7)
        self.assertTrue(log.verify_proof(proof))

    def test_proof_of_head(self):
        """Proof of the head entry has a single-element chain."""
        log = AuditLog()
        for i in range(5):
            log.append(f"event-{i}", timestamp=float(i))

        proof = log.get_proof(4)
        self.assertEqual(len(proof.chain_to_head), 1)
        self.assertTrue(log.verify_proof(proof))

    def test_proof_of_genesis(self):
        """Proof of the first entry includes the entire chain."""
        log = AuditLog()
        for i in range(5):
            log.append(f"event-{i}", timestamp=float(i))

        proof = log.get_proof(0)
        self.assertEqual(len(proof.chain_to_head), 5)
        self.assertTrue(log.verify_proof(proof))

    # ------------------------------------------------------------------
    # 8. verify_proof fails on tampered proof
    # ------------------------------------------------------------------
    def test_verify_proof_tampered(self):
        """Tampering with a proof's chain makes verification fail."""
        log = AuditLog()
        for i in range(10):
            log.append(f"event-{i}", timestamp=float(i))

        proof = log.get_proof(3)
        # Tamper with one entry in the proof chain
        proof.chain_to_head[2].event_data = "TAMPERED"

        self.assertFalse(log.verify_proof(proof))

    def test_verify_proof_tampered_entry(self):
        """Tampering with the proof's entry itself makes verification fail."""
        log = AuditLog()
        for i in range(5):
            log.append(f"event-{i}", timestamp=float(i))

        proof = log.get_proof(0)
        proof.entry.event_data = "TAMPERED"
        # Since entry is chain_to_head[0], this should fail
        self.assertFalse(log.verify_proof(proof))

    # ------------------------------------------------------------------
    # 9. Export / import round-trip
    # ------------------------------------------------------------------
    def test_export_import_roundtrip(self):
        """Exporting and re-importing preserves chain integrity."""
        log = AuditLog()
        for i in range(15):
            log.append(f"event-{i}", timestamp=float(i))

        json_str = log.export_json()
        restored = AuditLog.from_json(json_str)

        self.assertEqual(len(restored), len(log))
        self.assertTrue(restored.verify_integrity())

        # Check all entries match
        for i in range(len(log)):
            orig = log.get(i)
            rest = restored.get(i)
            self.assertEqual(orig.index, rest.index)
            self.assertEqual(orig.timestamp, rest.timestamp)
            self.assertEqual(orig.event_data, rest.event_data)
            self.assertEqual(orig.previous_hash, rest.previous_hash)
            self.assertEqual(orig.entry_hash, rest.entry_hash)

    def test_export_is_valid_json(self):
        """The exported string is valid JSON."""
        log = AuditLog()
        log.append("test", timestamp=1.0)

        json_str = log.export_json()
        parsed = json.loads(json_str)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 1)
        self.assertIn("entry_hash", parsed[0])

    def test_import_tampered_json_fails_verify(self):
        """Importing tampered JSON produces a log that fails verification."""
        log = AuditLog()
        for i in range(5):
            log.append(f"event-{i}", timestamp=float(i))

        json_str = log.export_json()
        entries = json.loads(json_str)
        entries[2]["event_data"] = "TAMPERED"
        tampered_json = json.dumps(entries)

        restored = AuditLog.from_json(tampered_json)
        self.assertFalse(restored.verify_integrity())

    # ------------------------------------------------------------------
    # 10. Empty log edge cases
    # ------------------------------------------------------------------
    def test_empty_log_head_is_none(self):
        """An empty log's head() returns None."""
        log = AuditLog()
        self.assertIsNone(log.head())

    def test_empty_log_len_is_zero(self):
        """An empty log has length zero."""
        log = AuditLog()
        self.assertEqual(len(log), 0)

    def test_empty_log_get_returns_none(self):
        """Getting any index from an empty log returns None."""
        log = AuditLog()
        self.assertIsNone(log.get(0))
        self.assertIsNone(log.get(5))

    def test_empty_log_proof_returns_none(self):
        """Getting a proof from an empty log returns None."""
        log = AuditLog()
        self.assertIsNone(log.get_proof(0))

    # ------------------------------------------------------------------
    # 11. Single entry log
    # ------------------------------------------------------------------
    def test_single_entry_log(self):
        """A log with one entry works correctly end-to-end."""
        log = AuditLog()
        entry = log.append("only-event", timestamp=100.0)

        self.assertEqual(len(log), 1)
        self.assertEqual(log.head(), entry)
        self.assertEqual(log.get(0), entry)
        self.assertTrue(log.verify_integrity())

        proof = log.get_proof(0)
        self.assertEqual(len(proof.chain_to_head), 1)
        self.assertTrue(log.verify_proof(proof))

    # ------------------------------------------------------------------
    # 12. get() and head() return correct entries
    # ------------------------------------------------------------------
    def test_get_returns_correct_entry(self):
        """get(i) returns the entry appended at position i."""
        log = AuditLog()
        entries = []
        for i in range(5):
            entries.append(log.append(f"event-{i}", timestamp=float(i)))

        for i, expected in enumerate(entries):
            self.assertEqual(log.get(i), expected)

    def test_head_returns_latest(self):
        """head() always returns the most recently appended entry."""
        log = AuditLog()
        for i in range(5):
            entry = log.append(f"event-{i}", timestamp=float(i))

        self.assertEqual(log.head(), entry)
        self.assertEqual(log.head().index, 4)

    def test_get_out_of_range(self):
        """get() with an out-of-range index returns None."""
        log = AuditLog()
        log.append("test", timestamp=1.0)

        self.assertIsNone(log.get(-1))
        self.assertIsNone(log.get(1))
        self.assertIsNone(log.get(100))

    # ------------------------------------------------------------------
    # 13. Default timestamp
    # ------------------------------------------------------------------
    def test_append_default_timestamp(self):
        """Appending without a timestamp uses the current time."""
        log = AuditLog()
        import time
        before = time.time()
        entry = log.append("auto-timestamp")
        after = time.time()

        self.assertGreaterEqual(entry.timestamp, before)
        self.assertLessEqual(entry.timestamp, after)


if __name__ == "__main__":
    unittest.main()
