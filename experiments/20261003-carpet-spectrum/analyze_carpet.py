"""Carpet decimation tests (search, nesting, pair-sum structure, multiplicities) + gasket controls on same code."""

import json
import sys
import time

import numpy as np

from lib import *
from search import search_all

OUT = {}


def distinct(ev):
    return cluster(ev, 1e-9)


def nesting_fraction(fine, coarse):
    f = fine[fine > 1e-9]
    j = np.clip(np.searchsorted(coarse, f), 1, len(coarse) - 1)
    d = np.minimum(np.abs(f - coarse[j]), np.abs(f - coarse[j - 1]))
    return float((d <= 1e-8).mean())


def pair_sum_peak(fine, tol=1e-8):
    n = len(fine)
    if n > 6000:  # O(n^2) memory; skipped for level 5 (documented)
        return [(float('nan'), -1)]
    iu = np.triu_indices(n, 1)
    s = np.sort((fine[:, None] + fine[None, :])[iu])
    brk = np.nonzero(np.diff(s) > tol)[0]
    starts = np.concatenate([[0], brk + 1])
    ends = np.concatenate([brk + 1, [len(s)]])
    cnt = ends - starts
    top = np.argsort(-cnt)[:3]
    return [(float(s[starts[i] : ends[i]].mean()), int(cnt[i])) for i in top]


def analyze_pair(name, fev, cev, dmax=6):
    fv, fm = distinct(fev)
    cv, cm = distinct(cev)
    t = time.time()
    res = {
        "name": name,
        "n_fine_distinct": len(fv),
        "n_coarse_distinct": len(cv),
        "nesting_fraction_R_identity": nesting_fraction(fv, cv),
    }
    res["search_raw"] = [{k: v for k, v in r.items() if k != "M"} for r in search_all(fv, cv, dmax)]
    res["search_no_identity"] = [
        {k: v for k, v in r.items() if k != "M"}
        for r in search_all(fv, cv, dmax, exclude_identity=True)
    ]
    res["pair_sum_top3(sum,count)"] = pair_sum_peak(fv)
    res["max_mult_fine"] = int(fm.max())
    res["frac_eigs_in_degenerate_levels_fine"] = float(fm[fm > 1].sum() / fm.sum())
    res["seconds"] = time.time() - t
    OUT[name] = res
    best_raw = max(r["frac"] for r in res["search_raw"])
    best_ni = max(r["frac"] for r in res["search_no_identity"])
    print(
        f"[{name}] distinct {len(fv)}/{len(cv)} nesting(identity)={res['nesting_fraction_R_identity']:.3f} "
        f"best_frac raw={best_raw:.3f} no-identity={best_ni:.3f} pair-sum top={res['pair_sum_top3(sum,count)'][0]} "
        f"maxmult={res['max_mult_fine']} {res['seconds']:.0f}s",
        flush=True,
    )
    for r in res["search_no_identity"]:
        a = None if r["a"] is None else [float(f"{x:.5g}") for x in r["a"]]
        print(
            f"      d={r['d']} matched={r['matched']}/{r['n_fine']} frac={r['frac']:.3f} cov={r['coverage']:.3f} a={a}",
            flush=True,
        )


if __name__ == "__main__":
    levels = (
        [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [2, 3]
    )  # coarse levels to test
    # gasket control through the SAME code path (sanity of this analysis script)
    G = np.load("gasket_4L2_spectra.npz")
    analyze_pair("CONTROL_gasket_5to6", G["L6"], G["L5"])
    for kind in ("L1", "L2"):
        S = dict(np.load(f"carpet_spectra_{kind}.npz"))
        try:
            S.update(dict(np.load(f"carpet_spectra_{kind}_n5.npz")))
        except FileNotFoundError:
            pass
        for n in levels:
            if f"n{n + 1}" in S:
                analyze_pair(f"carpet_{kind}_{n}to{n + 1}", S[f"n{n + 1}"], S[f"n{n}"])
    json.dump(
        OUT, open(f"analysis_pairs_{'_'.join(map(str, levels))}.json", "w"), indent=1, default=float
    )
