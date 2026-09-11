# Deep External Novelty Audit — Y-17 Project (2026-09-10)

**Commissioned by:** direct user request for a rigorous external-literature novelty audit across all
strong Y-17 results, testing 10 possible relations to existing literature (special case, counterexample,
boundary result, known-under-different-name, etc.) rather than just "are the methods new."

**Method:** 6 parallel, context-asymmetric `Agent(analyst, model=opus)` invocations, one per cluster
(A1: Boolean network dynamics/control, A2: Boolean network structural/canalization, B: Forsythe
conjecture, C: transient growth/Kreiss constants, D: TDA early-warning/lakes, E: Lovász theta random
circulant graphs). Each was briefed with the full FL Step -3 methodology, the 10 novelty-status
vocabulary, and explicit "primary sources only, no snippets, cite exact quotes" instructions.

## 0. Critical infrastructure finding (all 6 agents, independently)

**Every one of the 6 `analyst`-type agents reported having only `Read`/`Write`/`Edit` tools available —
no `WebFetch`, no `WebSearch`, no `mcp__arxiv__*`, no `mcp__semantic-scholar__*`.** This directly
contradicts the agent catalog's own listed toolset ("Tools: All, tools, Write, Edit, Read") — a
recurrence of the exact class of error `patterns.md` already logged in July 2026
(`[AVOID×1] Agent-каталог врёт про tools`), now confirmed a second time at a much larger scale (6/6
independent invocations, not 1).

**Consequence:** none of the 6 agents could complete the external half of the audit (opening primary
sources, quoting exact theorem statements). Per FL Step 2a (Substrate Gate), this is recorded as
`BLOCKED-INFRASTRUCTURE` for that half — **never** as evidence against novelty. Every external
literature reference below is marked `[MEMORY]` (agent's own training-data recall, unverified this
session) and capped at LOW-MEDIUM confidence per `integrity.md`.

**What happened instead — and turned out more valuable than expected:** all 6 agents pivoted to
**deductive/internal reanalysis** of the project's own committed artifacts (graph.yaml, decision.md,
run.json, and in one case the project's own Lean 4 proof file). This produced:
- 3 claims proven to be **literal tautologies** (follow from definitions alone, no domain content)
- 1 **exact mathematical inequality** derived from first principles that falsifies part of a headline
  claim (Lovász cluster) and surfaces a real unnoticed finding in already-collected data
- 1 **exact algebraic proof** that a "novel empirical finding" (asymmetric transfer degradation, B2
  cluster) is a scale-invariance artifact of the feature construction
- Multiple internal inconsistencies caught in the project's own artifacts (numeric errors, near-vacuous
  controls, an uncited/possibly-fabricated literature reference, invalid p-value computation)

None of this required external literature access. All of it is `[VERIFIED-DEDUCTIVE]` or
`[VERIFIED-REAL]` against the project's own files.

---

## 1. Summary table (all clusters)

| Y-17 result | nearest external problem/theorem | relation | novelty status | confidence | next cheapest decisive check |
|---|---|---|---|---|---|
| **A1 — Boolean network dynamics/control (Remy 2015)** ||||||
| j*=1 minimal observation delay (H-B7-14/15) | Observability index, Boolean control networks (Cheng&Qi 2009; Laschov/Margaliot/Even 2013) `[MEMORY]` | known framework ⇒ claim (instance) | `BENCHMARK-SPECIFIC-NUMERIC-RESULT` | medium | search "observability index" + Remy 2015/bladder cancer |
| M1/M2 marker sets insufficient at j=0 (H-B7-13) | same framework, negative instance | known framework ⇒ claim | `NO-NOVELTY` | medium | none needed |
| Schedule dependence of k*=5 (H-B7-22) | Klemm&Bornholdt PRE 2005; Chaves/Albert/Sontag JTB 2005 `[MEMORY]` | general theorem ⇒ claim | `KNOWN-BY-GENERAL-THEOREM` | medium | open Klemm&Bornholdt, verify "sync attractors unstable under timing" |
| k_adv=1, adversarial-safe window empty (H-B7-22) | strong basin of attraction / trap spaces (Zañudo&Albert 2015; Klarner et al. 2015) `[MEMORY]` | known theory ⇒ claim; computable by standard tool | `KNOWN-BY-GENERAL-THEOREM` | medium | **run `pystablemotifs` on k=1/branch_1 — single call** |
| Exact random-async escape probabilities (H-B7-26) | succession-diagram Markov chains, npj SysBio Apr 2026 `[VERIFIED-in-prior-report]`; PBN, Shmulevich 2002 `[MEMORY]` | more general method ⇒ claim (instance) | `KNOWN-METHOD-ONLY` (numbers: `BENCHMARK-SPECIFIC-NUMERIC-RESULT`) | high | re-solve in `fractions.Fraction` — is P(k=2)=2·P(k=1) exact? |
| CyclinE1 sharp point-of-no-return, no flip-back (H-B7-24) | forward-closure of reachable-attractor sets | **tautology** — the test could not fail | `NO-NOVELTY` | high (pure deduction) | none — provable in 2 lines |
| CyclinE1-not-CyclinA asymmetry (H-B7-24) | stable motifs / commitment points (Zañudo&Albert 2015; Fauré et al. 2006) `[MEMORY]` | general theory ⇒ claim | `KNOWN-BY-GENERAL-THEOREM` | low-medium | verify CyclinE1 ∈ stable motif, CyclinA ∉ (pyboolnet, one call) |
| Bounded-fairness starvation count (H-B7-25) | bounded fairness (Dershowitz et al. 2003); fair CTL model checking `[MEMORY]` | known apparatus answers a STRONGER question; our value degenerate with CyclinE1's PNR index | result: `KNOWN-METHOD-ONLY` (degenerate); question `L*(k)`: `POSSIBLE-NOVEL-SPECIAL-CASE` | low-medium | formalize `L*(k)` as fair-CTL query, test in pyboolnet |
| Fixed-point N&S perturbation condition, 35/35 nodes (H-B7-21) | definition of table lookup | **tautology, not even BN-specific** | `NO-NOVELTY` | high (pure deduction) | none |
| Branch automorphism via EGFR_stimulus (H-B7-27/28) | symmetry reduction arXiv:1203.3395 `[VERIFIED-in-prior-report]`; likely follows from definition given the invariant | known technique ⇒ claim; automorphism follows from invariant by construction | `KNOWN-BY-GENERAL-THEOREM` | medium-high | pyboolnet `percolate` — does EGFR_stimulus drop out automatically? |
| Contextual input redundancy (H-B7-27) | canalization arXiv:2303.16361 + CANA `[VERIFIED-in-prior-report]` | same result, different name | `KNOWN-SAME-RESULT-DIFFERENT-LANGUAGE` | medium-high | rename internally to "constant percolation" |
| ROBUST/FRAGILE/CRITERION_INVALID taxonomy (H-B7-17/19/20) | vacuity detection in model checking (Beer et al. 2001; Kupferman&Vardi 2003) `[MEMORY]` | known concept ⇒ ad-hoc instance | `KNOWN-SAME-RESULT-DIFFERENT-LANGUAGE` | medium | open Beer et al., compare vacuity def to CRITERION_INVALID |
| **A2 — Boolean network structural (re-audit of the prior internal audit)** ||||||
| Fixed-point preservation, single-bit (35 nodes) | **IS** the project's own Lean theorem `update_changes_iff` — general `Function.update` lemma | identity, not instance | `NO-NOVELTY` | high | stop citing as "theorem about the network" |
| Fixed-point preservation, multi-node simultaneous | same, trivial `List.forall` wrapper | identity | `NO-NOVELTY` | high | none |
| Branch automorphism (reclassified) | **trap-space percolation** (not symmetry reduction as previously stated) | invariant ⇒ percolation ⇒ EGFR_stimulus drops from rules ⇒ automorphism is CONSTRUCTIVE, not "found" | `KNOWN-BY-GENERAL-THEOREM` (conditional) | medium-high | **run pystablemotifs/PyBoolNet percolate — single call resolves this** |
| Automorphism extended to k=1..40 (4516 states) | closure of trap space | follows from the above by definition of closedness | `NO-NOVELTY` | medium-high | symbolic check that 3 rules preserve the subspace |
| FGFR3_stimulus asymmetry (negative control) | same algebra as above | predicted a priori, not a finding | `NO-NOVELTY` | high | **fix "1-2 orders of magnitude" claim — actual is ≥4 orders at k=5** |
| Early-exit BFS savings 84-90% | ∃-vs-∀ quantifier definition over finite sets | definition, not theorem; number is order-dependent | `NO-NOVELTY` (method) / `BENCHMARK-SPECIFIC-NUMERIC-RESULT` (number) | high | **verify both ROBUST test conditions are 2-state graphs — near-vacuous floor check** |
| Fragility rates by node (RBL2 33.3%/p21CIP 0%/CyclinE1 9.7%) | — (only non-derivable measured residual in this cluster) | genuinely computed, not from definitions | `BENCHMARK-SPECIFIC-NUMERIC-RESULT`; p21CIP subcase `POSSIBLE-NOVEL-SPECIAL-CASE` | medium | **investigate structural cause of exact 0/15 for p21CIP — could become a lemma** |
| **B — Forsythe conjecture / restarted CG** ||||||
| H-CAT37-1: 0/171 no counterexamples found | Forsythe conj., resolved FALSE for s≥4 by arXiv:2609.04659 `[UNKNOWN-BLOCKED]` | fully absorbed by external resolution; "near-measure-zero" framing unsupported (9 samples at known-positive config, 95% CI upper bound ≈28%) | `NO-NOVELTY` | high | open arXiv:2609.04659, check if counterexample set is provably open (positive measure) |
| H-CAT37-2: DE-search negative at n=5,6,7 | question of minimal dimension for s=4 `[UNKNOWN-BLOCKED]` | bounded stochastic negative gives no lower-bound information; search space artificially clipped, optimum pinned to boundary | `BENCHMARK-SPECIFIC-NUMERIC-RESULT` | high (result) / low (question status) | grep arXiv:2609.04659 + citing papers for "minimal"/"smallest"/"tight" |
| "10-40x delay" as standalone quantity | Kantorovich/Akaike 1959; Pronzato-Wynn-Zhigljavsky dynamical search `[MEMORY]` | measures κ pinned at box boundary, not proximity to Hopf bifurcation; the objective's Hopf-branch never executed for final candidates | `NO-NOVELTY` | high (internal) / medium-low (literature) | 1000 random spectra from same bounds → percentile of 314 |
| **C — Transient growth / Kreiss constants (Bridge 2)** ||||||
| Nondimensionalization identity M_{T,W}(B)=M_{1,0}(T(B-WI)) | semigroup exponential shift + time-homogeneity of exp(tA) | direct 3-line consequence of definition | `NO-NOVELTY` | high | none — self-certifying |
| K(A)≤sup‖e^{tA}‖≤e·n·K(A), 20/20, efficiency 3.7-31% | Kreiss Matrix Theorem (proven); sharpness question | numeric check of proven theorem; tightness numbers invalidated by later H-B2-1y (K biased 1.6-84x, never converged) | `KNOWN-BY-GENERAL-THEOREM` (+ non-measurement-grade `BENCHMARK-SPECIFIC-NUMERIC-RESULT`) | high/low | get a certified-accuracy K algorithm before any literature comparison |
| pseudopy cross-impl + "convergence depth scales with K(A)" | K(A)=sup_ε α_ε(A)/ε characterization `[MEMORY]` | (a) method application; (b) likely restatement of K's own definition | (a) `KNOWN-METHOD-ONLY`; (b) `INCONCLUSIVE-LITERATURE-COLLISION` | medium | build ε*(A) vs K(A) on the 16 H-B2-1y matrices — degeneracy test |
| **Asymmetric transfer degradation (7-30x/3.4x/22-200x)** | **K_ref feature is homogeneous of degree 0** — proven by substitution z=cw in Kreiss constant definition | arithmetic consequence of a CONSTANT predictor vs a target that trivially varies with T | `NO-NOVELTY` (general claim) / `BENCHMARK-SPECIFIC-NUMERIC-RESULT` (table) | high | **one-line check on saved run.json: is K_ref(C) identical across all T per matrix?** |
| Non-transferable fitted power-law, 19x speedup | generic OOD failure of regression; exponent partially measures its own bias (per H-B2-1y) | instance of known regression property | `NO-NOVELTY` | high | check if "19x" is proportional to n_grid convention |
| **D — TDA early-warning signals (Bridge 3, lakes)** ||||||
| H1-VR persistence invariant to window time-reversal (5/5 byte-identical) | VR complex defined purely via distance matrix; reversal is an isometry (permutation) of the point cloud | **literal tautology, 5-line proof, no theorem needed** | `KNOWN-BY-GENERAL-THEOREM` (definitionally true) | high (pure deduction) | add negative control: random shuffle (not reversal) MUST give different diagram |
| Consequence: detector blind to within-window direction | classical EWS (variance/AR1/skewness/spectrum) share the SAME time-reversal invariance | reframes: not a TDA weakness vs baseline, a shared property | `KNOWN-BY-GENERAL-THEOREM`/`NO-NOVELTY` | medium-high | verify arithmetically that the arc's own classical stats are also reversal-invariant |
| H-B3-2 chirality-excess REJECT (Windermere false alarm, floor 53-63%) | Baryshnikov 2022 chirality paper `[UNKNOWN-BLOCKED]` | application of published metric; outcome possibly predicted by source's own §4; project's floor >50% elsewhere means `CRITERION_INVALID`, not REJECT | `BENCHMARK-SPECIFIC-NUMERIC-RESULT` (arguably mis-classified) | medium | correlate chirality_excess trace with rolling-slope trace — if \|ρ\|>0.8, this re-tested baseline #1 |
| H-B3-1q/1r season-split collapse of cross-var coherence | Simpson/Yule effect; spurious regression (Yule 1926, Granger-Newbold 1974) `[MEMORY]` | instance of canonical statistical pitfall; mechanism postulated not established | `KNOWN-SAME-RESULT-DIFFERENT-LANGUAGE` (mechanism) + `BENCHMARK-SPECIFIC-NUMERIC-RESULT` (numbers) | medium | **open DNB (Chen/Liu/Aihara/Chen 2012, PMID 22461973) — highest-value single check in this cluster**; also: H-B3-1q's p-values (to 1e-43) computed on cumulative trajectories as if n=161 independent — statistically invalid, needs surrogate null |
| **E — Lovász theta, random circulant graphs (CAT31)** ||||||
| H-CAT31-1: θ/√n∈[0.975,1.018], slope=-0.035 | Conjecture 18, arXiv:2603.29571 `[UNKNOWN-BLOCKED]` | numeric support only; "≈1" is half-forced by **exact E[θ]≥√n** (derived from θ(G)θ(Ḡ)=n + AM-GM + self-complementarity); slope is miscalculated (should be ≈0 on n≥40, a negative slope is mathematically impossible) | `BENCHMARK-SPECIFIC-NUMERIC-RESULT` | high (status)/low (occupancy) | recompute slope on n≥40 only; state E[θ]≥√n explicitly |
| H-CAT31-2 reformulation identity via cosh | Lovász 1979 θ(G)θ(Ḡ)=n + ensemble self-complementarity | 2-line consequence; may BE the published companion-work lower bound | `NO-NOVELTY` | high/medium | **open the companion work cited inside arXiv:2603.29571 — does it use the same symmetrization?** |
| **Derived (not originally claimed): Var(log θ/√n) ∝ n^-0.96** | quantitative form of Conjecture 18's own o(1) term | genuinely new empirical measurement, found by re-analyzing existing run.json, verified to 4-5 digits against their own var_X | currently `BENCHMARK-SPECIFIC-NUMERIC-RESULT`, candidate `POSSIBLE-NOVEL-SPECIAL-CASE` | high (arithmetic)/low (novelty, unchecked) | **re-run at 8-10 n values in 64..4096, N≈200-500, get exponent CI — cheap, one night of compute** |
| H-CAT31-2 prime/composite tail null | random Cayley graphs on abelian groups (Alon, Green); Muzychuk, So `[MEMORY]` | known mechanism (coset alignment, exponentially rare at p=1/2) predicts this null | `NO-NOVELTY` | medium | pre-register n/p_min as continuous predictor instead of binary prime/composite |

---

## 2. Top-3 candidates most likely to be genuinely novel

1. **Var(log θ/√n) ∝ n^-0.96 (Lovász cluster, E)** — the single cleanest candidate. Not claimed by the
   project itself (found by the audit agent re-analyzing already-collected `var_X` data), arithmetically
   verified to 4-5 digits, gives a quantitative form of an o(1) term the conjecture's own source paper
   states only qualitatively. Cheap to strengthen (one night of compute at wider n range).
2. **p21CIP exact 0/15 fragility rate (Boolean network A2)** — the one measured residual in that whole
   cluster that isn't derivable from a definition. A structural explanation (if found) would lift it from
   observation to lemma about this specific network's p21CIP rule.
3. **The α_ε(A)-vs-κ(V)/ω(A) threshold at N≥40 (flagged by agent C, outside the assigned claim list)**
   — an empirically localized boundary between what resolvent/pseudospectral information predicts and
   what pure spectral/numerical-abscissa information cannot, on p<1e-6 evidence. Named in the project's
   own Relaxation Map but never run. Closest thing in the whole audit to `NEW-BOUNDARY-RESULT`.

## 3. Top-3 almost certainly already known

1. **Fixed-point preservation under rule perturbation (H-B7-21)** — literally the project's own Lean
   theorem `update_changes_iff`, a general `Function.update` lemma with zero Boolean-network content.
2. **CyclinE1 sharp point-of-no-return with no flip-back (H-B7-24)** — a tautological consequence of
   forward-closure of reachable-attractor sets; the test that "confirmed" it could not have failed.
3. **H1-VR persistence invariance to window time-reversal (TDA/lakes, D)** — a 5-line proof from the
   definition of the Vietoris-Rips complex (reversal is an isometry of the embedded point cloud).

## 4. Top-3 where one cheap check could flip the verdict sharply

1. **Branch graph automorphism via EGFR_stimulus (H-B7-27/28)** — running `pystablemotifs`/PyBoolNet
   `percolate` on one release-state (already-installed tooling, one function call) either reproduces the
   whole mechanism automatically (novelty → 0) or it doesn't (genuine additional content survives).
2. **Kreiss-constant asymmetric-transfer-degradation claim (H-B2-3, C)** — one line on already-saved
   `run.json`: is `K_ref(C)` identical across all T per matrix? If yes (very likely, per the derived
   degree-0 homogeneity proof), the whole "finding" collapses into an arithmetic artifact requiring a
   dated addendum.
3. **H-CAT31-2's cosh-reformulation identity vs the Bandeira et al. companion work** — a single primary-
   source read (the companion paper cited inside arXiv:2603.29571) either shows it already proves
   `E[θ]≥√n` via the same symmetrization (→ `NO-NOVELTY`, fully occupied) or it doesn't (→ the identity
   and its Var(X) consequence both remain live).

## 5. Final verdict

**No, among the currently registered Y-17 results, there is not yet one confirmed, honest candidate for
a new scientific statement external to the project** — but the reason is more specific and more useful
than a blanket "nothing here." Of ~33 audited claims:
- **9 are literal tautologies or trivial consequences of definitions** (no amount of literature search
  changes this — they were mis-classified as findings by the project's own internal process, not because
  the process is careless, but because "exhaustively verified" and "definitionally true" look identical
  from inside a single experiment without the cross-cluster deductive pass this audit performed).
- **~15 are correct, well-verified applications of established techniques/theorems to this project's
  specific models** — real, useful, but explicitly `KNOWN-BY-GENERAL-THEOREM` or `KNOWN-METHOD-ONLY`.
- **~6 remain genuinely unresolved** because external verification was blocked by a tooling failure, not
  because they were checked and found wanting (this must not decay into "probably known" over time —
  each has a named, cheap next check above).
- **2 are new empirical facts about the project's own data that the project itself never surfaced**
  (Var(X)∝n^-0.96; the p21CIP exact 0/15) — found only because this audit re-analyzed already-collected
  numbers with fresh eyes, not because new experiments were run.

The honest framing for ADR-121 going forward: the project's own stop-rule condition "(3) a new
theorem/literature gap that the B7/B3 audits did not find already established" is **still not met** by
anything currently registered — but this audit found something ADR-121 did not anticipate: **a small
number of genuinely new quantitative facts hiding inside data the project already has**, discoverable by
deductive reanalysis, not by running new experiments or waiting for a new substrate. That is arguably a
5th, cheaper resume condition worth adding explicitly.

## 6. Track 1 — local decisive checks (executed 2026-09-10, no external tools needed)

All 7 items executed directly in the main session (not delegated, given § 0's tool-inheritance
failure). Full detail in each experiment's own decision.md ADDENDUM; summary:

- **Lovász slope recomputed on n≥40 only: -0.0002 (≈flat), not -0.035.** The E[θ]≥√n exact
  inequality (Lovász 1979 + AM-GM) verified algebraically and numerically (5/9 sample means below
  1.0 are noise: SE at n=2560 is 0.0143, observed 0.975 is only 1.74σ below 1.0).
- **K_ref(C) is proven exactly homogeneous of degree 0** (algebraic proof from the Kreiss-constant
  definition). Numerically confirmed the implementation's FIXED `[X_FLOOR=1e-4, X_HI=60]` search
  range breaks this invariance at extreme scale (verified on a synthetic matrix: exact match for
  c∈[1e-4,10], ~40% error at c=1000) — a second, independent mechanism behind the "asymmetric
  transfer degradation" finding, alongside the already-known constant-predictor-vs-varying-target
  arithmetic.
- **H-B7-29's "1-2 orders of magnitude" corrected to exact 1.6–4.2** (verified against
  `metrics/run.json`: ratios 41.4x–15628x across the 10 conditions).
- **H-B7-31's ROBUST floor check confirmed near-vacuous**: both tested ROBUST conditions
  (branch_1/2, k=5) are exactly 2-state graphs — verified directly against `metrics/run.json`.
- **H-B7-26: found and Pearl-registered an exact rational relation**, `P(k=2)=2·P(k=1)` —
  `119/864 = 2×119/1728` exactly (`fractions.Fraction`, matched to full float64 precision across
  two independently-solved linear systems of different sizes). Mechanism unexplained, flagged.
- **H-B3-2: tested and REFUTED** the hypothesis that `chirality_excess` simply re-tests baseline #1
  (`trend_slope`) — correlation moderate (|r|=0.40–0.57) and sign-inconsistent across lakes, not
  the strong uniform correlation a disguised-baseline statistic would show.
- **H-B7-27: branch automorphism independently confirmed via `pyboolnet`'s trap-space solver**
  (genuinely independent tool, ASP-based, no dependency on this project's own BFS) — flipping
  `EGFR_stimulus` in the release-state gives an identical minimal trap space on all 21 other
  dimensions. `verification_strength` upgraded `medium`→`strong`.

## 7. Track 2 — external literature verification (executed 2026-09-10, WebFetch/arXiv/Semantic
Scholar loaded directly into the main session via `ToolSearch`, not delegated to a subagent again)

4 of 6 planned checks completed, all against primary sources opened directly (not snippets):

- **arXiv:2609.04659 (Forsythe resolution) — CONFIRMED via direct quote.** The paper's own
  "Consequences and further questions" section states verbatim: *"Natural questions include the
  smallest dimension in which nonconvergence can occur at each restart length."* The `s+4=8`
  minimality question H-CAT37-2 probed is confirmed OPEN by the theorem's own authors — resolves
  the earlier `[UNKNOWN-BLOCKED]` status. Theorem 1.1's exact statement also confirmed: every
  nonterminating orbit's limit "has support between s+1 and 2s nodes," matching the project's own
  citation exactly.
- **Bandeira et al. companion work — FOUND and CONFIRMED: `arXiv:2502.16227`, "The Lovász number
  of random circulant graphs" (Feb 2025, ~7 months before this project's work).** Its Theorem 1,
  verbatim: `√n ≤ E θ(G) ≤ C√(n log log n)`. The lower-bound proof, verbatim: the SAME argument
  this project's own audit independently derived (`θ(G)θ(Ḡ)=n` for vertex-transitive graphs + `G
  =d Ḡ` at p=1/2), reached via Jensen's inequality on the log rather than AM-GM — an equivalent
  route to the identical exact result. **`E[θ]≥√n` is definitively `KNOWN-BY-GENERAL-THEOREM`,
  already published.** The companion paper does NOT discuss variance/concentration of
  `θ(G)/√n - 1` at all, so the audit's own `Var(log θ/√n) ∝ n^-0.96` finding (§ 2, still the
  strongest single novel candidate in this whole audit) remains unaddressed by this primary source.
- **Chen/Liu/Liu/Li/Aihara 2012 (DNB, PMID 22461973) — OPENED (PMC3314989, open access) and
  CHECKED: structural mismatch found.** DNB's 3 published criteria (intra-group correlation up,
  inter-group correlation down, group SD up) are tracked WITHIN ONE SYSTEM over time ("an
  individual-based prediction," the paper's own words) — NOT a comparison between a manipulated
  and a reference system. H-B3-1q's actual design (static/per-season sign-count comparison BETWEEN
  Peter and Paul lakes) does not track any of DNB's three specific conditions. **Resolved: NOT
  `KNOWN-SAME-RESULT-DIFFERENT-LANGUAGE` via DNB** — the earlier `INCONCLUSIVE-LITERATURE-COLLISION`
  flag for this specific candidate is closed (a closer match may still exist elsewhere, unsearched).
- **Baryshnikov 2022 (chirality, `arXiv:1909.09846`) — OPENED directly.** Definition 2.6 confirmed
  to match the project's own implementation exactly (project's `L`/`N` = paper's `N`/`N̄`, same
  `s<t`/`s>t` split, correctly renamed not incorrectly redefined). Remark 2.7, verbatim: positive
  drift should produce more `N`-bars (paper's notation) than `N̄`-bars — translating to this
  project's labels, `chirality_excess` should DECREASE (correlate NEGATIVELY) with positive trend.
  Checked against Track 1's own correlation measurements: **2 of 3 lakes match this prediction in
  sign** (lower_zurich, windermere both negative) **but loch_leven does not** (positive) — a
  partial match consistent with real ecological data (seasonal, non-stationary) not behaving like
  the paper's idealized constant-drift Brownian motion, and further supporting (not contradicting)
  Track 1's finding that chirality is not simply trend-slope renamed.

**Not completed** (diminishing returns given session scope — flagged for a future session if
pursued): Trefethen & Embree "Spectra and Pseudospectra" Ch. 16 citation verification (currently
unquoted in H-B2-1u/decision.md, possibly `[MEMORY]` passed off as `[DOCS]`); a literature search
for certified-accuracy Kreiss-constant numerical algorithms (criss-cross/level-set methods) that
might make the arc's own non-converging grid-search moot.

## 8. Updated final verdict (supersedes § 5 for the checked clusters)

The Lovász and Forsythe clusters' remaining open items are now resolved by primary sources rather
than `[UNKNOWN-BLOCKED]`: `E[θ]≥√n` is confirmed published (not novel); the Forsythe "minimal
dimension" question is confirmed genuinely open (not settled) but this project's own search of it
remains methodologically inconclusive, not decisive. Neither changes § 5's overall verdict — the
project has zero confirmed new external contributions among currently registered results — but
both now rest on primary-source verification instead of an infrastructure gap.

## 9. Deepening the top candidate (H-CAT31-3, executed 2026-09-10, same session) — REJECTED for
the clean `-1` exponent, but the phenomenon survives as a precise, still-unexplained measurement

Per direct user request, the single strongest surviving candidate from §§ 2/8
(`Var(log θ/√n) ∝ n^-0.96`, estimated on 9 noisy points with reps tapering to 6 at the largest
`n`) was deepened: a new experiment (`H-CAT31-3`, `experiments/20260910-lovasz-theta-variance-
scaling-cat31-3/`) re-ran the same, already-verified `theta_via_lp` primitive on a wider range
(`n=32..3000`, capped below the originally-requested 4096 by a disclosed compute-cost finding —
LP solve time scales closer to `O(n^3)`-`O(n^4)` than assumed in this regime, benchmarked
directly: 0.17s/0.94s/6.68s/34.38s/88.68s at n=500/1000/2000/3000/4096) with far more replicates
(40-300 per point, vs the original's 6-25) and a pre-registered kill criterion (95% CI must
contain `-1.0` AND exclude both `-0.5` and `-2.0` to count as `CONFIRMED`).

**Result: weighted-OLS slope `-0.9126`, SE `0.0264`, 95% CI `[-0.9751, -0.8501]` — excludes
`-1.0` cleanly.** `REJECTED` per the pre-registered criterion — this is an observed exponent
noticeably different from `-1`, not a power-shortfall. A stability check (slope on the
`n=32..1024` half `-0.900` vs the `n=256..3000` half `-0.897`) shows no drift toward `-1` as `n`
grows.

**CALIBRATION CORRECTION (2026-09-10, user-caught overclaim in the first version of this
section):** the stability check was originally described as "arguing against"/"excluding" a
finite-size-correction explanation — too strong. Precise statement: **no detectable drift toward
`-1` over `n=32..3000`; a simple finite-range-correction explanation is disfavored, but an
asymptotic `-1` beyond the observed range is NOT ruled out** — in particular a slowly-varying
correction `Var(X_n) = C*n^-1*L(n)` (e.g. a logarithmic factor) could produce an effective
exponent near `-0.9` across several decades of `n` without the split-half check detecting it.
Full corrected discussion in the experiment's own `decision.md`.

**This is still a genuine, well-powered negative result, not an inconclusive one** — the CI is
tight enough (half-width ~0.06) to discriminate `-1` from its neighbors, not merely too wide to
say anything. The underlying phenomenon survives at a more precisely measured, but no longer
"clean-looking," exponent (`~-0.91`, not `~-1`). Per the audit's own novelty vocabulary, this
downgrades the finding from `POSSIBLE-NOVEL-SPECIAL-CASE` (§ 2's preliminary framing) to
`BENCHMARK-SPECIFIC-NUMERIC-RESULT` — a precise empirical number without an accompanying
structural explanation or candidate theorem, per `research-methodology.md`'s own Q6 discipline
(a numeric fact only becomes a special case once something explains why the number is what it
is). **One-line final status: a robust, unexplained empirical concentration law on random
circulant Lovász theta, with the natural `n^-1` law falsified over the tested range** — not a
discovery, not a failure. The recommended next cheap step is explicitly NOT a bigger sweep at
larger `n`; it is comparing the existing 9 points against a structurally-motivated correction
model (e.g. a logarithmic factor derived from the DFT/RIP structure `theta_via_lp` actually
uses) — an unmotivated multi-model curve-fitting contest on 9 points would not be a valid check.
Full detail, Kill Analysis, and Relaxation Map in
`experiments/20260910-lovasz-theta-variance-scaling-cat31-3/decision.md`.

**Revised final verdict:** among ~33+1 audited claims across this whole exercise, there is still
no confirmed new external scientific contribution — but the project's own single best novelty
candidate has now been tested as rigorously as this session's compute budget allows, and did not
survive as a clean result. This is the correct, honest outcome of taking a candidate seriously
enough to try to kill it, not a failure of the audit.

Total cost: 6 agents (~1.17M combined subagent tokens, ~45 min wall-clock parallel, Track "0")
+ Track 1 (7 local checks, main session) + Track 2 (4 of 6 external checks, main session,
~10 tool calls to arXiv/PMC/Semantic Scholar) + Track 3/§9 (1 new Standard-Ladder experiment,
`H-CAT31-3`, ~48 min wall-clock LP-solve compute, background, main session).
