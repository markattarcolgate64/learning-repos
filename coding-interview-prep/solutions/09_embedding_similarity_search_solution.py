"""
Embedding Similarity Search - Solution

Implements vector similarity search using two approaches:
1. Brute-force exact search via cosine similarity.
2. Approximate search via locality-sensitive hashing (LSH) with random
   hyperplane projections.
"""

import numpy as np


class BruteForceIndex:
    """Exact nearest-neighbour search via brute-force cosine similarity.

    Stores vectors in memory and compares every vector against the query at
    search time. Simple, exact, but O(n) per query.
    """

    def __init__(self) -> None:
        """Initialise the brute-force index."""
        self.vectors = {}
        self.ids = []

    def add(self, vector_id: str, vector: np.ndarray) -> None:
        """Add a vector to the index.

        Args:
            vector_id: A unique string identifier for the vector.
            vector: A 1-D numpy array representing the embedding.
        """
        self.vectors[vector_id] = vector
        self.ids.append(vector_id)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors.

        Args:
            a: First vector (1-D numpy array).
            b: Second vector (1-D numpy array).

        Returns:
            The cosine similarity as a float in [-1, 1]. Returns 0.0 if
            either vector has zero norm.
        """
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def search(self, query: np.ndarray, top_k: int = 5) -> list:
        """Find the top-k most similar vectors to the query.

        Args:
            query: A 1-D numpy array representing the query embedding.
            top_k: Number of results to return.

        Returns:
            A list of (vector_id, similarity_score) tuples sorted by
            similarity in descending order.
        """
        similarities = []
        for vid in self.ids:
            sim = self._cosine_similarity(query, self.vectors[vid])
            similarities.append((vid, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def batch_search(self, queries: np.ndarray, top_k: int = 5) -> list:
        """Search for multiple queries at once.

        Args:
            queries: A 2-D numpy array where each row is a query vector.
            top_k: Number of results to return per query.

        Returns:
            A list of result lists, one per query.
        """
        return [self.search(q, top_k) for q in queries]


class LSHIndex:
    """Approximate nearest-neighbour search via locality-sensitive hashing.

    Uses random hyperplane projections to hash vectors into binary codes.
    Multiple hash tables increase recall. Candidates are re-ranked by exact
    cosine similarity.
    """

    def __init__(
        self,
        dim: int,
        num_tables: int = 4,
        num_bits: int = 8,
        seed: int = 42,
    ) -> None:
        """Initialise the LSH index.

        Args:
            dim: Dimensionality of the input vectors.
            num_tables: Number of independent hash tables.
            num_bits: Number of hyperplane projections per table.
            seed: Random seed for reproducibility.
        """
        self.dim = dim
        self.num_tables = num_tables
        self.num_bits = num_bits

        rng = np.random.RandomState(seed)
        self.hyperplanes = [
            rng.randn(num_bits, dim) for _ in range(num_tables)
        ]
        self.hash_tables = [dict() for _ in range(num_tables)]
        self.vectors = {}

    def _hash_vector(self, vector: np.ndarray, table_idx: int) -> str:
        """Compute the LSH hash for a vector in a given table.

        Args:
            vector: A 1-D numpy array to hash.
            table_idx: Index of the hash table.

        Returns:
            A binary string of length num_bits (e.g. '01101001').
        """
        projections = self.hyperplanes[table_idx] @ vector
        bits = ''.join(['1' if p >= 0 else '0' for p in projections])
        return bits

    def add(self, vector_id: str, vector: np.ndarray) -> None:
        """Add a vector to all hash tables.

        Args:
            vector_id: A unique string identifier for the vector.
            vector: A 1-D numpy array representing the embedding.
        """
        self.vectors[vector_id] = vector
        for table_idx in range(self.num_tables):
            hash_key = self._hash_vector(vector, table_idx)
            if hash_key not in self.hash_tables[table_idx]:
                self.hash_tables[table_idx][hash_key] = set()
            self.hash_tables[table_idx][hash_key].add(vector_id)

    def search(self, query: np.ndarray, top_k: int = 5) -> list:
        """Find approximate top-k nearest neighbours for a query.

        Args:
            query: A 1-D numpy array representing the query embedding.
            top_k: Number of results to return.

        Returns:
            A list of (vector_id, similarity_score) tuples sorted by
            similarity in descending order.
        """
        # Collect candidates from all tables
        candidates = set()
        for table_idx in range(self.num_tables):
            hash_key = self._hash_vector(query, table_idx)
            if hash_key in self.hash_tables[table_idx]:
                candidates.update(self.hash_tables[table_idx][hash_key])

        # Compute exact cosine similarity for candidates
        results = []
        for vid in candidates:
            vec = self.vectors[vid]
            norm_q = np.linalg.norm(query)
            norm_v = np.linalg.norm(vec)
            if norm_q == 0.0 or norm_v == 0.0:
                sim = 0.0
            else:
                sim = float(np.dot(query, vec) / (norm_q * norm_v))
            results.append((vid, sim))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
