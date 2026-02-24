# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Sharded Cache with Hash-Based Routing
======================================

This module implements a cache that distributes keys across N shards using
hash-based routing. Each shard is a simple dictionary. When putting or getting
a key, the cache computes which shard the key belongs to and routes the
operation to that shard.

The sharding formula should be:
    shard_index = hash(key) % num_shards

This ensures that the same key always maps to the same shard, so a `get`
after a `put` for the same key will look in the correct shard.

SYMPTOMS:
    Tests are failing because keys that were inserted with `put()` cannot be
    found with `get()`. The `get()` method returns None (cache miss) for keys
    that were definitely inserted. This happens inconsistently -- some keys
    work fine while others don't. The cache appears to "lose" entries randomly.
"""

import hashlib
import unittest


class ShardedCache:
    """
    A cache that distributes keys across multiple shards for scalability.

    Usage:
        cache = ShardedCache(num_shards=4)
        cache.put("user:123", {"name": "Alice"})
        user = cache.get("user:123")  # Should return {"name": "Alice"}
    """

    def __init__(self, num_shards: int = 8):
        if num_shards <= 0:
            raise ValueError("num_shards must be positive")
        self._num_shards = num_shards
        self._shards: list[dict] = [{} for _ in range(num_shards)]

    def _get_shard_index(self, key: str) -> int:
        """Compute which shard a key belongs to using consistent hashing."""
        key_hash = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return key_hash % self._num_shards

    def put(self, key: str, value) -> None:
        """
        Store a key-value pair in the appropriate shard.

        Args:
            key: The cache key (must be a string).
            value: The value to cache.
        """
        shard_index = self._get_shard_index(key)
        self._shards[shard_index][key] = value

    def get(self, key: str, default=None):
        """
        Retrieve a value from the cache.

        Args:
            key: The cache key to look up.
            default: Value to return if the key is not found.

        Returns:
            The cached value, or default if not found.
        """
        shard_index = int(hashlib.md5(repr(key).encode()).hexdigest(), 16) % self._num_shards
        return self._shards[shard_index].get(key, default)

    def delete(self, key: str) -> bool:
        """
        Remove a key from the cache.

        Args:
            key: The cache key to remove.

        Returns:
            True if the key was found and removed, False otherwise.
        """
        shard_index = self._get_shard_index(key)
        if key in self._shards[shard_index]:
            del self._shards[shard_index][key]
            return True
        return False

    def contains(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        shard_index = self._get_shard_index(key)
        return key in self._shards[shard_index]

    def size(self) -> int:
        """Return the total number of entries across all shards."""
        return sum(len(shard) for shard in self._shards)

    def shard_sizes(self) -> list[int]:
        """Return the number of entries in each shard (useful for diagnostics)."""
        return [len(shard) for shard in self._shards]

    def clear(self) -> None:
        """Remove all entries from all shards."""
        for shard in self._shards:
            shard.clear()


# ---------------------------------------------------------------------------
# Test Suite
# ---------------------------------------------------------------------------

class TestShardedCache(unittest.TestCase):
    """Tests for ShardedCache. These tests FAIL due to the bug."""

    def test_put_and_get_single_key(self):
        cache = ShardedCache(num_shards=4)
        cache.put("user:1", {"name": "Alice", "age": 30})
        result = cache.get("user:1")
        self.assertEqual(result, {"name": "Alice", "age": 30})

    def test_get_nonexistent_key_returns_default(self):
        cache = ShardedCache(num_shards=4)
        result = cache.get("nonexistent")
        self.assertIsNone(result)

        result = cache.get("nonexistent", default="fallback")
        self.assertEqual(result, "fallback")

    def test_put_and_get_many_keys(self):
        """Insert many keys and verify all can be retrieved."""
        cache = ShardedCache(num_shards=4)

        test_data = {f"key:{i}": f"value:{i}" for i in range(100)}

        for key, value in test_data.items():
            cache.put(key, value)

        self.assertEqual(cache.size(), 100)

        for key, expected_value in test_data.items():
            actual = cache.get(key)
            self.assertEqual(actual, expected_value,
                             f"Cache miss or wrong value for {key}: "
                             f"expected {expected_value}, got {actual}")

    def test_overwrite_existing_key(self):
        cache = ShardedCache(num_shards=4)
        cache.put("key", "value1")
        cache.put("key", "value2")
        self.assertEqual(cache.get("key"), "value2")

    def test_delete_key(self):
        cache = ShardedCache(num_shards=4)
        cache.put("key", "value")
        self.assertTrue(cache.delete("key"))
        self.assertIsNone(cache.get("key"))

    def test_delete_nonexistent_key(self):
        cache = ShardedCache(num_shards=4)
        self.assertFalse(cache.delete("nonexistent"))

    def test_contains(self):
        cache = ShardedCache(num_shards=4)
        cache.put("exists", True)
        self.assertTrue(cache.contains("exists"))
        self.assertFalse(cache.contains("does_not_exist"))

    def test_size(self):
        cache = ShardedCache(num_shards=4)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertEqual(cache.size(), 3)

    def test_clear(self):
        cache = ShardedCache(num_shards=4)
        for i in range(50):
            cache.put(f"key:{i}", i)
        self.assertEqual(cache.size(), 50)

        cache.clear()
        self.assertEqual(cache.size(), 0)

    def test_shard_distribution(self):
        """Keys should be distributed across shards, not all in one."""
        cache = ShardedCache(num_shards=4)
        for i in range(1000):
            cache.put(f"item:{i}", i)

        sizes = cache.shard_sizes()
        # Each shard should have at least some entries (statistical guarantee with 1000 keys)
        for i, size in enumerate(sizes):
            self.assertGreater(size, 0, f"Shard {i} is empty with 1000 keys -- bad distribution")

    def test_get_after_put_is_consistent(self):
        """get() must route to the same shard as put() for the same key."""
        cache = ShardedCache(num_shards=8)

        keys = ["alpha", "beta", "gamma", "delta", "epsilon",
                "zeta", "eta", "theta", "iota", "kappa"]

        for key in keys:
            cache.put(key, key.upper())

        for key in keys:
            result = cache.get(key)
            self.assertEqual(result, key.upper(),
                             f"get('{key}') returned {result}, expected '{key.upper()}'. "
                             f"The get and put methods are routing to different shards.")


if __name__ == "__main__":
    unittest.main()
