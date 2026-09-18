# result_summary.md — H-CAT7-1 (GD-ANYTIME-FINITE-v1)

## 1. Substrate Gate (FL Step 2a) — READY

`metrics/substrate_check.json`. Four checks, none involving the hypothesis:

| check | result |
|---|---|
| exact PEP vs closed form `R_N = 1/(4Nh+2)` for constant `h ≤ 1`, 12 cases | max relative error **9.3e-9** |
| independent implementation (PEPit 0.5.1, its own SDP canonicalisation), 5 schedules incl. silver and ZLDC | max relative difference **3.5e-5** |
| analytic envelope-theorem gradient vs central finite differences, `eps` swept over 3 decades | best agreement **1.5e-6 … 3.2e-5**; discrepancy falls as `eps` grows, i.e. FD-noise-limited, not gradient-error-limited |
| schedule algebra: `1ᵀs̄_i = ρ^i − 1`, `\|s̄_i\| = 2^i − 1`, ZLDC prefix-monotone and strictly positive | exact to machine precision; prefix-monotone `True` |

All decision-relevant quantities are therefore accurate to ≥5 significant digits, four
orders of magnitude below the 5% decision margin. The verdict is not
solver-tolerance-limited.

## 2. Benchmark reconstruction (A1) — VERIFIED against the paper's own theorems

`metrics/benchmark_reconstruction.json`. The comparator is the genuine anytime
`O(n^{-1.119})` schedule of **Zhang, Lee, Du & Chen** (arXiv:2411.17668, COLT 2025 =
ref [14] of arXiv:2607.02053). No fallback downgrade applies.

The reconstruction is not merely transcribed from the prose — it is checked against
three *consequences* the paper proves, each computed by a route that shares no
arithmetic with the reconstruction:

* **Primitivity (their Definition 2)**, evaluated as a PEP with a different objective:
  `A_k(f_k−f*) + C_k‖g_k‖² + ½‖x_k−x*‖² ≤ ½‖x_1−x*‖²`. For silver orders 1–5 and for
  every ZLDC partial concatenation of length 2…40, the worst case is **exactly
  0.500000** — the defining inequality is saturated, as the construction intends.
* **Negative control on the same test**: constant `h=3` gives `3.96e6`, and silver-3
  with only its last step changed to 9.0 gives `441.8`. The test is not one that
  accepts everything.
* **Endpoint rate** `R_n ≤ 1/A_n` and **Lemma 7** `A_{t+1} ≥ t^{(c+log₂ρ)/(c+1)}/36`
  hold at every checked point; `2log₂ρ/(1+log₂ρ) = 1.1195452`, reproducing the quoted
  `1.119`.

Recorded discrepancy in the source: eq. (15) prints `M_i = Σ_{j=1}^{i} k_i`; the
subscript is a typo for `k_j`, and `k_j` is used.

## 3. A2 — the blocker's premise was wrong, and that is the finding

`claim.md` A2 asked whether PEPit can carry a hard prefix constraint across several
simultaneously optimised horizons. It cannot — and neither can any PEP tool, because
the request is not well posed. Making `η_k` a variable inside the PEP multiplies an
unknown stepsize by an unknown gradient; the interpolation constraints become bilinear
and the program stops being a relaxation of the worst case. Whatever such a program
returned would not be a worst case.

Resolved by architecture instead: **PEP as an exact inner evaluator on fixed numeric
stepsizes, outer non-convex search on top**, with prefix-consistency enforced
structurally — one `master` array, horizon `n` scored on `master[:n]`, no per-horizon
schedule object anywhere. The Das Gupta per-horizon trap is unreachable by
construction rather than by convention.

## 4. Structural finding — the optimiser stays inside ZLDC's family and inflates it

**CORRECTED 2026-09-19.** An earlier version of this section described the schedule as
"ZLDC scaled up by 1–7.5%, mass +3.4%". Those numbers came from the **reduced-budget
`quick_probe` schedule**, not from the main run's master — two different schedules were
conflated. Re-measured directly against `metrics/prefix_search.json`:

| quantity | corrected value |
|---|---|
| entrywise change vs ZLDC | **−1.41% to +9.38%** (not "+1 to +7.5%") |
| entries *below* ZLDC | **4 of 24** (the schedule is not a uniform inflation) |
| total stepsize mass | 56.88 vs 55.27 = **+2.91%** (not +3.4%) |

What survives the correction: the schedule remains inside ZLDC's structural family —
the alternating pattern and the long steps at indices 9/13/17/21 are preserved — and the
mass increase still tracks the realised gain at trained horizons (ratios 0.947–0.972),
consistent with `R_n ≲ 1/(2A_n)`. What does not survive: the characterisation as a
uniform inflation, and three of the four numbers used to state it.

**The training set coincided exactly with ZLDC's own structure, which was not by
design.** ZLDC's concatenation endpoints inside `n ≤ 24` are `{2,4,6,8,12,16,20,24}`;
the pre-registered `N_train = {4,8,12,16,20,24}` is a subset of them, and the
pre-registered `N_test = {5,7,11,15,19,23}` contains none of them. The split therefore
trained on exactly the horizons where ZLDC's guarantee is anchored and tested on the
intermediate points its construction exists to protect. This was luck, not insight —
`N_train` was chosen as multiples of 4 for cost reasons before the endpoint structure
was computed — but it makes the train/test contrast unusually sharp and it must be
reported, not quietly enjoyed.

## 5. Ceiling — and a correction to it found by re-checking

`metrics/ceiling.json`, `metrics/ceiling_recheck.json`. The ceiling is the best `R_n`
found over *all* length-`n` schedules with no cross-horizon coupling at all; any
prefix-consistent schedule is a feasible point of that problem.

`ceiling.py` walks horizons upward and warm-starts each from the previous optimum,
which correlates neighbouring results. The sequence came out non-monotone (n=16 →
0.9330, n=19 → 0.9748), so the suspicious horizons were re-optimised from scratch with
8 diverse, mutually unrelated cold starts. At `n = 15` this moved the ceiling from
**0.9490 to 0.9198** — the warm-start chain had been stuck. Warm-started ceiling values
are therefore reported as *upper bounds on the ceiling actually found*, not as the
ceiling, and the cold-start re-check supersedes them where both exist.

This matters because a ceiling above `0.95238` would mean the pre-registered 5% bar is
out of reach at that horizon for *any* schedule, making a FAIL there uninformative
about prefix-consistency. Establishing whether that is the case is exactly what the
re-check is for — and at `n = 19` it **is** the case: the re-checked ceiling is
**0.9673** (3.4% headroom), so the 5% bar is unreachable there by any schedule.

| n | 4 | 5 | 7 | 8 | 11 | 12 | 15 | 16 | 19 | 23 |
|---|---|---|---|---|---|---|---|---|---|---|
| ceiling ratio | 0.8987 | 0.9415 | 0.9447 | 0.9054 | 0.9101 | 0.8761 | **0.9198** | 0.9330 | **0.9673** | **0.8686** |
| headroom | 11.3% | 6.2% | 5.9% | 10.5% | 9.9% | 14.1% | 8.7% | 7.2% | **3.4%** | 15.1% |
| 5% bar reachable | yes | yes | yes | yes | yes | yes | yes | yes | **no** | yes |

(bold = cold-start re-check with 8 diverse starts, superseding the warm-start value)

**CORRECTED 2026-09-19.** An earlier version said the bar is "out of reach for any
schedule" at `n=19`. That overstates what these numbers can establish, and contradicts
`caveats.md` § 3, which states the point correctly. Every ceiling here is a value
*achieved* by a local multi-start search, so it is an **upper bound on the true optimal
`R_n`** — the true headroom is therefore **at least** what is tabulated, possibly more. A
better (e.g. branch-and-bound) optimum could reach 5% at `n=19`.

The defensible statement: at `n=19`, the best schedule found by 8 independent cold starts
improves on the benchmark by only 3.4%, so the 5% bar is **out of reach of this search**
there — which is enough to make a FAIL at that horizon uninformative about
prefix-consistency, but is not a statement about all schedules.

## 6. Main test (pre-registered) — FAIL

`metrics/prefix_search.json`. Ratios `R_n(candidate[:n]) / R_n(ZLDC[:n])`:

| n | 4 | 5 | 7 | 8 | 11 | 12 | 15 | 16 | 19 | 20 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| set | train | test | test | train | test | train | test | train | test | train | test | train |
| ratio | **0.9470** | 2.7945 | 2.3779 | 0.9544 | 2.3726 | 0.9604 | 1.8812 | 0.9672 | 2.0017 | 0.9694 | 3.1420 | 0.9720 |

`PASS_train = false`, `PASS_test = false`. One horizon of twelve meets the 5% bar.
On trained horizons the candidate is 3–5% better; on unseen horizons it is **1.9× to
3.1× worse**.

**Every number independently re-verified with PEPit** (`metrics/verify_main_numbers.json`):
max relative disagreement **1.5e-3** (typical 1e-5), **zero verdict flips**, and the
FAIL verdict re-derived from PEPit's numbers alone agrees with the run's own.

## 7. Strongest-case run and the local-optimality finding

Trained on **every** horizon `2..24` (`dense_train_test.py`, post-registration), the
optimiser converged to a schedule identical to ZLDC within `4.4e-7` — ratio
`1.0000000` at all 23 horizons.

**CORRECTED 2026-09-19 — this claim is weaker than first stated, and its headline number
was an artifact.** ZLDC is one of the three starting points of `dense_train_test.py`, so
"converged to ZLDC" is equally consistent with a stall at the start point. That was the
reason for probing the neighbourhood directly (`local_optimality_probe.py`, 42 probes,
no optimiser in the loop) — but the probe's own metric has a defect:

`worst_ratio` is the max over horizons `2..24`, and a perturbation that leaves entries 0
and 1 alone cannot change the `n=2` ratio, which therefore pins the metric at ≥1.0
regardless of what happens elsewhere. 12 of the 42 probes (single-coordinate at index
≥2) are subject to this floor. Verified in `metrics/local_optimality_probe.json`: the
`index=23, sign=+1` probe reports `worst_ratio = 1.0` with `argmax_n = 2` — i.e. **the
reported "minimum exactly 1.0" comes from a probe that was structurally incapable of
going below 1.0, and which may well have improved `n=24`.**

What still stands: the other 30 probes (10 uniform scalings and 16 random directions,
which do move entries 0/1, plus the 2 single-coordinate probes at index 0/1) genuinely
could have gone below 1.0 and did not, and 11 of the 12 floored probes independently
produced ratios >1 at other horizons. What does not stand: "42 probes, none improved,
minimum exactly 1.0" as evidence of an exhausted neighbourhood.

A separate line of work in this folder (**not mine** — see the provenance note in
`decision.md`) went further, deriving a first-order descent direction from the analytic
gradients and then finding that it too fails on the real objective at every step size in
both signs. On that account the local-optimality question at ZLDC is recorded as
**UNRESOLVED**, not confirmed. I have not independently reproduced that work and do not
vouch for it here; I report only that my own claim above was overstated.

The uniform-scaling slice shows why, and is the mechanism:

| λ | 0.90 | 0.95 | 0.99 | 0.995 | **1.005** | 1.01 | 1.02 | 1.05 | 1.10 |
|---|---|---|---|---|---|---|---|---|---|
| worst ratio | 1.110 | 1.052 | 1.010 | 1.005 | **1.688** | 2.829 | 7.782 | 138.8 | 10891 |
| binding n | 24 | 24 | 24 | 24 | **21** | 21 | 21 | 21 | 21 |

Shrinking degrades gently; growing by **half a percent** costs 69%. The binding horizon
switches at exactly `λ=1` from an endpoint (`n=24`) to `n=21`, the iterate immediately
after the long step at index 21 — precisely what ZLDC's construction is built to
protect.

A structural direction the numerical probes cannot reach fails too (`c_sweep.py`, the
construction's own free parameter `c` in `k_j = ⌊2·2^{cj}⌋`): 13 values, some giving
**2× gains at individual horizons** (best ratio 0.50), none improving the worst horizon;
best worst-ratio **1.0**, attained by the paper's own `c = log₂ρ`.

## 8. Positive control — PASS on the harness, explicit non-reproduction of the exponent

The pre-registered run completed. It finds schedules **8.6%** better than the benchmark
at `n=10` and **15.9%** better at `n=20` — matching the 5.9–15.1% headroom measured
independently by cold starts at `n ≤ 23`. That is what this control exists to establish,
and it passes.

Its large-`n` points, however, are not optima: `n=40` exited after **3 iterations**, and
`n=30`/`n=50` "converged" to ratios of 0.98 — far outside the 0.87–0.93 cold-start band —
via the same warm-start chain whose sticking was demonstrated at `n=15`.

| fit (pooled over every optimum obtained anywhere) | exponent |
|---|---|
| all horizons `4…50`, vs `N` | −1.1129 ± 0.0173 |
| cold-start-verified `4…23`, vs `N` | **−1.1601 ± 0.0203** |
| cold-start-verified `4…23`, vs `N+1` | −1.2873 ± 0.0218 |
| pre-registered run alone `10…50`, vs `N` | −1.0445 ± 0.0403 |

Same-convention fits span **0.116 = 2.9× the largest standard error**. The exponent here
is governed by optimiser quality per horizon, not by the mathematics, so no single value
is an estimate of the per-horizon-optimal rate. The literature's `−1.178` is compatible
with the best-optimised fit (≈0.9 σ) but is **not** reproduced. Exclusion of
`n = 30,40,50` is provenance-based (never cold-started), not residual-based.

## 9. Adversarial prefix check — PASS

Per-horizon optima do **not** share prefixes: numeric pairwise differences 1.9%–235%,
and functionally, truncating the `n=18` optimum costs 0.9%–15% versus each horizon's
own optimum. Per-horizon ≠ anytime, so the prefix constraint tests something the
published per-horizon result does not already contain.
