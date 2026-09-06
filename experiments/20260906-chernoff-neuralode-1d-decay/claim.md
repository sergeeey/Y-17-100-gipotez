# claim.md — 20260906-chernoff-neuralode-1d-decay

**Graph node:** `H-B2-1` · **Bridge:** `B2-CHERNOFF-UDE` · **Tier:** Standard (per existing graph scoping)
**Started autonomously** during the user's ~5-6h absence, per their explicit authorization to keep
working ("продолжай автономно выполнять все возможные задания").

## Correction Filed Before This Experiment Began (Gate 1 / Source-Trace discipline)

In this same session, an earlier "⚡ Урок" aside asserted: *"Ilya Chevyrev и Peter Friz формализовали
в 2022-м, что глубокие ResNet-сети — это в точности произведения операторов Чернова для rough
differential equations."* **This claim was checked via `WebSearch` before being used here and could NOT
be verified — no such paper or result was found.** This is treated as a fabricated/hallucinated citation
(the exact failure mode `null_results`/`pearl_registry` already caught twice in this project: Mangal/
GloBI, N_eff≈1.446·ρ̄). It is NOT used anywhere below. See `pearl_registry/INDEX.md` for the incident
entry. The mathematical content of `B2-CHERNOFF-UDE`'s own mechanism (Chernoff's product formula
bounding discrete-operator-product approximations of a C0-semigroup) is real and separately verified
below via a primary source read directly (not a WebSearch summary) — the BRIDGE to Neural-ODE/ResNet is
this project's own original hypothesis, not an existing published result.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | A 1-dimensional linear "ResNet block" `F(h)x = x + h·f(x)`, `f(x) = -x`, iterated `n` times with step `h = T/n`, compared to the analytic solution of `dx/dt = -x`, `x(0) = x0` |
| **Falsifiable predicate** | (a) `F` satisfies the three hypotheses of Chernoff's theorem for the generator `A = -1`; (b) the quantized rate-of-convergence bound from Galkin & Remizov (2021, arXiv:2104.01249, Theorem 1.2 / formula (2)) is an INFORMATIVE (not vacuous, not strictly looser than elementary Taylor analysis) predictor of the true numerical error |
| **Measurable outcome** | Symbolic + numerical comparison of the theorem's guaranteed asymptotic order `o(1/n^{m-1})` against the true empirical error order (estimated via log-log regression over `n`), for both a standard first-order block (`m=1`) and a second-order block (`m=2`) |

## FL Step -4: Source Trace

- **Chernoff's theorem (1968)**, general Banach-space statement: `[VERIFIED]` via primary source, read
  directly (`Read` tool, PDF pages, not `WebFetch` summary — `WebFetch` failed to decompress the PDF
  stream, same failure mode as two earlier papers this session; `Read` on the saved file worked, same
  fix as before). Source: Oleg E. Galkin & Ivan D. Remizov, "Upper and lower estimates for rate of
  convergence in the Chernoff product formula for semigroups of operators", arXiv:2104.01249v2
  (updated 1 Nov 2021), Theorem 1.1 (p.4) — general statement — and Theorem 1.2 (p.5) — the
  "one-dimensional real analog" used directly below.
- **Quantitative rate formula (2)**, p.6: for `s: [0,∞)→R` with `s(t) = Σ_{k=0}^m a^k t^k/k! + o(t^m)`
  as `t→0`, then `s(t/n)^n = e^{ta} + o(1/n^{m-1})` as `n→∞`, for all `t≥0`. `[VERIFIED]` — exact
  quote, transcribed directly from the PDF page image, not paraphrased from memory or a search summary.
- **Neural-ODE ↔ ResNet as an Euler discretization of a continuous dynamical system**: well-established,
  `[VERIFIED]` via `WebSearch` (Chen et al. 2018-style framing confirmed present across multiple
  independent sources: arXiv:2506.03227 "Bridging Neural ODE and ResNet: A Formal Error Bound for
  Safety Verification" 2025, arXiv:2007.15386 "resnet after all? neural odes and their numerical
  solution"). No source found connecting this specifically to Chernoff's product formula by name — the
  bridge itself (Chernoff apparatus applied to Neural-ODE/ResNet error bounds) appears to be genuinely
  novel to this project, not a rediscovery (FL Step -3 novelty check: no hit).

## FL Step -3: Novelty Check

`WebSearch` × 4 (Chevyrev/Friz/Chernoff/RDE; Chernoff+ResNet+operator-semigroup+product-formula;
Neural-ODE+Trotter/Chernoff+error-bound; ResNet+operator-splitting+discretization+convergence-rate) —
no existing paper found connecting Chernoff's product formula specifically to Neural-ODE/ResNet error
analysis. Closest existing work (arXiv:2506.03227, 2025) bounds Neural-ODE↔ResNet error via standard
Lipschitz/Grönwall numerical-ODE arguments, NOT via the Chernoff/Trotter product-formula apparatus. This
bridge is not pseudo-novelty (not a rephrasing of an existing result) — it is this project's own
original test of an analogy, exactly the kind of thing `01-cross-domain-bridges/` exists to check.

## Natural Language Statement

> "We characterize, for a specific 1-dimensional linear ResNet-style block approximating the ODE
> `dx/dt=-x`, whether (a) the block satisfies Chernoff's theorem's hypotheses for the corresponding
> semigroup generator, and (b) whether the one-dimensional quantitative Chernoff-rate theorem (Galkin &
> Remizov 2021) gives a convergence-rate estimate that is at least as tight as the true empirical error,
> for both a standard first-order (plain Euler) block and a second-order (Taylor-truncated) block."

## L0 Classification

**Descriptive** — this characterizes the actual behavior of a specific, fully-specified numerical
scheme against a known analytical ground truth (the exact solution `x0*e^{-T}`) and a specific published
theorem's guarantee. No population is sampled, no causal claim is made, no out-of-sample prediction.

## What This Does NOT Mean

1. Does NOT test any real, trained neural network — the "ResNet block" here is a hand-specified,
   analytically tractable linear toy (`f(x)=-x`), chosen so the true solution and every quantity are
   exactly computable, per the pre-registered kill criterion ("1D Neural ODE with analytic solution").
2. Does NOT prove or disprove that operator-semigroup theory COULD ever say something useful about
   Neural-ODE/ResNet error bounds in general — only that this ONE specific, correctly-cited, quantitative
   Chernoff-rate theorem, applied to this ONE tractable case, either is or is not more informative than
   elementary calculus.
3. A KILL verdict here is a kill of THIS bridge's practical value as scoped (kill_criterion b in
   `registry/graph.yaml`), not a claim that Chernoff's theorem itself is wrong — Chernoff's theorem is a
   real, correctly-verified, general result; the question is whether its know quantitative refinement is
   USEFUL here, not whether it is TRUE.

## MCID

The bound is "informative" (PASS-worthy) if its guaranteed order `o(1/n^{m-1})` matches or exceeds the
true empirical order in a log-log regression (slope comparison, tolerance ±0.15 in slope — enough to
distinguish order 1 from order 2 unambiguously but not overly strict about small-sample regression
noise). If the true empirical order is strictly better (larger magnitude negative slope) than what the
theorem guarantees, by more than this tolerance, the bound is "loose/non-informative" for this case.
