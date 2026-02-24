"""
LRU Cache
=========
Category   : Distributed Systems
Difficulty : ** (2/5)

Problem
-------
Implement a Least Recently Used (LRU) cache with O(1) time complexity for both
*get* and *put* operations.  This is LeetCode problem #146 and one of the most
frequently asked data-structure design questions.

The cache has a fixed capacity.  When the capacity is exceeded, the least
recently used entry is evicted.

Real-world motivation
---------------------
LRU caches appear everywhere in systems design:
  - CPU L1/L2/L3 hardware caches use LRU-like policies.
  - Memcached and Redis implement LRU eviction for in-memory key-value stores.
  - Operating-system page replacement algorithms are modelled on LRU.

The key insight is combining a **doubly linked list** (for O(1) insert / remove)
with a **hash map** (for O(1) lookup).  Two sentinel nodes (head and tail)
eliminate edge-case checks when the list is empty.



Run command
-----------
    pytest 03_lru_cache/test_exercise.py -v
"""


class Node:
    """A node in a doubly linked list used by the LRU cache."""

    def __init__(self, prev: int, next: int, key: int = 0, value: int = 0) -> None:
        """Initialise a doubly linked list node.

        Args:
            key: The cache key stored in this node.
            value: The cache value stored in this node.
        """
        self.key = key 
        self.value = value 
        self.prev = prev 
        self.next = next
        #if its a double linked list this should have a head/tail
        pass


        


class LRUCache:
    """An LRU cache backed by a doubly linked list and a hash map.

    Provides O(1) *get* and *put* operations.  When the cache exceeds its
    capacity the least recently used entry is evicted automatically.
    """

    def __init__(self, capacity: int) -> None:
        """Initialise the LRU cache.

        Args:
            capacity: The maximum number of key-value pairs the cache can hold.
        """
        self.capacity = capacity
        self.key_map = {}
        self.head = None
       

    def get(self, key: int) -> int:
        """Retrieve the value for *key*.

        If the key exists, moves the corresponding node to the front (most
        recently used position) and returns its value.  Otherwise returns -1.

        Args:
            key: The key to look up.

        Returns:
            The value associated with *key*, or -1 if the key is not present.
        """
        pass

    def put(self, key: int, value: int) -> None:
        """Insert or update a key-value pair.

        If the key already exists, updates its value and moves it to the front.
        If the key is new, creates a node and adds it to the front.  If the
        cache now exceeds capacity, evicts the least recently used node (the one
        just before the tail sentinel).

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        pass

    def _remove(self, node: Node) -> None:
        """Unlink a node from the doubly linked list.

        Does *not* remove the node from the hash map.

        Args:
            node: The node to unlink.
        """
        pass

    def _add_to_front(self, node: Node) -> None:
        """Insert a node right after the head sentinel (most recently used).

        Args:
            node: The node to insert.
        """
        pass


# Hints
# -----
# 1. Use sentinel (dummy) head and tail nodes so you never have to handle None
#    checks when linking or unlinking.
# 2. Most recently used items go right after the head sentinel.
# 3. The node just before the tail sentinel is the least recently used.
# 4. On *get*, move the accessed node to the front of the list.
# 5. On *put*, if the key already exists update its value and move it to front;
#    otherwise create a new node, add to front, and evict the LRU node (the one
#    before the tail sentinel) if over capacity.