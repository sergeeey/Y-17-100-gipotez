---
name: y17-lab-repo-and-variant-c
description: Y-17 lab lives in public repo sergeeey/Y-17-100-gipotez; user chose variant C (pilot through full FL stack before any automation); GeoSpectra file deliberately excluded from public repo
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d8443cd-ffe1-43e0-bdb5-efd0ebc5eada
  modified: 2026-09-06T06:19:00.004Z
---

Y-17 Cross-Domain Bridge Lab was turned into a public GitHub repo on 2026-09-06:
https://github.com/sergeeey/Y-17-100-gipotez (folder `E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez`, now a real git clone — was an extracted archive before).

User's meta-goal for this repo: an *exemplary experimental lab* — memory, hypothesis graph
and structure designed up front so a blind orchestrator can operate — AND a test bed for
the whole tool/agent/methodology stack. User picked **variant C** (AskUserQuestion,
2026-09-06): build the core (LAB.md, registry/graph.yaml, FL template, ledgers), then run
pilot H-B1-1a (Riemann zeros r-statistic, known answer r̄≈0.6027) through the FULL FL stack as
a positive control of the lab itself; only automate what actually hurt in the pilot (ADR-002).
Rejected: variant B (build the "lab OS" first) — conflicts with the project's own recorded
anti-overengineering feedback.

Privacy decision (ADR-001): `01-cross-domain-bridges/H-7 GeoSpectra Lab (…).md` is in
`.gitignore` and stays local-only — it references a third party's unsent correspondence and
a Discord transcript. README mention anonymized. User confirmed via AskUserQuestion.

**Why:** the user wants "everything digitized so an orchestrator can work blind", but the
project also carries a hard anti-overengineering lesson; C resolves the tension by making the
first experiment a known-answer positive control of the infrastructure.

**How to apply:** start every session from `LAB.md`, then `registry/graph.yaml` (status
changes go there FIRST). Every tool/agent/hook use → a row in `tooling-eval/LEDGER.md`,
summary counted by grep. Run `scripts/lab_check.py` + `pytest` before any commit. Do not
propose building `lab` CLI / CI / project hooks until the H-B1-1a pilot has produced
concrete pain points. See [[y17-project-context]] if written later.
