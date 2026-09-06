# claim.md — 20260906-kauffman-cellcycle-attractors-h1

**Graph node:** `H-B7-1` (new bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Origin:** CDT Protocol scoring session, 2026-09-06 — top-ranked candidate (score 3.5) among 6
non-blocked Hypothesis Revival Targets, chosen for low cost (small, tractable network, no specialized
package needed) and high kill_power (external, independently-computed ground truth exists).

> **What this bridges:** Kauffman's Cancer Attractor hypothesis (1971) — that differentiated and
> pathological cell states are genuine dynamical ATTRACTORS of a gene regulatory network, not
> separate ad-hoc models — against a specific, small, published Boolean network (Fauré et al. 2006,
> mammalian cell cycle control, 10 components) whose attractors have already been independently
> computed by a third-party tool (PyBoolNet). This experiment does NOT test a novel biological claim;
> it tests whether an independent, from-scratch implementation reproduces a known computational
> result — a REPRODUCTION test, the correct first step before trusting brute-force enumeration on
> anything genuinely new.

## Gate 1 — Artifact Identity

| Field | Value |
|-------|-------|
| artifact_id | `ART-FAURE-CELLCYCLE-BNET` |
| source | `https://raw.githubusercontent.com/hklarner/pyboolnet/master/pyboolnet/repository/faure_cellcycle/faure_cellcycle.bnet` |
| date_created (upstream rules) | 2006 (Fauré et al., Bioinformatics) — file itself dated by git history, not independently checked here |
| publication_status | rules: published, peer-reviewed. Encoding file: unpublished tooling from a citable open-source package (`pyboolnet`, `pip show` confirms it is not installed here but the repo/package is real and referenced by multiple review papers found via WebSearch) |
| hash (sha256) | `1ce4463e66f53db98ad0bc3c5203da8824f8a473681f56ecb963b9a61f93a2f3` |
| relates_to | `faure_cellcycle_attractors_pyboolnet.md` — independent third-party attractor computation on this exact file, used as positive control (Gate 3, below) |

Full record: `data/Data_README.md`.

## Gate 2 — Target Provenance

| Field | Value |
|-------|-------|
| who produced the rules | Fauré, Naldi, Chaouiya, Thieffry — human researchers, published, peer-reviewed |
| who produced the attractor report used as ground truth | PyBoolNet (algorithmic tool: exhaustive/BDD-based attractor detection), not an LLM, not a fit |
| what data the "predictor" (my own brute-force code) can see | Only the .bnet rule file — the attractor report is NOT consulted while writing the enumeration code, only afterward for comparison (analogous to Context Asymmetry: the checker doesn't see the answer key while reasoning) |
| was anything fitted/optimized | No — Boolean update rules and brute-force state-space enumeration are both exact, deterministic, no free parameters |
| kind of claim | **Reproduction/verification**, not a prediction and not a fit — my code either reproduces PyBoolNet's reported attractor set exactly, or it doesn't |

## Gate 3 — Positive-Control Digitization

The PyBoolNet-generated `faure_cellcycle_attractors_pyboolnet.md` report IS the positive control:
a known-identity result (steady state `0000001011`, complex-attractor trapspace `---1--0--0`, both
reported with `completeness: True` under both synchronous and asynchronous updating) computed by an
established, citable, independently-maintained tool against THIS EXACT rule file. My own brute-force
enumeration (written before consulting this report's specific numbers beyond what's needed to know
the expected FORM of the answer) must reproduce this exactly. A mismatch is a bug in my code, not a
finding about the biology — this experiment cannot itself produce a "the model is different from the
literature" claim; it can only produce "my implementation is/isn't correct."

## FL Step -4: Source Trace

- Paper existence: `[VERIFIED]` via WebSearch — Fauré et al. 2006, *Bioinformatics* 22(14):e124-e131,
  Oxford Academic DOI page confirmed to exist and to describe a 10-component Boolean model with the
  claimed attractor structure.
- Exact rules: `[VERIFIED]` via the pyboolnet `.bnet` file, whose header explicitly cites the same
  paper — NOT reconstructed from memory or from a qualitative prose description (multiple WebFetch
  attempts on the paper's own page, a PMC review, and ResearchGate all failed to expose the exact
  rule table in fetchable text; the file is the only source that gave the precise logical formulas).
- What was NOT independently verified: whether the pyboolnet `.bnet` file is a byte-perfect
  transcription of the original paper's Table/Figure (the paper's PDF itself was not fetchable). This
  is a disclosed limitation, not a silent gap — see "What This Does NOT Mean" below.

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md` and `pearl_registry/INDEX.md`: no prior mention of "boolean network",
"attractor", or "Kauffman" in this project. Meta-graph (`graphify-query.py find-all`) checked for
"Kauffman", "boolean network", "attractor", "GRN" — no substantive prior analysis in any of the 54
tracked repos (only unrelated keyword noise). This is the first Boolean-GRN-dynamics work in this lab.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Fauré et al. 2006 mammalian cell cycle Boolean network (10 named components, rules in `data/faure_cellcycle.bnet`) |
| **Falsifiable predicate** | Exhaustive synchronous-update brute-force enumeration over all 2^10=1024 states finds EXACTLY one point attractor and one complex (cyclic) attractor, matching PyBoolNet's reported steady state and trapspace |
| **Measurable outcome** | Set of attractors found by my own enumeration, compared field-by-field against `faure_cellcycle_attractors_pyboolnet.md` |

## Natural Language Statement

> "We verify, via independent from-scratch brute-force enumeration of all 1024 Boolean states under
> synchronous updating, that the Fauré et al. 2006 mammalian cell cycle network has exactly the
> attractor structure already reported by PyBoolNet for the same rule file: one point attractor and
> one complex attractor."

## L0 Classification

**Descriptive** — reproducing/verifying an already-published, already-computed result, not predicting
an unknown outcome or establishing causality.

## Kill Criterion (set BEFORE running)

- **CONFIRMED:** brute-force enumeration finds exactly 2 attractors (1 point, 1 complex), and the
  point attractor's state vector matches PyBoolNet's `0000001011` exactly.
- **KILLED (implementation bug, not a biology finding):** enumeration finds a different number of
  attractors, or a different point-attractor state, than PyBoolNet's report — would mean an error in
  my own Boolean-update code or state-enumeration logic, to be found and fixed before any further
  claim.
- **This experiment cannot produce a PROMOTE-tier claim about Kauffman's hypothesis itself** — it is
  a prerequisite reproduction step. The actual cancer-attractor claim (does the complex attractor's
  biological interpretation as "persistent proliferation" hold up, and does that generalize beyond
  this one network) is explicitly OUT OF SCOPE here — see Relaxation Map for the follow-up this
  would enable.

## What This Does NOT Mean

1. Does NOT test whether Kauffman's cancer-attractor hypothesis is TRUE in any general sense — one
   network, one already-known result, reproduced. A single reproduction is a prerequisite, not
   evidence for the broader hypothesis.
2. Does NOT independently verify that the `.bnet` file is a perfect transcription of the original
   1972-2006 paper's exact tables — relies on the file's own citation and the fact that it ships
   inside a citable, peer-reviewed-adjacent open-source package used by multiple published follow-up
   papers (found via WebSearch), not on reading the original PDF directly.
3. Does NOT establish that the "complex attractor = cancer-like proliferation" interpretation is
   itself correct biology — that interpretive claim belongs to the original paper's authors, not to
   this reproduction step.

## MCID

None in the usual PROMOTE/REJECT sense — this is a binary reproduction check (matches / does not
match the positive control). A match unblocks the NEXT experiment (an actual novel test of the
cancer-attractor claim, e.g. perturbing the network to see whether accessible attractors correspond
to known pathological states not built into the model by construction). A mismatch blocks that next
step until the implementation bug is found.
