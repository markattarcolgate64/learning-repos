"""
Bloom Filter - Solution

A space-efficient probabilistic data structure for set membership testing.
May return false positives but never false negatives.
"""

import math


class BloomFilter:
    def __init__(self, expected_items: int, false_positive_rate: float):
        """
        Initialize the Bloom filter.

        Args:
            expected_items: Expected number of items to be inserted (n).
            false_positive_rate: Desired false positive probability (p).
        """
        n = expected_items
        p = false_positive_rate

        # Optimal bit array size: m = -(n * ln(p)) / (ln(2)^2)
        self.size = math.ceil(-(n * math.log(p)) / (math.log(2) ** 2))

        # Optimal number of hash functions: k = (m / n) * ln(2)
        self.num_hashes = round((self.size / n) * math.log(2))
        self.num_hashes = max(1, self.num_hashes)

        self.bit_array = [False] * self.size

    def _hash(self, item: str, seed: int) -> int:
        """
        Compute a hash for the given item using a seed.

        Args:
            item: The item to hash.
            seed: The seed value for this hash function.

        Returns:
            An index into the bit array.
        """
        return hash(f"{seed}:{item}") % self.size

    def add(self, item: str) -> None:
        """
        Add an item to the Bloom filter.

        Args:
            item: The item to add.
        """
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            self.bit_array[index] = True

    def might_contain(self, item: str) -> bool:
        """
        Check if an item might be in the Bloom filter.

        Args:
            item: The item to check.

        Returns:
            True if the item might be in the set (possible false positive),
            False if the item is definitely not in the set.
        """
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False
        return True

    @property
    def bit_count(self) -> int:
        """
        Return the number of bits set to True.

        Returns:
            Count of set bits in the bit array.
        """
        return sum(self.bit_array)
