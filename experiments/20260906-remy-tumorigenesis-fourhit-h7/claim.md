# claim.md — 20260906-remy-tumorigenesis-fourhit-h7

**Graph node:** `H-B7-7` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-6` (Relaxation Map: "Four-hit permanent `do(RAS=1, TP53=0, p21CIP=0, RBL2=0)` —
directly removes the remaining redundant OR-branch identified here").

## EstimandOps L0 Gate

**Classification: CAUSAL.** Same structure as `H-B7-2`/`H-B7-3`/`H-B7-4`/`H-B7-5`/`H-B7-6`: a combined
intervention `do(RAS=1, TP53=0, p21CIP=0, RBL2=0)` applied simultaneously and permanently, compared
against the `Growth_arrest` starting fixed point and against the three-hit comparator already tested
(`H-B7-6`: RAS+TP53+p21CIP, REJECTED). The 4 identifiability assumptions are trivially satisfied for
the same reason as every prior experiment in this bridge (fully specified, exhaustively-verifiable
deterministic mechanism, cross-validated against `pyboolnet` in `H-B7-4` and again in `H-B7-6`).

**Explicit deviation from the Minimal Relaxation Rule, justified — FOURTH such deviation in this
bridge, and this time closes the set:** this experiment changes FOUR assumptions at once. This is not
scope creep — `H-B7-6`'s own `decision.md` named the EXACT mechanism this removes: `Growth_arrest` is
an explicit three-way redundant OR gate in the network's own source
(`Growth_arrest = p21CIP | RBL2 | RB1`). `H-B7-4` clamped none of the three; `H-B7-5` added `TP53`
(upstream of `p21CIP`, not one of the three OR-branches itself); `H-B7-6` clamped `p21CIP` (branch 1
of 3); this experiment adds `RBL2` (branch 2 of 3) — the ONLY remaining OR-branch not yet directly
addressed is `RB1` itself, which `H-B7-6` proved algebraically (and confirmed via `pyboolnet`) is
ALREADY forced to `0` at every fixed point of this branch whenever `p16INK4a`'s coupling condition
holds — meaning clamping `RBL2` on top of the existing three hits is the last DIRECT lever available
without adding a fifth, redundant clamp on a node (`RB1`) that the mechanism already shows cannot
independently block the outcome once `p21CIP` and `RBL2` are both off.

## Why `RBL2`, Specifically, as the Fourth Hit

`H-B7-6`'s `decision.md` identified `Growth_arrest = p21CIP | RBL2 | RB1` from the `.bnet` source
directly. With `p21CIP` already clamped to `0` (`H-B7-6`), the reached attractor showed `RBL2=1`
sufficient on its own to keep `Growth_arrest=1`. `RBL2`'s own rule
(`!CyclinE1&!CyclinD1`) and `H-B7-6`'s proof that `CyclinD1` is provably `0` at every fixed point of
this branch together imply `RBL2 = !CyclinE1` exactly at any fixed point here — so `RBL2` is
self-sustaining at `1` as long as `CyclinE1` stays at `0`, which is exactly the chicken-and-egg
problem `H-B7-6` named (`CyclinE1` needs `!RBL2` to turn on; `RBL2` needs `CyclinE1=1` to turn off).
Clamping `RBL2=0` directly breaks this specific loop, independent of whether `CyclinE1` can bootstrap
on its own.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, same bistable branch as `H-B7-4`/`5`/`6` `(DNA_damage=0, EGFR_stimulus=0, FGFR3_stimulus=1, Growth_inhibitors=1)`, `RAS` clamped to 1, `TP53` clamped to 0, `p21CIP` clamped to 0, AND `RBL2` clamped to 0, simultaneously and permanently |
| **Falsifiable predicate** | The quadruple clamp, started from the `Growth_arrest` fixed point, settles into `Proliferation` (per the model's own explicit phenotype node) rather than remaining `Growth_arrest` |
| **Measurable outcome** | Final attractor's `Growth_arrest`/`Proliferation` phenotype-node values, compared against `H-B7-6`'s three-hit result — using the model's own phenotype semantics per the correction made in `H-B7-6`, not raw bit-string novelty |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: no prior four-hit perturbation experiment
on this or any Boolean network in this project. First four-node combined test in the bridge, and the
first perturbation chosen to directly close an explicitly-named redundant-OR-gate structure rather
than to test a new biologically-motivated hypothesis from scratch.

## Kill Criterion (set BEFORE running)

- **CONFIRMED:** the combined `do(RAS=1, TP53=0, p21CIP=0, RBL2=0)` clamp reaches an attractor with
  the model's own phenotype nodes reading `Growth_arrest=0, Proliferation=1`. This would be the first
  confirmation in this bridge that a permanent-clamp combination reaches the true `Proliferation`
  phenotype from the `Growth_arrest` starting point.
- **REJECTED:** the quadruple clamp still reads `Growth_arrest=1` (or an attractor where neither
  phenotype node is unambiguously `1`) — would mean a FOURTH mechanism (beyond the named
  `p21CIP`/`RBL2`/`RB1` triad) sustains arrest, requiring a further trace analogous to `H-B7-5`'s and
  `H-B7-6`'s own.

## What This Does NOT Mean

1. A CONFIRMED result validates the SPECIFIC mechanistic chain traced across `H-B7-4`→`H-B7-6` for
   THIS branch and THIS model — not a general claim about real bladder cancer biology, where `RBL2`
   (p130) loss is not typically grouped with `RAS`/`TP53`/`p21CIP` as a "standard" cooperating set.
2. A REJECTED result would not invalidate `H-B7-6`'s algebraic/`pyboolnet`-confirmed proof that
   `CyclinD1` is dead in this branch — that proof concerns `CyclinD1` specifically, not every possible
   remaining route to `Proliferation`; a REJECTED result here would mean a route independent of the
   `p21CIP`/`RBL2`/`RB1`/`CyclinD1` axis exists and needs its own trace.
3. Does NOT test whether a TRANSIENT (not permanent) version of this same four-node combination, or a
   transient kick of `RBL2`/`CyclinE1` alone on top of the already-permanent three-hit base, would
   succeed where a straight permanent clamp does not — both named as alternative next steps in
   `H-B7-6`'s Relaxation Map, not tested here.

## MCID

Binary: does the model's own `Proliferation` phenotype node read `1` in the reached attractor? No
partial-credit threshold — read directly from the state, cross-checked against `pyboolnet`'s
independently-computed ground truth (inherited from `H-B7-4`/`H-B7-6`).
