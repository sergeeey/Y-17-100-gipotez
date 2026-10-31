# ERRATA for STAGE_C_FINAL_PROOF.md (2026-11-01)

`STAGE_C_FINAL_PROOF.md` is kept **unchanged** as the historical record. Its SHA-256 at the time of this erratum: `682eaad1859d86758b0892e56960ca43f19c62a45d338f3cec8953a4ce056f4e`. The errors below are corrected here, not in place.

## E1 — Hermiticity of the stored matrix R (lines 71–73; status: CLOSED here)

**Erroneous text.**
- Line 71: "R — эрмитова 20×20 матрица …"
- Line 72: "Это точная рациональная эрмитова матрица."
- Line 73: "**Проверено [VERIFIED-exact]:** R_sym := ½(R + Rᴴ) точно совпадает с R (np.array_equal)."

**Why it is wrong.** The stored array is not exactly Hermitian: `max |R − Rᴴ| = 5.2·10⁻¹⁷` (`o3_v3/audit_tests/check_D1_D4.py` output; Codex audit 2026-11-01, `review_package/codex_logs/o3v3_codex_audit_2026-11-01.txt`, section 2). Line 103 of the same file already records this (`np.array_equal(R, Rᴴ)` gives False). Lines 71–73 contradict line 103.

**Corrected statement.** Let R₀ be the stored complex 20×20 array (binary64 entries). The certified object is

  H := (R₀ + R₀ᴴ)/2, computed **exactly in arb** from the binary64 entries (`interval_cells_v3.py:82–107`).

H is exactly Hermitian (as an arb matrix). For every y ∈ ℂ²⁰, Re(yᴴR₀y) = yᴴHy. The separator is therefore stated for H (equivalently for Re(yᴴR₀y)), not for R₀ itself. The statement "R is Hermitian" must be replaced by "the certified matrix is H = (R₀+R₀ᴴ)/2".

## E2 — Threshold definition (line 74; status: CLOSED here)

**Erroneous/ambiguous text.** Line 74: "Порог s := 0.9·tr R/20 = 0.01368236038871751". This reads as an exact real value.

**Corrected statement.** s* is the binary64 value of the sequential evaluation

  t := Σ_i Re(R₀)_ii  (exact sum of binary64 values, = tr H), then s* := fl( fl(0.9·fl(t)) / 20 ).

Value: **s* = 0x1.c057f53368882p−7 = 0.01368236038871751.** The exact real 9t/200 rounded once gives 0x1.c057f53368881p−7 = 0.013682360388717509, one ulp lower. The certificate proves the bound against the sequentially computed s* (`interval_cells_v3.py:56–59`, `s_target_f = FRAC * trR_f / 20.0`).

Check (`o3_v3/audit_tests/check_D1_D4.py`): `trH_f = 0.3040524530826113`, `s_seq − s_round_once = 1.73·10⁻¹⁸`.

## E3 — Trace (line 73–74 context; status: CLOSED here)

`tr R₀ = Σ R₀_ii` has a complex part of size 1.2·10⁻¹⁷ (imaginary diagonal entries). The γ used in the certificate is γ = tr H − 20 s*, with tr H = Σ Re(R₀)_ii exactly. Difference from tr R₀: 2.3·10⁻¹⁷. The certified γ = 0.030405245308261095 is the same to the printed precision.

## E4 — Other sentences that depend on E1–E3

The same wording ("R Hermitian", "tr R", "s = 0.9 tr R/20") appears in `review_package/REVIEW_BRIEF.md`, `review_package/PROOF_OBLIGATIONS.md` (B8, B10), `review_package/O3_AUDIT_RECORD.md` §4, `review_package/EVIDENCE_LEDGER.md` row 10, and `RESEARCH_MILESTONE.md`. Those documents are corrected in the same pass (see `FINAL_CONSISTENCY_2026-11-01.md`).

## Status of the original defects

| Defect | Source | Status | Basis |
|---|---|---|---|
| D1 | Codex: stored R not exactly Hermitian | **CLOSED** | E1: certified object is H, verified in code |
| D3 | Codex: STAGE_C line 73 false | **CLOSED** (erratum, text unchanged) | E1 |
| D4 | Codex: s* definition | **CLOSED** | E2: sequential binary64 value stated, exact value given |
| D2 | Codex: manifests for runs A–B not in its packet | **CLOSED** | `FINAL_CONSISTENCY_2026-11-01.md` §D2 |
