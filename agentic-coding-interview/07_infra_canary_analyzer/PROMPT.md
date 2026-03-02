# Deployment Canary Analyzer

## The Prompt

> After every deploy, we need to compare the canary's metrics against the
> baseline to decide: proceed, pause, or rollback. Build a tool that takes
> before/after metrics and makes that recommendation with statistical
> confidence. Here's sample data from our last 5 deploys.

**Time budget:** ~45 minutes
**Difficulty:** ★★★

Sample data is in `data/`. Each CSV has columns: `timestamp`, `latency_p50`,
`latency_p99`, `error_rate`, `cpu_percent`, `memory_mb`.

- `deploy_01_clean.csv` through `deploy_03_clean.csv` — healthy deploys
- `deploy_04_latency_regression.csv` — latency p99 increased ~3x
- `deploy_05_error_spike.csv` — error rate jumped from 0.1% to 5%

---

<details>
<summary>Evaluation Criteria (open after attempting)</summary>

### What they're really testing

- **Statistical thinking** — do you use proper hypothesis tests or just thresholds?
- **Decision-making under uncertainty** — confidence levels, not binary answers
- **Handling noisy data** — real metrics are noisy; warm-up periods, outliers
- **Communication** — can you explain the recommendation in plain English?

### Strong signals

- Uses appropriate statistical tests (Welch's t-test, Mann-Whitney U, etc.)
- Accounts for warm-up period after deploy (excludes first N minutes)
- Handles noisy data without false positives (multiple metric agreement)
- Reports confidence level, not just "rollback" / "proceed"
- Explains the recommendation in plain language an on-call engineer would understand
- Correctly identifies deploy 04 (latency) and deploy 05 (errors) as problematic
- Correctly passes deploys 01-03 as clean

### Red flags

- Simple threshold comparison (error_rate > 1% → rollback) with no statistics
- No warm-up period handling (first few minutes are always noisy)
- Binary yes/no with no confidence level or nuance
- Ignores some metrics entirely (only looks at error rate, ignores latency)
- False positive on clean deploys due to normal noise

### Suggested tools & approaches

- `pandas` for data loading and aggregation
- `scipy.stats` for hypothesis testing (ttest_ind, mannwhitneyu)
- Web search for "canary analysis statistics" or "automated canary deployment"
- `matplotlib` for visualizing metric distributions
- Consider: what if one metric regresses but others improve? How to weigh?

</details>
