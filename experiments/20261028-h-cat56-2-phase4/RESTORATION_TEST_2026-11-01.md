# Restoration test, H-CAT56-2 milestone (2026-11-01)

Commit under test: `f0c6df5ccef9a5c7612f7436b4e64eed7f8c4a32` (branch `research/h-cat56-2-cfim-convention`, local only, not pushed).

## Procedure

1. `git clone` of the local repository into a scratch folder.
2. Extract `H-CAT56-2_large_artifacts_2026-10-31.tar.gz` (1 791 233 576 bytes, SHA-256 `411d9721ff2ec2221eae0cd7c252e6b55d5c40702d0522a33fd8748524543e30`) into the clone root.
3. `sha256sum -c experiments/20261028-h-cat56-2-phase4/ARCHIVE_SHA256SUMS.txt` from the clone root.
4. `sha256sum -c review_package/SHA256SUMS.txt` from `experiments/20261028-h-cat56-2-phase4`.
5. `python -I o3_v3/code/audit_v3_coverage.py 0 9 restoretest` on the restored tree.

## Results

| Run | Clone mode | Clone HEAD | Archive manifest | Review manifest | Audit chunks 0–9 |
|---|---|---|---|---|---|
| 1 | default (`core.autocrlf=true`) | f0c6df5… | 0 OK; all 7 938 entries unreadable (trailing `\r`) | 0 OK; all 84 entries unreadable | COMPLETE_STRICT |
| 2 | `-c core.autocrlf=false` | f0c6df5… | **7 938 OK / 0 failed** | 47 OK / 37 failed (of 84) | COMPLETE_STRICT |

Tracked phase4 files in the clone: 305 (both runs). Archive extraction exit 0 (both runs).

## Findings

**F1. Manifests fail on a default Windows clone (run 1).** With `core.autocrlf=true` git writes text files with CRLF on checkout. Every manifest line then carries a trailing `\r`, so `sha256sum -c` cannot open any file. Not data loss. Fix: clone with `git -c core.autocrlf=false clone …`.

**F2. Git did not keep the original bytes of text files with CRLF (run 2).** The 37 review-manifest files that fail contain CR bytes in the originals (for example 1 129 CR in `codex_logs/o3_codex_audit_2026-10-31.txt`, 133 in `STAGE_C_FINAL_PROOF.md`, 8 in `stage_e_v1/logs/exact_cert_result.json`). The git blobs and the clone contain none: on commit, `core.autocrlf=true` normalised CRLF to LF. Checked by byte count (`tr -cd '\r'`): originals 37/37 with CR, git blobs 0/37, clone 0/37. After removing CR the 37 files are identical to the originals, so the **content is the same, but SHA-256 pinned in certificates and manifests does not match the git copies**. Across all 305 committed text files, 135 contain CR bytes in the original.

**F3. Mitigation made (no repository setting changed).** A byte-exact snapshot of the 305 text files was taken from the working tree. It pins the state committed in `f0c6df5`; three of its files (`RESEARCH_MILESTONE.md`, `FINAL_CONSISTENCY_2026-11-01.md`, `review_package/SHA256SUMS.txt`) were edited afterwards in the documentation commit, so their newer versions are in git and not in the snapshot:
- `H-CAT56-2_milestone_archive_2026-10-31/H-CAT56-2_text_original_bytes_2026-11-01.tar.gz`, 2 726 241 bytes, SHA-256 `96105b63e2f6da1be0fe527523c8d227b1703135d694063d7a8f256ad7c7ebfa`.
- Manifest of the original bytes: `TEXT_ORIGINAL_BYTES_SHA256SUMS.txt` (305 lines, committed in the documentation commit that follows `f0c6df5`).
- Verified by extraction: 305 OK / 0 not OK.

For byte-exact certificate files use this archive, not the git checkout.

**F4. Not tested.** The 7 912 O3 record files were verified by hash (archive manifest) and chunks 0–9 were audited after restoration; the full audit of all 7 912 chunks on the restored tree was not rerun. The restored scripts were not executed beyond the coverage audit.

## Restoration commands

```bash
git -c core.autocrlf=false clone <local-repo-path> H-CAT56-2-restore
cd H-CAT56-2-restore
tar -xzf <path-to>/H-CAT56-2_large_artifacts_2026-10-31.tar.gz
sha256sum -c experiments/20261028-h-cat56-2-phase4/ARCHIVE_SHA256SUMS.txt
# byte-exact text files (certificates, manifests) for comparison:
mkdir ../H-CAT56-2-text-original && tar -xzf <path-to>/H-CAT56-2_text_original_bytes_2026-11-01.tar.gz -C ../H-CAT56-2-text-original
```

## Open decision (owner)

A permanent fix inside git would be a `.gitattributes` line `experiments/20261028-h-cat56-2-phase4/** -text` and re-adding the 135 files so the blobs keep CRLF. It changes repository configuration and rewrites those blobs in a new commit; it was **not** done without an owner decision.
