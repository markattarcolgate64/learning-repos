"""Tests for Iris Code Matching Engine."""

import os
import time
import unittest

from exercise import IrisCodeMatcher, MatchResult, CODE_BYTES, CODE_BITS


def _make_code(pattern: int = 0x00) -> bytes:
    """Create a code filled with a single byte pattern."""
    return bytes([pattern]) * CODE_BYTES


def _flip_bits(code: bytes, n_bits: int) -> bytes:
    """Flip exactly *n_bits* bits in *code* (from the front)."""
    ba = bytearray(code)
    flipped = 0
    for i in range(len(ba)):
        for bit in range(8):
            if flipped >= n_bits:
                return bytes(ba)
            ba[i] ^= 1 << bit
            flipped += 1
    return bytes(ba)


class TestHammingDistance(unittest.TestCase):
    """Test the static hamming_distance method."""

    def test_identical_codes(self):
        code = IrisCodeMatcher.random_code()
        self.assertAlmostEqual(IrisCodeMatcher.hamming_distance(code, code), 0.0)

    def test_opposite_codes(self):
        a = bytes([0x00]) * CODE_BYTES
        b = bytes([0xFF]) * CODE_BYTES
        self.assertAlmostEqual(IrisCodeMatcher.hamming_distance(a, b), 1.0)

    def test_known_distance(self):
        a = _make_code(0x00)
        # Flip exactly 512 bits → distance = 512/2048 = 0.25
        b = _flip_bits(a, 512)
        dist = IrisCodeMatcher.hamming_distance(a, b)
        self.assertAlmostEqual(dist, 0.25, places=5)

    def test_single_bit_flip(self):
        a = _make_code(0x00)
        b = _flip_bits(a, 1)
        self.assertAlmostEqual(
            IrisCodeMatcher.hamming_distance(a, b),
            1.0 / CODE_BITS,
            places=8,
        )

    def test_symmetry(self):
        a = IrisCodeMatcher.random_code()
        b = IrisCodeMatcher.random_code()
        self.assertAlmostEqual(
            IrisCodeMatcher.hamming_distance(a, b),
            IrisCodeMatcher.hamming_distance(b, a),
        )


class TestAddAndContains(unittest.TestCase):
    """Test adding codes and checking membership."""

    def setUp(self):
        self.matcher = IrisCodeMatcher()

    def test_empty_database(self):
        self.assertEqual(len(self.matcher), 0)

    def test_add_single(self):
        code = IrisCodeMatcher.random_code()
        self.matcher.add("iris_001", code)
        self.assertEqual(len(self.matcher), 1)
        self.assertIn("iris_001", self.matcher)

    def test_add_multiple(self):
        for i in range(10):
            self.matcher.add(f"iris_{i:03d}", IrisCodeMatcher.random_code())
        self.assertEqual(len(self.matcher), 10)

    def test_duplicate_id_raises(self):
        code = IrisCodeMatcher.random_code()
        self.matcher.add("iris_001", code)
        with self.assertRaises(ValueError):
            self.matcher.add("iris_001", IrisCodeMatcher.random_code())

    def test_wrong_code_length_raises(self):
        with self.assertRaises(ValueError):
            self.matcher.add("iris_001", b"\x00" * 10)

    def test_remove(self):
        code = IrisCodeMatcher.random_code()
        self.matcher.add("iris_001", code)
        self.assertTrue(self.matcher.remove("iris_001"))
        self.assertEqual(len(self.matcher), 0)
        self.assertNotIn("iris_001", self.matcher)

    def test_remove_nonexistent(self):
        self.assertFalse(self.matcher.remove("no_such_id"))


class TestQuery(unittest.TestCase):
    """Test querying for matches."""

    def setUp(self):
        self.matcher = IrisCodeMatcher()

    def test_exact_match(self):
        code = IrisCodeMatcher.random_code()
        self.matcher.add("iris_001", code)
        results = self.matcher.query(code, threshold=0.32)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].iris_id, "iris_001")
        self.assertAlmostEqual(results[0].distance, 0.0)

    def test_close_match(self):
        base = _make_code(0x00)
        # 20% distance — should match at 0.32 threshold
        close = _flip_bits(base, int(CODE_BITS * 0.20))
        self.matcher.add("iris_001", base)
        results = self.matcher.query(close, threshold=0.32)
        self.assertEqual(len(results), 1)
        self.assertLessEqual(results[0].distance, 0.32)

    def test_no_match(self):
        base = _make_code(0x00)
        # 50% distance — should NOT match at 0.32 threshold
        far = _flip_bits(base, int(CODE_BITS * 0.50))
        self.matcher.add("iris_001", base)
        results = self.matcher.query(far, threshold=0.32)
        self.assertEqual(len(results), 0)

    def test_multiple_matches_sorted(self):
        base = _make_code(0x00)
        # Add codes at distances 0.10, 0.20, 0.30
        for i, frac in enumerate([0.10, 0.20, 0.30]):
            code = _flip_bits(base, int(CODE_BITS * frac))
            self.matcher.add(f"iris_{i}", code)

        results = self.matcher.query(base, threshold=0.32)
        self.assertEqual(len(results), 3)
        # Should be sorted by distance ascending
        for i in range(len(results) - 1):
            self.assertLessEqual(results[i].distance, results[i + 1].distance)

    def test_threshold_boundary(self):
        base = _make_code(0x00)
        # Exactly at threshold (0.32 * 2048 = 655.36 → 655 bits)
        at_boundary = _flip_bits(base, 655)
        self.matcher.add("iris_001", base)
        results = self.matcher.query(at_boundary, threshold=0.32)
        # Should match (655/2048 ≈ 0.3198 < 0.32)
        self.assertEqual(len(results), 1)

    def test_empty_database_query(self):
        code = IrisCodeMatcher.random_code()
        results = self.matcher.query(code)
        self.assertEqual(len(results), 0)

    def test_results_are_match_result_type(self):
        code = IrisCodeMatcher.random_code()
        self.matcher.add("iris_001", code)
        results = self.matcher.query(code)
        self.assertIsInstance(results[0], MatchResult)


class TestBatchQuery(unittest.TestCase):
    """Test batch query functionality."""

    def setUp(self):
        self.matcher = IrisCodeMatcher()
        self.codes = []
        for i in range(20):
            code = IrisCodeMatcher.random_code()
            self.matcher.add(f"iris_{i:03d}", code)
            self.codes.append(code)

    def test_batch_returns_correct_count(self):
        queries = [self.codes[0], self.codes[5], self.codes[10]]
        results = self.matcher.batch_query(queries, threshold=0.32)
        self.assertEqual(len(results), 3)

    def test_batch_finds_exact_matches(self):
        queries = [self.codes[0], self.codes[1]]
        results = self.matcher.batch_query(queries, threshold=0.32)
        # Each query should find at least its own exact match
        for result_list in results:
            self.assertGreaterEqual(len(result_list), 1)
            self.assertAlmostEqual(result_list[0].distance, 0.0)

    def test_batch_empty_queries(self):
        results = self.matcher.batch_query([], threshold=0.32)
        self.assertEqual(len(results), 0)


class TestPerformance(unittest.TestCase):
    """Performance tests — ensure the matcher is fast enough."""

    def test_query_100k_codes(self):
        """Single query against 100K codes should complete in under 500ms."""
        matcher = IrisCodeMatcher()
        n = 100_000
        for i in range(n):
            matcher.add(f"iris_{i}", IrisCodeMatcher.random_code())

        query_code = IrisCodeMatcher.random_code()

        start = time.perf_counter()
        matcher.query(query_code, threshold=0.32)
        elapsed = time.perf_counter() - start

        self.assertLess(
            elapsed,
            0.5,
            f"Query against {n} codes took {elapsed:.3f}s (limit: 0.5s)",
        )

    def test_add_performance(self):
        """Adding 10K codes should take under 2 seconds."""
        matcher = IrisCodeMatcher()
        start = time.perf_counter()
        for i in range(10_000):
            matcher.add(f"iris_{i}", IrisCodeMatcher.random_code())
        elapsed = time.perf_counter() - start

        self.assertLess(
            elapsed,
            2.0,
            f"Adding 10K codes took {elapsed:.3f}s (limit: 2.0s)",
        )


if __name__ == "__main__":
    unittest.main()
