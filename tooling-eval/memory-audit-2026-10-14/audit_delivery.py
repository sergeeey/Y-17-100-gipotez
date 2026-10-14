"""M2 delivery: which true state facts are inside the first 2000 bytes of the SessionStart hook output?

Evidence = persisted hook outputs the harness wrote when the output exceeded its limit
(~/.claude/projects/<proj>/<session>/tool-results/hook-*-stdout.txt). The harness showed only the first
2 KB of each as a preview (observed twice in session 1d8443cd: 55.2 KB and 50 KB outputs).

The "after" arm is a SIMULATION of a hook change that is not deployed: digest inserted before the
banner (A) or after it (B, negative control). Facts are time-invariant ones only (visibility, branch,
registry size, U2 dates/reply, MO url, packet version) so a snapshot taken at session start is comparable.

Run: python audit_delivery.py [--out results_delivery.json]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import digest as dg  # noqa: E402

REPO = HERE.parents[1]
CLAUDE = Path.home() / ".claude"
WINDOW = 2000
MARK = "=== PROJECT ACTIVE CONTEXT"


def sh(cmd: list[str]) -> str:
    r = subprocess.run(
        cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return r.stdout.strip()


def truth_facts() -> list[dict]:
    """Independent of digest.py: direct tool calls / file reads."""
    vis = sh(
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
    branch = sh(["git", "branch", "--show-current"])
    blocks = re.split(
        r"\n  - id: ", (REPO / "registry" / "graph.yaml").read_text(encoding="utf-8")
    )[1:]
    n_hyp = sum(1 for b in blocks if re.search(r"\n\s+type:\s*hypothesis\b", b))
    u2 = (REPO / "outreach" / "U2_WAIT_LOG.md").read_text(encoding="utf-8")
    start = re.search(r"Clock started: \*\*(\d{4}-\d{2}-\d{2})\*\*", u2).group(1)
    mo = REPO / "outreach" / "MO_QUESTION.md"
    mo_id = (
        re.search(r"/questions/(\d+)", mo.read_text(encoding="utf-8")).group(1)
        if mo.exists()
        else "515586"
    )
    pk = (REPO / "outreach" / "lemma_blind_packet.md").read_text(encoding="utf-8").splitlines()[0]
    ver = re.search(r"\(v(\d+)\)", pk).group(1)
    return [
        {"id": "D1", "what": "repo visibility", "truth": vis, "re": rf"\b{re.escape(vis)}\b"},
        {"id": "D2", "what": "working branch", "truth": branch, "re": re.escape(branch)},
        {
            "id": "D3",
            "what": "registry hypothesis count",
            "truth": str(n_hyp),
            "re": rf"\b{n_hyp} hypotheses\b",
        },
        {
            "id": "D4",
            "what": "U2 email sent date",
            "truth": start,
            "re": rf"SENT-record exists {re.escape(start)}",
        },
        {
            "id": "D5",
            "what": "U2 window end",
            "truth": "start+30d",
            "re": r"window ends 20\d\d-\d\d-\d\d",
        },
        {"id": "D6", "what": "U2 reply status", "truth": "none", "re": r"reply on file: none"},
        {
            "id": "D7",
            "what": "MO question url",
            "truth": mo_id,
            "re": rf"mathoverflow\.net/questions/{mo_id}",
        },
        {
            "id": "D8",
            "what": "lemma packet version",
            "truth": f"v{ver}",
            "re": rf"lemma_blind_packet\.md v{ver}",
        },
    ]


def hook_outputs() -> list[Path]:
    return sorted(
        CLAUDE.glob("projects/E-*Y-17-100-gipotez/*/tool-results/hook-*-stdout.txt"),
        key=lambda p: p.stat().st_mtime,
    )


def score(text: str, facts: list[dict]) -> dict:
    hit = {f["id"]: bool(re.search(f["re"], text)) for f in facts}
    return {"hit": hit, "share": round(sum(hit.values()) / len(facts), 3)}


def window(text: str) -> str:
    return text.encode("utf-8")[:WINDOW].decode("utf-8", errors="ignore")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "results_delivery.json"))
    a = ap.parse_args()
    facts = truth_facts()
    outs = hook_outputs()
    res: dict = {
        "window_bytes": WINDOW,
        "facts": [{k: f[k] for k in ("id", "what", "truth")} for f in facts],
        "outputs": [],
    }
    dg_text = dg.build_digest(REPO)
    res["digest_bytes"] = len(dg_text.encode("utf-8"))
    res["digest_score"] = score(dg_text, facts)
    for p in outs:
        text = p.read_text(encoding="utf-8", errors="replace")
        i = text.find(MARK)
        prefix, rest = (text[:i], text[i:]) if i >= 0 else (text, "")
        arm_a = dg_text + "\n" + text
        arm_b = prefix + dg_text + "\n" + rest
        row = {
            "file": p.name,
            "bytes": len(text.encode("utf-8")),
            "offset_of_activeContext": len(prefix.encode("utf-8")),
            "activeContext_bytes_visible_in_window": max(0, WINDOW - len(prefix.encode("utf-8"))),
            "before_window": score(window(text), facts),
            "before_full_output": score(text, facts),
            "after_A_digest_first_window": score(window(arm_a), facts),
            "after_B_digest_after_banner_window": score(window(arm_b), facts),
        }
        res["outputs"].append(row)
    Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(
        "digest bytes:",
        res["digest_bytes"],
        "| digest carries",
        res["digest_score"]["share"],
        "of facts",
    )
    for r in res["outputs"]:
        print(
            f"{r['file'][:24]} bytes={r['bytes']} activeContext starts at byte {r['offset_of_activeContext']} "
            f"(visible activeContext bytes in window: {r['activeContext_bytes_visible_in_window']})\n"
            f"   before window {r['before_window']['share']} | before FULL output {r['before_full_output']['share']} | "
            f"after A {r['after_A_digest_first_window']['share']} | after B {r['after_B_digest_after_banner_window']['share']}"
        )


if __name__ == "__main__":
    main()
