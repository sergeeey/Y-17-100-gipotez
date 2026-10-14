# Memory audit — pre-registration (written 2026-10-14, BEFORE any improvement code)

Question type (EstimandOps L0): **Descriptive** (how accurate / complete / fresh is the memory the model actually receives)
+ a deterministic **intervention test** (same corpus, before vs after). No causal claim about people or model quality.

Scope = the 3 stores a session depends on: (S1) `.claude/memory/activeContext.md` (injected whole by
`~/.claude/hooks/session_start.py:619-621`), (S2) project auto-memory `~/.claude/projects/<proj>/memory/` (MEMORY.md index is
always loaded), (S3) hook-driven compaction `~/.claude/hooks/pre_compact.py::_create_progressive_summary`.

## Already known before pre-registering (recon, stated for honesty — not a result)
- 3 stale state-claims found by hand: "25776d4 not pushed", "MathOverflow post drafted/pending", "post_commit_memory fix UNCOMMITTED".
- `session_start.py` prints the whole 52 KB activeContext; the harness showed only a 2 KB preview of the 50 KB hook output.

## Metrics (fixed definitions)
- **M1 compaction fact retention.** Anchors = {commit hash 7-12 hex with digit+letter, ISO date, H-id, "Point N", slash-path with extension,
  decimal >=2 places or %, arXiv id, URL, verdict token (FALSIFIED/KILLED/CONFIRMED/REJECTED/WITHDRAWN/... uppercase list)}.
  retention = |anchors(old) ∩ anchors(new)| / |anchors(old)|. Inputs = real historical versions of activeContext.md (git, every 4th commit
  where a non-protected section exceeds VERBATIM_TAIL). Arms: PROD = real `pre_compact.py` code; ALT-A = anchor-preserving chunk summary, same
  20-line tail; ALT-B = ALT-A + byte-budget tail. Also: observed production events (summarized-count rises between consecutive commits).
- **M2 delivery.** Share of gold current-state facts whose TRUE value is inside the first 2000 bytes of the SessionStart hook output
  (persisted hook output files are the evidence). Before = actual output. After = simulation of "digest first" ordering (digest <=1500 B,
  generated from tools, not hand-written).
- **M3 state-claim accuracy.** Gold state-claims (frozen list below) classified CORRECT / STALE / CONFLICT / ABSENT against tool ground truth.
  accuracy = CORRECT / (CORRECT+STALE+CONFLICT) over claims that are present.
- **M4 referential integrity.** Dangling hash / path pointers in S1+S2 (hash resolved in Y-17 repo or ~/.claude repo; path resolved under
  repo, repo/.claude, ~/.claude). Split dangling into DELETED_IN_HISTORY vs NEVER_EXISTED. Also MEMORY.md index<->files, description equality.
- **M5 detector validity (positive/negative control).** Mutation test: inject seeded corruptions (hash flip, path rename, link removal,
  frontmatter deletion, future date, claim flip) into temp copies; recall per class; pristine-copy flag count.

## Gold state-claims (frozen now)
G1 pushed-status of 25776d4 · G2 MathOverflow question published? · G3 hooks fix committed? · G4 author email sent? (conflicting lines possible)
· G5 repo visibility · G6 U2 reply status · G7 U2 window end date · G8 lemma packet version · G9 canonical plan file exists+tracked
· G10 commits-behind of newest logged hash (numeric) · G11 coverage of entities from the 8 newest commits.

## Success thresholds (decided before implementing)
- T1: ALT retention >= 0.95 AND (ALT - PROD) >= +0.20 absolute AND ALT bytes <= 1.5 x PROD bytes AND second pass idempotent (no growth,
  no anchor loss) AND verdict-token retention >= 0.95.
- T2: delivery after >= 0.80 of gold facts the digest is designed to carry, with digest <= 1500 B and digest values == independent recomputation.
- T3: after remediation STALE+CONFLICT = 0 among gold claims; dangling-pointer count down >= 50% relative (only entries that are genuinely wrong,
  dated history left untouched).
- T4: mutation recall >= 0.90 on classes the detector claims to cover; undetectable classes listed explicitly (not hidden).

## Threats to validity (declared)
Same author wrote tests and fixes (circularity): mitigated by real historical inputs (M1), tool ground truth (M3), mutation control (M5), and a
frozen gold list. Anchors are a PROXY for facts (token present != meaning preserved) — verdict-token and association checks reduce, do not remove it.
Digest-delivery (M2 after) is a SIMULATION of a hook change that is NOT deployed here; global hook edits need the owner's go.
