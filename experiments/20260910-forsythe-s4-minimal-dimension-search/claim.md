# H-CAT37-2 — claim.md

## Origin

Direct follow-up from H-CAT37-1's retroscan (ADR-091, `pearl_registry/INDEX.md` entry
2026-09-10). Colbrook, Stepaniants, Townsend (arXiv:2609.04659) proved the Forsythe
conjecture FALSE for every restart length `s>=4`, via a diagonal SPD counterexample of
dimension `s+4` (dimension 8 for `s=4`), constructed through a certified
transverse-Hopf-bifurcation shadowing argument. The theorem's own machinery states that a
nonterminating limiting orbit at restart length `s` is supported on between `s+1` and `2s`
eigenvalues -- for `s=4`, between 5 and 8. **The authors' construction uses the upper end
of that range (8); minimality of dimension 8 is not addressed by the paper.**

**Source Trace (FL Step -4):** paper verified real via `mcp__arxiv__download_paper` (full
text, Theorem 1.1). Supplementary GitHub repository (`github.com/sgstepaniants/Forsythe`)
cloned and inspected directly -- confirmed the counterexample construction is NOT a simple
closed-form matrix (certified via rational arithmetic reaching numerators near 2^500000,
built through an analytic periodic-orbit/shadowing argument near a Hopf bifurcation). This
experiment does NOT attempt to reproduce that certificate -- it runs an INDEPENDENT
numerical search, honestly scoped as exploratory.

**Novelty Check (FL Step -3):** grep of `null_results/INDEX.md`, `parked/INDEX.md`,
`pearl_registry/INDEX.md`, `registry/graph.yaml` for "s=4"/"minimal dimension" in the
Forsythe context returns only this session's own pearl entry (2026-09-10) that motivated
this experiment -- not a re-attempt of anything prior.

## EstimandOps L0

**Question type:** Descriptive. "For restart length s=4, does a targeted (optimization-
driven, not random) numerical search find a diagonal SPD matrix of dimension n in {5,6,7}
whose restarted-CG residual-direction sequence fails to converge, or does the search
consistently fail to find one, informatively narrowing where the true minimal dimension for
an s=4 counterexample might lie?" No causal claim.

## Why this differs from H-CAT37-1 (not a re-run under a different name)

H-CAT37-1 used RANDOM and adversarial-spectrum (clustered/geometric) sampling -- a strategy
this session's own retroscan established was never capable of finding the authors'
near-measure-zero, Hopf-bifurcation-adjacent construction (their own certificate needed a
targeted analytic argument, not sampling). This experiment instead runs a GLOBAL
OPTIMIZATION search (`scipy.optimize.differential_evolution`) that explicitly maximizes an
objective correlated with non-convergence (the log-linear decay slope from H-CAT37-1's own
`_log_decay_slope`, reused unchanged) -- a search strategy actually suited to finding an
isolated bifurcation point, not a blind resample of the same kind H-CAT37-1 already
exhausted at n=5.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "the log-linear decay slope of `d_k` (H-CAT37-1's own
`_log_decay_slope`, reused here unchanged) is a sensible optimization objective for finding
a Hopf-bifurcation-adjacent matrix, because a Hopf bifurcation is exactly a point where a
mode's decay rate crosses zero."

**Check:** this is a plausibility argument from the general theory of Hopf bifurcations
(a real eigenvalue's real part crossing zero is the defining signature), not independently
re-derived for THIS specific restarted-CG dynamical system. Marked `[UNTESTED-MECHANISM]`
per falsification-ladder.md's own rule for a claim stated before it can be cheaply checked --
the check IS this experiment: if the optimizer never manages to push the decay slope toward
zero/positive at n in {5,6,7} despite explicitly trying to, that is itself evidence the
proxy objective is not finding anything interesting in this range (informative either way).

## The claim (falsifiable)

For restart length s=4, dimension n in {5, 6, 7}: run `differential_evolution` over
log-diagonal-entries, objective = maximize decay slope averaged over 3 fixed random initial
residual directions, each evaluated for 800 restarts (a fixed, moderate budget -- extended
to 5000 restarts as a follow-up check on ANY candidate the optimizer returns with a
near-zero or positive slope, per H-CAT37-1's own established practice of not trusting a
short observation window).

- **CONFIRMED (independent discovery)**: any candidate matrix, after the 5000-restart
  extended check, shows a genuinely non-decaying (near-zero or positive slope, sustained,
  not resolving to exact-solve or confirmed negative decay) residual-direction sequence --
  a real, independently found small-dimension counterexample.
- **INFORMATIVE_NEGATIVE**: the optimizer, despite explicitly searching for non-convergence,
  cannot push the decay slope above a small negative threshold at any tested n in {5,6,7} --
  narrows (does not prove) where the minimal counterexample dimension for s=4 might be,
  consistent with (not proof of) dimension 8 being minimal.

## What this does NOT mean

1. An INFORMATIVE_NEGATIVE result does NOT prove dimension 8 is minimal for s=4 -- a finite
   optimization run with a bounded budget (fixed maxiter/popsize, 3 seeds, log-diagonal
   bounds) cannot exhaustively rule out smaller dimensions; it is evidence, not proof, same
   epistemic status as H-CAT37-1's own original random-sampling finding.
2. A CONFIRMED result, if it occurs, would be a genuinely novel and citable finding (a
   smaller-than-published counterexample) -- but per this project's own calibration (ADR-084,
   ADR-085), the a priori probability is treated as LOW: this session's own reading of the
   published proof shows the construction requires delicate analytic machinery (transverse
   Hopf point, shadowing arguments) that a differential-evolution optimizer, evaluating a
   heuristic proxy objective, has no guarantee of navigating to.
3. Does NOT investigate restart lengths other than s=4, or dimensions above 7 (the paper's
   own dimension-8 construction is already an upper bound for s=4; searching there adds no
   new information).
