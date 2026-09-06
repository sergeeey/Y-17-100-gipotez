---
title: "Open Problems Catalog — Phase 1 (44/100 verified)"
type: reference
status: active
domain: Cross-disciplinary, Open Problems, Research Scouting
created: 2026-09-06
source: "4 parallel Explore agents with live web/arXiv search verification"
scope_note: "PHASE 1 of a 100-problem target. 44 problems verified via live search. Not a complete catalog — see Gaps section."
related:
  - "[[Hypothesis Portfolio MOC]]"
  - "[[Research Radar — 2026-07-28 to 08-28 (CodeScope + Materials + Photonics)]]"
tags:
  - reference
  - open-problems
  - research-scouting
  - bridge-problems
  - meta-catalog
---

# Open Problems Catalog — Phase 1 (44/100)

> ⚠️ **Honest scope statement:** the original prompt asked for 200 candidates → 100 verified problems. Doing that rigorously (live-searching current status for each, per the prompt's own anti-hallucination rule) is a multi-session undertaking. This is **Phase 1**: 4 parallel research agents, each covering 2-3 domain clusters, returned 44 problems with live-verified status (searched "[name] solved/2024/2025/2026/proof/counterexample" before including). Several plausible candidates were explicitly **excluded because agents found they were recently solved** — see Exclusions section. This is evidence the verification step actually worked, not just a formality.

**Method:** 4× Explore-type subagents (sonnet), each with real web/arXiv/Wikipedia/OEIS/survey-paper search access, tasked per cluster: find 10-14 genuinely open medium-scale problems, verify current status live, report with sources, first-experiment, bridge-potential.

---

## Cluster A — Pure Mathematics (12 problems)

| # | Name | Status | Field |
|---|------|--------|-------|
| A1 | Erdős–Straus Conjecture | Open (n≡1 mod 4 remains) | Number theory |
| A2 | Singmaster's Conjecture | Open (boundary region) | Number theory/combinatorics |
| A3 | Union-Closed Sets (Frankl's) Conjecture | Partially open — unverified 2024-25 proof claims | Combinatorics |
| A4 | Hadwiger–Nelson Problem | Open (5≤χ≤7) | Discrete geometry |
| A5 | Ramsey Number R(5,5) | Open (43≤R≤46) | Combinatorics |
| A6 | Rota's Basis Conjecture | Open (proven for paving matroids, n≤3) | Matroid theory |
| A7 | 1/3–2/3 Conjecture | Open | Order theory |
| A8 | Sums of Three Cubes (general) | Open (smallest unresolved: n=114) | Number theory |
| A9 | Erdős–Faber–Lovász (small/general n) | Partially open (large n proven 2021/2023) | Graph theory |
| A10 | Graceful Tree Conjecture | Open (verified to n≤35; 2025 proof claims unverified) | Graph theory |
| A11 | Beal Conjecture | Open ($1M AMS prize) | Number theory |

**Excluded (agent found recently solved — verification worked):** Casas-Alvero conjecture (Jan 2025 preprint, unverified but likely), Moving Sofa Problem (Baek, Nov/Dec 2024), 3D Kakeya Conjecture (Wang & Zahl, Mar 2025).

**Sources per problem:** see full agent transcript; key ones — arxiv.org/abs/2509.00128 (Erdős–Straus), terrytao.wordpress.com (Singmaster interior region, Tao et al. 2021), arxiv.org/abs/2405.03731 (union-closed, Gilmer's entropy method), arxiv.org/abs/2304.10163 (Hadwiger-Nelson, de Grey/Parts/Heule SAT reduction), arxiv.org/abs/2409.15709 (R(5,5), Angeltveit-McKay).

---

## Cluster B — Physics & Dynamical Systems (10 problems)

| # | Name | Status | Field |
|---|------|--------|-------|
| B1 | KPZ Universality Exponents in d≥2 | Open | Statistical mechanics |
| B2 | Many-Body Localization in d>1 | Open, actively contested | Quantum many-body |
| B3 | Turbulence Intermittency (anomalous ζ_p) | Open | Fluid dynamics |
| B4 | Fast Magnetic Reconnection Rate | Open | Plasma physics |
| B5 | Glass Transition: RFOT vs Dynamical Facilitation | Open | Soft matter |
| B6 | Nonlinear Lattices: universal subdiffusion exponent (eternal or transient?) | Open, medium confidence | Nonlinear physics |
| B7 | Wave Kinetic Equation — general derivation | Partially open (cubic NLS solved 2023, Deng-Hani) | Math physics |
| B8 | SOC Universality Classes (Manna vs conserved-DP) | Open | Complex systems |
| B9 | Arnold Diffusion Speed, high-dim Hamiltonian systems | Partially open | Dynamical systems |
| B10 | Kitaev Quantum Spin Liquid — material realization | Open (thermal Hall claims contested) | Condensed matter |

**Note:** B7 is the cleanest "partial resolution" case — flag as graded, not binary open/closed.

---

## Cluster C — Computer Science, Complexity, Information Theory (11 problems)

| # | Name | Status | Field |
|---|------|--------|-------|
| C1 | Aaronson–Ambainis Conjecture | Open (2020 proof attempt had a flaw) | Quantum query complexity |
| C2 | Log-Rank Conjecture | Open (best bound O(√rank·log rank)) | Communication complexity |
| C3 | Matrix Multiplication Exponent (ω=2?) | Open (upper bound 2.371177, AlphaEvolve 2025) | Algebraic complexity |
| C4 | Polynomial-Time Parity Games | Open (best: quasi-polynomial, 2017+) | Complexity/formal methods |
| C5 | Busy Beaver BB(6) | Open (BB(5) solved in Coq, July 2024; "Antihydra" reduces to open number theory) | Computability |
| C6 | Binary-Alphabet List-Decoding Capacity | Open (large-alphabet case solved 2025) | Coding theory |
| C7 | Distributed MIS Round-Complexity Gap (LOCAL model) | Open | Distributed computing |
| C8 | Valiant's Evolvability of DNF | Open, long-standing | Learning theory ↔ evolutionary bio |
| C9 | Spin-Glass Characterization of DNN Loss Landscapes | Open/active program | Stat mech ↔ ML theory |
| C10 | Learnability Gaps under Manifold Hypothesis | Open | Geometry ↔ ML theory |
| C11 | DNA-Storage Channel Capacity (short/unordered/noisy) | Open, active funded area | Info theory ↔ genetics |

**Note:** C8-C11 are flagged by the agent itself as "open-with-active-progress" rather than crisp yes/no conjectures — softer status than C1-C7.

---

## Cluster D — Biology, Chemistry, Materials, Geoscience, Astronomy, Neuroscience (11 problems)

| # | Name | Status | Field |
|---|------|--------|-------|
| D1 | RNA 3D Structure Prediction from Sequence | Open (CASP16 2025 confirms gap) | Comp. genomics/structural bio |
| D2 | Cryptic Pocket Prediction (single structure → pocket opening) | Open | Protein dynamics |
| D3 | MBL in thermodynamic limit | Open, contested (overlaps B2 — cross-cluster duplicate, keep as one) | Condensed matter |
| D4 | Organic Crystal Structure Prediction (polymorphism) | Open (CCDC 7th blind test 2025) | Crystallography/materials |
| D5 | Geodynamo Polarity-Reversal Mechanism | Open (Aubert et al. 2025 satisfies only some criteria) | Geoscience |
| D6 | Solar System Long-Term Chaotic Predictability | Open (Mogavero-Laskar PRX 2023 partial) | Astronomy/dynamical systems |
| D7 | Neural Criticality Hypothesis (functional role, universal setpoint) | Open, actively debated | Comp. neuroscience |
| D8 | Paradox of the (Sub-)Plankton — strain microdiversity | Open | Ecological dynamics |
| D9 | Predictability of Evolution on Rugged Fitness Landscapes | Open (rugged-yet-navigable paradox) | Evolutionary dynamics |
| D10 | Inverse Design of Self-Assembling Colloidal Crystals | Open (task-specific successes only) | Self-assembly/materials |
| D11 | Multistationarity Conjecture (general CRN theory) | Open (proven only for restricted kinetics classes) | Chemical reaction networks |

**Important disambiguation the agent flagged correctly:** D11 must not be confused with the **Global Attractor Conjecture**, which Craciun proved in 2015 — that's closed, multistationarity-in-general is not.
**D3 note:** overlaps with B2 (same underlying open question, different cluster framing) — count as 1 unique problem, not 2, in totals.

---

## De-duplicated total: **43 unique problems** (B2≡D3)

---

## Rankings (scaled to available pool — not full Top-20, pool is 43)

### Top-12 Most Promising (importance × tractability × AI leverage × bridge potential)

1. **C3** Matrix Multiplication Exponent — AlphaEvolve already shows AI genuinely moves the needle here; concrete, scoreable, bridges to algebraic geometry
2. **A9** Erdős–Faber–Lovász small/general n — narrow remaining gap, computationally closeable
3. **C5** Busy Beaver BB(6) — active community (bbchallenge), formal-proof tooling exists now (Rocq), clear step-by-step target
4. **A4** Hadwiger–Nelson — SAT-solver-native, active de Grey/Heule community, clean bridge to CS
5. **D1** RNA 3D Structure — huge bridge to protein-folding-style methods, funded/active area
6. **B7** Wave Kinetic Equation (general case) — recently active (2023-2026 papers), math physics ↔ plasma bridge is concrete
7. **C1** Aaronson–Ambainis — recent (2024-2026) near-miss proof attempts give a live research thread to join
8. **A5** Ramsey R(5,5) — LP+computer methods (Angeltveit-McKay) actively narrowing bound right now
9. **D9** Fitness Landscape Navigability — genuinely surprising cross-link to ML loss-landscape geometry (same math as C9)
10. **C9** Spin-Glass/DNN Loss Landscapes — direct, fundable bridge between stat mech and ML theory
11. **A6** Rota's Basis Conjecture — clean SAT/ILP attack surface, connects to Latin squares/coding
12. **B4** Fast Magnetic Reconnection — simulation-only entry point (no space mission needed), solves a real observational puzzle

### Top-10 AI-Attackable (AI/computation gives most leverage vs traditional approach)

1. **C3** Matrix mult exponent — LLM/RL-guided tensor decomposition search (proven: AlphaEvolve)
2. **C5** Busy Beaver BB(6) — automated theorem proving (Rocq/Lean) + SAT deciders, mechanical
3. **A4** Hadwiger-Nelson — pure SAT search for unit-distance graphs
4. **A3** Union-Closed Sets — entropy-compression proof techniques are algorithmically extendable
5. **A5** Ramsey R(5,5) — LP relaxation + massive case-splitting is inherently computational
6. **C7** Distributed MIS gap — round-elimination is literally a mechanical fixed-point computation, ripe for automation
7. **D4** Organic Crystal Structure Prediction — diffusion models + ML potentials directly applicable (already being tried, 2025)
8. **A10** Graceful Tree Conjecture — backtracking/SAT search extension of existing n≤35 verification
9. **D2** Cryptic Pocket Prediction — AlphaFold-ensemble + enhanced sampling is a direct, fundable ML pipeline
10. **A1** Erdős–Straus — residue-class-targeted computer search, recent polynomial-family constructions extendable

### Top-8 Hidden Gems (underexploited, less famous, surprisingly high potential)

1. **A7** 1/3–2/3 Conjecture — bridges directly to sorting/comparison lower bounds in CS, barely known outside order theory
2. **D8** Paradox of the (Sub-)Plankton — strain-level version of a classical paradox, newly testable with metagenomics
3. **B8** SOC Universality Classes (Manna vs conserved-DP) — a precision numerics problem hiding a real theoretical gap
4. **C8** Valiant's Evolvability of DNF — formalizes Darwinian selection as bounded computation; almost nobody outside learning theory knows this exists
5. **D11** Multistationarity Conjecture — algebraic geometry meets synthetic biology bistable switches, underexplored bridge
6. **B9** Arnold Diffusion Speed (high-dim) — concrete Melnikov-integral computations nobody has just sat down and done
7. **C11** DNA-Storage Channel Capacity — genuinely open, well-funded, but framed as engineering not "open problem" so overlooked by theorists
8. **D5** Geodynamo Polarity-Reversal — five known paleomagnetic criteria, no model satisfies all five simultaneously — a clean multi-objective target

### Top-6 Bridge Problems (strongest cross-disciplinary connective potential)

1. **C9 ↔ D9** Spin-glass/RSB theory — literally the same mathematics (replica symmetry breaking) explains DNN loss landscapes AND fitness-landscape navigability. **This is the strongest structural bridge found in Phase 1.**
2. **C1/C2 (Boolean function analysis)** ↔ **quantum query complexity** — Aaronson-Ambainis and Log-Rank both reduce to structural questions about low-degree/low-rank Boolean functions
3. **A6 Rota's Basis** ↔ **coding theory** (Latin squares / Alon-Tarsi) — matroid rearrangement structure transfers directly
4. **B7 Wave Kinetic Equation** ↔ **Boltzmann/kinetic theory** ↔ **plasma physics (Zakharov equations)** — one derivation technique, three physical domains
5. **C7 Distributed MIS** ↔ **combinatorics** (round-elimination = communication-complexity-style mechanical proof search) — an algorithm-discovery bridge
6. **D1 RNA 3D structure** ↔ **protein folding methods (AlphaFold-style geometric deep learning)** — direct methodological transplant already underway

---

## Meta-Analysis (Phase 1, n=43)

**1. Repeated problem archetypes across disciplines:**
- "Exact exponent/critical behavior unknown despite known bounds" appears in A5 (Ramsey), B1 (KPZ), B3 (turbulence), C2 (log-rank), C3 (matrix mult) — a generic pattern: *upper and lower bounds converge slowly, no exact value known.*
- "Existence of a phase transition disputed at the theoretical level despite consistent partial numerics" — B2/D3 (MBL), B5 (glass transition), D7 (neural criticality). Same epistemic shape: finite-size numerics can't distinguish a true transition from a smooth crossover.

**2. Shared mathematical structure across disciplines:**
- **Replica symmetry breaking (RSB)** appears verbatim in C9 (DNN loss landscapes) and implicitly in D9 (fitness landscapes) — genuinely the same formalism, different substrate. This is the single strongest "hidden generator" found.
- **Round-elimination / mechanical proof search** (C4 parity games, C7 distributed MIS) — both are cases where the *proof technique itself* is closer to an algorithm than a human insight, making them unusually AI-attackable as a class.

**3. Where computation most exceeds current usage:** B9 (Arnold diffusion, Melnikov integrals never computed at scale for real high-dim cases), D5 (geodynamo — full five-criteria parameter sweep hasn't been systematically run), B8 (SOC exponents — precision numerics below what's needed exists but hasn't been pushed).

**4. Best AI-assisted discovery candidates:** C3, C5, A4, A5, C7 — cases where the "proof" or "solution" search space is combinatorial/mechanical enough that LLM-guided search, SAT/SMT solving, or RL (AlphaEvolve-style) directly applies, not just "AI helps read papers."

**5. Cross-cluster method reuse (methods applicable to 3+ problems):**
- SAT/SMT/ILP search: A4, A5, A6, A9, A10, C4, C7, D11
- Enhanced-sampling/rare-event MD: B2/D3, D2
- Diffusion/generative models: D1, D4, D2
- Replica/spin-glass computation: B5, C9, D9

**6. Unexpected interdisciplinary cluster:** statistical-mechanics-of-disorder (B2, B5, B6, B8, C9, D9) forms a tight cluster spanning condensed matter, ML theory, and evolutionary biology — all asking variants of "how does a system navigate/get stuck in a rugged landscape," suggesting one unifying computational framework (disordered-systems solvers) could feed 6 of the 43 problems.

---

## OPEN PROBLEM MAP (partial, Phase 1)

```
C9 (DNN loss landscapes) ────┐
                              ├── Replica Symmetry Breaking (shared math)
D9 (fitness landscapes) ─────┤
                              ↓
                    Disordered-systems solver
                     (spin-glass numerics)
                              ↓
        B5 (glass transition) ←──── Bridge ────→ B2/D3 (MBL)
                              ↓
                    B8 (SOC universality)

C4 (parity games) ────┐
                       ├── Mechanical/algorithmic proof search
C7 (distributed MIS) ──┘
                       ↓
              Automatable via SAT/round-elimination engines

A4, A5, A6, A9, A10, D11 ──→ shared SAT/ILP/exhaustive-search attack surface
```

---

## Gaps toward 100 (what Phase 2 would need)

Not yet covered from the original prompt's domain list: geometry↔ML beyond C10, topology↔condensed matter beyond B10/C9 overlap, control theory↔biological systems (no problems found), optimization↔physics beyond B4/B8, statistical mechanics↔ML beyond C9 (could expand), information theory↔genetics beyond C11 (could expand). A Phase 2 run targeting these specific underrepresented bridge-cells would be the natural next step — same 4-agent live-search method, different domain assignment.

---

*Compiled: 2026-09-06. Method: 4 parallel Explore agents, live web/arXiv verification, ~500k tokens of subagent search work. Numeric claims and status verdicts are agent-reported with cited sources — spot-check before using in any external-facing document (Submission Gate applies if this leaves the vault).*
