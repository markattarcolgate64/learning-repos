# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Session Store with Expiry
=========================

System:
    An in-memory session store for a web application. Each session is created
    with a TTL (time-to-live) in seconds. Sessions should remain valid as long
    as they are actively accessed -- each access refreshes the session's
    expiration window. A cleanup method removes all expired sessions.

Expected behavior:
    - Creating a session stores data with a TTL.
    - Accessing (getting) a session refreshes its expiration timer.
    - A session that is continuously accessed should NEVER expire.
    - A session that has NOT been accessed within its TTL should expire.
    - The cleanup method should remove only truly expired sessions.

Symptoms:
    Tests are failing because sessions that are being actively accessed are
    still expiring. A user reports that they keep getting logged out even
    though they are actively clicking around the site.
"""

import time
import hashlib
import os
import unittest
from unittest.mock import patch


class Session:
    """Represents a single session with metadata."""

    def __init__(self, session_id, data, ttl):
        self.session_id = session_id
        self.data = data
        self.ttl = ttl
        self.created_at = time.time()
        self.last_accessed = time.time()

    def is_expired(self, current_time=None):
        """Check if this session has expired."""
        now = current_time or time.time()
        # Session expires if it hasn't been accessed within the TTL window
        return now > self.created_at + self.ttl

    def touch(self):
        """Refresh the session's last-accessed timestamp."""
        self.last_accessed = time.time()


class SessionStore:
    """In-memory session store with TTL-based expiry."""

    def __init__(self, default_ttl=3600):
        self._sessions = {}
        self.default_ttl = default_ttl

    def create_session(self, data, ttl=None):
        """Create a new session and return its ID."""
        ttl = ttl if ttl is not None else self.default_ttl
        session_id = hashlib.sha256(os.urandom(32)).hexdigest()[:32]
        session = Session(session_id, data, ttl)
        self._sessions[session_id] = session
        return session_id

    def get_session(self, session_id):
        """
        Retrieve session data by ID. Returns None if not found or expired.
        Accessing a session refreshes its expiry timer.
        """
        session = self._sessions.get(session_id)
        if session is None:
            return None
        if session.is_expired():
            del self._sessions[session_id]
            return None
        session.touch()
        return session.data

    def update_session(self, session_id, data):
        """Update the data for an existing session."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        if session.is_expired():
            del self._sessions[session_id]
            return False
        session.data = data
        session.touch()
        return True

    def delete_session(self, session_id):
        """Explicitly delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def cleanup(self):
        """Remove all expired sessions from the store."""
        now = time.time()
        expired_ids = [
            sid for sid, session in self._sessions.items()
            if session.is_expired(current_time=now)
        ]
        for sid in expired_ids:
            del self._sessions[sid]
        return len(expired_ids)

    @property
    def active_count(self):
        """Return the number of sessions currently stored (including expired)."""
        return len(self._sessions)


# ---------------------------------------------------------------------------
# Tests -- these should PASS once the bug is fixed
# ---------------------------------------------------------------------------

class TestSessionStore(unittest.TestCase):

    def test_create_and_retrieve_session(self):
        """A freshly created session should be retrievable."""
        store = SessionStore(default_ttl=60)
        sid = store.create_session({"user_id": 42, "role": "admin"})
        data = store.get_session(sid)
        self.assertIsNotNone(data)
        self.assertEqual(data["user_id"], 42)

    def test_session_expires_without_access(self):
        """A session should expire if not accessed within its TTL."""
        store = SessionStore()
        sid = store.create_session({"user_id": 1}, ttl=10)

        # Simulate time passing beyond the TTL with no access
        future = time.time() + 15
        with patch("time.time", return_value=future):
            data = store.get_session(sid)
        self.assertIsNone(data)

    def test_active_session_does_not_expire(self):
        """
        A session that is actively accessed should NOT expire, even if the
        total elapsed time since creation exceeds the TTL.
        """
        store = SessionStore()
        sid = store.create_session({"user_id": 7}, ttl=10)

        # Access the session at t+6 (within TTL from creation)
        t_plus_6 = time.time() + 6
        with patch("time.time", return_value=t_plus_6):
            data = store.get_session(sid)
            self.assertIsNotNone(data, "Session should be alive at t+6")

        # Now at t+12: it's been 12s since creation, but only 6s since last
        # access. Since TTL=10, the session should still be valid.
        t_plus_12 = time.time() + 12
        with patch("time.time", return_value=t_plus_12):
            data = store.get_session(sid)
            self.assertIsNotNone(
                data,
                "Session was accessed at t+6 and TTL is 10s, so it should "
                "still be alive at t+12 (only 6s since last access)."
            )

    def test_cleanup_removes_only_expired(self):
        """Cleanup should remove expired sessions and leave active ones."""
        store = SessionStore()
        sid_short = store.create_session({"user": "short"}, ttl=5)
        sid_long = store.create_session({"user": "long"}, ttl=60)

        # Advance time past the short TTL
        future = time.time() + 10
        with patch("time.time", return_value=future):
            removed = store.cleanup()

        self.assertEqual(removed, 1)
        self.assertIsNone(store.get_session(sid_short))
        self.assertIsNotNone(store.get_session(sid_long))

    def test_cleanup_does_not_remove_actively_used(self):
        """
        A session with a short TTL that is actively accessed should survive
        cleanup even if total time since creation exceeds the TTL.
        """
        store = SessionStore()
        sid = store.create_session({"user": "active"}, ttl=10)

        # Access at t+8
        t_plus_8 = time.time() + 8
        with patch("time.time", return_value=t_plus_8):
            store.get_session(sid)

        # Cleanup at t+15: 15s since creation, but only 7s since last access.
        t_plus_15 = time.time() + 15
        with patch("time.time", return_value=t_plus_15):
            removed = store.cleanup()

        self.assertEqual(removed, 0, "Active session should not be cleaned up")
        self.assertEqual(store.active_count, 1)


if __name__ == "__main__":
    unittest.main()
