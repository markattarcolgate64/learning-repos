# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Connection Pool Implementation
==============================

This module implements a simple database connection pool that manages a fixed
number of connections. Clients acquire connections from the pool, use them,
and then release them back for reuse.

The pool has a maximum size. If all connections are in use, `acquire()` raises
a `PoolExhaustedError`. When a connection is released, it should be returned
to the available pool so other clients can use it.

SYMPTOMS:
    Tests are failing because the pool becomes exhausted after several
    acquire/release cycles, even though connections are being released
    properly. After enough cycles, `acquire()` raises `PoolExhaustedError`
    when it shouldn't --- there should always be connections available if
    previous ones were released.
"""

import threading
import unittest


class PoolExhaustedError(Exception):
    """Raised when no connections are available in the pool."""
    pass


class Connection:
    """Represents a database connection."""

    _counter = 0
    _lock = threading.Lock()

    def __init__(self):
        with Connection._lock:
            Connection._counter += 1
            self.id = Connection._counter
        self.in_use = False

    def execute(self, query: str) -> str:
        if not self.in_use:
            raise RuntimeError("Cannot execute on a connection that is not acquired.")
        return f"Result of '{query}' on connection {self.id}"

    def __repr__(self):
        status = "in_use" if self.in_use else "available"
        return f"<Connection id={self.id} {status}>"


class ConnectionPool:
    """
    A thread-safe connection pool with a fixed maximum number of connections.

    Usage:
        pool = ConnectionPool(max_size=5)
        conn = pool.acquire()
        result = conn.execute("SELECT * FROM users")
        pool.release(conn)
    """

    def __init__(self, max_size: int = 5):
        self._max_size = max_size
        self._lock = threading.Lock()
        self._available: list[Connection] = []
        self._in_use: set[int] = set()

        # Pre-create all connections
        for _ in range(max_size):
            self._available.append(Connection())

    def acquire(self) -> Connection:
        """
        Acquire a connection from the pool.

        Returns:
            A Connection object ready for use.

        Raises:
            PoolExhaustedError: If no connections are available.
        """
        with self._lock:
            if not self._available:
                raise PoolExhaustedError(
                    f"All {self._max_size} connections are in use."
                )

            conn = self._available.pop()
            conn.in_use = True
            self._in_use.add(conn.id)
            return conn

    def release(self, conn: Connection) -> None:
        """
        Release a connection back to the pool.

        Args:
            conn: The connection to release.

        Raises:
            ValueError: If the connection does not belong to this pool.
        """
        with self._lock:
            if conn.id not in self._in_use:
                raise ValueError(
                    f"Connection {conn.id} is not managed by this pool or was already released."
                )

            conn.in_use = False
            self._in_use.discard(conn.id)
            # Return connection to the available pool
            self._available.append(Connection())

    @property
    def available_count(self) -> int:
        with self._lock:
            return len(self._available)

    @property
    def in_use_count(self) -> int:
        with self._lock:
            return len(self._in_use)


# ---------------------------------------------------------------------------
# Test Suite
# ---------------------------------------------------------------------------

class TestConnectionPool(unittest.TestCase):
    """Tests for ConnectionPool. These tests FAIL due to the bug."""

    def test_acquire_returns_connection(self):
        pool = ConnectionPool(max_size=3)
        conn = pool.acquire()
        self.assertIsInstance(conn, Connection)
        self.assertTrue(conn.in_use)

    def test_release_makes_connection_available(self):
        pool = ConnectionPool(max_size=3)
        conn = pool.acquire()
        pool.release(conn)
        self.assertEqual(pool.available_count, 3)
        self.assertEqual(pool.in_use_count, 0)

    def test_acquire_release_cycle_does_not_exhaust_pool(self):
        """Acquiring and releasing the same connection many times should never exhaust the pool."""
        pool = ConnectionPool(max_size=2)

        for i in range(100):
            conn = pool.acquire()
            result = conn.execute(f"SELECT {i}")
            self.assertIn(str(i), result)
            pool.release(conn)

        # Pool should still be fully available
        self.assertEqual(pool.available_count, 2)

    def test_pool_exhaustion(self):
        pool = ConnectionPool(max_size=2)
        conn1 = pool.acquire()
        conn2 = pool.acquire()

        with self.assertRaises(PoolExhaustedError):
            pool.acquire()

        pool.release(conn1)
        # Now we should be able to acquire again
        conn3 = pool.acquire()
        self.assertIsInstance(conn3, Connection)

    def test_execute_on_acquired_connection(self):
        pool = ConnectionPool(max_size=1)
        conn = pool.acquire()
        result = conn.execute("SELECT 1")
        self.assertIn("SELECT 1", result)
        pool.release(conn)

    def test_release_same_connection_twice_raises(self):
        pool = ConnectionPool(max_size=2)
        conn = pool.acquire()
        pool.release(conn)

        with self.assertRaises(ValueError):
            pool.release(conn)

    def test_connection_identity_preserved_across_cycles(self):
        """The same connection objects should be reused, not new ones created."""
        pool = ConnectionPool(max_size=1)

        conn1 = pool.acquire()
        original_id = conn1.id
        pool.release(conn1)

        conn2 = pool.acquire()
        self.assertEqual(conn2.id, original_id,
                         "Pool should reuse the same connection object, not create a new one.")


if __name__ == "__main__":
    unittest.main()
