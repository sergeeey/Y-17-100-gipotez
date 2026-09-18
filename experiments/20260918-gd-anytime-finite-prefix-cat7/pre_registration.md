# Pre-registration — H-CAT7-1 main test (written BEFORE any candidate schedule was searched)

Written 2026-09-18, after the Substrate Gate passed and after measuring SDP solve
cost, but **before running any prefix-consistent search and before computing any
candidate-vs-benchmark ratio**. The horizon sets below are fixed by compute cost,
not by results — no ratio at any horizon had been computed when this was written.
The only numbers known at the time of writing were (a) substrate-check
diagnostics and (b) raw PEP timings per horizon.

## Benchmark (A1, resolved)

`R_n` of the **Zhang–Lee–Du–Chen anytime schedule** (arXiv:2411.17668, COLT 2025 —
reference [14] of Tsai/Fatkhullin/Zhang/He arXiv:2607.02053), reconstructed exactly
from its own definitions (`phi`, `concat`, silver blocks, `k_j = floor(2·2^{cj})`,
`c = log2 rho`). This is the genuine **anytime** `O(n^{-1.119})` comparator, not the
non-anytime silver (`n^{-1.271}`) or per-horizon Das Gupta (`n^{-1.178}`) fallbacks
named in `controls.md`. No fallback downgrade is in effect.

## Horizon sets (disjoint, both inside the master schedule's length)

| | value |
|---|---|
| `K` (master schedule length) | **24** |
| `N_train` | **{4, 8, 12, 16, 20, 24}** |
| `N_test` | **{5, 7, 11, 15, 19, 23}** |

`N_test ∩ N_train = ∅`. Both sets lie within `1..K`, so every tested horizon is
scored on a genuine prefix of the one master schedule — a test horizon is one the
optimiser never saw, not one whose stepsizes came from the initialisation.

Cost rationale: one exact PEP solve costs ~0.01 s at `n=10`, ~0.65 s at `n=20`,
~2.4 s at `n=30`, ~12.8 s at `n=50`. `K=24` keeps a full multi-start search inside
the session budget; `K=40+` does not.

## PASS rule (restates `controls.md`, no new freedom)

PASS iff `R_n(candidate_prefix) / R_n(ZLDC_prefix) ≤ 1/1.05 = 0.952381` at **every**
`n ∈ N_train ∪ N_test`. Anything else — including a large average improvement with
one horizon short of 5%, or a train-only margin — is FAIL.

## Positive control (`controls.md`) horizons

`n ∈ {10, 20, 30, 40, 50}`, free (non-prefix-constrained) per-horizon optimisation,
target fitted exponent near `-1.178` (order-of-magnitude, literature-reported
empirical value, not a theorem constant).

## Adversarial prefix check

First `k = 10` entries of the per-horizon optima at the five control horizons,
compared pairwise. Expected: they differ. Coincidence would be the surprising
outcome and is to be escalated, not absorbed.
