#!/usr/bin/env python3
"""Path B — independent reimplementation for seed 701082.

Shares ONLY the mathematical specification in FORMAT.md and the JSON instance.
Does NOT import verify_exact_Q, h2_core, or any project LP helpers.

Uses:
  - numpy object-int Gaussian arithmetic for PCC / QFIM / generators
  - modular rank over several primes (cross-check)
  - optional FLINT exact rank if python-flint is installed (reported separately)

Usage:
  python path_b_independent.py instance_seed701082.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

D, R, K, S = 22, 2, 20, 16
MODULI = (1_000_003, 1_000_033, 999_983, 1_000_039)  # several primes


def load_blocks(path: Path) -> list[tuple[np.ndarray, np.ndarray]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "blocks_Re_Im" in data:
        out = []
        for blk in data["blocks_Re_Im"]:
            re = np.array(blk["Re"], dtype=object)
            im = np.array(blk["Im"], dtype=object)
            assert re.shape == (K, R) and im.shape == (K, R)
            out.append((re, im))
        return out
    # fallback flat
    blocks = []
    for x in data["blocks_flat"]:
        re = np.array([[x[c * R + a] for a in range(R)] for c in range(K)], dtype=object)
        im = np.array([[x[K * R + c * R + a] for a in range(R)] for c in range(K)], dtype=object)
        blocks.append((re, im))
    return blocks


def zadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def zsub(a, b):
    return a[0] - b[0], a[1] - b[1]


def zmul(a, b):
    # (ar+iai)(br+ibi)
    return a[0].dot(b[0]) - a[1].dot(b[1]), a[0].dot(b[1]) + a[1].dot(b[0])


def zdag(a):
    return a[0].T.copy(), (-a[1].T.copy())


def zscale(c: int, a):
    return c * a[0], c * a[1]


def ztimes_i(a):
    # i*(ar+i ai) = -ai + i ar
    return -a[1], a[0]


def is_zero(a) -> bool:
    return not (np.any(a[0]) or np.any(a[1]))


def make_L(B):
    """L = [[0, A^dag],[A, 0]] with A = -2i B = 2 Im - 2i Re."""
    re, im = B
    A = (2 * im, -2 * re)
    Ad = zdag(A)
    Lr = np.zeros((D, D), dtype=object)
    Li = np.zeros((D, D), dtype=object)
    Lr[R:, :R], Li[R:, :R] = A
    Lr[:R, R:], Li[:R, R:] = Ad
    return (Lr, Li), A


def support_sigmas():
    """Real basis of Herm(r) embedded as d x d (support block only). r=2 → 4 gens."""
    sig = []
    for a in range(R):
        m = (np.zeros((D, D), dtype=object), np.zeros((D, D), dtype=object))
        m[0][a, a] = 1
        sig.append(m)
    for a in range(R):
        for b in range(a + 1, R):
            m = (np.zeros((D, D), dtype=object), np.zeros((D, D), dtype=object))
            m[0][a, b] = m[0][b, a] = 1
            sig.append(m)
            m = (np.zeros((D, D), dtype=object), np.zeros((D, D), dtype=object))
            m[1][a, b] = -1
            m[1][b, a] = 1
            sig.append(m)
    return sig


def vec_ri(m) -> list[int]:
    return [int(v) for v in m[0].ravel()] + [int(v) for v in m[1].ravel()]


def check_pcc(Ls) -> bool:
    for i in range(S):
        for j in range(i + 1, S):
            c = zsub(zmul(Ls[i], Ls[j]), zmul(Ls[j], Ls[i]))
            # support-support block
            if not is_zero((c[0][:R, :R], c[1][:R, :R])):
                return False
    return True


def qfim(As) -> list[list[int]]:
    q = [1, 2]
    F = [[0] * S for _ in range(S)]
    for i in range(S):
        for j in range(S):
            m = zmul(zdag(As[i]), As[j])
            F[i][j] = int(sum(q[a] * m[0][a, a] for a in range(R)))
    return F


def det_mod(F: list[list[int]], p: int) -> int:
    """Exact det mod p via Gaussian elimination."""
    n = len(F)
    A = [[F[i][j] % p for j in range(n)] for i in range(n)]
    det = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if A[r][col] % p != 0), None)
        if pivot is None:
            return 0
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            det = (-det) % p
        inv = pow(A[col][col], -1, p)
        det = (det * A[col][col]) % p
        for j in range(col, n):
            A[col][j] = (A[col][j] * inv) % p
        for r in range(n):
            if r == col:
                continue
            factor = A[r][col]
            if factor == 0:
                continue
            for j in range(col, n):
                A[r][j] = (A[r][j] - factor * A[col][j]) % p
    return det % p


def build_rows(Ls) -> list[list[int]]:
    sig = support_sigmas()
    rows = []
    for sg in sig:
        for i in range(S):
            mm = ztimes_i(zsub(zmul(sg, Ls[i]), zmul(Ls[i], sg)))
            rows.append(vec_ri(mm))
        for i in range(S):
            for j in range(i + 1, S):
                w = zsub(zmul(zmul(Ls[i], sg), Ls[j]), zmul(zmul(Ls[j], sg), Ls[i]))
                rows.append(vec_ri(ztimes_i(w)))
    return rows


def rank_mod(rows: list[list[int]], p: int) -> int:
    if not rows:
        return 0
    m, n = len(rows), len(rows[0])
    A = [[rows[i][j] % p for j in range(n)] for i in range(m)]
    rank = 0
    row = 0
    for col in range(n):
        pivot = next((r for r in range(row, m) if A[r][col] % p != 0), None)
        if pivot is None:
            continue
        A[row], A[pivot] = A[pivot], A[row]
        inv = pow(A[row][col], -1, p)
        for j in range(col, n):
            A[row][j] = (A[row][j] * inv) % p
        for r in range(m):
            if r == row:
                continue
            factor = A[r][col]
            if factor == 0:
                continue
            for j in range(col, n):
                A[r][j] = (A[r][j] - factor * A[row][j]) % p
        rank += 1
        row += 1
        if row == m:
            break
    return rank


def flint_rank(rows: list[list[int]]) -> int | None:
    try:
        import flint
    except ImportError:
        return None
    return int(flint.fmpz_mat(rows).rank())


def run(blocks, *, label: str = "clean") -> dict:
    Ls, As = [], []
    max_abs = 0
    for B in blocks:
        max_abs = max(
            max_abs,
            int(np.max(np.abs(B[0].astype(object)))),
            int(np.max(np.abs(B[1].astype(object)))),
        )
        L, A = make_L(B)
        Ls.append(L)
        As.append(A)
    pcc = check_pcc(Ls)
    F = qfim(As)
    det_mods = {p: det_mod(F, p) for p in MODULI}
    qfim_ok = all(v != 0 for v in det_mods.values())
    rows = build_rows(Ls)
    ranks = {p: rank_mod(rows, p) for p in MODULI}
    # if all moduli agree, take that; else report disagreement
    uniq = set(ranks.values())
    rank_mod_agree = len(uniq) == 1
    rank_m = next(iter(uniq)) if rank_mod_agree else max(uniq)  # conservative note
    rank_f = flint_rank(rows)
    dim_v = rank_f if rank_f is not None else rank_m
    dim_vp = D * D - dim_v
    return {
        "label": label,
        "max_abs_entry": max_abs,
        "pcc_exact": pcc,
        "qfim_det_nonzero_moduli": qfim_ok,
        "det_moduli": det_mods,
        "n_rows": len(rows),
        "n_cols": len(rows[0]) if rows else 0,
        "rank_moduli": ranks,
        "rank_moduli_agree": rank_mod_agree,
        "flint_rank": rank_f,
        "dimV": dim_v,
        "dimVperp": dim_vp,
        "fires": dim_vp < D,
    }


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "instance_seed701082.json")
    blocks = load_blocks(path)

    clean = run(blocks, label="clean")
    print("PATH_B_CLEAN", json.dumps(clean, indent=2, default=str))

    # negative control 1: flip one entry
    broken = [(b[0].copy(), b[1].copy()) for b in blocks]
    broken[0][0][0, 0] = int(broken[0][0][0, 0]) + 1
    neg = run(broken, label="flip_B0_Re00")
    print("PATH_B_NEG_FLIP", json.dumps(neg, indent=2, default=str))

    # negative control 2: duplicate block → singular QFIM likely
    sing = [(b[0].copy(), b[1].copy()) for b in blocks]
    sing[1] = (sing[0][0].copy(), sing[0][1].copy())
    neg2 = run(sing, label="duplicate_B0_as_B1")
    print("PATH_B_NEG_SINGULAR", json.dumps(neg2, indent=2, default=str))

    # gate verdict
    path_b_pass = (
        clean["pcc_exact"]
        and clean["qfim_det_nonzero_moduli"]
        and clean["dimV"] == 463
        and clean["dimVperp"] == 21
        and clean["fires"]
        and clean["max_abs_entry"] <= 78
        and (clean["flint_rank"] in (None, 463))
        and clean["rank_moduli_agree"]
        and not neg["pcc_exact"]  # flip must break PCC (or at least not stay clean fire falsely)
    )
    # singular control: det should vanish
    sing_ok = not neg2["qfim_det_nonzero_moduli"]

    out = {
        "path_b_pass": path_b_pass,
        "singular_control_ok": sing_ok,
        "clean": clean,
        "neg_flip_pcc": neg["pcc_exact"],
        "neg_singular_qfim_ok_nonzero": neg2["qfim_det_nonzero_moduli"],
    }
    report = path.parent / "PATH_B_REPORT.json"
    report.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        "PATH_B_VERDICT", json.dumps({"path_b_pass": path_b_pass, "singular_control_ok": sing_ok})
    )


if __name__ == "__main__":
    main()
