# Coding Interview Prep

Practice problems for systems-oriented AI company interviews. Each problem is a
self-contained Python exercise with unittest-based test verification.

Solve each problem by hand — implement the TODO stubs, run the tests, iterate
until all green. Only check `solutions/` after completing or when truly stuck.

## Prerequisites

- Python 3.8+
- numpy (only needed for ML problems 06-09)

```bash
pip install numpy
```

## Running Tests

```bash
# Run tests for a specific problem
cd coding-interview-prep
python -m unittest 01_token_bucket_rate_limiter.test_exercise -v

# Run all tests
python -m unittest discover -s . -p "test_exercise.py" -v

# Convenience script
python run_all_tests.py
```

## Problems

### Distributed Systems

| # | Problem | Difficulty | Key Concepts |
|---|---------|------------|-------------|
| 01 | Token Bucket Rate Limiter | \* | Rate limiting, time-based refill |
| 02 | Bloom Filter | \*\* | Probabilistic data structures, hashing |
| 03 | LRU Cache | \*\* | Hash maps, doubly linked lists, O(1) ops |
| 04 | Vector Clock | \*\* | Causal ordering, distributed events |
| 05 | Merkle Tree | \*\*\* | Hash trees, data integrity, diff detection |

### ML Engineering

| # | Problem | Difficulty | Key Concepts |
|---|---------|------------|-------------|
| 06 | KNN Classifier | \* | Distance metrics, numpy vectorization |
| 07 | Mini-Batch Gradient Descent | \*\* | Optimization, batching, convergence |
| 08 | TF-IDF Vectorizer | \*\* | Text processing, term weighting |
| 09 | Embedding Similarity Search | \*\*\* | Cosine similarity, LSH, approximate NN |

### Full-Stack / Systems

| # | Problem | Difficulty | Key Concepts |
|---|---------|------------|-------------|
| 10 | Priority Job Queue | \*\* | Priority queues, job lifecycle, retries |
| 11 | Pub/Sub Message Broker | \*\* | Event-driven architecture, topic patterns |
| 12 | Middleware Pipeline | \*\* | Chain of responsibility, request/response |

## How to Use

1. Open `exercise.py` in the problem directory
2. Read the docstring for context, real-world motivation, and hints
3. Implement the TODO stubs (replace `pass` with your code)
4. Run tests: `python -m unittest XX_name.test_exercise -v`
5. Iterate until all tests pass
6. Check `solutions/` only after completing or when truly stuck

## Difficulty Ratings

- \* Easy — warm-up, ~20 minutes
- \*\* Medium — core interview level, ~30-45 minutes
- \*\*\* Hard — senior-level, ~45-60 minutes

## Structure

```
coding-interview-prep/
├── README.md
├── run_all_tests.py
├── 01_token_bucket_rate_limiter/
│   ├── __init__.py
│   ├── exercise.py          # Your implementation goes here
│   └── test_exercise.py     # Tests to verify correctness
├── ...
└── solutions/               # Reference implementations (no peeking!)
```
