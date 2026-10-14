---
name: y17-scientific-output-honest-assessment
description: "Y-17 project's calibrated verdict on its own scientific output (2026-09-10) — no big open problem solved, but real model-level results, negative/boundary results, and process improvements. Read before claiming the project \"found\" or \"discovered\" anything."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d8443cd-ffe1-43e0-bdb5-efd0ebc5eada
  modified: 2026-09-10T16:30:51.271Z
---

Confirmed by the user on 2026-09-10, following an independent context-asymmetric project audit
(`Agent(analyst)`, isolated context) and ADR-121/ADR-122. This is the calibrated, categorized
answer to "what did the Y-17 lab actually produce," distinct from — and more precise than —
ADR-121's own framing ("several well-verified results, no externally-confirmed new discovery
yet"). Link: [[y17-lab-repo-and-variant-c]].

**The verdict, verbatim, user-approved:**

> Из 100+ исходных задач каталога проект не решил ни одной крупной открытой проблемы. Но получил
> несколько точных модельных результатов, ряд отрицательных и граничных результатов, и сильно
> улучшил сам исследовательский процесс.

By category:

| Category | Present? |
|---|---|
| Solved a major open problem | **No** |
| Found a new general mathematical theorem-level result | **Not externally confirmed yet** |
| Obtained exact results inside specific models | **Yes** |
| Obtained new negative/boundary results | **Yes** |
| Found and fixed real bugs / false CONFIRMED verdicts | **Yes, many** |
| Found an externally-new scientific discovery | **No convincing confirmation yet** |

**Per-bridge summary of the positive output:**
- **Bridge 7** (Kauffman/Remy 2015 Boolean model): the strongest result cluster — minimal
  observation delay, fixed-point preservation conditions, schedule fragility (k*=5), exact
  escape probabilities (absorbing Markov chain), a genuine graph automorphism between
  branch_1/branch_2, mechanism via CyclinE1. After the B7 novelty audit (ADR-119), honestly
  reclassified as a **"strong model-level result cluster,"** not a "discovery" — the techniques
  are established, the application to this specific model is correct and deep.
- **Bridge 2** (Chernoff/Kreiss): correct boundary/null results — K_ref predictor transfer is
  limited (H-B2-3, REJECT); part of an earlier effect was a single-seed/wrong-surrogate artifact
  for a Kreiss-related quantity (H-B2-1k, CRITERION_INVALID).
- **Bridge 3** (May1972/TDA lakes): 0 confirmed / mostly killed / 1 parked out of ~17
  sub-hypotheses, but useful negative results — H-B3-1q/1r's per-season robustness check killed
  the "genuine intensifying signal" interpretation (the numbers themselves stayed correct);
  H-B3-2 (PH₀ chirality-excess, Baryshnikov 2022) did not survive as a practical detector.
- **CAT37 (Forsythe conjecture)**: after fixing a numerical instability, correctly found no
  counterexamples in the tested regime (0/171); 5 days later an external preprint
  (arXiv:2609.04659) fully resolved it (FALSE for s>=4) — does not contradict, explains why
  random search could never find the delicate construction required.
- **CAT31 (Lovász theta)**: an honest null on the prime/composite-tail hypothesis (H-CAT31-2).

**How to apply this:** when summarizing the project's achievements (to the user, in a report, in
any future session), do NOT say "the project discovered X" for anything in the B7/B2/B3/CAT
clusters — say "the project obtained an exact/model-level result about X, methods established,
application correct." Reserve "discovery" language for something that clears the 4 ADR-121 resume
conditions (new independent model / new dataset / new theorem-or-literature-gap / external open
problem with structural foothold) AND survives external verification — neither has happened yet
as of 2026-09-10. See [[y17-lab-repo-and-variant-c]] for repo/publishing context, and the
project's own `.claude/memory/decisions.md` ADR-121/ADR-122 for the mechanism (stop-rule +
evidence_mode/verification_strength schema) that keeps this distinction machine-checkable going
forward.
