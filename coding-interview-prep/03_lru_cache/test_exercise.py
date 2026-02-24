"""Tests for the LRU Cache exercise."""

import unittest

from .exercise import LRUCache


class TestLRUCache(unittest.TestCase):
    """Comprehensive tests for LRUCache."""

    # ------------------------------------------------------------------
    # 1. Basic get/put
    # ------------------------------------------------------------------
    def test_basic_get_put(self):
        """Simple put followed by get should return the stored value."""
        cache = LRUCache(capacity=2)
        cache.put(1, 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), 20)

    # ------------------------------------------------------------------
    # 2. Key not found returns -1
    # ------------------------------------------------------------------
    def test_key_not_found_returns_negative_one(self):
        """Getting a key that was never inserted should return -1."""
        cache = LRUCache(capacity=2)
        self.assertEqual(cache.get(99), -1)
        cache.put(1, 10)
        self.assertEqual(cache.get(2), -1)

    # ------------------------------------------------------------------
    # 3. Eviction: put beyond capacity evicts LRU
    # ------------------------------------------------------------------
    def test_eviction_beyond_capacity(self):
        """When capacity is exceeded the least recently used item is evicted."""
        cache = LRUCache(capacity=2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)  # Evicts key 1 (LRU)
        self.assertEqual(cache.get(1), -1, "Key 1 should have been evicted")
        self.assertEqual(cache.get(2), 2)
        self.assertEqual(cache.get(3), 3)

    # ------------------------------------------------------------------
    # 4. get() moves item to most recent (affects eviction order)
    # ------------------------------------------------------------------
    def test_get_moves_to_most_recent(self):
        """Accessing a key via get() should make it most recently used."""
        cache = LRUCache(capacity=2)
        cache.put(1, 1)
        cache.put(2, 2)
        # Access key 1 -- now key 2 is the LRU
        cache.get(1)
        cache.put(3, 3)  # Evicts key 2 (now LRU)
        self.assertEqual(cache.get(2), -1, "Key 2 should have been evicted")
        self.assertEqual(cache.get(1), 1, "Key 1 was accessed, should still be present")
        self.assertEqual(cache.get(3), 3)

    # ------------------------------------------------------------------
    # 5. put() with existing key updates value and moves to front
    # ------------------------------------------------------------------
    def test_put_existing_key_updates_and_moves_to_front(self):
        """Putting an existing key should update its value and make it MRU."""
        cache = LRUCache(capacity=2)
        cache.put(1, 1)
        cache.put(2, 2)
        # Update key 1's value -- now key 2 is LRU
        cache.put(1, 100)
        self.assertEqual(cache.get(1), 100, "Value should be updated to 100")
        # Inserting key 3 should evict key 2
        cache.put(3, 3)
        self.assertEqual(cache.get(2), -1, "Key 2 should have been evicted")
        self.assertEqual(cache.get(1), 100)
        self.assertEqual(cache.get(3), 3)

    # ------------------------------------------------------------------
    # 6. Capacity of 1: every new put evicts previous
    # ------------------------------------------------------------------
    def test_capacity_one(self):
        """With capacity 1, each new key evicts the previous one."""
        cache = LRUCache(capacity=1)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), 10)

        cache.put(2, 20)
        self.assertEqual(cache.get(1), -1, "Key 1 should be evicted")
        self.assertEqual(cache.get(2), 20)

        cache.put(3, 30)
        self.assertEqual(cache.get(2), -1, "Key 2 should be evicted")
        self.assertEqual(cache.get(3), 30)

    # ------------------------------------------------------------------
    # 7. Sequential pattern: correct eviction order with multiple ops
    # ------------------------------------------------------------------
    def test_sequential_eviction_order(self):
        """Verify eviction order through a sequence of mixed operations."""
        cache = LRUCache(capacity=3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        # Order (LRU -> MRU): 1, 2, 3

        cache.get(1)
        # Order: 2, 3, 1

        cache.put(4, 4)  # Evicts key 2
        # Order: 3, 1, 4
        self.assertEqual(cache.get(2), -1, "Key 2 should have been evicted")

        cache.put(5, 5)  # Evicts key 3
        # Order: 1, 4, 5
        self.assertEqual(cache.get(3), -1, "Key 3 should have been evicted")

        self.assertEqual(cache.get(1), 1)
        self.assertEqual(cache.get(4), 4)
        self.assertEqual(cache.get(5), 5)

    # ------------------------------------------------------------------
    # 8. Large sequence of operations
    # ------------------------------------------------------------------
    def test_large_sequence(self):
        """Stress test with many put/get operations."""
        capacity = 100
        cache = LRUCache(capacity=capacity)

        # Insert 200 items -- the first 100 should be evicted
        for i in range(200):
            cache.put(i, i * 10)

        # Keys 0..99 should be evicted
        for i in range(100):
            self.assertEqual(
                cache.get(i), -1,
                f"Key {i} should have been evicted",
            )

        # Keys 100..199 should still be present
        for i in range(100, 200):
            self.assertEqual(
                cache.get(i), i * 10,
                f"Key {i} should still be present with value {i * 10}",
            )


if __name__ == "__main__":
    unittest.main()
