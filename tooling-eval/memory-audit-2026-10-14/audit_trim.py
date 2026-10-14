"""M6: schedule of silent whole-section deletions by production _trim_old_entries (90-day rule), on the CURRENT activeContext.

The function reads datetime.now() internally, so 'today + D days' is emulated with max_age_days = 90 - D on a temp copy.
Run: python audit_trim.py [--out results_trim.json]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import memlib as ml  # noqa: E402

REPO = HERE.parents[1]
HOOKS = Path.home() / ".claude" / "hooks"


def load_prod():
    sys.path.insert(0, str(HOOKS))
    spec = importlib.util.spec_from_file_location("pc_trim", HOOKS / "pre_compact.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def headings(text: str) -> list[str]:
    return [h for h, _ in ml.parse_sections(text)[1]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "results_trim.json"))
    ap.add_argument("--src", default=str(REPO / ".claude" / "memory" / "activeContext.md"))
    a = ap.parse_args()
    mod = load_prod()
    src = Path(a.src).read_text(encoding="utf-8")
    h0 = headings(src)
    today = date.today()
    sched = {}
    for d in (0, 30, 53, 60, 66, 75, 90, 120):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "activeContext.md"
            p.write_text(src, encoding="utf-8")
            try:
                n = mod._trim_old_entries(p, max_age_days=max(1, 90 - d))
                after = headings(p.read_text(encoding="utf-8"))
                gone = [h for h in h0 if h not in after]
                sched[str(today + timedelta(days=d))] = {
                    "days_ahead": d,
                    "sections_removed": n,
                    "headings_removed": gone,
                    "bytes_removed": len(src.encode())
                    - len(p.read_text(encoding="utf-8").encode()),
                }
            except Exception as e:
                sched[str(today + timedelta(days=d))] = {
                    "days_ahead": d,
                    "error": f"{type(e).__name__}: {e}",
                }
    # does a trimmed section leave any archive anywhere?
    arch = [
        p.name
        for p in (REPO / ".claude" / "memory" / "history").glob("*")
        if "trim" in p.name.lower()
    ]
    out = {
        "today": str(today),
        "sections": h0,
        "schedule": sched,
        "trim_archive_files": arch,
        "hook_has_archive_write": "history"
        in (HOOKS / "pre_compact.py")
        .read_text(encoding="utf-8")
        .split("def _trim_old_entries")[1]
        .split("def extract_pending_items")[0],
    }
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    for k, v in sched.items():
        print(
            k,
            "+%dd" % v["days_ahead"],
            v.get("headings_removed", v.get("error")),
            "bytes:",
            v.get("bytes_removed"),
        )
    print(
        "trim archive files:",
        arch,
        "| _trim_old_entries writes an archive:",
        out["hook_has_archive_write"],
    )


if __name__ == "__main__":
    main()
