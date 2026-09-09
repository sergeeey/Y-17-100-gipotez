# H-B7-21 — Lean formalization pilot

**Origin:** user's explicit request (2026-09-10), following a discussion of OpenAI's "GPT-6
Astra" mathematical-research pipeline (structural reasoning -> proof candidate -> formalization
-> Lean certificate). This project's own `falsification-ladder.md` § Independent Verification
Strength Ladder already names "Symbolic solver / Lean / Coq" as the **Strong** tier for formal
claims — this pilot is the first time this project has actually used it, rather than only citing
it.

## What this is (and is not)

`HB721Core.lean` proves, in pure Lean 4 (no mathlib import — see "Why no mathlib" below):

1. **The abstract core theorem** (`update_changes_iff`): for ANY table `f : Row -> Bool` over ANY
   type `Row` with decidable equality, and any row `a`, flipping table entry `a` changes
   evaluation at `x` **if and only if** `x = a`. This is the exact necessary-and-sufficient
   condition `experiments/.../decision.md` states informally — now proven for every possible
   table of this shape, not just the 2984 concrete (node, row, branch) triples `run.py` checked
   numerically.
2. **The multi-node sufficiency corollary** (`all_safe_overrides_preserve_own_evaluation`): for
   ANY list of independent "safe" overrides (each targeting a row that is not its own row),
   every overridden node's evaluation at its own row is unchanged — generalizing `run.py`'s one
   concrete 2-node simultaneous-perturbation check to a list of arbitrary length.
3. **A concrete tie-in to real project data**: RBL2's actual `.bnet` rule
   (`!CyclinE1 & !CyclinD1`) and `PROLIFERATION_STATE`'s actual `(CyclinE1, CyclinD1) = (true,
   false)` values are encoded directly, and Lean's `decide` tactic (a kernel-level decision
   procedure, not a heuristic) independently confirms: flipping RBL2's own row breaks the
   evaluation; flipping any of the other 3 rows does not — the same fact H-B7-17's Python code
   found by direct enumeration, now confirmed by a completely different implementation (Lean's
   kernel, not CPython/`boolean.py`).

**What this does NOT do:** it does not re-encode the full 35-node Remy et al. 2015 network, its
`.bnet` parser, or the clamp/release simulation machinery in Lean. That would be a much larger
undertaking (parsing, 35 real boolean expressions, a synchronous-update simulator) — genuinely a
separate project, not a "pilot." The abstract theorem proven here is exactly what makes that
unnecessary for THIS specific claim: because the necessary-and-sufficient condition is proven for
*any* table over *any* row type, it automatically covers every one of the 35 real network nodes
without having to encode each one individually — the RBL2 instantiation above is a concrete
worked example, not an exhaustive network-wide replay in Lean.

## Why no mathlib

The natural mathlib primitive here is `Function.update`, and the natural tactic for the
`Decidable`-forall step would be mathlib's `Fintype`-based decidability instances. Both were
deliberately avoided for this pilot: mathlib is a multi-gigabyte dependency (Epoch AI's own
`FrontierMath Erdős` writeup reports 1.2 million lines of Lean for formalizing a single 18-page
proof — a concrete illustration of how expensive a full mathlib-backed formalization effort can
get). This project's own claim is small and finite enough that a from-scratch, dependency-free
core-Lean proof (~115 lines including comments) was both sufficient and far cheaper to set up and
audit. A future formalization of a genuinely open/asymptotic claim (e.g. the Forsythe or Lovász
catalog items) would very likely need mathlib and should budget for that cost explicitly, per
this same Epoch AI data point.

## Substrate (FL Step 2a — reproducibility)

Installed this session via `elan` (the standard Lean toolchain manager), no toolchain previously
present on this machine:

```
elan --version   -> elan 4.2.4 (227caca13 2026-08-25)
lean --version   -> Lean (version 4.33.1, x86_64-w64-windows-gnu, commit 819816b2e0a3bf...)
```

No `mathlib`/`lake` project was created — `HB721Core.lean` is a single self-contained file,
checked directly via `lean HB721Core.lean` (no `lakefile.toml`, no `lake build`).

## Reproduce

```bash
lean HB721Core.lean
```

Exit code 0, no warnings, no errors. The file's own trailing `#print axioms` commands report
both main theorems depend on exactly `[propext]` — a standard, non-controversial core Lean axiom
(propositional extensionality) — not `sorryAx` (which would mean an incomplete proof) and not
`Classical.choice` (not needed here, since everything is decidable). No `sorry`, `admit`, or
`native_decide` (which would trust compiled code over the kernel) appears anywhere in the file.

## Verdict on the pilot itself

**Worked, cheaply, for the right kind of claim.** Total cost: one `elan` install (~2 min), one
`lean --version` toolchain download (~1 min), ~115 lines of proof, a handful of iterate-on-
compiler-error cycles (documented honestly in `tooling-eval/LEDGER.md`, not hidden). This
confirms the scoping judgment from the chat discussion that prompted this pilot: Lean is
tractable and worth using for **finite, decidable claims about a fixed, closed system** (exactly
what H-B7-21's theorem is), and likely NOT worth it, without a much larger budget, for the
project's genuinely open/asymptotic catalog items (Forsythe, Lovász) — consistent with what
Epoch AI's own 1.2M-line example independently illustrates for a harder class of problem.
