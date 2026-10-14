"""Remediation of the project memory found wrong/misplaced by the audit (reversible via git; every step asserted).

1. G1/G2: replace the two hand-written state claims that are false today (push status, MO publication).
2. G4: neutralise the superseded 'Email NOT SENT' line; demote stale READ-THIS-FIRST markers.
3. Layout: archive 11 verbose 2026-09-14/15 H-CAT31-3 bullets VERBATIM, put '## Current Focus' first.
4. Add one reconciliation bullet that points to the generated digest instead of re-stating counts.
5. Auto-memory: fix the index line that contradicts its own file (G3); add a freshness note to the YBE state note.

Run: python remediate.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import memlib as ml  # noqa: E402

REPO = HERE.parents[1]
ACTIVE = REPO / ".claude" / "memory" / "activeContext.md"
ARCHIVE = REPO / ".claude" / "memory" / "history" / "activeContext-archive-2026-10-14.md"
AUTO = next((Path.home() / ".claude" / "projects").glob("E-*Y-17-100-gipotez")) / "memory"


def sub_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    before = ACTIVE.read_text(encoding="utf-8")
    t = before

    # ---- G1 + G2 (one sentence chain)
    m = re.search(
        r"Committed `25776d4`, not pushed\. Next: MathOverflow post drafted.*?outreach itself\" rule\.",
        t,
        re.S,
    )
    assert m, "G1/G2 sentence chain not found"
    new_chain = (
        "Committed `25776d4`, pushed (and `de046fb`; verified 2026-10-14 with `git branch -r --contains 25776d4` "
        "-> origin/feature/small-exact-instance). MathOverflow question PUBLISHED by the owner 2026-09-27 "
        "(https://mathoverflow.net/questions/515586; 0 answers, 56 views on 2026-10-14). Record and one OPEN defect "
        "(underscores lost in `Q_{ij}` and `\\sum_{a=1}^{2}` in the live source) are in `outreach/MO_QUESTION.md`."
    )
    t = t.replace(m.group(0), new_chain)

    # ---- G4 + marker demotion
    t = sub_once(
        t,
        "Email NOT SENT.",
        "Email NOT SENT. [SUPERSEDED 2026-09-23: email SENT, see the 2026-09-23 entry below]",
        "G4",
    )
    t = sub_once(
        t,
        "[2026-09-22 evening CHECKPOINT — H-CAT56-2 READ THIS FIRST.]",
        "[2026-09-22 evening CHECKPOINT — H-CAT56-2; demoted 2026-10-14: superseded by the 2026-09-27 CURRENT PLAN.]",
        "marker-checkpoint",
    )
    t = sub_once(
        t,
        "STOP-RULE АКТИВЕН — читать первым.**",
        "STOP-RULE АКТИВЕН [demoted 2026-10-14: порядок чтения теперь задаёт CURRENT PLAN 2026-09-27].**",
        "marker-adr121",
    )

    # ---- layout: archive verbose bullets verbatim, Current Focus first
    pre, secs = ml.parse_sections(t)
    names = [h for h, _ in secs]
    i_sf = next(i for i, h in enumerate(names) if h.startswith("## Scope Fence"))
    sf_head, sf_lines = secs[i_sf]
    pat = re.compile(
        r"^- \*\*\[(?:DERIVED \+ )?VERIFIED-(?:COMPUTATION|ANALYSIS)(?:/DERIVATION)? — 2026-09-1[45], H-CAT31-3"
    )
    moved = [ln for ln in sf_lines if pat.match(ln)]
    assert len(moved) == 11, f"expected 11 archive candidates, found {len(moved)}"
    pointer = (
        "- **[archived 2026-10-14]** 11 verbose H-CAT31-3 entries (Points 57-64, 2026-09-14/15; status of that node unchanged) "
        "moved VERBATIM to `.claude/memory/history/activeContext-archive-2026-10-14.md`; full record also in "
        "`experiments/20260910-lovasz-theta-variance-scaling-cat31-3/decision.md`."
    )
    # keep the original order of the remaining lines; the pointer replaces the first moved line's position
    first_idx = next(i for i, ln in enumerate(sf_lines) if pat.match(ln))
    new_sf = []
    for i, ln in enumerate(sf_lines):
        if i == first_idx:
            new_sf.append(pointer)
        if not pat.match(ln):
            new_sf.append(ln)
    secs[i_sf] = (sf_head, new_sf)
    i_cf = next(i for i, h in enumerate(names) if h.startswith("## Current Focus"))
    cf = secs.pop(i_cf)
    secs.insert(0, cf)

    # ---- reconciliation bullet at the top of Current Focus
    recon = (
        "- **[2026-10-14 RECONCILIATION — generated state beats written state.]** Push/publish/commit status and registry counts "
        "are no longer kept here as hand-written claims: 3 of them were false within 17 days (push status of `25776d4`, MathOverflow "
        "publication, the hooks-fix commit) and one superseded not-sent line survived next to the newer sent line. Current state = "
        "`python tooling-eval/memory-audit-2026-10-14/digest.py` (derived from git/gh/files). Work since 2026-09-27 (git log): "
        "`edc14e7` round 1 of the sequential autonomous run on five audited open problems (#30, #11, #1, #5, #17); `84950a6` round 2 "
        "on #30, #1, #11 (no LEAD); `1453996` protocol H-YBE-C3-TWIN-001. Evidence: `tooling-eval/memory-audit-2026-10-14/REPORT.md`."
    )
    cf_head, cf_lines = secs[0]
    secs[0] = (
        cf_head,
        ["", recon] + [x for x in cf_lines if not (x == "" and cf_lines.index(x) == 0)],
    )

    blocks = []
    for h, lines in secs:
        body = list(lines)
        while body and not body[-1].strip():
            body.pop()
        blocks.append("\n".join([h] + body))
    after = "\n".join(pre) + "\n" + "\n\n".join(blocks) + "\n"

    # ---- anchor audit: nothing may vanish except inside the intentionally replaced sentences
    arch_text = (
        "# activeContext archive — 2026-10-14 (moved verbatim from `## Scope Fence`; node status unchanged)\n\n"
        + "\n".join(moved)
        + "\n"
    )
    lost = ml.extract_anchors(before) - ml.extract_anchors(after) - ml.extract_anchors(arch_text)
    print("anchors lost (must be only from replaced sentences):", sorted(lost))
    print(
        f"bytes before {len(before.encode())} -> after {len(after.encode())} (+ archive {len(arch_text.encode())})"
    )
    if a.dry_run:
        return
    ACTIVE.write_text(after, encoding="utf-8", newline="\n")
    ARCHIVE.write_text(arch_text, encoding="utf-8", newline="\n")

    # ---- auto-memory: index line contradicted its own file
    idx = AUTO / "MEMORY.md"
    it = idx.read_text(encoding="utf-8")
    old_line = 'global hook fix for infinite "chore: auto-log commit history entry" commit chain, left UNCOMMITTED in hooks repo pending user go-ahead'
    new_line = (
        'global hook fix for infinite "chore: auto-log commit history entry" commit chain; committed in the ~/.claude hooks repo '
        "as 2dca838 (2026-09-08); if the chain recurs, first `grep _is_self_log_commit` in the hook (the fix was once lost from the working copy)"
    )
    idx.write_text(sub_once(it, old_line, new_line, "index-G3"), encoding="utf-8", newline="\n")

    ybe = AUTO / "ybe-c3-audit-orchestration-state.md"
    yt = ybe.read_text(encoding="utf-8").rstrip("\n")
    if "Freshness check 2026-10-14" not in yt:
        yt += (
            "\n\n**Freshness check 2026-10-14:** this note was last written 2026-10-05. Since then `git log --grep=YBE` shows "
            "`1453996` (protocol H-YBE-C3-TWIN-001: twin exclusion at R0, constant QYBE C^3, P12 pilot) and rounds `edc14e7`, `84950a6` on "
            "neighbouring open problems; treat the state above as possibly superseded and re-verify against git before relying on it.\n"
        )
        ybe.write_text(yt, encoding="utf-8", newline="\n")
    print("written: activeContext.md, archive, MEMORY.md index line, ybe freshness note")


if __name__ == "__main__":
    main()
