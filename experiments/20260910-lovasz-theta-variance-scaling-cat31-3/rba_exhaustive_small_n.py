"""Exhaustive small-n control: EXACT q*E[R] with no Monte Carlo at all.

For small primes the whole central layer is enumerable: every q-subset S of
{1..m} and, for each, every free j.  That gives the exact population value of
q*E[R1], q*E[R2], q*E[R] with zero sampling error, so the Monte-Carlo machinery
used at n=509..4093 can be checked against a value it did not produce.

This is a control, NOT part of the pre-specified 509/1021/2053/4093 scaling fit:
at n=23..41 the central layer is far from any asymptotic regime, and mixing
these q into the model comparison would conflate two different questions.
"""

from __future__ import annotations

import itertools
import json
import time
from pathlib import Path

import numpy as np
import rba_decomposition_test as R

HERE = Path(__file__).resolve().parent


def exact_layer(n, method="highs-ipm", max_subsets=None):
    m = (n - 1) // 2
    q = m // 2
    F = m - q
    lp = R.ReducedLP(n, method=method)
    cache = {}

    def solve(key):
        if key not in cache:
            w, _st, _, _, _ = lp.solve(np.array(key))
            cache[key] = None if w is None else R.p_from_w(w)
        return cache[key]

    r1s, r2s, r0s, Is, Ds, bulk_errs, dI_errs = [], [], [], [], [], [], []
    allS = list(itertools.combinations(range(1, m + 1), q))
    if max_subsets and len(allS) > max_subsets:
        rng = np.random.default_rng(4242)
        idx = rng.choice(len(allS), size=max_subsets, replace=False)
        allS = [allS[i] for i in sorted(idx)]
        exhaustive = False
    else:
        exhaustive = True
    t0 = time.perf_counter()
    for Stup in allS:
        got = solve(Stup)
        if got is None:
            continue
        p, w0 = got
        S = np.array(Stup)
        supp = np.nonzero(p)[0]
        pk = p[supp]
        s2 = float(pk @ pk)
        s3 = float((pk * pk) @ pk)
        I_S = q * s2
        D_S = q * q * (s3 - s2 * s2)
        tau = w0 / (1.0 - w0)
        free = np.setdiff1d(np.arange(1, m + 1), S)
        C = lp.cosval[np.outer(free, supp + 1) % n]
        mj = C @ pk
        Aj = (C @ (pk * pk)) - mj * s2
        gA = (tau + mj) * Aj
        bulk_errs.append(abs(float(gA.mean()) - (n / (4.0 * F)) * (s3 - s2 * s2)))
        inner, unorm = [], []
        for j in free:
            got_c = solve(tuple(sorted((*Stup, int(j)))))
            if got_c is None:
                continue
            pc = got_c[0]
            u = pc - p
            ip = float(p @ u)
            un = float(u @ u)
            inner.append(ip)
            unorm.append(un)
            I_c = (q + 1) * float(pc @ pc)
            dI_errs.append(abs((I_c - I_S) - (I_S / q + 2 * (q + 1) * ip + (q + 1) * un)))
        inner = np.asarray(inner)
        unorm = np.asarray(unorm)
        r1s.append(2.0 * (q + 1) * float((inner + gA).mean()))
        r2s.append((q + 1) * float(unorm.mean()))
        r0s.append(s2)
        Is.append(I_S)
        Ds.append(D_S)
    el = time.perf_counter() - t0
    r1 = float(np.mean(r1s))
    r2 = float(np.mean(r2s))
    r0 = float(np.mean(r0s))
    return {
        "n": n, "m": m, "q": q, "F": F, "exhaustive": exhaustive,
        "num_S": len(r1s), "num_S_total": len(list(itertools.combinations(range(1, m + 1), q))),
        "lp_solves": len(cache), "elapsed_s": el,
        "qR0": q * r0, "qR1": q * r1, "qR2": q * r2,
        "qR1_plus_R2": q * (r1 + r2), "qR_total": q * (r0 + r1 + r2),
        "E_I": float(np.mean(Is)), "E_D": float(np.mean(Ds)),
        "K_ADC": float(np.mean(Ds) / (np.mean(Is) - 1.0)),
        "cancel_ratio": abs(r1 + r2) / (abs(r1) + abs(r2)),
        "max_bulk_identity_error": float(max(bulk_errs)),
        "max_delta_I_identity_error": float(max(dI_errs)),
    }


def main():
    out = [exact_layer(n, max_subsets=3000) for n in (17, 23, 29, 31, 37, 41)]
    (HERE / "metrics").mkdir(exist_ok=True)
    (HERE / "metrics" / "rba_exhaustive_small_n.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
