# controls.md — H-CAT56-1 (PCC-SUFFICIENCY-QUASIPURE-v1)

## Positive Control
_Known-good input: a case ABOVE the Eq. (15) threshold, where Theorem 3 guarantees PCC
is sufficient. If the harness reports a PCC-true/Theorem-1-false instance here, the
harness itself is broken — do not trust any below-threshold result until this passes._

**Input:** Construct a quasi-pure state at `(d,s)` satisfying inequality (15) with
comfortable margin (not right at the boundary). Confirm PCC holds for this construction
(should be constructible by design, matching Theorem 3's own setup), then confirm
Theorem 1's criterion ALSO holds (Theorem 3 guarantees this).

**Expected output:** PCC=true, Theorem-1-criterion=true, for every sampled instance at
this above-threshold `(d,s)`.

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

- **Primary search:** `N=200` randomly sampled quasi-pure states per tested `(d,s)` pair,
  at the SMALLEST feasible `(d,s)` below the Eq. 15 threshold (per the Pearl Card's own
  prediction that a counterexample, if real, is more likely at small dimension).
- **If N=200 finds zero counterexamples:** escalate to ONE additional `(d,s)` pair
  (still below threshold, next-smallest) at the same `N=200` — not an open-ended search.
  Stop after 2 `(d,s)` pairs regardless of outcome; report LEAD (not CONFIRMED) if both
  are clean.
- **Any single counterexample found stops the search immediately** — a found instance is
  the result, no further sampling needed to "confirm" an existence claim.

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

The exact numerical tolerance for "=0" in PCC/Theorem-1 checks must be pre-registered
before running (not tuned after seeing results) — matches this project's own established
discipline (e.g. H-CAT31-3's own numerical-threshold corrections). Suggest starting at
machine-precision-relative tolerance (`1e-8` relative to the operator norm) and only
loosening if the positive control itself fails to pass at that tolerance, with any
loosening explicitly logged.
