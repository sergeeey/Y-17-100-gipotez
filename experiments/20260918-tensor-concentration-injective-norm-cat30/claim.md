# H-CAT30-1 — claim.md

> **ERRATUM (2026-09-18, see `decision.md`): REJECTED.** The pilot design below is
> mathematically DEGENERATE — fixing `n` while scanning `d` confines the optimization to an
> at-most-`n`-dimensional subspace regardless of `d`, so it could never have probed the open
> `p<2r` regime this claim targets. Caught by context-asymmetric skeptic review, independently
> re-verified (closed-form match to 0.48%, exact `x*∈span{a_i}` to machine precision). Read
> `decision.md` first — the claim and pre-registration below are preserved for the record, not
> because their conclusion holds.

## Origin

Catalog item #30, `00-catalog/100 Open Problems — raw catalog (source, 2026-09-06).md`
line 1321: "Sharp tensor concentration inequalities, не сводящиеся к грубой matricization".
Selected 2026-09-18 per ADR-087's scope-expansion mandate (H-CAT31-3's active search paused
after Point 95; user explicitly authorized picking a new catalog-sourced candidate
unconnected to the H-7/ChernoffPy/May1972 anchors). Selected from a background screening
agent's ranked shortlist (5-8 candidates from the ~81 unscreened catalog items) as the
top cost/leverage pick: same source family (Bandeira et al.) already successfully worked
with for H-CAT31-1..3, low friction to find the exact formulation.

**Source Trace (FL Step -4):** the raw catalog's own paraphrase ("Problem"/"Why It Is Still
Open" sections) is templated boilerplate (per this project's own skeptic-assessment of the
100-item catalog) and was NOT trusted as-is. Verified directly: `arXiv:2603.29571` ("Randomstrasse101:
Open Problems of 2025", Bandeira, Dmitriev, Lucca, Nizić-Nikolac, Rödder, submitted 2026-03-31)
is a real, currently-listed arXiv paper (confirmed via direct browser fetch of the abstract page
and the full HTML text). The exact problem is **Entry 8, "Tensor Concentration Inequalities" (by
Kevin Lucca), Conjecture 16 ("Type-2 constant of Tensors")**:

For symmetric deterministic tensors `T_1,...,T_n ∈ (R^d)^⊗r`, i.i.d. standard Gaussian
`g_1,...,g_n`, and `p≥2`:

```
E||Σ_i g_i T_i||_{I_p} ≤ Õ_{r,p}( d^{1/2-1/p} · sqrt(Σ_i ||T_i||_{I_p}^2) )
```

where `||T||_{I_p} = max_{||x||_p≤1} |⟨T,x^⊗r⟩|` is the symmetric injective `ℓ_p` norm
(`Õ` hides multiplicative constants depending on `r,p` and polylog factors in `d,n`).

**What is already proven (per the source, read directly, not via any secondhand paraphrase):**
Conjecture 16 is SETTLED for `p≥2r` (Bandeira/Guntuboyina/Jain et al. 2024, "BGJ+24" in the
source's own citation, via a Dudley entropy-integral / covering-number argument; a 2025 follow-up
by Aden-Ali removed a log factor and the `p`-dependence in that regime). It is **OPEN for `p<2r`**
— the source's own words: "a volumetric barrier prevents us from proving Equation 2 for `p<2r`,
which would consist of very interesting cases for further applications" — including, notably,
the `r=p=2` matrix case via the SAME geometric/covering-number technique (that specific corner is
separately settled by the older, different Ahlswede-Winter/noncommutative-Khintchine route, so
its status is "proven by other means, not by this conjecture's own technique" — a nuance the
source itself flags explicitly, and not conflated here).

**Novelty Check (FL Step -3):** `grep -il "tensor"` across `null_results/INDEX.md`,
`parked/INDEX.md`, `registry/graph.yaml` returns no matches — this is not a re-attempt of
anything prior in this project.

## EstimandOps L0

**Question type:** Descriptive. "For the simplest fully-open sub-case `r=3, p=2` (chosen because
`d^{1/2-1/p}=d^0=1`, i.e. the conjecture predicts a dimension-FREE rate up to polylog factors —
a sharp, clean, falsifiable-by-scaling target), using a specific constructed family of symmetric
order-3 tensors, does the Monte-Carlo-estimated `E||Σ g_i T_i||_{I_2}` grow with `d` (holding `n`
and `Σ||T_i||_{I_2}^2` fixed), or does it stay bounded — informative either way about whether this
construction is consistent with the conjecture's claimed rate in the open regime." No causal claim,
no claim about the conjecture's truth in general (a bounded numerical probe on one construction
family is evidence, not proof; see "What this does NOT mean" below).

## Zero-Signal Gate

Entity: Conjecture 16's injective-`ℓ_2`-norm bound for order-3 (`r=3`) tensor families. Falsifiable
predicate: `E-norm` scales as `d^β` with `β` significantly different from `0` (the conjectured
rate) vs. `β≈0` (consistent). Measurable outcome: weighted power-law regression on Monte-Carlo
estimates across `d ∈ {5,10,20,40,80,160}`, with a pre-registered 95% CI threshold. All three
present — proceeds.

## Construction (exact, not a Monte-Carlo approximation on the RHS)

`T_i = a_i^{⊗3}` for `a_i` unit vectors (`||a_i||_2=1`) in `R^d`, drawn i.i.d. uniformly random on
the sphere, FIXED per `d` (not resampled per Monte Carlo replicate — the conjecture's own `T_i` are
"symmetric deterministic tensors", randomness is only over `g_i`). By a direct Hölder-duality
argument (`p=2` self-dual): for `T=a^⊗r`, `⟨T,x^⊗r⟩=⟨a,x⟩^r`, so `||T||_{I_2} = max_{||x||_2≤1}
|⟨a,x⟩|^r = ||a||_2^r`. For `||a_i||_2=1`, this gives `||T_i||_{I_2}=1` EXACTLY — independently
re-verified numerically to `1.0000000000` at `d∈{5,40,160}` via the same optimization routine used
for the LHS (`verify_single_tensor_norm.py`), not merely asserted algebraically.

`Σ_i ||T_i||_{I_2}^2 = n` exactly (n=20 throughout), so the conjectured bound's RHS is
`Õ_{3,2}(sqrt(n))` — a constant independent of `d` up to polylog(d) factors.

## LHS estimation method (the actual computational core)

`E||Σ_i g_i T_i||_{I_2} = E_g[ max_{||x||_2=1} |Σ_i g_i ⟨a_i,x⟩^3| ]` is the expected symmetric
injective norm of a random order-3 tensor — computing the inner `max` exactly is NP-hard in
general (stated explicitly in the source itself). Estimated via multi-restart symmetric-tensor
power iteration (`x ← normalize(A^T(g⊙(Ax)^2))`, the standard higher-order power method for cubic
forms), 50 random restarts × 70 iterations per Monte Carlo draw, taking the best `|f(x)|` found.

**Independent cross-checks (before trusting any pilot number):**
1. Power iteration vs. an independently-implemented `scipy.optimize` search (Nelder-Mead on a
   scale-invariant reparametrization, 6 random starts) on a `d=10,n=15` test case: **exact
   agreement, 0.0000% relative gap**.
2. Restart-count robustness at the two largest tested `d` (80, 160): re-running the SAME 20
   `(A,g)` pairs from the pilot with 400 restarts × 150 iterations instead of 50×70 gives
   **0.0000% change** in every estimate — rules out the specific concern that a fixed restart
   budget would systematically under-estimate the true supremum more severely as `d` grows
   (curse-of-dimensionality search bias), which would have spuriously produced a false flat/
   decreasing trend.
3. Single-tensor normalization claim (`||T_i||_{I_2}=1`) independently verified numerically to
   10 decimal places at 3 different `d` values via the identical optimization routine, not just
   algebraically asserted.

## The claim (falsifiable, pre-registered BEFORE this pilot's numbers were seen)

Weighted power-law fit `log(E-norm) = α + β·log(d)` across `d∈{5,10,20,40,80,160}`
(`n_gaussian_draws=60` per `d`, inverse-variance weighted):

- **LEAD**: 95% CI on `β` excludes 0 AND is bounded away from `[-0.1,0.1]` (i.e., a real,
  non-negligible growth or decay rate beyond what polylog(d) factors could plausibly account
  for) — worth a deeper, adversarial-search follow-up in the style of H-CAT37-1→H-CAT37-2.
- **INFORMATIVE-NEGATIVE**: CI is consistent with `β≈0` (a flat/bounded asymptotic trend,
  distinguishing this from a small-`d` transient) — consistent with (not proof of) the
  conjecture's claimed dimension-free rate for this random construction family.

## What this does NOT mean

1. This is a RANDOM (not adversarial) construction — a bounded/flat result here is much WEAKER
   evidence than an adversarial search (optimizing over the `a_i` themselves to maximize the
   LHS/RHS ratio, as the catalog's own suggested "First Research Experiment" actually asks for)
   failing to find growth. This pilot is the natural first (baseline) step, matching this
   project's own established convention (H-CAT37-1's random search before H-CAT37-2's
   adversarial follow-up) — not a substitute for the adversarial search.
2. Even a clean INFORMATIVE-NEGATIVE result does NOT prove Conjecture 16 in the open `p<2r`
   regime — it is one data point on one construction family (`r=3, p=2`, rank-1 `T_i`), not a
   proof for general (non-rank-1, adversarially chosen) tensor families.
3. Does NOT address `p=3,4,5` (also open for `r=3`, since `2r=6`) — `p=2` was chosen specifically
   because it makes the conjectured rate exactly dimension-FREE (`d^0`), the sharpest and most
   falsifiable-by-scaling special case, not because the other open `p` values are less
   interesting.
4. A LEAD result would NOT itself be a disproof of Conjecture 16 either — the conjecture's `Õ`
   notation hides an unspecified multiplicative constant depending on `r,p` and polylog factors;
   a modest, bounded power-law-looking trend over a finite `d`-range could still be consistent
   with a genuine polylog(d) rate that merely looks power-law-like over a limited range (the
   same caveat this project already learned the hard way for H-CAT31-3's own `mean(CV²)`
   model-comparison, Point 87).
