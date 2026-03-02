"""
Secure Audit Log - Solution

A tamper-evident, hash-chained audit log for verification events.
Each entry's SHA-256 hash incorporates the previous entry's hash,
forming an immutable chain similar to a simplified blockchain.
"""

import hashlib
import json
import time as _time
from dataclasses import dataclass
from typing import Optional

GENESIS_HASH = "0" * 64


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
    """Proof that a specific entry is part of a valid chain."""
    entry: LogEntry
    chain_to_head: list  # list[LogEntry] from this index to head (inclusive)


def compute_hash(previous_hash: str, index: int, timestamp: float,
                 event_data: str) -> str:
    """Compute the SHA-256 hash for a log entry."""
    return hashlib.sha256(
        f"{previous_hash}{index}{timestamp}{event_data}".encode()
    ).hexdigest()


class AuditLog:
    """A tamper-evident, hash-chained audit log."""

    def __init__(self) -> None:
        self._entries: list[LogEntry] = []

    def append(self, event_data: str, timestamp: Optional[float] = None) -> LogEntry:
        if timestamp is None:
            timestamp = _time.time()

        index = len(self._entries)
        previous_hash = (
            self._entries[-1].entry_hash if self._entries else GENESIS_HASH
        )
        entry_hash = compute_hash(previous_hash, index, timestamp, event_data)

        entry = LogEntry(
            index=index,
            timestamp=timestamp,
            event_data=event_data,
            previous_hash=previous_hash,
            entry_hash=entry_hash,
        )
        self._entries.append(entry)
        return entry

    def get(self, index: int) -> Optional[LogEntry]:
        if index < 0 or index >= len(self._entries):
            return None
        return self._entries[index]

    def head(self) -> Optional[LogEntry]:
        if not self._entries:
            return None
        return self._entries[-1]

    def __len__(self) -> int:
        return len(self._entries)

    def verify_integrity(self) -> bool:
        return self.verify_range(0, len(self._entries))

    def verify_range(self, start: int, end: int) -> bool:
        if not self._entries:
            return True
        for i in range(start, end):
            entry = self._entries[i]

            # Determine the expected previous hash
            if i == 0:
                expected_prev = GENESIS_HASH
            else:
                expected_prev = self._entries[i - 1].entry_hash

            # Check previous_hash linkage
            if entry.previous_hash != expected_prev:
                return False

            # Recompute and compare entry_hash
            recomputed = compute_hash(
                entry.previous_hash, entry.index, entry.timestamp, entry.event_data
            )
            if entry.entry_hash != recomputed:
                return False

        return True

    def get_proof(self, index: int) -> Optional[InclusionProof]:
        if index < 0 or index >= len(self._entries):
            return None
        chain = self._entries[index:]
        return InclusionProof(
            entry=self._entries[index],
            chain_to_head=list(chain),
        )

    def verify_proof(self, proof: InclusionProof) -> bool:
        chain = proof.chain_to_head
        if not chain:
            return False

        for i, entry in enumerate(chain):
            # Determine the expected previous hash for the first entry
            if i == 0:
                expected_prev = entry.previous_hash
            else:
                expected_prev = chain[i - 1].entry_hash

            # Verify previous_hash linkage (for entries after the first)
            if i > 0 and entry.previous_hash != expected_prev:
                return False

            # Verify the hash itself
            recomputed = compute_hash(
                entry.previous_hash, entry.index, entry.timestamp, entry.event_data
            )
            if entry.entry_hash != recomputed:
                return False

        return True

    def export_json(self) -> str:
        entries_data = []
        for e in self._entries:
            entries_data.append({
                "index": e.index,
                "timestamp": e.timestamp,
                "event_data": e.event_data,
                "previous_hash": e.previous_hash,
                "entry_hash": e.entry_hash,
            })
        return json.dumps(entries_data, indent=2)

    @classmethod
    def from_json(cls, data: str) -> "AuditLog":
        entries_data = json.loads(data)
        log = cls()
        for item in entries_data:
            entry = LogEntry(
                index=item["index"],
                timestamp=item["timestamp"],
                event_data=item["event_data"],
                previous_hash=item["previous_hash"],
                entry_hash=item["entry_hash"],
            )
            log._entries.append(entry)
        return log
