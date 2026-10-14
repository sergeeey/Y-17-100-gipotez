"""M3 state-claim accuracy, M4 referential integrity, M5 mutation validity of the detector.

Run:  python audit_state.py --label before|after [--out results_state_<label>.json]
Ground truth comes from tools (git, gh, curl, files) at measurement time, never from memory text.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import memlib as ml  # noqa: E402

REPO = HERE.parents[1]
HOME = Path.home()
CLAUDE = HOME / ".claude"
ACTIVE = REPO / ".claude" / "memory" / "activeContext.md"
AUTO_DIR = next((CLAUDE / "projects").glob("E-*Y-17-100-gipotez")) / "memory"
MO_URL = "https://mathoverflow.net/questions/515586"  # owner-posted 2026-09-27, see outreach/MO_QUESTION.md
TODAY = date.today()


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 30) -> tuple[str, int]:
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
    except Exception as e:  # noqa: BLE001
        return f"ERR {e}", 1


def git(*a: str, cwd: Path = REPO) -> tuple[str, int]:
    return run(["git", *a], cwd=cwd)


# ------------------------------------------------------------------ stores
def load_stores() -> dict[str, str]:
    s = {"activeContext.md": ACTIVE.read_text(encoding="utf-8")}
    if AUTO_DIR.exists():
        for p in sorted(AUTO_DIR.glob("*.md")):
            s[f"auto/{p.name}"] = p.read_text(encoding="utf-8")
    return s


# ------------------------------------------------------------------ ground truth
def truth_repo_visibility() -> str:
    out, rc = run(
        [
            "gh",
            "repo",
            "view",
            "sergeeey/Y-17-100-gipotez",
            "--json",
            "visibility",
            "-q",
            ".visibility",
        ]
    )
    return out if rc == 0 else "unknown"


def truth_pushed(h: str) -> str:
    out, rc = git("branch", "-r", "--contains", h)
    return "pushed" if rc == 0 and out.strip() else "not pushed"


def truth_mo_published() -> str:
    out, rc = run(["curl", "-s", "-o", os.devnull, "-w", "%{http_code}", "-I", "-m", "8", MO_URL])
    if out.strip() in {"200", "301", "302"}:
        return "published"
    return "unknown" if rc else "not published"


def truth_hooks_fix_committed() -> str:
    out, _ = git(
        "log",
        "--oneline",
        "--grep=guard post_commit_memory against its own auto-log commit loop",
        cwd=CLAUDE,
    )
    return "committed" if out.strip() else "uncommitted"


def u2_clock_start() -> date | None:
    p = REPO / "outreach" / "U2_WAIT_LOG.md"
    if not p.exists():
        return None
    m = re.search(r"Clock started: \*\*(\d{4}-\d{2}-\d{2})\*\*", p.read_text(encoding="utf-8"))
    return datetime.strptime(m.group(1), "%Y-%m-%d").date() if m else None


def truth_email_sent() -> str:
    return (
        "SENT" if (REPO / "outreach" / "2026-09-23-authors-email-SENT.md").exists() else "NOT SENT"
    )


def truth_u2_reply() -> str:
    p = REPO / "outreach" / "U2_WAIT_LOG.md"
    txt = p.read_text(encoding="utf-8") if p.exists() else ""
    rows = [r for r in txt.splitlines() if r.startswith("| 20")]
    classes = [r.strip().strip("|").split("|")[-1].strip() for r in rows]
    return "no reply" if all(c in {"SENT", "no-answer so far"} for c in classes) else "reply"


def truth_u2_window_end() -> str:
    d = u2_clock_start()
    return str(d + timedelta(days=30)) if d else "unknown"


def truth_packet_version() -> str:
    p = REPO / "outreach" / "lemma_blind_packet.md"
    first_line = p.read_text(encoding="utf-8").splitlines()[0] if p.exists() else ""
    m = re.search(r"\(v(\d+)\)", first_line)
    return f"v{m.group(1)}" if m else "unknown"


def truth_plan_file(rel: str) -> str:
    p = REPO / rel
    if not p.exists():
        return "missing"
    _, rc = git("ls-files", "--error-unmatch", rel)
    return "tracked" if rc == 0 else "untracked"


# ------------------------------------------------------------------ gold state-claims
def first(rx: str, text: str, grp: int = 1) -> str | None:
    m = re.search(rx, text)
    return m.group(grp) if m else None


def every(rx: str, text: str, grp: int = 1) -> list[str]:
    return [m.group(grp) for m in re.finditer(rx, text)]


def gold_claims(stores: dict[str, str]) -> list[dict]:
    act = stores["activeContext.md"]
    auto = "\n".join(v for k, v in stores.items() if k.startswith("auto/"))
    allm = act + "\n" + auto
    rows: list[dict] = []

    def add(gid, desc, claims, truth):
        claims = [c for c in claims if c]
        if not claims:
            verdict = "ABSENT"
        else:
            ok = [c == truth for c in claims]
            verdict = "CORRECT" if all(ok) else ("CONFLICT" if any(ok) else "STALE")
        rows.append({"id": gid, "desc": desc, "claims": claims, "truth": truth, "verdict": verdict})

    add(
        "G1",
        "pushed-status of commit 25776d4",
        [first(r"Committed `?25776d4`?,?\s+(not pushed|pushed)", act)],
        truth_pushed("25776d4"),
    )
    c2 = []
    if re.search(r"MathOverflow[^.\n]{0,220}not yet published", allm):
        c2.append("not published")
    if re.search(r"mathoverflow\.net/questions/\d+", allm):
        c2.append("published")
    add("G2", "MathOverflow question published?", c2, truth_mo_published())
    c3 = []
    if re.search(r"left UNCOMMITTED in hooks repo", allm):
        c3.append("uncommitted")
    if re.search(r"committed (?:in|to) (?:the )?hooks repo|hooks repo[^.\n]{0,60}committed", allm):
        c3.append("committed")
    add("G3", "post_commit_memory self-log-loop fix committed?", c3, truth_hooks_fix_committed())
    c4 = []
    for m in re.finditer(r"Email NOT SENT[^\n]{0,60}|EMAIL: SENT|EMAIL SENT", act):
        s = m.group(0)
        if "NOT SENT" in s:
            if "[SUPERSEDED" in s:
                continue  # explicitly neutralised historical statement
            c4.append("NOT SENT")
        else:
            c4.append("SENT")
    add("G4", "author email sent?", c4, truth_email_sent())
    add(
        "G5",
        "repo visibility",
        every(r"Repo:\*\*[^\n]*?\b(PUBLIC|PRIVATE)\b", act),
        truth_repo_visibility(),
    )
    add(
        "G6",
        "U2 reply status",
        ["no reply" if re.search(r"no reply|no answer|awaiting reply", act) else None],
        truth_u2_reply(),
    )
    add(
        "G7",
        "U2 window end date",
        every(r"(?:until|~|window to)\s*~?(20\d\d-\d\d-\d\d)", act),
        truth_u2_window_end(),
    )
    add(
        "G8",
        "lemma packet version",
        [f"v{x}" for x in every(r"lemma_blind_packet\.md` v(\d+)", act)],
        truth_packet_version(),
    )
    plan = first(r"Canonical: `(outreach/CURRENT_PLAN_[\d-]+\.md)`", act)
    t9 = truth_plan_file(plan) if plan else "n/a"
    verdict9 = (
        "ABSENT"
        if not plan
        else "CORRECT"
        if t9 == "tracked"
        else "RISK"
        if t9 == "untracked"
        else "STALE"
    )
    rows.append(
        {
            "id": "G9",
            "desc": "canonical plan file exists+tracked",
            "claims": [plan] if plan else [],
            "truth": t9,
            "verdict": verdict9,
        }
    )
    m = re.search(r"## Auto-commit log\s*\n- \[[^\]]+\] `([0-9a-f]{7,})`", act)
    if m:
        lag, _ = git("rev-list", "--count", f"{m.group(1)}..HEAD")
        lag_i = int(lag) if lag.isdigit() else -1
        rows.append(
            {
                "id": "G10",
                "desc": "commits between newest logged hash and HEAD",
                "claims": [m.group(1)],
                "truth": lag_i,
                "verdict": "STALE" if lag_i > 5 else "CORRECT",
            }
        )
    else:
        rows.append(
            {
                "id": "G10",
                "desc": "commits between newest logged hash and HEAD",
                "claims": [],
                "truth": None,
                "verdict": "ABSENT",
            }
        )
    log, _ = git("log", "-8", "--format=%s%n%b")
    ents = set(re.findall(r"\bH-[A-Z0-9]+(?:-[A-Za-z0-9]+)*\b", log)) | set(
        re.findall(r"\b[A-Z][a-z]+(?:-[A-Z][a-z]+)+\b", log)
    )
    found = [e for e in ents if e in allm]
    cov = round(len(found) / len(ents), 3) if ents else 1.0
    rows.append(
        {
            "id": "G11",
            "desc": "entities of 8 newest commits present in memory",
            "claims": sorted(found),
            "truth": sorted(ents),
            "coverage": cov,
            "verdict": "CORRECT" if cov >= 0.5 else "STALE",
        }
    )
    return rows


def accuracy(rows: list[dict]) -> dict:
    cnt: dict[str, int] = {}
    for r in rows:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    present = cnt.get("CORRECT", 0) + cnt.get("STALE", 0) + cnt.get("CONFLICT", 0)
    return {
        "counts": cnt,
        "accuracy_present": round(cnt.get("CORRECT", 0) / present, 3) if present else None,
    }


# ------------------------------------------------------------------ M4 integrity
def hash_resolves(h: str) -> bool:
    for cwd in (REPO, CLAUDE):
        _, rc = git("cat-file", "-e", f"{h}^{{commit}}", cwd=cwd)
        if rc == 0:
            return True
    return False


BASES = [
    REPO,
    REPO / ".claude",
    REPO / ".claude" / "memory",
    CLAUDE,
    CLAUDE / "memory",
    CLAUDE / "rules",
    HOME,
]


def path_resolves(tok: str) -> bool:
    if any((b / tok).exists() for b in BASES):
        return True
    out, rc = git("ls-files", f"*{tok}")  # abbreviated relative path living under a subdir
    return rc == 0 and bool(out.strip())


def path_ever_existed(tok: str) -> bool:
    for cwd in (REPO, CLAUDE):
        out, _ = git("log", "--all", "--oneline", "-1", "--", tok, cwd=cwd)
        if out.strip():
            return True
    return False


def usable_path(tok: str) -> bool:
    bad = ("...", "<", ">", "*", "{", "}", "~", "$")
    return not any(x in tok for x in bad) and not tok.startswith(("http", "./", "../"))


_CACHE: dict[tuple, object] = {}


def _memo(key, fn):
    if key not in _CACHE:
        _CACHE[key] = fn()
    return _CACHE[key]


def commit_set(text: str) -> set[str]:
    return _memo(("cs", hash(text)), lambda: ml.commit_refs(text))  # type: ignore[return-value]


def pointer_flags(stores: dict[str, str]) -> list[dict]:
    flags: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for name, text in stores.items():
        for typ, val in ml._typed_matches(text):
            if (typ, val) in seen:
                continue
            seen.add((typ, val))
            if (
                typ == "hash"
                and val in commit_set(text)
                and not _memo(("h", val), lambda v=val: hash_resolves(v))
            ):
                flags.append({"store": name, "type": "DANGLING_HASH", "value": val})
            elif (
                typ == "path"
                and usable_path(val)
                and not _memo(("p", val), lambda v=val: path_resolves(v))
            ):
                flags.append(
                    {
                        "store": name,
                        "type": "DANGLING_PATH",
                        "value": val,
                        "ever_existed": _memo(("e", val), lambda v=val: path_ever_existed(v)),
                    }
                )
            elif typ == "date":
                try:
                    if datetime.strptime(val, "%Y-%m-%d").date() > TODAY + timedelta(days=90):
                        flags.append({"store": name, "type": "FUTURE_DATE", "value": val})
                except ValueError:
                    flags.append({"store": name, "type": "MALFORMED_DATE", "value": val})
    return flags


def frontmatter_flags(stores: dict[str, str]) -> list[dict]:
    out = []
    for name, text in stores.items():
        if not name.startswith("auto/") or name.endswith("MEMORY.md"):
            continue
        m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
        fm = m.group(1) if m else ""
        for key in ("name:", "description:"):
            if key not in fm:
                out.append({"store": name, "type": "FM_INVALID", "value": f"missing {key}"})
        if not re.search(r"type:\s*(user|feedback|project|reference)", fm):
            out.append(
                {"store": name, "type": "FM_INVALID", "value": "missing/invalid metadata.type"}
            )
    return out


def index_flags(stores: dict[str, str]) -> tuple[list[dict], dict]:
    idx = stores.get("auto/MEMORY.md", "")
    linked = re.findall(r"\]\(([^)]+\.md)\)", idx)
    present = {k.split("/", 1)[1] for k in stores if k.startswith("auto/")} - {"MEMORY.md"}
    flags = [
        {"store": "auto/MEMORY.md", "type": "DANGLING_INDEX", "value": f}
        for f in linked
        if f not in present
    ]
    flags += [
        {"store": f"auto/{f}", "type": "ORPHAN_FILE", "value": f}
        for f in sorted(present - set(linked))
    ]
    return flags, {"index_entries": len(linked), "files": len(present)}


def all_flags(stores: dict[str, str]) -> list[dict]:
    f2, _ = index_flags(stores)
    return pointer_flags(stores) + frontmatter_flags(stores) + f2


# ------------------------------------------------------------------ layout / age
def layout_metrics(stores: dict[str, str]) -> dict:
    act = stores["activeContext.md"]
    lines = act.splitlines()
    off, first_current = 0, None
    for ln in lines:
        if "CURRENT PLAN" in ln or ln.startswith("## Current Focus"):
            first_current = off
            break
        off += len(ln.encode("utf-8")) + 1
    runs = max((len(m.group(0)) for m in re.finditer(r"\n{3,}", act)), default=0)
    return {
        "bytes": len(act.encode("utf-8")),
        "lines": len(lines),
        "longest_line_bytes": max((len(x.encode("utf-8")) for x in lines), default=0),
        "byte_offset_of_first_current_marker": first_current,
        "read_this_first_markers": len(
            re.findall(r"READ THIS FIRST|читать первым|read first", act, re.I)
        ),
        "max_consecutive_newlines": runs,
        "summarized_lines": act.count("[summarized]"),
    }


def age_metrics() -> dict:
    out = {}
    for p in sorted(AUTO_DIR.glob("*.md")):
        age = (datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)).days
        mt = re.search(r"type:\s*(\w+)", p.read_text(encoding="utf-8"))
        out[p.name] = {"age_days": age, "type": mt.group(1) if mt else None}
    return out


# ------------------------------------------------------------------ M5 mutation test
def mutate(stores: dict[str, str], seed: int = 7, n: int = 12) -> dict:
    rng = random.Random(seed)
    base = {(f["type"], f["value"]) for f in all_flags(stores)}
    res: dict[str, dict] = {}

    def pool_of(typ: str) -> list[tuple[str, str]]:
        return sorted(
            {(s, v) for s, t in stores.items() for ty, v in ml._typed_matches(t) if ty == typ}
        )

    def rec(cls, inj, det, missed):
        res[cls] = {
            "injected": inj,
            "detected": det,
            "recall": round(det / inj, 3) if inj else None,
            "missed": missed[:3],
        }

    def trial(pool, make_mut, expect_type, expect_val=None):
        rng.shuffle(pool)
        inj = det = 0
        missed = []
        for s, v in pool[:n]:
            mv = make_mut(v)
            if mv is None:
                continue
            st = dict(stores)
            st[s] = st[s].replace(v, mv, 1)
            inj += 1
            new = {(f["type"], f["value"]) for f in all_flags(st)} - base
            want = (expect_type, expect_val if expect_val is not None else mv)
            if want in new:
                det += 1
            else:
                missed.append(mv)
        return inj, det, missed

    pool = [(s, v) for s, v in pool_of("hash") if hash_resolves(v)]
    rec(
        "hash_flip",
        *trial(
            pool,
            lambda v: (
                (v[:-1] + ("0" if v[-1] != "0" else "1"))
                if not hash_resolves(v[:-1] + ("0" if v[-1] != "0" else "1"))
                else None
            ),
            "DANGLING_HASH",
        ),
    )
    pool = [(s, v) for s, v in pool_of("path") if usable_path(v) and path_resolves(v)]
    rec(
        "path_rename",
        *trial(
            pool, lambda v: f"{v.rpartition('.')[0]}_v2.{v.rpartition('.')[2]}", "DANGLING_PATH"
        ),
    )
    pool = [(s, v) for s, v in pool_of("date") if v.startswith("2026-09")]
    rec("future_date", *trial(pool, lambda v: "2027-03-01", "FUTURE_DATE", "2027-03-01"))

    idx_files = [k for k in stores if k.startswith("auto/") and not k.endswith("MEMORY.md")]
    inj = det = 0
    for k in idx_files:
        st = {kk: vv for kk, vv in stores.items() if kk != k}
        inj += 1
        det += any(
            f["type"] == "DANGLING_INDEX" and f["value"] == k.split("/", 1)[1]
            for f in all_flags(st)
        )
    rec("index_link_removed", inj, det, [])
    inj = det = 0
    for k in idx_files:
        st = dict(stores)
        st[k] = re.sub(r"\ndescription:[^\n]*", "", st[k], count=1)
        inj += 1
        det += any(f["type"] == "FM_INVALID" and f["store"] == k for f in all_flags(st))
    rec("frontmatter_description_deleted", inj, det, [])

    # claim flips: only for claims that are CORRECT in the pristine state, flipped at the claim's own span
    pristine = {r["id"]: r["verdict"] for r in gold_claims(stores)}
    flips = [
        ("G5", r"Repo:\*\*[^\n]*?\b(PUBLIC|PRIVATE)\b", "PRIVATE"),
        ("G8", r"lemma_blind_packet\.md` v(\d+)", "2"),
        ("G7", r"(?:until|~|window to)\s*~?(2026-10-23)", "2026-11-23"),
    ]
    inj = det = 0
    missed = []
    for gid, rx, rep in flips:
        txt = stores["activeContext.md"]
        m = re.search(rx, txt)
        if not m or pristine.get(gid) != "CORRECT":
            continue
        st = dict(stores)
        st["activeContext.md"] = txt[: m.start(1)] + rep + txt[m.end(1) :]
        inj += 1
        if {r["id"]: r for r in gold_claims(st)}[gid]["verdict"] in {"STALE", "CONFLICT"}:
            det += 1
        else:
            missed.append(gid)
    rec("claim_flip_gold", inj, det, missed)

    inj = det = 0
    txt = stores["activeContext.md"]
    m = re.search(r"node stays `lead`", txt)
    if m:
        st = dict(stores)
        st["activeContext.md"] = txt.replace(m.group(0), "node stays `killed`", 1)
        inj = 1
        new = {(f["type"], f["value"]) for f in all_flags(st)} - base
        det = int(bool(new))
    rec("free_text_semantic_flip (control: expected undetectable)", inj, det, [])
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--out")
    ap.add_argument("--no-mutation", action="store_true")
    a = ap.parse_args()
    stores = load_stores()
    rows = gold_claims(stores)
    items = all_flags(stores)
    by: dict[str, int] = {}
    for f in items:
        by[f["type"]] = by.get(f["type"], 0) + 1
    _, idx_stat = index_flags(stores)
    res = {
        "label": a.label,
        "date": str(TODAY),
        "head": git("rev-parse", "--short", "HEAD")[0],
        "gold_claims": rows,
        "gold_accuracy": accuracy(rows),
        "integrity": {
            "flags_by_type": by,
            "total_flags": len(items),
            "index": idx_stat,
            "dangling_paths_deleted_in_history": sum(
                1 for f in items if f["type"] == "DANGLING_PATH" and f.get("ever_existed")
            ),
            "dangling_paths_never_existed": sum(
                1 for f in items if f["type"] == "DANGLING_PATH" and not f.get("ever_existed")
            ),
            "items": items,
        },
        "layout": layout_metrics(stores),
        "ages": age_metrics(),
    }
    if not a.no_mutation:
        res["mutation"] = mutate(stores)
    out = Path(a.out or HERE / f"results_state_{a.label}.json")
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(
        json.dumps(
            {k: res[k] for k in ("label", "head", "gold_accuracy", "layout")}, indent=1, default=str
        )
    )
    for r in rows:
        print(
            f"{r['id']:4} {r['verdict']:8} claims={str(r['claims'])[:56]:56} truth={str(r['truth'])[:36]}"
        )
    print("integrity flags:", by, "| index:", idx_stat)
    if "mutation" in res:
        print(
            "mutation recall:",
            {k: (v["injected"], v["recall"]) for k, v in res["mutation"].items()},
        )


if __name__ == "__main__":
    main()
