# claim.md — 20260907-chernoff-neuralode-nd-pseudospectral-crossimpl

**Graph node:** `H-B2-1s` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (verification of an
already-CONFIRMED, already-merged claim — reuses the exact population, adds an independent
third-party computation)
**Parent:** `H-B2-1r` (CONFIRMED: pseudospectral abscissa `alpha_eps(A)` explains M1 at N=40,50,
after a self-caught grid-boundary bug and an independent local-vs-global convergence check.
Skeptic `[WEAKENED]` named "no cross-implementation check against an established tool" as the
one remaining, undone limitation — "the load-bearing gap.")

## Why This Experiment, Specifically — User's Own Framing, Priority 1

Direct user instruction (2026-09-07): before pursuing any new hypothesis on top of H-B2-1r,
close the one concrete, cheap, already-named gap — an independent package computing the SAME
quantity on the SAME matrices. User's own diagram:

```
your alpha_eps(A) implementation
        v
independent package / method
        v
same matrices
        v
compare values and ranks
```

User's own kill criterion, verbatim: "if the independent implementation diverges materially
specifically at the large-N cases the main conclusion rests on, H-B2-1r is weakened or killed."

**Why `pseudopy` specifically:** the exact package named by the skeptic in `H-B2-1r`'s own
Step 8a pass ("pseudopy, EigTool"). Verified available on PyPI (`pseudopy==1.2.5`) before
committing to it — not assumed from memory. Its `NonnormalMeshgrid` class computes
`sigma_min(zI-A)` on a user-specified grid via SVD — confirmed by direct empirical test against
a symmetric matrix (where `sigma_min(zI-A) = dist(z, spectrum)` exactly): `pseudopy`'s `.Vals`
array matches this exact formula to 4 decimal places, confirming it computes the SAME quantity
`H-B2-1r`'s own `pseudospectral_abscissa()` computes, not a related-but-different one (e.g. the
resolvent norm `1/sigma_min`, which would have been silently wrong to compare against).

**Honest caveat about "independence":** `pseudopy` is unmaintained (last compatible with
pre-2.0 `shapely`; needed a one-line compatibility shim — `shapely.ops.cascaded_union ->
unary_union`, a pure rename with no behavior change, applied at the call site, not by patching
the installed package). `NonnormalMeshgrid` uses the SAME basic algorithm as `H-B2-1r`'s own
routine (grid search + per-point SVD of `zI-A`) — this is cross-IMPLEMENTATION (two independently
written codebases), not cross-ALGORITHM. Per the Independent Verification Strength Ladder
(`falsification-ladder.md`), this sits at "independently-written code" — a real, useful rung,
but it would NOT catch a bug shared by the underlying algorithmic approach itself (e.g. if grid
search itself has a fundamental blind spot no finer resolution would fix — unlikely given the
convergence already shown in `H-B2-1r`'s local-vs-global check, but not ruled out by this
experiment specifically).

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Do two independent implementations of the same well-defined
mathematical quantity (`alpha_eps(A)` at a fixed `eps`) agree on the same inputs? No causal or
predictive framing.

## FL Step 0a — Mechanism Claim Gate

No new behavioral claim about a test/statistic is introduced — this experiment checks numerical
AGREEMENT between two implementations of a mathematically well-defined quantity, not a new
mechanism-behavior sentence. `pseudopy`'s `Vals` convention was verified empirically (see above,
symmetric-matrix exact-formula check) before being trusted, following the same discipline
`H-B2-1r` itself used for its own routine.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(alpha_eps_mine, alpha_eps_pseudopy)` pairs at `N_DIM` in {40, 50} — the exact "primary large-N regime" the user specified, reusing the EXACT SAME matrices `H-B2-1r` already built (via `build_matrix_with_seed_and_n`, same seeds 0-14), 15 seeds each, 30 total pairs. M1 values reused from `H-B2-1r`'s own `metrics/run.json` — not recomputed |
| **Falsifiable predicate** | The two implementations' `alpha_eps` values agree closely (not diverge materially) at N=40 and N=50, AND both give the same correlation-with-M1 verdict (individually significant, positive sign) at both slices |
| **Measurable outcome** | Per-slice: (a) max relative difference between `alpha_eps_mine` and `alpha_eps_pseudopy`, (b) Spearman rank correlation BETWEEN the two implementations' values (do they rank matrices the same way, even if absolute values differ slightly due to grid resolution), (c) `alpha_eps_pseudopy` vs M1 Spearman correlation, compared against `H-B2-1r`'s own `alpha_eps_mine` vs M1 result |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md`: named verbatim as the remaining limitation in `H-B2-1r`'s
own decision.md Relaxation Map ("A full cross-implementation check... would close skeptic
concern #5 completely — named, not done"). Confirmed novel — first actual execution.

## Kill Criterion (set BEFORE running — the user's own framing, made precise)

- **CONFIRMED (H-B2-1r's claim strengthens):** at N=40 AND N=50, `alpha_eps_pseudopy` vs M1 is
  individually significant (alpha=0.05, positive sign) — matching `H-B2-1r`'s own verdict — AND
  the two implementations' raw values agree closely (median relative difference < 15%, no
  systematic large divergence at either large-N slice).
- **WEAKENED (H-B2-1r's claim needs scoping):** implementations broadly agree in RANK (high
  Spearman correlation between `alpha_eps_mine` and `alpha_eps_pseudopy`) and both still show
  significant M1 correlation, but with a NOTABLE, consistent value gap (systematic bias, not
  just noise) at large N — informative about grid-resolution limits, not about whether the
  underlying relationship is real.
- **KILLED/materially weakened (the user's own named outcome):** at N=40 OR N=50 specifically,
  `alpha_eps_pseudopy` vs M1 loses significance (p>=0.05) or flips sign, OR the two
  implementations' values diverge so much (low rank correlation, large systematic gap) that they
  cannot be considered measurements of the same underlying quantity at that N.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1o`'s or the `kappa(V)`/`omega(A)` sub-arc's verdicts —
   unrelated descriptors.
2. A CONFIRMED verdict here does NOT constitute a fully independent cross-ALGORITHM check (see
   honest caveat above — both implementations use grid+SVD) — it closes the cross-IMPLEMENTATION
   gap specifically, which is what was named as missing.
3. Does NOT establish causality.
4. Per the user's own stated roadmap: does NOT by itself license moving to Priority 2 (fresh
   confirmatory experiment on new seeds) — that is explicitly gated on THIS experiment passing.

## MCID

Per-slice (N=40, N=50) significance of `alpha_eps_pseudopy` vs M1 (alpha=0.05), reported
alongside the direct value-agreement and rank-agreement statistics between the two
implementations, so a reader can see both "do the numbers roughly match" and "does the
scientific conclusion survive" as separate, explicit facts.
