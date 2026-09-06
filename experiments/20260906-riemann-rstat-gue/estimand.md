# estimand.md — 20260906-riemann-rstat-gue
# question_type = descriptive → causal layer omitted by design (rules/estimand-ops.md)

## L1 Attributes

**Population:** imaginary parts γ₁…γ₁₀₀₀₀₀ of the first 100,000 nontrivial zeros of ζ(s), as tabulated in
Odlyzko `zeros1` (accuracy 3·10⁻⁹). Inclusion: all. Exclusion: none — a corrupted entry aborts the run
rather than being dropped.

**Intervention:** none (descriptive).

**Comparator:** GUE surmise ⟨r⟩ = 0.602658. Null: Poisson 0.386294. Discriminating alternative: GOE 0.535898.

**Endpoint:** ⟨r⟩ = mean over n of r_n = min(s_n, s_{n+1}) / max(s_n, s_{n+1}), with s_n = γ_{n+1} − γ_n.
Dimensionless, in [0, 1]. No unfolding applied (property of r; tested, not assumed).

**Summary measure:** absolute difference ⟨r⟩ − 0.602658; secondary: efficiency = (⟨r⟩ − floor)/(ceiling − floor).

**MCID:** 0.01.

---

## Intercurrent Events (ICE)

| Event | Strategy | Rationale |
|-------|----------|-----------|
| Non-positive spacing s_n ≤ 0 (duplicate / misordered zero) | composite → abort | A corrupted file is a pipeline failure. Dropping the pair would silently bias ⟨r⟩ (r=0 pairs pull it down); imputing is meaningless for a deterministic table. |
| Download fails or count ≠ 100,000 | composite → Substrate Gate `BLOCKED-INFRASTRUCTURE` | "Test could not run" ≠ "test failed". Recorded in substrate_gate.md, never as evidence against the claim. |

---

## Natural Language Statement

> "We estimate the mean consecutive-spacing ratio ⟨r⟩ of the first 100,000 nontrivial zeta zeros,
> comparing it to the GUE surmise 0.602658 (null: Poisson 0.386294), handling corrupted spacings by
> aborting the run (composite)."

---

## What This Result Does NOT Mean

1. Does NOT generalize to zeros at greater height (only heights ≲ 7.5·10⁴ are in the population); the
   direction of any drift is reported by the data-swap sensitivity, not extrapolated.
2. Does NOT establish causality — nothing was intervened upon.
3. Does NOT apply to any spectrum other than these zeros; in particular it says nothing about chromatin
   contact matrices (`H-B1-1b`).
4. Does NOT distinguish GUE from other β=2 ensembles (e.g. CUE) — ⟨r⟩ alone is not that sharp.

---

## Sensitivity Analyses (≥2 required)

1. **Data swap** — first 50k vs last 50k zeros. Expected: both within band; last half closer to 0.6027.
2. **Convention flip** — raw vs locally-unfolded spacings (sliding-window mean, w = 501). Expected: |Δ| < 0.002.
3. **Noise injection** — σ = 10 % of mean spacing. Expected: ⟨r⟩ decreases (repulsion smeared) but stays > 0.5.
4. **Alternative implementation** — pure-Python loop. Expected: identical to 1e-12.
