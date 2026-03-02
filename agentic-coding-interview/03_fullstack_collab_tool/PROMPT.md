# Real-Time Collaborative Code Snippets

| Category | Difficulty | Time |
|----------|-----------|------|
| Full Stack | ★★★★ | ~60 min |

## The Prompt

> Build a web app where users can create code snippets, get a shareable link, and collaboratively edit in real-time with syntax highlighting. Think a minimal Pastebin meets Google Docs.

---

<details>
<summary>Evaluation Criteria (for interviewers)</summary>

### What They're Really Testing

- Full-stack architecture decisions (WebSockets vs SSE vs polling)
- State synchronization strategy
- Conflict resolution approach (OT vs CRDT vs last-write-wins)
- Frontend polish
- Backend persistence design

### Strong Signals

- Considers conflict resolution
- Syntax highlighting works for multiple languages
- Shareable links work end-to-end
- Handles disconnection/reconnection gracefully
- Has basic error handling

### Red Flags

- No real-time sync (just polling)
- No conflict handling at all
- Broken when multiple users edit simultaneously
- No persistence (data lost on refresh)

### Suggested Tools

- **Web search** for CRDT/OT libraries, WebSocket frameworks
- **npm/pip** for package management
- **Browser automation** to test multi-user scenarios
- **Git** for checkpointing progress

</details>
