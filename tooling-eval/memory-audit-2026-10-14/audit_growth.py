"""P2-5 of the review: does the anchor-preserving summary make the file grow without bound?

Synthetic long-run: start from the real BEFORE snapshot; repeatedly append batches of realistic new bullets
(~1.2 KB, with anchors, dated one day apart) to '## Current Focus' and run one compaction; track bytes.
Arms: original hook, patched hook. Only the 90-day trim bounds the long run in production, so it is also applied
(emulated by dropping bullets older than 90 simulated days at each round).
Run: python audit_growth.py
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import audit_compaction as ac  # noqa: E402

PATCHED = HERE / "proposed" / "pre_compact_patched.py"


def load(path: Path, name: str):
    sys.path.insert(0, str(ac.HOOKS))
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def bullet(rng: random.Random, d: date, i: int) -> str:
    h = "".join(rng.choice("0123456789abcdef") for _ in range(7)) + "a1"[i % 2]
    filler = " ".join(
        rng.choice(["result", "kill", "check", "audit", "scan", "ratio", "bound", "sweep", "claim"])
        for _ in range(120)
    )
    return (
        f"- **[{d} H-SIM-{i}, commit `{h[:7]}`]** experiments/{d}-sim-{i}/decision.md verdict KILLED value "
        f"{rng.uniform(0, 9):.4f}; {filler}"
    )


def run(label: str, mod, rounds: int, per_round: int) -> list[int]:
    rng = random.Random(11)
    text = (HERE / "snapshots" / "before" / "activeContext.md").read_text(encoding="utf-8")
    day = date(2026, 10, 14)
    sizes = []
    for r in range(rounds):
        add = [bullet(rng, day + timedelta(days=r), r * per_round + k) for k in range(per_round)]
        text = text.replace("## Current Focus\n", "## Current Focus\n" + "\n".join(add) + "\n", 1)
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "activeContext.md"
            p.write_text(text, encoding="utf-8")
            sim_days = (day + timedelta(days=r)) - date.today()
            mod._trim_old_entries(p, max_age_days=max(1, 90 - sim_days.days))
            ac.prod_compact(mod, p.read_text(encoding="utf-8"))  # discard
            text = ac.prod_compact(mod, p.read_text(encoding="utf-8"))
        sizes.append(len(text.encode("utf-8")))
    return sizes


def main() -> None:
    orig = ac.load_prod()
    pat = load(PATCHED, "pc_growth_patched")
    rounds, per = 120, 5  # 600 new bullets over 120 simulated days
    out = {}
    for name, mod in (("orig", orig), ("patched", pat)):
        s = run(name, mod, rounds, per)
        out[name] = {
            "start": s[0],
            "r30": s[29],
            "r60": s[59],
            "r90": s[89],
            "end": s[-1],
            "max": max(s),
        }
    Path(HERE / "results_growth.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
