# H-CAT56-2 — external package freeze (2026-09-22)

Frozen BEFORE any author email is sent. Not a new experiment.
L0: **descriptive / constructive** package inventory + scope statement.

## Package contents (canonical)

| Role | Path |
|---|---|
| Exact instance (PASS-SMALL) | `experiments/20260920-small-exact-qi-instance/instance_d22_r2_s16.jsonl` (seed **701082**) |
| Exact verifier over ℚ | `experiments/20260920-small-exact-qi-instance/verify_exact_Q.py` |
| Companion verifier | `experiments/20260920-small-exact-qi-instance/verify_instance.py` |
| Instance decision | `experiments/20260920-small-exact-qi-instance/decision.md` |
| Counterexample claim + structural theory | `experiments/20260919-pcc-generic-quasipure-cat56-2/{claim,decision}.md` |
| Obs2 / scope write-up | `experiments/20260920-h-cat56-2-verification-gates/proof_and_scope.md` |
| Positive control (paper LMCC ∈ V⊥) | `experiments/20260920-h-cat56-2-verification-gates/gate4b_lmcc_in_vperp.py` |
| Novelty audit (WEAK) | `experiments/20260920-h-cat56-2-verification-gates/novelty_audit.md` |

## Reproduce in seconds

```powershell
cd experiments/20260920-small-exact-qi-instance
python verify_exact_Q.py instance_d22_r2_s16.jsonl 701082
```

Requires: `numpy`, `python-flint`.

Re-run 2026-09-22 (this freeze session):

```text
pcc_exact_full_commutators: True
qfim_det_nonzero_exact: True
dimV_over_Q_exact: 463
dimVperp_exact: 21
fires_dimVperp_lt_d: True
max_abs_entry_B: 78
```

## What the package asserts

1. An explicit Gaussian-integer quasi-pure PCC state exists at `d=22, r=2, s=16`
   with `dim_ℝ V = 463`, hence `dim V⊥ = 21 < 22`.
2. **If** Observation 2 / Simultaneous Hollowization (Yang–Imai–Pezzé, arXiv:2601.21801)
   apply as published, then this state cannot saturate single-copy matrix QCRB
   (`F^C = F^Q`), so PCC is not sufficient for generic quasi-pure states in this regime.
3. Separately proven here (elementary LA): C-ID / C-LB / C-CEIL for `dim V⊥`
   on the PCC quasi-pure class — independent of Observation 2.

## What the package does NOT assert

- Novelty as settled fact (`[WEAK]` keyword scan only).
- Independence from Observation 2 / Hollowization Theorem 1 / Ref. [29] null-outcome iff.
- Collective / asymptotic / Holevo / singular-weight scalar bounds.
- Eq. (16) ancilla subclass (sufficiency already proven in the source).
- That the found instance is typical (it was search-selected).

## Status label for external readers

```text
H-CAT56-2: exact counterexample package internally certified;
portability passed via independent local reimplementation;
theorem-chain read and consistent;
novelty and external reproduction unresolved.
```

Canonical freeze: `outreach/CHECKPOINT_FREEZE_2026-09-22.md`  
Portability artifacts: `outreach/independent-repro-bundle-701082/` (+ `.zip`, `GATE_REPORT.md`)

## Next gates (owner / external — not new internal experiments)

1. Hand ZIP with `outreach/THIRD_PARTY_BRIEF.md` (discrepancy-first; do not ask for 463/21).
2. After 24h cooling-off: send `outreach/2026-09-22-authors-email-DRAFT-v2.md` per `SEND_CHECKLIST_channel_A.md`.
3. Pause new internal H-CAT56 experiments until an external U2/U3 signal.
