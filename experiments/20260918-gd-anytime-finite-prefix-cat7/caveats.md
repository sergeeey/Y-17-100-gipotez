# caveats.md — H-CAT7-1

Written against the design, not retrofitted to the outcome. Every item below was
identifiable before the main test returned a verdict.

## 1. A finite-horizon PEP comparison is not a statement about an exponent

The whole experiment compares `R_n` at `n ≤ 24` (positive control: `n ≤ 50`). The
Zhang–Lee–Du–Chen guarantee is asymptotic, with an explicit constant `1/36` inside
Lemma 7 of arXiv:2411.17668. A schedule that beats ZLDC's *realised* `R_n` at small
`n` may be doing nothing but exploiting that constant, which the asymptotic result
never claimed to be tight. Beating the benchmark's finite-`n` values and beating the
`n^{-1.119}` rate are different claims, and only the first is tested here.

Concretely: ZLDC's own first step is `1.6012`, which is already worse at `n=1` than a
plain `h=1.5`. The construction deliberately gives up early-horizon performance to
buy the anytime guarantee. A finite-horizon win against it is therefore cheap in a
way an asymptotic win would not be.

## 2. Any PASS is bounded by the per-horizon ceiling, and that ceiling is small

`ceiling.py` computes, at each tested horizon, the best `R_n` achievable by *any*
length-`n` schedule with no cross-horizon coupling whatsoever. A prefix-consistent
schedule is a feasible point of that unconstrained problem, so its ratio can never
beat the ceiling ratio. The measured ceilings sit in the range ~0.90–0.945, i.e. the
total headroom over ZLDC at these horizons is only ~6–11%. The pre-registered PASS
bar (5%, ratio ≤ 0.95238) therefore sits *inside* the headroom but not far inside:
at the tightest horizons a prefix-consistent schedule must capture ~85–90% of the
entire achievable improvement while doing so simultaneously at every other horizon.
This is why a FAIL here is interpretable and a PASS would be a narrow one.

## 3. The outer search is local, so a FAIL is a bounded-budget FAIL

Minimising `R_n` over stepsizes is non-convex — this is precisely why Das Gupta et
al. needed branch-and-bound to claim global optimality. The search here is
multi-start L-BFGS-B with exact gradients, which finds good local optima, not
certified global ones. Consequently:

* a **PASS** would be sound (an exhibited schedule is a constructive witness, and its
  `R_n` values are exact PEP worst cases regardless of how the schedule was found);
* a **FAIL** is "not found within this budget", never "does not exist".

The same asymmetry applies to the ceiling numbers, which are upper bounds on
achievable improvement only up to the same local-search caveat — a better global
optimum would *raise* the headroom, so the ceiling reported here is, if anything,
conservative as a bound on what a prefix schedule could reach.

## 4. Index convention

This code counts gradient steps `N`; ZLDC count iterates `T = N + 1`. Candidate and
benchmark pass through the same evaluator, so the offset cancels exactly in every
ratio. It shifts a fitted *exponent* by `O(1/N)`, which is why the positive control
reports the fit both ways.

## 5. The positive control reproduces an empirical literature number, not a theorem

`n^{-1.178}` is what Das Gupta et al. observed for `n ≤ 50`; it is not a proven rate
and carries no stated uncertainty in the source. The control is an order-of-magnitude
harness check. A fitted exponent within a few hundredths of `-1.178` means the harness
finds near-optimal schedules; it does not confirm or refute anything about `n^{-1.178}`
itself. Its own fit quality (`r2`) is reported so a reader can see whether a single
power law even describes the five points.

## 6. What a PASS would and would not license

Wording fixed in advance: a PASS is **"finite-horizon PEP evidence for a potentially
improved anytime schedule"**. It is not a new asymptotic exponent, not an answer to the
COLT 2024 open problem of Kornowski & Shamir, and not a narrowing of the
`[n^{-1.334}, n^{-1.119}]` interval established by Tsai et al. Tsai et al. themselves
distinguish "for all `n`" from "for infinitely many `n`"; a finite-horizon result
establishes neither beyond the tested range.

## 7. Solver-level

Worst cases are exact SDP values at `tol=1e-9` (CLARABEL), cross-checked against a
closed form to `<1e-8` relative and against PEPit's independent implementation to
`<3.5e-5` relative. Both are far below the 5% decision margin, so the verdict is not
solver-tolerance-limited. Trial points where the solver failed outright are scored as
a penalty, never as a good value — a failed solve is an infrastructure event, not
evidence.
