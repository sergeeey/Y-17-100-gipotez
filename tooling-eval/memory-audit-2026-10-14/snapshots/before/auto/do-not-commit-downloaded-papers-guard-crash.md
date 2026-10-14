---
name: do-not-commit-downloaded-papers-guard-crash
description: Worker folders may hold downloaded third-party papers (PDF/PNG/txt in lit/); pre_commit_guard crashes on them and they should not be committed
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9e146a80-48ac-4700-aadb-0cf8d72b4b4e
  modified: 2026-10-13T13:50:03.902Z
---

Workflow workers download papers into `experiments/<id>/lit/` (PDFs, rendered PNG pages, text dumps). Before `git add` of a worker folder, check for them and leave `lit/` out of the index.

**Why:** on 2026-10-13 `pre_commit_guard.py` crashed with `'NoneType' object has no attribute 'strip'` ("failing closed", commit denied) because `git diff --cached` output containing non-UTF-8 bytes (0xb7, 0xad from the txt dumps, PDF/PNG headers) could not be decoded by its subprocess reader. Committing copies of third-party publications is also unwanted. Found by running the hook by hand: `python ~/.claude/hooks/pre_commit_guard.py < hook_in.json` with a simulated PreToolUse JSON.

**How to apply:** after a workflow run, `git rm -r --cached experiments/<id>/lit` (files stay on disk), cite sources in decision.md instead. A commit denied by "security hook crashed" means reproduce the hook locally first, not retry. Related: [[y17-lab-repo-and-variant-c]].
