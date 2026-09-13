# Negative-Space Miner — H-CAT31-3 (Lovász theta variance scaling), 2026-09-13

Run per `/negative-space-miner`. Source discipline: external published literature only, found
live this session via WebSearch/WebFetch (no arXiv/Semantic Scholar MCP calls made this pass —
the project's own same-day `literature_check_2026-09-13.md` already used those channels for the
adjacent novelty question; this pass deliberately used WebSearch/WebFetch as a second, independent
channel rather than re-querying the same APIs). Every source below carries the evidence marker it
earned: `[VERIFIED-REAL]` = fetched and read (abstract/theorem-level) via WebFetch or quoted
directly in WebSearch's synthesis with a resolvable URL; `[INFERRED]` = derived from confirmed
facts; `[UNKNOWN]` = not independently confirmed to primary-source standard this pass.
Per Hard Rule 2, the project's own null_results (4 independent failed attempts to control theta's
LP-optimizer sensitivity via worst-case vertex-jump geometry) are treated as already mined and are
**not** re-examined here — this run is scoped to external literature only.

---

## Stage -1 — Topic filter

**Question:** does an aggregated failure map already exist for "why do concentration-of-measure
proofs succeed for some combinatorial-optimization/SDP-relaxation statistics and fail for others"?

**Answer: partially yes, and this lowers the ambition of this run explicitly, per the skill's own
instruction.** Sourav Chatterjee's monograph *Superconcentration and Related Topics* (Springer,
2014) `[VERIFIED-REAL — found via WebSearch, Google Books listing confirms scope]` already
synthesizes a cross-domain theory (superconcentration, chaos, multiple valleys) linking Gaussian
concentration failures/successes across spin glasses, first-passage percolation, and related
models. Warnke's "method of typical bounded differences" is itself framed (in its own abstract, per
WebFetch) as a methodological fix motivated by exactly the failure mode this run is mining. **What
is NOT already aggregated:** neither of these existing syntheses mentions SDP-relaxation values
(Lovász theta, max-cut SDP) at all — confirmed by a dedicated search this pass (see Stage 1,
category "SDP/theta + superconcentration") that came back empty. So: the *general* theory of
why-concentration-succeeds-or-fails is a mature, aggregated field (Chatterjee's book is the
existing registry) — this run's honest contribution, if any, is narrower: confirming that this
existing theory has never been brought into contact with the SDP/theta family at all, and
assembling the specific external conflict-map rows that would be needed to do so. This is a
**confirmation of an existing gap**, not a new synthesis from scratch.

---

## Stage 0 — Baseline

1. **Dominant theory:** concentration of combinatorial-optimization and SDP-relaxation statistics
   around their mean is established via the bounded-differences (McDiarmid) inequality and its
   variance form (Efron-Stein), extended where needed by Talagrand's convex-distance inequality and
   martingale/Azuma edge-exposure arguments. `[VERIFIED-REAL]` — corroborated by the project's own
   `literature_check_2026-09-13.md` (Efron-Stein-Steele row) and independently by this pass's
   WebSearch on Efron-Stein (UCLA lecture notes, CMU 36-788 scribe notes).
2. **Assumed mechanism:** if altering one input coordinate (one edge, one weight) changes the
   statistic by at most `c_k` (its Lipschitz/sensitivity constant), then `Var(f) ≲ Σc_k²`, and
   sub-Gaussian tail bounds follow. `[VERIFIED-REAL]`.
3. **Key confirming observations typically cited:** TSP tour-length concentration (Steele 1981,
   Rhee-Talagrand) `[WEAK — cited by name in secondary sources, not independently fetched this
   pass]`; `θ(G(n,1/2))` concentrating in a `polylog(n)`-width window (Arora-Bhaskara 2011)
   `[VERIFIED-REAL — already primary-source-confirmed in the project's own literature_check]`;
   SDP relaxations of chromatic number concentrating in constant-length intervals for sparse random
   graphs `p < n^{-1/2-ε}` (Coja-Oghlan and coauthors) `[VERIFIED-REAL — confirmed this pass via
   WebSearch synthesis, matches the project's own prior finding]`.
4. **Variables the theory considers essential:** per-coordinate sensitivity `c_k`, number of
   independent inputs `n`, independence/weak-dependence structure.
5. **What the theory should predict if true:** for a graph statistic with `O(1)` per-edge
   sensitivity among `Θ(n²)` edges, the *naive* bound gives `Var = O(n²)` (i.e. std-dev `O(n)`) —
   this is almost always far weaker than the true fluctuation scale for any statistic anyone
   actually cares about. The theory's own naive form therefore predicts near-vacuous bounds by
   default; the interesting empirical question — and the one this mining run targets — is which
   *refinements* recover tightness, under what conditions, and which statistics resist even the
   refinements.

---

## Stage 1 — Search for negative space

Queries run this pass (separate, not OR-combined), each reported with what it returned:

| # | Query | Category | Result |
|---|---|---|---|
| 1 | `second-order Poincaré inequality Chatterjee eigenvalue fluctuations concentration failure bounded differences too weak` | boundary/methodological | Confirmed Chatterjee's 2007/2009 second-order Poincaré framework (`arXiv:0705.1224`) as the standard fix for eigenvalue-fluctuation CLTs where naive bounds are insufficient |
| 2 | `Efron-Stein inequality loose combinatorial optimization variance overestimate underestimate` | null/boundary | Confirmed Efron-Stein is a variance *upper* bound (not two-sided) and that it "avoids pessimistic worst-case bounds like those underlying McDiarmid's" — i.e. the field already flags McDiarmid specifically, not Efron-Stein, as the pessimistic one |
| 3 | `"bounded differences" concentration inequality fails combinatorial optimization value sharp variance` | **mandatory named-debate category** | **Direct hit**: Warnke, "On the method of typical bounded differences" (`arXiv:1212.5796`, *Combinatorics, Probability and Computing* 2016) — an explicitly named methodological fix for exactly this failure mode |
| 4 | (follow-up fetch) `arxiv.org/abs/1212.5796` | same | `[VERIFIED-REAL]` — fetched directly; mechanism confirmed: worst-case Lipschitz constants "often make the resulting bounds too weak to be useful"; fix relaxes the Lipschitz condition to a high-probability event `Γ` |
| 5 | (follow-up fetch) `arxiv.org/html/2407.12672` | same cluster | `[VERIFIED-REAL]` — "A concentration inequality for random combinatorial optimisation problems" (2024). Direct numeric comparison for minimum spanning trees: naive bounded-differences gives `O(n)` std-dev, Talagrand gives `O(√n)`, this paper's "patchability"/red-green-split method gives `O(n^{-1/4})` relative width (weaker than a prior `O(n^{-1/2})` log-Sobolev result, honestly reported as such in the paper) |
| 6 | `semidefinite programming relaxation value concentration random graph max-cut theta chromatic number variance` | domain-specific | No new negative-space hit beyond what the project's own literature_check already had (Coja-Oghlan sparse-regime results); confirms no broader SDP-concentration-failure literature exists beyond that cluster |
| 7 | `spin glass free energy concentration McDiarmid too weak Guerra Talagrand variance order` | **mandatory named-debate category** | **Direct hit**: superconcentration/no-superconcentration dichotomy in spin glasses (see Stage 2 rows) |
| 8 | `Chatterjee superconcentration free energy external field variance order Poincaré` | follow-up | `[VERIFIED-REAL]` — confirmed the explicit switching condition (external field present/absent) and the with-field paper's exact variance-order statement `cN ≤ Var(f_N) ≤ CN` |
| 9 | `sharp threshold versus coarse threshold graph property Friedgut Kalai symmetry concentration failure` | **mandatory named-debate category** | **Direct hit**: Friedgut-Kalai (1996) sharp-threshold-for-symmetric-properties theorem, and Friedgut's separate coarse-threshold characterization for "junta-like/local" properties — a second, independent named dichotomy |
| 10 | `publication bias concentration of measure results file drawer problem statistics` | Exhaustion Completeness check | General file-drawer literature confirmed as a real, well-documented phenomenon in science broadly; **no domain-specific paper found** documenting file-drawer bias specifically within the concentration-inequality literature — see Stage 3 for how this is handled |
| 11 | `"Lovász theta" OR "SDP value" superconcentration OR "second-order Poincaré" random graph` | domain intersection | **Confirmed absence**: no source found connecting superconcentration/second-order-Poincaré theory to Lovász theta or any SDP relaxation value. `SOURCE_NOT_FOUND` for this exact intersection — consistent with, not proof of, a genuine gap |
| 12 | `circulant graph symmetry concentration inequality group invariance variance reduction random matrix` | mechanism-support | Found "Group Symmetry and Covariance Regularization" (`arXiv:1111.7061`) `[VERIFIED-REAL — WebSearch synthesis with resolvable URL, abstract-level only, not independently fetched]`: projecting onto a circulant/group-invariant fixed-point subspace measurably reduces estimator variance versus the unconstrained estimate — a statistical-estimation result, not a concentration-of-measure result per se, cited here only as *mechanism-support* for Cluster B (Stage 3), not as a conflict-map row of its own |

**Absence-is-not-evidence discipline applied:** query 11's empty result is recorded as
`SOURCE_NOT_FOUND`, not interpreted as "concentration for theta definitely fails" or "definitely
holds" — it means nobody has yet asked the question with this specific toolkit.

---

## Stage 2 — Conflict map

| # | Source | Year | Effect size | Expected | What happened | Method | System | Conditions | Explanation (working) | Tag |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Warnke, "Method of typical bounded differences," `arXiv:1212.5796` `[VERIFIED-REAL]` | 2012/2016 | Bound so loose as to be "not useful" (qualitative — no single number given in the fetched abstract) | Standard McDiarmid should give a usable concentration bound | Worst-case Lipschitz constant `c_k` is dominated by rare configurations; naive bound vacuous | McDiarmid/bounded-differences (baseline) vs. relaxed-to-high-probability-event fix | Reverse `H`-free process (`H` 2-balanced) | Worst-case single-step change ≫ typical single-step change | Worst-case-vs-typical Lipschitz mismatch | methodological |
| C2 | "A concentration inequality for random combinatorial optimisation problems," `arXiv:2407.12672` `[VERIFIED-REAL]` | 2024 | Naive: `O(n)` std-dev; Talagrand: `O(√n)`; this paper: `O(n^{-1/4})` relative width (weaker than a cited prior `O(n^{-1/2})` log-Sobolev result) | A single "best" method should dominate | Different methods give different, non-monotonically-improving rates; naive method is the weakest by a wide margin | "Patchability" + red-green-split + Talagrand on a dual problem | Minimum spanning tree (random edge weights) | Patchability parameter `ℓ(ℱ)`, certifiability | Method choice, not just tightness of a single universal inequality, determines the achievable rate | methodological |
| C3 | Chatterjee, superconcentration (SK model, no external field) — *Superconcentration and Related Topics* `[VERIFIED-REAL, WebSearch-synthesized with resolvable citation]` | ~2008/2014 | `Var(free energy)` is *smaller order* than the generic Poincaré-implied order (superconcentration) | Poincaré/bounded-differences order should hold generically | Variance collapses to a smaller order than the naive bound predicts | Gaussian concentration theory / second-order Poincaré | Sherrington-Kirkpatrick spin glass, `h=0` | No external field (full symmetry of `±1` spin flip) | Symmetry removes independent "surprise directions," collapsing effective degrees of freedom | model-dependent |
| C4 | "Fluctuations of the free energy in the mixed `p`-spin models with external field," `arXiv:1509.07071`, *PTRF* 2016 `[VERIFIED-REAL]` | 2016 | `cN ≤ Var(f_N) ≤ CN` (standard order, explicit two-sided bound) | Should match C3's superconcentrated (smaller) order if the mechanism were universal | Variance reverts to the *generic* Poincaré order once an external field is present | Same family (mixed `p`-spin SK-type models) | Same family, `h²+β₁² ≠ 0` | External field breaks the `h=0` symmetry | Symmetry-breaking restores the generic (non-superconcentrated) order | model-dependent |
| C5 | Friedgut & Kalai, "Every monotone graph property has a sharp threshold" (1996) `[VERIFIED-REAL — WebSearch synthesis, standard result, Semantic Scholar listing confirms]` | 1996 | Sharp threshold width `o(1)` relative to threshold location | — (this IS the positive baseline for this cluster) | Every *symmetric* (vertex-transitive-group-invariant) monotone graph property concentrates sharply around its threshold | Fourier-analytic / hypercontractivity (KKL-type) argument | Any monotone graph property invariant under a transitive automorphism group | Full symmetry (transitive group action) | Symmetry forces influence to spread evenly across coordinates, which is what drives sharp thresholds in the KKL framework | model-dependent |
| C6 | Friedgut's coarse-threshold characterization (companion result, same literature cluster) `[VERIFIED-REAL — WebSearch synthesis]` | ~1999 | Threshold width `Θ(1)` relative to location (does NOT shrink) | Symmetric-group heuristic (C5) might suggest sharpness is generic | Properties "approximable by a local property" (determined by a small/constant-size substructure — a junta) have genuinely coarse thresholds, e.g. triangle-containment | Same Fourier-analytic framework | Junta-like / locally-determined monotone properties | Property effectively depends on `O(1)` coordinates, not the full symmetric structure | A different notion of "structure" (junta-ness) than C5's symmetry defeats concentration even under nominal symmetry of the ambient probability space | model-dependent |
| C7 | Arora & Bhaskara, "A note on the Lovász theta number of random graphs" (2011) `[VERIFIED-REAL — already primary-source-confirmed in project's own literature_check]` | 2011 | `Pr[|θ(G)-μ|>t] ≤ exp(-t^{4/3}/(C log³n))` — `polylog(n)`-width concentration | Naive McDiarmid on theta's edge-sensitivity would give a much wider (weaker) window | A refined (non-naive) argument achieves genuinely tight concentration | Refined martingale / edge-exposure argument (not stated as naive bounded-differences) | `G(n,1/2)`, dense Erdős–Rényi | Dense regime, unstructured (no cyclic symmetry) | Refinement of the exposure argument recovers tightness even without extra symmetry | context-dependent |
| C8 | Coja-Oghlan and coauthors, SDP relaxations of chromatic number `[VERIFIED-REAL — confirmed in project's own literature_check, re-confirmed this pass]` | various | Constant-length-interval concentration | — | Concentration holds, but only in the *sparse* regime `p < n^{-1/2-ε}` | SDP-specific + sparse-graph techniques | `G(n,p)`, sparse | `p < n^{-1/2-ε}` | Sparsity itself may be doing the work that symmetry does in C5/C3 — untested link, flagged not asserted | scale-dependent |
| C9 | Bandeira, Błasiok, Dmitriev, Faure, Kireeva, Kunisky, "The Lovász number of random circulant graphs," `arXiv:2502.16227` `[VERIFIED-REAL — primary-source-confirmed in project's own literature_check]` | 2025 | Even the *mean*'s leading constant is unresolved (`√n ≤ E θ(G) ≤ C√(n log log n)`, gap unclosed) | A 2025 paper on the field's own flagship structured (cyclic-symmetric) ensemble should have settled at least the mean | Field has NOT yet reached the variance/concentration question for this exact structured, highly-symmetric case | Direct SDP analysis + conjecture (open) | Random dense circulant graphs, `p=0.5` | Cyclic symmetry (self-complementary ensemble) | Absence of result, not a failed result — informative boundary, not a null | unexplained (absence) |

---

## Stage 3 — Failure structure

### Clustering

**Cluster A — Worst-case-vs-typical sensitivity mismatch** (C1, C2, C7 as the "fix succeeds" pole).
Shared condition across C1/C2: the statistic's *worst-case* per-coordinate Lipschitz constant is
achieved on a rare/atypical configuration, so a bound built from it is far looser than the true
fluctuation scale. C7 shows the "fix succeeds" pole directly for a theta-adjacent statistic
(dense Erdős–Rényi, not circulant).

**Cluster B — Symmetry-breaking as a variance-order switch** (C3↔C4, C5↔C6). Shared condition:
both pairs show a *dichotomy* where the presence/absence of a specific kind of structure
(external field; junta-ness) switches the variance/threshold behavior between two qualitatively
different orders, not just two different constants.

### Ruling Theory Trap gate (mandatory)

For Cluster A, walking every candidate hidden variable from the mandated list:

- **Scale** — considered and rejected as the primary driver: C1 (reverse `H`-free process) and C2
  (MST) operate at different scales/regimes but share the *same* mismatch mechanism regardless of
  scale; scale modulates magnitude, not whether the mismatch occurs.
- **Time** — rejected: none of C1/C2/C7 are time-evolving processes in the relevant sense (C1's
  process is technically a random graph process, but the failure mode is about spatial/coordinate
  sensitivity at a fixed step, not temporal drift).
- **Process stage** — rejected for the same reason as time; not applicable to static SDP values
  like C7/theta.
- **Hidden sample heterogeneity** — considered seriously, rejected as primary but kept as a
  contributing factor: MST edge weights (C2) could have heterogeneous distributions driving some
  of the rate gap, but the paper's own comparison (naive vs. Talagrand vs. patchability, all on the
  *same* weight distribution) isolates the method, not the data, as the source of the gap — so
  method choice dominates over heterogeneity in this specific evidence.
- **Threshold effect** — rejected as the primary explanation for Cluster A specifically (that is
  Cluster B's mechanism, not this one) — kept separate rather than merged, per the Ruling Theory
  Trap's ≥2-candidates rule below.
- **Nonlinearity** — considered: MST/graph-optimization values ARE highly nonlinear in the input
  weights, and this is arguably WHY worst-case Lipschitz constants get so large relative to typical
  ones (a single reweighted edge can occasionally re-route the entire tree). This is not rejected —
  it is folded into the "worst-case-vs-typical mismatch" framing itself as the underlying cause of
  the mismatch, not a separate candidate.
- **Variable interaction** — considered and rejected as separately explanatory: interaction between
  coordinates is implicit in any graph optimization value; C1/C2 do not indicate interaction
  strength itself is the discriminating variable (both high- and low-interaction sub-cases exist
  within "combinatorial optimization" generally, and the papers don't split on this axis).
- **Reverse causation** — not applicable (these are proof-technique results about a fixed
  mathematical object, not an observational causal claim).
- **Selection effects** — relevant, but reassigned to the Exhaustion Completeness check below
  rather than kept as a per-cluster candidate, since it operates at the level of "which results get
  published" rather than "which mechanism explains a given result."
- **Measurement error** — not applicable; these are exact mathematical statements, not
  noisy measurements.
- **Feedback loop** — rejected: no feedback structure in either C1's process construction or C2's
  static MST optimization.
- **Adaptation** — rejected: no adaptive/learning component in any of C1/C2/C7.
- **Environmental regime** — this is effectively Cluster B's variable (symmetry present/absent), not
  Cluster A's — kept separate, not merged, matching the ≥2-candidates rule below at the
  cross-cluster level.
- **Decline effect** — not applicable; these are proof results, not replicated empirical effect
  sizes across studies over time.

**Result: exactly one retained candidate for Cluster A** (worst-case-vs-typical Lipschitz mismatch,
with nonlinearity folded in as the underlying driver of the mismatch itself, not a second
independent candidate) — no ≥2-candidate split required here.

For Cluster B, the same walk-through:

- **Scale** — rejected: C3/C4 are both the `N→∞` mixed `p`-spin SK-type model; C5/C6 are both
  asymptotic-in-`n` graph-property statements. Scale is held fixed within each pair; the switch is
  the external field/junta-ness, not `N` or `n` itself.
- **Threshold effect** — genuinely a strong second candidate here (a threshold IS what C5/C6 are
  about literally). **Per the ≥2-candidates rule: threshold effect and symmetry-breaking are BOTH
  retained as competing (not merged) explanations for Cluster B**, since C5/C6's own vocabulary
  ("sharp" vs. "coarse" threshold) is threshold-shaped language, while C3/C4's vocabulary
  ("superconcentration," "external field") is symmetry-shaped language — the two source pairs use
  genuinely different descriptive frames for what may or may not be the same underlying mechanism.
  This is carried into Stage 4 as two hypotheses that partially overlap rather than one hypothesis
  asserting they are identical.
- **Nonlinearity** — considered: the free-energy functional and monotone graph properties are both
  nonlinear, but nonlinearity is present on BOTH poles of each pair (with and without field; sharp
  and coarse threshold) — it does not discriminate, so rejected as the switching variable here
  (unlike Cluster A, where it was folded into the retained explanation).
- **Variable interaction** — considered: junta-ness (C6) IS a statement about interaction being
  concentrated on `O(1)` coordinates rather than spread out — this overlaps with, rather than
  competes against, the symmetry-breaking framing, and is treated as the same underlying phenomenon
  described at the "coordinate interaction" level instead of the "group-symmetry" level, not a
  third independent candidate.
- **Environmental regime** — this is essentially a restatement of "external field present/absent"
  for C3/C4; not a separate candidate, same as symmetry-breaking.
- All remaining candidates (time, process stage, hidden sample heterogeneity, reverse causation,
  selection effects, measurement error, feedback loop, adaptation, decline effect) — rejected for
  Cluster B for the same reasons given under Cluster A (not applicable to static proof-theoretic
  results about fixed mathematical objects).

**Result for Cluster B: two retained, competing candidates** — symmetry-breaking and threshold
effect — carried forward as two related but distinct Repair Hypotheses in Stage 4.

### Exhaustion Completeness check (mandatory)

**Generic-list-only or domain-exhaustive?** The retained candidates (worst-case/typical mismatch
for Cluster A; symmetry-breaking and threshold-effect for Cluster B) plausibly cover the
*proof-technique* explanation space reached by this search, but the domain-specific question this
run was explicitly asked to check — **could the same publication-bias mechanism that inflates
positive concentration results also be operating symmetrically on the negative side?** — deserves
its own answer, not an assumption.

**Answer, based on what Stage 1 query 10 and the conflict map itself actually show:** yes, a
specific, asymmetric version of this mechanism is visible directly in the conflict map, not merely
plausible in the abstract. Every negative-space row found this pass (C1, C2's naive-bound
comparison, C4, C6) is NOT a standalone "we tried to prove concentration and failed" paper — each
negative result appears **embedded as motivation or a comparison baseline inside a paper whose main
contribution is the positive fix or the positive companion result.** Warnke's own abstract (C1)
states the naive-bound failure as the *reason for the paper*, not as its finding. The MST rate
comparison in C2 exists only as one row of a table inside a paper about the new method. C4 and C6
exist as the "complementary" half of a two-paper (or two-section) structure whose other half is the
positive result (C3, C5). **No paper in this search existed solely to report a concentration
failure with no accompanying fix or positive counterpart.** This is itself informative: it suggests
the discipline's version of the file-drawer effect is not "negative results go completely
unpublished" (the classical social-science framing) but "negative results are published, but only
as scaffolding for a positive result in the same paper" — a structurally different, and arguably
more severe, form of the bias, because it means a negative-space search like this one will
systematically *undercount* pure failures relative to fixed ones, having no channel to find a
failure that nobody has yet fixed. **This is recorded as a limitation of this run's own conflict
map**, not resolved further — searching for genuinely standalone negative-result papers in this
specific niche (concentration of SDP/combinatorial-optimization values) was attempted (queries 3,
6) and came back with only the embedded-negative-result pattern above, consistent with, not proof
of, this being the dominant reporting mode in this field.

---

## Stage 4 — Repair Hypotheses

Two hypotheses, not five — per the skill's own preference for fewer, well-justified hypotheses.
`H2a`/`H2b` are the two competing Cluster-B candidates kept genuinely separate rather than merged
into a single overclaiming hypothesis (per the Ruling Theory Trap's ≥2-candidates rule above).

### Hypothesis H1 — Worst-Case/Typical Sensitivity Mismatch

**Mechanism:** for a combinatorial-optimization or SDP-relaxation value `f(X)` on `n`
weakly-dependent inputs, standard bounded-differences concentration is loose or vacuous exactly
when `f`'s worst-case single-coordinate Lipschitz constant `c_k` is achieved only on a rare,
atypical input configuration, while `f`'s *typical* single-coordinate sensitivity (conditioned on a
high-probability event `Γ`) is much smaller. Tight concentration is recovered whenever a method
explicitly exploits this gap (Warnke's relaxed-Lipschitz-on-`Γ` construction; the 2024 paper's
patchability/certifiability parameter `ℓ(ℱ)`; Arora-Bhaskara's refined edge-exposure martingale for
theta).

**Positive results it explains:** C7 (theta on `G(n,1/2)` — refined martingale beats naive bound);
C2's own patchability result relative to its own naive baseline (both reported within the same
paper).

**Negative results it explains:** C1 (naive McDiarmid vacuous for the reverse-`H`-free process); C2's
own naive-bound row (`O(n)` std-dev for MST, essentially uninformative).

**Switching variable (boundary condition):** the ratio `ρ = c_typical(Γ) / c_worst-case`, together
with `P(Γᶜ)`. C2's own Theorem 2.5 gives a genuinely concrete, sourced quantitative relationship
for the MST case specifically: relative concentration width `∝ (λ/m)^{q/(q+1)}` where `λ` is the
patching cost and `q` is the certifiability exponent — i.e. the achievable rate is a *computable
function* of how cheaply an almost-optimal structure can be "patched" to feasibility, not a vague
qualitative judgment.

**Duhem-Quine qualifier:** H1 is compatible with C1 under Warnke's own measurement apparatus (an
explicit high-probability event `Γ` with a stated tail bound `P(Γᶜ)`, and a companion "typical"
Lipschitz constant defined only on `Γ`) — if a different paper's implicit definition of "typical"
sensitivity were used instead, C1's specific numbers would not transfer. H1 is compatible with C2
under that paper's own patchability/certifiability framework specifically (`ℓ(ℱ)`-certifiable
families) — the `O(n^{-1/4})` rate is NOT claimed to be universal; the paper itself reports a prior,
stronger `O(n^{-1/2})` log-Sobolev result for the same MST problem, so H1 does not claim the
patchability method is the *best* available fix, only that it is *a* fix exploiting the same
mismatch mechanism. H1 is compatible with C7 only under the dense, unstructured `G(n,1/2)` regime —
it makes no claim about the circulant case (C9), where no refined method has been attempted at all.

**Rescue-unfalsifiability check:** does the `Γ`/`ρ` framing explain away literally any negative
result? No — it fails a concrete, statable test: if a statistic's naive bound is loose AND no
`Γ`-conditioned typical-Lipschitz argument closes the gap after being attempted (as is currently
true for C9 — the circulant theta expectation itself is unresolved, so nobody has even reached the
variance-refinement stage), H1 predicts the negative result should persist, and does not retroactively
explain it away as "must be some untried `Γ`." This satisfies fix (a): a concrete, checkable
quantitative relationship exists (C2's own `(λ/m)^{q/(q+1)}` form), not merely a qualitative escape
hatch.

---

### Hypothesis H2a — Symmetry-Breaking Switch (Cluster B, symmetry framing)

**Mechanism:** when a random structure carries an unbroken symmetry (SK model with `h=0`; a monotone
graph property invariant under a transitive automorphism group), the statistic's fluctuations are
constrained to move coherently across many coordinates at once, collapsing the number of effectively
independent "surprise directions" and producing either superconcentration (variance smaller than the
generic Poincaré order, C3) or a sharp threshold (C5). Breaking the symmetry (external field, C4)
restores the generic variance order.

**Positive results it explains:** C3 (SK, `h=0`, superconcentration); C5 (symmetric monotone
properties, sharp threshold).

**Negative results it explains:** C4 (SK with field, standard `cN≤Var≤CN` order — i.e. "negative"
relative to the superconcentration baseline C3 sets, not negative in an absolute sense).

**Switching variable (boundary condition):** presence/magnitude of a symmetry-breaking term. C4's
own paper states the concrete, numeric condition directly: `h² + β₁² ≠ 0` triggers the standard
order `cN ≤ Var(f_N) ≤ CN`; by direct complementarity, C3's own regime is exactly `h=0` (and,
implicitly, `β₁=0` for the pure even-`p` case Chatterjee treats). This is a genuine, sourced,
binary numeric threshold — not a vague "sufficiently symmetric" qualifier.

**Duhem-Quine qualifier:** H2a is compatible with C3 under Chatterjee's own even-`p`, `h=0`
construction specifically — the superconcentration result is proved for that family, not asserted
for all Gaussian-dependent statistics generically. H2a is compatible with C4 under that paper's own
stated condition `h²+β₁²≠0` — if a future paper found superconcentration surviving at small nonzero
field (a near-`h=0` regime), that would directly falsify H2a's binary framing, not merely narrow it
(see Stage 5).

**Rescue-unfalsifiability check:** the `h²+β₁²≠0` threshold is an actual number from the source
(zero vs. nonzero), satisfying fix (a) directly — this is as concrete as a threshold gets.

---

### Hypothesis H2b — Junta/Local-Determination Switch (Cluster B, threshold framing)

**Mechanism:** a monotone property's threshold sharpness is governed by whether the property is
"approximable by a local property" — effectively determined by a constant-size substructure (a
junta) — rather than genuinely spread across all `n` coordinates. Junta-like properties (C6,
triangle-containment) have coarse thresholds regardless of the ambient symmetry group being fully
transitive; genuinely global, non-junta-approximable properties (C5) have sharp thresholds.

**Positive results it explains:** C5 (non-junta, symmetric monotone properties — sharp threshold).

**Negative results it explains:** C6 (junta-approximable properties — coarse threshold, even though
the *ambient* probability space is still fully symmetric under the same automorphism group as C5's
examples).

**Switching variable (boundary condition):** whether the property is approximable, within a stated
error, by a function of a constant number of coordinates (a formal junta-distance parameter, as
used in Friedgut's own junta theorem — not independently re-derived with exact constants in this
pass; flagged below).

**Duhem-Quine qualifier:** H2b is compatible with C5 under Friedgut-Kalai's transitive-automorphism-
group framework specifically. H2b is compatible with C6 under Friedgut's own "approximable by a
local property" characterization — a property that is symmetric under the automorphism group
(satisfying H2a's condition) can STILL be junta-like (triangle-containment IS invariant under the
full symmetric group `S_n` acting on vertices, yet has a coarse threshold) — this is the concrete
reason H2a and H2b are kept as separate, non-merged hypotheses: **H2a's condition (unbroken
symmetry) is not sufficient for H2b's positive outcome (sharp threshold/tight concentration);
junta-ness is an independent axis that can defeat concentration even under full symmetry.**

**Rescue-unfalsifiability check:** this is the weaker of the two Cluster-B hypotheses, honestly
flagged. Unlike H2a's binary `h²+β₁²≠0` threshold, this pass did not locate an independently-fetched,
exact numeric "junta-distance" threshold from Friedgut's own theorem statement (only a WebSearch
synthesis of it) — per the rescue check's own instructions, **H2b is downgraded explicitly to "one
of several competing, unestablished hypotheses"** rather than presented as confirmed with a
numeric threshold. Applying fix (b), not fix (a), here.

---

## Stage 5 — Unexpected predictions

**For H1 (worst-case/typical mismatch):** if H1 is true, then for the circulant-theta case (C9)
specifically, we should observe that a `Γ`-conditioned refinement — bounding theta's *typical*
sensitivity to a single edge flip, conditioned on the circulant graph's degree sequence staying near
its mean — closes most of the gap between a naive McDiarmid bound and the field's own genuinely
observed (if not yet proven) tight behavior, whereas the standard/naive McDiarmid bound applied
directly to theta's LP formulation would predict a variance far larger than `O(1/n)`. **The
standard model (plain bounded differences) would rather predict** a variance bound many orders too
loose to be informative at all — consistent with the field not having attempted this calculation
(C9), not with the calculation having been attempted and failed.

**For H2a (symmetry-breaking):** if H2a is true, then introducing an explicit symmetry-breaking
perturbation into the random circulant-graph ensemble — e.g. biasing the edge-inclusion probability
`p` away from exactly `0.5` so the ensemble is no longer self-complementary, which is precisely the
project's own claim.md caveat about `p≠0.5` losing the `sqrt(n)`-normalization argument — should, if
the same mechanism operates here as in the SK model, push `Var(log(θ/√n))` toward a *larger* order
than whatever tight order holds at exactly `p=0.5`, mirroring C3→C4's `h=0→h≠0` transition
qualitatively (not quantitatively — H2a's numeric threshold is specific to the SK free-energy
functional and is NOT claimed to transfer numerically to theta). **The standard model would rather
predict** no qualitative change from `p=0.5` to nearby `p`, since naive bounded-differences theory
does not treat self-complementarity as a distinguished point at all.

**For H2b (junta/local-determination):** if H2b is true, then a *different* SDP-relaxation
statistic that is "local" in Friedgut's sense — e.g. a statistic dominated by the count of a fixed
small subgraph pattern rather than a genuinely global spectral/SDP quantity — should show a coarse,
non-shrinking-width concentration behavior even when computed on the SAME symmetric circulant
ensemble that gives tight behavior for theta itself. **The standard model would rather predict**
uniformly tight concentration for any "nice" (bounded-sensitivity) statistic on a symmetric
ensemble, with no distinction between global and junta-like statistics — H2b specifically predicts
this distinction should appear even holding the ensemble's symmetry fixed.

---

## EstimandOps L0 gate (mandatory before finalizing)

**Classification: DESCRIPTIVE.** All three Repair Hypotheses (H1, H2a, H2b) describe how a
proof-technique's success/failure and a statistic's variance *order* covary with a stated structural
condition (typical/worst-case Lipschitz ratio; symmetry-breaking field; junta-approximability) —
they are claims about which regime a given (source, statistic) pair falls into, not causal claims
about an intervention's effect, and not predictive claims about an unobserved new case beyond the
explicit, hedged predictions in Stage 5 (which are themselves flagged as predictions to test, not
established facts). No DAG or identifiability layer is triggered.

---

## What flagged for Stage 6 (Attack) and Stage 8 (Novelty) — explicitly NOT done here

- **Stage 6 (Attack):** not run in this pass, per the calling instructions — requires a separate,
  context-asymmetric agent. The clean handoff block is provided in the final report back, not in
  this file.
- **Stage 8 (Novelty Check):** not run in this pass. Flagged items worth an explicit novelty check
  later: (a) whether H1's `Γ`-conditioned-typical-Lipschitz mechanism has ever been proposed
  specifically for SDP-relaxation values (this pass's query 11 found nothing, consistent with
  novelty but not proof); (b) whether H2a/H2b's *joint* application (both symmetry-breaking AND
  junta-approximability as independent, non-reducible axes for the SAME statistic) has been stated
  as an explicit two-axis framework anywhere, or whether this run's Stage 3 split is itself the
  first time these two literatures (spin-glass superconcentration; graph-property threshold theory)
  have been cross-referenced against each other for this purpose.

---

## Stage 6 — Attack (delegated, context-asymmetric skeptic, 2026-09-13)

**Verdict: WEAKENED**, leaning toward FALSIFIED on the "same-mechanism unification" claim
specifically; the narrow, scope-limited MST rate survives as a much weaker case study, not a
general principle. Three independent, non-overlapping defects found:

1. **The "same mechanism" unification is a category label, not a mechanism.** Warnke's
   Γ-conditioning, the 2024 patchability argument, and Arora-Bhaskara's edge-exposure martingale
   share only the property "beats naive McDiarmid by not using the worst-case Lipschitz constant
   globally" — a property shared by essentially every non-trivial improvement over McDiarmid
   (Talagrand's inequality, log-Sobolev, entropy method, exchangeable pairs). H1 gives no rule for
   choosing among these methods for a NEW problem, so it has zero discriminating power beyond
   "if a refined bound works, it exploited a gap" — true by construction, not a testable mechanism.
2. **The Duhem-Quine "concrete threshold" is not a threshold on the stated switching variable.**
   H1 names `ρ=c_typical(Γ)/c_worst-case` and `P(Γ^c)` as the switching variables, but the cited
   quantitative relationship `(λ/m)^(q/(q+1))` is in DIFFERENT variables (`λ`=patching cost,
   `q`=certifiability exponent, MST-specific), with no value of `ρ` at which naive→tight is stated.
   The citation is decorative for the general claim, load-bearing only for the narrow MST case.
3. **The unfalsifiability escape hatch is not closed.** "No Γ-conditioned argument closes the gap
   after being genuinely attempted" leaves "genuinely attempted" undefined — any future negative
   result can be attributed to an untried Γ rather than to H1 being wrong, exactly the move H1's
   own falsifiability clause claims to forbid.

**Alternative explanation offered by the attacker (not adopted, recorded for completeness):** the
three positive-pole techniques may succeed for unrelated, problem-specific structural reasons
(combinatorially-named rare events for Warnke; direct edge-stability for θ(G(n,1/2)); Talagrand
convex-distance machinery re-narrated for MST) — "worst-vs-typical mismatch" would then be a
post-hoc unifying STORY across three unrelated results, not a shared mechanism. Untested.

**Most dangerous confounder identified:** survivorship/publication bias in the positive pole — all
three positive examples are published SUCCESSFUL refinements; cases where a worst-vs-typical gap
resisted every method don't appear in either pole, because (per this run's own Stage -1/3 finding)
negative results in this literature are published only as internal baselines inside papers with a
positive fix, never as standalone "we tried and failed" reports.

**Citation verification (requested by the attacker, who had no tool access; run separately,
2026-09-13):** all three load-bearing citations independently confirmed real and matching their
claimed content — arXiv:2407.12672 (Joel Larsson Danielsson, "A concentration inequality for
random combinatorial optimisation problems," July 2024, Theorem 2.5 on `(r,λ,ε)`-patchable
families confirmed to exist and match the general shape claimed, exact MST instantiation not
independently re-derived), arXiv:1212.5796 (Warnke 2012/CPC 2016, content matches exactly),
arXiv:2502.16227 (Bandeira et al. Feb 2025, content matches). No hallucinated sources. This closes
the citation-integrity concern but does NOT rescue the three structural defects above, which are
independent of citation accuracy.

**Disposition:** H1 is DOWNGRADED from "mechanism explaining loose-concentration cases" to
"taxonomy label for techniques that improve on McDiarmid" — useful for organizing the literature,
not usable as a predictive or explanatory Repair Hypothesis. Per this skill's own Null Results
Protocol: the conflict map and clustering (Stages 2-3) remain valid for a future attempt; what is
killed is specifically H1 as a unifying mechanism claim, not the underlying observation that a
worst-vs-typical sensitivity gap is real and present in at least 4 independently-sourced cases.
Stage 8 (Novelty Check) is now moot for H1 given the downgrade — not run.

**attack status:** `survived weak attack` is not applicable (attack WAS delegated to a
context-asymmetric agent) — final status is **WEAKENED**, not `survived`.
