# H-CAT37-1 — decision.md

## Retroscan addendum (2026-09-10, ADR-091)

**The general conjecture is now PROVEN FALSE for every s>=4.** Colbrook, Stepaniants, and
Townsend, "A Complete Resolution of Forsythe's Conjecture for Restarted Conjugate
Gradients", arXiv:2609.04659 (submitted 4 Sep 2026, five days after this experiment's
2026-09-09 run) — verified real via `mcp__arxiv__download_paper` and the authors' own
supplementary GitHub (`github.com/sgstepaniants/Forsythe`, Lean-formalized proof, verified
by cloning and inspecting the repository directly, not taking the arXiv abstract alone).
Sharp classification: TRUE for s in {1,2,3} (s=1 was already Akaike's 1959 theorem), FALSE
for every s>=4, via an explicit diagonal SPD counterexample of dimension s+4.

**Does this invalidate this experiment's 0/171 finding? No — and here is why, checked, not
assumed.** The counterexample is NOT a simple closed-form matrix a search could stumble
onto. It is constructed via a certified transverse-Hopf-bifurcation shadowing argument: the
authors' own computer-assisted-proof stage uses exact rational arithmetic with numerators/
denominators reaching magnitudes near 2^500000, and the paper's own scope note states that
even *"Proposition C.1.2's particular epsilon_0, M, and N construction is outside the
configured theorem set"* — i.e. the authors themselves have not reduced this to one clean,
publishable floating-point example either. This experiment's random and adversarial
(clustered/geometric-spectrum) sampling at n<=12, s<=11 was never capable of finding a
construction this delicate — a near-measure-zero point in parameter space, reachable only
via the specific analytic machinery of their proof. The 0/171 finding stands as exactly
what claim.md always said it was (`## What this does NOT mean`, item 4): informative
evidence that *this specific sampling strategy* found nothing at these n, s — never a claim
about the general conjecture, which is now settled by an entirely different (and vastly
more sophisticated) method.

**What DOES need updating:** the `registry/graph.yaml` node status text, which previously
read as if the conjecture itself remained open — corrected (see `PROB-CAT-37`/`H-CAT37-1`,
updated 2026-09-10) to state the resolution explicitly and distinguish "this experiment's
own narrow finding" from "the general theorem," which the original wording did not clearly
separate.

**A genuinely open, well-scoped follow-up this resolution creates:** the theorem states
every nonterminating limiting orbit at restart length s is supported on between s+1 and 2s
eigenvalues (for s=4: between 5 and 8). Their explicit construction uses dimension 8 (the
upper end of that range). Whether a genuine s=4 counterexample exists at dimension 5, 6, or
7 is not settled by the paper (they prove existence at s+4, not minimality). This is a
concrete, well-posed, small-scope question — distinct from "reproduce their certificate"
(assessed separately as disproportionate for a session-scale task, see below) — that a
targeted (not random) numerical search could address. Not attempted in this addendum;
flagged as the honest next step if pursued.

**"Reproduce the author's certificate" — assessed, not just attempted.** Investigated
whether this is a cheap first test as hoped: cloned the supplementary repository and read
`NUMERICAL_TARGETS.md` and `computer-assisted-proof/README.md` directly. The certificate
that IS reproducible cheaply (`bash computer-assisted-proof/verify.sh`) checks the finite
algebraic/interval premises of a Hopf-bifurcation argument (root branches, tangent
constructions, phase weights) — it is not itself an explicit test matrix, and running it
would only confirm the authors' own certificate is internally consistent, not give this
project a numeric example to test its own H-CAT37-1 code against. Extracting an actual
finite floating-point counterexample matrix would require engaging with the periodic-orbit/
shadowing analytic argument directly (the Lean proof's own scope note: this translation is
"outside the configured theorem set" even for the authors). This is genuinely a
multi-session-scale undertaking, not a quick verification — correcting the optimistic
framing in the direction-scoping message that prompted this addendum.

---

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
