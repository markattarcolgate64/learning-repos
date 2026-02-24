"""Tests for the Bloom Filter exercise."""

import unittest

from exercise import BloomFilter


class TestBloomFilter(unittest.TestCase):
    """Comprehensive tests for BloomFilter."""

    # ------------------------------------------------------------------
    # 1. Empty filter: might_contain returns False for everything
    # ------------------------------------------------------------------
    def test_empty_filter_returns_false(self):
        """An empty Bloom filter should say 'not present' for any query."""
        bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
        self.assertFalse(bf.might_contain("hello"))
        self.assertFalse(bf.might_contain("world"))
        self.assertFalse(bf.might_contain(""))
        self.assertFalse(bf.might_contain("anything"))

    # ------------------------------------------------------------------
    # 2. No false negatives: every added item returns True
    # ------------------------------------------------------------------
    def test_no_false_negatives(self):
        """Every item that was added must be reported as possibly present."""
        bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
        items = ["apple", "banana", "cherry", "date", "elderberry"]
        for item in items:
            bf.add(item)
        for item in items:
            self.assertTrue(
                bf.might_contain(item),
                f"Added item '{item}' must be found (no false negatives)",
            )

    # ------------------------------------------------------------------
    # 3. Multiple items: all added items found
    # ------------------------------------------------------------------
    def test_multiple_items_all_found(self):
        """Adding many items -- all should still be found afterwards."""
        bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
        items = [f"item_{i}" for i in range(500)]
        for item in items:
            bf.add(item)
        for item in items:
            self.assertTrue(
                bf.might_contain(item),
                f"Item '{item}' should be found after being added",
            )

    # ------------------------------------------------------------------
    # 4. Optimal sizing: m and k are reasonable
    # ------------------------------------------------------------------
    def test_optimal_sizing(self):
        """The computed bit-array size and hash count should be positive."""
        bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
        self.assertGreater(bf.size, 0, "Bit-array size m must be > 0")
        self.assertGreater(bf.num_hashes, 0, "Number of hashes k must be > 0")
        # For n=1000, p=0.01: theoretical m ~ 9585, k ~ 7
        self.assertGreater(bf.size, 1000, "m should be larger than n for low FP rate")
        self.assertLessEqual(bf.num_hashes, 20, "k should be a reasonable number")

    # ------------------------------------------------------------------
    # 5. bit_count increases as items are added
    # ------------------------------------------------------------------
    def test_bit_count_increases(self):
        """The number of set bits should increase (or stay same) as items are added."""
        bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
        self.assertEqual(bf.bit_count, 0, "Empty filter should have 0 bits set")

        bf.add("first")
        count_after_first = bf.bit_count
        self.assertGreater(count_after_first, 0, "After adding an item, bits should be set")

        bf.add("second")
        count_after_second = bf.bit_count
        self.assertGreaterEqual(
            count_after_second,
            count_after_first,
            "bit_count should not decrease when adding items",
        )

        bf.add("third")
        count_after_third = bf.bit_count
        self.assertGreaterEqual(count_after_third, count_after_second)

    # ------------------------------------------------------------------
    # 6. False positive rate is near expected (with tolerance)
    # ------------------------------------------------------------------
    def test_false_positive_rate(self):
        """After inserting N items, the observed FP rate on absent items
        should be reasonably close to the configured rate."""
        n = 1000
        p = 0.05  # 5% target FP rate
        bf = BloomFilter(expected_items=n, false_positive_rate=p)

        # Insert n items
        for i in range(n):
            bf.add(f"present_{i}")

        # Test 10000 absent items
        test_count = 10000
        false_positives = 0
        for i in range(test_count):
            if bf.might_contain(f"absent_{i}"):
                false_positives += 1

        observed_rate = false_positives / test_count
        # Allow generous tolerance -- FP rate should be within 3x the target
        self.assertLess(
            observed_rate,
            p * 3,
            f"Observed FP rate {observed_rate:.4f} is too high (target {p})",
        )

    # ------------------------------------------------------------------
    # 7. Different string lengths work
    # ------------------------------------------------------------------
    def test_different_string_lengths(self):
        """Strings of varying lengths should all work correctly."""
        bf = BloomFilter(expected_items=100, false_positive_rate=0.01)

        items = [
            "",               # empty string
            "a",              # single char
            "ab",             # two chars
            "hello world",    # medium
            "x" * 1000,       # long string
        ]
        for item in items:
            bf.add(item)
        for item in items:
            self.assertTrue(
                bf.might_contain(item),
                f"Item of length {len(item)} should be found",
            )


if __name__ == "__main__":
    unittest.main()
