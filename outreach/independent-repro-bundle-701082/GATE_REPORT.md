# Portability / independent-reimplementation gate — seed 701082

**Date:** 2026-09-22  
**Environment:** local Windows, this workspace  
**Verdict:** **PASSED**

Not peer review. Not a human third party. But two computational paths share only the mathematical specification (`FORMAT.md`) and the input object — not the implementation.

## Integrity

| Check | Result |
|---|---|
| `blocks_flat` canonical SHA-256 | `4f2fce7cf7562ad99c6e7eaee0bb54afd1809ec8588de5726b7e1aab057274f3` |
| Matches `SHA256.txt` | YES |
| `max_abs` | 78 |

## Path A — black-box (`verify_exact_Q.py`)

Command:

```text
python verify_exact_Q.py instance_d22_r2_s16.jsonl 701082
```

Stdout (verbatim):

```text
{'n_rows': 544, 'n_cols': 968, 'max_abs_entry_B': 78, 'pcc_exact_full_commutators': True, 'qfim_det_nonzero_exact': True, 'dimV_over_Q_exact': 463, 'dimVperp_exact': 21, 'fires_dimVperp_lt_d': True}
```

| Gate | Value |
|---|---|
| PCC exact | True |
| QFIM nonsingular | True |
| dimV | 463 |
| dimV⊥ | 21 |
| max_abs | 78 |

**Path A: PASS**

## Path B — independent reimplementation (`path_b_independent.py`)

No imports of `verify_exact_Q`, `h2_core`, or project LP helpers. Own Gaussian-integer arithmetic; modular rank over 4 primes + FLINT exact rank as cross-check.

Clean instance:

| Gate | Value |
|---|---|
| PCC exact | True |
| QFIM det ≠ 0 (4 moduli) | True |
| rank moduli (all 4) | 463 |
| flint_rank | 463 |
| dimV / dimV⊥ | 463 / 21 |
| max_abs | 78 |

### Negative controls

| Control | Expected | Observed |
|---|---|---|
| Flip `B0.Re[0,0] += 1` | PCC fails | `pcc_exact=false`; rank→464 |
| Duplicate B0 as B1 | singular QFIM | all `det_moduli=0`; dimV⊥=25 (does not fire) |

**Path B: PASS** (`path_b_pass=true`, `singular_control_ok=true`)  
Artifact: `PATH_B_REPORT.json`

## Gate statement

Independently obtained on both paths:

\[
\operatorname{PCC}=0,\qquad
\operatorname{rank}F^Q=16,\qquad
\dim\mathcal V=463,\qquad
\dim\mathcal V_\perp=21.
\]

> **portability / independent-reimplementation gate пройден в этой среде.**

## Explicit non-claims

- Not peer review / not independent human.
- Obs.2 / Ref.[29] theorem reading is a separate gate.
- Author novelty (U2) is a separate gate.
- Email not sent.
