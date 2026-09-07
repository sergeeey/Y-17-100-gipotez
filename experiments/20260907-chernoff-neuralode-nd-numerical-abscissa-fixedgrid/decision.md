# decision.md — 20260907-chernoff-neuralode-nd-numerical-abscissa-fixedgrid (H-B2-1q)

## Result

Pre-registered primary criterion: **NOT_REPLICATED**. N=64, on fresh seeds 100-159 (zero overlap
with `H-B2-1p`'s seeds 0-59): rho=0.073, p=0.579 — nowhere near significant, and far from
`H-B2-1p`'s original rho=0.298, p=0.021.

| N_DIM | rho | p | n |
|---|---|---|---|
| 56 | 0.077 | 0.560 | 60 |
| 64 | 0.073 | 0.579 | 60 |
| 72 | 0.093 | 0.481 | 60 |

All three fresh slices show small, positive, individually non-significant correlations —
strikingly consistent with each other (rho 0.07-0.09) and with `H-B2-1o`'s N=40/N=50 null
(rho=0.007 each) and `H-B2-1p`'s N=80 null (rho=0.088, p=0.506), NOT with `H-B2-1p`'s disputed
N=64 result. This is not a borderline or ambiguous outcome — it is a clean, three-way-consistent
null.

## The Dispute Is Resolved

`H-B2-1p`'s N=64 finding (rho=0.298, p=0.021, seeds 0-59) does NOT replicate on fresh,
pre-registered-grid data (seeds 100-159). Per the skeptic pass that flagged this dispute in
`H-B2-1p`: N=64 and N=80 were chosen adaptively, specifically because N=40/50 were null, to test
for "reappearance" — and that adaptive selection inflated the false-positive rate beyond the
naive p=0.021 suggested. This experiment is the direct test of that concern, and the concern was
correct: **`H-B2-1p`'s N=64 result was drawer-selection, not a real, replicable relationship.**

## Honest Arc-Wide Conclusion (H-B2-1m through H-B2-1q, complete)

| N_DIM | rho | p | individually significant? | seed range |
|---|---|---|---|---|
| 16 | 0.357 | 0.00514 | **yes** | 40-99 |
| 24 | 0.254 | 0.05049 | borderline | 40-99 |
| 32 | 0.368 | 0.00380 | **yes** | 40-99 |
| 40 | 0.007 | 0.9587 | no | 40-99 |
| 50 | 0.007 | 0.9570 | no | 40-99 |
| 56 | 0.077 | 0.560 | no | 100-159 |
| 64 (adaptive) | 0.298 | 0.021 | yes (drawer-selected) | 0-59 |
| 64 (fixed-grid) | 0.073 | 0.579 | no | 100-159 |
| 72 | 0.093 | 0.481 | no | 100-159 |
| 80 | 0.088 | 0.506 | no | 0-59 |

**The honest, final reading of this arc:** `omega(A)` correlates solidly with M1 at N in
{16,32} (both p<0.01, on the seed range 40-99 already used for a confirmatory Fisher test in
`H-B2-1o`). The relationship is genuinely absent — not underpowered, not intermittent, not an
artifact of any single unlucky pair — at every N_DIM tested from 40 upward (40, 50, 56, 64, 72,
80, spanning two independent seed ranges). The one apparent exception (N=64 on seeds 0-59) has
now been directly tested and shown not to replicate. `omega(A)`, like `kappa(V)` before it, has a
real explanatory ceiling somewhere between N=32 and N=40, and nothing tested in this arc explains
what governs M1 above that ceiling.

## Kill Analysis

**What this experiment killed:** the "unlucky pair" reading of `H-B2-1p`'s N=64/N=80 result —
directly, not by inference. N=64 was re-tested on independent data under a genuinely
pre-registered fixed grid and did not replicate.

**What this experiment did NOT kill:** the solid N=16/N=32 result (untouched, different
question); the possibility that some OTHER descriptor (pseudospectral abscissa, named but never
tested in this arc) explains M1 above N~35-40. Only `kappa(V)` and `omega(A)` have been ruled out
as explanations at large N, not the general possibility that transient growth is explicable
there by some other means.

**Revival Condition (mandatory per FL null_results protocol):** this specific claim — that
`omega(A)` explains M1 at N>=40 — is `hard_killed` in the sense that no further seed-count or
grid-density increase at N in {40,...,80} is expected to change the answer (the pattern across
TWO independent seed ranges, six total N_DIM values from 40 to 80, is too consistent to be a
power problem). Revival would require a DIFFERENT descriptor (pseudospectral abscissa or another
candidate) to be proposed and tested — not more seeds on the same two descriptors already ruled
out at this range.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1o`'s CONFIRMED-but-scoped verdict for N in {16,24,32} —
   that result used a different seed range (40-99) and stands independently.
2. Does NOT prove no descriptor could ever explain M1 at large N — only that `kappa(V)` and
   `omega(A)`, the two tested in this arc, do not.
3. Does NOT establish causality.
4. This experiment, by design, only directly re-tested N=64 (the disputed value) plus two
   flanking points (56, 72) for context — it does not re-test N=80 (already null in `H-B2-1p`)
   on fresh seeds, though the consistency of 56/64/72 with the existing 40/50/80 pattern makes a
   separate re-test of 80 low-priority.

## Relaxation Map / Next Steps (not auto-launched)

- The B2-CHERNOFF-UDE bridge's open question is now cleanly stated: what explains transient
  growth M1 at N_DIM>=40, given that both tested cheap descriptors (`kappa(V)`, `omega(A)`) have
  a real explanatory ceiling there? Pseudospectral abscissa (named, deferred as expensive, back
  in `H-B2-1n`'s own claim.md) is the most obvious next candidate, but this is a NEW hypothesis
  requiring a new claim.md, not a further variation of the current two descriptors.
- This was the last step named in `H-B2-1p`'s Relaxation Map. Per this session's own standing
  discipline against auto-chaining without a checkpoint, and because the next genuine step
  requires a new descriptor (a real design decision, not a parameter sweep), this experiment
  stops the H-B2-1* numerical-abscissa sub-arc here and awaits user direction.

## Pearl Registry Update

Closes the entry from `H-B2-1p` about N=64's disputed status — resolved NOT_REPLICATED, with a
number, not left open. New entry: the arc-wide six-point null pattern from N=40 to N=80 across
two independent seed ranges is strong enough evidence to `hard_killed` (not just REJECT) the
"omega(A) explains M1 at large N" claim specifically — any future attempt to revive it should
require a different descriptor, not more seeds on the same one.
