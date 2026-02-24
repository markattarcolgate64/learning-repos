"""
LRU Cache - Solution

A Least Recently Used cache with O(1) get and put operations,
implemented using a doubly linked list and a hash map.
"""


class Node:
    """Doubly linked list node for the LRU cache."""

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        """
        Initialize the LRU cache.

        Args:
            capacity: Maximum number of items the cache can hold.
        """
        self.capacity = capacity
        self.cache = {}

        # Sentinel head and tail nodes to simplify edge cases.
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        """
        Retrieve a value from the cache.

        Args:
            key: The key to look up.

        Returns:
            The value if found, -1 otherwise.
        """
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """
        Insert or update a key-value pair in the cache.
        Evicts the least recently used item if the cache is at capacity.

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_front(node)

            if len(self.cache) > self.capacity:
                # Evict the least recently used node (just before tail).
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]

    def _remove(self, node: Node) -> None:
        """
        Remove a node from the doubly linked list.

        Args:
            node: The node to remove.
        """
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: Node) -> None:
        """
        Add a node right after the head sentinel (most recently used position).

        Args:
            node: The node to add.
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
