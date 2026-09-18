# manifest.md — H-CAT7-1 artifacts

## Blocker resolution (claim.md HD-MAVP A1 / A2)

**A1 — benchmark schedule: RESOLVED, no fallback downgrade.**
Reference [14] of Tsai/Fatkhullin/Zhang/He (arXiv:2607.02053) was traced by reading
that paper's own bibliography: **Zihan Zhang, Jason D. Lee, Simon S. Du, Yuxin Chen,
"Anytime Acceleration of Gradient Descent", Proc. 38th COLT, 2025** (arXiv:2411.17668,
open access). Its construction is fully explicit and is reimplemented exactly in
`pep_core.py`:

| element | source | implementation |
|---|---|---|
| join stepsize `φ(x,y) = [-(x+y) + √((x+y+2)² + 4(x+1)(y+1))]/2` | eq. (10), from Zhang & Jiang 2024 Thm 3.1 | `phi` |
| `concat(s,r) = [s, φ(1ᵀs, 1ᵀr), r]` | eq. (11) | `concat` |
| silver schedule `s̄_0 = []`, `s̄_i = concat(s̄_{i-1}, s̄_{i-1})` | Definition 5 (Altschuler & Parrilo) | `silver_schedule` |
| anytime schedule: repeat `s̄_j` exactly `k_j = ⌊2·2^{cj}⌋` times, `c = log₂ρ`, folded by (12) | §3.1 | `zldc_anytime_schedule` |

Verified independently of the paper's prose: `1ᵀs̄_i = ρ^i − 1` to machine precision for
`i = 1..6`, `|s̄_i| = 2^i − 1`, and `2log₂ρ/(1+log₂ρ) = 1.11955` reproduces the quoted
`1.119`. Note recorded in the code: eq. (15) prints `M_i = Σ_{j=1}^{i} k_i`; the
subscript is a typo for `k_j` and `k_j` is used.

The comparator is therefore the genuine **anytime** `O(n^{-1.119})` schedule. Neither
fallback named in `controls.md` (silver `n^{-1.271}`, non-anytime; Das Gupta
`n^{-1.178}`, non-anytime) is in use as the benchmark, so **no "COMPARISON WEAKENED"
downgrade applies**.

**A2 — prefix constraint inside the solver: RESOLVED, and the premise was wrong.**
The blocker asked whether PEPit's solver interface can carry a hard prefix constraint
across several simultaneously-optimised horizons. It cannot, and — more importantly —
*no* PEP tool can, because it would be mathematically invalid: making `η_k` a variable
inside the PEP multiplies an unknown stepsize by an unknown gradient, so the
interpolation constraints become bilinear and the SDP is no longer a relaxation of the
worst case. The number such a program returns would not be a worst case at all.

The correct architecture, used here: **PEP as an exact inner evaluator on a fixed
numeric schedule, outer non-convex search on top.** Prefix-consistency is enforced
*structurally*: `pep_prefix_search.py` holds exactly one `master` array of length `K`
and evaluates horizon `n` on `master[:n]`. No per-horizon schedule object exists in
that file, so the Das Gupta per-horizon trap is unreachable by construction, not by
convention.

`PEPit 0.5.1` was installed and *is* used — as an independent second implementation in
the Substrate Gate, which is the role it can actually play here.

## Files

| file | role |
|---|---|
| `pep_core.py` | exact PEP (cvxpy, Taylor et al. interpolation) + the three published schedules |
| `optimizer.py` | outer L-BFGS-B search; per-horizon and prefix-consistent modes; power-law fit |
| `substrate_check.py` | FL Step 2a Substrate Gate (4 checks) → `metrics/substrate_check.json` |
| `pep_unconstrained_baseline.py` | positive control, per-horizon optima → `metrics/positive_control.json` |
| `check_prefix_consistency.py` | adversarial prefix check → `metrics/prefix_consistency_check.json` |
| `ceiling.py` | per-horizon ceiling at the main test's horizons → `metrics/ceiling.json` |
| `pep_prefix_search.py` | MAIN TEST → `metrics/prefix_search.json` |
| `no_collapse_tests.py` | 4 of the 7 no-collapse tests → `metrics/no_collapse_tests.json` |
| `pre_registration.md` | horizon split + PASS rule, fixed before any ratio was computed |

Added during execution, each because a specific number needed checking rather than reporting:

| file | role |
|---|---|
| `verify_benchmark_reconstruction.py` | checks the reconstructed ZLDC schedule against the paper's own theorems (primitivity, endpoint rate, Lemma 7) with its own negative control → `metrics/benchmark_reconstruction.json` |
| `verify_main_numbers.py` | recomputes every number in the verdict with PEPit and re-derives the verdict from those numbers alone → `metrics/verify_main_numbers.json` |
| `recheck_ceiling.py` | re-optimises the suspicious (non-monotone) ceiling horizons from 8 cold starts → `metrics/ceiling_recheck.json` |
| `dense_train_test.py` | strongest-case variant: every horizon `2..24` is a training horizon → `metrics/dense_train_test.json` |
| `local_optimality_probe.py` | 42 direct probes around the benchmark, no optimiser in the loop, to tell a finding from a stall → `metrics/local_optimality_probe.json` |
| `c_sweep.py` | structural (non-perturbative) direction: the construction's own free parameter `c` → `metrics/c_sweep.json` |
| `noise_injection_fix.py` | corrected noise-injection case after the original was found void (its randomised starts had been sliced off) → `metrics/noise_injection_fixed.json` |
| `quick_probe.py` | reduced-budget preliminary read of the main test, reported separately → `metrics/quick_probe.json` |
| `test_pep_invariants.py` | 18 regression tests locking in the invariants the verdict rests on |

**Still in flight at the time of writing:** `pep_unconstrained_baseline.py` (the
pre-registered positive control at `n ∈ {10,…,50}`) had run 5+ hours without completing
— the exact PEP costs ~13 s per solve at `n=50` and grows ≈ `n^{3.5}`. It writes
`metrics/positive_control.json` only on completion. The positive control's function is
served in the meantime by a reconstructed fit over `n = 4…19`; see `controls.md` and
`decision.md`, where the deviation is recorded rather than glossed. The warm-start
`ceiling.py` run was deliberately terminated once `recheck_ceiling.py` showed its
warm-start chain could stick; its partial output is preserved as
`metrics/ceiling_warmstart_partial.log`.

## Environment

Python 3.13.2 (conda-forge), numpy 2.3.4, scipy 1.16.3, cvxpy 1.9.2, PEPit 0.5.1,
solvers CLARABEL (primary, `tol=1e-9`) with SCS fallback. All new code ruff-clean.
