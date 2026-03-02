"""
Analytics processing module.

Contains the core event processing logic: validation, deduplication,
enrichment, and storage.
"""

import json
import hashlib
import time

from db import get_user, ensure_user, insert_event, get_recent_events


def _compute_event_hash(event: dict) -> str:
    """Compute a hash for deduplication."""
    # BUG: Serializes to JSON on every hash computation (expensive)
    raw = json.dumps(event, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def _deduplicate_events(events: list[dict]) -> list[dict]:
    """Remove duplicate events from a batch.

    Uses a naive O(n^2) comparison approach.
    """
    unique = []
    seen_hashes = []

    for event in events:
        h = _compute_event_hash(event)
        # O(n^2): linear scan through seen_hashes for every event
        is_dup = False
        for seen in seen_hashes:
            if seen == h:
                is_dup = True
                break
        if not is_dup:
            unique.append(event)
            seen_hashes.append(h)

    return unique


def _enrich_event(event: dict) -> dict:
    """Add user metadata to the event.

    N+1 problem: queries the database for every single event individually,
    even when the same user appears in multiple events in the batch.
    """
    user_id = event["user_id"]
    ensure_user(user_id)
    user = get_user(user_id)

    # Serialize to JSON and back to "deep copy" — wasteful
    enriched = json.loads(json.dumps(event))
    enriched["user_name"] = user["name"] if user else "unknown"
    enriched["user_plan"] = user["plan"] if user else "unknown"
    return enriched


def _validate_event(event: dict) -> bool:
    """Validate that event has required fields."""
    # Re-serializes to JSON just to check structure
    try:
        raw = json.dumps(event)
        parsed = json.loads(raw)
        return all(k in parsed for k in ("user_id", "event_type", "payload", "timestamp"))
    except (TypeError, ValueError):
        return False


def process_event_batch(events: list[dict]) -> dict:
    """Process a batch of analytics events.

    Steps:
    1. Validate each event
    2. Deduplicate the batch
    3. Enrich with user data
    4. Store each event

    Returns a summary dict.
    """
    start = time.time()

    # Step 1: Validate — re-serializes every event
    valid_events = []
    for event in events:
        if _validate_event(event):
            valid_events.append(event)

    # Step 2: Deduplicate — O(n^2) with redundant JSON serialization
    deduped = _deduplicate_events(valid_events)

    # Step 3: Enrich — N+1 DB queries (one per event, no caching)
    enriched = []
    for event in deduped:
        enriched.append(_enrich_event(event))

    # Step 4: Store — one insert per event, new connection each time
    stored_ids = []
    for event in enriched:
        row_id = insert_event(event)
        stored_ids.append(row_id)

    elapsed = time.time() - start

    return {
        "received": len(events),
        "valid": len(valid_events),
        "deduped": len(deduped),
        "stored": len(stored_ids),
        "elapsed_ms": round(elapsed * 1000, 2),
    }
