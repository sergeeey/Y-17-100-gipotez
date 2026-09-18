# controls.md — H-CAT7-1 (GD-ANYTIME-FINITE-v1)

> Status after execution, 2026-09-18. Original pre-registered text preserved in the
> italicised rationales; results filled in below each control.

---

## Substrate Gate (FL Step 2a) — run before any control, verdict **READY**

`metrics/substrate_check.json`. Four checks, none involving the hypothesis:

| check | result | verdict |
|---|---|---|
| exact PEP vs closed form `R_N = 1/(4Nh+2)`, `h ≤ 1`, 12 cases | max rel. error **9.3e-9** | PASS |
| PEPit 0.5.1 independent implementation, 5 schedules (incl. silver, ZLDC) | max rel. diff **3.5e-5** | PASS |
| analytic envelope-theorem gradient vs central FD, `eps` over 3 decades | best **1.5e-6 … 3.2e-5**, falling as `eps` grows → FD-noise-limited | PASS |
| schedule algebra `1ᵀs̄_i = ρ^i−1`, `\|s̄_i\| = 2^i−1`, ZLDC prefix-monotone, all-positive | exact to machine precision | PASS |

All decision-relevant values are accurate to ≥5 significant digits — four orders of
magnitude below the 5% decision margin. The verdict is not solver-tolerance-limited.

---

## Positive Control
_Known-good input: reproduce the ALREADY-PUBLISHED per-horizon result (Das Gupta et al., cited in Tsai et al. arXiv:2607.02053 p.5) — if the PEP solver setup cannot reproduce `R_n≈O(n^{-1.178})` for per-horizon-optimized (NOT prefix-constrained) schedules at `n≤50`, the harness itself is untrustworthy before any prefix-consistency claim is tested._

**Input:** Solve the unconstrained (no prefix requirement) `R_n`-minimizing PEP for individual `n`.

**Expected output:** Fitted decay rate close to `O(n^{-1.178})` (order-of-magnitude match, not exact — this is a literature-reported empirical rate, not an exact theorem constant).

**Command:**
```
python pep_unconstrained_baseline.py        # pre-registered horizons {10,20,30,40,50}
```

**Result: [x] PASS** — in a *reconstructed* form, with the deviation stated.

Per-horizon-optimal `R_n` at `n ∈ {4,5,7,8,11,12,15,16,19}` (from `ceiling.py` /
`recheck_ceiling.py`) fits a power law with exponent

* **−1.1183 ± 0.0155** (r² = 0.99866) against `N` gradient steps,
* **−1.2528 ± 0.0225** (r² = 0.99775) against `N+1` iterates,

and the literature's empirical `−1.178` lies between the two index conventions. The
harness therefore finds near-optimal per-horizon schedules, which is what this control
exists to establish.

**Deviation recorded honestly:** the pre-registered run at `n ∈ {10,…,50}` costs ~13 s
per exact PEP solve at `n=50` and did not complete inside the session; the fit above is
over `n = 4…19` instead. It is order-of-magnitude evidence about the harness, and it is
*not* a reproduction of Das Gupta et al.'s number at their horizon range. See
`decision.md` § "What this does NOT mean" item 5.

---

## Negative Control — THE ADVERSARIAL PREFIX CHECK (the single most important control this claim has)
_This is the control this whole redesign exists to add. A schedule that is secretly per-horizon-tuned (the trap named in claim.md's Source Trace) MUST be caught and rejected here._

**Input:** Per-horizon-optimal (NOT prefix-constrained) schedules; compare their first `k` entries across horizons.

**Expected output (rejection):** The per-horizon-optimal schedules for different `n` MUST NOT share a common prefix. If they DID, the per-horizon result IS secretly already an anytime schedule — a genuinely surprising finding, to be flagged, not silently treated as a null result.

**Command:**
```
python check_prefix_consistency.py
```

**Result: [x] PASS (prefixes differ, confirming per-horizon ≠ anytime, as expected)**

`metrics/prefix_consistency_check.json`, two probes that share no arithmetic:

* **Probe A (numeric):** pairwise max relative differences over the first `k = min(10,n)`
  entries at `n ∈ {6,10,14,18}` range from **1.9% to 235%**. No pair coincides.
* **Probe B (functional):** truncating the `n=18` optimum to length `n` gives `R_n`
  **0.9%–15% worse** than that horizon's own optimum. Not equivalent.

No escalation required. The prefix constraint is therefore testing something the
published per-horizon result does not already contain.

---

## Pre-registered PASS margin for the main claim (fills the MCID from claim.md)

PASS requires the found prefix-consistent schedule's `R_n` to beat the benchmark by
**at least a factor of 1.05** (ratio ≤ 0.952381) at EVERY tested `n` in both `N_train`
and `N_test` — not just on average.

**Result: FAIL.** Worst train ratio 0.9720, worst test ratio 3.1420; one horizon of
twelve (`n=4`, ratio 0.9470) meets the bar.

**Defect in this MCID, recorded:** the 5% margin was set without a feasibility check
against the achievable headroom. At `n=19` the unconstrained per-horizon optimum
(8 diverse cold starts) is only **3.4%** better than the benchmark, so the bar is
unreachable there by *any* schedule and the FAIL at that horizon is uninformative about
prefix-consistency. `decision.md` § Relaxation Map V1 replaces it with a ceiling-relative
margin.

---

## No-Collapse Tests

All six cases return the same verdict, **FAIL**, and the mechanism is the same in every
one (`metrics/no_collapse_tests.json`, `metrics/noise_injection_fixed.json`).

| Test | What changes | Result | Notes |
|---|---|---|---|
| Data swap | horizon split `N_train={3,7,13,17,21}`, `N_test={4,9,14,19,23}` | **[x] FAIL (verdict stable)** | worst train **0.9969**, worst test **1.1890**. Trained on the *intermediate* horizons, the optimiser **shrinks** the schedule (mass ×0.976) instead of inflating it, gains almost nothing, and correspondingly does not blow up on test — the mechanism predicts exactly this |
| Noise injection | randomised optimiser start points, 3 seeds | **[x] FAIL (verdict stable)** | corrected run, `metrics/noise_injection_fixed.json`: seed 101 → worst train 0.9972 / test 2.5275; seed 202 → 1.0301 / 4.4755; seed 303 → 1.0066 / 4.1299. Verdicts identical, **results genuinely distinct** (`distinct_results: true`), so the stability means something. From purely random starts the optimiser cannot even beat the benchmark on the training horizons — the multi-start from ZLDC/silver was doing the work. See the void-test note below |
| Scale variation (small) | 2 training horizons `{6,16}` | **[x] FAIL (verdict stable)** | worst train 0.9659, worst test **1.5449** |
| Scale variation (large) | 11 training horizons `{4,6,…,24}` | **[x] FAIL (verdict stable)** | worst train **0.9860**, worst test **3.8165**. The blow-ups land at `n=9,13,17,21` — precisely the iterates immediately after ZLDC's four long steps (indices 9/13/17/21) |
| Convention flip | `G_n` (squared gradient norm) instead of `R_n` | **[x] FAIL (verdict stable)** | worst train and test both **1.0000**: the optimiser returned **ZLDC itself** (identical to 1e-5). Independent confirmation of the local-optimality finding on a *different objective* |

**Monotone trend across training-set size** — an unplanned but clean result. The best
achievable worst-train ratio degrades toward 1.0 as more horizons must be served at once:

| training horizons | 2 | 6 | 11 | 23 (dense) |
|---|---|---|---|---|
| worst train ratio | 0.9659 | 0.9714 | 0.9860 | **1.0000** |

i.e. the more of the anytime requirement you actually impose, the less improvement over
the benchmark survives — reaching exactly zero when every horizon is required.

**A void test, found and corrected rather than reported.** The two pre-registered
"noise injection" cases returned bit-identical numbers (worst train 0.9714, worst test
3.4498 in both). Cause: `no_collapse_tests.py` builds five candidate starts and truncates
with `[:n_starts]`; when the budget was cut to `n_starts = 2`, the truncation removed
exactly the two randomised starts, leaving `[zldc, silver_prefix]`, which do not depend
on the seed. The two "different seeds" were the same computation, and their agreement was
a tautology — a test that cannot vary is not a test. `noise_injection_fix.py` re-runs it
with **randomised starts only** and three seeds; that run supersedes the two void cases.
| Negative control | adversarial prefix check above | **[x] PASS** | prefixes differ, two independent probes |
| Adversarial input | THE prefix-consistency check above | **[x] PASS** | elevated to its own top-level control |
| Alternative tool | independent implementation | **[x] PASS** | PEPit 0.5.1 agrees to **3.5e-5** on 5 schedules in the Substrate Gate, and re-derives the main test's FAIL verdict from its own numbers with **zero flips** (`metrics/verify_main_numbers.json`) |

_Full-Ladder: all 7 required — this is a Full-Ladder experiment (research/AI-generated hypothesis, per CLAUDE.md dispatcher)._

**Note on the "Alternative tool" row:** it was pre-registered as a contingency ("if
PEPit cannot express the prefix constraint, re-implement via `cvxpy`"). What actually
happened is the reverse and stronger — the `cvxpy` PEP was written first as the primary
evaluator, and PEPit served throughout as the *independent* cross-implementation, on
both the substrate checks and every number in the final verdict.

---

## Additional controls added during execution (not pre-registered)

| control | why it was added | result |
|---|---|---|
| **Benchmark reconstruction check** (`verify_benchmark_reconstruction.py`) | the reconstructed ZLDC schedule is the single load-bearing external object; matching the prose is not verification | primitivity potential saturated at **exactly 0.500000** for silver orders 1–5 and every ZLDC concatenation of length 2…40; endpoint rate and Lemma 7 hold everywhere checked; **negative controls rejected** (constant `h=3` → 3.96e6; silver-3 with one step altered → 441.8) |
| **Ceiling** (`ceiling.py`) | Floor–Ceiling discipline: a FAIL is uninterpretable without an arm allowed to cheat in the way the hypothesis forbids | per-horizon headroom over ZLDC is only **3.4%–14.1%** across `n=4…19` |
| **Ceiling re-check** (`recheck_ceiling.py`) | the warm-started ceiling sequence came out non-monotone, and one value decided an argument | at `n=15` the ceiling moved **0.9490 → 0.9198** (the warm-start chain was stuck); at `n=19` it survived, **0.9748 → 0.9673** |
| **Local optimality probe** (`local_optimality_probe.py`) | the dense run returned `1.0000000` at every horizon — a suspiciously clean number that must be distinguished from an optimiser stall | **42 probes, none below 1.0**; ZLDC confirmed a local minimax optimum, with a sharp asymmetry (+0.5% uniform scaling costs 69%, −0.5% costs 0.5%) |
| **`c`-sweep** (`c_sweep.py`) | a structural direction the numerical probes cannot reach: the construction's own free parameter | 13 values of `c`; some give **2× gains at individual horizons**, none improves the worst horizon; best worst-ratio **1.0**, attained by the paper's own `c = log₂ρ` |
| **Regression tests** (`test_pep_invariants.py`) | lock in the invariants the verdict rests on | **18/18 pass** |

---

## Notes

The A1 fallback described in the original pre-registration (silver stepsize schedule,
non-anytime `O(n^{-1.271})`) was **not** needed. Reference [14] of arXiv:2607.02053 was
traced to Zhang, Lee, Du & Chen, *Anytime Acceleration of Gradient Descent*, COLT 2025
(arXiv:2411.17668), whose construction is fully explicit and was reconstructed exactly
and verified against its own theorems. **No "COMPARISON WEAKENED" downgrade applies** —
the comparator is the genuine anytime `O(n^{-1.119})` schedule.
