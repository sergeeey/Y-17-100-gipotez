# controls.md — 20260906-riemann-rstat-gue

All numbers from `metrics/controls.json` and `metrics/run.json`, seed 0, 2026-09-06. `[VERIFIED]` = read from file.

## Positive Control

**Input:** 500 synthetic GUE matrices, N = 400, complex Hermitian `(A + A†)/2`, central 50 % of eigenvalues
(bulk) → ≈ 10⁵ ratios, comparable to the data.
**Expected output:** ⟨r⟩ within 0.01 of the GUE surmise 0.602658.
**Command:** `python run.py controls --seed 0`
**Result:** [x] PASS — ⟨r⟩ = 0.60060 ± 0.00073 `[VERIFIED-SYNTHETIC]`.
Note: this is 2.8 SE *below* the 3×3 surmise and matches the large-N numeric ≈ 0.5996–0.6006 quoted from
memory in claim.md → that `[MEMORY]` value is now `[VERIFIED-SYNTHETIC]`.

## Discriminating Control (GOE, β = 1)

**Input:** 500 GOE matrices, same protocol.
**Expected:** ⟨r⟩ separated from GUE by more than the tolerance (otherwise the metric cannot tell β=1 from β=2
and `Q-GOE-vs-GUE` would be unanswerable with it).
**Result:** [x] PASS — ⟨r⟩ = 0.53102 ± 0.00081; separation 0.070 = 7 × tolerance `[VERIFIED-SYNTHETIC]`.
Also confirms the `[MEMORY]` large-N GOE value 0.5307.

## Negative Control

**Input:** 100,000 Poisson levels (i.i.d. exponential spacings) — level repulsion removed.
**Expected (rejection):** kill criterion fires: |⟨r⟩ − 0.602658| ≥ 0.01.
**Result:** [x] PASS — ⟨r⟩ = 0.38666 (analytic 0.386294); `kill_criterion_fired: true` `[VERIFIED-SYNTHETIC]`.
The criterion **can fail**. Not validation theater.

## Floor–Ceiling (Step 4a) — resolved before Step 6

| | value | source |
|---|---|---|
| floor (mechanism removed) | 0.386294 | Poisson, analytic |
| ceiling (privileged answer) | 0.602658 surmise / **0.60060 empirical** | Atas 2013 / positive control |
| pass band | [0.59266, 0.61266] | |
| CRITERION_VALID | yes — floor outside band | |
| TASK_FEASIBLE | yes — empirical ceiling inside band | |
| headroom | 0.216 = 21.6 × MCID | |

## No-Collapse Tests (from `run.json`)

| Test | What changes | Result | Notes |
|---|---|---|---|
| Data swap | first 50k vs last 50k zeros | [x] PASS | 0.61188 vs 0.60995 — both in band; **monotone decrease with height** (see result_summary) |
| Noise injection | σ = 10 % of mean spacing on each zero | [x] PASS | 0.59023 > 0.5 (pre-registered); repulsion smeared, signal survives |
| Scale variation | ×0.1 and ×10 | [x] PASS | identical to 2e-14 — exact invariance as theory requires |
| Convention flip | local unfolding, window 501 | [x] PASS | Δ = 1.2e-6 — r is density-independent (A2 holds) |
| Negative control | Poisson | [x] PASS | see above |
| Adversarial input | spacings shuffled (P(s) kept, correlations destroyed) | REPORTED | ζ shuffled 0.6432 vs GUE shuffled 0.6346 — **P(s) of low zeros differs from GUE P(s)** by ≈ 0.009 in ⟨r⟩; consistent with the height trend |
| Alternative tool | pure-Python loop | [x] PASS | 0.6109167772757004 — bit-identical |

Full-Ladder minimum (all 7) met; 6 gated PASS + 1 reported-by-design.

## Notes

- Pre-registered PASS threshold for noise (⟨r⟩ > 0.5) was met with margin 0.09; a tighter threshold was
  not pre-registered, so none is claimed post hoc.
- The shuffled-spacing comparison was deliberately ungated in claim.md; it turned out to carry signal
  (see result_summary § Unexpected Observations). Post-hoc it must stay "reported", not "passed".
