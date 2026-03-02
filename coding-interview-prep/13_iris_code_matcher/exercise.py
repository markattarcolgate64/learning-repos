"""
Iris Code Matching Engine
==========================
Category   : Biometrics / Performance
Difficulty : *** (3/5)

Problem
-------
Build an iris code matching system. Iris codes are binary vectors (2048 bits)
that represent the unique pattern of a person's iris. Given a query iris code,
find all matches in a database using normalised Hamming distance with a
configurable threshold.

Your matcher must support:
  - Adding iris codes to the database
  - Querying for matches against the entire database
  - Batch queries for throughput
  - Scaling to 100K+ codes with sub-100ms single query time

Normalised Hamming distance is the fraction of bits that differ between two
codes: distance = popcount(a XOR b) / total_bits.  A distance below 0.32
typically indicates the same iris; above 0.45 indicates different irises.

Real-world motivation
---------------------
This is the core problem at Tools for Humanity (Worldcoin).  When a person
scans their iris at an Orb device, the resulting iris code must be compared
against every previously-registered code to ensure the person hasn't already
signed up.  At scale this means matching against tens of millions of codes
with strict latency requirements.

Hints
-----
1. Represent each iris code as a Python ``bytes`` object (2048 bits = 256 bytes).
2. For popcount of XOR, you can convert to ``int`` and use ``int.bit_count()``
   (Python 3.10+), or iterate over bytes with a lookup table.
3. For batch queries, consider using numpy (if available) to vectorise the
   XOR + popcount across all database codes at once.
4. Think about early termination — if the first 128 bits already exceed the
   threshold, you can skip the remaining bits.

Run command
-----------
    python -m unittest 13_iris_code_matcher.test_exercise -v
"""

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class MatchResult:
    """A single match from a query."""
    iris_id: str
    distance: float  # normalised Hamming distance (0.0 – 1.0)


# ---------------------------------------------------------------------------
# Iris Code Matcher
# ---------------------------------------------------------------------------

CODE_BITS = 2048
CODE_BYTES = CODE_BITS // 8  # 256


class IrisCodeMatcher:
    """Database of iris codes supporting efficient Hamming-distance queries.

    Each iris code is a ``bytes`` object of length 256 (2048 bits).
    """

    def __init__(self) -> None:
        """Initialise an empty iris code database."""
        # TODO: Set up internal storage for iris codes.
        #       Consider what data structure gives you fast batch XOR.
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def add(self, iris_id: str, code: bytes) -> None:
        """Register a new iris code.

        Args:
            iris_id: Unique identifier for this iris.
            code:    Raw iris code, exactly 256 bytes (2048 bits).

        Raises:
            ValueError: If *code* is not 256 bytes or *iris_id* is duplicate.
        """
        # TODO: Validate inputs and store the code.
        raise NotImplementedError

    def remove(self, iris_id: str) -> bool:
        """Remove an iris code by ID.

        Returns:
            True if the code was found and removed, False otherwise.
        """
        # TODO: Remove from storage.
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def query(self, code: bytes, threshold: float = 0.32) -> list[MatchResult]:
        """Find all iris codes within *threshold* normalised Hamming distance.

        Args:
            code:      Query iris code (256 bytes).
            threshold: Maximum normalised Hamming distance to consider a match.

        Returns:
            List of MatchResult sorted by distance (ascending).
        """
        # TODO: Compare *code* against every stored code.
        #       Return matches where distance <= threshold, sorted ascending.
        raise NotImplementedError

    def batch_query(
        self, codes: list[bytes], threshold: float = 0.32
    ) -> list[list[MatchResult]]:
        """Run multiple queries and return results for each.

        Args:
            codes:     List of query iris codes.
            threshold: Maximum normalised Hamming distance.

        Returns:
            List of result lists, one per query code.
        """
        # TODO: Run self.query for each code.  Consider vectorised approaches
        #       for better throughput.
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """Return the number of iris codes in the database."""
        # TODO
        raise NotImplementedError

    def __contains__(self, iris_id: str) -> bool:
        """Check whether an iris ID is registered."""
        # TODO
        raise NotImplementedError

    @staticmethod
    def hamming_distance(a: bytes, b: bytes) -> float:
        """Compute normalised Hamming distance between two iris codes.

        Returns:
            Float in [0.0, 1.0] representing the fraction of differing bits.
        """
        # TODO: XOR the two byte-strings and count the differing bits.
        raise NotImplementedError

    @staticmethod
    def random_code() -> bytes:
        """Generate a random iris code (useful for testing)."""
        import os
        return os.urandom(CODE_BYTES)
