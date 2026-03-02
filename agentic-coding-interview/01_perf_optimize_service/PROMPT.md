# Optimize a Slow Service

## The Prompt

> This Python service handles user analytics events. In production it processes
> ~2K events/sec but we need it at 15K. Profile it, identify the bottlenecks,
> and optimize. Don't rewrite from scratch — fix what's there.

**Time budget:** ~45 minutes
**Difficulty:** ★★★

Starter code is in `app/`. Run with:

```bash
cd app && pip install -r requirements.txt
python server.py
# In another terminal:
python benchmark.py
```

---

<details>
<summary>Evaluation Criteria (open after attempting)</summary>

### What they're really testing

- **Profiling methodology** — do you measure before you optimize?
- **Bottleneck identification** — can you distinguish algorithmic issues from I/O issues?
- **Targeted fixes** — do you fix the top bottleneck first, or shotgun changes everywhere?
- **Benchmarking discipline** — do you measure the impact of each change?
- **Systems intuition** — connection pooling, batching, caching, algorithmic complexity

### Strong signals

- Profiles the code before touching anything (cProfile, py-spy, line_profiler)
- Identifies bottlenecks in priority order and fixes the biggest one first
- Benchmarks after every change to confirm improvement
- Recognizes the N+1 query pattern, the O(n²) dedup, and the redundant serialization
- Considers connection pooling, batch writes, and caching
- Final throughput is measurably higher with numbers to prove it

### Red flags

- Rewrites the entire service from scratch
- Guesses at bottlenecks without profiling
- Makes changes but never measures improvement
- Focuses on micro-optimizations while ignoring the O(n²) loop
- Adds complexity (async, threading) before fixing algorithmic issues

### Suggested tools & approaches

- `cProfile` / `py-spy` / `line_profiler` for profiling
- `wrk` or `ab` or the provided `benchmark.py` for load testing
- Web search for Python performance patterns, connection pooling
- Git commits between each optimization for easy rollback

</details>
