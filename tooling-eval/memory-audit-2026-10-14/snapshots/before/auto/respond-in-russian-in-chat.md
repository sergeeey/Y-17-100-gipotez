---
name: respond-in-russian-in-chat
description: "User wants all chat replies in Russian, always visible in chat (not silently done in files only)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1d8443cd-ffe1-43e0-bdb5-efd0ebc5eada
  modified: 2026-09-07T07:20:21.549Z
---

User explicitly asked: "отвечай всегда на русском и пиши мне сюда в чат всегда" — always respond
in Russian, and always write updates here in chat (not just silently do work in files without a
chat-visible summary).

**Why:** stated directly, no incident behind it — a standing communication preference for this
project's sessions.

**How to apply:** in this project (Y-17 100 gipotez), write all chat-facing text in Russian —
status updates, summaries, questions, explanations. This does not override the project's own
`IDENTITY` convention of English for code/technical terms/identifiers inside files (variable
names, commit messages, code comments) — those stay English per `CLAUDE.md`'s IDENTITY section
and existing project convention (ADRs, decision.md, LAB.md are already written in Russian prose
with English code/technical terms inline — this preference matches and reinforces that existing
mixed-language pattern, it does not introduce a new one). Also: don't let long autonomous work
stretches go chat-silent — even during `/loop` cycles, surface a periodic Russian-language
summary of what happened, not just file edits.
