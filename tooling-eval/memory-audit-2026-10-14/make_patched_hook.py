"""Build proposed/pre_compact_patched.py (a minimal, self-contained patch of the PRODUCTION hook) and its unified diff.

Nothing under ~/.claude is modified: the patched copy lives next to this script and is evaluated by
audit_patched_hook.py on the same real history as the original. Deploying it is the owner's decision.

Edits (each asserted, so the patch fails loudly if the production file changed):
 E1 _section_is_newest_first: malformed date -> False instead of ValueError (hook crash, reproduced).
 E2 _split_into_chunks: a top-level bullet starts a new entry; '[summarized]' lines stay separate (idempotent).
 E3 _summarize_chunk: keep the first <=117 chars AND every anchor (hash/date/id/path/number/verdict) of the entry.
 E4 _create_progressive_summary: no trailing-blank accretion on unchanged/protected sections (non-idempotent rewrites).
 E5 _trim_old_entries: archive removed sections to history/trimmed-<date>.md instead of silent deletion; safe date parse;
    an archive I/O failure skips the trim instead of crashing.
 E7 _cap_summaries: bound the active summary lines per section (12 KB), moving older ones verbatim to history/.
 E6 main(): run the trim BEFORE the progressive summary so the archive holds the original (not summarised) text.
"""

from __future__ import annotations

import difflib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path.home() / ".claude" / "hooks" / "pre_compact.py"
OUT_DIR = HERE / "proposed"


def replace_func(text: str, name: str, new_src: str) -> str:
    m = re.search(rf"^def {name}\(.*?(?=^def |^# WHY|^class |\Z)", text, re.S | re.M)
    assert m, f"function {name} not found"
    return text[: m.start()] + new_src.rstrip("\n") + "\n\n\n" + text[m.end() :]


def main() -> None:
    t = SRC.read_text(encoding="utf-8")

    # ---- E1
    old = """    first = datetime.strptime(dates[0], "%Y-%m-%d")
    last = datetime.strptime(dates[-1], "%Y-%m-%d")
    return first > last"""
    new = """    try:
        first = datetime.strptime(dates[0], "%Y-%m-%d")
        last = datetime.strptime(dates[-1], "%Y-%m-%d")
    except ValueError:  # malformed date (typo): unknown order, must never crash the hook
        return False
    return first > last"""
    assert t.count(old) == 1
    t = t.replace(old, new)

    # ---- E2
    t = replace_func(
        t,
        "_split_into_chunks",
        '''def _split_into_chunks(lines: list[str]) -> list[list[str]]:
    """Split `lines` into entries: blank-line separated, one per top-level bullet, '[summarized]' lines alone.

    WHY (memory audit 2026-10-14): blank-line chunking folded N consecutive bullets (this file format has no
    blank lines between entries) into ONE summary line; and a block of '[summarized]' lines was re-collapsed
    to its first line on the next pass.
    """
    chunks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if line.strip().startswith("[summarized]"):
            if current:
                chunks.append(current)
                current = []
            chunks.append([line])
        elif re.match(r"[-*] ", line):
            if current:
                chunks.append(current)
            current = [line]
        elif line.strip():
            current.append(line)
        elif current:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks''',
    )

    # ---- E3
    t = replace_func(
        t,
        "_summarize_chunk",
        '''_ANCHOR_RES = (
    ("verdict", re.compile(r"\\b(FALSIFIED|KILLED|CONFIRMED|REJECTED|WITHDRAWN|RETRACTED|PARKED|SUPERSEDED|"
                           r"PARTIALLY_SUPPORTED|PROMOTE|VALIDATED|INCONCLUSIVE|NEEDS_WORK|BLOCKED|CORRECTED)\\b")),
    ("id", re.compile(r"\\bH-[A-Z0-9]+(?:-[A-Za-z0-9]+)*\\b")),
    ("hash", re.compile(r"\\b(?=[0-9a-f]*\\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,12}\\b")),
    ("date", re.compile(r"\\b20\\d\\d-\\d\\d-\\d\\d(?!\\d)")),
    ("path", re.compile(r"(?<![\\w/.-])[\\w.-]+(?:/[\\w.-]+)+\\.[A-Za-z]\\w{0,4}\\b")),
    ("point", re.compile(r"\\bPoints? \\d+\\b")),
    ("num", re.compile(r"(?<![\\w.])-?\\d+\\.\\d{2,}(?![\\w.])|\\b\\d+(?:\\.\\d+)?%")),
    ("arxiv", re.compile(r"\\b\\d{4}\\.\\d{4,5}\\b")),
)
_URL_RE = re.compile(r"https?://[^\\s)`\\]>]+")
_ANCHOR_CAP = 520


def _summarize_chunk(chunk: list[str]) -> str:
    """One "[summarized] ..." line per entry: the first <=117 chars plus every anchor not already shown.

    WHY (memory audit 2026-10-14): head-only summaries dropped 11.6% of all hashes/dates/ids/numbers/verdicts per
    compaction when replayed on this project's real history, and in 5 real compaction events 6 of 118 verdict
    tokens (FALSIFIED/KILLED/...) vanished, leaving the claim without its refutation. An already-summarized line
    is kept as is: re-truncating it at 160 chars erased anchors on a later pass.
    """
    line = _first_content_line(chunk)
    if line is None:
        return "[summarized] (empty entry)"
    if line.startswith("[summarized]"):
        return line
    head = _truncate_at_word_boundary(line)
    body = " ".join(s.strip() for s in chunk)
    seen: set[str] = set()
    extra: list[str] = []
    for u in _URL_RE.findall(body):
        u = u.rstrip(".,;")
        if u not in seen and u not in head:
            seen.add(u)
            extra.append(u)
    body = _URL_RE.sub(" ", body)
    for _, rx in _ANCHOR_RES:
        for m in rx.finditer(body):
            val = m.group(0)
            if val not in seen and val not in head:
                seen.add(val)
                extra.append(val)
    budget = _ANCHOR_CAP - len(head) - 28
    kept: list[str] = []
    used = 0
    for val in extra:
        if used + len(val) + 2 <= budget:
            kept.append(val)
            used += len(val) + 2
    dropped = len(extra) - len(kept)
    tail = ""
    if kept or dropped:
        tail = " {anchors: " + "; ".join(kept) + (f"; +{dropped} more" if dropped else "") + "}"
    return f"[summarized] {head}{tail}"''',
    )

    # ---- E4 (two unchanged-section emissions)
    old_a = """            block = "\\n".join([section.heading] + section.lines)
            compressed_sections.append(block)
            continue

        body = section.lines"""
    new_a = """            block = "\\n".join([section.heading] + _rstrip_blank(section.lines))
            compressed_sections.append(block)
            continue

        body = section.lines"""
    assert t.count(old_a) == 1, "E4a"
    t = t.replace(old_a, new_a)
    old_b = """            # Short enough — no compression needed
            block = "\\n".join([section.heading] + section.lines)"""
    new_b = """            # Short enough — no compression needed
            block = "\\n".join([section.heading] + _rstrip_blank(section.lines))"""
    assert t.count(old_b) == 1, "E4b"
    t = t.replace(old_b, new_b)
    helper = '''def _rstrip_blank(lines: list[str]) -> list[str]:
    """Drop trailing blank lines: every rewrite re-joins sections with a blank line, so keeping the original
    trailing blanks added two blank lines per section per pass (17 consecutive newlines seen in the real file)."""
    out = list(lines)
    while out and not out[-1].strip():
        out.pop()
    return out


'''
    marker = "def _create_progressive_summary("
    assert t.count(marker) == 1
    t = t.replace(marker, helper + marker)

    # ---- E6 (review P2-2): run the 90-day trim before the summary so the archive holds the original text
    old_main_trim = (
        "        trimmed = _trim_old_entries(active)\n"
        "        if trimmed:\n"
        '            print(f"[PreCompact] Trimmed {trimmed} stale section(s) from {active.name}")\n'
    )
    assert t.count(old_main_trim) == 1, "E6a"
    t = t.replace(old_main_trim, "")
    old_main_comp = "        compressed = _create_progressive_summary(active)\n"
    assert t.count(old_main_comp) == 1, "E6b"
    t = t.replace(
        old_main_comp,
        "        trimmed = _trim_old_entries(active)  # archive-then-trim first (verbatim archive)\n"
        "        if trimmed:\n"
        '            print(f"[PreCompact] Trimmed {trimmed} stale section(s) from {active.name}")\n'
        + old_main_comp,
    )

    # ---- E7 (review P2-5): anchored summaries must not make the active file grow without bound
    old_nf = "            summary_lines = _summarize_chunks(to_compress)\n"
    old_of = "            summary_lines = _summarize_chunks(head)\n"
    assert t.count(old_nf) == 1 and t.count(old_of) == 1, "E7a"
    t = t.replace(
        old_nf,
        old_nf
        + "            summary_lines = _cap_summaries(summary_lines, active_path, oldest_at_end=True)\n",
    )
    t = t.replace(
        old_of,
        old_of
        + "            summary_lines = _cap_summaries(summary_lines, active_path, oldest_at_end=False)\n",
    )
    cap_helper = '''_SUMMARY_CAP = 12000  # bytes of summary lines kept active per section; the rest moves, verbatim, to history/


def _cap_summaries(lines: list[str], active_path: Path, oldest_at_end: bool) -> list[str]:
    """Keep the newest summary lines up to _SUMMARY_CAP bytes; move older ones VERBATIM to history/compacted-<date>.md.

    WHY (memory audit 2026-10-14): anchored summaries keep up to ~520 B per entry; without a bound the active file
    grew ~2x faster than the original in a synthetic long run. Moving (not dropping) keeps every anchor retrievable.
    An I/O failure keeps everything in place (never lose, never crash).
    """
    sizes = [len(x.encode("utf-8")) + 1 for x in lines]
    if sum(sizes) <= _SUMMARY_CAP:
        return lines
    newest_first = list(range(len(lines))) if oldest_at_end else list(range(len(lines) - 1, -1, -1))
    kept_idx: list[int] = []
    used = 0
    for i in newest_first:
        if kept_idx and used + sizes[i] > _SUMMARY_CAP - 160:  # reserve room for the pointer line (idempotency)
            break
        kept_idx.append(i)
        used += sizes[i]
    moved_idx = sorted(set(range(len(lines))) - set(kept_idx))
    if not moved_idx:
        return lines
    try:
        arch = active_path.parent / "history"
        arch.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(UTC).strftime("%Y-%m-%d")
        with open(arch / f"compacted-{stamp}.md", "a", encoding="utf-8") as fh:
            fh.write("\\n".join(lines[i] for i in moved_idx) + "\\n\\n")
    except OSError:
        return lines
    kept = [lines[i] for i in sorted(kept_idx)]
    pointer = f"[summarized] [{len(moved_idx)} older summary lines moved verbatim to history/compacted-{stamp}.md]"
    return kept + [pointer] if oldest_at_end else [pointer] + kept


'''
    marker2 = "def _create_progressive_summary("
    assert t.count(marker2) == 1
    t = t.replace(marker2, cap_helper + marker2)

    # ---- E5
    old_c = '        newest_date = max(datetime.strptime(d, "%Y-%m-%d") for d in date_strings)\n\n        if newest_date < cutoff:\n            removed += 1\n        else:\n            kept_sections.append(section)'
    new_c = """        try:
            newest_date = max(datetime.strptime(d, "%Y-%m-%d") for d in date_strings)
        except ValueError:  # a malformed date must not crash the hook or delete the section
            kept_sections.append(section)
            continue

        if newest_date < cutoff:
            removed += 1
            removed_sections.append(section)
        else:
            kept_sections.append(section)"""
    assert t.count(old_c) == 1, "E5a"
    t = t.replace(old_c, new_c)
    t = t.replace(
        "    kept_sections: list[_Section] = []\n    removed = 0\n",
        "    kept_sections: list[_Section] = []\n    removed_sections: list[_Section] = []\n    removed = 0\n",
        1,
    )
    old_d = "    # ── Rebuild file ──\n    compressed_sections = "
    new_d = """    # WHY (memory audit 2026-10-14): the 90-day rule deleted whole sections (Scope Fence, Project State, Open
    # Questions on this project) with no copy anywhere. Archive them verbatim first.
    try:
        archive_dir = context_path.parent / "history"
        archive_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(UTC).strftime("%Y-%m-%d")
        with open(archive_dir / f"trimmed-{stamp}.md", "a", encoding="utf-8") as fh:
            for s in removed_sections:
                fh.write("\\n".join([s.heading] + s.lines).rstrip("\\n") + "\\n\\n")
    except OSError:  # cannot archive -> do not delete anything, do not crash the hook (review P2-1)
        return 0

    # ── Rebuild file ──
    compressed_sections = """
    assert t.count(old_d) == 1, "E5b"
    t = t.replace(old_d, new_d)

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "pre_compact_patched.py").write_text(t, encoding="utf-8", newline="\n")
    diff = difflib.unified_diff(
        SRC.read_text(encoding="utf-8").splitlines(keepends=True),
        t.splitlines(keepends=True),
        fromfile="hooks/pre_compact.py (production)",
        tofile="hooks/pre_compact.py (proposed)",
    )
    (OUT_DIR / "pre_compact.diff").write_text("".join(diff), encoding="utf-8", newline="\n")
    n = sum(1 for _ in (OUT_DIR / "pre_compact.diff").read_text(encoding="utf-8").splitlines())
    print("wrote proposed/pre_compact_patched.py and proposed/pre_compact.diff (%d diff lines)" % n)


if __name__ == "__main__":
    main()
