---
name: resume-stalled-agent-with-sendmessage
description: "When a spawned Agent() hits its turn limit before finishing, resume it with SendMessage(to: agentId) — never a fresh Agent() call with the same prompt"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1d8443cd-ffe1-43e0-bdb5-efd0ebc5eada
  modified: 2026-09-08T18:04:47.341Z
---

When a background subagent (Agent tool) stops because it hit its turn limit (not an
error) with a `partial result`/`stopped at its N-turn limit` note in the task
notification, the correct recovery is `SendMessage({to: <agentId>, message: "..."})` to
resume that exact session with its accumulated context intact.

**Why:** `Agent()` always spawns a brand-new, memory-less session — even when the prompt
says "continue exactly where you left off." A fresh agent has no access to the first
agent's partial findings, tool calls already made, or reasoning so far. Calling `Agent()`
again is not a continuation, it is a second, fully independent attempt that duplicates
work and wastes the first agent's tokens entirely.

**How to apply:** On a `<task-notification>` whose summary contains "stopped at its
N-turn limit" or similar (as opposed to "completed"), always reach for `SendMessage`
first. Only fall back to a fresh `Agent()` call if the task itself has changed enough
that resuming the old context would be actively wrong (rare).

**Incident:** In the Y-17 100 gipotez project (2026-09-08, H-B2-1z experiment), a
mandatory reviewer agent hit its 12-turn limit with only a partial finding ("all 8 tests
pass... let me check ruff..."). Instead of `SendMessage(to: <that agentId>, ...)`, a new
`Agent(reviewer, ...)` call was made by mistake — this spawned a second, fully
independent reviewer with zero memory of the first one's progress. The second one *also*
hit its 12-turn limit before producing a report, having re-done the same initial steps
from scratch. Net effect: two reviewer runs, ~280k combined subagent tokens, zero
delivered verdict — recovered only by the primary session doing the final verification
itself (a hand-derived closed-form check plus a second independent numerical method).

**Honest mitigation, not a violation of [[skeptic-pass-caught-degenerate-sample]]:** per that
memory's own rule ("don't let agent caps silently substitute for FL Step 8a... that should be
flagged, not silently absorbed"), the self-review substitution here WAS flagged explicitly
(`BLOCKED` row in `tooling-eval/LEDGER.md`, an explicit "reviewer did not reach a verdict" note
in `decision.md` and the ADR, no claim of reviewer approval) — the failure mode this memory is
about is purely mechanical (wasted tokens from a wrong resume method), not a repeat of the
silent-substitution failure that memory already covers.

**Update (same session, H-B2-2 experiment): confirmed `SendMessage` is NOT actually available
as a callable tool in this environment** — `ToolSearch({query: "select:SendMessage", ...})`
returned no match, despite the `Agent` tool's own description and `ListAgents`' description both
referencing it as the correct resume mechanism. So the "correct recovery" this memory describes
is, in THIS environment, not achievable at all — not a mistake to avoid, a capability gap to
work around. Revised guidance: **first try `ToolSearch("select:SendMessage")` (or check the
active tool list) to confirm the tool actually exists in the current session before assuming it
does.** If unavailable, do NOT spawn a second `Agent()` with the same prompt either (confirmed
wasteful per the original incident below) — instead do the review directly: re-derive the
agent's likely checks yourself (math validity, edge cases, cross-checking decision.md's numbers
against metrics/run.json) and document the self-review explicitly in decision.md's FL Step 8a
section, same discipline as if the reviewer had run. By the third occurrence in one session
(H-B2-1z twice, H-B2-2 once, even with a narrowly-scoped 4-file review), this stopped looking
like bad luck and started looking like this environment's reviewer-agent turn budget being
generally too tight for this project's task sizes — worth a quick `/doctor`-style check or a
user question about raising the turn limit, rather than retrying the same call a fourth time.

**Resolution found (same session, H-B2-2, on user request to actually wait for a real
verdict instead of accepting self-review as final):** the real fix was neither a resume
mechanism nor giving up — it was **shrinking the review's scope**. Three broad reviews
("review this experiment" / "review these 4 files") all hit the 12-turn limit. A FOURTH
attempt, scoped to exactly two concrete checks (verify one specific mathematical claim by
re-deriving it; run these two specific commands and report their output) completed
successfully on the first try, reaching a real `VERDICT: LGTM` and independently
re-deriving the same proof the self-review had already produced. **Lesson: when a reviewer
agent times out, the fix is usually not a different resume strategy — it's asking it to
verify fewer, more specific things per call.** A broad "review this" invites the agent to
re-read everything from scratch each time; a narrow "check exactly this claim and run
exactly these commands" gives it a task it can actually finish within its turn budget.

Related: [[y17-lab-repo-and-variant-c]] for the project this incident happened in;
[[skeptic-pass-caught-degenerate-sample]] for the adjacent (but distinct) lesson about not
silently substituting self-review for an actual agent pass.
