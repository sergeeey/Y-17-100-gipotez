---
name: post-commit-memory-self-log-loop-fixed
description: "post_commit_memory.py hook infinite self-referencing commit loop, fixed 2026-09-07"
metadata: 
  node_type: memory
  type: project
  originSessionId: bb2e03dc-81df-4637-8de0-217306b9e06a
  modified: 2026-09-08T08:38:14.216Z
---

`~/.claude/hooks/post_commit_memory.py` (global, applies to every project) appends a
log entry to `activeContext.md`/`history/commits-*.md` on every `git commit`. It never
commits itself — but the write leaves the file dirty, and committing that dirty file as
`chore: auto-log commit history entry` is itself a `git commit`, re-triggering the hook.
Observed live in Y-17-100-gipotez: 6+ chained commits (`d05b5bf`..`2b7f922` on `main`),
manually cut off.

**Fix (2026-09-07):** added `_is_self_log_commit()` in `post_commit_memory.py` — a
case-insensitive prefix match on `"chore: auto-log commit history entry"` — checked
right after `commit_msg` is read in `main()`, before any writes. A commit whose own
message matches this pattern is skipped entirely (no archive write, no active-log
write, no nudge). Real work commits are unaffected. 9 new unit/integration tests in
`~/.claude/hooks/tests/test_post_commit_memory.py`, all passing; ruff clean; verified
live by piping a synthetic self-log-style commit event into the hook and confirming
zero writes/output.

**Update (2026-09-08):** the fix was found MISSING from the working copy of
`post_commit_memory.py` again (0 matches for `_is_self_log_commit`, despite this note
claiming it was written and tested on 2026-09-07) — the `.pyc` cache in
`~/.claude/hooks/__pycache__/` still had bytecode referencing the function, proving it
existed on disk at some point and was later lost/overwritten before ever being
committed. Re-implemented from this note's own spec + the still-present test file
(`~/.claude/hooks/tests/test_post_commit_memory.py`, itself untracked/uncommitted until
now) and **committed** in the hooks repo (`C:\Users\serge\.claude\hooks`) as commit
`2dca838`, 2026-09-08. 256/256 hooks tests pass, ruff clean.

**Why this matters going forward:** the fix lives in the global hooks repo
(`C:\Users\serge\.claude\hooks`), a separate git repo from any project. It is now
**committed** (`2dca838`) — no longer pending go-ahead. If a future session sees this
same infinite-commit-chain symptom in ANY project, check first whether `2dca838` (or a
later commit) is present in the hooks repo's `git log` before re-diagnosing from
scratch — and if the working copy has once again lost the function despite the commit
existing, that itself is a new, separate incident worth investigating (something is
overwriting `post_commit_memory.py` outside of normal edits).

**How to apply:** if a session hits a chain of `chore: auto-log commit history entry`
commits again, first check `grep _is_self_log_commit ~/.claude/hooks/post_commit_memory.py`
— if it's missing despite `2dca838` being in the hooks repo's history, something reverted
or overwrote the file after that commit; re-apply the same fix (see `2dca838`'s diff) and
investigate the overwrite mechanism rather than silently re-authoring it from scratch.
