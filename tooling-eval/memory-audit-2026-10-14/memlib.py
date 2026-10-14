"""Shared helpers for the 2026-10-14 memory audit: anchors, retention, anchor-preserving compactor.

Anchors are a PROXY for facts (token present != meaning preserved); see PREREG.md threats to validity.
The compactor mirrors the structure of ~/.claude/hooks/pre_compact.py::_create_progressive_summary
(sections, protected headings, newest-first detection) and changes ONLY what the audit found lossy:
the one-line-per-block summary, the line-count verbatim tail, and non-idempotent repeated passes.
"""

from __future__ import annotations

import re
from datetime import datetime

# ---------------------------------------------------------------- anchors
HASH_RE = re.compile(r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,12}\b")
DATE_RE = re.compile(r"\b20\d\d-\d\d-\d\d(?!\d)")
HID_RE = re.compile(r"\bH-[A-Z0-9]+(?:-[A-Za-z0-9]+)*\b")
POINT_RE = re.compile(r"\bPoints? \d+\b")
PATH_RE = re.compile(r"(?<![\w/.-])[\w.-]+(?:/[\w.-]+)+\.[A-Za-z]\w{0,4}\b")
NUM_RE = re.compile(r"(?<![\w.])-?\d+\.\d{2,}(?![\w.])|\b\d+(?:\.\d+)?%")
ARXIV_RE = re.compile(r"\b\d{4}\.\d{4,5}\b")
URL_RE = re.compile(r"https?://[^\s)`\]>]+")
VERDICT_RE = re.compile(
    r"\b(FALSIFIED|KILLED|CONFIRMED|REJECTED|WITHDRAWN|RETRACTED|PARKED|SUPERSEDED|"
    r"PARTIALLY_SUPPORTED|PROMOTE|VALIDATED|INCONCLUSIVE|NEEDS_WORK|BLOCKED|OVERCLAIM\w*|CORRECTED)\b"
)

# priority when an anchored summary must drop something (earlier = kept first)
TYPE_ORDER = ["verdict", "hid", "hash", "date", "path", "point", "num", "arxiv", "url"]


def _typed_matches(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for u in URL_RE.findall(text):
        out.append(("url", u.rstrip(".,;")))
    t = URL_RE.sub(" ", text)
    for typ, rx in (
        ("verdict", VERDICT_RE),
        ("hid", HID_RE),
        ("hash", HASH_RE),
        ("date", DATE_RE),
        ("path", PATH_RE),
        ("point", POINT_RE),
        ("num", NUM_RE),
        ("arxiv", ARXIV_RE),
    ):
        for m in rx.findall(t):
            out.append((typ, m))
    return out


_COMMIT_CTX_RE = re.compile(r"commit|branch|pushed|squash|rebase|merge|cherry|revert|HEAD|\(local", re.I)
_NOT_COMMIT_CTX_RE = re.compile(r"sha-?256|sha-?1\b|md5|checksum|uuid|session|agentid|agent id", re.I)


def commit_refs(text: str) -> set[str]:
    """Hex tokens that are plausibly COMMIT references (context keyword nearby; not sha256/UUID/ellipsised)."""
    out: set[str] = set()
    for m in HASH_RE.finditer(text):
        s, e = m.start(), m.end()
        after = text[e : e + 40]
        near = text[max(0, s - 60) : e + 40]
        if _NOT_COMMIT_CTX_RE.search(text[max(0, s - 24) : s]):
            continue
        if after.startswith(("...", "\u2026")) or text[max(0, s - 1) : s] == "-" or re.match(r"-[0-9a-f]", after):
            continue
        if _COMMIT_CTX_RE.search(near):
            out.add(m.group(0))
    return out


def extract_anchors(text: str) -> set[str]:
    return {f"{t}:{v}" for t, v in _typed_matches(text)}


def retention(old: str, new: str) -> dict:
    a, b = extract_anchors(old), extract_anchors(new)
    kept = a & b
    by_type: dict[str, list[int]] = {}
    for x in a:
        typ = x.split(":", 1)[0]
        by_type.setdefault(typ, [0, 0])
        by_type[typ][1] += 1
        if x in b:
            by_type[typ][0] += 1
    return {
        "n_old": len(a),
        "n_kept": len(kept),
        "retention": (len(kept) / len(a)) if a else 1.0,
        "lost": sorted(a - b),
        "by_type": by_type,
    }


# ---------------------------------------------------------------- compactor
NEVER_SUMMARIZE_PREFIXES = ("## Error", "## Decision", "## Correction", "## Bug")


def parse_sections(content: str) -> tuple[list[str], list[tuple[str, list[str]]]]:
    preamble: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    heading: str | None = None
    cur: list[str] = []
    for line in content.splitlines():
        if line.startswith("## "):
            if heading is not None:
                sections.append((heading, cur))
            else:
                preamble = cur[:]
            heading, cur = line, []
        else:
            cur.append(line)
    if heading is not None:
        sections.append((heading, cur))
    else:
        preamble = cur
    return preamble, sections


def _is_summary_line(ln: str) -> bool:
    return ln.strip().startswith("[summarized]")


def split_chunks(lines: list[str]) -> list[list[str]]:
    """Blank-line-separated chunks; every '[summarized]' line is its own chunk.

    WHY (found by this audit's idempotency test): production keeps a block of consecutive
    '[summarized]' lines as ONE chunk, so a later pass reduces the whole block to its first line.
    """
    chunks: list[list[str]] = []
    cur: list[str] = []
    for ln in lines:
        if _is_summary_line(ln):
            if cur:
                chunks.append(cur)
                cur = []
            chunks.append([ln])
        elif ln.strip():
            cur.append(ln)
        elif cur:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def _is_summary_chunk(c: list[str]) -> bool:
    return len(c) == 1 and _is_summary_line(c[0])


def newest_first(lines: list[str]) -> bool:
    dates = DATE_RE.findall("\n".join(lines))
    if len(dates) < 2:
        return False
    try:
        return datetime.strptime(dates[0], "%Y-%m-%d") > datetime.strptime(dates[-1], "%Y-%m-%d")
    except ValueError:  # malformed date (typo): unknown order, never crash the hook
        return False


def _first_content_line(chunk: list[str]) -> str | None:
    for ln in chunk:
        s = ln.strip()
        if s and not re.match(r"^[-*#>|]+\s*$", s):
            return s
    return None


def truncate_word(text: str, limit: int = 117) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit]
    sp = cut.rfind(" ")
    if sp > 0:
        cut = cut[:sp]
    return cut + "..."


def summarize_chunk_anchored(chunk: list[str], head_limit: int = 117, cap: int = 520) -> str:
    """One line per chunk: first <=117 chars (as production) + every anchor the head does not show.

    Already-summarized lines are returned unchanged (idempotent; production re-truncates them to
    160 chars, erasing anchors on a later pass).
    """
    line = _first_content_line(chunk)
    if line is None:
        return "[summarized] (empty entry)"
    if line.startswith("[summarized]"):
        return line
    head = truncate_word(line, head_limit)
    body = " ".join(s.strip() for s in chunk)
    seen: set[str] = set()
    items: list[tuple[int, str]] = []
    for typ, val in _typed_matches(body):
        key = f"{typ}:{val}"
        if key in seen or val in head:
            continue
        seen.add(key)
        items.append((TYPE_ORDER.index(typ), val))
    items.sort(key=lambda x: x[0])
    budget = cap - len(head) - len("[summarized]  {anchors: }")
    used, kept, dropped = 0, [], 0
    for _, val in items:
        if used + len(val) + 2 <= budget:
            kept.append(val)
            used += len(val) + 2
        else:
            dropped += 1
    tail = ""
    if kept or dropped:
        tail = " {anchors: " + "; ".join(kept) + (f"; +{dropped} more" if dropped else "") + "}"
    return f"[summarized] {head}{tail}"


def _plain(chunk: list[str]) -> str:
    line = _first_content_line(chunk)
    if line is None:
        return "[summarized] (empty entry)"
    if line.startswith("[summarized]"):
        return truncate_word(line, 160)
    return f"[summarized] {truncate_word(line)}"


def _nbytes(lines: list[str]) -> int:
    return sum(len(ln.encode("utf-8")) + 1 for ln in lines if not _is_summary_line(ln))


def compact_text(
    text: str,
    *,
    verbatim_lines: int = 20,
    verbatim_bytes: int | None = None,
    anchored: bool = True,
    cap: int = 520,
) -> str:
    """Anchor-preserving, idempotent counterpart of production _create_progressive_summary."""
    preamble, sections = parse_sections(text)
    if not sections:
        return text
    summarize = (lambda c: summarize_chunk_anchored(c, cap=cap)) if anchored else _plain
    blocks: list[str] = []
    for heading, lines in sections:
        body = list(lines)
        while body and not body[-1].strip():
            body.pop()
        if any(heading.startswith(p) for p in NEVER_SUMMARIZE_PREFIXES):
            blocks.append("\n".join([heading] + body))
            continue
        newest = newest_first(body)
        if verbatim_bytes is None:
            if len(body) <= verbatim_lines:
                blocks.append("\n".join([heading] + body))
                continue
            if newest:
                verb, comp = body[:verbatim_lines], body[verbatim_lines:]
            else:
                verb, comp = body[len(body) - verbatim_lines :], body[: len(body) - verbatim_lines]
            summ = [summarize(c) for c in split_chunks(comp)] or ["[summarized] (empty section)"]
            parts = verb + [""] + summ if newest else summ + [""] + verb
            blocks.append("\n".join([heading] + parts))
            continue
        if _nbytes(body) <= verbatim_bytes:
            blocks.append("\n".join([heading] + body))
            continue
        chunks = split_chunks(body)
        order = chunks if newest else list(reversed(chunks))
        used, n_keep = 0, 0
        for c in order:
            size = 0 if _is_summary_chunk(c) else _nbytes(c) + 1
            if n_keep and used + size > verbatim_bytes:
                break
            used += size
            n_keep += 1
        keep, rest = order[:n_keep], order[n_keep:]
        if not newest:
            keep, rest = list(reversed(keep)), list(reversed(rest))
        summ = [summarize(c) for c in rest]
        vtxt: list[str] = []
        for c in keep:
            vtxt += c + [""]
        vtxt = vtxt[:-1] if vtxt else vtxt
        if summ and vtxt:
            parts = vtxt + [""] + summ if newest else summ + [""] + vtxt
        else:
            parts = vtxt or summ
        blocks.append("\n".join([heading] + parts))
    return "\n".join(preamble) + "\n" + "\n\n".join(blocks) + "\n"
