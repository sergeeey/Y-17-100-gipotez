"""O3 v2 (certified): rigorous ball-arithmetic bound for S- cells, with an explicit kernel certificate.

Relative to code/interval_cells.py (v1) the bound formulas are unchanged (including the upper-bound
rule for lambda_K). New: every cell must pass the kernel certificate before its bound is used.

Kernel certificate (all checks in arb, 192 bit; inputs exact: integers, float64 R and cell edges):
  (a) det(G) > 0 with G = Phi0 Phi0^T            -> Phi0 has full row rank 36 -> dim ker Phi0 = 4
  (b) Phi0 * Z0 contains 0 entrywise             -> columns of Z0 lie in ker Phi0 (exact u0 enclosed)
  (c) Gershgorin on Z0^T Z0 - I: row sums < 1    -> columns of Z0 are linearly independent
  (d) Phi0 * P contains 0 entrywise              -> P annihilates the row space of Phi0
(a)+(b)+(c) make Z0 a basis of ker Phi0. P is the exact orthogonal projector onto ker Phi0 because
P = I - Phi0^T G^-1 Phi0 is built from the exact Phi0 by arb operations, and arb enclosures contain the
exact values (inclusion isotonicity). The float SVD only supplies the starting vectors Zf; P projects
them exactly, so no float kernel enters the bound.

A failed certificate returns status CERT_FAIL with the failed items. It is never skipped.
Not checked here: the cell lemma (perturbation inequality) and the cone reduction (math, see PHASE3).
"""

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
sys.path.insert(0, BASE + r"\20261027-h-cat56-2-discovery\code")
import s8_admissible_span as sa  # noqa: E402

S = list(range(4, 16))
As = sa.load_A(INST)
R_raw = np.load(RPATH)["R"]
R_HERMITIAN_EXACT = bool(np.array_equal(R_raw, R_raw.conj().T))
# WHY: R is symmetrised in arb (below), not in float: the stored file is Hermitian only up to ~5e-17
R = 0.5 * (
    R_raw + R_raw.conj().T
)  # float copy: only for trR_f (s_target is re-checked in arb via final_gap)
FRAC = 0.9
trR_f = float(np.trace(R).real)
s_target_f = FRAC * trR_f / 20.0  # same float ops as the certificate
BX = [np.array(v, complex) for v in ([1, 0], [1j, 0], [0, 1], [0, 1j])]
PHIf = np.array([sa.phi_rows(As, S, x) for x in BX])  # 4 x 36 x 40, exact integers in doubles


def to_arb_mat(a):
    r, c = a.shape
    return arb_mat(r, c, [arb(float(v)) for v in a.flatten()])


PHI = [to_arb_mat(PHIf[j]) for j in range(4)]


def real_form_of_hermitian_part_arb(Rr):
    """Real 40x40 form [[A, -B], [B, A]] of H = (R + R^H)/2 with A = Re H, B = Im H, all in arb.

    Re H_ij = (Re R_ij + Re R_ji)/2,  Im H_ij = (Im R_ij - Im R_ji)/2. Exact sums of doubles in ball arithmetic,
    so the enclosure contains the exact Hermitian part of the file's R (no float rounding).
    """
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
tr_exact = sum((arb(float(R[i, i].real)) for i in range(20)), arb(0))
s_target = arb(s_target_f)
final_gap = tr_exact - 20 * s_target  # must be > 0 for the Phase-3 criterion


def np_of(B):
    n, m = B.nrows(), B.ncols()
    return np.array([[float(B[i, j].mid()) for j in range(m)] for i in range(n)])


def lam_max_upper(B):
    """Rigorous upper bound (arb) for lambda_max of a symmetric arb matrix B (Gershgorin on V^-1 B V)."""
    n = B.nrows()
    Bf = np_of(B)
    Bf = 0.5 * (Bf + Bf.T)
    _, V = np.linalg.eigh(Bf)
    Vb = to_arb_mat(V)
    C = Vb.inv() * B * Vb
    best = None
    for i in range(n):
        up = (C[i, i] + sum((abs(C[i, j]) for j in range(n) if j != i), arb(0))).upper()
        if best is None or float(up) > float(best):
            best = up
    return best


mn_up = max(lam_max_upper(Mb), lam_max_upper(-1 * Mb), key=lambda t: float(t))


def lo(x):
    return float(x.lower())


def hi(x):
    return float(x.upper())


def contains_zero(x):
    # NaN (indeterminate ball) makes both comparisons False, so it is rejected
    return lo(x) <= 0.0 <= hi(x)


def build_cell(cell):
    """Exact (ball) centre, Phi0, G, pseudo-inverse data, projector P and kernel basis Z0 for one cell."""
    th_lo, th_hi, ph_lo, ph_hi = (float(v) for v in cell)
    a_tl, a_th, a_pl, a_ph = arb(th_lo), arb(th_hi), arb(ph_lo), arb(ph_hi)
    th_c, ph_c = (a_tl + a_th) / 2, (a_pl + a_ph) / 2
    hth, hph = (a_th - a_tl) / 2, (a_ph - a_pl) / 2
    du = (hth / 2 + (a_th / 2).sin() * hph + arb(1e-12)).upper()
    u0 = [(th_c / 2).cos(), arb(0), (th_c / 2).sin() * ph_c.cos(), (th_c / 2).sin() * ph_c.sin()]
    Phi0 = PHI[0] * u0[0]
    for j in range(1, 4):
        Phi0 = Phi0 + PHI[j] * u0[j]
    G = Phi0 * Phi0.transpose()
    Pinv = Phi0.transpose() * G.inv()  # 40 x 36
    P = I40 - Pinv * Phi0
    # WHY: the float SVD only seeds the starting vectors; P projects them exactly onto ker Phi0
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
    """Return the list of failed certificate items (empty list = certified). Checks (a)-(d) in the module docstring."""
    fails = []
    d = G.det()
    if not (lo(d) > 0.0):
        fails.append("a: det(G) not certified > 0 (Phi0 not certified full row rank 36)")
    R0 = Phi0 * Z0
    if not all(contains_zero(R0[i, k]) for i in range(R0.nrows()) for k in range(R0.ncols())):
        fails.append("b: Phi0*Z0 does not contain 0 (columns not certified in kernel)")
    Gm = Z0.transpose() * Z0
    for i in range(4):
        s = sum(
            (hi(abs(Gm[i, j] - (arb(1) if i == j else arb(0)))) for j in range(4)),
            0.0,
        )
        if not (s < 1.0):
            fails.append(
                "c: Gram Z0^T Z0 - I not certified < 1 (columns not certified independent)"
            )
            break
    PP = Phi0 * P
    if not all(contains_zero(PP[i, j]) for i in range(PP.nrows()) for j in range(PP.ncols())):
        fails.append("d: Phi0*P does not contain 0 (projector not certified)")
    return fails


def gram_defect(Z0):
    """Certified upper bound (arb) delta >= ||Z0^T Z0 - I||_2, via Gershgorin row sums in ball arithmetic.

    WHY: Z0 = Z* T with Z* an exact orthonormal kernel basis, T = Z*^T Z0, T^T T = I + E, ||E|| <= delta.
    Then ||T^-1||^2 <= 1/(1 - delta), and every quantity of the bound (lambda_K, ||M Z||, kappa_K) computed
    from Z0 is at most 1/(1 - delta) times the exact value; hence B_true <= B_code / (1 - delta).
    """
    Gm = Z0.transpose() * Z0
    rows = [
        sum((abs(Gm[i, j] - (arb(1) if i == j else arb(0))) for j in range(4)), arb(0)).upper()
        for i in range(4)
    ]
    d = rows[0]
    for r in rows[1:]:
        if float(r) > float(d):
            d = r
    return d


def cell_bound(cell):
    """Certified bound for one cell: {'status': 'OK', 'B_up': arb, ...} or {'status': 'CERT_FAIL'|'KAPPA_GE_1', ...}."""
    b = build_cell(cell)
    fails = kernel_certificate(b["Phi0"], b["G"], b["P"], b["Z0"])
    if fails:
        return {"status": "CERT_FAIL", "reasons": fails}
    du, Pinv, Z0 = b["du"], b["Pinv"], b["Z0"]
    Z0t = Z0.transpose()
    A = [Pinv * PHI[j] for j in range(4)]  # 40 x 40
    t_full = [lam_max_upper(A[j].transpose() * A[j]) for j in range(4)]
    t_K = []
    for j in range(4):
        X = A[j] * Z0
        t_K.append(lam_max_upper(X.transpose() * X))
    kappa = (du * sum((t for t in t_full), arb(0)).sqrt()).upper()
    kappa_K = (du * sum((t for t in t_K), arb(0)).sqrt()).upper()
    lam_h = lam_max_upper(Z0t * Mb * Z0)
    # WHY: the test must use the UPPER bound of lambda_K, not its midpoint; max(lambda_K, 0) <= max(upper, 0)
    lam_up = lam_h.upper()
    lamK = lam_up if float(lam_up) > 0 else arb(0)
    mz = lam_max_upper(Z0t * M2 * Z0).sqrt().upper()
    one_minus = arb(1) - kappa
    if not (one_minus > 0):
        return {"status": "KAPPA_GE_1"}
    rho = (kappa_K / one_minus).upper()
    B = (lamK + 2 * mz * rho + mn_up * rho * rho).upper()
    delta = gram_defect(Z0)
    one_minus_delta = arb(1) - delta
    if not (one_minus_delta > 0):
        return {
            "status": "CERT_FAIL",
            "reasons": ["c: delta >= 1 (non-orthonormality not controlled)"],
        }
    B_cert = (B / one_minus_delta).upper()  # certified bound for an exact orthonormal kernel basis
    return {
        "status": "OK",
        "B_up": B_cert,
        "B_code": B,
        "delta": delta,
        "kappa": kappa,
        "rho": rho,
        "lamK": lamK,
        "mz": mz,
    }
