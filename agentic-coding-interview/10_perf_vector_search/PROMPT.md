# Fast Vector Search Engine

**Category:** Performance Engineering
**Difficulty:** ★★★★
**Time:** ~60 min

---

## The Prompt

Build a vector similarity search engine that can handle 1M 768-dimensional vectors. Queries should return top-10 nearest neighbors in under 50ms. You can use any algorithm or data structure, but implement the core search yourself — no FAISS or Annoy.

---

<details>
<summary>Evaluation Criteria (open after attempting)</summary>

### What They're Really Testing

- Knowledge of ANN algorithms (LSH, k-d trees, IVF, HNSW, product quantization)
- Systems-level thinking (memory layout, cache efficiency, NumPy vectorization, possible SIMD)
- Rigorous benchmarking (latency percentiles not just averages, recall@K measurement)
- Understanding of the speed/recall tradeoff

### Strong Signals

- Chooses an appropriate algorithm and explains why (e.g., IVF for simplicity, HNSW for quality)
- Considers memory layout (contiguous arrays, float32 vs float16)
- Benchmarks with proper methodology (warm-up, percentiles, multiple runs)
- Measures recall@10 against brute force ground truth
- Handles edge cases (duplicate vectors, zero vectors)
- Explains tradeoff knobs

### Red Flags

- Brute force only (doesn't meet the latency target)
- No recall measurement (fast but wrong)
- No benchmarking methodology
- Ignores memory usage
- Doesn't test at the specified scale (1M vectors)

### Suggested Tools

- **Web search** for ANN algorithm comparisons
- **NumPy** for vectorized operations
- **matplotlib** for benchmark visualizations
- **memory_profiler** for memory analysis
- **time/timeit** for latency measurement

</details>
