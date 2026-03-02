"""
Secure Audit Log
=================
Category   : Security / Data Integrity
Difficulty : **** (4/5)

Problem
-------
Build a tamper-evident log for verification events using hash chains.
Every entry's hash includes the previous entry's hash, forming an
immutable chain (like a simplified blockchain). The log must support
appending entries, verifying chain integrity, generating inclusion
proofs, and serialization for persistence.

Real-world motivation
---------------------
Tools for Humanity processes billions of identity verifications. Regulators
and auditors need confidence that verification records haven't been
tampered with after the fact. A hash-chained audit log provides
cryptographic guarantees of data integrity without requiring a full
blockchain.

Hints
-----
1. Each entry's hash = SHA256(previous_hash + index + timestamp + event_data).
2. The first entry (index 0) uses a well-known genesis hash (e.g., 32 zero bytes).
3. For inclusion proofs, you need to return enough information to recompute
   the hash chain from the entry to the current head.
4. Use json for serialization — store entries as a list of dicts.

Run command
-----------
    python -m unittest 17_secure_audit_log.test_exercise -v
"""

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Optional

GENESIS_HASH = "0" * 64  # 64 hex zeros (SHA-256 of nothing, conceptually)


@dataclass
class LogEntry:
    """A single entry in the audit log."""
    index: int
    timestamp: float
    event_data: str
    previous_hash: str
    entry_hash: str


@dataclass
class InclusionProof:
    """Proof that a specific entry is part of a valid chain.

    Contains the entry itself and all entries from that index to the
    current head (inclusive), allowing independent verification.
    """
    entry: LogEntry
    chain_to_head: list  # list[LogEntry] from this index to head (inclusive)


def compute_hash(previous_hash: str, index: int, timestamp: float,
                 event_data: str) -> str:
    """Compute the SHA-256 hash for a log entry.

    The hash is computed over the concatenation of:
        previous_hash + index + timestamp + event_data

    Args:
        previous_hash: The hash of the previous entry (or GENESIS_HASH).
        index: The entry's position in the log.
        timestamp: The entry's timestamp.
        event_data: The event data string.

    Returns:
        The hex-encoded SHA-256 digest.
    """
    return hashlib.sha256(
        f"{previous_hash}{index}{timestamp}{event_data}".encode()
    ).hexdigest()


class AuditLog:
    """A tamper-evident, hash-chained audit log.

    Each entry's hash incorporates the previous entry's hash, forming
    an immutable chain from genesis to head. Supports integrity
    verification, inclusion proofs, and JSON serialization.
    """

    def __init__(self) -> None:
        """Initialise an empty audit log with the genesis hash."""
        # TODO: Create an empty list for entries and store the genesis hash.
        raise NotImplementedError

    def append(self, event_data: str, timestamp: Optional[float] = None) -> LogEntry:
        """Append a new entry to the log.

        Computes the hash chain link from the previous entry (or genesis)
        and stores the new entry.

        Args:
            event_data: The event data string to record.
            timestamp: Optional timestamp; defaults to time.time().

        Returns:
            The newly created LogEntry.
        """
        # TODO: Determine the previous hash (genesis if empty, else last entry's hash).
        #       Compute the new entry's hash, create the LogEntry, and append it.
        raise NotImplementedError

    def get(self, index: int) -> Optional[LogEntry]:
        """Retrieve a log entry by its index.

        Args:
            index: The zero-based index of the entry.

        Returns:
            The LogEntry at that index, or None if out of range.
        """
        # TODO: Return the entry at the given index, or None.
        raise NotImplementedError

    def head(self) -> Optional[LogEntry]:
        """Return the most recent log entry, or None if the log is empty."""
        # TODO: Return the last entry, or None.
        raise NotImplementedError

    def __len__(self) -> int:
        """Return the number of entries in the log."""
        # TODO: Return the length of the entries list.
        raise NotImplementedError

    def verify_integrity(self) -> bool:
        """Verify the entire hash chain from genesis to head.

        Recomputes every entry's hash and checks that:
        1. Each entry's previous_hash matches the prior entry's entry_hash.
        2. Each entry's entry_hash matches the recomputed hash.

        Returns:
            True if the chain is intact, False if any tampering is detected.
        """
        # TODO: Walk the chain and verify each link.
        raise NotImplementedError

    def verify_range(self, start: int, end: int) -> bool:
        """Verify a sub-range [start, end) of the hash chain.

        Checks that entries within the range form a valid chain. The first
        entry in the range is checked against its stored previous_hash
        (which could be the genesis hash if start == 0).

        Args:
            start: Start index (inclusive).
            end: End index (exclusive).

        Returns:
            True if the sub-chain is valid, False otherwise.
        """
        # TODO: Verify hashes for entries in [start, end).
        raise NotImplementedError

    def get_proof(self, index: int) -> Optional[InclusionProof]:
        """Generate an inclusion proof for the entry at the given index.

        The proof contains the entry and all subsequent entries up to and
        including the current head, allowing independent verification.

        Args:
            index: The index of the entry to prove.

        Returns:
            An InclusionProof, or None if the index is out of range.
        """
        # TODO: Build an InclusionProof from entries[index:].
        raise NotImplementedError

    def verify_proof(self, proof: InclusionProof) -> bool:
        """Verify that an inclusion proof is valid.

        Recomputes the hash chain for the proof's entries and checks
        that each link is consistent.

        Args:
            proof: The InclusionProof to verify.

        Returns:
            True if the proof is valid, False otherwise.
        """
        # TODO: Walk the chain_to_head list and verify hashes.
        raise NotImplementedError

    def export_json(self) -> str:
        """Serialise the entire log to a JSON string.

        Each entry is stored as a dict with keys: index, timestamp,
        event_data, previous_hash, entry_hash.

        Returns:
            A JSON string representing the log.
        """
        # TODO: Convert entries to list of dicts and serialize with json.dumps.
        raise NotImplementedError

    @classmethod
    def from_json(cls, data: str) -> "AuditLog":
        """Deserialise an AuditLog from a JSON string.

        Args:
            data: The JSON string produced by export_json.

        Returns:
            A new AuditLog instance with the entries restored.
        """
        # TODO: Parse JSON, reconstruct LogEntry objects, and return a new AuditLog.
        raise NotImplementedError
