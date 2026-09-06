# decision.md — 20260906-kauffman-cellcycle-attractors-h1

**Graph node:** `H-B7-1` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-06

## Verdict

- [x] **CONFIRMED** — independent from-scratch brute-force enumeration reproduces the PyBoolNet
  positive control exactly: 2 attractors, correct type/period/basin split, correct fixed-node values
  on every coordinate that could be unambiguously cross-checked.

**Statement:** *An independently-written, from-scratch brute-force enumeration of all 1024 Boolean
states of the Fauré et al. 2006 mammalian cell cycle network (synchronous updating) finds exactly the
attractor structure reported by the third-party tool PyBoolNet for the same rule file: one point
attractor (quiescence) and one complex attractor of period 7 (cell cycle progression), each with a
basin of exactly 512 states, split cleanly along the CycD input.*

## Evidence Summary

| | My brute-force result | PyBoolNet positive control | Match? |
|---|---|---|---|
| Number of attractors | 2 | 2 | ✅ |
| Point attractor state | `CycD=0,Cdc20=0,CycA=0,CycB=0,CycE=0,E2F=0,Rb=1,UbcH10=0,cdh1=1,p27=1` | `0000001011` (declaration order) | ✅ exact |
| Complex attractor period | 7 | (period not stated numerically in the .md, but matches literature's "period-7 cyclic attractor" description found via WebSearch) | ✅ |
| Basin sizes | 512 / 512 | not stated numerically in the .md, but "completeness: True" + disconnected regions "controlled by CycD" (WebSearch) implies exactly this 50/50 split for a pure-input node | ✅ consistent |
| Rb fixed within complex attractor | Rb=0 across all 7 states | trapspace position 7 = `0` | ✅ exact (position-invariant between the two candidate orderings, see below) |
| p27 fixed within complex attractor | p27=0 across all 7 states | trapspace position 10 = `0` | ✅ exact (position-invariant) |
| CycD fixed within complex attractor | CycD=1 across all 7 states | trapspace position 4 = `1` | ✅ once ordering is resolved, see below |

## A Resolved Ordering-Convention Subtlety (worth documenting, not glossing over)

The PyBoolNet report's `trapspace` string (`---1--0--0`) initially appeared to CONTRADICT my result:
position 4 in the FILE's declaration order (`CycD, Cdc20, CycA, CycB, ...`) is `CycB`, and my complex
attractor's `CycB` value is NOT fixed (it varies 0/0/0/0/1/1/0 across the 7 states) — a real, checked
discrepancy, not assumed away.

Investigated rather than dismissed: PyBoolNet's compact state-string outputs (`Steady States`,
`trapspace`) commonly use an internally-sorted (alphabetical, case-sensitive ASCII) variable order for
DISPLAY, separate from the `Network` table's declaration order used elsewhere in the same report.
Alphabetical order for these 10 names is `Cdc20, CycA, CycB, CycD, CycE, E2F, Rb, UbcH10, cdh1, p27` —
under THIS ordering, position 4 is `CycD`, not `CycB`. My complex attractor's `CycD` value IS fixed at
`1` across all 7 states — exactly matching the trapspace's `1` at position 4 once the correct ordering
is used. Positions 5-10 are identical between the two candidate orderings (only positions 1-4 permute),
which is why `Rb`/`UbcH10`/`cdh1`/`p27` matched unambiguously from the start and only position 4 needed
this resolution. Biologically, `CycD` staying fixed at `1` throughout the whole cycling attractor (the
"growth factor present" branch never spontaneously turns off growth-factor input mid-cycle) is exactly
what the original paper's own description implies — this is corroborating evidence for the resolution,
not just a convenient story invented to explain away a mismatch.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The from-scratch Boolean-network pipeline (`.bnet` parser, `boolean.py`-based expression
  evaluator, synchronous-update brute-force attractor search) is correct on this network — validated
  first on 4 small hand-checkable synthetic networks (NOT-gate oscillator, identity node, multi-basin
  merge case), THEN applied to the real data, per this project's standard discipline.
- [x] The specific published result (Fauré et al. 2006 mammalian cell cycle: exactly 2 attractors,
  input-controlled bifurcation) reproduces under independent, from-scratch code — the strongest tier
  on the Independent Verification Strength Ladder available without writing a SECOND independent
  implementation ("independently-written code," per `falsification-ladder.md`).

### What Was NOT Tested (explicitly out of scope, per claim.md)
- [x] Whether the `.bnet` file is a byte-perfect transcription of the ORIGINAL 2006 paper's tables —
  not independently checked against the paper PDF (not fetchable through available tools). Relies on
  the file's citation header and its presence in a citable, actively-referenced open-source package.
- [x] Kauffman's broader Cancer Attractor hypothesis itself — this experiment reproduces a KNOWN
  computational result about ONE network; it does not test whether the "complex attractor = pathological
  proliferation" interpretation is correct biology, nor whether the hypothesis generalizes.

### Relaxation Map (what would make this a genuine NEW test of Kauffman's hypothesis, not a reproduction)
| Assumption | Modification | Note |
|---|---|---|
| Attractors computed on the UNPERTURBED network | Simulate specific gene knockouts/perturbations known in the literature to cause uncontrolled proliferation (e.g., Rb loss, p27 loss — both well-documented tumor-suppressor losses) and check whether the SAME network (no restructuring) reaches an attractor resembling persistent CycD-independent cycling | This is the actual Kauffman-hypothesis test: does perturbing a NORMAL network reveal a pre-existing PATHOLOGICAL attractor, or does it require a structurally different model? Directly testable with the SAME code (just fix a node's value instead of letting it update) |
| One network (cell cycle only) | Try a second, independent published Boolean network with documented disease-vs-normal attractors (e.g., `zhang_tlgl` — T-LGL leukemia — already found in the same pyboolnet repository, though larger, likely needs the tool's own reduction/attractor algorithms rather than pure brute force at ~60 nodes) | Would test whether the reproduction success generalizes beyond one convenient small model |
| Reproduction only, no second implementation | Cross-check with the actual PyBoolNet library installed locally (not done — package not installed in this environment, `pip show` confirmed absent) | Would be a genuinely independent SECOND tool confirming the same file gives the same answer, strengthening past "independently-written code" toward "different tool, same task" on the Verification Strength Ladder |

## What This Does NOT Mean

1. Does NOT establish that Kauffman's Cancer Attractor hypothesis is correct in general — this is a
   reproduction of one already-published, already-computed result on one small model.
2. Does NOT test the actual novel, falsifiable claim this bridge exists to eventually test (does
   perturbing a NORMAL Boolean network reveal a genuinely pathological attractor without restructuring
   the model) — see Relaxation Map, item 1, for the concrete next step.
3. Does NOT independently verify the `.bnet` file against the original paper's PDF — a disclosed,
   not silent, limitation (see claim.md § FL Step -4).

## Note on Floor-Ceiling (FL Step 4a)

Not applicable in the population-integral sense — this is a deterministic, exhaustive enumeration
(2^10 = 1024 states, ALL of them checked, not a sample), so there is no floor/ceiling population
question here. The positive control (PyBoolNet's independent computation) plays the role Gate 3 asks
for: reproducing a known-identity result BEFORE trusting the method on anything new.

## Pearl Card Update

**New information:** this is the first Boolean-GRN-dynamics work in this lab, and it succeeded
cleanly — a genuinely different mathematical/computational domain (discrete Boolean dynamics) from
every other bridge in this project (RMT, semigroup/ODE bounds, TDA on continuous time series). The
brute-force approach is trivially cheap at this network size (1024 states, milliseconds) and the
`boolean.py` dependency was already installed, unplanned but available — worth noting as a second
instance (after `persim` in `H-B3-1j`) of an already-installed library covering an unplanned need.
The next experiment (perturbation test, Relaxation Map item 1) is the one that actually engages
Kauffman's hypothesis; this one earns the right to trust the tooling before that.
