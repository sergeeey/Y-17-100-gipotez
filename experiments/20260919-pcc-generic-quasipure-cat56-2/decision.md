# H-CAT56-2 — decision.md

## Verdict

**COUNTEREXAMPLE-CERTIFIED** (conditional on Observation 2 / Theorem 1 of Yang-Imai-Pezze
arXiv:2601.21801 as published, `[DOCS]`) **plus a proven structural result** that replaces
H-CAT56-1's "ceiling" conjecture: **STRUCTURAL-CEILING-PROVEN in the opposite direction** — the
ceiling does *not* stay below the certification level for all `r^2 + 1 < d`; it does for
`r = 2, d <= 21` and `r = 3, d <= 22`, and it fails from `d = 22` (`r = 2`) / `d = 23` (`r = 3`).

Blunt statement: for generic quasi-pure states (Yang Eq. 12, not Eq. 16) with PCC true and a
full-rank QFIM, states with a certified `dim V_perp < d` **exist**, e.g. `d = 22, r = 2, k = 20,
s = 16`, `dim V_perp = 21 < 22`. By Observation 2 such a state cannot have its QCRB saturated,
so **PCC is not sufficient for generic quasi-pure states**, contradicting the conjecture the
source paper calls open. This is a pilot-found result (registration note in `claim.md`): it was
not a blind pre-registered prediction, and it is re-verified below by four independent routes.
The `[UNVERIFIED]` weak point is not the arithmetic but the dependence on the published
Observation 2 (see "What this does NOT mean").

## Headline number, four independent routes (`d = 22, r = 2, s = 16`, seed 20260919)

| route | code path | `dim V` | `dim V_perp` | file |
|---|---|---|---|---|
| reduced block pipeline (float64, tolerance sweep 1e-5..1e-12, flat) | `h2_core.ranks` | 463 (M 64 + W 399) | **21** | `metrics/verify_candidate.json` |
| full `d x d` H-CAT56-1 pipeline (`pcc_core.analyse`: Lyapunov-formula SLD from `rho, d rho`, own W/M builder, own PCC), plain and random-unitary basis | `pcc_core.analyse` | 463 / 463 | 21 / 21, `pcc_holds` true, `rank_is_robust` true, QFIM rank 16 | same |
| structural identity `r^2 + dim P + dim Q` from independent nullspaces | `h2_ext.dim_p/dim_q` | — | 4 + 16 + 1 = **21** | same |
| **exact arithmetic in F_p[i]** (two primes p = 67108837, 67108777), all objects built from the FULL `d x d` definitions, SLD Lyapunov and PCC exactly 0, QFIM determinant non-zero mod p | `fp_certify.py` | `rank_mod_p` = 463 = `d^2-d+1` (both primes) | 21 | `metrics/fp_certify_d22_r2_s16.json` |

Second config `d = 23, r = 3, s = 12`: reduced 507, full pipeline 507, identity 9+12+1 = 22, F_p
507 (need 507) -> `dim V_perp = 22 < 23` (`verify_candidate.json`, `fp_certify_d23_r3_s12.json`).
Singular-value gap: M-block dropped part exactly 0, W-block gap 4.9e13 (`d=22`) and 1.2e14
(`d=23`). Certificates are **exactly at the threshold** (`dim V = d^2 - d + 1`): the margin is one
dimension, which is why the exact check mattered.

Random sampling of the PCC variety, `N = 40` each (`extended.json`): `dim V_perp` equals
`r^2 + s + 1` in every sample; certified robust firing at all five firing configs
`(22,2,16) (23,2,17) (24,2,18) (23,3,12) (24,3,13)`: **200/200** samples (PCC true, QFIM
full-rank, rank robust); `n_below_LB = 0`.

## What was proven (elementary linear algebra; then verified numerically)

Setup (from H-CAT56-1 S1-S3, verified there and again here by the full pipeline): support/kernel
basis, `L_i = [[0, A_i^dag],[A_i, 0]]`, `A_i` complex `k x r`; PCC <=> `A_i^dag A_j` Hermitian.

* **C-ID (exact).** `V_perp = Herm(r) (+) P (+) Q` with
  `P = {Y in C^{k x r}: A_i^dag Y Hermitian for all i}` and
  `Q = {Z in Herm(k): A_i^dag Z A_j Hermitian for i != j}`. Proof: `iM` has only support-kernel
  blocks, `iW` only kernel-kernel blocks, none has a support-support block. `Y perp i A_i S` for all
  Hermitian `S` iff `herm(i Y^dag A_i) = 0` iff `A_i^dag Y` Hermitian. `Z perp i W_{ij,S}` iff
  `Im Tr(S A_j^dag Z A_i) = 0` for all Hermitian `S` iff `A_j^dag Z A_i` Hermitian. Hence
  `dim V_perp = r^2 + dim P + dim Q` exactly. Verified: **234/234** robust samples over
  `r in {2,3}, k = 2..12/9, s = 2..11` (`metrics/theory.json`, 0 failures); also equal on all
  200+ samples of `verify_candidate.json` / `extended.json`.
* **C-LB (rigorous lower bound, rank-nullity).** Every `A_j` lies in `P` and, with full-rank QFIM
  (a Gram matrix of the `A_j` in a positive-weighted real inner product), they are real-independent:
  `dim P >= s`. The map `Y -> (A_i^dag Y - h.c.)_i` goes from `R^{2kr}` to `R^{s r^2}`: `dim P >=
  2kr - s r^2`. `I in Q` (that is PCC): `dim Q >= 1`; `Z -> (A_i^dag Z A_j - h.c.)_{i<j}` goes from
  `R^{k^2}` to `R^{C(s,2) r^2}`: `dim Q >= k^2 - C(s,2) r^2`. So
  `dim V_perp >= LB(k,r,s) = r^2 + max(s, 2kr - s r^2) + max(1, k^2 - C(s,2) r^2)`.
  No sample anywhere violates it (`n_below_LB = 0` in every run; 234 theory samples).
* **C-CEIL (consequence, computed by exhaustive `s <= 2kr` in `theory.json`).**
  `min_s LB < d` first happens at `d = 22 (r=2)`, `23 (r=3)`, `31 (r=4)`, `41 (r=5)`.
  Therefore **for `r = 2, d <= 21` and `r = 3, d <= 22` no quasi-pure PCC state can ever have a
  certified `dim V_perp < d`** — a theorem for those sizes, not a search statement — and
  H-CAT56-1's observed maxima at d = 7, 8 (40, 54) are explained: they equal
  `d^2 - (r^2 + s* + 1)` with `s*` the largest non-degenerate `s`; d = 6 (24) is the small-`k`
  exception noted below.
* **Why H-CAT56-1's ceiling `2rk + k^2 - 1` was the wrong obstruction.** The true `V_M` ceiling is
  `2kr - dim P <= 2kr - s`: every `A_j` itself is orthogonal to `V_M` (the extra dependency H-CAT56-1
  could not find, its Relaxation Map V2). It costs exactly `s` dimensions, and QFIM full rank forces
  `s` large enough that `2kr - s r^2` stops helping; the two constraints cross at
  `s ~ 2kr/(r^2+1)`, which is where `LB` is minimal and where the sampler sits (`s*`). The closed
  form of the measured value is `dim V_perp = r^2 + s* + 1` with
  `s* = ceil(2kr/(r^2+1))` (from the sequential-kernel count `(s-1)(r^2+1) < 2kr`), matched in
  every sampled config with `k >= 5` (`r = 2`: d = 7..25; `r = 3`: d = 10, 11, 23..29; pilot
  output, and `random.json` / `extended.json`); for `d = 6` (`k = 4`) extra dependence in `Q`
  appears (`dim V_perp = 12 > LB = 9`), `[measured, not proven tight]`.

## Results at the required configurations (`random.json`, `N = 200`, seed 20260919)

| `d, r, s` | `r^2+1<d` | PCC true | QFIM full | robust | max `dim V` | need | min `dim V_perp` | LB | fires |
|---|---|---|---|---|---|---|---|---|---|
| 6, 2, 4 | yes | 200 | 200 | 200 | 24 | 31 | 12 | 9 | 0 |
| 7, 2, 4 | yes | 200 | 200 | 198 | 40 | 43 | 9 | 9 | 0 |
| 8, 2, 5 | yes | 200 | 200 | 200 | 54 | 57 | 10 | 10 | 0 |
| 10, 3, 5 | **no (10 = d)** | 200 | 200 | 200 | 85 | 91 | 15 | 15 | 0 |
| 11, 3, 5 | yes | 200 | 200 | 200 | 106 | 111 | 15 | 15 | 0 |

`(7,2)`: 2 of 200 samples were not tolerance-flat/gapped ("not robust") and are excluded from any
verdict; none of the 198 robust ones fires. This reproduces H-CAT56-1's 24/40/54 exactly.
Verdict at these configs, and the only wording licensed: **no certified counterexample found
under this sampler** — and additionally **none can exist** for `r = 2, d <= 21` (C-CEIL). At
`(10,3)` the `r^2 + 1 < d` condition is false, so the arithmetic control behaved as required.

Structured starts (`structured.json`, `N = 100` per start x 4 start types x 5 configs; starts:
rank-1, real, sparse, Eq.-(16)-like block-diagonal `A_1`; `s` also raised by +2/+4 where the
QFIM allowed): max QFIM rank reached 4/5/5/5/6 at d = 6/7/8/10/11 (a non-generic start at
`(11,3)` admitted `s = 6`); `min dim V_perp - LB = 0` (generic value attained, never below);
`n_below_LB = 0`, robust fires 0. Adaptive optimisation: see the section below.

## Controls (`controls.json`, `verify_candidate.json`)

| control | result |
|---|---|
| positive: rank-detector injection, float route, `d = 4, 6, 8, 12, 22`, 40 each | fires 40/40 at `rank = d^2-d+1`, **0/40** at `d^2-d` |
| positive: exact F_p arm, injected integer stack at `d = 6` | rank 31 -> fires; rank 30 -> does not |
| positive: exact machinery on a known non-firing state (`exact_certify.py`, `d=8,r=2,s=5`) | exact PCC, exact Lyapunov, exact QFIM det, `rank_mod_p = 54 =` float `dim V` |
| negative: Eq. (16) class (theorem: saturable), `d = 8, 12, 22` (`s = 3, 3, 4`), 20 each | PCC true 60/60, min `dim V_perp` 40 / 120 / 444 (all `>= d`), fires **0/60** |
| negative: random blocks (no PCC) | PCC true 0/200, min violation 6.9e-2 |
| negative: generic PCC, `d = 22`, `s = 4, 10` (LB >= d) | `dim V_perp` 444 / 264 in 40/40 each, fires 0 |

Limitation of the Eq. (16) control: at `d = 22` only `s = 4` was sampled (the least-squares
Eq.-(16) sampler at larger `s` was not run); the control therefore shows the harness does not
fire on a theorem-saturable class, not that Eq. (16) never fires at `s = 16`.

## Rank-Certificate Gate

1. Spectrum logged, gap: M-block dropped singular values exactly 0; W-block gap 4.9e13 / 1.2e14
   (`verify_candidate.json`). 2. High precision: not mpmath here; replaced by exact F_p (point 5).
3. Threshold sweep 1e-5..1e-12 flat and gapped on all 280 extended samples (`robust` = 40/40 per config); Gram-eigenvalue route
   agrees (after fixing my own Gram tolerance, see defects). 4. Independent reconstruction: the
   full `d x d` H-CAT56-1 pipeline (different SLD solver, different W/M builder) gives the same `dim V`
   in two bases. 5. Exact: **not a Q(i) point** — see next section.

## Substrate Gate (FL Step 2a): **READY**

Environment: Python 3.13.2, numpy 2.3.4, scipy 1.16.3, sympy 1.14.0; single BLAS thread; cores
16-23, BELOW_NORMAL (recorded in every JSON `resources`). Code provenance: SLD/PCC/W/M builder is
H-CAT56-1's `pcc_core` (reviewer-passed there, substrate-checked against closed forms), reused by
import. My reduced pipeline is tested against it (agreement of `dim V`: 463=463 and 507=507 on the
firing states; 24/40/54 = H-CAT56-1's separately measured maxima at d = 6/7/8). Artifacts persisted
to `metrics/`, files written atomically (tmp + replace); all 14 JSON files in metrics/ re-parsed complete.
One rank-detector control and the exact machinery both pass on states with known answers.

### Exactness: what I could NOT do

An explicit Gaussian-rational point was not produced for the firing states: the sequential exact
kernel construction has exponentially growing entries (no-LLL run at `d=22, s=16` killed after ~30 min;
`sympy` LLL raised `AssertionError`; `metrics/exact_qi_construction_attempt.json`, timings are
observations, not script measurements). In its place: (a) exact arithmetic in `F_p[i]` (all checks
above), (b) the check that the F_p kernel dimension at **every** stage equals the generic char-0
kernel dimension of the float sampler (`80,76,...,20` for `d=22`; `120,111,...,21` for `d=23`;
`kernel_dims_equal_float_generic` true for both primes and both configs), and (c) a **lifting
argument stated as a derivation, not machine-checked** (`fp_certify.py` docstring): the tower of
linear kernels is an open subscheme of an affine space over `Z_(p)`, the QFIM determinant and a
`(d^2-d+1)`-minor of the `iW/iM` stack are polynomials on it that are non-zero mod p, hence non-zero
over Q, hence Q(i)-points with `dim V >= d^2-d+1` exist (rank over F_p can only drop). Status of the
exact claim: `[DERIVED]`, not `[VERIFIED]`; the float+full-pipeline+F_p evidence is `[VERIFIED-REAL]`
on the sampled states.

## Adaptive search (pre-registered strategy S-C) and how it went

Final run (`metrics/adaptive.json`, v3 = `trust-constr`, PCC as equality constraints, random and
block-diagonal starts, **reduced budget: 4/4/3/2/2 restarts, `maxiter` 120**, 1284 s):

| `d, r, s` | runs | surrogate start -> end | max `dim V` reached | need | valid (PCC<1e-9, QFIM full, robust) | valid below LB | valid fires |
|---|---|---|---|---|---|---|---|
| 6, 2, 4 | 4 | 7.1-8.2 -> 9.6-9.7 | 24 | 31 | 4 | 0 | 0 |
| 7, 2, 4 | 4 | 9.2-9.9 -> 10.985-10.986 | 40 | 43 | 4 | 0 | 0 |
| 8, 2, 5 | 3 | 10.7-11.2 -> 12.7-12.8 | 54 | 57 | 3 | 0 | 0 |
| 10, 3, 5 | 2 | 17.4-18.4 -> 20.6 | 91 (**invalid**) | 91 | 1 | 0 | 0 |
| 11, 3, 5 | 2 | 18.9-19.7 -> 22.0 | 106 | 111 | 2 | 0 | 0 |

The optimiser did raise the surrogate everywhere (so this time the search actually moved), yet the
valid `dim V` stayed at the generic value (24/40/54/85/106) — consistent with C-LB, which forbids
more. **One instructive artefact:** at `(10,3,5)` one run returned `dim V = 91`, i.e. `dim V_perp = 9
< d = 10`, an apparent "certified firing" **at the arithmetic control configuration where firing is
impossible**. Its PCC residual after optimisation was 1.2e-5 (relative), far above the 1e-9
pre-registered tolerance; the optimiser had bought rank by leaving the PCC variety. It is
excluded by the validity conditions — exactly the trap the pre-registered "PCC true" clause exists
for. It is the only run in the whole experiment that appeared to fire outside the LB region, and it
does not count (reported, not hidden). Two strategies (S-B structured starts, S-C surrogate
optimisation) produced no new maximum: stop rule applied.

## No-collapse tests (all 7)

| test | what changed | result |
|---|---|---|
| Data swap | seeds 20260919/20/21/22/23/24; two independent F_p primes and F_p seeds | PASS, `dim V_perp` identical (21 at d=22; 22 at d=23) |
| Noise injection | rank tolerance 1e-5..1e-12 | PASS flat; PCC residual 1e-16 relative |
| Scale variation | `d` 6..24, `r` 2,3, `s` 2..18 | PASS: firing exactly where `LB < d`; `d = 22` fires (`s`=16), `s`=4/10 does not |
| Convention flip | random unitary basis; alternate `q` weights; different rank routes | PASS (463=463) |
| Negative control | Eq. (16), random non-PCC, small `s` | PASS |
| Adversarial | Eq.-(16)-like block-diagonal and rank-1/real/sparse `A_1` starts | PASS: never below LB; QFIM rank 6 reached at (11,3) from a rank-1 start (a non-generic branch admits more `s`); minimum `V_perp - LB` over that row's samples = 3 |
| Alternative tool | reduced vs full `pcc_core` vs nullspace identity vs F_p exact | PASS, four routes agree |

## Kill Analysis

**Killed:** (i) H-CAT56-1's conjecture that the `{W,M}` ceiling keeps the no-go from firing for all
`r^2 + 1 < d` — refuted at `d >= 22`; (ii) "PCC is sufficient for generic quasi-pure states" —
refuted (conditional on Observation 2), at `(22,2,16)`, `(23,3,12)` and 200/200 samples of five
firing configs; (iii) the `2rk + k^2 - 1` ceiling as the operative obstruction (it is
`2kr - dim P`, costing `s`).

**NOT killed:** Observation 2 / Theorem 1 themselves (inherited); sufficiency of PCC for `d <= 21`
(`r=2`), `<= 22` (`r=3`) — there the certified test cannot fire, so the conjecture stays open for
those sizes: it is not confirmed, merely not refutable by this route (`dim V_perp >= d` never proves
saturability); saturability of any state with `dim V_perp >= d` is untouched; states with
`lambda`-dependent spectrum; the Eq. (16) class (paper's theorem stands, control passes).

**Relaxation Map (one assumption each, separate experiments):**
* R1 — check the paper's own Observation 2 statement/proof in the LaTeX and independently confirm
  non-saturability at the certified state by an unrelated method (e.g. certified optimisation of the
  classical-Fisher gap over POVMs at `d=22` is infeasible; a smaller analogue via the identity
  `V_perp = Herm(r) + P + Q` at exotic `(r, k, s)` outside the LB region is impossible, so the
  independent check must be theoretical).
* R2 — raise `r` (4, 5): LB says first firing at `d = 31, 41`; test with the F_p pipeline.
* R3 — the `d <= 21` region: `dim V_perp >= d` proves nothing; V3 of H-CAT56-1 (a global certificate
  of saturability, e.g. SOS/Lasserre) is the remaining route.
* R4 — non-generic branches with `dim Q > 1` / `dim P > s` are irrelevant to firing (they only raise
  `dim V_perp`).

## Resource use (post-registration caps)

Order received mid-run: <=3 processes, cores 16-23, BELOW_NORMAL, 1 BLAS thread, <2 GB/process.
Applied via `caps.py` (imported first in every script; recorded per JSON). At most 3 of my worker
processes ran concurrently (a stray exact-arithmetic job was killed). **Measured peak working set per
process: 72-116 MB** (max 116.3 MB in `controls.json`, 113.6 MB in `verify_candidate.json`); worst-case
total for 3 concurrent processes < 0.4 GB, far below 2 GB / 8 GB. No `N` was reduced for resource
reasons **except the adaptive search** (labelled below). Everything else ran at its registered N.

## Post-registration changes (all labelled)

1. Pilot preceded registration (claim.md note).
2. Adaptive surrogate: v1 used the T-th singular value (zero gradient) -> SLSQP never moved
   (`adaptive_v1_inert_surrogate.json`, start value = end value in all 48 runs); v2 = sum of top-T
   singular values, SLSQP aborted with "Singular matrix C in LSQ subproblem" from redundant PCC rows
   (`adaptive_v2_slsqp_singular_jacobian.json`, same start=end); v3 = `trust-constr`, and
   (resource/time, post-registration) restarts reduced from 12/12/12/6/6 to 4/4/3/2/2 and
   `maxiter` 300 -> 120 because `trust-constr` with finite-difference Jacobians did not finish the
   registered budget in >30 min.
3. My Gram-eigenvalue rank tolerance in `verify_candidate.py` first used `(1e-9*scale)^2`, below the
   float64 eigenvalue noise floor, and disagreed with the SVD rank (`gram_agrees` False) purely from
   round-off — the same defect family as H-CAT56-1's defect 3 (thresholds relative to noise);
   corrected to `1e-12 * top eigenvalue`. The reported certificate never depended on it (SVD route,
   full pipeline, F_p rank were unaffected).
4. First `controls` run had two bugs of mine: detector direction inverted ("fires at `d^2-d+5`"
   counted as failure) and an injected-stack builder that regenerated its random coefficients inside
   a comprehension (rank came out 36, not 31). Both fixed before any result was used; the fixed
   run is the one in `controls.json`.
5. `h2_core.load_old` had to register the imported H-CAT56-1 module in `sys.modules` before
   `exec_module` (a `@dataclass` in an importlib-by-path module otherwise crashes).

## What this does NOT mean

1. It is not a proof that PCC fails to be sufficient, independent of the source paper: it inherits
   Observation 2 (linear-independence step re-derived by me in prose: `d` rank-one projectors of
   linearly independent vectors are linearly independent; but Theorem 1's "saturation <=> all POVM
   vectors are hollow for all `W, M`" is `[DOCS]`, not re-proved here).
2. It says nothing about `r = 2, d <= 21` / `r = 3, d <= 22`, where the conjecture is neither
   confirmed nor refuted.
3. `s = 16` parameters on `d = 22` is far from any standard multiparameter metrology setup; the
   result is about a mathematical class, not about experiments.
4. No explicit rational state was built; existence of one rests on the F_p lifting derivation.
5. The rank-nullity bound `LB` is a lower bound valid for all PCC quasi-pure states with
   independent `A_j`; tightness (`= r^2+s+1`) was only measured, at the sampled `(k, s)`.
6. Adaptive-search null results (below) are not evidence about states off the sampled/optimised set;
   at the required configs nothing further is needed since C-CEIL already excludes firing.

## Claim Entropy

| component | start | now | note |
|---|---|---|---|
| unsupported HIGH claims | 0 | 0 | exact claim marked `[DERIVED]` |
| hidden assumptions | 2 | 1 | constant-spectrum family still assumed; Observation 2 stays inherited but is now named in the verdict |
| missing negative controls | 0 | 0 | |
| ambiguous definitions | 0 | 0 | |
| unresolved blockers | 0 | 1 | independent confirmation of Observation 2 (R1) |
| **total** | **2** | **2** | did not decrease: one hidden assumption made explicit, one blocker uncovered |

## Pearl Gate (proposals; nothing written to pearl_registry, per instructions)

| field | value |
|---|---|
| observation | For generic quasi-pure states with PCC, `dim V_perp = r^2 + dim P + dim Q` exactly, with `P` = solutions of `A_i^dag Y` Hermitian, `Q` = solutions of `A_i^dag Z A_j` Hermitian. Every `A_j` is orthogonal to `V_M`: the QFIM-nondegeneracy itself eats `s` dimensions of `V`. |
| falsifiable prediction | At `r = 4, s = s*`, the F_p pipeline fires first at `d = 31` and not at `d = 30` (`theory.json`); any PCC state with `dim V_perp < LB` falsifies the bound. |
| impact_score | 7 |
| next_check | 2026-11-15 |

## Reuse notes (H-CAT56-1)

Imported by path: `pcc_core.analyse`, `pcc_core.Model`, `pcc_core.herm`, `pcc_core.random_unitary`,
`pcc_core.sample_bipartite_quasipure` (Eq. 16 negative control). Not modified. Bugs/quirks found in
the old folder: none affecting results. Interface note: importing it by path needs
`sys.modules` registration (my `load_old`). Its S4 "ceiling `2rk + k^2 - 1`" is a valid but
non-sharp bound (the sharp statement is C-ID/C-LB); its remark that "certified test could not fire
at any size tested" remains true for `d <= 8, r <= 3`, now with a proof for `d <= 21 / 22`.
Contradiction with H-CAT56-1's decision.md: only its "What this does NOT mean #4" ("does not
establish that `dim V` cannot reach `d^2-d+1`") is settled here — it *can*, from `d = 22`.

## Orchestrator's independent verification (added 2026-09-19, after the agent finished)

Per the project's rule that an agent's `[VERIFIED]` is the orchestrator's `[INFERRED]`, the
headline was re-checked before it entered the registry. Two independent things:

1. **The necessity argument behind Observation 2 was re-derived from scratch** (not taken from the
   paper). Classical FIM equals QFIM iff, for every outcome `omega`, `(L_i - c_i)|omega>` lies in
   `ker rho` with real `c_i` (write `Q - F = sum_omega` of a Gram matrix of the components of
   `sqrt(rho) L_i |omega>` orthogonal, in the real inner product, to `sqrt(rho)|omega>`). From that,
   `<omega| iM_{i,ab} |omega> = 0` and `<omega| iW_{ij,ab} |omega> = 0` for every rank-one outcome,
   so every saturating rank-one POVM element lies in `V_perp`; the elements sum to `I`, so their
   vectors span `C^d`, and `d` linearly independent rank-one projectors are real-linearly
   independent, hence `dim V_perp >= d`. Rank-one refinement of a saturating POVM still saturates
   (a refinement cannot lower the Fisher information, which is capped by the QFIM). So
   `dim V_perp < d` really does forbid saturation: the counterexample does not rest on trusting the
   preprint. Consistency check: for pure states (`r = 1`) the lower bound C-LB, minimised over every `s`
   from 1 to `2k`, stays above `d` (e.g. 5 at `d = 3`, 31 at `d = 21`, 60 at `d = 41`, computed
   directly), so the test never fires for pure states, in line with Matsumoto's sufficiency of
   weak commutativity. (An earlier draft of this sentence said "`>= 2d`"; that was wrong, the
   minimum over `s` is smaller, and only the "never fires" conclusion was checked and kept.)
2. **The headline number was recomputed by new code** (`orchestrator_independent_check.py`,
   `metrics/orchestrator_independent_check.json`) that shares nothing with `h2_core.py`,
   `pcc_core.py` or `fp_certify.py`: full `22 x 22` matrices, `rho` and `d rho` built first, the SLD
   solved from `d rho = (rho L + L rho)/2` in the eigenbasis, PCC checked on the full commutators
   `Pi_r [L_i, L_j] Pi_r`, `V` built from the paper's own `sigma` operators, a different RNG and
   sampler, and a random unitary change of basis. Results (4 runs = 2 seeds x plain/rotated):
   `d = 22, r = 2, s = 16`: `dim V = 463`, `dim V_perp = 21 < 22` in **4/4**, identical under
   tolerances 1e-6 to 1e-12, singular-value gap between 6.5e11 and 4.9e12, PCC residual <= 2.0e-14,
   QFIM full rank. Controls behave as predicted: `d = 21` (`s = 16`) gives `dim V_perp = 21 = d`,
   no firing; `d = 22, s = 8` gives 340, no firing; `d = 20, s = 14` gives 21, no firing;
   `d = 23, r = 2, s = 17` gives 22 < 23, firing.

What this does **not** establish: exactness over `Q(i)` (still the F_p route plus a lifting
argument, `[DERIVED]`), and novelty. A keyword scan of arXiv:2601.21801, 2405.00405 and 2602.12097
found no prior counterexample for quasi-pure states, but that is `[WEAK]`, not a literature review.
The regime is also specific: many parameters relative to the dimension (`s = 16` in `d = 22`);
sufficiency at smaller `d` and smaller `s` remains open, because the certified route cannot fire
there (C-CEIL).

## Files

`claim.md`, `controls.md` (registered), `orchestrator_independent_check.py` (added, see above), `caps.py`, `h2_core.py` (reduced pipeline, sequential
sampler), `h2_ext.py` (`dim P/Q`, LB, full model), `h2_main.py` (modes: random, extended,
structured, adaptive, controls, theory), `verify_candidate.py`, `exact_certify.py`, `fp_certify.py`,
`pilot_scratch*.py` (throw-away pilot), `candidates/` (saved float blocks `.npz` for both firing
states, plus `exact_blocks_d8...json`), `metrics/*.json`. All Python `ruff`-clean.
