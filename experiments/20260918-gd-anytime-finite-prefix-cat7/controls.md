# controls.md — H-CAT7-1 (GD-ANYTIME-FINITE-v1)

## Positive Control
_Known-good input: reproduce the ALREADY-PUBLISHED per-horizon result (Das Gupta et al., cited in Tsai et al. arXiv:2607.02053 p.5) — if the PEP solver setup cannot reproduce `R_n≈O(n^{-1.178})` for per-horizon-optimized (NOT prefix-constrained) schedules at `n≤50`, the harness itself is untrustworthy before any prefix-consistency claim is tested._

**Input:** Solve the unconstrained (no prefix requirement) `R_n`-minimizing PEP for individual `n∈{10,20,30,40,50}`.

**Expected output:** Fitted decay rate close to `O(n^{-1.178})` (order-of-magnitude match, not exact — this is a literature-reported empirical rate, not an exact theorem constant).

**Command:**
```
python pep_unconstrained_baseline.py   # to be written
```

**Result:** [ ] PASS [ ] FAIL — not yet run.

---

## Negative Control — THE ADVERSARIAL PREFIX CHECK (the single most important control this claim has)
_This is the control this whole redesign exists to add. A schedule that is secretly per-horizon-tuned (the trap named in claim.md's Source Trace) MUST be caught and rejected here._

**Input:** Take the schedule found in the Positive Control (per-horizon-optimal, NOT prefix-constrained) and DIRECTLY test it as if it were a single anytime schedule — i.e., check whether its first `k` entries (for the smallest tested `n`) match the first `k` entries used at larger `n`.

**Expected output (rejection):** The per-horizon-optimal schedules for different `n` MUST NOT share a common prefix — i.e., `η^{(n=10)}_{1..10} ≠ η^{(n=20)}_{1..10}` in general. If they DID happen to share a prefix, that would mean the per-horizon result IS secretly already an anytime schedule — a genuinely surprising finding in its own right, to be flagged, not silently treated as a null result.

**Command:**
```
python check_prefix_consistency.py   # to be written; compares first-k entries across per-horizon-optimal schedules
```

**Result:** [ ] PASS (prefixes differ, confirming per-horizon ≠ anytime, as expected) [ ] FAIL (prefixes coincide — surprising, escalate before proceeding)

---

## Pre-registered PASS margin for the main claim (fills the MCID from claim.md)

To avoid reporting PEP solver numerical noise as a finding: PASS requires the found prefix-consistent schedule's `R_n` to beat the benchmark by **at least a factor of 1.05** (5% relative improvement) at EVERY tested `n` in both `N_train` and `N_test` — not just on average. A smaller or inconsistent margin is FAIL, not a weak PASS. (5% chosen conservatively relative to typical PEP solver tolerance, ~1e-6 relative on the SDP itself — the 5% margin is about distinguishing a real structural improvement from a schedule that merely fits `N_train`'s specific horizons, not about numerical precision of the solver.)

---

## No-Collapse Tests

| Test | What changes | Result | Notes |
|---|---|---|---|
| Data swap | different `N_train`/`N_test` split (different horizon sets) | [ ] PASS [ ] FAIL | not yet run |
| Noise injection | n/a — PEP is a worst-case deterministic optimization, no natural noise-injection analog; substitute: perturb initial guess for the PEP solver, confirm convergence to same optimum | [ ] PASS [ ] FAIL | not yet run |
| Scale variation | different `N_train` SIZE (e.g. 5 vs 15 horizons) | [ ] PASS [ ] FAIL | not yet run |
| Convention flip | `G_n` (squared gradient norm) instead of `R_n` (function value) — different rate class per Tsai et al.'s own Theorem 1.2 | [ ] PASS [ ] FAIL | not yet run |
| Negative control | see Adversarial Prefix Check above | [ ] PASS [ ] FAIL | not yet run |
| Adversarial input | THE prefix-consistency check above (elevated to its own top-level control, not merely one of 7) | [ ] PASS [ ] FAIL | not yet run |
| Alternative tool | if `PEPit` cannot express the prefix constraint (A2 in claim.md), re-implement the PEP directly via `cvxpy` and cross-check | [ ] PASS [ ] FAIL | not yet run |

_Full-Ladder: all 7 required — this is a Full-Ladder experiment (research/AI-generated hypothesis, per CLAUDE.md dispatcher)._

---

## Notes

The benchmark schedule realizing `O(n^{-1.119})` (Zhang et al., ref [14] in Tsai et al. 2026) has not yet been obtained in exact form — this is Unknown A1 in claim.md and must be resolved before the Positive Control can be finalized. If the exact schedule cannot be found/reconstructed, the silver stepsize schedule (Altschuler & Parrilo, realizing the weaker `O(n^{-1.271})` NON-anytime rate) is a documented fallback comparator, with the comparison explicitly relabeled (comparing against a non-anytime rate is a different, weaker claim than comparing against the anytime `n^{-1.119}` — must not be silently substituted without updating claim.md).
