# Configurable API Gateway

| Category | Difficulty | Time |
|----------|-----------|------|
| Backend | ★★★★ | ~60 min |

## The Prompt

> Build an HTTP proxy that sits in front of any backend service and provides: per-client rate limiting, request/response logging, circuit breaking, and basic auth. It should be configurable via a YAML file. Make it production-ready.

---

<details>
<summary>Evaluation Criteria (for interviewers)</summary>

### What They're Really Testing

- Networking fundamentals (HTTP proxying, connection management, header forwarding)
- Reliability patterns (circuit breaker state machine, token bucket rate limiter)
- Configuration design (schema validation, sensible defaults, hot reload?)
- Operational concerns (structured logging, metrics, graceful shutdown)

### Strong Signals

- Circuit breaker with proper state machine (closed -> open -> half-open -> closed)
- Rate limiter handles bursts correctly (token bucket or sliding window)
- Clean YAML config schema with validation
- Good error responses (429 with Retry-After, 503 with reason)
- Handles backend timeouts gracefully
- Structured logging with request IDs

### Red Flags

- Circuit breaker is just a boolean flag (no half-open state)
- Rate limiter is trivially bypassable (per-request not per-client)
- Hardcoded configuration
- Crashes when backend is unreachable
- No request correlation/tracing

### Suggested Tools

- **Web search** for circuit breaker patterns, HTTP proxy libraries
- **aiohttp/httpx** for async proxying
- **pyyaml** for config parsing
- **wrk/ab** for load testing

</details>
