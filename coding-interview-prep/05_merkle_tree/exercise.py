"""
Merkle Tree
===========
Category   : Distributed Systems
Difficulty : *** (3/5)

Problem
-------
Implement a Merkle tree for data integrity verification.  A Merkle tree is a
binary hash tree where every leaf node holds the hash of a data block and every
internal node holds the hash of its two children concatenated together.

Merkle trees allow efficient and secure verification of large data structures.
They are used in Git (for content-addressed storage), Bitcoin (for transaction
verification), and Cassandra (for anti-entropy repair).

Real-world motivation
---------------------
When two nodes in a distributed system need to check whether they hold the same
data, comparing every record is prohibitively expensive.  A Merkle tree lets
them compare just the root hash first, then drill down only into the subtrees
that differ.  This reduces the amount of data transferred from O(n) to
O(log n) in the common case where most data is identical.

Hints
-----
1. Use SHA-256 for hashing (hashlib.sha256).
2. If the number of leaves is odd, duplicate the last leaf so every internal
   node has exactly two children.
3. Build the tree bottom-up: hash pairs of nodes until one root remains.
4. A Merkle proof is a list of (sibling_hash, direction) tuples that lets a
   verifier recompute the root hash from a single leaf.
5. To find differing blocks between two trees, recursively compare subtrees
   starting from the root -- only descend into children whose hashes differ.

Run command
-----------
    pytest 05_merkle_tree/test_exercise.py -v
"""

import hashlib


class MerkleNode:
    """A single node in a Merkle tree."""

    def __init__(self, hash_value: str, left=None, right=None, data=None):
        """Initialise a Merkle tree node.

        Args:
            hash_value: The SHA-256 hex digest stored at this node.
            left: Optional left child MerkleNode.
            right: Optional right child MerkleNode.
            data: Optional original data string (only set for leaf nodes).
        """
        # TODO: Store hash_value, left, right, and data as instance attributes.
        pass


class MerkleTree:
    """A Merkle (hash) tree built from a list of data blocks.

    The tree is constructed bottom-up.  Each leaf holds the hash of a data
    block, and each internal node holds the hash of its two children's hashes
    concatenated together.
    """

    def __init__(self, data_blocks: list):
        """Build a Merkle tree from a list of data strings.

        Args:
            data_blocks: A list of strings, each representing one data block.
        """
        # TODO: Store data_blocks, create leaf nodes, and build the tree.
        # Hint: Create a leaf for each block using _hash(block), then call
        #       _build_tree with the list of leaves.
        pass

    @staticmethod
    def _hash(data: str) -> str:
        """Compute the SHA-256 hex digest of a string.

        Args:
            data: The input string to hash.

        Returns:
            The hex-encoded SHA-256 digest.
        """
        # TODO: Return hashlib.sha256(data.encode()).hexdigest()
        pass

    def _build_tree(self, leaves: list):
        """Recursively build the Merkle tree from a list of leaf nodes.

        If the list has an odd number of nodes, duplicate the last node so
        that every internal node has exactly two children.

        Args:
            leaves: A list of MerkleNode objects (the current level).

        Returns:
            The root MerkleNode of the constructed tree.
        """
        # TODO: Base case -- if only one node remains, it is the root.
        # TODO: If odd count, duplicate the last leaf.
        # TODO: Pair adjacent nodes, hash their concatenated hashes, create
        #       parent nodes, and recurse on the parent level.
        # Hint: parent_hash = _hash(left.hash_value + right.hash_value)
        pass

    def get_root_hash(self) -> str:
        """Return the root hash of the Merkle tree.

        Returns:
            The hex-encoded SHA-256 root hash, or an empty string if the
            tree is empty.
        """
        # TODO: Return self.root.hash_value (handle empty tree).
        pass

    def get_proof(self, index: int) -> list:
        """Generate a Merkle proof for the data block at *index*.

        A Merkle proof is a list of (sibling_hash, direction) tuples where
        direction is 'left' or 'right', indicating on which side the sibling
        sits relative to the path from the target leaf to the root.

        Args:
            index: The zero-based index of the data block.

        Returns:
            A list of (hash: str, direction: str) tuples forming the proof.
        """
        # TODO: Walk from the target leaf to the root, collecting sibling
        #       hashes and their directions at each level.
        # Hint: At each level, determine if the index is even or odd to know
        #       whether the sibling is to the left or right.  Then move up:
        #       index = index // 2.
        pass

    @staticmethod
    def verify_proof(data: str, proof: list, root_hash: str) -> bool:
        """Verify a Merkle proof against an expected root hash.

        Args:
            data: The original data string for the leaf being verified.
            proof: A list of (hash, direction) tuples as returned by
                   get_proof.
            root_hash: The expected root hash to verify against.

        Returns:
            True if the proof is valid and matches the root hash, False
            otherwise.
        """
        # TODO: Start with current_hash = _hash(data).
        # TODO: For each (sibling_hash, direction) in proof, combine
        #       current_hash with sibling_hash in the correct order and
        #       re-hash.
        # TODO: Return current_hash == root_hash.
        # Hint: If direction == 'left', the sibling is on the left:
        #       current_hash = _hash(sibling_hash + current_hash)
        pass

    @staticmethod
    def find_differences(tree_a, tree_b) -> list:
        """Find the indices of data blocks that differ between two trees.

        Uses the tree structure to prune comparison: only descends into
        subtrees whose root hashes differ.

        Args:
            tree_a: A MerkleTree instance.
            tree_b: A MerkleTree instance of the same size.

        Returns:
            A sorted list of zero-based indices where the data blocks differ.
        """
        # TODO: Recursively compare nodes from tree_a and tree_b.
        # TODO: If hashes match, skip that subtree entirely.
        # TODO: If both nodes are leaves with different hashes, record the
        #       index.
        # Hint: Write a helper that tracks the current index range as it
        #       recurses into left (first half) and right (second half).
        pass
