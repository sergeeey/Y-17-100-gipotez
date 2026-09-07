# claim.md — 20260907-chernoff-neuralode-nd-numerical-abscissa

**Graph node:** `H-B2-1n` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (reuses existing,
already-verified pipeline pieces byte-identically; one new scalar descriptor added)
**Parent:** `H-B2-1m` (kappa(V) WEAKENED, power follow-up: strong, individually-significant
relationship with M1 at `N_DIM` in {3,4,8,12} — all rho>=0.88; undetectable at `N_DIM` in
{16,24,32,40,50} even at 40 seeds/slice, point estimates moved TOWARD zero with more data, not
toward significance. Primary open question shifted from statistical to mechanistic: what
explains transient growth once kappa(V) stops being sufficient?)

## Why This Experiment, Specifically

`H-B2-1m`'s own decision.md named the concrete next step explicitly (not a vague "investigate
more"): a targeted test of a specific alternative descriptor at the large-`N_DIM` values where
kappa(V) failed, not another broad N-sweep. This experiment tests the **numerical abscissa**
`omega(A) = lambda_max((A + A^T)/2)` — the largest eigenvalue of the symmetric part of `A` — a
classical, cheap-to-compute descriptor of transient growth from the SAME theoretical family as
kappa(V) (non-normal matrix theory), but structurally different: it does not go through
eigenvectors or their conditioning at all, so it cannot inherit whatever makes kappa(V)
specifically fail at large `N_DIM`.

**Why this specific alternative, not pseudospectral abscissa or another option named in
`H-B2-1m`'s Relaxation Map:** cost and a clean theoretical anchor. The numerical abscissa is a
single eigenvalue computation on a symmetric matrix (cheap, numerically stable — unlike
`cond(V)` on a non-normal matrix's possibly near-defective eigenvector matrix, a numerical-
stability concern the FL Step 8a skeptic pass on `H-B2-1m` raised and left unresolved). It has a
direct, proven bound via the Bendixson/Lumer-Phillips inequality:
`d/dt ||x(t)||^2 = x^T(A+A^T)x <= 2*omega(A)*||x||^2`, giving `||exp(tA)|| <= exp(t*omega(A))` for
the INITIAL growth rate — a different, complementary bound to the Trefethen-Embree inequality
kappa(V) is built on (which bounds the asymptotic/eigenvalue-driven regime). Pseudospectral
abscissa is the more complete descriptor in the literature but requires computing an
epsilon-pseudospectrum (expensive, especially at N_DIM up to 50) — deferred unless this cheaper
test is uninformative.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE** (same as the whole H-B2-1* arc — a correlational claim about a
measured mathematical quantity, no causal intervention framing).

## FL Step 0a — Mechanism Claim Gate

**Checked for a triggering sentence:** the underlying inequality
(`d/dt||x||^2 <= 2*omega(A)*||x||^2`) is a PROVEN mathematical fact (Bendixson's theorem /
Lumer-Phillips, standard operator theory), not an assumed behavioral claim about how a specific
implementation behaves — the same status as the Trefethen-Embree inequality underlying kappa(V),
which also did not trigger Step 0a in `H-B2-1l`/`H-B2-1m`. No synthetic counter-example check
required; this is analogous to accepting a cited theorem, not an unverified "X targets Y"
sentence about a specific test/statistic's empirical behavior.

**One thing that IS checked here, cheaply, before relying on it:** does `omega(A)` even VARY
meaningfully across the seeds in this population, or is it near-constant (which would make any
correlation test with M1 uninformative by construction, the same class of concern Step 0a
targets)? Checked directly in `run.py` before the correlation is computed — reported alongside
the correlation, not assumed.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(omega(A), M1)` pairs on the SAME matrices `H-B2-1m`'s power follow-up already built — `N_DIM` in {16,24,32,40,50}, 40 seeds each (200 total pairs), via `build_matrix_with_seed_and_n` UNCHANGED (Minimal Relaxation Rule: identical population, only a new descriptor computed on it) |
| **Falsifiable predicate** | `omega(A)` correlates with M1 (Spearman) at large `N_DIM` where kappa(V) did not — specifically, majority of the 5 slices individually significant at alpha=0.05, matching the bar `H-B2-1m` itself used |
| **Measurable outcome** | Per-`N_DIM`-slice Spearman rho/p (same per-slice discipline as `H-B2-1m`, never pooled across `N_DIM` without the same confound check that FL Step 0a already established applies to this population) |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md` / `null_results/INDEX.md` / all `H-B2-1*` graph nodes: no
prior test of numerical abscissa or any non-kappa(V) descriptor in this project. `H-B2-1m`'s own
decision.md names this exact direction as untested. Confirmed novel.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (alternative descriptor works where kappa(V) failed):** majority of the 5 large-N
  slices individually significant at alpha=0.05, with rho of consistent sign.
- **WEAKENED (partial):** some but not majority of slices significant, or inconsistent sign.
- **REJECTED (does not explain the large-N gap either):** no slice individually significant —
  leaves transient growth at large `N_DIM` unexplained by either kappa(V) or omega(A); a genuine,
  informative null about this specific pair of candidate descriptors, not evidence that NO
  descriptor could work (pseudospectral abscissa and other options remain untested).

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1m`'s own verdict (WEAKENED stands regardless of this
   result — this tests a DIFFERENT descriptor, not a re-test of kappa(V)).
2. A REJECTED verdict here does NOT mean transient growth at large N is inherently unexplainable
   — only that these two specific, cheap descriptors (kappa(V), omega(A)) do not capture it;
   pseudospectral abscissa and other options remain open.
3. Does NOT establish causality — both `omega(A)` and M1 are functions of the same random
   coupling matrix; this tests explanatory/correlational power, not a causal mechanism.
4. Even a CONFIRMED verdict would only show `omega(A)` correlates at `N_DIM>=16` — this
   experiment does not test whether it ALSO holds at small `N_DIM` (where kappa(V) already works
   well; not the open question here).

## MCID

Whether a majority of the 5 large-`N_DIM` slices show `omega(A)` individually significant
(alpha=0.05) with consistent-sign correlation to M1 — reported as an exact count, matching the
bar this project's own `H-B2-1m` set for kappa(V) at the same population.
