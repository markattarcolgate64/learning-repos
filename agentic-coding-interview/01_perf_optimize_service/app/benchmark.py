"""
Benchmark script for the analytics service.

Sends batches of events and measures throughput.

Usage:
    # Start the server first: python server.py
    python benchmark.py
"""

import json
import time
import random
import string
import urllib.request

URL = "http://localhost:5050/events"
BATCH_SIZE = 50
NUM_BATCHES = 20
NUM_USERS = 10

EVENT_TYPES = ["page_view", "click", "purchase", "signup", "logout", "search", "share"]


def random_event():
    return {
        "user_id": f"user_{random.randint(1, NUM_USERS)}",
        "event_type": random.choice(EVENT_TYPES),
        "payload": {
            "page": f"/page/{''.join(random.choices(string.ascii_lowercase, k=5))}",
            "duration_ms": random.randint(100, 5000),
            "referrer": random.choice(["google", "direct", "twitter", "email"]),
        },
        "timestamp": time.time() + random.uniform(-60, 60),
    }


def run_benchmark():
    total_events = 0
    total_time = 0.0
    errors = 0

    print(f"Benchmarking: {NUM_BATCHES} batches x {BATCH_SIZE} events = {NUM_BATCHES * BATCH_SIZE} total events")
    print(f"Target: {URL}")
    print()

    for i in range(NUM_BATCHES):
        events = [random_event() for _ in range(BATCH_SIZE)]

        # Add some duplicates (~10% of batch)
        num_dupes = BATCH_SIZE // 10
        for _ in range(num_dupes):
            events.append(random.choice(events).copy())

        body = json.dumps({"events": events}).encode()
        req = urllib.request.Request(
            URL,
            data=body,
            headers={"Content-Type": "application/json"},
        )

        start = time.time()
        try:
            resp = urllib.request.urlopen(req)
            result = json.loads(resp.read())
            elapsed = time.time() - start
            total_events += result["stored"]
            total_time += elapsed
            print(f"  Batch {i+1:3d}: {result['stored']:3d} stored in {elapsed*1000:.0f}ms")
        except Exception as e:
            errors += 1
            elapsed = time.time() - start
            total_time += elapsed
            print(f"  Batch {i+1:3d}: ERROR - {e}")

    print()
    print("=" * 50)
    print(f"Total events stored: {total_events}")
    print(f"Total time:          {total_time:.2f}s")
    print(f"Throughput:          {total_events / total_time:.0f} events/sec")
    print(f"Avg batch latency:   {(total_time / NUM_BATCHES) * 1000:.0f}ms")
    print(f"Errors:              {errors}")
    print("=" * 50)


if __name__ == "__main__":
    run_benchmark()
