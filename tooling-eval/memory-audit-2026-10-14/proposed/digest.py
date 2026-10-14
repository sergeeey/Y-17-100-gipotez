"""Generated session digest: STATE is derived from tools at read time, never hand-written.

Why (memory audit 2026-10-14): hand-written state claims in activeContext.md went stale within hours
(G1-G4) while the hook-derived auto-commit log stayed current (G10). Deriving the digest removes the
class of error instead of policing it. Budget: <= 1500 bytes so it fits the 2 KB window the harness
shows of a large SessionStart hook output.

Usage: python digest.py [--repo PATH]   (prints the digest)
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path

BUDGET = 1500


def _run(cmd: list[str], cwd: Path, timeout: int = 20) -> tuple[str, int]:
    try:
        r = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return r.stdout.strip(), r.returncode
    except Exception:
        return "", 1


def _git(repo: Path, *a: str) -> tuple[str, int]:
    return _run(["git", *a], repo)


def git_line(repo: Path) -> tuple[str, list[str]]:
    branch, _ = _git(repo, "branch", "--show-current")
    lr, rc = _git(repo, "rev-list", "--left-right", "--count", "@{u}...HEAD")
    behind, ahead = ("?", "?")
    if rc == 0 and lr.split():
        behind, ahead = lr.split()[:2]
    dirty, _ = _git(repo, "status", "--porcelain")
    n_dirty = len([x for x in dirty.splitlines() if x.strip()])
    un, rc2 = _git(repo, "log", "@{u}..HEAD", "--format=%h")
    unpushed = un.split() if rc2 == 0 else []
    shown = ", ".join(unpushed[:3]) + (f" +{len(unpushed) - 3}" if len(unpushed) > 3 else "")
    # review finding P1-1: a failed query (no upstream, git error) must never read as "nothing unpushed"
    state = (shown or "none") if rc2 == 0 else "unknown (no upstream or git error)"
    return (
        f"git: {branch} | ahead {ahead} behind {behind} | dirty {n_dirty} | unpushed: {state}",
        unpushed,
    )


def visibility(repo: Path) -> str:
    out, rc = _run(
        [
            "gh",
            "repo",
            "view",
            "--json",
            "nameWithOwner,visibility",
            "-q",
            '.nameWithOwner + " " + .visibility',
        ],
        repo,
    )
    return f"repo: {out}" if rc == 0 and out else "repo: visibility unknown (gh unavailable)"


def registry_line(repo: Path) -> str:
    p = repo / "registry" / "graph.yaml"
    if not p.exists():
        return "registry: graph.yaml missing"
    blocks = re.split(r"\n  - id: ", p.read_text(encoding="utf-8"))[1:]
    counts: dict[str, int] = {}
    n = 0
    for b in blocks:
        t = re.search(r"\n\s+type:\s*(\S+)", b)
        s = re.search(r"\n\s+status:\s*(\S+)", b)
        if t and t.group(1) == "hypothesis":
            n += 1
            st = s.group(1) if s else "?"
            counts[st] = counts.get(st, 0) + 1
    order = ["confirmed", "killed", "lead", "blocked", "parked"]
    parts = [f"{k} {counts[k]}" for k in order if k in counts] + [
        f"{k} {v}" for k, v in sorted(counts.items()) if k not in order
    ]
    return f"registry: {n} hypotheses = " + ", ".join(parts)


def u2_line(repo: Path, today: date) -> str:
    log = repo / "outreach" / "U2_WAIT_LOG.md"
    if not log.exists():
        return "U2: no wait log"
    txt = log.read_text(encoding="utf-8")
    m = re.search(r"Clock started: \*\*(\d{4}-\d{2}-\d{2})\*\*", txt)
    start = datetime.strptime(m.group(1), "%Y-%m-%d").date() if m else None
    rows = [r for r in txt.splitlines() if r.startswith("| 20")]
    classes = [r.strip().strip("|").split("|")[-1].strip() for r in rows]
    if not classes:  # review finding P2-3: all([]) is vacuously true, an empty log proves nothing
        reply = "unknown (log has no rows)"
    else:
        reply = (
            "none" if all(c in {"SENT", "no-answer so far"} for c in classes) else "YES (see log)"
        )
    sent = (
        "SENT-record exists"
        if (repo / "outreach" / "2026-09-23-authors-email-SENT.md").exists()
        else "no SENT-record"
    )
    if not start:
        return f"U2: email {sent}; reply on file: {reply}"
    end = start + timedelta(days=30)
    left = (end - today).days
    return f"U2: email {sent} {start}; reply on file: {reply}; window ends {end} ({left} d left)"


def mo_line(repo: Path) -> str:
    p = repo / "outreach" / "MO_QUESTION.md"
    if not p.exists():
        return "MO: no record"
    txt = p.read_text(encoding="utf-8")
    url = re.search(r"^url:\s*(\S+)", txt, re.M)
    posted = re.search(r"^posted:\s*(\S+)", txt, re.M)
    defect = re.search(r"^open_defect:\s*(.+)$", txt, re.M)
    if not url:
        return "MO: record has no url"
    code, _ = _run(
        [
            "curl",
            "-s",
            "-o",
            "NUL" if _is_windows() else "/dev/null",
            "-w",
            "%{http_code}",
            "-I",
            "-m",
            "8",
            url.group(1),
        ],
        repo,
    )
    live = code.strip() in {"200", "301", "302"}  # P2-3: "000"/404/403 must not read as published
    status = f"HTTP {code}" if live else f"URL unverified (HTTP {code or 'n/a'})"
    short = (
        url.group(1).split("/questions/")[0]
        + "/questions/"
        + url.group(1).split("/questions/")[1].split("/")[0]
    )
    d = (
        f"; open defect: {defect.group(1).strip()[:70]}"
        if defect and defect.group(1).strip().lower() != "none"
        else ""
    )
    word = "question live, posted" if live else "record says posted"
    return f"MO: {word} {posted.group(1) if posted else '?'} {short} ({status}){d}"


def _is_windows() -> bool:
    import os

    return os.name == "nt"


def packet_line(repo: Path) -> str:
    p = repo / "outreach" / "lemma_blind_packet.md"
    if not p.exists():
        return "packet: lemma_blind_packet.md missing"
    first = p.read_text(encoding="utf-8").splitlines()[0]
    m = re.search(r"\(v(\d+)\)", first)
    return f"packet: outreach/lemma_blind_packet.md v{m.group(1) if m else '?'}"


def recent_line(repo: Path, n: int = 5) -> list[str]:
    out, _ = _git(repo, "log", f"-{n}", "--format=%h %s")
    return [x[:58] for x in out.splitlines()]


def build_digest(repo: Path, now: datetime | None = None) -> str:
    now = now or datetime.now().astimezone()
    head, _ = _git(repo, "rev-parse", "--short", "HEAD")
    gl, _ = git_line(repo)
    lines = [
        f"## DIGEST (generated from tools {now.isoformat(timespec='minutes')}; HEAD {head}; hand-edits are overwritten)",
        gl,
        visibility(repo),
        registry_line(repo),
        u2_line(repo, now.date()),
        mo_line(repo),
        packet_line(repo),
    ]
    recents = recent_line(repo)
    text = "\n".join(lines)
    for i in range(len(recents), 0, -1):
        cand = text + "\nrecent: " + " | ".join(recents[:i])
        if len(cand.encode("utf-8")) <= BUDGET:
            return cand + "\n"
    return text.encode("utf-8")[: BUDGET - 1].decode("utf-8", errors="ignore") + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]))
    a = ap.parse_args()
    d = build_digest(Path(a.repo))
    print(d, end="")
    print(f"[{len(d.encode('utf-8'))} bytes]")
