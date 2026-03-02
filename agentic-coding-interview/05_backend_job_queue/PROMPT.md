# Durable Job Queue

| Category | Difficulty | Time |
|----------|-----------|------|
| Backend | ★★★★ | ~60 min |

## The Prompt

> Build a job queue system that supports: priorities, retries with exponential backoff, dead letter queues, concurrent workers, and durability across restarts. Use SQLite or files for persistence — no Redis or RabbitMQ.

---

<details>
<summary>Evaluation Criteria (for interviewers)</summary>

### What They're Really Testing

- Distributed systems fundamentals (at-least-once delivery, idempotency, backpressure)
- Concurrency handling (locking strategies, race conditions under concurrent access)
- Durability guarantees (crash recovery, WAL mode)
- Clean API design that's pleasant to use

### Strong Signals

- Handles worker crashes gracefully (jobs return to queue)
- Demonstrates with a realistic workload
- Tests concurrent worker access explicitly
- Considers poison pill jobs (always fail)
- Uses SQLite WAL mode or equivalent for crash safety
- Clean separation between queue and worker

### Red Flags

- No crash recovery (jobs lost on restart)
- Race conditions when multiple workers dequeue
- Dead letter queue mentioned but not implemented
- Untested concurrent access
- No backoff (just immediate retry)

### Suggested Tools

- **Web search** for SQLite documentation, concurrency patterns
- **Threading/multiprocessing** docs
- **pytest** for testing concurrent behavior

</details>
