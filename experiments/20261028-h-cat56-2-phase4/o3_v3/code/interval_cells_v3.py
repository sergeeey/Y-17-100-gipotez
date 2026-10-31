"""O3 v3 (strict): interval certificate for S- cells, with every decision made in arb.

Relative to o3_v2/code/interval_cells_v2.py the bound formulas are unchanged. What changes is the decision
logic, which in v2 used binary64 selection on the critical path (review: O3_AUDIT_RECORD.md, items 3-4):

  * max/min of arb enclosures: max(a,b) = (a+b+|a-b|)/2 and min(a,b) = (a+b-|a-b|)/2 are arb expressions whose
    enclosure contains the true max/min. No float() comparison is used for any selection.
  * sign tests are arb comparisons. python-flint arb comparisons are certain: `x > 0` is True only if every
    value of the enclosure is positive (checked in o3_v3/metrics/arb_semantics_test.py).
  * the kernel-certificate row sums and the contains-zero tests are arb.
  * the margin 1e-12 is the exact decimal enclosure arb("1e-12"), not the binary64 literal.
  * tr R is the exact sum of the binary64 real diagonal of R_raw. The Hermitian part H = (R_raw+R_raw^H)/2 has
    real diagonal equal to Re R_raw, so the trace is exact and refers to the same H as the cell bounds.
  * s_target_f = fl(0.9*tr R/20) is computed exactly as in v2, so the threshold value is unchanged.

Kernel certificate, as in v2 (all arb, 192 bit):
  (a) det(G) > 0 with G = Phi0 Phi0^T            -> Phi0 has full row rank 36 -> dim ker Phi0 = 4
  (b) Phi0 * Z0 contains 0 entrywise              -> sanity (exact kernel membership is algebraic, see build_cell)
  (c) Gershgorin on Z0^T Z0 - I: row sums < 1     -> columns of Z0 are linearly independent
  (d) Phi0 * P contains 0 entrywise               -> sanity (P is the exact projector by construction)
P = I - Phi0^T G^-1 Phi0 is built in arb from the exact Phi0; the float SVD only seeds the starting vectors,
which P projects exactly. Not checked here: the cell lemma (math) and the cone reduction (see STAGE_C).
"""

import hashlib
import os
import sys

import numpy as np
from flint import arb, arb_mat, ctx

ctx.prec = 192
BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
RPATH = (
    BASE
    + r"\20261028-h-cat56-2-phase3\metrics\inputs\s14_R_4-5-6-7-8-9-10-11-12-13-14-15_nx250.npz"
)
S8PATH = BASE + r"\20261027-h-cat56-2-discovery\code\s8_admissible_span.py"
sys.path.insert(0, BASE + r"\20261027-h-cat56-2-discovery\code")
import s8_admissible_span as sa  # noqa: E402


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


S = list(range(4, 16))
As = sa.load_A(INST)
R_raw = np.load(RPATH)["R"]
R_HERMITIAN_EXACT = bool(np.array_equal(R_raw, R_raw.conj().T))
FRAC = 0.9
# same float expression as v2 (the diagonal of the average is exactly Re R_ii, so the value is unchanged)
trR_f = float(np.trace(0.5 * (R_raw + R_raw.conj().T)).real)
s_target_f = FRAC * trR_f / 20.0
BX = [np.array(v, complex) for v in ([1, 0], [1j, 0], [0, 1], [0, 1j])]
PHIf = np.array([sa.phi_rows(As, S, x) for x in BX])  # 4 x 36 x 40, exact integers in doubles


def arb_max(a, b):
    """arb enclosure containing max(a, b): (a + b + |a - b|)/2."""
    return (a + b + abs(a - b)) / 2


def arb_min(a, b):
    """arb enclosure containing min(a, b): (a + b - |a - b|)/2."""
    return (a + b - abs(a - b)) / 2


def to_arb_mat(a):
    r, c = a.shape
    return arb_mat(r, c, [arb(float(v)) for v in a.flatten()])


PHI = [to_arb_mat(PHIf[j]) for j in range(4)]


def real_form_of_hermitian_part_arb(Rr):
    """Real 40x40 form [[A, -B], [B, A]] of H = (R + R^H)/2 with A = Re H, B = Im H, all in arb (exact sums)."""
    n = Rr.shape[0]
    re = [
        [(arb(float(Rr[i, j].real)) + arb(float(Rr[j, i].real))) / 2 for j in range(n)]
        for i in range(n)
    ]
    im = [
        [(arb(float(Rr[i, j].imag)) - arb(float(Rr[j, i].imag))) / 2 for j in range(n)]
        for i in range(n)
    ]
    entries = []
    for i in range(2 * n):
        for j in range(2 * n):
            if i < n and j < n:
                entries.append(re[i][j])
            elif i < n:
                entries.append(-im[i][j - n])
            elif j < n:
                entries.append(im[i - n][j])
            else:
                entries.append(re[i - n][j - n])
    return arb_mat(2 * n, 2 * n, entries)


Mb = real_form_of_hermitian_part_arb(R_raw)
M2 = Mb * Mb
I40 = arb_mat(40, 40, [1 if i == j else 0 for i in range(40) for j in range(40)])
tr_exact = sum((arb(float(R_raw[i, i].real)) for i in range(20)), arb(0))
s_target = arb(s_target_f)
final_gap = tr_exact - 20 * s_target  # arb; must be certainly > 0


def np_of(B):
    n, m = B.nrows(), B.ncols()
    return np.array([[float(B[i, j].mid()) for j in range(m)] for i in range(n)])


def lam_max_upper(B):
    """Rigorous arb upper bound for lambda_max of a symmetric arb matrix B.

    Eigenvectors of a float matrix only seed the similarity V; C = V^-1 B V is computed in arb, and Gershgorin
    row bounds on C are enclosures of the eigenvalues of B. The maximum over rows is an arb max.
    """
    n = B.nrows()
    Bf = np_of(B)
    Bf = 0.5 * (Bf + Bf.T)
    _, V = np.linalg.eigh(Bf)
    Vb = to_arb_mat(V)
    C = Vb.inv() * B * Vb
    best = None
    for i in range(n):
        up = (C[i, i] + sum((abs(C[i, j]) for j in range(n) if j != i), arb(0))).upper()
        best = up if best is None else arb_max(best, up)
    return best.upper()


mn_up = arb_max(lam_max_upper(Mb), lam_max_upper(-1 * Mb)).upper()


def contains_zero(x):
    """Certain containment: lower <= 0 <= upper, both arb comparisons (no float conversion)."""
    return bool(x.lower() <= 0) and bool(x.upper() >= 0)


def build_cell(cell):
    """Exact (ball) centre, Phi0, G, pseudo-inverse data, projector P and kernel basis Z0 for one cell."""
    th_lo, th_hi, ph_lo, ph_hi = (float(v) for v in cell)
    a_tl, a_th, a_pl, a_ph = arb(th_lo), arb(th_hi), arb(ph_lo), arb(ph_hi)
    th_c, ph_c = (a_tl + a_th) / 2, (a_pl + a_ph) / 2
    hth, hph = (a_th - a_tl) / 2, (a_ph - a_pl) / 2
    margin = arb("1e-12")  # exact decimal enclosure, positive
    du = (hth / 2 + (a_th / 2).sin() * hph + margin).upper()
    u0 = [(th_c / 2).cos(), arb(0), (th_c / 2).sin() * ph_c.cos(), (th_c / 2).sin() * ph_c.sin()]
    Phi0 = PHI[0] * u0[0]
    for j in range(1, 4):
        Phi0 = Phi0 + PHI[j] * u0[j]
    G = Phi0 * Phi0.transpose()
    Pinv = Phi0.transpose() * G.inv()  # 40 x 36
    P = I40 - Pinv * Phi0
    # the float SVD only seeds the starting vectors; P projects them exactly onto ker Phi0
    u0f = [float(t.mid()) for t in u0]
    Phi0f = sum(u0f[j] * PHIf[j] for j in range(4))
    _, _, Vt = np.linalg.svd(Phi0f)
    Zf = to_arb_mat(Vt[36:].T)
    Z1 = P * Zf
    cols = [[Z1[i, k] for i in range(40)] for k in range(4)]
    Q = []
    for k in range(4):
        v = cols[k][:]
        for q in Q:
            d = sum((q[i] * v[i] for i in range(40)), arb(0))
            v = [v[i] - d * q[i] for i in range(40)]
        nrm = sum((x * x for x in v), arb(0)).sqrt()
        Q.append([x / nrm for x in v])
    Z0 = arb_mat(40, 4, [Q[k][i] for i in range(40) for k in range(4)])
    return {"du": du, "Phi0": Phi0, "G": G, "Pinv": Pinv, "P": P, "Z0": Z0}


def kernel_certificate(Phi0, G, P, Z0):
    """List of failed certificate items (empty = certified). Decisions are arb comparisons only."""
    fails = []
    if not bool(G.det() > 0):
        fails.append("a: det(G) not certified > 0 (Phi0 not certified full row rank 36)")
    R0 = Phi0 * Z0
    if not all(contains_zero(R0[i, k]) for i in range(R0.nrows()) for k in range(R0.ncols())):
        fails.append("b: Phi0*Z0 does not contain 0")
    Gm = Z0.transpose() * Z0
    for i in range(4):
        s = sum((abs(Gm[i, j] - (arb(1) if i == j else arb(0))) for j in range(4)), arb(0))
        if not bool(s.upper() < 1):
            fails.append(
                "c: Gram Z0^T Z0 - I not certified < 1 (columns not certified independent)"
            )
            break
    PP = Phi0 * P
    if not all(contains_zero(PP[i, j]) for i in range(PP.nrows()) for j in range(PP.ncols())):
        fails.append("d: Phi0*P does not contain 0")
    return fails


def gram_defect(Z0):
    """Certified arb upper bound delta >= ||Z0^T Z0 - I||_2 (Gershgorin row sums, arb max)."""
    Gm = Z0.transpose() * Z0
    rows = [
        sum((abs(Gm[i, j] - (arb(1) if i == j else arb(0))) for j in range(4)), arb(0)).upper()
        for i in range(4)
    ]
    d = rows[0]
    for r in rows[1:]:
        d = arb_max(d, r)
    return d.upper()


def cell_bound(cell):
    """Certified bound for one cell: {'status': 'OK', 'B_up': arb, ...} or a failure status."""
    b = build_cell(cell)
    fails = kernel_certificate(b["Phi0"], b["G"], b["P"], b["Z0"])
    if fails:
        return {"status": "CERT_FAIL", "reasons": fails}
    du, Pinv, Z0 = b["du"], b["Pinv"], b["Z0"]
    Z0t = Z0.transpose()
    A = [Pinv * PHI[j] for j in range(4)]
    t_full = [lam_max_upper(A[j].transpose() * A[j]) for j in range(4)]
    t_K = []
    for j in range(4):
        X = A[j] * Z0
        t_K.append(lam_max_upper(X.transpose() * X))
    kappa = (du * sum((t for t in t_full), arb(0)).sqrt()).upper()
    kappa_K = (du * sum((t for t in t_K), arb(0)).sqrt()).upper()
    lam_h = lam_max_upper(Z0t * Mb * Z0)
    lamK = arb_max(lam_h.upper(), arb(0)).upper()  # max(lambda_K, 0) enclosed; no float sign test
    mz = lam_max_upper(Z0t * M2 * Z0).sqrt().upper()
    one_minus = arb(1) - kappa
    if not bool(one_minus > 0):
        return {"status": "KAPPA_GE_1"}
    rho = (kappa_K / one_minus).upper()
    B = (lamK + 2 * mz * rho + mn_up * rho * rho).upper()
    delta = gram_defect(Z0)
    one_minus_delta = arb(1) - delta
    if not bool(one_minus_delta > 0):
        return {
            "status": "CERT_FAIL",
            "reasons": ["c: delta >= 1 (non-orthonormality not controlled)"],
        }
    B_cert = (B / one_minus_delta).upper()
    return {
        "status": "OK",
        "B_up": B_cert,
        "delta": delta,
        "kappa": kappa,
        "rho": rho,
        "lamK": lamK,
        "mz": mz,
    }


CODE_FILES = {
    "interval_cells_v3.py": os.path.abspath(__file__),
    "s8_admissible_span.py": S8PATH,
    "R_input.npz": RPATH,
    "instance.jsonl": INST,
}
