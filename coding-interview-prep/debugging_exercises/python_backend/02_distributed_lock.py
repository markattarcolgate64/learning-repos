# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Distributed Lock Manager
========================

This module implements a simplified distributed lock manager that uses
timestamps for TTL (time-to-live) based lock expiry. Clients can acquire
named locks with a TTL. If a lock is held by another client and has NOT
expired, acquisition attempts by other clients should fail. If the lock
HAS expired, another client should be able to take it over.

The lock manager stores:
    - lock name -> (owner, expiry_timestamp)

SYMPTOMS:
    Tests are failing because locks that should still be valid (not yet
    expired) are being stolen by other clients. Specifically, a lock
    acquired at time T with a TTL of 5 seconds is being considered expired
    at exactly time T + 5, but it should still be valid at that instant.
    The lock should only be considered expired AFTER T + 5, not at T + 5.
"""

import time
import unittest
from unittest.mock import patch


class LockAcquisitionError(Exception):
    """Raised when a lock cannot be acquired."""
    pass


class DistributedLockManager:
    """
    A simplified distributed lock manager with TTL-based expiry.

    Usage:
        manager = DistributedLockManager()
        manager.acquire("resource-1", owner="client-A", ttl=30)
        # ... do work ...
        manager.release("resource-1", owner="client-A")
    """

    def __init__(self):
        # lock_name -> (owner: str, expiry_time: float)
        self._locks: dict[str, tuple[str, float]] = {}

    def acquire(self, lock_name: str, owner: str, ttl: float = 30.0) -> bool:
        """
        Attempt to acquire a named lock.

        Args:
            lock_name: The name/key of the resource to lock.
            owner: Identifier of the client acquiring the lock.
            ttl: Time-to-live in seconds. The lock expires after this duration.

        Returns:
            True if the lock was successfully acquired.

        Raises:
            LockAcquisitionError: If the lock is held by another client
                and has not expired.
        """
        current_time = time.monotonic()

        if lock_name in self._locks:
            existing_owner, expiry_time = self._locks[lock_name]

            # If the same owner re-acquires, refresh the lock
            if existing_owner == owner:
                self._locks[lock_name] = (owner, current_time + ttl)
                return True

            # Check if the existing lock has expired
            if current_time < expiry_time:
                raise LockAcquisitionError(
                    f"Lock '{lock_name}' is held by '{existing_owner}' "
                    f"until {expiry_time:.2f} (current: {current_time:.2f})"
                )

        # Lock is either free or expired --- acquire it
        self._locks[lock_name] = (owner, current_time + ttl)
        return True

    def release(self, lock_name: str, owner: str) -> bool:
        """
        Release a lock. Only the owner can release their own lock.

        Args:
            lock_name: The name/key of the resource to unlock.
            owner: Identifier of the client releasing the lock.

        Returns:
            True if the lock was released.

        Raises:
            LockAcquisitionError: If the lock is not held or held by
                another client.
        """
        if lock_name not in self._locks:
            raise LockAcquisitionError(
                f"Lock '{lock_name}' is not currently held."
            )

        existing_owner, _ = self._locks[lock_name]
        if existing_owner != owner:
            raise LockAcquisitionError(
                f"Lock '{lock_name}' is held by '{existing_owner}', "
                f"not '{owner}'."
            )

        del self._locks[lock_name]
        return True

    def is_locked(self, lock_name: str) -> bool:
        """Check if a lock is currently held and not expired."""
        if lock_name not in self._locks:
            return False

        _, expiry_time = self._locks[lock_name]
        current_time = time.monotonic()

        if current_time < expiry_time:
            return True

        # Lock has expired, clean it up
        del self._locks[lock_name]
        return False


# ---------------------------------------------------------------------------
# Test Suite
# ---------------------------------------------------------------------------

class TestDistributedLockManager(unittest.TestCase):
    """Tests for DistributedLockManager. These tests FAIL due to the bug."""

    def test_acquire_free_lock(self):
        manager = DistributedLockManager()
        result = manager.acquire("resource-1", owner="client-A", ttl=10)
        self.assertTrue(result)

    def test_release_lock(self):
        manager = DistributedLockManager()
        manager.acquire("resource-1", owner="client-A", ttl=10)
        result = manager.release("resource-1", owner="client-A")
        self.assertTrue(result)

    def test_cannot_steal_non_expired_lock(self):
        """A lock that has NOT expired should NOT be acquirable by another client."""
        manager = DistributedLockManager()

        # Client A acquires at time 100 with TTL of 5 (expires at 105)
        with patch("time.monotonic", return_value=100.0):
            manager.acquire("resource-1", owner="client-A", ttl=5)

        # At time 105 exactly, the lock should still be valid (it expires AFTER 105)
        with patch("time.monotonic", return_value=105.0):
            with self.assertRaises(LockAcquisitionError):
                manager.acquire("resource-1", owner="client-B", ttl=5)

    def test_expired_lock_can_be_acquired(self):
        """A lock that HAS expired should be acquirable by another client."""
        manager = DistributedLockManager()

        # Client A acquires at time 100 with TTL of 5 (expires at 105)
        with patch("time.monotonic", return_value=100.0):
            manager.acquire("resource-1", owner="client-A", ttl=5)

        # At time 105.001, the lock has expired
        with patch("time.monotonic", return_value=105.001):
            result = manager.acquire("resource-1", owner="client-B", ttl=5)
            self.assertTrue(result)

    def test_owner_can_reacquire_own_lock(self):
        manager = DistributedLockManager()
        manager.acquire("resource-1", owner="client-A", ttl=5)
        # Same owner re-acquires (refresh)
        result = manager.acquire("resource-1", owner="client-A", ttl=10)
        self.assertTrue(result)

    def test_wrong_owner_cannot_release(self):
        manager = DistributedLockManager()
        manager.acquire("resource-1", owner="client-A", ttl=10)

        with self.assertRaises(LockAcquisitionError):
            manager.release("resource-1", owner="client-B")

    def test_is_locked_returns_true_for_active_lock(self):
        manager = DistributedLockManager()

        with patch("time.monotonic", return_value=100.0):
            manager.acquire("resource-1", owner="client-A", ttl=5)

        # At time 104, lock is still active
        with patch("time.monotonic", return_value=104.0):
            self.assertTrue(manager.is_locked("resource-1"))

    def test_is_locked_returns_false_for_expired_lock(self):
        manager = DistributedLockManager()

        with patch("time.monotonic", return_value=100.0):
            manager.acquire("resource-1", owner="client-A", ttl=5)

        # At time 106, lock has expired
        with patch("time.monotonic", return_value=106.0):
            self.assertFalse(manager.is_locked("resource-1"))

    def test_is_locked_boundary(self):
        """At exactly the expiry time, the lock should still be considered active."""
        manager = DistributedLockManager()

        with patch("time.monotonic", return_value=100.0):
            manager.acquire("resource-1", owner="client-A", ttl=5)

        # At exactly 105, it should still be locked
        with patch("time.monotonic", return_value=105.0):
            self.assertTrue(manager.is_locked("resource-1"))


if __name__ == "__main__":
    unittest.main()
