# Third-party brief — H-CAT56-2 seed 701082

Give them the ZIP only. Do **not** tell them the expected `(463, 21)`.

## What to send

`outreach/independent-repro-bundle-701082.zip`

Contains: `FORMAT.md`, instance JSON/JSONL, `verify_exact_Q.py`, SHA256, Path-B script (optional — they may ignore it).

## Task wording (copy-paste)

> Here are a mathematical specification (`FORMAT.md`) and an exact instance.
> Independently check: PCC, nonsingular QFIM, construction of \(\mathcal V\), its rank, and whether Observation 2 as stated in the cited source applies to this object.
> Report any discrepancy.
> You may use or ignore the included verifier scripts; a from-scratch implementation from `FORMAT.md` alone is preferred.

## What not to say

- Do not ask them to “confirm 463/21”.
- Do not narrate our Path A/B verdicts as the target.
- Do not ask for a novelty opinion in the same pass (separate question if needed).

## Success criterion for U3

Any written report that either:

1. reproduces the same four gates from an independent construction, or  
2. documents a concrete discrepancy (object, definition, or Obs.2 applicability).

Silence or “looks fine” without recomputation does **not** close U3.
