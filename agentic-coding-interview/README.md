# Agentic Coding Interview Prep

Practice exercises for interviews where you use an AI coding agent (Claude Code,
Cursor, etc.) with full tool access to complete open-ended engineering tasks.

## How This Is Different

Traditional coding interviews give you a well-defined problem and test whether
you can write the algorithm. Agentic interviews give you a **vague, realistic
engineering task** and test whether you can:

- Break an ambiguous problem into concrete steps
- Direct an AI coding agent effectively (tool selection, parallelism, delegation)
- Ship working software end-to-end, not just write functions
- Handle real-world messiness — incomplete specs, flaky data, external APIs
- Make good engineering tradeoffs under time pressure

## The Exercises

| # | Discipline | Exercise | Difficulty | Starter Code? |
|---|-----------|----------|------------|---------------|
| 01 | Perf Engineering | [Optimize a Slow Service](01_perf_optimize_service/PROMPT.md) | ★★★ | Yes |
| 02 | ML | [Fix a Broken Training Pipeline](02_ml_debug_pipeline/PROMPT.md) | ★★★★ | Yes |
| 03 | Full Stack | [Real-Time Collaborative Code Snippets](03_fullstack_collab_tool/PROMPT.md) | ★★★★ | No |
| 04 | Product Eng | [On-Call Incident Dashboard](04_product_oncall_dashboard/PROMPT.md) | ★★★ | No |
| 05 | Backend | [Durable Job Queue](05_backend_job_queue/PROMPT.md) | ★★★★ | No |
| 06 | Backend | [Configurable API Gateway](06_backend_api_gateway/PROMPT.md) | ★★★★ | No |
| 07 | Infrastructure | [Deployment Canary Analyzer](07_infra_canary_analyzer/PROMPT.md) | ★★★ | Yes (data) |
| 08 | AI Research Eng | [Multi-Head Self-Attention from Scratch](08_ai_research_attention/PROMPT.md) | ★★★★★ | No |
| 09 | ML | [LLM Evaluation Harness](09_ml_eval_harness/PROMPT.md) | ★★★★ | No |
| 10 | Perf Engineering | [Fast Vector Search Engine](10_perf_vector_search/PROMPT.md) | ★★★★ | No |

## How to Practice

1. **Open the PROMPT.md** for an exercise — read only "The Prompt" section
2. **Set a timer** for the listed time budget
3. **Work with your AI agent** to complete the task end-to-end
4. **When done**, open the collapsible evaluation criteria to self-assess
5. **Reflect** on what you'd do differently next time

## Tips for Agentic Interviews

- **Start by clarifying scope** — the prompt is intentionally vague. Deciding
  what to build (and what *not* to build) is part of the test.
- **Profile/research before coding** — jumping straight to implementation is
  a red flag. Understand the problem space first.
- **Ship something working** — a working MVP beats a perfect design doc. Get
  something running, then iterate.
- **Use the right tool for the job** — web search for research, agents for
  parallel exploration, browser for testing UIs, git for checkpoints.
- **Communicate your thinking** — narrate your approach as you go. The
  interviewer is watching your process, not just the output.
- **Benchmark and validate** — "it works" isn't enough. Show measurements,
  tests, and evidence.
