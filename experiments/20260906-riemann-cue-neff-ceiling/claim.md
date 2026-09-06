# claim.md — 20260906-riemann-cue-neff-ceiling

**Graph node:** `H-B1-1c` · **Bridge:** `B1-RMT-RIEMANN-HIC` · **Tier:** Standard (derivative known-answer
test, reuses the already-validated substrate/harness of `20260906-riemann-rstat-gue`)

> **Role of this experiment:** known-answer test #2 — the pilot (`H-B1-1a`) found ⟨r⟩ = 0.61092 for the
> first 100,000 zeta zeros, **+0.0103 above the asymptotic value**, and flagged `efficiency > 1 →
> CEILING_MISSPECIFIED` because the ceiling used was the N→∞ value, not a ceiling for the actual (finite-
> height) population measured. This experiment computes the CORRECT, height-dependent ceiling from
> Nishigaki (2025/PTEP 2026, arXiv:2507.10193) and checks whether the pilot's excess matches it.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 100,000 zeta zeros already downloaded and cached (`../20260906-riemann-rstat-gue/data/zeros1.txt`, sha256 verified in that experiment's `manifest.md`) |
| **Falsifiable predicate** | The observed relative excess of ⟨r⟩ over the exact sine-kernel limit matches, in sign and order of magnitude, Nishigaki's empirically-fitted finite-size correction 0.1896·N_e(T)^(−3.081) |
| **Measurable outcome** | ratio `observed_relative_deviation / predicted_relative_deviation`; PASS iff this ratio is in [1/3, 3] (see MCID — loose on purpose, see extrapolation caveat below) |

## FL Step -4: Source Trace (primary source read directly, not summarized)

**Corrects a near-miss:** an earlier note in this repo's `pearl_registry/INDEX.md` (written during the
`H-B1-1a` decision) cited an unverified figure "N_eff ≈ 1.446124 · ρ̄(γ_N)" from a WebSearch synthesis. That
number does **not** appear in the primary source and would have been a fabricated-precision error if used.
Fetched the actual PDF (`arxiv.org/pdf/2507.10193v1`) and read pages 12–14 directly.

| Claim | Source (verbatim, with equation number) | Status |
|---|---|---|
| N_e(T) = (1/√(12Λ)) · log(T/2π), Λ = 1.573151071... | Nishigaki 2025 (PTEP), Eq. (42), p.12. Λ attributed to ref. [3] Bogomolny–Bohigas–Leboeuf–Monastra 2006 (arithmetic constant from prime sums) | `[VERIFIED]` — read directly from PDF |
| Exact sine-kernel (N→∞) limit: 𝔼[r̃]∞ = 0.5997504209... | Same paper, p.14, citing the author's own prior work [13, Table 1] | `[VERIFIED]` — read directly from PDF |
| Empirical fit: relative deviation ⟨r̃⟩_T/𝔼[r̃]∞ − 1 ≈ 0.1896·N_e(T)^(−3.081) | Same paper, Fig. 6 caption, p.14: "the optimal linear fit to the six data points" (log-log), fit to Odlyzko's real zero data at n = 10⁸, 10⁹, 10¹⁰, 1.037×10¹¹, 1.304×10¹⁶, 1.000×10²³ | `[VERIFIED]` — read directly from PDF |

**Important scope note (found during this source trace, not hidden):** the six data points behind the fit
span n = 10⁸ to 10²³. This experiment applies the fit to n = 100,000 (10⁵) — **3+ orders of magnitude
below the fitted range**. This is an out-of-sample extrapolation, not a same-range validation. The MCID
below is set loose specifically because of this.

## Natural Language Statement

> "We estimate the ratio of the observed relative excess of ⟨r⟩ (first 100,000 zeta zeros, from
> `H-B1-1a`) over the exact sine-kernel limit, to Nishigaki's fitted power-law prediction for that same
> excess at the height of the 100,000th zero, treating the extrapolation 3+ orders of magnitude below the
> fitted range as a limitation to report, not to paper over."

## Falsifiable Claim

**Claim:** `observed_relative_deviation / predicted_relative_deviation` ∈ [1/3, 3].
**Check:** `python run.py` → `metrics/run.json["ratio_observed_to_predicted"]`.

## What This Does NOT Mean

1. Does NOT validate Nishigaki's fit in its calibrated range (n ≥ 10⁸) — this experiment only tests extrapolation to n = 10⁵.
2. Does NOT establish a NEW ceiling formula for future H-B1 experiments beyond restating the published one.
3. A PASS does NOT mean the pilot's original tolerance (0.01, MCID) should have been 0.002 in practice — the *correct* ceiling depends on T, and the loose [1/3, 3] band here reflects that this is a sanity check on the extrapolation, not a replacement tight criterion.

## MCID

MCID = factor-of-3 band on the ratio (not a numeric difference) — deliberately loose given the 3+ order of
magnitude extrapolation named above; a tight band would misrepresent how far outside the fitted range this test operates.
