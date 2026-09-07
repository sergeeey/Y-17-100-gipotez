# claim.md — 20260907-chernoff-neuralode-nd-eigenvector-conditioning

**Graph node:** `H-B2-1l` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard
**Parent:** `H-B2-1k`'s own pearl_registry entry (impact 7) — a unifying hypothesis linking TWO
independently-observed, previously-unexplained findings: `H-B2-1i`'s seed-ensemble right-skew of
`M1` (impact score noted there) and `H-B2-1k`'s own N-dependent non-monotonicity of `M1`. Both
were speculatively attributed to "eigenvalue clustering of the perturbed matrix" without a test.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Tests whether a specific, theoretically-motivated quantity
(eigenvector matrix conditioning) correlates with `M1` across two ALREADY-COLLECTED datasets —
no new stochastic draws, no intervention, no causal claim.

## Why This Experiment, Specifically — A Better-Grounded Mechanism Than the Original Pearl Wording

The original pearl hypothesis (both `H-B2-1i` and `H-B2-1k` entries) proposed "eigenvalue
clustering" informally. This experiment sharpens it to a specific, classically-motivated
quantity: for a diagonalizable matrix `A = V Λ V⁻¹`, the transient-growth bound
`‖exp(tA)‖ ≤ κ(V)·max_i exp(t·Re(λ_i))` holds, where `κ(V) = ‖V‖·‖V⁻¹‖` is the eigenvector
matrix's condition number (standard non-normal-matrix theory — e.g. Trefethen & Embree,
*Spectra and Pseudospectra*). `κ(V)` blows up precisely when eigenvectors become nearly
parallel — which typically (not always) happens when eigenvalues cluster. This is a MORE
specific, falsifiable mechanism than raw "eigenvalue gap," directly tied to `M1`'s own defining
quantity (`M1` is itself a measure of `‖exp(tA)‖`'s transient excess over the dominant
exponential rate).

## Reused Data — No New Draws

- **Population 1 (seed-ensemble):** the 30 matrices already built by `H-B2-1i`'s own
  `build_matrix_with_seed(seed)` for `seed ∈ {0..29}` at fixed `N_DIM=8`, `coupling_magnitude=15`.
  `M1` values are already computed and committed in `H-B2-1i`'s own `metrics/run.json`.
- **Population 2 (N-sweep):** the 9 matrices already built by `H-B2-1k`'s own
  `build_matrix(n_dim)` for `n_dim ∈ {3,4,8,12,16,24,32,40,50}` at fixed `coupling_magnitude=15`,
  `seed=0`. `M1` values are already committed in `H-B2-1k`'s own `metrics/run.json`.

This experiment adds ONLY the eigenvector-conditioning computation (`np.linalg.eig`,
`np.linalg.cond`) on top of these already-built, already-validated matrices — reusing both prior
experiments' `build_matrix*` functions unchanged (Minimal Relaxation Rule).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `κ(V)` (eigenvector matrix condition number, 2-norm) for each matrix `A` already built in `H-B2-1i`'s seed-ensemble and `H-B2-1k`'s N-sweep |
| **Falsifiable predicate** | `κ(V)` is POSITIVELY correlated with the already-measured `M1` — in BOTH populations independently (same direction, even though each has a small sample: n=30 and n=9 respectively) |
| **Measurable outcome** | Spearman rank correlation between `κ(V)` and `M1` in each population, reported separately (never pooled — the two populations vary different things: seed vs. N_DIM) |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md`: no prior `H-B2-1*` experiment has computed eigenvector
conditioning at all — every prior experiment reported `M1`/`M2`/order/efficiency, never `κ(V)`.
Confirmed genuinely untested; this is the first attempt to mechanistically explain WHY `M1`
varies the way it does across seed or dimension, rather than just observing that it does.

## Kill Criterion (set BEFORE running)

- **CONFIRMED:** Spearman rho between `κ(V)` and `M1` is POSITIVE in BOTH populations
  (seed-ensemble AND N-sweep) — consistent, cross-population support for the eigenvector-
  conditioning mechanism.
- **REJECTED:** Spearman rho is negative or negligible (|rho| < 0.2) in either population — the
  proposed mechanism does not explain the observed `M1` variation, at least not as the dominant
  driver.
- **MIXED:** positive in one population but not the other — would suggest the mechanism is
  real but not the ONLY driver, or population-specific (e.g. seed variation and dimension
  variation could stress different aspects of conditioning).

## What This Does NOT Mean

1. Does NOT establish CAUSATION (that ill-conditioned eigenvectors CAUSE large `M1`) — both are
   properties of the SAME matrix `A`, and a correlation here (even if strong) reflects a shared
   dependence on the random coupling draw, not a manipulable causal pathway. This is a
   descriptive, mechanistic-association claim, not a causal one, per EstimandOps L0.
2. Does NOT explain 100% of `M1`'s variation even if CONFIRMED — `κ(V)` is A mechanism, not
   necessarily THE only one; the classical bound is an inequality, not an exact equality, so
   `M1` and `κ(V)` need not move in lockstep even under the correct mechanism.
3. With n=9 (N-sweep) and n=30 (seed-ensemble), statistical power is limited — a CONFIRMED
   verdict here is suggestive, not a strong statistical claim; reported alongside sample sizes.

## MCID

Sign and rough magnitude of the Spearman correlation between `κ(V)` and `M1` in each population —
reported as exact numbers, not a binary pass/fail threshold beyond the sign check above.
