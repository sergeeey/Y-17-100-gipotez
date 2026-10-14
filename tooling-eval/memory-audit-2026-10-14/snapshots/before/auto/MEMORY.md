# Memory index — Y-17 100 gipotez

- [Y-17 lab repo & variant C](y17-lab-repo-and-variant-c.md) — public repo sergeeey/Y-17-100-gipotez; pilot-before-automation chosen; GeoSpectra file stays local-only
- [Skeptic pass caught degenerate sample](skeptic-pass-caught-degenerate-sample.md) — real incident: context-asymmetric skeptic caught a flaw 8+ rounds of self-review missed; don't let agent caps silently substitute for FL Step 8a
- [7-of-7 means generator failure, not skeptic success](7-of-7-means-generator-failure-not-skeptic-success.md) — a 100% hit rate is a finding about the generator, not license to run the checker on more work
- [Respond in Russian in chat](respond-in-russian-in-chat.md) — always reply in Russian here, always surface chat-visible summaries (code/technical terms stay English)
- [post_commit_memory self-log loop fixed](post-commit-memory-self-log-loop-fixed.md) — global hook fix for infinite "chore: auto-log commit history entry" commit chain, left UNCOMMITTED in hooks repo pending user go-ahead
- [Resume stalled agent with SendMessage](resume-stalled-agent-with-sendmessage.md) — a turn-limited Agent() must be resumed via SendMessage(to: agentId), never a fresh Agent() call — that spawns an independent, memory-less duplicate
- [Y-17 scientific output — honest assessment](y17-scientific-output-honest-assessment.md) — no big open problem solved; real model-level/negative/boundary results only. Don't call B7/B2/B3/CAT results "discoveries"
- [YBE C3 audit state + orchestration](ybe-c3-audit-orchestration-state.md) — E0/E1 plan, verified facts, Claude=verifier/Cursor=executor protocol, other LLM outputs untrusted
- [Do not commit downloaded papers](do-not-commit-downloaded-papers-guard-crash.md) — worker lit/ folders crash pre_commit_guard (non-UTF-8); unstage them, cite sources instead
