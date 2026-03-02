# LLM Evaluation Harness

**Category:** ML
**Difficulty:** ★★★★
**Time:** ~60 min

---

## The Prompt

Build a tool that compares outputs from two LLMs on a set of prompts. It should compute automated quality metrics — factuality, coherence, instruction-following — and produce a structured comparison report. Make it extensible for new metrics.

---

<details>
<summary>Evaluation Criteria (open after attempting)</summary>

### What They're Really Testing

- Evaluation methodology knowledge (LLM-as-judge, embedding similarity, regex/rule-based checks, reference-based metrics)
- Software design (plugin/registry architecture for metrics, clean abstractions)
- Statistical rigor (significance testing, confidence intervals, handling small sample sizes)
- Practical ML engineering (handling API failures, caching, cost awareness)

### Strong Signals

- Uses multiple complementary metric types (not just one)
- Plugin architecture makes adding new metrics trivial
- Considers inter-annotator agreement for LLM-as-judge
- Produces actionable report (not just numbers — includes examples of where models differ)
- Handles edge cases (empty outputs, refusals, very long responses)
- Includes cost/latency tracking

### Red Flags

- Single metric only (just "accuracy")
- No statistical analysis (just raw averages)
- Hardcoded to specific model APIs
- No extensibility
- Ignores edge cases
- No example outputs in the report

### Suggested Tools

- **Web search** for LLM evaluation best practices (HELM, lm-eval-harness patterns)
- **API clients** for model inference
- **pandas** for data aggregation
- **scipy** for statistical tests

</details>
