"""
Reference solution for Iris Code Matching Engine.

Key design decisions:
- Store codes as Python int (2048-bit) for fast XOR + bit_count via int.bit_count()
- Also keep a bytes→int lookup for O(1) conversion at query time
- Use int.bit_count() (Python 3.10+) which is a single CPU instruction on modern hardware
- Sorted output by distance for deterministic results
"""

import os
from dataclasses import dataclass


@dataclass
class MatchResult:
    iris_id: str
    distance: float


CODE_BITS = 2048
CODE_BYTES = CODE_BITS // 8


class IrisCodeMatcher:

    def __init__(self) -> None:
        # Parallel arrays for cache-friendly iteration
        self._ids: list[str] = []
        self._codes_int: list[int] = []
        # For O(1) contains/remove by ID
        self._id_to_index: dict[str, int] = {}

    def add(self, iris_id: str, code: bytes) -> None:
        if len(code) != CODE_BYTES:
            raise ValueError(f"Code must be {CODE_BYTES} bytes, got {len(code)}")
        if iris_id in self._id_to_index:
            raise ValueError(f"Duplicate iris_id: {iris_id}")

        code_int = int.from_bytes(code, byteorder="big")
        idx = len(self._ids)
        self._ids.append(iris_id)
        self._codes_int.append(code_int)
        self._id_to_index[iris_id] = idx

    def remove(self, iris_id: str) -> bool:
        if iris_id not in self._id_to_index:
            return False

        idx = self._id_to_index.pop(iris_id)
        last_idx = len(self._ids) - 1

        if idx != last_idx:
            # Swap with last element for O(1) removal
            last_id = self._ids[last_idx]
            self._ids[idx] = last_id
            self._codes_int[idx] = self._codes_int[last_idx]
            self._id_to_index[last_id] = idx

        self._ids.pop()
        self._codes_int.pop()
        return True

    def query(self, code: bytes, threshold: float = 0.32) -> list[MatchResult]:
        if len(code) != CODE_BYTES:
            raise ValueError(f"Code must be {CODE_BYTES} bytes, got {len(code)}")

        query_int = int.from_bytes(code, byteorder="big")
        threshold_bits = threshold * CODE_BITS
        matches = []

        for i, stored_int in enumerate(self._codes_int):
            diff_bits = (query_int ^ stored_int).bit_count()
            if diff_bits <= threshold_bits:
                distance = diff_bits / CODE_BITS
                matches.append(MatchResult(iris_id=self._ids[i], distance=distance))

        matches.sort(key=lambda m: m.distance)
        return matches

    def batch_query(
        self, codes: list[bytes], threshold: float = 0.32
    ) -> list[list[MatchResult]]:
        return [self.query(code, threshold) for code in codes]

    def __len__(self) -> int:
        return len(self._ids)

    def __contains__(self, iris_id: str) -> bool:
        return iris_id in self._id_to_index

    @staticmethod
    def hamming_distance(a: bytes, b: bytes) -> float:
        a_int = int.from_bytes(a, byteorder="big")
        b_int = int.from_bytes(b, byteorder="big")
        return (a_int ^ b_int).bit_count() / CODE_BITS

    @staticmethod
    def random_code() -> bytes:
        return os.urandom(CODE_BYTES)
