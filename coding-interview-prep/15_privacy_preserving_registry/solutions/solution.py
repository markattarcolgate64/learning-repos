"""
Privacy-Preserving Set Membership - Solution

A registry combining salted SHA-256 commitments with a hand-rolled Bloom filter
for fast, space-efficient, privacy-preserving duplicate detection.
"""

import hashlib
import json
import base64
import math
import os
from typing import Optional


class PrivacyPreservingRegistry:
    """A registry that checks set membership without storing raw identifiers."""

    def __init__(self, expected_items: int = 100_000, fp_rate: float = 0.001) -> None:
        self.expected_items = expected_items
        self.fp_rate = fp_rate

        # Bloom filter sizing
        # m = -n * ln(p) / (ln2)^2
        n = max(expected_items, 1)
        ln2 = math.log(2)
        self._m = max(int(-n * math.log(fp_rate) / (ln2 ** 2)), 64)
        # k = (m / n) * ln2
        self._k = max(int((self._m / n) * ln2), 1)

        # Bit array as bytearray
        self._bits = bytearray((self._m + 7) // 8)

        # Exact set for authoritative lookups
        self._exact_set: set[str] = set()

    # ------------------------------------------------------------------
    # Internal Bloom filter helpers
    # ------------------------------------------------------------------
    def _bloom_indices(self, commitment: str) -> list[int]:
        """Derive k bit positions from a commitment string using SHA-256."""
        digest = hashlib.sha256(commitment.encode()).digest()  # 32 bytes

        # We need k indices.  Slice the 32-byte digest into k segments.
        # If k > 16 (unlikely), wrap around with a secondary hash.
        indices = []
        data = digest
        while len(indices) < self._k:
            # Each index uses 2 bytes (16 bits) for mod m
            for offset in range(0, len(data) - 1, 2):
                if len(indices) >= self._k:
                    break
                val = int.from_bytes(data[offset : offset + 2], "big")
                indices.append(val % self._m)
            if len(indices) < self._k:
                # Hash the previous digest to get more bytes
                data = hashlib.sha256(data).digest()
        return indices

    def _bloom_add(self, commitment: str) -> None:
        """Set all k bits for the given commitment."""
        for idx in self._bloom_indices(commitment):
            byte_pos = idx // 8
            bit_pos = idx % 8
            self._bits[byte_pos] |= 1 << bit_pos

    def _bloom_check(self, commitment: str) -> bool:
        """Return True if all k bits are set (possibly registered)."""
        for idx in self._bloom_indices(commitment):
            byte_pos = idx // 8
            bit_pos = idx % 8
            if not (self._bits[byte_pos] & (1 << bit_pos)):
                return False
        return True

    # ------------------------------------------------------------------
    # Commitment helpers
    # ------------------------------------------------------------------
    def commit(self, identifier: str, salt: Optional[str] = None) -> str:
        """Create commitment = SHA256(salt + identifier) as hex."""
        if salt is None:
            salt = os.urandom(16).hex()
        h = hashlib.sha256((salt + identifier).encode())
        return h.hexdigest()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def register(self, commitment: str) -> bool:
        """Register a commitment. Returns True if new, False if duplicate."""
        is_new = commitment not in self._exact_set
        self._exact_set.add(commitment)
        self._bloom_add(commitment)
        return is_new

    # ------------------------------------------------------------------
    # Duplicate checks
    # ------------------------------------------------------------------
    def check_duplicate_fast(self, commitment: str) -> bool:
        """Bloom filter check only (may have false positives)."""
        return self._bloom_check(commitment)

    def check_duplicate_exact(self, commitment: str) -> bool:
        """Exact set check. Returns True if definitely registered."""
        return commitment in self._exact_set

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------
    def size(self) -> int:
        """Return the number of registered commitments."""
        return len(self._exact_set)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------
    def export_state(self) -> bytes:
        """Serialise the full registry state to bytes."""
        state = {
            "expected_items": self.expected_items,
            "fp_rate": self.fp_rate,
            "m": self._m,
            "k": self._k,
            "bits": base64.b64encode(bytes(self._bits)).decode("ascii"),
            "exact_set": sorted(self._exact_set),
        }
        return json.dumps(state).encode("utf-8")

    @classmethod
    def import_state(cls, data: bytes) -> "PrivacyPreservingRegistry":
        """Reconstruct a registry from bytes produced by export_state."""
        state = json.loads(data.decode("utf-8"))

        registry = cls.__new__(cls)
        registry.expected_items = state["expected_items"]
        registry.fp_rate = state["fp_rate"]
        registry._m = state["m"]
        registry._k = state["k"]
        registry._bits = bytearray(base64.b64decode(state["bits"]))
        registry._exact_set = set(state["exact_set"])

        return registry
