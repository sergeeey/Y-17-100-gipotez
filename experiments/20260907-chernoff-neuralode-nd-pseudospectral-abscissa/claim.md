# claim.md — 20260907-chernoff-neuralode-nd-pseudospectral-abscissa

**Graph node:** `H-B2-1r` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (reuses existing,
already-verified population-construction and M1-measurement code byte-identically; the
pseudospectral abscissa computation is genuinely new — first non-trivial new numerical routine
in this arc, and gets its own correctness tests before any real run)
**Parent:** `H-B2-1q` (the numerical-abscissa sub-arc closed: `kappa(V)` and `omega(A)` both have
a real explanatory ceiling for M1 between N=32 and N=40, confirmed on six N_DIM values across two
independent seed ranges. decision.md's own Relaxation Map named this exact next step: "Pseudospectral
abscissa — new candidate descriptor for M1 at N>=40 ... requires a new claim.md.")

## Why This Experiment, Specifically

`H-B2-1n`'s own claim.md already named the pseudospectral abscissa as "the more complete
descriptor in the literature" for transient growth, deferred at the time only because it is
expensive (requires a 2D grid search over the complex plane, not a single closed-form eigenvalue
computation like `kappa(V)` or `omega(A)`). Now that both cheaper descriptors have a *confirmed*
ceiling at N>=40 (not just "not yet tested"), the deferred, more expensive option is the correct
next step — not a third cheap variant of the same idea.

**Theoretical grounding (why this specific quantity, not an arbitrary third guess):** the
Kreiss Matrix Theorem is a PROVEN result (not an assumed behavior) relating the pseudospectral
abscissa to the actual transient growth bound: for any `eps > 0`,
`(alpha_eps(A) - alpha(A)) / eps <= sup_t ||exp(tA)|| <= e*n*K(A)`, where `K(A) = sup_eps
(alpha_eps(A)-alpha(A))/eps` is the Kreiss constant. Unlike `kappa(V)` (Trefethen-Embree,
eigenvector-conditioning-based) or `omega(A)` (Bendixson, initial-growth-rate-based), the
pseudospectral abscissa is sensitive to the FULL resolvent behavior across the complex plane, not
just eigenvectors or the instantaneous derivative at t=0 — the two respects in which the cheaper
descriptors could plausibly be missing something relevant to LARGE-t transient growth specifically.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE** (same as the whole H-B2-1* arc).

## FL Step 0a — Mechanism Claim Gate

**The theory is proven, the COMPUTATION is approximate — two separate concerns, both addressed:**
- The Kreiss Matrix Theorem itself is a proven bound (same status as Bendixson/Trefethen-Embree —
  no Step 0a check needed for the theorem).
- The GRID-BASED computation of `alpha_eps(A)` used here (search over a finite 2D grid in the
  complex plane for the boundary where `sigma_min(zI-A) <= eps`) is a discretized APPROXIMATION,
  not exact — this is a genuine correctness risk, addressed via two positive-control tests before
  any real run (not deferred to a skeptic pass after the fact):
  1. **Exact-formula check on a symmetric (normal) matrix:** for normal A,
     `alpha_eps(A) = alpha(A) + eps` EXACTLY (pseudospectrum is a union of eps-disks around each
     eigenvalue). The grid-based computation must match this to within grid resolution.
  2. **Sensitivity check on a strongly non-normal matrix:** a large upper-triangular test matrix
     (matching this project's own matrix family) must show `alpha_eps(A)` SUBSTANTIALLY LARGER
     than `alpha(A) + eps` — demonstrating the implementation actually captures non-normality,
     not silently falling back to the trivial normal-matrix answer.

Both tests are written and must pass BEFORE the real (expensive) run — see `tests/`.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(alpha_eps(A), M1)` pairs at `N_DIM` in {3,4,8,12,40,50} — small-N values (matching `H-B2-1m`'s original range, where `kappa(V)` worked well, as a sanity/positive-control check that the new descriptor isn't simply broken) plus the two large-N values (40,50) already confirmed null for both prior descriptors. 15 seeds per slice (matches `H-B2-1m`/`H-B2-1n`'s original scale — first pass on an expensive new computation, not the 40-60 seed scale of later confirmatory runs) |
| **Falsifiable predicate** | `alpha_eps(A)` correlates with M1 at N_DIM in {40,50}, where BOTH `kappa(V)` and `omega(A)` were confirmed null on six independent tests |
| **Measurable outcome** | Per-`N_DIM`-slice Spearman rho/p, same never-pooled discipline as every prior experiment in this arc |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md` / `null_results/INDEX.md`: pseudospectral abscissa named as
deferred in `H-B2-1n`'s claim.md, never tested. Confirmed novel — first actual execution.

## Kill Criterion (set BEFORE running)

- **CONFIRMED:** at least one of N=40/N=50 individually significant (alpha=0.05, positive sign)
  — pseudospectral abscissa explains SOME of the large-N gap that both cheaper descriptors left
  open. Small-N slices (3,4,8,12) serve as a sanity check, not part of this specific criterion —
  they were already established as explicable by `kappa(V)`; this experiment's job is the large-N
  gap specifically.
- **REJECTED:** neither N=40 nor N=50 individually significant — even the theoretically richer
  descriptor does not explain transient growth at large N with this specific matrix family; the
  gap remains genuinely open, informative about the LIMITS of resolvent-based descriptors for
  this problem, not proof no explanation exists.

## What This Does NOT Mean

1. Does NOT retroactively change any prior verdict in this arc (`H-B2-1m` through `H-B2-1q`) —
   this tests a DIFFERENT descriptor.
2. A CONFIRMED verdict does NOT establish pseudospectral abscissa as cheap or practical for
   general use — it is expensive by construction (grid search); this experiment measures whether
   it explains M1, not whether it should replace `kappa(V)`/`omega(A)` as a practical tool.
3. A REJECTED verdict does NOT prove transient growth at large N is fundamentally unexplainable
   by resolvent-based methods — only that THIS grid-based approximation, at this `eps` and this
   grid resolution, did not find a relationship. A finer grid or different `eps` remains untested.
4. Does NOT establish causality.

## MCID

Individual significance (alpha=0.05, positive sign) at N=40 or N=50, reported alongside the
small-N sanity-check slices for full transparency about whether the descriptor even works where
it's expected to.
