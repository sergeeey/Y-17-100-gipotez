# decision.md — 20260910-remy-tumorigenesis-exact-large-deviation-h30

## Verdict: **CONFIRMED** (for Hypothesis B — geometry problem persists, exactness does not rescue it)

## Result Summary (`metrics/run.json`)

| Fit | n | distinct x | r | r² |
|---|---|---|---|---|
| `log(P) ~ PNR_step` (primary, matches original report's axis) | 4 | **3** | -0.9449 | **0.8929** |
| `log(P) ~ n_transient` (alternative) | 4 | 4 | -0.8515 | 0.7251 |
| `log(P) ~ expected_steps_to_absorption` (alternative) | 4 | 4 | -0.7239 | 0.5240 |

**Original informal report's own r²: `0.8913` (Monte Carlo based). Exact-number `r²: 0.8929`.
`Δr² = +0.0016` — a change smaller than rounding noise, not a material improvement.**

- Both alternative candidate x-axes fit WORSE than PNR-step, not better.
- Of H-B7-22's own 40 originally-tested `k` values (both branches counted once via `branch_1`,
  since branch_2 is a confirmed isomorphic duplicate): **only 4 are non-trivial**
  (`k=1..4`, `SCHEDULE_FRAGILE`); **36 are trivially `P=1.0`** (`SCHEDULE_ROBUST`, `k>=5`), carrying
  zero `log(P)` information no matter how precisely they're computed.

## Mandatory checks against claim.md's own Kill Criterion

- [x] Hypothesis A (exactness materially helps): `r²>0.95` OR `distinct_x>=8` — **NOT met**
  (`r²=0.8929`, `distinct_x=3`)
- [x] Hypothesis B (geometry problem persists): `|Δr²|<0.05` AND `distinct_x<=4` AND
  `n_nontrivial<=4` — **ALL met**

## Interpretation

This directly and formally closes the user's own priority item 4 (re-assess the large-deviation
claim), deferred through H-B7-27/28/29 while the branch-isomorphism thread was held. The finding is
unambiguous: **the original weak `r²` was never a Monte Carlo sampling-noise artifact — it was
always a data-geometry limitation** (few distinct x-values, small effective sample size, driven by
the fact that the vast majority of this experimental family's own domain sits in a trivial
`P=1.0` region). Exact computation cannot manufacture new distinct x-values from a domain that
structurally doesn't have them. The user's own original verdict — "LEAD, не PROMOTE" — stands,
now on a firmer, formally re-verified footing rather than an open question.

**What would actually resolve this (named, not attempted here):** a genuinely different
release-state family — different clamp targets, not just different `k` under the SAME clamp scheme
— would be needed to generate new, independent, non-trivial `(x, log P)` pairs. This is a
meaningfully larger undertaking than this cheap reassessment cycle, correctly out of scope here.

## FL Step 8a — Independent Reviewer

Full-tier claim closing a priority item the user explicitly named — mandatory per FL Step 8a.
Context-asymmetric: reviewer given `claim.md` + `run.py` only, no reasoning chain. Scoped narrowly:
independently re-derive the primary `log(P) ~ PNR_step` regression from the SAME three already-
committed source files (`H-B7-24`, `H-B7-26`, `H-B7-28` metrics), using an independently-written
linear regression implementation (not calling this experiment's own `linreg` function), and confirm
`r²≈0.8929`, `n=4`, `n_distinct_x=3`.

**Verdict: CONFIRMED-REAL.** Reviewer wrote fully independent, hand-derived regression formulas
(no numpy/scipy, no call to this experiment's own `linreg`), reading the same three upstream
committed JSON files directly.

- Independently computed: `n=4`, `n_distinct_x=3`, `slope=-0.49244970999201804`,
  `r=-0.9449471076224893`, `r_squared=0.8929250362041085` — matches the committed value to full
  float precision (17 significant digits), not just the ~4-decimal figure quoted in `claim.md`.
- Independently confirmed source values: `PNR_step` `{5,4,4,2}` for `k=1..4`,
  `exact_escape_probability_branch_1` `{0.0689, 0.1377, 0.1852, 0.3333}`.

## Skeptic Concerns

No `[FALSIFIED]` concerns raised. Reviewer's independent from-scratch regression matched the
committed value bit-for-bit — no dismiss/accept/mitigate entries needed.

## Caveats / What This Does NOT Mean

Per claim.md's own "What This Does NOT Mean" section — unchanged and reaffirmed:

1. Does NOT mean the large-deviation/Kramers hypothesis is FALSE — only that this experimental
   family cannot supply enough data to test it rigorously.
2. Does NOT claim the alternative axes are inherently worse in general, only on this sample.
3. Does NOT retroactively invalidate H-B7-26/27/28/29's own confirmed findings.
4. Does NOT re-open the branch-isomorphism mechanism thread — this closes a separate, independent
   priority item.

## MCID

Not formally applicable in the usual estimand sense (n=4 too small) — the qualitative bar the user
themselves set (does `r²` improve enough to change "LEAD, не PROMOTE") was not cleared
(`Δr²=0.0016`).
