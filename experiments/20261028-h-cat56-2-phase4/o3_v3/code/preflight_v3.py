"""O3 v3 preflight (run before any full pass).

1. arb identities: arb_max / arb_min enclose the true max / min on random exact pairs.
2. negative controls, which must be REJECTED:
   (a) a cell with a deliberately broken projector (P = I) -> kernel certificate must fail;
   (b) the threshold lowered to just below a certified B_up -> the arb decision must be False.
3. positive test: the 1000 closest-to-threshold cells of metrics/interval_top1000.json, of which 248 lie in the
   early chunks 0..3420 (mapping: o3_v3_preflight_top_map.json, exact leaf indices). Every cell must certify
   with arb-certain B_up < s_target; the enclosures are compared with the stored binary64 B_up values.

Output: o3_v3/metrics/preflight_v3.json
Usage : python -I o3_v3/code/preflight_v3.py [n_workers]
"""

import json
import os
import random
import sys
from multiprocessing import Pool

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE4 = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "..", "metrics", "preflight_v3.json")
TOP = os.path.join(PHASE4, "metrics", "interval_top1000.json")
MAP = os.path.join(PHASE4, "o3_v3_preflight_top_map.json")
EARLY_LIMIT = 1710500  # leaves 0..1710499 = chunks 0..3420


def _load():
    sys.path.insert(0, HERE)
    import interval_cells_v3 as ivl  # noqa: E402

    return ivl


def _certify_cell(cell):
    ivl = _load()
    s = ivl.s_target
    r = ivl.cell_bound([float(v) for v in cell])
    if r["status"] != "OK":
        return {"status": r["status"], "reasons": r.get("reasons", [])}
    b = r["B_up"]
    sl = s - b
    return {"status": "OK", "certain_positive": bool(sl > 0), "slack": str(sl), "bup": str(b)}


def arb_identity_tests():
    from flint import arb, ctx

    ctx.prec = 192
    ivl = _load()
    rng = random.Random(20261031)
    bad = 0
    for _ in range(2000):
        x, y = rng.uniform(-5, 5), rng.uniform(-5, 5)
        ax, ay = arb(x), arb(y)
        mx = ivl.arb_max(ax, ay)
        mn = ivl.arb_min(ax, ay)
        # the enclosure must contain the exact max / min (both are exact binary64 values)
        if not (bool(mx.lower() <= max(x, y)) and bool(mx.upper() >= max(x, y))):
            bad += 1
        if not (bool(mn.lower() <= min(x, y)) and bool(mn.upper() >= min(x, y))):
            bad += 1
    return {"random_pairs": 2000, "enclosure_failures": bad}


def negative_controls():
    from flint import arb

    ivl = _load()
    out = {}
    # (a) broken projector: P = I instead of the exact projector
    cell = [3.130087797680651, 3.130471292877622, 5.241228857008265, 5.2416123522052365]
    b = ivl.build_cell(cell)
    fails = ivl.kernel_certificate(b["Phi0"], b["G"], ivl.I40, b["Z0"])
    out["broken_projector_rejected"] = len(fails) > 0
    out["broken_projector_reasons"] = fails
    # (b) threshold just below a certified bound must be rejected by the arb decision
    r = ivl.cell_bound(cell)
    if r["status"] == "OK":
        b_up = r["B_up"]
        s_fake = b_up - arb("1e-15")
        out["lowered_threshold_rejected"] = not bool(s_fake - b_up > 0)
    else:
        out["lowered_threshold_rejected"] = None
    return out


def positive_test(n_workers):
    with open(TOP, encoding="utf-8") as fh:
        top = json.load(fh)
    rows = top["rows"]
    with open(MAP, encoding="utf-8") as fh:
        mp = json.load(fh)
    early = set(mp["early_leaf_indices"])
    cells = [r["cell"] for r in rows]
    with Pool(n_workers) as pool:
        res = pool.map(_certify_cell, cells, chunksize=4)
    n_cert = sum(1 for r in res if r["status"] == "OK" and r["certain_positive"])
    stored = [r["B_up"] for r in rows]
    max_dev = 0.0
    for r, st in zip(res, stored):
        if r["status"] == "OK":
            # stored value is printed to 11 significant digits: compare to that resolution
            max_dev = max(
                max_dev,
                abs(float(r["bup"].split("+/-")[0].strip("[ ")) - st) if "+/-" in r["bup"] else 0.0,
            )
    return {
        "cells": len(cells),
        "certified_with_arb_positive_slack": n_cert,
        "failed": [r for r in res if not (r["status"] == "OK" and r.get("certain_positive"))][:5],
        "early_cells_in_list": len(early),
        "stored_vs_v3_max_abs_deviation_reporting_only": max_dev,
        "note": "slack and bup strings are arb enclosures; the deviation above is a float report, not a decision",
    }


def main():
    n_workers = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    report = {
        "arb_identities": arb_identity_tests(),
        "negative_controls": negative_controls(),
        "positive_1000_closest": positive_test(n_workers),
    }
    ok = (
        report["arb_identities"]["enclosure_failures"] == 0
        and report["negative_controls"].get("broken_projector_rejected") is True
        and report["negative_controls"].get("lowered_threshold_rejected") is True
        and report["positive_1000_closest"]["certified_with_arb_positive_slack"]
        == report["positive_1000_closest"]["cells"]
    )
    report["PREFLIGHT_V3"] = "PASS" if ok else "FAIL"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    print(json.dumps(report, indent=1), flush=True)


if __name__ == "__main__":
    main()
