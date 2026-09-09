# H-B2-4 — decision.md

## Result

**Clean, unambiguous null result — the exact opposite of the CRITERION_INVALID single-seed
sweep's own apparent (uninformative) signal.**

| `N_DIM` | Mean `M1` (30 seeds) |
|---|---|
| 3 | 4.40 |
| 4 | 4.87 |
| 8 | 8.39 |
| 12 | 13.11 |
| 16 | 24.09 |
| 24 | 46.86 |
| 32 | 122.79 |
| 40 | 354.16 |
| 50 | 1211.06 |

Averaged across 30 independent seeds (per `N_DIM`), the `M1(N_DIM)` curve is **perfectly
monotonically increasing** — `observed_sign_changes = 0`. The permutation null (2000 permutations,
each independently reshuffling each seed's own 9 `M1` values across the 9 `N_DIM` labels) gives a
mean of 4.64 sign changes and a 95th percentile of 6 — the observed value (0) is at the EXTREME
LOW end of the null distribution, not the high end a real non-monotonic effect would need.
`p_value = 1.0` (fraction of permutations with `>= 0` sign changes — trivially all of them, since
0 is the minimum possible value).

## Interpretation

`H-B2-1k`'s own original single-seed sweep found 8 sign changes (apparent strong non-monotonicity)
— but that sweep's own FL Step 8a skeptic pass showed this was statistically indistinguishable
from pure noise (`P(>=1 sign change | 9 iid draws) ~= 0.999994`). Averaging over 30 independent
seeds at each `N_DIM` cancels that noise and reveals the TRUE underlying relationship is smooth
and monotonic — the appearance of non-monotonicity in the single-seed sweep was exactly the
seed-to-seed noise artifact the skeptic pass predicted, not a real dimensional effect.

## Verdict

**REJECTED** — `H-B2-1j`'s own pearl_registry falsifiable prediction ("intermediate `N` should
show a non-monotonic `M1` profile") does NOT hold once seed noise is properly averaged out via
the multi-seed/permutation-test design `H-B2-1k`'s own decision.md explicitly named as the
correct fix. This is a clean, decisive, INFORMATIVE null — unlike `H-B2-1k`'s own
`CRITERION_INVALID` verdict (uninformative, criterion passed by pure noise regardless of the
truth), this experiment's own kill criterion (permutation-test p-value) is well-calibrated and
gives a confident answer either way — here, a confident REJECT.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the specific claim (from `H-B2-1j`'s own pearl_registry entry, impact 7)
that `M1(N_DIM)` shows genuine non-monotonic structure at a fixed spectral range, isolating
dimension from range. Multi-seed averaging shows the true relationship is smoothly monotonic.

**What was NOT killed:**
- `H-B2-1k`'s own raw `M1` measurements — real, valid data, only the "non-monotonic structure"
  INTERPRETATION (built on a single noisy seed) was ever invalidated, per that experiment's own
  `evidence` field note.
- The general observation (established across the whole B2 arc) that `M1` grows rapidly and
  systematically with `N_DIM` at fixed spectral range — confirmed here even more cleanly than
  before (smooth, not noisy).
- `H-B2-1l`'s own sharper eigenvector-conditioning mechanism hypothesis — untouched, this
  experiment does not test mechanism, only existence of the non-monotonic pattern itself.

**Relaxation Map:** none proposed — this closes a specific, previously-flagged, single-assumption
statistical gap cleanly, with a confident (not inconclusive) result. No further variant is
motivated by this outcome; the underlying question ("is `M1(N_DIM)` monotonic at fixed spectral
range?") is now answered: yes, monotonic, once measured properly.

## Revival Condition

Not applicable in the classic sense — the answer is confident, not `CRITERION_INVALID`. A future
revival would require a genuinely different design change (e.g. a different spectral-range
convention, or a materially different coupling structure), not a repeat of this exact question.

## FL Step 8a

**Not run** — REJECT verdict with a well-calibrated, confidently-decisive statistical test (not a
surprising CONFIRMED/PROMOTE result); per FL's own scope, Step 8a's mandatory pass applies to
PROMOTE-shaped or surprising findings.

## Scope note

Direct execution of `H-B2-1k`'s own named, previously-never-attempted fix ("needs a multi-seed x
multi-N grid with a permutation-test criterion instead"), closing a specific statistical loose
end left open by that experiment's own `CRITERION_INVALID` verdict. Not a new bridge-level claim
— Bridge 2's own broader status is documented elsewhere; this closes one flagged sub-question
within the already-explored B2 arc.
