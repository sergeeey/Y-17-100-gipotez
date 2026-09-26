# Classification of the 45 `confirmed` hypothesis nodes (2026-09-27)

Source: `registry/graph.yaml` (93 hypothesis nodes: 45 confirmed, 24 killed, 22 lead, 1 blocked, 1 parked). Classified from the node title and fields (`evidence`, `verification_strength`, `l0_type`) ONLY;
the underlying experiments were NOT re-read or re-verified, so every label is `[INFERRED]`. The rubric was fixed before looking at the nodes.

Rubric: **A** reproduction of a known/published result or positive control; **B** a numerical property of the lab's own or literature model; **C** a verification step on an earlier lab node (cross-implementation, replication, robustness, explanation of a prior observation); **D** an explicit candidate new claim.

## Totals

| Category | Nodes |
|---|---|
| A reproduction of known | 3 |
| B property of own model | 26 |
| C verification step on earlier node | 15 |
| D candidate new claim | 1 |
| **Total** | **45** |

By direction: B2 (18) = 9 B + 9 C; B7 (22) = 1 A + 15 B + 6 C; B1 (2) = 2 A; CAT31 (1) B; CAT37 (1) B; CAT56 (1) D.

## Reading

- 15 of 45 (a third) are self-verification steps of the lab, not independent results; independent things established: 26 + 3 + 1 = 30, of which 26 are model-level properties.
- External anchor: 4 nodes (A and D). Novelty was audited for one node only (H-CAT56-2, and there it is `WEAK`); nothing is claimed either way for the B nodes.
- `verification_strength` is set (medium/strong/weak) on only 10 of 45 nodes, the literal `none` on 2, and is empty on 33: the registry records status but almost never the strength of the basis.
- Borderline (B versus C; the split could move by about 5): H-B2-1g, H-B2-1j, H-B2-1l, H-B2-1w, H-B7-19, H-B7-30.

## Table

| # | id | cat | verification_strength | l0 | note | title (first 170 chars) |
|---|---|---|---|---|---|---|
| 1 | H-B1-1a | A | medium | descriptive |  | Riemann zeros r-statistic replicates GUE prediction (Montgomery–Odlyzko) — infrastructure positive control |
| 2 | H-B1-1c | A | weak | descriptive |  | Known-answer test #2: finite-height excess of <r> over the exact sine-kernel limit for the first 100k zeta zeros matches Nishigaki (2025) PTEP finite-N_eff CUE fit |
| 3 | H-B2-1 | B | None | descriptive |  | A concrete Neural-ODE/ResNet layer satisfies the hypotheses of Chernoff's theorem (is a discrete approximation of a C0-semigroup) |
| 4 | H-B2-1b | B | None | descriptive |  | Relaxation Map row 2 from H-B2-1's correction: does the K_j=0/Theorem 3.1 mechanism generalize to a genuine 2D matrix Chernoff block (two distinct eigenvalues)? |
| 5 | H-B2-1c | B | None | descriptive |  | Relaxation Map row 1 from H-B2-1b: does the K_j=0/Theorem 3.1 mechanism survive a non-normal matrix (Kreiss matrix theorem territory, transient growth)? |
| 6 | H-B2-1d | B | None | descriptive |  | Relaxation Map from H-B2-1b (sign structure): does the K_j=0/Theorem 3.1 mechanism survive a mixed-sign spectrum (one growing, one decaying eigenvalue)? |
| 7 | H-B2-1e | B | None | descriptive |  | Combined stress test: does the K_j=0/Theorem 3.1 mechanism survive non-normality AND mixed-sign spectrum SIMULTANEOUSLY (H-B2-1c and H-B2-1d combined)? |
| 8 | H-B2-1f | B | None | descriptive |  | Dimension scale-up from H-B2-1e: does the K_j=0/Theorem 3.1 mechanism survive N=8 (widely-separated 'stiff' eigenvalues, non-normal, mixed-sign)? |
| 9 | H-B2-1g | B | None | descriptive | borderline | Does H-B2-1f's counterintuitive finding (M1 smaller at N=8) survive 5x stronger coupling? Establishes: bound validity and practical usefulness are separate axes |
| 10 | H-B2-1i | C | None | descriptive |  | Is H-B2-1g's M1=158.93 (seed=0, coupling=15) a typical draw, or an unlucky/lucky one? Seed-ensemble test (H-B2-1g's own named open question) |
| 11 | H-B2-1j | B | None | descriptive | borderline | Does the Theorem 3.1 bound stay valid and order-matching at N_DIM=50 (vs N_DIM<=8 tested in every prior H-B2-1* experiment)? LAB.md's own named open item |
| 12 | H-B2-1l | C | None | descriptive | borderline | Does eigenvector-matrix conditioning kappa(V) explain M1's variation? Sharpens the informal 'eigenvalue clustering' mechanism pearled by both H-B2-1i and H-B2-1k into a s |
| 13 | H-B2-1r | C | None | descriptive |  | Does pseudospectral abscissa alpha_eps(A) explain M1 at N_DIM in {40,50}, where BOTH kappa(V) and omega(A) are hard_killed? Grounded in the (proven) Kreiss Matrix Theorem |
| 14 | H-B2-1s | C | None | descriptive |  | Cross-implementation check of H-B2-1r's pseudospectral abscissa claim via pseudopy (independently-written package) -- closes the skeptic's named remaining gap, per user's |
| 15 | H-B2-1t | C | None | descriptive |  | Fresh-seed confirmatory replication of pseudospectral abscissa at N=40,50 (user's own Priority 2), with kappa(V)/omega(A) as pre-registered comparators, not new hypothese |
| 16 | H-B2-1v | C | strong | descriptive |  | Independent cross-implementation check of H-B2-1u's small-eps Kreiss constant growth via pseudopy.NonnormalAuto (user's own corrected Priority: cross-check the genuinely  |
| 17 | H-B2-1w | B | None | predictive | borderline | Does a fitted K(A)-based log-linear model predict M1's magnitude more precisely than the naive Kreiss ceiling e*n*K(A) or the arc's own established alpha_eps-only correla |
| 18 | H-B2-1x | C | None | predictive |  | Robustness check on H-B2-1w's K(A) exponent (~1.94, no CI, 20 training points): does it hold with a 4x larger training set, 95% confidence intervals, and validation on a  |
| 19 | H-B2-1y | C | None | descriptive |  | Is H-B2-1w/1x's super-linear M1~K(A)^2.2-2.5 exponent a genuine property of this matrix family, or an artifact of the shallow K(A) estimate's own systematic, K-magnitude- |
| 20 | H-B2-2 | C | None | descriptive |  | Does a direct resolvent-norm reference K_ref(A)=max(kappa(lambda_1), floored real-axis line search) -- no pseudopy at all -- give an accurate K(A) across the FULL H-B2-1x |
| 21 | H-B7-1 | A | None | descriptive |  | The Fauré et al. 2006 mammalian cell cycle Boolean network has EXACTLY the two attractors reported in the literature (one point attractor = quiescence, one complex attrac |
| 22 | H-B7-3 | B | None | causal |  | Transient (finite-duration) perturbation of Rb/p27 followed by release -- the STRICT operationalization of Kauffman's hypothesis (pathological state = pre-existing attrac |
| 23 | H-B7-7 | B | None | causal |  | Combined permanent do(RAS=1, TP53=0, p21CIP=0, RBL2=0) four-hit perturbation on the Remy et al. 2015 network's bistable branch -- directly removes the second remaining re |
| 24 | H-B7-8 | B | None | causal |  | Necessity test do(p21CIP=0, RBL2=0) on the Remy et al. 2015 network's bistable branch WITHOUT clamping RAS/TP53 -- directly operationalizes H-B7-7's own FL Step 8a skepti |
| 25 | H-B7-9 | B | None | causal |  | Transient do(p21CIP=0, RBL2=0) for k=1,3,10,30 steps then RELEASED to fully unperturbed wild-type dynamics, on the Remy et al. 2015 network's bistable branch -- the sharp |
| 26 | H-B7-10 | B | None | causal |  | Fine duration sweep k=4..9 of the transient do(p21CIP=0, RBL2=0) clamp on the Remy et al. 2015 network's bistable branch -- pins down the exact relapse/escape threshold H |
| 27 | H-B7-11 | B | None | causal |  | Cross-branch generalization test of the permanent do(p21CIP=0, RBL2=0) clamp on the SECOND (and only other) phenotype-divergent branch of the Remy et al. 2015 network --  |
| 28 | H-B7-12 | B | None | causal |  | Transient do(p21CIP=0, RBL2=0) duration sweep on the SECOND branch (H-B7-11), testing whether H-B7-10's exact threshold k*=5 generalizes -- and, per its own skeptic pass, |
| 29 | H-B7-14 | B | None | predictive |  | Minimal Relaxation Rule variant of H-B7-13 (ONE assumption changed, user's own direct instruction 2026-09-10: 'наблюдай маркеры через j шагов после снятия клэмпа'): does  |
| 30 | H-B7-15 | C | None | predictive |  | Exhaustive (not sampled) verification of H-B7-14's j*=1 claim: does j=1 sufficiency hold over the COMPLETE clamped-trajectory orbit (every achievable release-state for AN |
| 31 | H-B7-18 | C | None | descriptive |  | WHY does H-B7-17's flip_TF_drop_CyclinE1 perturbation (RBL2 := !CyclinD1) abolish the transient escape entirely rather than shift its threshold -- does it destabilize the |
| 32 | H-B7-19 | B | None | predictive | borderline | Does H-B7-14/15's synchronous j*=1 minimal-observability finding survive exhaustive single-bit truth-table perturbations of p21CIP's own rule -- the OTHER clamped node, n |
| 33 | H-B7-21 | B | None | descriptive |  | Synthesize the three sensitivity profiles (RBL2/p21CIP/CyclinE1, H-B7-17/19/20) and derive a minimal necessary/sufficient condition for the Proliferation attractor's own  |
| 34 | H-B7-22 | B | None | descriptive |  | Is H-B7-13's own synchronous k*=5 safe/unsafe release threshold schedule-independent, or can some fair ASYNCHRONOUS update order reach a different eventual fate (not just |
| 35 | H-B7-23 | B | None | descriptive |  | What FRACTION of random fair asynchronous schedules reach PROLIFERATION from H-B7-22's own 8 confirmed SCHEDULE_FRAGILE release-states (k=1..4, both branches) -- closing  |
| 36 | H-B7-24 | B | None | descriptive |  | Along the shortest async-escaping path from each of H-B7-22's 8 confirmed SCHEDULE_FRAGILE release-states, is there a single sharp 'point of no return' step after which G |
| 37 | H-B7-26 | B | medium | descriptive |  | For H-B7-22's own async reachability graph restricted to any one release-state's reachable component -- a finite absorbing Markov chain under H-B7-23's own uniform-random |
| 38 | H-B7-27 | C | strong | descriptive |  | Mechanistic explanation of H-B7-26's own unplanned observation (branch_1/branch_2 give numerically identical exact escape probabilities at every k): is phi=flip(EGFR_stim |
| 39 | H-B7-28 | C | medium | descriptive |  | Does H-B7-27's own FGFR3=True/GRB2=False/EGFR=False invariant and phi=flip(EGFR_stimulus) branch isomorphism, confirmed for H-B7-26's own 10 conditions (k=1..5), extend t |
| 40 | H-B7-29 | C | medium | descriptive |  | Contrast/control test (Mechanism Development Mode question 5, structural asymmetry) for H-B7-27/28's own EGFR_stimulus-inertness finding: is FGFR3_stimulus -- the OTHER f |
| 41 | H-B7-30 | B | medium | descriptive | borderline | Directly executes the user's own explicit priority item 4 from the original H-B7-26 redirect (re-assess the large-deviation/Kramers claim), deferred through H-B7-27/28/29 |
| 42 | H-B7-31 | C | medium | descriptive |  | Formalizes and corrects an earlier informal, never-registered sci-hypothesis-skill finding ('H9-B: n_states_visited is a cheap discriminator of SCHEDULE_FRAGILE vs SCHEDU |
| 43 | H-CAT37-1 | B | none | descriptive |  | Restarted s-step optimal-gradient iteration on SPD matrices (n<=12, s<=11, random/clustered/geometric spectra) shows no counterexample to the Forsythe conjecture, and ind |
| 44 | H-CAT31-1 | B | none | descriptive |  | Random dense circulant graphs (n=10..2560, p=0.5): theta(G)/sqrt(n) stays close to 1 across ~3 orders of magnitude in n, consistent with the tight Conjecture 18 rather th |
| 45 | H-CAT56-2 | D | medium | descriptive |  | PCC-GENERIC-QUASIPURE-v2: for GENERIC quasi-pure states (Yang arXiv:2405.00405 Eq.12) satisfying PCC in the only regime where the certified no-go can fire (r^2+1<d), does |
