# decision.md — H-B2-1n (numerical abscissa omega(A) vs M1 at large N_DIM where kappa(V) failed)

## Result

**Verdict: WEAKENED** (per pre-registered criterion) — only 1 of 5 large-`N_DIM` slices
individually significant at alpha=0.05, below the majority (3/5) bar for CONFIRMED. But all 5
slices are positive with similar, moderate magnitude — a materially different, more consistent
pattern than kappa(V) showed on the identical population (2 of 5 slices negative).

| N_DIM | Spearman rho | p-value | Individually significant? |
|---|---|---|---|
| 16 | 0.213 | 0.188 | No |
| 24 | 0.209 | 0.195 | No |
| 32 | 0.234 | 0.147 | No |
| 40 | 0.349 | 0.027 | Yes |
| 50 | 0.270 | 0.092 | No |

**Comparison to kappa(V) at the identical population (H-B2-1m power follow-up):**

| N_DIM | kappa(V) rho | omega(A) rho |
|---|---|---|
| 16 | -0.012 | **0.213** |
| 24 | -0.091 | **0.209** |
| 32 | 0.157 | **0.234** |
| 40 | 0.057 | **0.349** |
| 50 | 0.298 | **0.270** |

omega(A) is positive at all 5 slices where kappa(V) was mixed-sign; magnitude is comparable to or
larger than kappa(V) at every slice except N_DIM=50.

## Exploratory, post-hoc analysis (explicitly NOT part of the pre-registered verdict)

Two additional observations, computed AFTER seeing the individually-non-significant slices,
walled off from the verdict per the Anti-Overfitting Gate's discipline against post-hoc
criterion relaxation (the verdict above was computed and fixed before either of these numbers
were touched — confirmed directly in `run.py`, and independently confirmed by the FL Step 8a
skeptic pass below):

1. **Fisher combination of the 5 independent slice p-values:** statistic=22.43, combined
   p=0.0131 (independently re-verified: `combine_pvalues([0.1879,0.1952,0.1466,0.0273,0.0918],
   method="fisher")` reproduces both numbers exactly). Legitimate — the 5 slices are genuinely
   independent (`SeedSequence([n_dim, seed])`, distinct `n_dim` values, no shared stream), unlike
   the pooled-raw-data confound FL Step 0a caught in `H-B2-1m`'s own design. This combines
   *independent test statistics*, not raw data points across dimension.
2. **Sign-consistency, a separate information channel from the individual p-values (skeptic
   finding, independently re-verified):** under a pure null, `P(all 5 slices same sign) = 2 *
   0.5^5 = 0.0625`. All 5 slices being positive is itself weak evidence against the null,
   orthogonal to the "only 1/5 individually significant" framing.

## FL Step 8a Skeptic Pass — full context-asymmetric run

Ran `Agent(skeptic)` with claim.md + run.py + real result numbers, no session history.
**Verdict: CONFIRMED-REAL.** Re-derived the kill-criterion code mapping line-by-line (matches
claim.md exactly), confirmed the Fisher-walling is algorithmically real (`verdict` is computed
and assigned in the code BEFORE `combine_pvalues` is even called — physically incapable of
influencing it), confirmed the independence assumption for Fisher combination is met
(`SeedSequence([n_dim, seed])` with distinct `n_dim` per slice), independently re-derived the
Fisher arithmetic (matches to the reported precision), verified `numpy.linalg.eigvalsh` is
backward-stable at this matrix size (no numerical-stability concern, unlike `cond(V)`'s open
concern from `H-B2-1m`), and confirmed the near-degenerate-omega check does what it claims
(catches rank-collapse, not a "small variance relative to M1" concern that would be a Spearman
misunderstanding — Spearman is scale-free by construction).

**Response Matrix:**
- **[MEDIUM, ACCEPTED] "Fisher walling is algorithmically real but narratively porous"** — the
  skeptic's concern is not that the code is wrong, but that presenting `fisher_p_combined=0.0131`
  in the same result dict as `verdict=WEAKENED` risks a LATER reader (a future session, or a
  next-round claim.md) silently treating WEAKENED as "essentially CONFIRMED, just underpowered"
  without a NEW, independently pre-registered test. **Response: explicit written guardrail below**
  — WEAKENED is the standing verdict; the Fisher/sign-consistency numbers motivate, but do not
  substitute for, a genuinely new pre-registered confirmatory experiment.
- **[LOW-MEDIUM, ACCEPTED] Sign-consistency is its own evidence channel, not captured by claim.md's
  three-way verdict framing** — correct, added explicitly above rather than left implicit.
- **[LOW, DISMISSED — not a bug]** near-degenerate check concern — skeptic's own analysis
  confirmed the check does what it claims; no fix needed.
- **[LOW, DISMISSED]** numerical stability of `eigvalsh` — skeptic confirmed no concern at this
  matrix size.

## Kill Analysis (WEAKENED — partial, not a clean REJECT or CONFIRMED)

**What is KILLED:** the claim that omega(A) *individually and majority-significantly* explains
M1 at large `N_DIM` under the pre-registered bar — it does not, at this sample size (40
seeds/slice).

**What is NOT killed, and is arguably strengthened:**
- omega(A) shows a more consistent (uniformly positive) and often larger-magnitude relationship
  with M1 than kappa(V) did on the IDENTICAL population — a real, verified comparison, not
  incidental.
- The combined evidence (Fisher p=0.0131, sign-consistency p=0.0625) is suggestive of a real,
  weak effect that this experiment's power (n=40/slice) was not quite sufficient to confirm
  slice-by-slice — but this is a **hypothesis for a follow-up experiment, not a promoted claim**.

**Relaxation Map — the correct next step is explicitly named, not vague:**
- A **NEW, separately pre-registered experiment**, with the Fisher-combination (or an
  equivalent multi-slice combined test) as the PRIMARY kill criterion from the start — not a
  retroactive re-analysis of this same data (would be double-dipping / optional stopping bias) —
  ideally on a FRESH seed range (e.g. seeds 40-99) to avoid reusing the same 200 data points for
  both the exploratory discovery and the confirmatory test.
- This is a genuinely new experiment design decision (what primary statistic to pre-register,
  how many seeds, whether to hold the N_DIM set fixed) — **not launched automatically as part of
  this decision.md**, per this session's own standing discipline about not auto-chaining new
  experiments without a checkpoint.

## What This Does NOT Mean

1. Does NOT establish omega(A) as confirmed superior to kappa(V) — only that it shows a more
   consistent SIGN pattern on this specific comparison; magnitude comparison is close at most
   slices, and neither descriptor clears its own pre-registered bar cleanly.
2. Does NOT retroactively upgrade this experiment's own verdict to CONFIRMED — the Fisher/
   sign-consistency numbers are exploratory and explicitly guardrailed, per the skeptic's own
   accepted concern.
3. Does NOT establish causality between omega(A) and M1.
4. A future confirmatory experiment along the Relaxation Map's suggested design could still
   REJECT — the current evidence is suggestive, not proof.

## Pearl Registry Update

New falsifiable, testable side-finding: omega(A) is uniformly positive (5/5) and of comparable-
or-larger magnitude than kappa(V) at every large-`N_DIM` slice tested, on the identical
population — a genuine, verified comparison worth a properly pre-registered confirmatory
follow-up (fresh seeds, Fisher combination as primary criterion), not an automatic promotion.
