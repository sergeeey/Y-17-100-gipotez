# WHY: independent consistency check of the O3 v2 journal (metrics/o3_progress.jsonl) against the leaf count,
# the chunk cover, and the recorded input hashes.  Read-only; writes metrics/o3_journal_audit_2026-10-31.json.
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
JOURNAL = os.path.join(ROOT, "metrics", "o3_progress.jsonl")
SUMMARY = os.path.join(ROOT, "metrics", "o3_summary.json")
INPUTS = [
    os.path.join(ROOT, "inputs", "R.npz"),
    os.path.join(ROOT, "inputs", "leaves.npy"),
    os.path.join(ROOT, "inputs", "instance.jsonl"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


chunks = {}
dup = 0
with open(JOURNAL, encoding="utf-8") as fh:
    for line in fh:
        rec = json.loads(line)
        c = rec["chunk"]
        if c in chunks:
            dup += 1
        chunks[c] = rec

n_total = sum(r["n"] for r in chunks.values())
ok_total = sum(r["ok"] for r in chunks.values())
fail_total = sum(r["fails"] for r in chunks.values())
summary = json.load(open(SUMMARY, encoding="utf-8"))
out = {
    "chunks_unique": len(chunks),
    "chunks_expected": summary["chunks_total"],
    "duplicate_lines": dup,
    "leaves_journal_sum_n": n_total,
    "leaves_expected": summary["leaves_total"],
    "ok_journal_sum": ok_total,
    "fails_journal_sum": fail_total,
    "cover_complete": sorted(chunks) == list(range(summary["chunks_total"])),
    "counts_match": n_total == summary["leaves_total"] and ok_total == n_total and fail_total == 0,
    "input_sha256": {os.path.relpath(p, ROOT): sha256(p) for p in INPUTS if os.path.exists(p)},
    "summary_leaves_sha256": summary["leaves_sha256"],
    "summary_final_gap": summary["final_gap_trR_minus_20s"],
    "summary_s_target": summary["s_target"],
    "note": "per-leaf B_up is NOT stored for chunks of the earlier run; only ok/fails per chunk. Interval verdict rests on arb ok flags.",
}
out["AUDIT_PASS"] = out["cover_complete"] and out["counts_match"] and out["duplicate_lines"] == 0
json.dump(
    out,
    open(os.path.join(ROOT, "metrics", "o3_journal_audit_2026-10-31.json"), "w", encoding="utf-8"),
    indent=1,
)
print(json.dumps(out, indent=1))
