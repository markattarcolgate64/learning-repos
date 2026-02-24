"""
Bloom Filter
=============
Category   : Distributed Systems
Difficulty : ** (2/5)

Problem
-------
Implement a Bloom filter -- a space-efficient probabilistic data structure that
tests whether an element is a member of a set.  False positives are possible,
but false negatives are not: if the filter says "not present" the element is
definitely absent, but if it says "possibly present" it might be wrong.

Real-world motivation
---------------------
Bloom filters are used everywhere in large-scale systems:
  - Google Bigtable / Apache HBase use them to avoid unnecessary disk reads.
  - CDNs use them to decide whether to cache a URL (cache on second hit).
  - Chrome used a Bloom filter to check URLs against a list of known-malicious
    sites before making a network request.

Hints
-----
1. Optimal bit array size:  m = -(n * ln(p)) / (ln(2) ** 2)
2. Optimal hash count:      k = (m / n) * ln(2)
3. For hashing with a seed, use:  hash(f"{seed}:{item}") % self.size
4. To add an item, set the bit at every hash position to True.
5. To query, check that *all* hash positions are True.

Run command
-----------
    pytest 02_bloom_filter/test_exercise.py -v
"""

import math


class BloomFilter:
    """A probabilistic set-membership data structure.

    Supports *add* and *might_contain* operations.  False positives are
    possible; false negatives are not.
    """

    def __init__(self, expected_items: int, false_positive_rate: float) -> None:
        """Initialise the Bloom filter.

        Computes the optimal bit-array size (*m*) and number of hash functions
        (*k*) from the expected number of items and the desired false-positive
        rate.

        Args:
            expected_items: The anticipated number of distinct items (n).
            false_positive_rate: The desired probability of a false positive (p),
                e.g. 0.01 for a 1 % rate.
        """

        # TODO: Compute optimal size (m) using:
        #       m = -(n * ln(p)) / (ln(2) ** 2)
        #bit array size (m)
        optimal_size = -(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2)

        # TODO: Compute optimal number of hash functions (k) using:
        #       k = (m / n) * ln(2)
        # optimal number of hash fns (k)
        optimal_hash_fns = (optimal_size / expected_items) * math.log(2)

        # TODO: Initialise a bit array of size m (all False).
        # Hint: self.size = int(...)  -- round m up with int() or math.ceil()
        #       self.num_hashes = int(...)
        #       self.bit_array = [False] * self.size
        self.size = math.ceil(optimal_size)
        self.num_hashes = int(optimal_hash_fns)
        self.bit_array = [False] * self.size
        
        

    def _hash(self, item: str, seed: int) -> int:
        """Compute a hash of *item* using the given *seed*.

        Args:
            item: The element to hash (converted to string).
            seed: An integer seed that selects which hash function to use.

        Returns:
            An index into the bit array (0 <= index < self.size).
        """
        # TODO: Combine seed and item, then hash and mod by self.size.
        return hash(f"{seed}{item}") % self.size

    def add(self, item: str) -> None:
        """Add an item to the Bloom filter.

        Sets the bits at all *k* hash positions to True.

        Args:
            item: The element to insert.
        """
        # TODO: For each hash function (seed 0 .. k-1), compute the index
        #       and set bit_array[index] = True.
        #we use the seeds as hash functions 
        for seed in range(self.num_hashes):
            self.bit_array[self._hash(item, seed)] = True        


    def might_contain(self, item: str) -> bool:
        """Test whether *item* is possibly in the set.

        Args:
            item: The element to look up.

        Returns:
            False if the item is *definitely not* in the set.
            True  if the item is *possibly* in the set (may be a false positive).
        """
        # TODO: For each hash function, compute the index.  If any bit is
        #       False, return False immediately.  Otherwise return True.
        for seed in range(self.num_hashes):
            val = self.bit_array[self._hash(item, seed)]
            if not val:
                return False 

        return True 

    @property
    def bit_count(self) -> int:
        """Return the number of bits currently set to 1.

        Returns:
            The count of True values in the bit array.
        """
        # TODO: Count and return the number of True values in self.bit_array.        
        return sum(self.bit_array)
