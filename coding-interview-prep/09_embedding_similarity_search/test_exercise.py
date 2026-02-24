"""
Tests for Embedding Similarity Search (Brute Force and LSH).

Run with:
    python -m unittest 09_embedding_similarity_search.test_exercise -v
"""

import unittest
import numpy as np
from .exercise import BruteForceIndex, LSHIndex


class TestBruteForceIndex(unittest.TestCase):
    """Tests for exact brute-force cosine similarity search."""

    # ------------------------------------------------------------------
    # 1. Cosine similarity: parallel vectors = 1.0
    # ------------------------------------------------------------------

    def test_cosine_parallel_vectors(self):
        """Parallel (identical direction) vectors should have cosine similarity 1.0."""
        idx = BruteForceIndex()
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([3.0, 0.0, 0.0])
        sim = idx._cosine_similarity(a, b)
        self.assertAlmostEqual(sim, 1.0, places=6)

    # ------------------------------------------------------------------
    # 2. Cosine similarity: orthogonal vectors = 0.0
    # ------------------------------------------------------------------

    def test_cosine_orthogonal_vectors(self):
        """Orthogonal vectors should have cosine similarity 0.0."""
        idx = BruteForceIndex()
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([0.0, 1.0, 0.0])
        sim = idx._cosine_similarity(a, b)
        self.assertAlmostEqual(sim, 0.0, places=6)

    # ------------------------------------------------------------------
    # 3. Self-search: vector is its own nearest neighbor
    # ------------------------------------------------------------------

    def test_self_is_nearest_neighbor(self):
        """A vector should be its own nearest neighbor when searched."""
        idx = BruteForceIndex()
        v1 = np.array([1.0, 0.0])
        v2 = np.array([0.0, 1.0])
        v3 = np.array([1.0, 1.0])
        idx.add("v1", v1)
        idx.add("v2", v2)
        idx.add("v3", v3)

        results = idx.search(v1, top_k=3)
        self.assertEqual(results[0][0], "v1")
        self.assertAlmostEqual(results[0][1], 1.0, places=6)

    # ------------------------------------------------------------------
    # 4. Search returns results sorted descending
    # ------------------------------------------------------------------

    def test_search_sorted_descending(self):
        """Search results should be sorted by similarity in descending order."""
        idx = BruteForceIndex()
        idx.add("a", np.array([1.0, 0.0]))
        idx.add("b", np.array([1.0, 1.0]))
        idx.add("c", np.array([0.0, 1.0]))

        query = np.array([1.0, 0.0])
        results = idx.search(query, top_k=3)
        scores = [score for _, score in results]
        self.assertEqual(scores, sorted(scores, reverse=True),
                         "Results are not in descending order of similarity.")

    # ------------------------------------------------------------------
    # 5. top_k: returns correct number of results
    # ------------------------------------------------------------------

    def test_top_k_count(self):
        """search(top_k=k) should return exactly k results (or fewer if index is smaller)."""
        idx = BruteForceIndex()
        for i in range(10):
            idx.add(f"v{i}", np.random.randn(4))

        results = idx.search(np.random.randn(4), top_k=5)
        self.assertEqual(len(results), 5)

        results = idx.search(np.random.randn(4), top_k=20)
        self.assertEqual(len(results), 10, "Should return all vectors when top_k > n.")

    # ------------------------------------------------------------------
    # 6. batch_search: works for multiple queries
    # ------------------------------------------------------------------

    def test_batch_search(self):
        """batch_search should return one result list per query."""
        idx = BruteForceIndex()
        idx.add("a", np.array([1.0, 0.0]))
        idx.add("b", np.array([0.0, 1.0]))
        idx.add("c", np.array([1.0, 1.0]))

        queries = np.array([[1.0, 0.0], [0.0, 1.0]])
        all_results = idx.batch_search(queries, top_k=2)

        self.assertEqual(len(all_results), 2)
        # First query [1,0] should find "a" first
        self.assertEqual(all_results[0][0][0], "a")
        # Second query [0,1] should find "b" first
        self.assertEqual(all_results[1][0][0], "b")

    # ------------------------------------------------------------------
    # Extra: zero vector handling
    # ------------------------------------------------------------------

    def test_zero_vector_similarity(self):
        """Cosine similarity with a zero vector should return 0.0."""
        idx = BruteForceIndex()
        a = np.array([1.0, 2.0])
        z = np.array([0.0, 0.0])
        self.assertAlmostEqual(idx._cosine_similarity(a, z), 0.0)
        self.assertAlmostEqual(idx._cosine_similarity(z, a), 0.0)


class TestLSHIndex(unittest.TestCase):
    """Tests for approximate nearest-neighbour search via LSH."""

    # ------------------------------------------------------------------
    # 7. LSH finds true nearest neighbor with high probability
    # ------------------------------------------------------------------

    def test_lsh_finds_true_nearest_neighbor(self):
        """LSH with enough tables should find the true nearest neighbor."""
        dim = 16
        rng = np.random.RandomState(42)

        # Build an index with many tables for high recall
        lsh = LSHIndex(dim=dim, num_tables=16, num_bits=8, seed=42)
        bf = BruteForceIndex()

        # Add a set of random vectors
        vectors = {}
        for i in range(50):
            v = rng.randn(dim)
            vid = f"v{i}"
            vectors[vid] = v
            lsh.add(vid, v)
            bf.add(vid, v)

        # Query with a vector near one of the stored ones
        query = vectors["v0"] + rng.randn(dim) * 0.01

        bf_results = bf.search(query, top_k=1)
        lsh_results = lsh.search(query, top_k=1)

        self.assertGreater(len(lsh_results), 0, "LSH returned no results.")
        # The true nearest neighbor should be found by LSH
        self.assertEqual(lsh_results[0][0], bf_results[0][0],
                         "LSH did not find the true nearest neighbor.")

    # ------------------------------------------------------------------
    # 8. LSH search returns results sorted descending
    # ------------------------------------------------------------------

    def test_lsh_results_sorted(self):
        """LSH search results should be sorted by similarity descending."""
        dim = 8
        lsh = LSHIndex(dim=dim, num_tables=8, num_bits=4, seed=42)

        rng = np.random.RandomState(123)
        for i in range(30):
            lsh.add(f"v{i}", rng.randn(dim))

        results = lsh.search(rng.randn(dim), top_k=5)
        if len(results) > 1:
            scores = [s for _, s in results]
            self.assertEqual(scores, sorted(scores, reverse=True),
                             "LSH results are not sorted in descending order.")

    # ------------------------------------------------------------------
    # 9. Add and search basic functionality works
    # ------------------------------------------------------------------

    def test_lsh_add_and_search_basic(self):
        """Adding vectors and searching should return results."""
        dim = 4
        lsh = LSHIndex(dim=dim, num_tables=4, num_bits=4, seed=0)

        lsh.add("x", np.array([1.0, 0.0, 0.0, 0.0]))
        lsh.add("y", np.array([0.0, 1.0, 0.0, 0.0]))
        lsh.add("z", np.array([1.0, 0.1, 0.0, 0.0]))

        results = lsh.search(np.array([1.0, 0.0, 0.0, 0.0]), top_k=3)
        self.assertIsInstance(results, list)
        # Should find at least the query-identical vector "x"
        result_ids = [vid for vid, _ in results]
        self.assertIn("x", result_ids,
                       "LSH did not find the exact match vector.")

    # ------------------------------------------------------------------
    # Extra: LSH top_k respects the limit
    # ------------------------------------------------------------------

    def test_lsh_top_k_limit(self):
        """LSH should return at most top_k results."""
        dim = 8
        lsh = LSHIndex(dim=dim, num_tables=8, num_bits=4, seed=42)
        rng = np.random.RandomState(7)
        for i in range(50):
            lsh.add(f"v{i}", rng.randn(dim))

        results = lsh.search(rng.randn(dim), top_k=3)
        self.assertLessEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()
