# claim.md — H-CAT7-1 (GD-ANYTIME-FINITE-v1)

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | A prefix-consistent, positive stepsize schedule `η=(η_1,η_2,...)` for gradient descent on the class of `L`-smooth convex functions (worst-case, via Performance Estimation Problem / PEP methodology, `PEPit`). |
| **Falsifiable predicate** | On a fixed, pre-registered training set of stopping times `N_train`, a SINGLE prefix schedule (same `η_1..η_k` used for every horizon `n≥k`) achieves a worst-case `R_n` PEP objective strictly, and by a pre-registered margin, better than the benchmark schedule realizing the known anytime rate `O(n^{-1.119})` (Zhang et al., cited in Tsai/Fatkhullin/Zhang/He 2026) — AND retains that margin on a disjoint, unseen `N_test`. |
| **Measurable outcome** | Run PEPit optimization under the prefix constraint (see Controls); compare `R_n(η_found)` vs `R_n(η_benchmark)` on `N_train` and `N_test`; PASS/FAIL per pre-registered margin below. |

> Gate rule satisfied: entity, predicate, outcome all concretely specified.

---

## L0: Question Type

- [x] Descriptive — "does a prefix-consistent finite-horizon schedule beat the known anytime benchmark, within a specific finite-horizon proxy test?"
- [ ] Predictive
- [ ] Causal

This is explicitly NOT a claim about the asymptotic exponent, and explicitly NOT an attempt to resolve the COLT 2024 open problem (Kornowski & Shamir) or close the gap established by Tsai/Fatkhullin/Zhang/He 2026 (arXiv:2607.02053). It is a bounded, finite-horizon existence question used as a cheap generator of structural hypotheses about *where* a better schedule's stepsize-mass distribution differs from known schedules — nothing more.

---

## Natural Language Statement

> We estimate whether a single prefix-consistent stepsize schedule (summary measure: worst-case PEP objective `R_n`, via `PEPit`), for GD on `L`-smooth convex functions (population: the standard PEP worst-case function class), evaluated at a pre-registered set of finite horizons `N_train ∪ N_test`, beats the benchmark schedule realizing the published `O(n^{-1.119})` anytime rate — with the SAME prefix required across all tested horizons (no per-horizon retuning; this is the ICE this claim must handle, via a hard prefix-consistency constraint, not by treating cross-horizon schedule variation as nuisance/missing data).

---

## Source Trace (mandatory, AI-generated claim per FL Steps -4/-3, verified via direct fetch, not search-engine paraphrase)

1. **COLT 2024 open problem** — Kornowski & Shamir, PMLR v247:5335-5339, open-access (PMLR), `[VERIFIED]` via direct fetch. States the anytime-vs-non-anytime GD rate question is open.
2. **Tsai, Fatkhullin, Zhang, He — "Lower Bounds for Anytime Acceleration of Gradient Descent"**, arXiv:2607.02053 (2026-07-02), open-access (arXiv), `[VERIFIED]` via direct fetch of the PDF (pages 1-6 read in full, not summary-only).
   - **Theorem 1.1** (page 5, quoted verbatim): "No stepsize schedule `η∈(0,∞)^ℕ` satisfies `R_n(η)=o(n^{-4/3})`."
   - **Best known anytime upper bound**: `O(n^{-1.119})` (Zhang et al., cited by Tsai et al. as ref [14]), realizing a partial answer to the COLT 2024 open problem.
   - **Confirmed gap**: "the answer to the COLT open problem lies between `n^{-1.334}` and `n^{-1.119}`" (page 5, "Implications" paragraph) — this project's own independent read confirms this exact interval, not accepted from a paraphrase.
   - **The trap this claim is specifically designed to avoid** (page 5, quoted verbatim): *"Lastly, from the numerical side, Das Gupta et al. [16] minimized `R_n(η)` over all `η` for each `n≤50` and found that the resulting convergence rates decay roughly as `O(n^{-1.178})`. This provides evidence that an `ω(n^{-2})` lower bound likely holds for both anytime and non-anytime convergence rates of GD."* — **this `n^{-1.178}` number is a PER-HORIZON (schedule retuned separately for each `n`) result, cited by its own authors as evidence toward a DIFFERENT, unrelated conjecture (`ω(n^{-2})`), NOT as an anytime rate.** Treating a per-horizon-optimal schedule as if it were an anytime schedule would silently reproduce this already-published, non-anytime result under a different name — the single most important negative control this claim must pass (see Controls: Adversarial Prefix Check).

---

## Claim Entropy

| Component | Count |
|---|---|
| Unsupported HIGH claims | 0 |
| Hidden assumptions | 0 (see HD-MAVP below) |
| Missing negative controls | 0 (prefix-consistency adversarial control defined in controls.md) |
| Ambiguous definitions | 0 |
| Unresolved blockers | 1 |
| **Total claim_entropy** | 1 |

> Unresolved blocker: `PEPit` not yet installed/used in this project; feasibility of the prefix-consistency constraint within PEPit's own solver interface not yet confirmed.

---

## Counterfactual Frame

| Question | Answer |
|---|---|
| What must change for H to be true? | A schedule class exists whose PEP-optimal member, under the prefix constraint, beats the `n^{-1.119}` benchmark on a bounded horizon range — no new physics/laws required, purely a question of whether the known schedule (silver stepsize / Zhang et al.'s construction) is locally improvable within reach of PEPit's solver on this bounded proxy. |
| How many independent changes required? | 1 — this is a direct computational search within an already-standard methodology (PEP), no new theory needed to RUN the test (only to interpret a PASS, which explicitly does NOT claim a new asymptotic result — see "What This Does NOT Mean"). |
| Known system where these conditions already hold? | Yes — PEPit is a standard, published tool (Taylor et al.) already cited in the literature searched above; this project has no prior PEPit usage, but the tool itself is mature and widely used in this exact literature. |

**Verdict:** `within-framework`.

---

## Falsifiable Claim

**Claim:** A single prefix-consistent stepsize schedule found by PEPit search beats the `n^{-1.119}`-realizing benchmark's worst-case `R_n` by a pre-registered margin on both `N_train` and unseen `N_test`.

**Check:** Run `pep_prefix_search.py` (to be written); compare `R_n(η_found)` vs `R_n(η_benchmark)` at each `n` in `N_train ∪ N_test`; PASS iff pre-registered margin (controls.md) holds on BOTH sets.

---

## HD-MAVP Decomposition

### Assumptions

| # | Assumption | Type | Role | Depends On | Evidence | Status |
|---|---|---|---|---|---|---|
| A1 | The benchmark schedule realizing `O(n^{-1.119})` (Zhang et al., ref [14] in Tsai et al.) can be reconstructed or closely approximated for use as the PEP comparator | empirical/tooling | core | — | not yet obtained — construction not given in the abstract-level fetch, needs full-text or a standard/silver-schedule proxy | unknown |
| A2 | PEPit's solver interface supports a HARD prefix-consistency constraint (same `η_1..η_k` across multiple simultaneously-optimized horizons `n_1<n_2<...`) without prohibitive computational cost | tooling | core | — | not yet tested | unknown |
| A3 | A pre-registered improvement margin can meaningfully distinguish "real structural improvement" from PEP solver noise/numerical tolerance | mathematical | belt | A2 | standard PEP numerical tolerance is well-documented in the PEPit literature | alive |
| A4 | `N_train`/`N_test` split with a hard prefix constraint is a valid finite-horizon proxy for "informative about schedule structure," even though PASS here does NOT resolve the actual asymptotic open problem | operational | peripheral | — | explicit in "What This Does NOT Mean" below — this is a generator of hypotheses, not a proof | alive |

**Principal Assumption (cut vertex):** A2 — if PEPit cannot express the prefix constraint at all (or only at prohibitive cost), the whole approach needs a different implementation (custom PEP formulation via `cvxpy` directly, bypassing PEPit's convenience layer).

### Constraints

- Constraint 1: Applies ONLY to the `R_n` (function-value) rate, not `G_n` (squared gradient norm) — matches the literature's own R_n/G_n split (Tsai et al. Theorem 1.1 vs 1.2).
- Constraint 2: A PASS on a bounded `N_train ∪ N_test` (e.g. up to `n≈200-500`, PEP computational cost permitting) says nothing about the true asymptotic behavior — explicitly not extrapolated.

### Unknowns

- [U] Exact construction of the `n^{-1.119}` benchmark schedule (Zhang et al.) — needs to be obtained before any comparison is meaningful.
- [U] PEPit's actual solver cost/scalability for a joint multi-horizon prefix-constrained search — unknown until attempted.

### Dependencies

- Dependency 1: `boyko-specialist`/catalog-screening dispatch (2026-09-18) that surfaced #7 with verified open-access sources.
- Dependency 2: `ADR-123` (2026-09-18) — this catalog item passes the two-part gate established there (source-traced to a specific, still-open, verified-recent literature gap; both sources open-access verified).

---

## Pearl Card

**Prediction:** if a PASS is found, the schedule's stepsize-mass distribution (where/how large stepsizes are placed relative to the horizon) should differ structurally from both the pure `n^{-1.119}` benchmark AND the per-horizon `n^{-1.178}` schedules of Das Gupta et al. — this structural difference, if found, is itself the interesting output, independent of whether the raw `R_n` margin is large.

**Falsification:** this claim is WRONG (FAIL) if, after a pre-registered solver budget, no prefix-consistent schedule beats the benchmark on `N_train`, OR a schedule beats it on `N_train` but the margin vanishes/reverses on `N_test` (the exact failure mode this claim's prefix constraint exists to catch).

---

## What This Does NOT Mean

1. Does NOT resolve the COLT 2024 open problem (Kornowski & Shamir) or narrow the `[n^{-1.334}, n^{-1.119}]` gap established by Tsai/Fatkhullin/Zhang/He 2026 — this is a finite-horizon proxy, not an asymptotic proof.
2. Does NOT establish a new asymptotic exponent even under a PASS — a finite-horizon PEP result generalizes to an asymptotic rate only with separate, much stronger machinery (matching this project's own established discipline from H-CAT31-3: a finite-`n` fit is never asymptotic evidence on its own).
3. Does NOT apply if PEPit cannot express the prefix constraint (A2) — in that case this claim is `BLOCKED-INFRASTRUCTURE`, not `FAIL` (per Substrate Gate discipline, `falsification-ladder.md` Step 2a) — infrastructure failure is never recorded as evidence against the claim.
4. A PASS does NOT mean the found schedule is anywhere near practical/production-usable — it is a structural-hypothesis generator only (see Pearl Card).

---

## MCID

MCID: pre-registered in `controls.md`, defined as a specific `R_n` improvement ratio, not "any positive difference" — protects against reporting solver noise as a finding (same discipline as this project's own PEP-adjacent LP-tolerance controls in H-CAT31-3).
