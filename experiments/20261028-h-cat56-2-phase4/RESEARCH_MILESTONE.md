# RESEARCH_MILESTONE — H-CAT56-2 (state on 2026-10-31)

Frozen internal state of the H-CAT56-2 research line: S+ existence certificate, S− no-go (Theorem N for F_U), O3 v3 separator certification. Every status below is internal: the same model family and the same author chain produced all of it. **No external review has been performed.**

Branch at freeze: `research/h-cat56-2-cfim-convention`. Remote: none pushed. Local only.

## 1. Status by claim

Evidence markers follow `integrity.md`. "Internal" = single model family, same author chain. "Codex" = a read-only cross-model audit; it is not an external expert review.

| # | Claim | Status | Evidence (path, relative to repo root) |
|---|---|---|---|
| S+.1 | Logic of the existence theorem: 1764 rank-one regular outcomes on 280 directions saturate the 12×12 QFIM at θ=0 | PROVED-hand (internal). Codex S+ audit: **PASS WITH CONDITIONS, 8/10**; YPZJ theorem text not checked by Codex; the "identical M\* checked twice" claim is UNCHECKED (the two runs use different y) | `experiments/20261028-h-cat56-2-phase4/S_PLUS_CERTIFICATE_FINAL_v2.md` §1; `review_package/codex_logs/splus_codex_audit_2026-10-31.txt` |
| S+.2 | 484 coordinate equalities A·M = b hold exactly, over ℚ (run A) | VERIFIED-EXACT | `stage_e_v1/logs/exact_cert_result.json` (rows_violated_exactly 0, independent rows 175) |
| S+.3 | Same 484 equalities hold exactly, over ℤ with an independently built A (run B) | VERIFIED-EXACT | `stage_e_v1/logs/verify_exact_integer_v3.json` (rows_checked 484, violated 0) |
| S+.4 | All 280 blocks are positive definite, exactly (ℚ and ℤ) | VERIFIED-EXACT | both logs above |
| S+.5 | Inputs are shared between the two runs (bases, start moments, row list); y is recomputed in run A but only loaded from checkpoint in run B | CONDITIONAL on inputs: not regenerated independently | `S_PLUS_CERTIFICATE_FINAL_v2.md` §4 |
| S+.6 | CFIM = QFIM at θ=0 via YPZJ thm:reg (saturation ⇔ A_aᴴy = ξ_a x, ξ real) | PROVED given YPZJ (arXiv:1806.07337, LaTeX read, not checked by Codex); numeric control: relative trace deficit 2.4·10⁻¹² (matrix max error 1.5·10⁻¹⁰) | `stage_e_v1/logs/control_differential.json` |
| S+.7 | Exact POVM elements written out as rationals | NOT DONE (not needed for existence; irrational ĉ from Cholesky) | `S_PLUS_CERTIFICATE_FINAL_v2.md` §5–6 |
| S−.1 | Theorem N for F_U: uniform trace gap tr(F^Q(sh) − F_E(sh)) ≥ c for finite and Borel POVMs, D1 convention | PROVED-hand (internal), conditional on the separator (S−.2) | `experiments/20261028-h-cat56-2-phase4/review_package/REVIEW_BRIEF.md`; `PROOF_OBLIGATIONS.md` B3–B16 |
| S−.2 | Separator: sup over 𝒴¹ of Re(yᴴR₀y) = yᴴHy ≤ s* with H = (R₀+R₀ᴴ)/2 (exact), s* = fl(fl(0.9·tr H)/20) = 0x1.c057f53368882p−7, γ = tr H − 20 s* ≥ 0.0304 (see `ERRATA_STAGE_C_FINAL_PROOF.md`) | VERIFIED-INTERVAL (strict v3, internal; see §2) | `o3_v3/metrics/audit_run{A,B,C,D}.json` |
| S−.3 | D2 trace limit along each fixed ray: trace ≤ tr F^Q(0) − c | PROVED-hand | PROOF_OBLIGATIONS B15–B16 |
| S−.4 | D2 limit along arbitrary curves | FALSE in general (direction-dependent null-outcome limits); only limsup along curves holds | PROOF_OBLIGATIONS B15 |
| S−.5 | Borel transition: F^C_M = sup over partitions = integral, θ-independent μ = tr M | PROVED-hand (Prop 7) | `ARTICLE_DRAFT_v4_2026-10-31.md` |
| S−.6 | General C¹ families: Theorem N | CONDITIONAL on an existing separator with γ > 0 | REVIEW_BRIEF "Not claimed" |
| S−.7 | General C¹ families: N₁ limit form and Prop 8 | FALSIFIED (rank jump; toy 65.51 vs 61.51, trace jump 3.9976). The factor 4 in "4 tr τ" was checked only with tr τ = 1 in the toy, so it is not tested separately | `toy_rank_jump/rank_jump_check.out`, `povm8_jump.out` |
| S−.8 | Without continuity of ∂ρ at 0, the uniform statement for general families | FALSIFIED (explicit counterexample); minimality of the condition NOT established | `THEOREM_NATURAL_D2_NOGO_v8.md` |
| S−.9 | Composite criterion (Nurdin arXiv:2402.11567 v5) does not apply to S− (264 < 399 generators) | PROVED-hand (counting) | `EVIDENCE_LEDGER.md` ledger rows 23–24 (file lines 29–30) |
| S−.10 | Nurdin IEEE CSL correction (DOI 10.1109/LCSYS.2024.3451468) | UNKNOWN: full text not available locally | — |
| S−.11 | Professor's 20×3 construction does not close S− | UNKNOWN: construction not in the files | — |
| S−.12 | Novelty of instance-level S+/S− results | PARTIAL: known literature checked by search excerpts only (2402.11567, 1806.07337, 2602.12097); priority UNKNOWN | `EVIDENCE_LEDGER.md` row 25 |

## 2. O3 v3 certification (strict)

- Scope: 7 912 chunks of 500 leaves (the last chunk has 341), 3 955 841 leaves in total. Chunk ranges of runs A–D are disjoint and cover 0…7911.
- Each leaf: one arb ball enclosure with 192-bit precision; decision `s* − B_up > 0` evaluated by arb comparison; per-leaf record stored (`o3_v3/records/chunk_XXXXX.jsonl.gz`); journal `o3_v3/metrics/o3v3_progress.jsonl` holds each chunk's record SHA-256.
- Results (`o3_v3/metrics/audit_run*.json`, all `COMPLETE_STRICT`, `problems: []`):

| Run | Chunks | Leaves | Failed leaves | Min slack, arb enclosure | Max B_up, arb enclosure |
|---|---|---|---|---|---|
| A | 0–1710 | 855 500 | 0 | [3.1338e-8 ± 6.7e-13] | [0.01368232905 ± 2.3e-12] |
| B | 1711–3420 | 855 000 | 0 | [2.9217e-8 ± 7.1e-13] | [0.01368233117 ± 2.6e-12] |
| C | 3421–5600 | 1 090 000 | 0 | [8.40e-9 ± 5.2e-12] | [0.01368235198 ± 6.1e-12] |
| D | 5601–7911 | 1 155 341 | 0 | [2.022e-8 ± 5.8e-12] | [0.01368234016 ± 5.9e-12] |

- Overall: minimum certified slack 8.40·10⁻⁹ (run C); maximum B_up below s* = 0.01368236038871751 by ≈ 8.4·10⁻⁹.
- Preflight `o3_v3/metrics/preflight_v3.json`: PASS (2 000 arb identity pairs with 0 failures; negative controls rejected; 1 000 closest cells certified).
- Decision path is arb-only. Float is used only to seed eigenvectors and the SVD of a similarity transform; the bounds are computed in arb on V⁻¹BV and do not depend on the seed's accuracy.
- Code hashes match the run manifests (runs C and D). Input hashes: leaves 29ab7b14…, R 55b898d6…, instance 05289920…, `s8_admissible_span.py` 72a690f9….

**Still open (O3):**
- C-O3-3: the driver records expected input hashes but does not check them.
- C-O3-4: `STAGE_C_FINAL_PROOF.md` line 73 still says the float symmetrisation equals the stored matrix; the code and the later correction say it does not.
- No independent audit of the v3 formulas yet (see §4, next stage).
- Codex audit (`review_package/O3_AUDIT_RECORD.md` §1) was run on v2 code only.

## 3. Provenance gaps found while freezing (do not hide)

- `stage_e_v1/logs/exact_povm_Mstar.json` (3 082 831 319 bytes, 3.08 GB) is written by `stage_e_v1/code/exact_povm.py` (lines 144–148). The log `exact_povm.log` records "M* saved 5233.6 s", and `REPORT_STAGE_E_v2_2026-10-31.md` names the file. Its origin is therefore established. What did not finish is the later LDL step (`S_PLUS_CERTIFICATE_FINAL_v2.md` §6), whose result file does not exist. No certificate reads `exact_povm_Mstar.json`: it appears only in `exact_povm.py`, `REPORT_STAGE_E_v2`, and the archive manifest. It is kept unmodified.
- `o3_v2/inputs/leaves.npy` and `o3_v3/inputs/leaves.npy` are identical (SHA-256 29ab7b14…). Both are kept.
- Files `stage_e_v1/logs/*.bak-*` and `PROOF_CERTIFICATES/SHA256SUMS.txt.bak-*` are kept unmodified.
- The H-CAT56-2 tree was **untracked** in git before this commit. The external inputs (discovery, submission package, phase3) are also untracked and are not in the commit; they are in the archive instead.

## 4. Open questions and next scientific stage

Next stage (no large computation before it): **independent audit of the O3 v3 formulas**, then the package for Prof. Nurdin.

Items for that audit:
1. arb semantics of `max`/`min`, `contains_zero`, and the margin 10⁻¹² in du (`o3_v3/code/interval_cells_v3.py`).
2. `phi_rows` in `s8_admissible_span.py` (real constraints A_iᴴy ∈ ℝx).
3. Provenance and precision of R (float column generation; certificate applies to the recorded exact matrix).
4. Cell lemmas L1–L4, kernel certificate (a)–(d), and projector P.
5. Tiling verifier code (`o3_v2/metrics/tiling_exact_check.json`, TILING_EXACT; verifier not re-read).

Other open items:
- C-O3-3 (driver hash enforcement), C-O3-4 (STAGE_C l.73 text).
- S+: independent regeneration of bases and y (the shared-input condition S+.5); explicit POVM elements not written.
- YPZJ saturation lemma: independent check of the primary text.
- Novelty: full literature search; priority unknown.
- Nurdin IEEE CSL correction: full text needed; not available locally.
- Professor's 20×3 construction: not in the files.
- General C¹ extension: conditional; explicit s₁, c and θ₀ are not explicit (θ₀ and C₀ come from Łojasiewicz).
- External review: none. `review_package/DRAFT_TO_NURDIN.md` is unsent and has placeholders for author name and affiliation.

## 5. Artifacts and how they are kept

- **Git (local commit, no push):** text sources, documents, journals, logs, JSON results, manifests — 288 files under `experiments/20261028-h-cat56-2-phase4/`, plus this file and `ARCHIVE_SHA256SUMS.txt`. Excluded from git: `.claude/` and `__pycache__/` (tool state), and binary or large files (see archive).
- **Archive (outside the repo, local disk):** `H-CAT56-2_milestone_archive_2026-10-31/H-CAT56-2_large_artifacts_2026-10-31.tar.gz`. Contents: all 7 912 O3 v3 record files `o3_v3/records/chunk_XXXXX.jsonl.gz`; `leaves.npy` (two copies); the 3.08 GB JSON and other `.npy`, `.npz`, `.pkl`, `.bak-*` files in phase4; and five external inputs (discovery `s8_admissible_span.py`, the R and prefix `.npz` files, the instance `.jsonl`, the phase3 R copy). Paths inside the archive are relative to the repo root, so it extracts into a repo copy.
- **Per-file manifest:** `experiments/20261028-h-cat56-2-phase4/ARCHIVE_SHA256SUMS.txt` (SHA-256 of every archived file, committed to git so the hashes are in history).
- **Restoration:** see §6.

## 6. Restoration

```bash
git clone <local-repo-path> H-CAT56-2-restore
cd H-CAT56-2-restore
tar -xzf <path-to>/H-CAT56-2_large_artifacts_2026-10-31.tar.gz
sha256sum -c experiments/20261028-h-cat56-2-phase4/ARCHIVE_SHA256SUMS.txt
```

The restoration test result is recorded separately (`RESTORATION_TEST.md`) and lists what was checked and what was not.

## 7. Backup status

Local only. The repository has a configured remote (`origin`, GitHub). Nothing has been pushed; this freeze exists only on this machine. No release has been created, and the archive has not been transferred.

## 8. Privacy and publication checks (before any push)

A security pass over the 288 staged files returned COMMIT_WITH_NOTES, with no BLOCK for a local commit. No secrets, tokens or real email addresses were found in the working-tree copies (the `@` hits are numpy matrix products). The following must be settled before a push:

1. `review_package/DRAFT_TO_NURDIN.md` is an unsent draft letter to a third party, with placeholders. It is not covered by `.gitignore`. Decide whether it stays local (ignore it and unstage) or is published.
2. `review_package/codex_logs/*.txt` contain raw tool-session transcripts with paths of the form `C:\Users\serge\...` and global rules text. Least useful to publish; redact or exclude.
3. About 36 files contain absolute paths with the user folder name. `HANDOFF_2026-10-30.md` lines 38–40 is one example. Redact or exclude before publishing.
4. Eleven numeric hits matching a 12-digit or phone-like pattern in four text files (`O3_AUDIT_RECORD.md`, `control_differential_stdout.txt`, two Codex logs) were **not inspected**. They are most likely hash or numeric strings. Unverified.
5. Versioned drafts (`ARTICLE_DRAFT*`, `RESEARCH_MEMO_DRAFT*`, `EVIDENCE_LEDGER_*` v1–v5) are unpublished claims and carry a submission gate; they must not be presented as final.
