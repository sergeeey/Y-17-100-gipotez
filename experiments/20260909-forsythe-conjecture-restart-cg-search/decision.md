# H-CAT37-1 — decision.md

## Result

### First run (500 restarts) — a real bug caught before any claim was made

Two problems surfaced, in sequence, before a trustworthy number existed:

1. **Threshold artifact.** The original classifier required `d_k < 1e-8` sustained for 20
   restarts within a fixed 500-restart budget. 48/144 pairs "failed" this — but every one
   of them had `final_d` in the 1e-6 to 1e-4 range and was still visibly decreasing
   (`final_d < max_d_last_50` in nearly all cases). Reporting these as counterexamples to a
   58-year-old conjecture would have been overclaiming on a miscalibrated stopping rule, not
   a real finding. Fixed by replacing the hard threshold with a log-linear decay-slope test
   over the trailing 150 restarts (`_log_decay_slope`) — distinguishes "still decaying,
   just slowly" from "plateaued."
2. **Numerical substrate bug (Mechanism Claim Gate catch).** After the threshold fix, a
   second, more serious pattern remained: 22 pairs showed a *positive* decay slope
   (residual gap growing), concentrated entirely in the `geometric` (ill-conditioned,
   cond(A)~1e6) matrix family. Direct diagnosis (`diag_krylov.py`) found the cause: the raw
   power-basis Krylov construction `[y, Ay, A^2y, ...]` had `cond(V)` reaching **1e19 at
   s=7** for cond(A)=1e6 — numerically singular well past double precision. The Galerkin
   solve against that basis was producing garbage, not evidence about the Forsythe
   iteration. Fixed by replacing the power basis with a Lanczos-orthonormalized one
   (`krylov_orthonormal_basis`, full reorthogonalization, `cond(Q)=1` by construction,
   regression-tested in `tests/`).

Both fixes are the Mechanism Claim Gate (`falsification-ladder.md` Step 0a) working as
intended: neither bug was found by staring at code, both were found by checking whether an
implausible early result ("residual gap growing") survived a targeted, minimal diagnostic.

### Final run (1500 restarts, corrected classifier + corrected Krylov basis)

| bucket | primary (s>=3, n=144) | secondary (s=2, n=27) |
|---|---:|---:|
| `exact_solve_hit` (trivial, uninformative) | 118 | 18 |
| `converged_strict` (d_k < 1e-8 sustained) | 3 | 0 |
| `converging_slowly_real` (confirmed negative log-slope) | 17 | 9 |
| `no_decay_detected` (candidate) | 6 | 0 |

6 candidates remained even at 1500 restarts, all in the `geometric` (cond(A)~1e6) family.
**Extended-restart follow-up (up to 8000 restarts) resolves all 6**: 5 hit `exact_solve_hit`
and 1 shows a confirmed negative decay slope (`-6.3e-4`). This is captured directly as a
regression test (`test_no_genuine_counterexample_survives_extended_restart_budget`,
parametrized over all 6 cases) so the claim is re-checked, not just asserted in prose.

**Zero genuine counterexamples found** across 171 tested (n, mode, s, seed) combinations
(n in {5,8,12}, s in {2,...,n-1}, 3 matrix families x 3 seeds each), once measurement
artifacts (threshold miscalibration, numerical substrate bug) are corrected.

### Secondary claim — independent numerical check on the 3 fresh (Aug 2026) s=2 proofs

27/27 s=2 pairs are either exact solves (18) or confirmed decaying (9) — no plateau, no
candidate counterexample. Consistent with (does not verify the mathematical content of)
Colbrook/Stepaniants/Townsend, Liesen, and Peng's independent August 2026 claimed proofs
for s=2.

## Verdict

**CONFIRMED** (numerical evidence on the tested sample is consistent with the Forsythe
conjecture) — matching what the source paper itself already states ("numerical evidence
suggests the conjecture is true"). Per claim.md's own pre-registered calibration, this was
the a priori expected outcome, not a surprise; the value of this experiment was in (a)
independently reproducing that numerical evidence with a from-scratch implementation, and
(b) the two real methodology bugs caught and fixed before any claim was made — the
`no_decay_detected` bucket at 1500 restarts is an honest artifact-in-progress, not silently
smoothed over, and the extended-restart test makes that verifiable by anyone re-running the
suite.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the hypothesis that this specific from-scratch implementation, at
n<=12 and s<=11, would find a counterexample to the general (s>=3) Forsythe conjecture. It
did not, on 171 tested combinations.

**What was NOT killed:** the conjecture itself (never provable by finite search — see claim.md
§ What This Does NOT Mean #1), nor any claim about n>12 or s>=12 behavior.

**Revival condition:** a genuinely different test would need either (a) n>12 with a
numerically-robust extended-precision implementation (double precision starts becoming
marginal for cond(A)~1e6 well before n=12; the 6 late-resolving candidates in this run are
a direct signal of that margin), or (b) a systematic sweep over a much larger seed/mode
space than 3 seeds x 3 modes. Neither is planned — this experiment's own low a priori
probability of finding something 58 years of research missed (claim.md § What This Does
NOT Mean #4) was confirmed, not surprising.

## Skeptic Concerns (pre-answered, FL Step 8a — self-review, no reviewer turn spent given
the low-stakes, non-architectural nature of a single descriptive numerical claim; the two
real bugs already caught and fixed via the Mechanism Claim Gate substitute for an external
adversarial pass here)

- "Only n<=12 tested — this proves nothing about the general conjecture" →
  **Accepted, explicitly stated in claim.md before any run.** Never claimed otherwise.
- "The remaining margin at cond(A)~1e6 might hide something real at higher precision" →
  **Accepted limitation**, named as the revival condition above, not investigated further
  here (matches this experiment's own cost discipline — a cheap first check, not an
  open-ended investigation).
- "Two implementation bugs in the first version — how do we know there isn't a third?" →
  **Cannot rule out with certainty**, but the regression test suite (12 tests, including 2
  bugs' own regression guards: orthonormality-regardless-of-conditioning, and the
  extended-restart resolution check) raises the bar for a silent third bug materially above
  the first version's bare `run.py` with no tests.

## Scope note

This experiment falls under the 2026-09-09 scope expansion (ADR-087) — a standalone
catalog item (#37) with no thematic connection to this project's original 4 anchors
(H-7/RMT, ChernoffPy, May1972, Bridge 3/7 infrastructure). Registered and run under the
expanded scope, not as a "bridge" in the original sense.
