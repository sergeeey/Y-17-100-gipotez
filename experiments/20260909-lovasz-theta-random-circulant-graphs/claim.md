# H-CAT31-1 — claim.md

## Origin

Continuation of the 2026-09-09 scope expansion (ADR-087). Catalog item #31 ("Типичный
Lovász theta number случайных circulant graphs"). Source Trace done properly this time —
full primary text fetched via `mcp__arxiv__download_paper` (not the catalog's paraphrase,
not a WebSearch snippet) on arXiv:2603.29571 (Bandeira, Dmitriev, Lucca, Nizic-Nikolac,
Rodder, "Randomstrasse101: Open Problems of 2025"), Entry 9, Conjecture 18.

**Source Trace (FL Step -4):** real, citable, 2026 publication (ETH Zurich probability
group's stable-reference writeup of their open-problems blog). Formal statement:

> **Conjecture 18.** Let G be distributed as a random dense circulant graph. Then
> E[theta(G)] = (1+o(1)) sqrt(n).

The paper itself states a **partial result already exists** (their own companion paper
BBD+25): a precise lower bound and an upper bound O(sqrt(n log log n)). The gap between
that upper bound and the conjectured tight (1+o(1))sqrt(n) is what remains open. This is
NOT a blank "prove X" problem (which killed #39 on scoping) — there is an existing partial
theoretical envelope this experiment's numbers can be checked against directly.

**Novelty Check (FL Step -3):** grep of `null_results/INDEX.md`, `parked/INDEX.md`,
`pearl_registry/INDEX.md`, `registry/graph.yaml` for "Lovász"/"Lovasz"/"circulant"/"theta
number" returns zero prior matches in this project.

## EstimandOps L0

**Question type:** Descriptive. "For random dense circulant graphs on n vertices, how does
E[theta(G)] scale with n — consistent with the conjectured sqrt(n), or with an extra
log-log factor matching only the paper's own weaker published upper bound?" No causal claim.

## The formal object and why it is cheaply computable (not proof-theoretic like #39)

Circulant graphs are Cayley graphs on Z_n, hence vertex-transitive. For vertex-transitive
graphs, Lovász's own 1979 result gives an EXACT closed form (not a bound) via the
eigenvalues of the adjacency matrix A (degree d = largest eigenvalue lambda_1):

  theta(G) = n * (-lambda_min) / (d - lambda_min)

Because A is circulant, its eigenvalues are exactly the discrete Fourier transform of the
first row (a classical fact, not assumed here) -- computable via `numpy.fft.fft`, no SDP
solver needed. This is a genuinely different computational situation from #39/#43
(existence of a universal algorithm/bound, unfalsifiable by finite search): here the
question is an ASYMPTOTIC SCALING RATE, directly measurable by sampling n across a wide
range and fitting E[theta(G)]/sqrt(n) vs n -- exactly the "measure a number against a
threshold/trend" shape this project's FL methodology is built for.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "theta(G) = n*(-lambda_min)/(d-lambda_min) exactly, for any
vertex-transitive G" -- a specific, checkable claim about a named formula's applicability,
used to justify skipping the much more expensive SDP solve entirely.

**Check:** the paper's own Table 1 independently derives theta(G) for circulant graphs via
FOUR different linear programs (not the eigenvalue ratio-bound formula). Rather than trust
either derivation from memory, `run.py` implements BOTH the eigenvalue formula and the
paper's own "time-domain primal" LP (via `scipy.optimize.linprog`), and cross-validates
them against each other on many random circulant graphs before the eigenvalue formula
(much cheaper, needed for the n up to several hundred this experiment requires) is trusted
for the main sweep. **Result: HOLDS** -- see `tests/` and the positive-control section of
`decision.md` (agreement to LP solver tolerance across all cross-validated instances).

## The claim (falsifiable)

For random dense circulant graphs (edge probability 1/2, symmetric neighbor sampling) at
n in a wide range (small to several hundred vertices, many repetitions per n), fit
`E[theta(G)] / sqrt(n)` as a function of n:

- **CONFIRMED** (consistent with Conjecture 18): the ratio `theta(G)/sqrt(n)` shows no
  systematic growth trend with n over the tested range (flat or converging), OR any
  residual growth is far below the paper's own O(sqrt(log log n)) fallback rate.
- **INCONCLUSIVE_AT_THIS_SCALE**: log(log(n)) grows so slowly that n would need to be
  astronomically large to distinguish the two hypotheses numerically -- if this is
  confirmed analytically before running (see note below), the experiment is reframed to
  report the measured ratio and its trend honestly, not force a binary verdict a finite
  sample cannot support.

## What this does NOT mean

1. Does NOT prove or disprove Conjecture 18 -- no finite numerical sweep can establish an
   asymptotic (n -> infinity) statement. A CONFIRMED verdict here is numerical evidence
   consistent with the tight conjecture over the tested range, not a proof.
2. log(log(n)) is an extremely slowly growing function -- distinguishing "flat" from
   "grows like sqrt(log log n)" numerically may be infeasible at any computationally
   reachable n (log(log(10^6)) ~ 2.6, log(log(10^12)) ~ 3.2 -- the function barely moves
   across enormous ranges of n). This experiment states this limitation explicitly BEFORE
   running, not after finding the numbers don't discriminate well, per this project's own
   Floor-Ceiling / Mechanism Claim Gate discipline (name the limit before, not after).
3. Does NOT investigate Conjecture 17 (the more general Erdos-Renyi G(n,1/2) version) --
   circulant graphs specifically, per catalog item #31's own scope.
