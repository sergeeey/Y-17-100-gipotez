# H-CAT56-1 — decision.md

## Verdict

**REPEAT**, with the pre-registered claim **not tested as written**, and four substantive
results attached.

Blunt statement first. The pre-registered question was whether a counterexample to "PCC is
sufficient for quasi-pure states" exists below the Eq. (15) threshold, with the search
space specified as states of **Eq. (16)** of the source paper. Reading the primary LaTeX
source found that the paper's own End Matter **proves sufficiency for exactly that class**,
unconditionally, with no reference to the Eq. (15) threshold. The question the paper leaves
open is about *generic* quasi-pure states — a strictly larger class, defined in a different
paper. The pre-registered search space and the open question are two different objects that
share a name.

This is not a failed search. It is a **Gate-1 artifact-identity miss**
(`artifact-provenance-gates.md`): a verdict about object A was on its way to being reported
as a verdict about object B.

The four results worth keeping, none of them the pre-registered claim:

1. **The artifact-identity correction itself** (C3), with the mechanism separating the two
   classes derived and verified (C4): PCC is `B_i†B_j` Hermitian in general, but its
   `a ≠ b` half is vacuous for Eq. (16).
2. **A structural bound** — `dim 𝒱_⊥ ≥ r² + 1` for any quasi-pure state satisfying PCC — so
   the certified test can only ever fire when `r² + 1 < d`, which is false at the
   pre-registered primary configuration.
3. **A measured demonstration that a failed non-convex search is not a certificate**: 0/8
   where a theorem guarantees success, unchanged at 16× budget, against 3/3 with LP slack
   exactly 0 once the search is restricted to the right structural branch.
4. **A forced QFIM degeneracy** at `k = d − r = 1` for generic quasi-pure states (rank-1
   QFIM in 200/200), absent from the Eq. (16) class — the same mechanism as (1) surfacing
   in a second observable.

No `BLOCKED-INFRASTRUCTURE` component. The Substrate Gate returned `READY` on all six
checks, and every number below was reproduced along at least one independent path —
including exact rational arithmetic.

---

## Step 0 — what the primary source says, and where the briefing was wrong

Read as **LaTeX e-print** (`arxiv.org/e-print/2601.21801` → `main-final.tex`, 76 079
characters), not HTML, not a summary. Jing Yang, Satoya Imai, Luca Pezzè, *A geometric
criterion for optimal measurements in multiparameter quantum metrology*.

Five corrections; four are load-bearing.

### C1 — `n` is not a function of `(d, s)`

The briefing asked me to pin down the correspondence `n` ↔ `(d,s)`. There is none. The
paper defines `n = dim 𝒱_⊥ − 1 ≤ d² − 1`, with
`𝒱 ≡ span_ℝ{i W^(α)_{ij,ab}, i M^(α)_{i,ab}}`. So `n = d² − 1 − dim 𝒱`, and `dim 𝒱` is a
property of the individual state that must be **measured** by a rank computation; it is
only bounded above by `s(s+1)r²/2`. "A `(d,s)` pair below the threshold" is therefore not a
well-formed specification, and it also silently omits the **rank `r`**. `threshold_scan.py`
measures the status instead of assuming it.

### C2 — `|ψ_{a,Δ}⟩` and `|φ_{a,Δ}⟩` are different objects

They are, and the difference is the entire mechanism. In Eq. (16) the state lives on
primary ⊗ ancilla; the eigenvectors of `ρ_Δ` are `|ψ_{a,Δ}⟩ = |φ_{a,Δ}⟩ ⊗ |a⟩`, while
`|φ_{a,Δ}⟩` is the primary-system factor alone. PCC (Eq. 8) is stated in `|ψ⟩`; Eq. (17) is
its reduction in `|φ⟩`.

### C3 — the paper PROVES sufficiency for the pre-registered class

End Matter, "Proof of the results on quasi-pure states". For Eq. (16) states
`L_i = Σ_a L_{i,a} ⊗ |a⟩⟨a|`, hence `W_{ij,ab} = 𝒲_{ij,ab} ⊗ |a⟩⟨b|` and
`M_{i,ab} = ℳ_{i,ab} ⊗ |a⟩⟨b|`. Against the LMCC basis `|π_{ν,a}⟩ = |e^(a)_ν⟩ ⊗ |a⟩`,

    ⟨π_{ν,a}|W_{ij,cd}|π_{ν,a}⟩ = ⟨e^(a)_ν|𝒲_{ij,cd}|e^(a)_ν⟩ δ_{ac} δ_{ad},

so **every `a ≠ b` condition is annihilated by the ancilla factor** and only the diagonal
`a = a` conditions survive — which are exactly the single-pure-state optimal-measurement
conditions for `|φ_{a,Δ}⟩`, constructible by Matsumoto (2002) / Pezzè et al. (2017). The
main text then says, in the same paragraph:

> "for generic quasi-pure states, whether PCC is sufficient or not is still open"

**Generic**, not Eq. (16). Eq. (16) is introduced as "this class of quasi-pure states
generated via the classical correlations between a primary system and an ancilla" — a
sufficient engineering recipe, not the definition.

The definition is in Yang, arXiv:2405.00405 (fetched and read directly, Eq. 12): `ρ(x)` is
quasi-pure iff `Π_r ∂_x ρ Π_r = 0`. Eq. (16) is that paper's own Figure-3 "universal
protocol to create the quasi-pure structure ... using classical correlations with ancillary
systems" — one construction inside the class.

**Consequence:** the pre-registered search ran in a space where a counterexample is
excluded by a theorem. Zero counterexamples there is the *predicted* outcome — a control on
the harness, not evidence about the conjecture.

### C4 — the mechanism, derived and verified numerically

With `B_i ≡ Π_k G_i Π_r` the kernel–support block of the `i`-th generator:

| class | PCC is equivalent to |
|---|---|
| generic quasi-pure | `B_i† B_j` **Hermitian** for every `i ≠ j` — `r²` real conditions per pair, **including `a ≠ b`** |
| Eq. (16) bipartite | only the `a = a` conditions, `Im⟨D_iφ_a\|D_jφ_a⟩ = 0`; the `a ≠ b` ones hold automatically because `B_i` is ancilla-block-diagonal |

That one difference is what makes one class provable and the other open. It also produces a
second, independently observable consequence (the QFIM collapse at `k = 1`, below).

### C5 — a factor-2 slip in the paper (cosmetic, recorded not absorbed)

End Matter writes `𝒲_{ij,ab} = 2(|D_iφ_a⟩⟨D_jφ_b| − |D_jφ_a⟩⟨D_iφ_b|)`. With the paper's
own `L_{i,a} = 2(|D_iφ_a⟩⟨φ_a| + h.c.)`, so `L_{i,a}|φ_a⟩ = 2|D_iφ_a⟩`, the definition
`𝒲 = L_{i,a}|φ_a⟩⟨φ_b|L_{j,b} − (i↔j)` gives **4**, not 2. Numerically irrelevant (every
condition is homogeneous `= 0`).

---

## Protocol corrections received mid-run — both adopted, both then measured

Two corrections arrived from the coordinator while the experiment was running. Both are
correct, and in both cases this experiment produced the measurement that proves the point.

### Correction 1 — only the exact rank test may certify a negative

A counterexample may be claimed **only** from Observation 2 (`dim 𝒱_⊥ < d ⟹ the QCRB
cannot be saturated`), never from a failed optimiser search, because "the search did not
converge" and "no such measurement exists" are different facts.

That correction arrived **after** my first positive-control run had already produced the
failure it warns about. See § "the measurement" below.

### Correction 2 — a second exact certificate (completeness feasibility)

The paper's End Matter algorithm: find admissible `v^(ω)`, then look for `α^(ω) ≥ 0` with
`Σ α^(ω) = d` and `Σ α^(ω) v^(ω) = 0`; *"If such {α^(ω)} does not exist, then the QCRB is
not saturable."* Implemented as **test 2** (`pcc_sat.alpha_feasibility`) and run on every
sample where test 1 did not fire.

**A caveat I must report rather than bury, because the positive control measured it.** The
statement is exact for the *complete* set of admissible `v`. The LP half is genuinely exact
— HiGHS returns feasible/infeasible, not "did not converge". But the *enumeration* of
admissible `v` is the paper's algorithm step 1, and it is non-convex: the admissible `v`
form a variety of dimension `n − (d−1)`, finite only when `n = d − 1`. Every sample here
has `n ≫ d − 1`, so the set must be **sampled**, and LP-infeasibility over a sample is not
infeasibility over the variety.

**Measured, not argued:** in the positive control at `d = 8`, where Theorem 3 *guarantees*
saturability, test 2 returned **`LP_INFEASIBLE_ON_SAMPLE` on 20 of 20 samples**. Had its
negative side been treated as a certificate, this experiment would have reported **20 false
counterexamples in its own positive control**. The harness wiring refuses to convert
`LP_INFEASIBLE_ON_SAMPLE` into a candidate, and the positive control passed because of that
refusal. Test 2 is therefore used **only in its positive direction**, where it is sound.

### The measurement: same code, same state, opposite answer

At `d = 8` (Eq. 16, above the Eq. 15 threshold, Theorem 3 applies) the search-based route
fails totally — and it is **not** a code defect and **not** a budget problem:

| evidence | result |
|---|---|
| probe success at `d = 4` / `d = 6` (`probe_check.json`) | **8/8** and **8/8**, explicit POVMs, `‖ΣE − I‖ ≤ 8.6e-13`, `\|CFIM − QFIM\|/\|QFIM\| ≤ 1.4e-11` |
| probe success at `d = 8` | **0/8**, LP slack exactly `8.0 = Tr I` (no mass placed at all) |
| start-count sweep at `d = 8` (`probe_start_sweep.json`), 250 → 4000 starts, 16× | **0/3 at every budget**; slack stays `8.0` |
| **branch-restricted search at `d = 8`** (`lmcc_branch_probe.json`) | **LP slack exactly `0.0`, 3/3**, explicit **26-element** POVM, `‖ΣE − I‖ ≤ 1.9e-12`, `\|CFIM − QFIM\|/\|QFIM\| ≤ 6.7e-15` |

The last row is the explanation. The paper's own optimal POVM has the LMCC form
`|e^(a)_ν⟩ ⊗ |a⟩` — a **product vector with a definite ancilla index**, i.e. a measure-zero
subvariety that a Gaussian random start reaches with probability zero. Restricting the
search to those branches recovers the measurement immediately.

So: **same code, same states, same budget, a different start distribution — and the answer
flips from "no saturating measurement found" to an explicit one verified to 1e-15.** That
is the cleanest available demonstration of why a failed search must never be read as a
non-existence certificate, and it is simultaneously a constructive numerical confirmation
of the paper's LMCC theorem at `d = 8`.

---

## Rank-Certificate Gate (all five points)

The certified test is a rank deficiency of a floating-point matrix, so the rank itself
needs certifying. All five required points were run.

**1. Full spectrum logged; how small is "small"?** Per-sample `rank_gap_ratio` plus explicit
kept/dropped singular values for every model family (`structure_check.json`):

| model family | `dim 𝒱` | last KEPT singular value (rel.) | first DROPPED (rel.) |
|---|---|---|---|
| bipartite `d_sys=2, r=2, s=2` | 8 | 4.55e-02 | 4.49e-15 |
| bipartite `d_sys=3, r=2, s=2` | 12 | 1.14e-01 | **0** (exact) |
| bipartite `d_sys=4, r=2, s=2` | 12 | 1.99e-01 | **0** (exact) |
| generic `d=3, r=2, s=2` | 3 | 5.77e-01 | 4.20e-16 |
| generic `d=4, r=2, s=2` | 8 | 1.18e-01 | 6.49e-15 |
| generic `d=6, r=2, s=4` | 24 | 2.77e-02 | 9.20e-16 |
| generic `d=7, r=3, s=3` | 36 | 8.94e-03 | 2.10e-16 |

A 12–15 order-of-magnitude gap in every family; nothing is smeared. Across the search runs
the per-sample gap ratio ranged from **1.01e10 to exactly infinite** (dropped block
numerically zero).

**2. High precision.** mpmath at 40 digits reproduces the float64 rank in every family at
every threshold `1e-4 … 1e-12` (`structure_check.json`, `reverify.json`).

**3. Pre-registered threshold sweep + an explicit ambiguity category.** Rank is recomputed
at `1e-5, 1e-6, 1e-8, 1e-10, 1e-12` relative, fixed before running. If it moves anywhere in
that range — or disagrees with an independent Gram-eigenvalue route, or the gap falls below
`1e4` — the sample is `NUMERICALLY_AMBIGUOUS` and **no verdict is issued**. Observed count
of ambiguous samples across all 1400 search samples: **0**, plateau flat on every one.

**4. Independent re-implementation.** `reverify.py`, four simultaneous differences: Yang's
closed-form SLD instead of the Lyapunov solve (agreement **3.6e-15**), rotated basis,
rescaled generators, `∂ρ` from finite differences, and rank from Gram eigenvalues plus a
40-digit mpmath SVD. **`dim 𝒱_⊥` agrees 18/18; the certified verdict agrees 18/18.**

**5. Exact (non-floating-point) arithmetic.** `exact_rank.py` builds quasi-pure states over
the **Gaussian rationals** — PCC (`B_i†B_j` Hermitian) is *linear* in `B_j`, so an exact
rational solution comes from a sympy nullspace with no tolerance anywhere — and takes the
rank by exact Gaussian elimination:

| case | exact `dim 𝒱` | float64 `dim 𝒱` | PCC exactly zero? | certified? |
|---|---|---|---|---|
| `d=3, r=2, k=1` | 3 | 3 | **yes, symbolically** | no |
| `d=4, r=2, k=2` | 8 | 8 | **yes** | no |
| `d=5, r=2, k=3` | 12 | 12 | **yes** | no |
| `d=5, r=3, k=2` | 12 | 12 | **yes** | no |

Exact and float agree in every case, so the float ranks used throughout are not
conditioning artefacts. And the exact route **does** fire when it should: on injected
exactly-rank-deficient stacks it returned `dim 𝒱_⊥ = 2 < 3` and `3 < 4`, correctly, 2/2.

---

## Substrate Gate (FL Step 2a) — READY

`substrate_check.json`. The SLD solver is checked against **closed forms**, not itself.

| check | result |
|---|---|
| pure qubit, 1 parameter: `L = 2 ∂ρ`, QFI = 1 (exercises the kernel branch) | **1.1e-15**, **1.1e-15** |
| mixed qubit, Bloch closed form `b = ∂r + [(r·∂r)/(1−\|r\|²)]r`, `a = −(r·∂r)/(1−\|r\|²)` | **1.6e-14**, rel. QFI **3.6e-15** |
| random full-rank qutrit vs an **independent** dense Lyapunov solve (no eigendecomposition) | **1.0e-14**; defining-equation residual **1.8e-15** |
| quasi-pure samplers: `Π_r ∂_iρ Π_r = 0`, `Π_r L_i Π_r = 0`, analytic vs finite-difference `∂ρ` | **1.6e-15**, **5.9e-15**, **2.0e-9** (FD-limited) |
| Herm ↔ ℝ^{d²} isometry round trip / inner-product preservation | **1.2e-16**, **4.4e-16** |
| Eq. (15) threshold vs hand arithmetic, `d = 3…8` → `6, 12, 18, 25, 33, 42` | exact, error **0** |

---

## Controls

| control | result |
|---|---|
| **Positive control** — Eq. (16), `d = 8`, above threshold, Theorem 3 applies | **PASS** — 20/20 PCC true with margin (max violation **4.4e-14** against a `1e-8` tolerance), 0/20 below threshold, `dim 𝒱_⊥ = 52 ≥ d = 8` with margin 44, rank robust 20/20, **0 certified counterexamples**. Test 2 returned `LP_INFEASIBLE_ON_SAMPLE` 20/20 — the false negative documented above, correctly refused as a candidate |
| **Negative control** — random Hermitian matrices substituted for the SLDs | **PASS** — PCC true in **0 of 500**; minimum violation **3.98e-02**, median **2.87e-01**, ~6 orders of magnitude above tolerance. The PCC check is not vacuous |
| **Rank-detector control** — injected error: can the certified test fire at all? | **PASS** — with `𝒱` hand-built so `dim 𝒱_⊥ = d − 1`, Observation 2 fired **40/40**; with `dim 𝒱_⊥ = d + 3`, **0/40** false fires. A test that cannot return YES is not a test |
| **Probe-capability control** + start sweep + branch probe | see the table in the previous section |

---

## Main search — the pre-registered run

`main_search.json`. `N = 200` per configuration, two configurations, stop on the first
candidate — exactly as pre-registered. Configurations chosen by `threshold_scan.py`.

| config | `d` | `r` | `s` | n | PCC w/ margin | below Eq. (15) | `dim 𝒱_⊥` | `dim 𝒱_⊥ − d` | ambiguous | candidates |
|---|---|---|---|---|---|---|---|---|---|---|
| smallest feasible | 4 | 2 | 2 | 200 | **200** | **200** | 8 | +4 | 0 | **0** |
| escalation | 6 | 2 | 2 | 200 | **200** | **200** | 24 | +18 | 0 | **0** |

Max SLD residual **3.3e-15**; max PCC violation **8.6e-13**; QFIM full rank 400/400; rank
robust 400/400.

**Test 2 fired on its sound (positive) side on every sample**: `200/200` and `200/200`
feasible, yielding an **explicit complete optimal POVM** for each — 6–8 elements at
`d = 4`, 24 at `d = 6`, LP slack exactly `0.0`, `‖ΣE − I‖ ≤ 2.8e-12`, and
`|CFIM − QFIM|/|QFIM| ≤ 8.1e-12` (`d=4`) and `≤ 4.1e-9` (`d=6`).

So for the pre-registered class the result is stronger than "no counterexample found":
**a saturating measurement was constructed and verified for all 400 states** — a numerical
confirmation of the paper's LMCC theorem, consistent with C3.

**Verdict, in the wording the corrected protocol requires:** *no counterexample was found
via **either** exact non-saturability test (Observation 2 rank test; End Matter
completeness-feasibility) under this sampling distribution.* This is **not** evidence that
PCC is sufficient, and **not** a claim that these samples are saturable *in general* — the
paper allows non-saturability for reasons outside both tests. (The 400 explicit verified
POVMs are a separate, stronger statement, and they *are* direct evidence of saturability
for those specific states — a construction, not a failed search.)

Per-sample classification: `UNRESOLVED_BY_BOTH_EXACT_TESTS` on 400/400.

---

## Why the null was structurally guaranteed here

Derived S1–S5, then verified numerically on 21 models (`structure_check.json`, max block
violation **6.6e-16**):

* **S1** `Π_r L_i Π_r = 0` for a quasi-pure state ⟹ `L_i|ψ_a⟩` lies in the kernel.
* **S2** ⟹ `M_{i,ab}` is **purely support↔kernel off-block**.
* **S3** ⟹ `W_{ij,ab}` is **purely kernel–kernel**.
* **S4** With `k = d − r`: `dim 𝒱_M ≤ 2rk`, and — because PCC *is* the statement that the
  `W`'s are traceless — `dim 𝒱_W ≤ k² − 1`. Hence

      dim 𝒱_⊥ = d² − dim 𝒱 ≥ (r+k)² − 2rk − k² + 1 = r² + 1.

* **S5** Observation 2 fires only when `dim 𝒱_⊥ < d`. Therefore a certified counterexample
  among quasi-pure states **requires `r² + 1 < d`**.

Measured `dim 𝒱_⊥ − (r² + 1) ≥ 1` on all 21 models; the `𝒱_M`/`𝒱_W` split sums to `dim 𝒱`
exactly and respects both sub-ceilings on all 21.

**At the pre-registered primary configuration `d = 4, r = 2`: `r² + 1 = 5 > 4 = d`.** The
certified test could not have fired there for *any* state in the class, at any sample size.
200 samples of nothing.

At `d = 6, r = 2` the condition is satisfied, so the test is arithmetically live; firing
then needs `dim 𝒱 ≥ d² − d + 1 = 31` against a structural ceiling of 31. A sweep of
`s = 2…8` never came close:

| `d` | `k` | ceiling `2rk + k² − 1` | needed to certify | max `dim 𝒱` observed |
|---|---|---|---|---|
| 6 | 4 | 31 | 31 | **24** |
| 7 | 5 | 44 | 43 | **40** |
| 8 | 6 | 59 | 57 | **54** |

So further linear dependencies among `{W, M}` exist beyond those S4 accounts for — the
subject of the paper's own Supplemental §"Results on the linearly (in)dependence of
`{W, M}`", which I did not reproduce. Marked `[UNKNOWN]`.

---

## Post-registration extension — the class the open question is actually about

`extension.json`, `extension_nondegenerate.json`. Same protocol, both exact tests,
`N = 200` per configuration, applied to **generic** quasi-pure states (Yang Eq. 12) via the
`B_i†B_j` Hermitian characterisation of C4.

| `d` | `r` | `s` | n | PCC w/ margin | below Eq. (15) | `dim 𝒱_⊥` | `dim 𝒱_⊥ − d` | QFIM rank | candidates |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 2 | 2 | 200 | 200 | 200 | 6 | +3 | **1 of 2** | 0 |
| 4 | 2 | 2 | 200 | 200 | 200 | 8 | +4 | 2 of 2 | 0 |
| 5 | 2 | 3 | 200 | 200 | 200 | 10 | +5 | 3 of 3 | 0 |
| 6 | 2 | 4 | 200 | 200 | 200 | 12 | +6 | 4 of 4 | 0 |

Five configuration-runs over four distinct configurations, 1000 samples in total; `d = 4`
was sampled twice under independent seeds (`91820260918` and `5620260918`) and returned
identical structure both times, which doubles as a data-swap replication.

`NO_CERTIFIED_COUNTEREXAMPLE_FOUND` on all of them; 0 candidates, 0 `NUMERICALLY_AMBIGUOUS`,
rank robust on 1000/1000, with the same one-directional reading. Test 2 was feasible on
**1000 of 1000** samples (max `|CFIM − QFIM|/|QFIM| = 1.9e-9`), so here too the result is an
explicit verified optimal POVM per state rather than a mere absence.

**A degenerate configuration found and quarantined, not averaged away.** The `d = 3` row has
a **rank-1 QFIM in 200 of 200 samples** — the two parameters are not independently
estimable, so the multiparameter question is vacuous there. This is forced, not bad luck:
for a generic quasi-pure state with `k = d − r = 1`, the `a = a` part of PCC gives
`β_{2,a} = c_a β_{1,a}` with `c_a` real, and the `a ≠ b` part then forces `c_1 = c_2 = c`,
collapsing the QFIM to the rank-1 form `[[1, c],[c, c²]]`. Verified across four `(d, r, s)`
combinations with `k = 1`: **generic QFIM rank = 1 in every case, while the Eq. (16) class
at the same sizes gives rank 2** — because there the `a ≠ b` conditions are vacuous. Same
mechanism as C4, surfacing in a second observable. The extension was re-run at
non-degenerate configurations rather than the `d = 3` row being deleted; both runs are kept.

---

## No-Collapse tests (all 7)

| test | what changed | result |
|---|---|---|
| Data swap | seven seeds across runs (`5620260918`, `91820260918`, `314159`, `560918`, `4242`, `555`, `20260919`) | **PASS** — verdict and every `dim 𝒱_⊥` identical |
| Noise injection | rank tolerance swept `1e-5 … 1e-12` | **PASS** — plateau flat on 1400/1400 search samples; 0 ambiguous |
| Scale variation | `N` = 3, 8, 20, 200; `d` = 3…8; `s` = 2, 3, 4; probe starts 250 → 4000 | **PASS** — no verdict changed |
| Convention flip | global unitary reparametrisation; generator rescaling ×3.7; analytic vs finite-difference `∂ρ`; SLD kernel-block convention | **PASS** — `dim 𝒱_⊥` invariant, 18/18. The kernel-block freedom is provably irrelevant: by S2/S3 both `W` and `M` depend only on the support↔kernel blocks of `L` |
| Negative control | random Hermitian for SLDs | **PASS** — 0/500 |
| Adversarial input | near-degenerate weights `q_a` | **PASS, and vacuous by construction** — `L_i` for a quasi-pure state depends only on `B_i`, not on `q_a` at all, so PCC, `W`, `M`, `dim 𝒱_⊥` and the whole verdict are **independent of the eigenvalue weights**. Only the QFIM depends on them. Derived, then confirmed by the `q`-independence of every recorded rank |
| Alternative tool | independent Lyapunov SLD; closed-form SLD; Gram-eigenvalue rank; 40-digit mpmath SVD; **exact rational arithmetic**; LP-dual separation vs direct POVM optimisation | **PASS** — 1.0e-14, 3.6e-15, exact, exact, exact |

---

## Six defects found in my own instrumentation, and the pattern behind them

1. **The `d = 8` positive control failed on first run** (2/3 "not saturable" where a theorem
   says otherwise). That failure motivated — and then independently confirmed — correction 1.
   It was not swept up as a result.
2. **Test 2's negative side would have produced 20 false counterexamples** in the positive
   control had it been treated as a certificate. Caught because the positive control exists
   and because the wiring refuses to promote `LP_INFEASIBLE_ON_SAMPLE`.
3. **`rank_is_robust` was false on ~52 % of `d = 4` samples** because the Gram-matrix rank
   route used a `1e-16` relative cut — exactly the float64 eigenvalue noise floor of a
   squared-singular-value matrix. Since `rank_is_robust` is ANDed into the candidate
   predicate, this would have **suppressed a genuine candidate had one occurred**. Fixed to
   `1e-12` on the Gram, still ~1e15 below the observed gap.
4. **Three separate "relative-to-its-own-largest-value" thresholds inverted on identically
   zero objects.** When `k = d − r = 1`, PCC forces every `W` to vanish exactly (rank ≤ 1
   inside a 1-dimensional kernel block, and traceless). Dividing such a matrix by its own
   norm divides round-off by round-off: the block-structure check reported an O(1)
   "violation", and the `𝒱_W` dimension came out as 4 for a set of zero matrices.
5. **Two rank plateaus were queried below their own input's noise floor** — mpmath at
   `1e-20` on float64 input, and `1e-10` on a path whose `∂ρ` came from finite differences
   with an ~`1e-10` error floor. Both "disagreements" were properties of input precision,
   not of the rank.
6. **This file was truncated to zero bytes** by a patch script whose `write_text` raised a
   `UnicodeEncodeError` *after* opening the file for writing. Recovered by rewriting in
   full. Recorded because it is the same class of hazard as the rest: a step that looks
   atomic and is not.

The pattern behind 3–5 is one thing: **a threshold expressed relative to a quantity that can
itself be zero or noise-dominated is not a threshold.** It produced both a spurious failure
and a dangerous spurious pass in the same experiment.

---

## Claim Entropy (Perelman monotone invariant)

Recorded here rather than by editing `claim.md`, which is left as the original spec.

| component | at claim.md | now | why |
|---|---|---|---|
| unsupported HIGH claims | 0 | 0 | — |
| hidden assumptions | 0 | **1** | found, not introduced: `claim.md` assumed Eq. (16) *is* the quasi-pure class; it is a proper subclass with its own sufficiency proof |
| missing negative controls | 0 | 0 | negative control 0/500, plus a rank-detector injected-error control, a probe-capability control, a start-count sweep and a branch probe that were not in the spec |
| ambiguous definitions | 0 | 0 | two resolved: `n` ↔ `(d,s)` (C1), `ψ` vs `φ` (C2) |
| unresolved blockers | 1 | **0** | A1 resolved — SLD implemented and verified against three closed forms, an independent solver, and exact arithmetic |
| **total** | **1** | **1** | did **not** decrease |

Per `perelman-audit.md` a step where `claim_entropy` does not decrease does not count. It
did not decrease, and that is the correct record: one blocker cleared, one hidden assumption
uncovered. The uncovered assumption is the actual output of this run.

---

## Kill Analysis

**What is killed:**

* The claim **as pre-registered** for the stated search space `{Eq. (16), d = 4 and d = 6,
  r = 2, s = 2}` — killed by a *theorem*, not a sample size: the paper's End Matter proves
  sufficiency for that whole class, S5 independently shows the certified detector cannot
  fire at `d = 4, r = 2`, and 400 explicit saturating POVMs were constructed and verified.
* **`(d,s)` as an adequate coordinate system** for this question. It omits `r`, and the
  below/above-threshold status is not a function of it at all (C1).
* **Search-based non-saturability** as a method here, killed quantitatively: 0/8 success
  where a theorem guarantees success, unchanged over a 16× budget range, while the same code
  at the same budget succeeds 3/3 once restricted to the correct structural branch.
* **Treating test 2's infeasibility as a certificate**, killed by direct measurement: 20/20
  false negatives in the positive control.

**What is NOT killed:**

* **The open question itself**, entirely untouched. Whether PCC is sufficient for generic
  quasi-pure states remains open. 1000 generic-quasi-pure samples produced no certified
  counterexample, but the only certification route available (Observation 2) is
  one-directional and, by S5, structurally blind at every size tested.
* **A counterexample via a mechanism outside both tests.** A state with `dim 𝒱_⊥ ≥ d` for
  which no complete POVM nonetheless exists is invisible to everything used here.
* **The `r² + 1 < d` region**, which S5 identifies as the only place the certified route
  *could* fire and which `dim 𝒱` does not reach at `d ≤ 8, r ≤ 3` — for reasons not
  determined here.
* **The harness**, verified against three closed forms, an independent Lyapunov solver, a
  closed-form SLD, a 40-digit mpmath SVD, exact rational arithmetic, an injected-error
  detector control, and hundreds of explicit POVMs reproducing CFIM = QFIM to 1e-15.

**Relaxation Map** (one assumption per variant; separate experiment ids):

* **V1 — replace the search space.** Pre-register the generic class (Yang Eq. 12) via the
  `B_i†B_j` characterisation, excluding `k = 1` as QFIM-degenerate. Run here post-hoc; V1 is
  the pre-registered version of it.
* **V2 — explain the ceiling.** Determine what additional linear dependence keeps `dim 𝒱`
  below `2rk + k² − 1`; the paper's Supplemental §"linear (in)dependence of `{W, M}`" is the
  starting point. Would convert an empirical plateau into a second necessary condition.
* **V3 — get an exact test for the `dim 𝒱_⊥ ≥ d` case.** This is the real blocker.
  Saturability is membership of `I/d` in the convex hull of the rank-one projectors inside
  `𝒱_⊥`; a certified NO needs a verified separating hyperplane, i.e. a *global* minimum of
  `⟨u|X|u⟩` over `{|u| = 1, ⟨u|A_k|u⟩ = 0}`. A sums-of-squares / Lasserre relaxation supplies
  exactly that with a certificate. The branch probe shows why nothing less will do.
* **V4 — raise the rank.** Everything here is `r ≤ 3`, and S5 makes `d > r² + 1` harder as
  `r` grows, so a counterexample is more likely at small `r` and large `k`.

---

## Pearl Card outcome

**Prediction (from `claim.md`):** *"if a counterexample is found, it should appear at the
SMALLEST tested `(d,s)` below threshold."*

**Correct?** **Not testable as stated, and its reasoning is now contradicted.** No
counterexample was found anywhere; but S5 inverts the intuition — the certified route
requires `d > r² + 1`, i.e. a **large kernel**, so the smallest dimension is the *least*
likely place for this mechanism. The smallest tested configuration turned out to be the one
place where the detector is provably blind.

**Falsification condition triggered?** No.

---

## Pearl Gate

Three side-findings are testable and do not belong to this claim. Proposed rows for
`pearl_registry/INDEX.md` — the orchestrator owns that file; nothing is written to it here.

| field | value |
|---|---|
| source | `20260918-pcc-sufficiency-quasipure-cat56` |
| observation | For quasi-pure states the SLD — and hence PCC, `W`, `M`, `dim 𝒱_⊥` and the entire saturability verdict — is **completely independent of the eigenvalue weights `q_a`**; only the QFIM depends on them. An entire axis of the apparent parameter space is inert. |
| falsifiable prediction | Sweeping `q_a` across the simplex at fixed generators, including to near-degeneracy, changes no rank and no verdict to machine precision, for any `(d, r, s)`. One extra loop in the harness. |
| impact_score | 4 — narrows the search space for anyone attacking this conjecture numerically, and turns the standard "near-degenerate weights" adversarial test into a provable no-op |
| trigger_condition | any numerical attack on PCC sufficiency, or quasi-pure-state metrology experiment design |
| next_check | 2026-11-15 |
| status | pending |

| field | value |
|---|---|
| source | `20260918-pcc-sufficiency-quasipure-cat56` |
| observation | A non-convex search failed **totally and reproducibly** (0/8, unchanged over a 16× budget increase) in a regime where the answer is a theorem — and succeeded **3/3 with LP slack exactly 0** once restricted to the measure-zero structural branch the theorem's solution actually lives on. Same code, same states, same budget, different start distribution, opposite answer. |
| falsifiable prediction | Wherever a known solution has a product/block structure, uniform random multi-start will fail at a rate approaching 1 as dimension grows, while a structure-restricted start recovers it at the same budget. Testable on any of this project's other non-convex searches by adding one structured-start arm. |
| impact_score | 6 — converts "a failed search is not a certificate" from a methodological slogan into a measured, reproducible mechanism, and points at the concrete fix (structured starts) rather than just a warning |
| trigger_condition | any experiment whose negative conclusion rests on a non-convex search failing |
| next_check | 2026-11-15 |
| status | pending |

| field | value |
|---|---|
| source | `20260918-pcc-sufficiency-quasipure-cat56` |
| observation | Three independent instrumentation defects in one experiment shared one cause: a numerical threshold expressed **relative to a quantity that can itself be identically zero or noise-dominated**. It produced both a spurious FAIL (block-structure check at `k = 1`, where PCC forces `W ≡ 0`) and a spurious PASS-suppressor (Gram rank at the float64 noise floor, which would have hidden a genuine candidate). |
| falsifiable prediction | Auditing other numerical harnesses in this project for `x > scale(x) * tol` where `scale(x)` derives from `x` itself will find further instances; each is fixed by an externally-derived reference scale. Grep plus one injected-zero case per site. |
| impact_score | 5 — methodological, applies to every rank/ratio test in this repo, and one instance here failed in the invisible, fail-safe-looking direction |
| trigger_condition | any experiment whose verdict depends on a numerical rank, a relative residual, or a ratio test |
| next_check | 2026-11-15 |
| status | pending |

---

## What this does NOT mean

1. Does **not** resolve, or move, the open question of whether PCC is sufficient for generic
   quasi-pure states. It relocates it: the question is about Yang's Eq. (12) class, not the
   Eq. (16) construction.
2. The 1000 generic-quasi-pure samples with zero certified counterexamples are **not**
   evidence for sufficiency. The only certification route used is one-directional and, by
   S5, cannot fire at any configuration tested.
3. The hundreds of explicit POVMs **are** direct evidence that those specific sampled states
   are saturable — a verified construction, not a failed search — but they say nothing about
   states outside the sample and nothing about the general conjecture.
4. Does **not** establish that `dim 𝒱` cannot reach `d² − d + 1`. The sweep is bounded
   (`d ≤ 8`, `r ≤ 3`, `s ≤ 8`, 8 samples per cell) and the obstruction is unexplained.
5. The `r² + 1` bound (S4/S5) is derived under PCC and a parameter-independent spectrum, and
   verified on 21 models — it is not a statement about arbitrary mixed states.
6. Nothing here is a statement about experimental quantum metrology. Every object is a
   randomly sampled mathematical model.

---

## Files

| file | role |
|---|---|
| `pcc_core.py` | SLD, samplers, PCC, `W`/`M`, `dim 𝒱_⊥`, Eq. (15) threshold, rank diagnostics |
| `pcc_sat.py` | exact test 1 (Observation 2), exact test 2 (completeness feasibility), the explicitly non-decisive constructive probe |
| `pcc_sld_harness.py` | modes: positive / negative / rank-detector / probe-capability controls, main search, extensions |
| `substrate_check.py` | FL Step 2a + closed-form SLD verification |
| `threshold_scan.py` | measures below/above Eq. (15) per configuration instead of assuming it |
| `structure_check.py` | S1–S5 verified numerically; `𝒱_M`/`𝒱_W` split; ceiling sweep; `k = 1` QFIM degeneracy; singular-spectrum evidence |
| `exact_rank.py` | Rank-Certificate Gate point 5 — exact Gaussian-rational rank, plus an injected-deficiency arm |
| `reverify.py` | independent second-path reconstruction (protocol step 4) |
| `probe_start_sweep.py` | self-falsification: is the `d = 8` search failure a budget problem? (no) |
| `lmcc_branch_probe.py` | why it fails: structural-branch coverage, and the POVM recovered |
| `metrics/*.json` | all recorded outputs; every number in this file comes from one of them |

All Python is `ruff`-clean.
