# decision.md — 20260906-riemann-cue-neff-ceiling

**Graph node:** `H-B1-1c` · **Date:** 2026-09-06 · **Role:** known-answer test #2, checks the pilot's
CEILING_MISSPECIFIED excess against the correct height-dependent prediction

## Verdict

- [x] **PROMOTE** — claim holds, comfortably inside the pre-registered band (see caveat below)
- [ ] REPEAT / REJECT / ARCHIVE

**Promoted statement:** *The excess of ⟨r⟩ = 0.61092 over the exact sine-kernel limit 0.59975 (relative
deviation +1.86%) for the first 100,000 zeta zeros matches Nishigaki's (2025) fitted finite-N_eff
correction (predicted +1.77%) to within a ratio of 1.05 — despite the fit being extrapolated 3+ orders of
magnitude below its calibrated range (n=10⁸–10²³ → applied at n=10⁵). The "last 50k zeros" window gives
ratio 0.88, same conclusion. This resolves the `CEILING_MISSPECIFIED` flag from `H-B1-1a`'s decision.md:
the pilot's excess was never evidence against GUE universality — it was a correctly-signed, correctly-sized
finite-height correction that the pilot's ceiling (built for N→∞) could not see.*

## Floor-Ceiling Interval

_Mapping for this experiment (ratio-of-two-formulas test, not a raw metric): the null model with the
FINITE-SIZE MECHANISM REMOVED assumes zero correction (i.e. treats the sample as already asymptotic,
which is exactly the mistake `H-B1-1a` made); the privileged-access performer is Nishigaki's literature
formula, which "sees" the true finite-N_eff physics we don't have independent access to. Efficiency =
observed/ceiling is then identical to the `ratio_observed_to_predicted` already computed in `run.py`._

### Population
Same as `claim.md`: first 100,000 zeta zeros (cumulative) and last-50k window, cached `zeros1.txt`.

### Floor
- Construction: null model with the finite-size mechanism removed — assume zero correction (asymptotic already reached)
- Value: 0 (by construction)
- Result: [x] MEASURED

### Ceiling
- Construction: Nishigaki (2025) fitted formula, privileged access to the true finite-N_eff correction
- Value: 0.017668 (cumulative) / 0.019243 (last-50k window)
- Result: [x] MEASURED

### Efficiency
- Value: 1.054 (cumulative) / 0.884 (last-50k window)
- Result: [x] REPORTED
- Not degenerate: ceiling ≠ floor (0.0177 ≠ 0), observed is not below floor (both relative deviations positive)

## Decision (Step 4a)

- [x] `PROCEED` — floor (0) ≠ ceiling (≈0.018–0.019); the pre-registered [1/3,3] band on efficiency is
  healthy headroom, not a degenerate near-zero denominator.

## Evidence Summary

| Check | Result |
|-------|--------|
| Formula source | `[VERIFIED]` — read directly from primary-source PDF (arXiv:2507.10193v1, pp.12–14), not a secondary summary |
| Near-miss caught | An earlier unverified figure ("N_eff ≈ 1.446·ρ̄(γ_N)", from a WebSearch synthesis, recorded in `pearl_registry/INDEX.md` during the `H-B1-1a` decision) does **not** appear in the primary source — would have been a fabricated-precision error if used. Not used. |
| Harness | `tests/test_cue_neff_ceiling.py`, 5 tests, all pass — includes a negative control (`test_pass_band_can_fail`) confirming the [1/3,3] band is not vacuous |
| Data reuse | Same cached, sha256-verified `zeros1.txt`; same tested `mean_r()` from `H-B1-1a` — no new data, no new untested code path for the statistic itself |
| Cumulative (n=1..100k) | ratio 1.054 → PASS |
| Last-50k window | ratio 0.884 → PASS |

## Rationale

PROMOTE, not REPEAT: both windowings pass with large margin inside the pre-registered [1/3,3] band, which
was itself set loose specifically because of the extrapolation risk (see `claim.md` § scope note). The
result coming in this tight (ratios within ~12% of 1.0) is stronger than the band demanded — worth stating
plainly, not downplaying, but also not grounds to retroactively tighten the band post hoc (that would be
the exact overclaim pattern this repo's rules warn against).

## Skeptic Concerns and Resolution

Full asymmetric-context skeptic pass **not run** — this is a Standard-Ladder derivative test (reuses an
already-skeptic-reviewed substrate from `H-B1-1a`), not a fresh Full-Ladder promotion. Pre-answered
concerns instead:

| Concern | Resolution |
|---|---|
| "3+ orders of magnitude extrapolation makes this meaningless" | **Accepted as a stated limitation**, not dismissed — `claim.md` names it explicitly and the loose [1/3,3] band is the direct response. The result still PASSING that loose band, and doing so this tightly, is informative; it does not retroactively justify treating the extrapolation as safe in general. |
| "Only 2 windowings tested, not independent" | **Accepted**: cumulative and last-50k overlap (last 50k ⊂ first 100k). Both point the same direction. A fully independent check would need a disjoint height range (e.g. `zeros2` table), not attempted here — scope of this experiment was to close the `H-B1-1a` flag, not open a new data-acquisition task. |

## What This Does NOT Mean

1. Does NOT validate Nishigaki's fit in general — only checks whether extrapolating it 3+ orders of magnitude below its calibrated range gives a directionally and order-of-magnitude correct answer for this one case.
2. Does NOT mean the original `H-B1-1a` tolerance (0.01) should be retroactively replaced by a height-dependent one — that would require redesigning `H-B1-1a` before, not after, seeing this result.
3. Does NOT test any new mechanism — this is a literature-formula check against already-collected data, not a new experiment on new data.

## Pearl Card Update

**Was the Prediction correct?** Yes — ratio landed inside [1/3,3] on both windowings, tighter than required.
**Falsification condition triggered?** No.
**Follow-up filed:** none required — this closes the `CEILING_MISSPECIFIED` open item from `H-B1-1a`.
