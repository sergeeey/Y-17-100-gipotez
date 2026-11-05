"""Independent audit of the O3 v3 records (no interval recomputation; reads records and journals only).

Checks, for every chunk in the journal:
  * the chunk ID is in the expected set, and every expected chunk appears exactly once (coverage, no duplicates);
  * the record file exists and its SHA-256 equals the hash stored in the journal line;
  * the record file has exactly n lines, leaf indices base..base+n-1 in order (no gap, no duplicate leaf);
  * every line has ok = true (any failure is reported with its leaf index and reasons);
  * the number of ok lines equals the journal's ok count.
Then, over all leaves: the minimum certified slack, as an arb enclosure parsed from the record strings, and the
decision "min slack certainly positive" (arb comparison). Parsing uses python-flint arb("a +/- r"), so the result
is an enclosure, not a float.
Also checks that the input hashes in the run manifests equal the files on disk.

Usage (from phase4): python -I o3_v3/code/audit_v3_coverage.py <first_chunk> <last_chunk> <out_name>
Output: o3_v3/metrics/audit_<out_name>.json
"""

import gzip
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
O3V3 = os.path.normpath(os.path.join(HERE, ".."))
RECORDS = os.path.join(O3V3, "records")
PROGRESS = os.path.join(O3V3, "metrics", "o3v3_progress.jsonl")
CHUNK = 500
N_LEAVES = 3955841
N_CHUNKS = (N_LEAVES + CHUNK - 1) // CHUNK


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def parse_arb(s):
    """Parse an arb enclosure string '[m +/- r]' or 'm +/- r' into an arb value (exact enclosure)."""
    from flint import arb

    t = s.strip().strip("[]").strip()
    return arb(t)


def main():
    first, last, name = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    expected = list(range(first, last + 1))
    report = {"expected_chunks": [first, last], "problems": []}

    journal = {}
    dup_lines = 0
    with open(PROGRESS, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec["chunk"] in journal:
                dup_lines += 1
                report["problems"].append(f"duplicate journal line for chunk {rec['chunk']}")
            journal[rec["chunk"]] = rec
    report["journal_duplicate_lines"] = dup_lines
    present = [c for c in expected if c in journal]
    missing = [c for c in expected if c not in journal]
    extra = sorted(c for c in journal if c < first or c > last)
    report["chunks_expected"] = len(expected)
    report["chunks_present"] = len(present)
    report["missing_chunks"] = missing[:50]
    report["n_missing"] = len(missing)
    report["extra_chunks_outside_range"] = extra[:50]

    leaves_total = 0
    ok_total = 0
    min_slack = None
    max_bup = None
    fails = []
    for c in present:
        jr = journal[c]
        base = c * CHUNK
        n = min(CHUNK, N_LEAVES - base)
        if jr["n"] != n:
            report["problems"].append(f"chunk {c}: journal n={jr['n']} expected {n}")
        path = os.path.join(RECORDS, f"chunk_{c:05d}.jsonl.gz")
        if not os.path.exists(path):
            report["problems"].append(f"chunk {c}: record file missing")
            continue
        if sha256_file(path) != jr["record_sha256"]:
            report["problems"].append(f"chunk {c}: record SHA-256 mismatch with journal")
        ok_c = 0
        expect_leaf = base
        with gzip.open(path, "rt", encoding="utf-8") as gz:
            for line in gz:
                if not line.strip():
                    continue
                r = json.loads(line)
                if r["leaf"] != expect_leaf:
                    report["problems"].append(
                        f"chunk {c}: leaf {r['leaf']} where {expect_leaf} expected"
                    )
                    expect_leaf = r["leaf"]
                expect_leaf += 1
                leaves_total += 1
                if r.get("ok") is True:
                    ok_c += 1
                    sl = parse_arb(r["slack"])
                    bu = parse_arb(r["bup"])
                    min_slack = sl if min_slack is None else _arb_min(min_slack, sl)
                    max_bup = bu if max_bup is None else _arb_max(max_bup, bu)
                else:
                    fails.append(
                        {
                            "chunk": c,
                            "leaf": r["leaf"],
                            "status": r.get("status"),
                            "reasons": r.get("reasons"),
                        }
                    )
        if ok_c != jr["ok"]:
            report["problems"].append(f"chunk {c}: ok lines {ok_c} != journal ok {jr['ok']}")
        ok_total += ok_c

    report["leaves_read"] = leaves_total
    report["leaves_expected_in_range"] = sum(min(CHUNK, N_LEAVES - c * CHUNK) for c in present)
    report["ok_lines"] = ok_total
    report["failed_leaves"] = len(fails)
    report["first_failures"] = fails[:20]
    report["min_slack_enclosure"] = None if min_slack is None else str(min_slack)
    report["min_slack_certainly_positive"] = None if min_slack is None else bool(min_slack > 0)
    report["max_bup_enclosure"] = None if max_bup is None else str(max_bup)
    report["max_bup_below_threshold_certain"] = None

    # Input hashes: every run manifest overlapping this range must describe files that are on disk now.
    # WHY "unlocated" is reported, not passed: inputs outside the repo (R_input.npz, instance.jsonl,
    # s8_admissible_span.py) cannot be checked from here and must not count as verified.
    checked, mismatch, unlocated = [], [], []
    covered = set()
    digests_of = {}  # chunk -> set of inputs digests of the manifests that cover it
    metrics_dir = os.path.join(O3V3, "metrics")
    for fn in sorted(os.listdir(metrics_dir)):
        if not (fn.startswith("run_manifest_") and fn.endswith(".json")):
            continue
        with open(os.path.join(metrics_dir, fn), encoding="utf-8") as fh:
            man = json.load(fh)
        if man["last_chunk"] < first or man["first_chunk"] > last:
            continue
        man_digest = hashlib.sha256(
            json.dumps(man["sha256"], sort_keys=True).encode("utf-8")
        ).hexdigest()
        for c in range(max(first, man["first_chunk"]), min(last, man["last_chunk"]) + 1):
            covered.add(c)
            digests_of.setdefault(c, set()).add(man_digest)
        # WHY input_name/want_sha, not name: `name` is the output label used for audit_<name>.json below.
        for input_name, want_sha in man["sha256"].items():
            found = [
                p
                for p in (
                    os.path.join(O3V3, "inputs", input_name),
                    os.path.join(HERE, input_name),
                )
                if os.path.exists(p)
            ]
            if not found:
                unlocated.append(f"{fn}:{input_name}")
            elif sha256_file(found[0]) == want_sha:
                checked.append(f"{fn}:{input_name}")
            else:
                mismatch.append(f"{fn}:{input_name}")
    report["manifest_inputs_checked"] = sorted(set(checked))
    report["manifest_inputs_mismatch"] = sorted(set(mismatch))
    report["manifest_inputs_unlocated"] = sorted(set(unlocated))

    # WHY coverage is a problem, not a note: a range with no manifest has no recorded inputs to check,
    # so silence there must not read as a pass (review of 6164265, P1-2).
    uncovered = [c for c in expected if c not in covered]
    report["manifest_uncovered_chunks"] = len(uncovered)
    if uncovered:
        report["problems"].append(
            f"no run manifest covers {len(uncovered)} chunk(s), first {uncovered[:5]}"
        )

    # Journal digests: a line written under other inputs must not be accepted. Lines without the field
    # are older runs (before the resume guard) and are counted, not failed.
    d_ok = d_bad = d_absent = 0
    for c in present:
        rec_digest = journal[c].get("inputs_digest")
        if rec_digest is None:
            d_absent += 1
        elif digests_of.get(c) == {rec_digest}:
            d_ok += 1
        else:
            d_bad += 1
            report["problems"].append(
                f"chunk {c}: journal inputs_digest does not match its run manifest"
            )
    report["journal_inputs_digest_ok"] = d_ok
    report["journal_inputs_digest_bad"] = d_bad
    report["journal_inputs_digest_absent"] = d_absent

    # WHY a separate flag: inputs outside the repo are not checkable here, so COMPLETE_STRICT alone does
    # not say the mathematical inputs were verified. Read this flag with the verdict.
    # WHY absent and bad count too: a journal line with no digest is not tied to any manifest, so it
    # cannot be called verified (review of 32d6f26).
    report["inputs_fully_verified"] = bool(
        not unlocated and not mismatch and not uncovered and d_absent == 0 and d_bad == 0
    )

    report["verdict"] = (
        "COMPLETE_STRICT"
        if (
            not report["problems"]
            and not missing
            and not fails
            and leaves_total == report["leaves_expected_in_range"]
            # WHY: the slack flag was computed but never gated the verdict, so a run with
            # every record ok=true and a negative certified lower bound was still reported
            # COMPLETE_STRICT (found 2026-11-05). None (no ok leaves) is not True -> fails closed.
            and report["min_slack_certainly_positive"] is True
            and not report["manifest_inputs_mismatch"]
        )
        else "INCOMPLETE_OR_FAILED"
    )
    out = os.path.join(O3V3, "metrics", f"audit_{name}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "first_failures"}, indent=1))


def _arb_min(a, b):
    return (a + b - abs(a - b)) / 2


def _arb_max(a, b):
    return (a + b + abs(a - b)) / 2


if __name__ == "__main__":
    main()
