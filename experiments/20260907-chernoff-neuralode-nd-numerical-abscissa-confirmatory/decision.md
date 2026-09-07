# decision.md — 20260907-chernoff-neuralode-nd-numerical-abscissa-confirmatory (H-B2-1o)

## Result

Pre-registered primary criterion: **CONFIRMED** — Fisher-combined p = 0.00192 < 0.05 (threshold
set in claim.md before the run), on 300 fresh (N_DIM, seed) pairs with ZERO overlap with
`H-B2-1n`'s exploratory-discovery seeds.

| N_DIM | rho | p | n |
|---|---|---|---|
| 16 | 0.357 | 0.00514 | 60 |
| 24 | 0.254 | 0.05049 | 60 |
| 32 | 0.368 | 0.00380 | 60 |
| 40 | 0.007 | 0.9587 | 60 |
| 50 | 0.007 | 0.9570 | 60 |

Fisher combined statistic = 27.833, p = 0.0019. All 5 slices positive sign. 2/5 individually
significant at alpha=0.05 (N=16, N=32); N=24 borderline (p=0.0505).

## FL Step 8a — Skeptic Pass (context-asymmetric: claim.md + run.py + run.json only, no session
history, no decision.md)

**Verdict: `[WEAKENED]`.** The pre-registered rule fired correctly and the letter of CONFIRMED
holds — skeptic explicitly accepted this. The substantive finding: **99.4% of the Fisher signal
comes from 3 of 5 slices (N=16: 37.9%, N=24: 21.4%, N=32: 40.1%); N=40 and N=50 contribute a
combined 0.6%.** rho=0.007 at BOTH N=40 and N=50 — not "weaker signal", indistinguishable from
zero to three decimal places, twice. Skeptic's core objection: Fisher's method tests "the null is
false somewhere in the set", not "the effect is uniform across the set" — the recomposed claim
"omega(A) correlates with M1 across N_DIM in {16,...,50}" is stronger than what the sub-tests, or
their Fisher combination, actually license.

**Response per the Skeptic Response Matrix (WEAKENED → promote with `[WEAK]` marker + document
caveat, not a kill):**

| Skeptic concern | Severity | Response |
|---|---|---|
| Fisher hides heterogeneity; recomposed "works across N" claim overreaches | HIGH | **Accepted.** Verdict stands as CONFIRMED per the pre-registered letter, but scoped explicitly below — this decision.md does NOT claim a uniform effect across the tested range. |
| Pre-registration not cryptographically committed; peeking cannot be ruled out from artifacts alone | LOW `[ГИПОТЕЗА]` | **Accepted as a real gap, mitigated but not eliminated.** `claim.md` was written and saved to disk before `run.py` was written or executed this session (file creation order, not a cryptographic commitment) — weak but real evidence against post-hoc tuning. Documented as a process improvement for future confirmatory runs: commit `claim.md` to git before generating the seed range as a stronger guarantee. |
| N=24 at p=0.0505, suspiciously close to threshold | LOW | **Dismissed as load-bearing.** Skeptic's own sensitivity check: verdict survives N=24 wobbling to p=0.10 (Fisher would still give ~0.013); only flips if N=24 degrades to ~p=0.5. Not the deciding factor. |
| Shared code across slices means Fisher's statistical independence != epistemic independence; `measure_m1`/`omega(A)` could be degenerate (near-constant) at high N, producing a spurious rho~=0 | MEDIUM | **Dismissed, cheaply verified from data already in hand (no new experiment needed).** See below. |

**Degeneracy check (resolves the MEDIUM concern):** direct inspection of the already-collected
per-seed data at N=40 and N=50 — `m1` spans **30.96 to 1621.70** at N=40 (CV=1.03) and **55.62 to
4672.25** at N=50 (CV=1.00); `omega(A)` has CV=0.070 (N=40) and 0.063 (N=50). Both quantities vary
substantially and non-degenerately at high N — rho~=0 is a genuine "these two are decoupled",
not a constant-value artifact of either measurement.

**Partial-conjunction test (post-hoc, walled off from the pre-registered verdict, same Anti-
Overfitting Gate discipline as `H-B2-1n`'s own exploratory Fisher computation — reported for
transparency, NOT used to overturn the pre-registered CONFIRMED):** Bonferroni-adjusted r=3-of-5
partial-conjunction p = **0.151** (3rd-smallest p-value 0.0505, adjusted by (5-3+1)=3). This
STRICTER test — requiring evidence the effect holds in a majority of slices rather than
"somewhere in the set" — does NOT clear alpha=0.05. This directly substantiates the skeptic's
HIGH-severity concern with a number, not just an argument.

## Honest Scoped Conclusion

The pre-registered primary criterion (Fisher combination) says **CONFIRMED**: the combined
evidence across the 5-slice family is non-null, and it replicates `H-B2-1n`'s exploratory finding
on completely independent data (seeds 40-99 vs. 0-39) — this is real, not noise or double-dipping.

But the honest scope, established by the skeptic pass plus a same-session post-hoc check: **the
signal is concentrated at N_DIM in {16, 24, 32} and is genuinely absent (rho~=0.007, twice) at
N_DIM in {40, 50}.** A stricter partial-conjunction test (p=0.151) does not support reading this
as a uniform effect. `omega(A)`, like `kappa(V)` before it, does **not** explain transient growth
at the largest tested dimensions (N>=40) — the primary open question `H-B2-1m` raised (what
governs M1 once these cheap descriptors stop working) remains open specifically for N>=40, while
`omega(A)` gains a genuine, replicated (if narrow-scope) advantage over `kappa(V)` at the
mid-range (N in {16,24,32}), where `kappa(V)` itself was already established as strong at small N
(N in {3,4,8,12}) and untested in this specific 16-32 band by `H-B2-1m`.

## Kill Analysis

**What this experiment killed:** the null hypothesis that `H-B2-1n`'s exploratory Fisher signal
was an artifact of the specific 200-point sample — it replicates on 300 fresh, non-overlapping
data points.

**What this experiment did NOT kill / does NOT establish:** a uniform relationship between
`omega(A)` and M1 across the full tested N_DIM range; the partial-conjunction test explicitly
fails to support that stronger reading (p=0.151). The N>=40 mechanistic gap `H-B2-1m` opened
remains fully open.

## What This Does NOT Mean

1. Does NOT establish `omega(A)` as a general-purpose replacement for `kappa(V)` — it has never
   been tested at small N (`H-B2-1m`'s N in {3,4,8,12} band, where `kappa(V)` is strong).
2. Does NOT mean the descriptor works "across N_DIM in {16,...,50}" — the partial-conjunction
   test explicitly fails that stronger claim (p=0.151); the honest reading is "works at N in
   {16,24,32}, absent at N in {40,50}".
3. Does NOT establish causality — both quantities are functions of the same random matrix.
4. Does NOT retroactively change `H-B2-1n`'s own WEAKENED verdict (that was a different,
   non-overlapping dataset).

## Relaxation Map / Next Steps (not auto-launched)

- A dedicated test at N_DIM in {64, 80} (skeptic's own suggestion) would discriminate "vanishes
  permanently above some N threshold" from "N=40,50 were an unlucky pair of slices" — genuinely
  new data required, not launched automatically.
- Future confirmatory experiments in this arc should commit `claim.md` to git BEFORE generating
  the seed range being tested, closing even the weak/hypothetical peeking gap the skeptic flagged.

## Pearl Registry Update

Two new falsifiable, testable side-findings from this experiment's own post-hoc analysis (Caveat
Gate — both name a specific untested alternative, not vague "more work needed"):
1. Partial-conjunction (k-of-n) testing as a standard companion to any future Fisher-combination
   verdict in this arc — Fisher alone materially overstates uniformity when slices are
   heterogeneous, demonstrated here with a concrete number (0.0019 vs. 0.151 on the same data).
2. Whether the omega(A)-M1 relationship reappears at N_DIM in {64, 80} (would support "N=40,50
   unlucky") or stays null (would support "genuine ceiling around N~35-40") — a concrete,
   cheap-to-run discriminating test, not launched in this session.
