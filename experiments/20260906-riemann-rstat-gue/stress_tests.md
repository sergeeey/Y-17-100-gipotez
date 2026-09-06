# Stress Tests — 20260906-riemann-rstat-gue

Source: `metrics/stress.json` (`python run.py stress`, 2026-09-06). All values `[VERIFIED]` from file.

## Adversarial Test Cases

### Case 1: Low-height regime — first 1,000 zeros only
**Input:** `zeros[:1000]` (heights 14 … ≈ 1,420)
**Expected:** drift away from GUE; **no PASS threshold pre-registered** (claim.md § Unknowns marked this [W])
**Actual:** ⟨r⟩ = 0.61704, Δ to surmise = +0.0144 — outside the ±0.01 band
**Result:** REPORTED — informative, not gated. Confirms the height trend seen in the data-swap (0.617 → 0.612 → 0.610 → 0.6006).

### Case 2: Injected duplicate zero (ICE: corrupted data must abort, not bias)
**Input:** `zeros[500] = zeros[499]`
**Expected:** `ValueError`, pipeline stops; ⟨r⟩ is never computed on corrupted input
**Actual:** `non-positive spacing at index 499: data corrupted/misordered — aborting`
**Result:** PASS

### Case 3: Parser robustness — CRLF line endings + trailing blank/whitespace lines
**Input:** file text with `\n → \r\n` and appended `\r\n\r\n   \r\n`
**Expected:** identical array (count and values)
**Actual:** identical (`np.allclose`, same size)
**Result:** PASS

## Stress Summary

| Case | Type | Result |
|---|---|---|
| 1 | boundary (low height) | REPORTED — outside band, expected direction |
| 2 | adversarial (corruption) | PASS |
| 3 | edge case (encoding) | PASS |

**Overall stress verdict:** PASS on gated cases; case 1 is the most informative number in the whole
experiment and feeds the Pearl Gate (see result_summary § Unexpected Observations).

## Notes

- Case 1 was deliberately left ungated in claim.md because the convergence rate was unknown. Adding a
  threshold *now* would be post-hoc; the correct move is a follow-up experiment with higher tables and a
  pre-registered functional form for the height dependence.
- Not tested (known gap): a file where the first zero is correct but later entries are shifted by one
  column — the first-zero + monotonicity + count checks would not catch a *consistent* systematic
  transcription error. Mitigation available: compare zeros[1], zeros[2] to published 21.022040, 25.010858.
