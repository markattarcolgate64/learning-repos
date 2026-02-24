"""Tests for the Merkle Tree exercise."""

import hashlib
import unittest

from .exercise import MerkleTree, MerkleNode


class TestMerkleTree(unittest.TestCase):
    """Comprehensive tests for MerkleTree and MerkleNode."""

    @staticmethod
    def _sha256(data: str) -> str:
        """Helper to compute SHA-256 hex digest."""
        return hashlib.sha256(data.encode()).hexdigest()

    # ------------------------------------------------------------------
    # 1. Same data produces same root hash
    # ------------------------------------------------------------------
    def test_same_data_same_root_hash(self):
        """Two trees built from the same data should have identical root hashes."""
        data = ["block_0", "block_1", "block_2", "block_3"]
        tree1 = MerkleTree(data)
        tree2 = MerkleTree(data)
        self.assertEqual(tree1.get_root_hash(), tree2.get_root_hash())

    # ------------------------------------------------------------------
    # 2. Different data produces different root hash
    # ------------------------------------------------------------------
    def test_different_data_different_root_hash(self):
        """Two trees built from different data should have different root hashes."""
        tree1 = MerkleTree(["a", "b", "c", "d"])
        tree2 = MerkleTree(["a", "b", "c", "e"])
        self.assertNotEqual(tree1.get_root_hash(), tree2.get_root_hash())

    # ------------------------------------------------------------------
    # 3. Changing one block changes root hash
    # ------------------------------------------------------------------
    def test_changing_one_block_changes_root(self):
        """Modifying even one block should produce a different root hash."""
        data_original = ["block_0", "block_1", "block_2", "block_3"]
        data_modified = ["block_0", "MODIFIED", "block_2", "block_3"]
        tree_orig = MerkleTree(data_original)
        tree_mod = MerkleTree(data_modified)
        self.assertNotEqual(tree_orig.get_root_hash(), tree_mod.get_root_hash())

    # ------------------------------------------------------------------
    # 4. Valid Merkle proof verifies correctly
    # ------------------------------------------------------------------
    def test_valid_proof_verifies(self):
        """A proof generated for a block should verify against the root hash."""
        data = ["alpha", "beta", "gamma", "delta"]
        tree = MerkleTree(data)
        root_hash = tree.get_root_hash()

        for i, block in enumerate(data):
            proof = tree.get_proof(i)
            self.assertTrue(
                MerkleTree.verify_proof(block, proof, root_hash),
                f"Proof for block {i} ('{block}') should verify correctly",
            )

    # ------------------------------------------------------------------
    # 5. Tampered data fails proof verification
    # ------------------------------------------------------------------
    def test_tampered_data_fails_proof(self):
        """Verifying with tampered data should fail."""
        data = ["alpha", "beta", "gamma", "delta"]
        tree = MerkleTree(data)
        root_hash = tree.get_root_hash()

        proof = tree.get_proof(0)
        # Use wrong data for verification
        self.assertFalse(
            MerkleTree.verify_proof("TAMPERED", proof, root_hash),
            "Tampered data should fail proof verification",
        )

    # ------------------------------------------------------------------
    # 6. Odd number of leaves: handled correctly
    # ------------------------------------------------------------------
    def test_odd_number_of_leaves(self):
        """Trees with odd numbers of leaves should build correctly."""
        data = ["one", "two", "three"]
        tree = MerkleTree(data)
        root_hash = tree.get_root_hash()
        self.assertIsInstance(root_hash, str)
        self.assertTrue(len(root_hash) > 0, "Root hash should not be empty")

        # Proofs should still verify
        for i, block in enumerate(data):
            proof = tree.get_proof(i)
            self.assertTrue(
                MerkleTree.verify_proof(block, proof, root_hash),
                f"Proof for odd-leaf block {i} should verify",
            )

    # ------------------------------------------------------------------
    # 7. Single block tree works
    # ------------------------------------------------------------------
    def test_single_block_tree(self):
        """A tree with one block should have root hash = hash of that block."""
        data = ["only_block"]
        tree = MerkleTree(data)
        expected_hash = self._sha256("only_block")
        self.assertEqual(tree.get_root_hash(), expected_hash)

        # Proof for the single block should verify
        proof = tree.get_proof(0)
        self.assertTrue(MerkleTree.verify_proof("only_block", proof, tree.get_root_hash()))

    # ------------------------------------------------------------------
    # 8. find_differences: correctly identifies changed blocks
    # ------------------------------------------------------------------
    def test_find_differences_identifies_changes(self):
        """find_differences should return the indices of differing blocks."""
        data_a = ["block_0", "block_1", "block_2", "block_3"]
        data_b = ["block_0", "CHANGED", "block_2", "CHANGED"]
        tree_a = MerkleTree(data_a)
        tree_b = MerkleTree(data_b)

        diffs = MerkleTree.find_differences(tree_a, tree_b)
        self.assertEqual(sorted(diffs), [1, 3])

    # ------------------------------------------------------------------
    # 9. find_differences: identical trees return empty list
    # ------------------------------------------------------------------
    def test_find_differences_identical_trees(self):
        """Identical trees should have no differences."""
        data = ["block_0", "block_1", "block_2", "block_3"]
        tree_a = MerkleTree(data)
        tree_b = MerkleTree(data)

        diffs = MerkleTree.find_differences(tree_a, tree_b)
        self.assertEqual(diffs, [])

    # ------------------------------------------------------------------
    # 10. Proof for each leaf index works
    # ------------------------------------------------------------------
    def test_proof_for_each_leaf_index(self):
        """Generate and verify proofs for every leaf in a larger tree."""
        data = [f"data_{i}" for i in range(8)]
        tree = MerkleTree(data)
        root_hash = tree.get_root_hash()

        for i in range(len(data)):
            proof = tree.get_proof(i)
            self.assertTrue(
                MerkleTree.verify_proof(data[i], proof, root_hash),
                f"Proof for leaf index {i} should verify",
            )
            # Also check that proofs have entries (except possibly for single-block)
            self.assertGreater(
                len(proof), 0,
                f"Proof for leaf {i} in an 8-block tree should have steps",
            )

    # ------------------------------------------------------------------
    # Bonus: MerkleNode stores attributes correctly
    # ------------------------------------------------------------------
    def test_merkle_node_attributes(self):
        """MerkleNode should store hash_value, left, right, and data."""
        node = MerkleNode(hash_value="abc123", left=None, right=None, data="hello")
        self.assertEqual(node.hash_value, "abc123")
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        self.assertEqual(node.data, "hello")


if __name__ == "__main__":
    unittest.main()
