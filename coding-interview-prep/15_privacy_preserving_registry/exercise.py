"""
Privacy-Preserving Set Membership
==================================
Category   : Cryptography / Data Structures
Difficulty : *** (3/5)

Problem
-------
Implement a privacy-preserving registry that can check whether a biometric
commitment has already been registered, without storing the raw biometric
identifier.

The registry has two layers:

1. **Cryptographic commitments** -- raw identifiers are never stored.  Instead,
   a salted SHA-256 hash (the "commitment") is computed and used as the key.
2. **Bloom filter** -- a space-efficient probabilistic set that supports fast
   ``O(k)`` membership queries with a tuneable false-positive rate.  The Bloom
   filter sits in front of an exact set and is useful when the registry is
   distributed across nodes that only keep the compact filter.

You must implement the Bloom filter from scratch (no external libraries).

Real-world motivation
---------------------
Tools for Humanity's World ID protocol must ensure uniqueness ("one person, one
proof") without ever storing plaintext biometric data.  A commitment scheme
hides the original iris code, while a Bloom filter enables lightweight,
privacy-friendly duplicate checks that can run on edge devices or be synced
across a distributed network with minimal bandwidth.

Hints
-----
1. A commitment is simply ``SHA256(salt + identifier)`` expressed as a hex
   string.  Generate a random 16-byte salt when none is provided.
2. Optimal Bloom filter parameters: ``m = -n * ln(p) / (ln 2)^2`` bits and
   ``k = (m / n) * ln 2`` hash functions, where *n* is the expected number of
   items and *p* is the target false-positive rate.
3. Derive *k* hash indices from a single SHA-256 digest by slicing it into *k*
   equal-width segments and converting each segment to an integer mod *m*.
4. For ``export_state`` / ``import_state``, serialise the bit-array with
   ``base64`` and wrap everything in JSON.

Run command
-----------
    python -m unittest 15_privacy_preserving_registry.test_exercise -v
"""

import hashlib
import json
import base64
import math
import os
from typing import Optional


class PrivacyPreservingRegistry:
    """A registry that checks set membership without storing raw identifiers.

    Combines cryptographic commitments (salted SHA-256) with a hand-rolled
    Bloom filter for fast, space-efficient duplicate detection.
    """

    def __init__(self, expected_items: int = 100_000, fp_rate: float = 0.001) -> None:
        """Initialise the registry with a Bloom filter sized for the expected load.

        Args:
            expected_items: Anticipated number of unique commitments.
            fp_rate: Target false-positive probability for the Bloom filter.
        """
        raise NotImplementedError("Implement __init__")

    # ------------------------------------------------------------------
    # Commitment helpers
    # ------------------------------------------------------------------
    def commit(self, identifier: str, salt: Optional[str] = None) -> str:
        """Create a cryptographic commitment for *identifier*.

        The commitment is ``SHA256(salt + identifier)`` encoded as a lowercase
        hex string.  If *salt* is ``None``, a random 16-byte hex salt is
        generated.

        Args:
            identifier: The raw identifier to commit (e.g. an iris code string).
            salt: Optional hex-encoded salt.  A random one is generated if
                omitted.

        Returns:
            The commitment as a 64-character lowercase hex string.
        """
        raise NotImplementedError("Implement commit")

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def register(self, commitment: str) -> bool:
        """Register a commitment.

        Returns ``True`` if the commitment is new (was not previously
        registered) and ``False`` if it is a duplicate.  Either way the
        commitment is added to both the Bloom filter and the exact set.

        Args:
            commitment: A hex-encoded commitment string.

        Returns:
            ``True`` if newly registered, ``False`` if duplicate.
        """
        raise NotImplementedError("Implement register")

    # ------------------------------------------------------------------
    # Duplicate checks
    # ------------------------------------------------------------------
    def check_duplicate_fast(self, commitment: str) -> bool:
        """Bloom-filter-only membership check (may have false positives).

        Returns ``True`` if the commitment is *possibly* registered (all
        Bloom filter bits are set), ``False`` if it is *definitely not*
        registered.

        Args:
            commitment: A hex-encoded commitment string.

        Returns:
            ``True`` if possibly registered, ``False`` if definitely not.
        """
        raise NotImplementedError("Implement check_duplicate_fast")

    def check_duplicate_exact(self, commitment: str) -> bool:
        """Exact membership check against the authoritative set.

        Returns ``True`` if the commitment is *definitely* registered.

        Args:
            commitment: A hex-encoded commitment string.

        Returns:
            ``True`` if registered, ``False`` otherwise.
        """
        raise NotImplementedError("Implement check_duplicate_exact")

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------
    def size(self) -> int:
        """Return the number of registered commitments.

        Returns:
            Count of unique commitments that have been registered.
        """
        raise NotImplementedError("Implement size")

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------
    def export_state(self) -> bytes:
        """Serialise the full registry state to bytes.

        The format should capture the Bloom filter bit-array, the exact set,
        and all configuration parameters so that ``import_state`` can fully
        reconstruct the registry.

        Returns:
            A ``bytes`` object containing the serialised state.
        """
        raise NotImplementedError("Implement export_state")

    @classmethod
    def import_state(cls, data: bytes) -> "PrivacyPreservingRegistry":
        """Reconstruct a registry from bytes produced by ``export_state``.

        Args:
            data: Bytes previously returned by ``export_state``.

        Returns:
            A new :class:`PrivacyPreservingRegistry` instance with identical
            state.
        """
        raise NotImplementedError("Implement import_state")
