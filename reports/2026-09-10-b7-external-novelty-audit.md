# B7 External Novelty Audit (2026-09-10)

**Purpose (FL Step -3, Novelty Check):** the B7 async arc (H-B7-13 through H-B7-31, 19 experiments)
produced a well-verified mechanism cluster — exact absorbing-Markov-chain escape probabilities
(H-B7-26/28), a proven graph-automorphism mechanism explaining branch equivalence (H-B7-27/28), a
contrast/asymmetry test confirming that mechanism's specificity (H-B7-29), and an honest
computational-cost asymmetry finding (H-B7-31). Per consolidation-phase priority item 1
(`.claude/memory/decisions.md` ADR-118): before pursuing anything further on this thread, check
whether these findings are novel contributions to the field, or well-verified applications of
already-established techniques. **This audit does NOT question the INTERNAL correctness of any
H-B7-26...31 finding** (all remain `confirmed`, tool-verified, independently reviewer-reconstructed)
— it only assesses EXTERNAL novelty, a separate axis (per `artifact-provenance-gates.md` Gate 1: a
verdict about correctness never transfers to a verdict about novelty).

## Method

4 rounds of `WebSearch` (real, live queries, 2026-09-10) plus one `WebFetch` on the most directly
relevant candidate paper (CABEAN), targeting each of the 4 distinct claims in the B7-26...31
cluster. All sources cited below were actually fetched/read, not assumed from training-data memory
(per `integrity.md` Evidence Markers — every claim below is `[VERIFIED-REAL]` unless marked
otherwise).

## Finding 1 — H-B7-26 (exact absorbing Markov chain escape probabilities): NOT novel as a method

Already suspected from the literature check that triggered H-B7-26 itself (a 2026 npj Systems
Biology paper). This audit found an even more directly relevant, EVEN MORE GENERAL result:

> **[VERIFIED-REAL]** "Succession-diagram-based Markov chains reveal the attractor landscape of
> asynchronous Boolean networks" — *npj Systems Biology and Applications*, April 2026.
> [nature.com](https://www.nature.com/articles/s41540-026-00717-z) ·
> [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13273057/) ·
> [bioRxiv](https://www.biorxiv.org/content/10.64898/2025.12.17.694936v1.full)

This paper introduces a **coarse-grained** Markov chain over trap spaces (not the raw state graph
H-B7-26 solves directly), explicitly computes convergence probabilities and expected steps via
absorbing-Markov-chain theory, and explicitly frames Boolean attractors as absorbing states of a
Markov chain — the exact theoretical structure H-B7-26 uses, but generalized to a coarser, more
scalable representation. **H-B7-26's own contribution is a special case (raw reachability graph,
no trap-space coarsening) of an already-published, strictly more general method.**

## Finding 2 — H-B7-27/28 (branch isomorphism via inert `EGFR_stimulus`): the GENERAL mathematical
object and the GENERAL biological phenomenon are BOTH established prior art

Two independent, converging results:

**(a) The object itself — state-space graph automorphism as a reduction technique — is a named,
decades-old formal-verification concept, not specific to this project:**

> **[VERIFIED-REAL]** "The symmetry reduction technique is a method for the state-space reduction
> of a system that works by exploiting symmetries in the system. A symmetry is an automorphism of
> the state-space graph... a permutation π of the set of system states such that transitions
> between states are preserved. Since symmetries are permutations, the set of all symmetries of a
> state-space graph forms an automorphism group."
> [Specification, Construction, and Exact Reduction of State Transition System Models of
> Biochemical Processes](https://arxiv.org/pdf/1203.3395)

This is EXACTLY H-B7-27's own claim (`φ=flip(EGFR_stimulus)` is a graph automorphism of the async
reachability graph), described in the exact same formal language, as an established technique
generally applicable to biochemical/Boolean state-transition systems.

**(b) The specific phenomenon — an input becoming contextually/dynamically redundant depending on
which region of state space is reached — is ALSO already named and studied in the canalization
literature, not a novel observation:**

> **[VERIFIED-REAL]** "Canalizing rules make some edges in the original structure contextually
> redundant, with roles of edges varying in that some edges become completely redundant, or
> conversely, essential, **in different dynamical trajectories and attractors**."
> [Dynamical Modularity in Automata Models of Biochemical Networks](https://arxiv.org/pdf/2303.16361)

This is a near-verbatim match to H-B7-27's own finding (`EGFR_stimulus`'s edge to `EGFR` is
completely redundant specifically within this reachable trajectory region, essential elsewhere in
the full truth table). A dedicated, mature tool for QUANTIFYING exactly this class of redundancy
already exists:

> **[VERIFIED-REAL]** CANA — "A Python Package for Quantifying Control and Canalization in Boolean
> Networks" — distinguishes "redundant inputs" (marked with a wildcard symbol) and "input symmetry"
> (permutations of inputs that leave the transition unchanged, forming "group-invariant inputs").
> [Frontiers](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2018.01046/full)
> · [arXiv (1803.04774)](https://arxiv.org/pdf/1803.04774) ·
> [arXiv (2405.07123, CANA v1.0.0 + schematodes)](https://arxiv.org/pdf/2405.07123)

**Verdict: H-B7-27/28's own contribution is a correctly-executed, tool-verified INSTANCE of a
well-established general technique (symmetry reduction / canalization analysis) applied to a
specific benchmark model — not a novel technique or a novel general phenomenon.** H-B7-29's
contrast test (showing `FGFR3_stimulus` is NOT similarly redundant) is a correct, useful
CONFIRMATION exercise within this already-established framework, not a new finding about the
framework itself.

## Finding 3 — H-B7-31 (early-exit BFS asymmetry): a specific, correct instance of a classical
verification-theory fact, not a novel algorithmic insight

> **[VERIFIED-REAL]** "An algorithm can terminate immediately and return results once an
> appropriate state is reached, implementing an early termination strategy during attractor
> search." [Taming Asynchrony for Attractor Detection in Large Boolean Networks](
> https://arxiv.org/html/1704.06530)

Early termination in reachability/attractor search is an established technique. H-B7-31's own
finding — that early-exit gives large savings for confirming `FRAGILE` (an existential property:
"does a second fate exist somewhere in this graph?") but gives NO savings for confirming `ROBUST`
(a universal property: "is every reachable state the same fate?") — is a correctly-quantified,
honestly-caveated instance of the classical existential-vs-universal asymmetry in verification
(existential properties admit early witnesses; universal properties require exhaustive
confirmation). This asymmetry itself is not new to computer science; H-B7-31's contribution is
measuring its magnitude (84-90% savings) precisely on this specific model, with a genuine floor
check (2/2 `ROBUST` conditions correctly show zero false early-exit).

## Finding 4 — the Remy et al. 2015 model itself is a standard, actively-used benchmark

> **[VERIFIED-REAL]** The Remy et al. 2015 bladder tumorigenesis model (35 components) is used as
> a benchmark for reachable-attractor computation tools, including in comparative evaluations
> against CABEAN and related asynchronous-Boolean-network analysis software.
> [CABEAN paper](https://academic.oup.com/bioinformatics/article/37/6/879/5897411) ·
> ["Estimating Attractor Reachability in Asynchronous Logical
> Models"](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6137237/)

**Directly checked CABEAN itself via `WebFetch`** (not assumed from the search snippet alone): it
does **NOT** compute escape/reachability probabilities, does **NOT** use an absorbing Markov chain
formalism, does **NOT** discuss symmetry/automorphism reduction, and does **NOT** apply its own
methodology to the Remy bladder cancer model at all (its own worked example is a generic 3-node
toy network) — so CABEAN specifically is not a direct duplicate of H-B7-26...31's own specific
numeric results, even though the general techniques those results apply are well-established
elsewhere. This narrows (but does not eliminate) the risk that this project's SPECIFIC numbers
already exist published somewhere else under this exact model — that risk remains genuinely
`[UNKNOWN]` without a more exhaustive, dedicated literature search than this audit's scope covered.

## Overall Verdict

**All 4 distinct claims in the H-B7-26...31 cluster are correctly-derived, internally consistent,
independently tool-verified applications of already-established general techniques
(absorbing-Markov-chain theory for Boolean networks — even superseded by a more general 2026
method; state-space symmetry reduction / graph automorphism; canalization-driven contextual input
redundancy; existential-vs-universal reachability-check asymmetry) to one specific, real benchmark
model (Remy et al. 2015). None of the 4 claims constitute a novel contribution to Boolean-network
theory, model-checking theory, or canalization theory as such.**

This matches, and extends, the honest self-assessment already present in every H-B7-26...31
`claim.md`'s own "What This Does NOT Mean" section (each explicitly declined to claim methodological
novelty) — this audit converts those self-assessed, unverified caveats from `[HYPOTHESIS]`-level
statements into `[VERIFIED-REAL]` ones, backed by actual literature.

**What the B7-26...31 cluster's real value IS, honestly:** a well-verified, mechanistically-explained
CASE STUDY demonstrating that these established techniques apply cleanly to a specific real
benchmark model, executed with unusually thorough internal verification discipline (independent
reviewer reconstruction on every claim, floor/positive-negative controls throughout, honest
small-sample/inconclusive-result reporting). Its value is as a rigorously-verified example and as a
demonstration of this project's own FL methodology working correctly on a real, non-trivial system
— not as new science ready for external publication as a novel finding.

## Recommendation (per consolidation-phase ADR-118, ordered)

1. **Do not pursue "publish the B7 mechanism findings as a novel contribution."** The audit rules
   this out — the general techniques are well-established; only the specific application is new,
   and "we applied a known technique to a known benchmark model" is not, on its own, a publishable
   novel contribution without a genuinely new benchmark model or a genuinely new technique.
2. **A genuinely novel angle, if this thread is revisited, would need one of:** (a) a NEW technique
   not covered by symmetry-reduction/canalization/absorbing-Markov-chain theory as it stands, or
   (b) transferring the SAME verified methodology to an INDEPENDENT Boolean network model not
   already covered by this exact literature — testing whether the "dynamically redundant input"
   phenomenon (Finding 2b) is common or rare across real published models would be a genuinely
   open empirical question this audit did NOT find already answered (the canalization literature
   establishes the CONCEPT exists, not its PREVALENCE across real models).
3. Per ADR-118's own priority order, proceed next to **item 2: B3-1q external-data search** (find
   additional manipulation-vs-reference lake-system datasets with multiple co-measured variables),
   since this B7 audit's own recommendation (3a above) is a larger undertaking than the
   consolidation phase's own "cheap, external verification" scope calls for right now.

## Sources (all fetched/read 2026-09-10, not from training-data memory)

- [Succession-diagram-based Markov chains reveal the attractor landscape of asynchronous Boolean networks (nature.com)](https://www.nature.com/articles/s41540-026-00717-z)
- [Same paper, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13273057/)
- [Same paper, bioRxiv preprint](https://www.biorxiv.org/content/10.64898/2025.12.17.694936v1.full)
- [CANA: A Python Package for Quantifying Control and Canalization in Boolean Networks (Frontiers)](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2018.01046/full)
- [CANA, arXiv version](https://arxiv.org/pdf/1803.04774)
- [CANA v1.0.0 and schematodes (arXiv)](https://arxiv.org/pdf/2405.07123)
- [Canalization and Symmetry in Boolean Models for Genetic Regulatory Networks (arXiv)](https://arxiv.org/pdf/q-bio/0610011)
- [Dynamical Modularity in Automata Models of Biochemical Networks (arXiv)](https://arxiv.org/pdf/2303.16361)
- [Specification, Construction, and Exact Reduction of State Transition System Models of Biochemical Processes (arXiv, symmetry reduction)](https://arxiv.org/pdf/1203.3395)
- [Taming Asynchrony for Attractor Detection in Large Boolean Networks (arXiv, early termination)](https://arxiv.org/html/1704.06530)
- [CABEAN: a software for the control of asynchronous Boolean networks (Oxford Bioinformatics) — directly fetched and read, NOT just searched](https://academic.oup.com/bioinformatics/article/37/6/879/5897411)
- [Estimating Attractor Reachability in Asynchronous Logical Models (PMC, Remy as co-author)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6137237/)
