"""
Embedding Similarity Search
============================
Category   : ML Engineering
Difficulty : *** (3/5)

Problem
-------
Implement vector similarity search using two approaches:

1. **Brute-force** -- compute cosine similarity between the query and every
   stored vector, then return the top-k most similar results.
2. **Approximate (LSH)** -- use locality-sensitive hashing with random
   hyperplane projections to bucket similar vectors together, allowing
   sub-linear search at the cost of some accuracy.

Real-world motivation
---------------------
Embedding similarity search is the backbone of modern retrieval systems:
  - Semantic search engines (e.g. Google, Bing) rank documents by embedding
    similarity to a query embedding.
  - Recommendation systems (Spotify, Netflix) find items whose embeddings
    are close to user-preference vectors.
  - Retrieval-Augmented Generation (RAG) pipelines retrieve relevant context
    chunks by comparing query embeddings against a vector store.

Brute-force search is exact but O(n) per query. Locality-sensitive hashing
(LSH) trades a small amount of accuracy for dramatically faster lookups by
hashing similar vectors into the same bucket with high probability.

Hints
-----
1. Cosine similarity: dot(a, b) / (norm(a) * norm(b)).  Handle zero-norm
   vectors by returning 0.0.
2. For LSH, generate random hyperplanes from a normal distribution.  The
   sign of dot(vector, hyperplane) gives one bit of the hash.
3. Use multiple hash tables to increase recall -- a candidate is any vector
   that shares a bucket with the query in *any* table.
4. After collecting LSH candidates, re-rank them by exact cosine similarity
   to get the final top-k results.

Run command
-----------
    pytest 09_embedding_similarity_search/test_exercise.py -v
"""

import numpy as np


class BruteForceIndex:
    """Exact nearest-neighbour search via brute-force cosine similarity.

    Stores vectors in memory and compares every vector against the query at
    search time.  Simple, exact, but O(n) per query.
    """

    def __init__(self) -> None:
        """Initialise the brute-force index.

        Sets up internal storage for vectors and their corresponding IDs.
        """
        # TODO: Create a dict to map vector_id -> np.ndarray.
        # TODO: Create a list to maintain insertion-order IDs.
        pass

    def add(self, vector_id: str, vector: np.ndarray) -> None:
        """Add a vector to the index.

        Args:
            vector_id: A unique string identifier for the vector.
            vector: A 1-D numpy array representing the embedding.
        """
        # TODO: Store the vector in the dict keyed by vector_id.
        # TODO: Append vector_id to the ID list.
        pass

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors.

        Args:
            a: First vector (1-D numpy array).
            b: Second vector (1-D numpy array).

        Returns:
            The cosine similarity as a float in [-1, 1].  Returns 0.0 if
            either vector has zero norm.
        """
        # TODO: Compute dot(a, b) / (norm(a) * norm(b)).
        # Hint: Use np.dot, np.linalg.norm.  Guard against division by zero.
        pass

    def search(self, query: np.ndarray, top_k: int = 5) -> list:
        """Find the top-k most similar vectors to the query.

        Args:
            query: A 1-D numpy array representing the query embedding.
            top_k: Number of results to return.

        Returns:
            A list of (vector_id, similarity_score) tuples sorted by
            similarity in descending order.
        """
        # TODO: Compute cosine similarity between query and every stored vector.
        # TODO: Sort results by similarity descending.
        # TODO: Return the top_k entries as [(id, score), ...].
        # Hint: Use a list comprehension, then sorted(..., key=..., reverse=True).
        pass

    def batch_search(self, queries: np.ndarray, top_k: int = 5) -> list:
        """Search for multiple queries at once.

        Args:
            queries: A 2-D numpy array where each row is a query vector.
            top_k: Number of results to return per query.

        Returns:
            A list of result lists, one per query.  Each inner list contains
            (vector_id, similarity_score) tuples sorted descending.
        """
        # TODO: Call self.search for each row in queries.
        # Hint: [self.search(q, top_k) for q in queries]
        pass


class LSHIndex:
    """Approximate nearest-neighbour search via locality-sensitive hashing.

    Uses random hyperplane projections to hash vectors into binary codes.
    Multiple hash tables increase recall.  Candidates are re-ranked by exact
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
            num_tables: Number of independent hash tables (more = higher
                recall, more memory).
            num_bits: Number of hyperplane projections per table (more =
                finer buckets, fewer collisions).
            seed: Random seed for reproducibility.
        """
        # TODO: Store dim, num_tables, num_bits.
        # TODO: Generate random hyperplanes for each table.
        #       Shape per table: (num_bits, dim), drawn from np.random.randn.
        # TODO: Create a list of hash-table dicts (one per table).
        # TODO: Create a dict to store vectors by ID.
        # Hint: Use np.random.RandomState(seed) for reproducibility.
        #       self.hyperplanes[i] has shape (num_bits, dim).
        pass

    def _hash_vector(self, vector: np.ndarray, table_idx: int) -> str:
        """Compute the LSH hash for a vector in a given table.

        Projects the vector onto the table's hyperplanes and converts the
        signs of the dot products into a binary hash string.

        Args:
            vector: A 1-D numpy array to hash.
            table_idx: Index of the hash table (selects which hyperplanes).

        Returns:
            A binary string of length num_bits (e.g. '01101001').
        """
        # TODO: Compute projections = hyperplanes[table_idx] @ vector.
        # TODO: Convert signs to bits: '1' if projection >= 0 else '0'.
        # TODO: Join bits into a single string.
        # Hint: ''.join(['1' if p >= 0 else '0' for p in projections])
        pass

    def add(self, vector_id: str, vector: np.ndarray) -> None:
        """Add a vector to all hash tables.

        Args:
            vector_id: A unique string identifier for the vector.
            vector: A 1-D numpy array representing the embedding.
        """
        # TODO: Store the vector in the vectors dict.
        # TODO: For each table, compute the hash and insert vector_id into
        #       the corresponding bucket.
        # Hint: Each bucket is a set of vector IDs sharing the same hash.
        pass

    def search(self, query: np.ndarray, top_k: int = 5) -> list:
        """Find approximate top-k nearest neighbours for a query.

        Hashes the query in each table, collects candidate IDs from matching
        buckets, then re-ranks candidates by exact cosine similarity.

        Args:
            query: A 1-D numpy array representing the query embedding.
            top_k: Number of results to return.

        Returns:
            A list of (vector_id, similarity_score) tuples sorted by
            similarity in descending order.
        """
        # TODO: Collect candidate IDs from all tables (union of bucket hits).
        # TODO: For each candidate, compute exact cosine similarity with query.
        # TODO: Sort candidates by similarity descending and return top_k.
        # Hint: Use a set to deduplicate candidates across tables.
        #       Re-use the cosine similarity formula from BruteForceIndex.
        pass
