# controls.md — H-CAT56-1 (PCC-SUFFICIENCY-QUASIPURE-v1)

## Positive Control
_Known-good input: a case ABOVE the Eq. (15) threshold, where Theorem 3 guarantees PCC
is sufficient (hence `dim(V^⊥)≥d` must hold — Theorem 3's construction could not exist
otherwise, per Observation 2's own contrapositive). If the harness reports a
PCC-true/`dim(V^⊥)<d` instance here, the harness itself is broken — do not trust any
below-threshold result until this passes._

**Input:** Construct a quasi-pure state at `(d,s)` satisfying inequality (15) with
comfortable margin (not right at the boundary). Confirm PCC holds for this construction
(should be constructible by design, matching Theorem 3's own setup), then confirm
`dim(V^⊥)≥d` via the SVD-based rank computation (Theorem 3's own guarantee implies this
must hold — a rank DEFICIENCY here would mean either the harness's rank computation is
wrong, or the positive-control construction itself is wrong; either way, stop and
diagnose before proceeding to any below-threshold sample).

**Expected output:** PCC=true, `dim(V^⊥)≥d` (no rank deficiency), for every sampled
instance at this above-threshold `(d,s)`.

**Command:**
```
python pcc_sld_harness.py --mode positive_control   # to be written
```

**Result:** [ ] PASS [ ] FAIL — not yet run.

---

## Negative Control
_Known-bad input: a construction with NO commuting-derivative structure at all (generic
random Hermitian `L_i` with no relation to any real `ρ_Δ`'s SLDs) should FAIL PCC with
high probability — confirms the PCC check itself is not vacuously true._

**Input:** Replace the computed SLDs with independently-drawn random Hermitian matrices
of the same dimension (breaking the SLD-defining relation entirely).

**Expected output (rejection):** PCC check returns false for generic random matrices —
confirms the check is not trivially satisfied by construction.

**Command:**
```
python pcc_sld_harness.py --mode negative_control   # to be written
```

**Result:** [ ] PASS (correctly rejected) [ ] FAIL — not yet run.

---

## Pre-registered sample size (before any below-threshold run)

Per this project's own Anti-Overfitting Gate discipline: sample size is fixed BEFORE
seeing any below-threshold result, not increased post-hoc if the first batch looks
"almost" informative.

**Impossibility certificate, not construction.** The decisive per-sample test is exact
linear algebra (Observation 2: `dim(V^⊥)<d` ⟹ saturation impossible — a rank/SVD
computation on the vectorized `W_ij,ab`/`M_i,ab` operators), never a constructive
optimizer search for a saturating measurement. An optimizer's failure to construct one is
NEVER treated as evidence of impossibility anywhere in this experiment.

- **Primary search:** `N=200` randomly sampled quasi-pure states per tested `(d,s)` pair,
  at the SMALLEST feasible `(d,s)` below the Eq. 15 threshold (per the Pearl Card's own
  prediction that a counterexample, if real, is more likely at small dimension).
- **If N=200 finds zero CANDIDATE counterexamples** (PCC-true-with-margin AND
  `dim(V^⊥)<d`-with-margin): escalate to ONE additional `(d,s)` pair (still below
  threshold, next-smallest) at the same `N=200` — not an open-ended search. Stop after 2
  `(d,s)` pairs regardless of outcome. Report ONLY "no counterexample found via this
  exact test under this sampling distribution" — explicitly NOT as LEAD or any other
  evidence toward sufficiency (the rank test is one-directional; see claim.md's
  correction).
- **Candidate counterexample gate:** a sample counts as a CANDIDATE only if PCC holds
  with margin (not at the numerical tolerance boundary) AND `dim(V^⊥)<d` is confirmed
  with margin, re-checked at increased numerical precision (tighter SVD tolerance /
  different solver) to rule out a tolerance artifact at the rank-deficiency boundary.
- **Independent reconstruction required before CONFIRMED status.** Any candidate must be
  reconstructed from its own specification (state, parameters) by a SECOND computation
  path — a different basis/parametrization of the same physical quasi-pure state, or an
  independently-written SLD/rank computation — that does NOT import the first pass's
  basis, tolerances, or intermediate objects. Only after this passes is the candidate
  reported as a CONFIRMED counterexample; a candidate that fails independent
  reconstruction is discarded, not reported as a finding, and does not count toward the
  pre-registered sample.
- **Any single CONFIRMED counterexample stops the search immediately** — a confirmed
  instance is the result, no further sampling needed.

---

## No-Collapse Tests

| Test | What changes | Result | Notes |
|---|---|---|---|
| Data swap | different random seed for the sampling | [ ] PASS [ ] FAIL | not yet run |
| Noise injection | perturb the SLD linear-system solve tolerance | [ ] PASS [ ] FAIL | not yet run |
| Scale variation | different `N` (50 vs 200 vs 500) | [ ] PASS [ ] FAIL | not yet run |
| Convention flip | alternate parametrization of the unitary `U_Δ` in Eq. 16 | [ ] PASS [ ] FAIL | not yet run |
| Negative control | see above | [ ] PASS [ ] FAIL | not yet run |
| Adversarial input | quasi-pure states with near-degenerate `q_a` weights (stress the rank-`r` structure) | [ ] PASS [ ] FAIL | not yet run |
| Alternative tool | if feasible, cross-check the SLD solve via a second method (e.g. explicit eigen-decomposition-based formula vs. a generic linear-system solver) | [ ] PASS [ ] FAIL | not yet run |

_Full-Ladder: all 7 required — this is a Full-Ladder experiment (research/AI-generated
hypothesis, per CLAUDE.md dispatcher)._

## Notes

The exact numerical tolerance for "=0" in the PCC check, and the singular-value
threshold used for the `dim(V^⊥)` rank computation, must both be pre-registered
before running (not tuned after seeing results) — matches this project's own established
discipline (e.g. H-CAT31-3's own numerical-threshold corrections). Suggest starting at
machine-precision-relative tolerance (`1e-8` relative to the operator norm) and only
loosening if the positive control itself fails to pass at that tolerance, with any
loosening explicitly logged.
