"""
Merkle Tree - Solution

A hash tree used for efficient data verification and synchronization.
Each leaf node is a hash of a data block, and each internal node is
a hash of its children's hashes.
"""

import hashlib
from typing import List, Optional, Tuple


class MerkleNode:
    """A node in the Merkle tree."""

    def __init__(
        self,
        hash_value: str,
        left: Optional["MerkleNode"] = None,
        right: Optional["MerkleNode"] = None,
        data: Optional[str] = None,
    ):
        self.hash_value = hash_value
        self.left = left
        self.right = right
        self.data = data


class MerkleTree:
    def __init__(self, data_blocks: List[str]):
        """
        Build a Merkle tree from a list of data blocks.

        Args:
            data_blocks: List of string data blocks.
        """
        self.data_blocks = data_blocks

        # Create leaf nodes
        self.leaves = [
            MerkleNode(hash_value=self._hash(block), data=block)
            for block in data_blocks
        ]

        # Build the tree from leaves up
        if self.leaves:
            self.root = self._build_tree(list(self.leaves))
        else:
            self.root = MerkleNode(hash_value=self._hash(""))

    @staticmethod
    def _hash(data: str) -> str:
        """
        Compute the SHA-256 hash of a string.

        Args:
            data: The string to hash.

        Returns:
            The hex digest of the SHA-256 hash.
        """
        return hashlib.sha256(data.encode()).hexdigest()

    def _build_tree(self, nodes: List[MerkleNode]) -> MerkleNode:
        """
        Recursively build the Merkle tree from a list of nodes.

        Args:
            nodes: The current level of nodes to combine.

        Returns:
            The root node of the (sub)tree.
        """
        if len(nodes) == 1:
            return nodes[0]

        # If odd number of nodes, duplicate the last one
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])

        parent_nodes = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1]
            combined_hash = self._hash(left.hash_value + right.hash_value)
            parent = MerkleNode(
                hash_value=combined_hash,
                left=left,
                right=right,
            )
            parent_nodes.append(parent)

        return self._build_tree(parent_nodes)

    def get_root_hash(self) -> str:
        """
        Return the root hash of the Merkle tree.

        Returns:
            The hash value of the root node.
        """
        return self.root.hash_value

    def get_proof(self, index: int) -> List[Tuple[str, str]]:
        """
        Generate a Merkle proof (audit path) for the data block at the given index.

        Args:
            index: Index of the data block in the original list.

        Returns:
            A list of (hash, direction) tuples where direction is 'left' or 'right',
            indicating which side the sibling hash is on.
        """
        proof = []
        nodes = list(self.leaves)

        target_index = index

        while len(nodes) > 1:
            # If odd number of nodes, duplicate the last one
            if len(nodes) % 2 == 1:
                nodes.append(nodes[-1])

            next_level = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1]

                if i == target_index or i + 1 == target_index:
                    if target_index % 2 == 0:
                        # Target is the left child, sibling is on the right
                        proof.append((right.hash_value, "right"))
                    else:
                        # Target is the right child, sibling is on the left
                        proof.append((left.hash_value, "left"))

                combined_hash = self._hash(left.hash_value + right.hash_value)
                parent = MerkleNode(hash_value=combined_hash, left=left, right=right)
                next_level.append(parent)

            target_index = target_index // 2
            nodes = next_level

        return proof

    @staticmethod
    def verify_proof(data: str, proof: List[Tuple[str, str]], root_hash: str) -> bool:
        """
        Verify a Merkle proof for a data block against a known root hash.

        Args:
            data: The data block to verify.
            proof: The Merkle proof as a list of (hash, direction) tuples.
            root_hash: The expected root hash.

        Returns:
            True if the proof is valid, False otherwise.
        """
        current_hash = MerkleTree._hash(data)

        for sibling_hash, direction in proof:
            if direction == "left":
                current_hash = MerkleTree._hash(sibling_hash + current_hash)
            else:
                current_hash = MerkleTree._hash(current_hash + sibling_hash)

        return current_hash == root_hash

    @staticmethod
    def find_differences(
        tree_a: "MerkleTree", tree_b: "MerkleTree"
    ) -> List[int]:
        """
        Find indices of data blocks that differ between two Merkle trees.
        Efficiently skips subtrees whose root hashes match.

        Args:
            tree_a: The first Merkle tree.
            tree_b: The second Merkle tree.

        Returns:
            A sorted list of indices where the data blocks differ.
        """
        differences = []

        def _compare(node_a: Optional[MerkleNode], node_b: Optional[MerkleNode],
                     start: int, end: int) -> None:
            """Recursively compare subtrees."""
            # If both are None, no difference
            if node_a is None and node_b is None:
                return

            # If one is None but not the other, all indices differ
            if node_a is None or node_b is None:
                differences.extend(range(start, end))
                return

            # If hashes match, entire subtree is identical -- skip
            if node_a.hash_value == node_b.hash_value:
                return

            # If these are leaf nodes with different hashes, record the difference
            if node_a.data is not None or node_b.data is not None:
                differences.extend(range(start, end))
                return

            # Internal nodes with different hashes: recurse into children
            mid = (start + end) // 2
            _compare(node_a.left, node_b.left, start, mid)
            _compare(node_a.right, node_b.right, mid, end)

        max_len = max(len(tree_a.data_blocks), len(tree_b.data_blocks))
        if max_len == 0:
            return []

        # Calculate the effective size (next power of 2 for balanced tree)
        effective_size = 1
        while effective_size < max_len:
            effective_size *= 2

        _compare(tree_a.root, tree_b.root, 0, effective_size)

        # Filter to only valid indices
        differences = [i for i in differences if i < max_len]
        return sorted(differences)
