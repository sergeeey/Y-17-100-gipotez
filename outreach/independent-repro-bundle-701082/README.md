# Independent repro bundle — seed 701082

**Purpose:** give a third party enough to falsify the H-CAT56-2 exact instance
*without* trusting agent logs or importing `h2_core.py`.

**Status claim for this bundle:** portable object + project verifier.
Not “objectively proven”. The next gate is *your* second implementation.

## Files

| File | What |
|---|---|
| `instance_seed701082.json` | Single-object JSON: flat blocks + structured `Re`/`Im` matrices |
| `instance_d22_r2_s16.jsonl` | Original jsonl (may contain other seeds; use seed 701082) |
| `verify_exact_Q.py` | Project black-box verifier (needs `numpy` + `python-flint`) |
| `SHA256.txt` | Hash of canonical `blocks_flat` JSON |
| `FORMAT.md` | Layout + definitions for a from-scratch second verifier |

## Path A — black-box (their script)

```powershell
cd outreach/independent-repro-bundle-701082
python verify_exact_Q.py instance_d22_r2_s16.jsonl 701082
```

Expect roughly:

```text
pcc_exact_full_commutators: True
qfim_det_nonzero_exact: True
dimV_over_Q_exact: 463
dimVperp_exact: 21
fires_dimVperp_lt_d: True
max_abs_entry_B: 78
```

## Path B — your own verifier (recommended)

Do **not** import `verify_exact_Q.py` internals or any `h2_*.py`.
Build PCC / QFIM / V from definitions in FORMAT.md using `blocks_Re_Im`.
Compare only the four numbers above.

Suggested negative controls:

1. Flip one integer in `blocks_Re_Im[0].Re[0][0]` → PCC must fail.
2. Force singular QFIM (e.g. duplicate two blocks) → det = 0.
3. Restrict to a known non-firing size conceptually (`d=21` theory) — not this file.
4. Unitary change of basis on the full 22×22 picture — rank of V invariant.

## Integrity

```text
blocks_flat_canonical_sha256=
4f2fce7cf7562ad99c6e7eaee0bb54afd1809ec8588de5726b7e1aab057274f3
```

(recompute: `sha256(json.dumps(blocks, separators=(',',':')))` over the 16×80 int lists)

## Honest scope

This bundle lets you close the **portability / independent-reimplementation** gate.
Theorem chain Obs.2 / Ref.[29] is separate reading. Author novelty (U2) is separate.
