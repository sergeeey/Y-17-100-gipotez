# Final consistency and preservation check, H-CAT56-2 (2026-11-01)

**Verdicts.** O3 v3: **PASS** (internal; not externally reviewed). NOVELTY: **PARTIAL** (central subset-dependence claim NOT ESTABLISHED as new). PRESERVATION: **VERIFIED LOCALLY, NO REMOTE COPY** (commit `f0c6df5`; archive 7 938/7 938 OK; restoration tested; git normalised CRLF in 135 text files, byte-exact snapshot added). Everything exists on one machine only.

Historical documents are unchanged. `STAGE_C_FINAL_PROOF.md` SHA-256 = 682eaad1…f56f4e (before and after). Errors are corrected in `ERRATA_STAGE_C_FINAL_PROOF.md`.

## 1. D1: the certified functional is the Hermitian part H

**Claim.** The certificate bounds Re(yᴴR₀y) for the stored complex array R₀, because it bounds yᴴHy with H = (R₀+R₀ᴴ)/2.

**Evidence (code).**
- `o3_v3/code/interval_cells_v3.py:82–104` builds the 40×40 real form from `re[i][j] = (Re R₀_ij + Re R₀_ji)/2` and `im[i][j] = (Im R₀_ij − Im R₀_ji)/2`, all in arb from binary64 entries. These are the real and imaginary parts of H_ij, computed exactly. The block form is `[[A, −B],[B, A]]` with A = Re H, B = Im H.
- `interval_cells_v3.py:107` `Mb` is this form. `cell_bound` (lines 232–239) uses only `Mb`, `M2 = Mb·Mb` and `mn_up = ‖Mb‖`. The R₀ array is never used directly.

**Evidence (numerical).** `o3_v3/audit_tests/check_D1_D4.py`:
- max |R₀ − R₀ᴴ| = 5.204·10⁻¹⁷; max |Im diag R₀| = 1.175·10⁻¹⁷.
- Random test (`dense_sup_grid.py`, 200 random y): |Re(yᴴR₀y) − [y;ȳ-form] of H| = 1.8·10⁻¹⁵.

**Conclusion.** The certified object is H_exact = (R₀+R₀ᴴ)/2 computed in arb. For any y, Re(yᴴR₀y) = yᴴHy. The separator is therefore stated as sup over unit y of Re(yᴴR₀y), or equivalently for the Hermitian matrix H. **Status: CLOSED.** Replacing the wording of R by H is not the proof; the proof is the code path above, which uses only H.

## 2. D4 and the trace: definitions of tr and s*

- t := Σ_i Re(R₀)_ii = tr H (exact in arb: `tr_exact`, `interval_cells_v3.py:110`). Difference from the complex trace of R₀: |tr R₀ − tr H| = 2.3·10⁻¹⁷ (`check_D1_D4.py`).
- s* is the binary64 value of the sequential evaluation `FRAC * trR_f / 20.0` (`interval_cells_v3.py:56–59`, FRAC = 0.9), i.e. s* = fl(fl(0.9·t)/20).
  - Value: **0x1.c057f53368882p−7 = 0.01368236038871751** (`check_D1_D4.py`: `s_seq`).
  - Exact rational 9t/200 rounded once: 0x1.c057f53368881p−7 = 0.013682360388717509. The difference is 1.73·10⁻¹⁸.
- γ = tr H − 20 s* = 0.030405245308261095 (`check_D1_D4.py`; arb `final_gap`, `interval_cells_v3.py:112`, asserted > 0 by the driver).

**Conclusion.** The certificate proves the bound against the sequentially computed s*. This is the value every dependent document now states. **Status: CLOSED** (D4).

## 3. D3: STAGE_C line 73

Line 73 (and lines 71–72) claim that R is exactly Hermitian. Line 103 of the same file records the false result. The erratum states the corrected claim. **Status: CLOSED by erratum; historical text unchanged.**

## 4. D2: manifests A–D and coverage

| Run | Chunks | Leaves | Manifest | leaves.npy | interval_cells_v3.py | o3_run_v3.py | R_input.npz | instance.jsonl | s8_admissible_span.py |
|---|---|---|---|---|---|---|---|---|---|
| A | 0–1710 | 855 500 | run_manifest_runA.json | 29ab7b14… | bd719f0f… | 25e852af… | 55b898d6… | 05289920… | 72a690f9… |
| B | 1711–3420 | 855 000 | run_manifest_runB.json | same | same | same | same | same | same |
| C | 3421–5600 | 1 090 000 | run_manifest_runC.json | same | same | same | same | same | same |
| D | 5601–7911 | 1 155 341 | run_manifest_runD.json | same | same | same | same | same | same |

- Disk hashes of all six files equal the entries above (checked 2026-11-01).
- Chunk ranges are contiguous and disjoint: 0–1710, 1711–3420, 3421–5600, 5601–7911. Sum 7912 chunks, 3 955 841 leaves.
- Codex was given only runs C and D manifests (`review_package/codex_logs/o3v3_codex_prompt_2026-11-01.txt`). That gap was in its packet. The files for A and B exist in the repository. **Status: CLOSED.** Limits: the manifests are self-reported by the run driver; the driver does not enforce hashes (C-O3-3, still open).

## 5. Threshold and separator: summary of the O3 verdict

- Certified: every leaf has B_cert < s*, with minimum slack 8.40·10⁻⁹ (run C) and maximum B_cert = 0.01368235198 (run C). Strict v3, arb-only decisions.
- Independent, not certified: dense grid (31×61) sup ≈ 0.00212; cell test on the 1 000 tightest cells (5×5 and 9×9): 0 violations, worst ratio 0.159.
- Codex (cross-model, read-only): sections 1–8 PASS; section 2 CONDITIONAL only on the stored-R wording (D1); section 7 CONDITIONAL only on the packet (D2); section 5 PASS with the one-ulp note (D4).

**O3 v3 verdict: PASS** (internal). Basis: the audited lemma, the arb decision logic, the closed definitions D1/D2/D4, and the integrity checks. **Not** an external review. Not a full independent recomputation of the 3 955 841 cells (not performed: no concrete defect was found that would justify it).

## 6. NOVELTY

Matrix: `NOVELTY_MATRIX.md`. Summary:
- Full text read: Suzuki–Yang–Hayashi (1911.02790v3), sections 4.1 and 5.4 (text 4.4). Their D-invariance and asymptotic-classicality conditions (eqs. 102–104) are the closest prior framework for the central subset-dependence claim. Their text says these results are "not reported in literature" (their claim).
- Abstract read: Nurdin 2402.11567v5; Nurdin 2405.01471 is **withdrawn** (arXiv v2, 22 Dec 2024: irreparable error in Lemma 2 §4; Corollaries 2, 3 and Theorem 3 incorrect), so it is not used; Yang–Pang–Zhou–Jordan 1806.07337v3 (Lemma 3 excerpt).
- **Not accessible:** the IEEE correction (DOI 10.1109/LCSYS.2024.3451468) — **UNKNOWN**. Any statement depending on what it changed is UNKNOWN.
- Not done: test of S₊ and S₋ against D-invariance (Suzuki eq. 102) and against the conditions of 2402.11567 (2405.01471 is withdrawn). Until done, the subset-dependence claim is **NOT ESTABLISHED** as new.

**NOVELTY verdict: PARTIAL.** Supported: the instance-level S₊ certificate, the uniform trace-gap no-go for S₋ (under the conventions and the audited separator), and the rank-jump counterexample. Not supported: the subset dependence as a new phenomenon.

## 7. PRESERVATION

| Item | State | Status |
|---|---|---|
| 288 phase4 text files | staged in git index (`git diff --cached`: 288 files, all under phase4) | staged, not committed |
| RESEARCH_MILESTONE.md, ERRATA, FINAL_CONSISTENCY, NOVELTY_MATRIX, O3_V3_INDEPENDENT_AUDIT, the audit tests | not yet staged | pending |
| Archive `H-CAT56-2_large_artifacts_2026-10-31.tar.gz` (outside repo) | 1.79 GB; `gzip -t` OK | integrity of the stream verified |
| Archive SHA-256 and entry count | computed in background | see §8 |
| ARCHIVE_SHA256SUMS.txt (7 938 entries) | written, committed to git only after commit | pending |
| Commit | **not made** (the goal forbids commit) | held |
| Push / remote backup | **none** (origin is a GitHub remote; nothing pushed) | local only |
| Restoration test | performed 2026-11-01 after commit `f0c6df5`: archive 7 938/7 938 OK in a byte-exact clone; audit of chunks 0–9 COMPLETE_STRICT; 37 manifest files differ from the git checkout by CR only (git normalised CRLF in 135 of 305 text files). Byte-exact snapshot added (305/305 OK). See `RESTORATION_TEST_2026-11-01.md` | done, with that finding |

**PRESERVATION verdict: INCOMPLETE.** The data is on local disk; the commit, the restoration test and the remote copy are missing.

## 8. Archive checks

- Archive `H-CAT56-2_large_artifacts_2026-10-31.tar.gz` (in `H-CAT56-2_milestone_archive_2026-10-31/`, outside the repository): size 1 791 233 576 bytes; SHA-256 `411d9721ff2ec2221eae0cd7c252e6b55d5c40702d0522a33fd8748524543e30`; `gzip -t`: OK; non-directory entries: 7 938 (= 7 933 phase4 files + 5 external inputs), matching `ARCHIVE_SHA256SUMS.txt` (7 938 lines).
- Extraction into a fresh scratch folder: 7 938 files present. Per-file check against `ARCHIVE_SHA256SUMS.txt`: see §8a.

### 8a. Per-file verification of the extracted archive

Result: **7 938 OK, 0 FAILED** (`sha256sum -c ARCHIVE_SHA256SUMS.txt` run in the extracted folder). The archive's file contents match the manifest. This verifies the archive, not a restored repository: the restoration test (clone plus archive) still needs a commit and remains **not performed**.

## 9. Open items (not closed here)

- C-O3-3: the driver does not enforce input hashes. A code change; not started.
- Nurdin IEEE correction [S4]: UNKNOWN.
- Test of S₊ and S₋ against Suzuki D-invariance (eq. 102) and the conditions of 2402.11567: not performed.
- Independent review by a mathematician or a model from another family for the proof chain: not performed.
