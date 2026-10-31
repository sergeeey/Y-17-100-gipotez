# O3 audit record (2026-10-31)

**Subject:** interval certificate for the separator R of S₋ = {4,…,15}: sup over unit y ∈ 𝒴¹ of yᴴRy ≤ s_float, with tr R − 20 s_float > 0.

**Independence.** Auditor: Codex CLI (a different model family from the one that wrote the proof text), run read-only, context-blind, on primary artifacts only. Full log: `review_package/codex_logs/o3_codex_audit_2026-10-31.txt` (SHA-256 67bc99dd…; reported as `tokens used 120 932`). This is an automated cross-model audit, **not** an external expert review.

**Codex verdict: PASS WITH CONDITIONS, confidence 8/10.**

## 1. Codex findings, with my reconciliation

| # | Codex item | Codex status | My check | Result |
|---|---|---|---|---|
| 1 | phi_rows defines exactly the real constraints A_iᴴy ∈ ℝx | CONFIRMED | read `discovery/code/s8_admissible_span.py` lines 46–58: g₁ = x₀a₁ − x₁a₀, g₃ = x̄₀a₀ + x̄₁a₁, real/imag split correct | CONFIRMED |
| 2 | Cell lemmas L1–L4 correct as implemented | CONFIRMED | not re-derived; consistent with `STAGE_C_FINAL_PROOF.md` §5 | CONFIRMED (by Codex; not re-read by me) |
| 3 | Directed rounding | REFUTED as fully rigorous | selection by `float(...)` at `interval_cells_v2.py` lines 111, 116, 203, 175, 229 (ulp-scale; see §3) | Confirmed as a formal gap |
| 4 | Strict gap | CONFIRMED for the binary target; REFUTED for literal 0.9·tr R/20 | **recomputed:** s_float − 9 tr R/200 = +1.8041124150158794·10⁻¹⁸ (exact rational); tr R − 20 s_float = 0.030405245308261095 | Confirmed numerically |
| 5 | Covering | UNCHECKED from listed artifacts | `o3_v2/metrics/tiling_exact_check.json`: verdict TILING_EXACT, 3 955 841 leaves matched, 5 274 284 tree nodes visited, 0 uncovered at depth 10 | Exact tiling file exists; verifier code not re-read |
| 6 | Journaling | CONFIRMED as aggregate; not per-leaf | **recomputed:** 7 912 distinct chunks, IDs = 0…7911, Σn = Σok = 3 955 841, Σfails = 0 (`o3_progress.jsonl`) | CONFIRMED |
| 7 | Historical caveats | CONFIRMED not to invalidate v2, with provenance condition | `logs/o3_run_v2.log`: two invocations (first 1 710 500 leaves, chunks 0…3420, no end marker; RESUME 20:39:16 Oct 29, 2 245 341 leaves, 21 925 s); code mtimes 14:54–14:56 Oct 29 precede both | CONFIRMED; first-invocation termination reason UNKNOWN |
| 8 | Dependencies outside phase4 | CONFIRMED | `s8_admissible_span.py` (discovery), instance and R (submission package and phase3) are read by path; hashes of R (55b898d6…) equal across the two copies | CONFIRMED; driver does not enforce these hashes |

## 2. Reconciliation of the leaf count (DoD 1)

- Chunk journal: 7 912 chunks = ⌈3 955 841/500⌉. Chunks 0…3420: 3 421 × 500 = **1 710 500** leaves, elapsed up to 20 375.8 s (first invocation). Chunks 3421…7911: 4 490 × 500 + 341 = **2 245 341** leaves, elapsed from 46.9 s (RESUME). Total 3 955 841.
- `ok_this_run = 2 245 341` in `o3_summary.json` is the **resumed invocation's counter only**, not the total. Codex and the driver's skip-logic (`o3_run_v2.py` lines 66, 131) confirm this.
- Total compute: ≈ 5.66 h (first) + ≈ 6.09 h (resume) ≈ **11.7 h**, against a 4-h-per-run budget. Each invocation exceeded the single-run limit. The first invocation's stop reason is not recorded in the log (no traceback, no summary).
- Code: the three code files have mtime 14:54–14:56 Oct 29, before the first invocation started (≈ 14:59). Both invocations therefore used the same code, **inferred from mtimes**, not from a per-record hash.

## 3. Floating-point points (DoD 2): status of each

| Location | Operation | Effect | Status |
|---|---|---|---|
| `interval_cells_v2.py` l.111 | Gershgorin row choice via `float(up) > float(best)` | may keep the smaller of two arb uppers that round to the same float | **open**, ulp-scale |
| l.116 | norm choice `key=float` | same | **open**, ulp-scale |
| l.203 | max Gram-defect row chosen after float conversion | same | **open**, ulp-scale |
| l.175 | kernel-certificate row sums in `float(x.upper())` | ulp-scale error in a certificate sum | **open**, ulp-scale |
| l.229 | `float(lam_up) > 0` | underflow could drop a tiny positive λ_K | **open**, only if λ_K ≈ 10⁻³⁰⁸ (not expected) |
| l.90 | `s_target = arb(s_target_f)` | exact injection of the binary64 threshold | exact (by definition of s*) |
| l.40–42 | Hermitian average in float | ≈ 10⁻¹⁷ difference from the arb symmetrisation | bounded; far below slack |
| l.138 | `+ arb(1e-12)` margin | positive safety margin, direction correct | exact |
| driver `float(s−b)`, `float(b)` | reporting only | acceptance uses arb `s−b > 0` (`o3_run_v2.py` l.109) | not on the decision path |

**Quantitative bound on the ulp-scale items:** each float selection can change a certified upper by at most one binary64 ulp of the candidate (≈ 2·10⁻¹⁶ relative). The recorded minimum slack in the resumed run is 8.40·10⁻⁹, so these items cannot change any resumed-run decision. For chunks 0…3420, **the per-leaf slack is not recorded**, so the same bound cannot be checked there. This is the residual gap.

## 4. Threshold definition (resolution of Codex item 4)

The certificate proves B_up < s_float on every leaf, where **s_float = fl(0.9 · tr R / 20) = 0.01368236038871751**. The exact real 0.9·tr R/20 differs from s_float by +1.80·10⁻¹⁸ (recomputed). Resolution: **define the separator constant as s\* := s_float** (binary64, explicit). Then γ := tr R − 20 s\* = **0.030405245308261095** (arb-certified). The literal "s\* = 0.9·tr R/20" in the review text is replaced by this definition. This changes no computed number.

## 5. Status after the audit

| Claim | Status |
|---|---|
| Separator: sup_{𝒴¹} yᴴRy ≤ s_float for all leaves of the resumed chunks 3421…7911 | **VERIFIED-INTERVAL** (arb ok flags, per-leaf slack minimum 8.40·10⁻⁹ recorded) |
| Same for chunks 0…3420 | **VERIFIED-INTERVAL with condition C-O3-1**: chunk-level ok flags only, no per-leaf slack |
| Tiling / coverage of all x ∈ S³ | **VERIFIED-EXACT** (`tiling_exact_check.json`, TILING_EXACT); verifier code re-read: not yet |
| γ = tr R − 20 s_float ≥ 0.0304 | **VERIFIED-INTERVAL** (`final_gap`, arb 192 bits) |
| Literal s\* = 0.9·tr R/20 | **FALSIFIED as an exact-real statement** (off by 1.8·10⁻¹⁸); not used after the definition in §4 |

## 6. Conditions on the O3 certificate

- **C-O3-1 (early records):** chunks 0…3420 have no per-leaf slack or B_up. A strict record needs a re-run with per-leaf logging, or a stored chunk-level minimum slack. Cost: ≈ 5.7 h of compute, split into two ≤ 4-h invocations (within 24 cores per run).
- **C-O3-2 (float selections):** replace the four float-based selections at l.111, l.116, l.175, l.203 by arb-only comparisons, and l.229 by an arb sign test. This is needed only for a strictly formal certificate; it needs a re-run together with C-O3-1.
- **C-O3-3 (provenance):** the driver does not enforce expected hashes for the external R, the instance, `s8_admissible_span.py`, or the code. Hashes are listed in `review_package/SHA256SUMS.txt`; enforcement needs a driver change.
- **C-O3-4 (documentation):** `STAGE_C_FINAL_PROOF.md` line 73 states that the float symmetrisation equals the stored matrix; the later correction (line 103) and the code say it does not. The text should be corrected; the certificate itself uses H = (R_raw + R_rawᴴ)/2 in arb.

## 7. Effect on Theorem N

- With s\* = s_float, Theorem N for F_U keeps γ ≥ 0.0304 and its constants. Its status is **PROVED-hand, conditional on the separator (VERIFIED-INTERVAL with conditions C-O3-1 to C-O3-4)**.
- If C-O3-1 cannot be closed, the separator is verified for chunks 3421…7911 only with per-leaf evidence; for chunks 0…3420 the claim rests on arb ok flags, which the code emits only after a passing arb comparison. The Theorem N statement for F_U then depends on the correctness of that code path for those 1 710 500 leaves, which is not independently re-observable from the stored records.

## 8. Decision required from the owner

Re-run chunks 0…3420 with per-leaf slack logging and arb-only selection (≈ 5.7 h, two invocations). The constraint is 24 cores and 4 h per run. This is a computational decision and was not started.

## 9. Strict re-certification, v3 (2026-10-31): supersedes §8 and closes C-O3-1, C-O3-2

The decision in §8 was carried out as a new certificate, `o3_v3/`, leaving `o3_v2/` unchanged as history.

**What changed (v3 vs v2).**
- Per-leaf records for all 3 955 841 leaves (`o3_v3/records/chunk_XXXXX.jsonl.gz`, one JSON line per leaf: `ok`, `slack` as arb enclosure, `bup` as arb enclosure, or the failure status and reasons). The chunk-level SHA-256 of each record file is in the journal `o3_v3/metrics/o3v3_progress.jsonl`.
- Decisions are arb-only. `interval_cells_v3.py` contains no float comparison in any selection; the Gershgorin row choice, the norm choice, the Gram-defect maximum and the kernel-certificate sums all use arb `max`/`min` (`max(a,b) = (a+b+|a−b|)/2`). The float SVD and eigendecomposition only seed similarity transforms; the bounds are computed in arb on `V⁻¹BV`, which is valid for any invertible `V`. A poor seed can only produce a recorded failure, never a silent pass.
- The driver's run minimum is an arb `min`, not a float selection. The driver asserts `final_gap > 0` (arb) before starting and refuses to run otherwise.
- Preflight `o3_v3/metrics/preflight_v3.json`: PASS. 2 000 random arb identity pairs with 0 enclosure failures; negative controls (broken projector rejected; lowered threshold rejected); the 1 000 closest cells, all certified with arb-certain positive slack.

**Runs (each ≤ 24 workers, each a separate invocation, disjoint chunk ranges).**

| Run | Chunks | Leaves | Audit verdict | Min slack (arb enclosure) | Max B_up (arb enclosure) |
|---|---|---|---|---|---|
| A | 0–1710 | 855 500 | COMPLETE_STRICT | [3.1338e-8 ± 6.7e-13] | [0.01368232905 ± 2.3e-12] |
| B | 1711–3420 | 855 000 | COMPLETE_STRICT | [2.9217e-8 ± 7.1e-13] | [0.01368233117 ± 2.6e-12] |
| C | 3421–5600 | 1 090 000 | COMPLETE_STRICT | [8.40e-9 ± 5.2e-12] | [0.01368235198 ± 6.1e-12] |
| D | 5601–7911 | 1 155 341 | COMPLETE_STRICT | [2.022e-8 ± 5.8e-12] | [0.01368234016 ± 5.9e-12] |

Coverage: 1711 + 1710 + 2180 + 2311 = 7 912 chunks; 855 500 + 855 000 + 1 090 000 + 1 155 341 = 3 955 841 leaves. No duplicates, gaps, failed leaves, or record-hash mismatches (`o3_v3/metrics/audit_run*.json`, `problems: []`). Overall minimum certified slack = the run C value, 8.40·10⁻⁹ (lower bound positive); overall maximum B_up is below s_float = 0.01368236038871751 by ≈ 8.4·10⁻⁹.

**Code integrity.** The SHA-256 of `o3_run_v3.py` and `interval_cells_v3.py` in the manifests of runs C and D equal the files on disk; the code files were last modified before run C started. Input hashes (leaves, R, instance, `s8_admissible_span.py`) are recorded in each `run_manifest_run*.json`.

**Status after v3.**
- Separator, all leaves of chunks 0–7911: **VERIFIED-INTERVAL (strict v3)**. Internal only: this is the same model family and author chain, and no one has yet audited the v3 code independently.
- C-O3-1 (no per-leaf slack for 0–3420): **closed** for v3.
- C-O3-2 (float selections on the decision path): **closed** for v3.
- C-O3-3 (driver does not enforce expected input hashes): **open**. Hashes are recorded in the manifests but not checked by the driver.
- C-O3-4 (stale text in `STAGE_C_FINAL_PROOF.md` l.73): **open**. Not edited in this pass.
- Not in the review package: the 7 912 record files themselves (about 3.9 M lines, large). Their chunk hashes are in the journal, so the records can be checked against the journal once the files are supplied.
- The Codex audit in §1 was for v2 code. An independent audit of `o3_v3/code/` is still needed.
