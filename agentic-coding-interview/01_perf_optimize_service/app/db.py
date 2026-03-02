"""
Simulated database layer.

Uses an in-memory list to simulate a database. Each "query" has realistic
latency to mimic a real DB connection.
"""

import time
import json
import random
import sqlite3

_DB_PATH = ":memory:"


def _get_connection():
    """Create a new SQLite connection every call (no pooling)."""
    conn = sqlite3.connect(_DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            event_type TEXT,
            payload TEXT,
            timestamp REAL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            plan TEXT,
            created_at REAL
        )
    """)
    return conn


def insert_event(event: dict) -> int:
    """Insert a single analytics event. Returns the row ID."""
    conn = _get_connection()
    cursor = conn.execute(
        "INSERT INTO events (user_id, event_type, payload, timestamp) VALUES (?, ?, ?, ?)",
        (event["user_id"], event["event_type"], json.dumps(event["payload"]), event["timestamp"]),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def get_user(user_id: str) -> dict | None:
    """Look up a user by ID."""
    conn = _get_connection()
    row = conn.execute("SELECT user_id, name, plan, created_at FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return {"user_id": row[0], "name": row[1], "plan": row[2], "created_at": row[3]}
    return None


def ensure_user(user_id: str):
    """Create user if not exists."""
    conn = _get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, name, plan, created_at) VALUES (?, ?, ?, ?)",
        (user_id, f"User {user_id}", random.choice(["free", "pro", "enterprise"]), time.time()),
    )
    conn.commit()
    conn.close()


def get_recent_events(user_id: str, limit: int = 100) -> list[dict]:
    """Get recent events for a user."""
    conn = _get_connection()
    rows = conn.execute(
        "SELECT id, user_id, event_type, payload, timestamp FROM events WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return [
        {"id": r[0], "user_id": r[1], "event_type": r[2], "payload": json.loads(r[3]), "timestamp": r[4]}
        for r in rows
    ]
