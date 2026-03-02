# On-Call Incident Dashboard

| Category | Difficulty | Time |
|----------|-----------|------|
| Product Engineering | ★★★ | ~45 min |

## The Prompt

> Build a dashboard that an on-call engineer would actually want to use at 3 AM. It should aggregate service health from multiple sources — logs, metrics, health endpoints — and surface what matters. CLI or web, your choice.

---

<details>
<summary>Evaluation Criteria (for interviewers)</summary>

### What They're Really Testing

- Product taste and empathy (what information matters when you're woken up at 3 AM?)
- Data aggregation from heterogeneous sources
- UX under stress (clear hierarchy, minimal noise, actionable information)
- Practical engineering (actually works with real/mock endpoints)

### Strong Signals

- Clear visual hierarchy (critical issues first)
- Highlights anomalies not raw data
- Supports drill-down from summary to detail
- Includes helpful context (recent deploys, runbook links, who's on call)
- Actually usable under time pressure
- Refreshes automatically

### Red Flags

- Dumps raw JSON/metrics with no prioritization
- Beautiful but takes 5 min to understand
- Requires complex setup during an incident
- Shows everything with equal weight
- No auto-refresh

### Suggested Tools

- **Web search** for dashboard design patterns
- **rich/textual** for CLI or **React/Vue** for web
- **Mock data generators** for simulating service health
- **Browser** to test the UI

</details>
