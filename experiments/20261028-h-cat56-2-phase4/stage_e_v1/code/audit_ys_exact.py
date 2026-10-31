# WHY: independent exact audit of the POVM-vector subspace Y_S+(x_j) used by the S+ certificate.
# Re-derives the membership condition from its definition, NOT from ys_space.py / exact_cert.py:
#   y in Y_S(x)  <=>  for every i in S: A_i^dagger y = lambda_i * x  with lambda_i real.
# Exact arithmetic (fractions.Fraction) throughout. Reads:
#   - instance blocks (floats converted exactly via Fraction(float)), same A_i convention as ys_space.py
#   - exact basis vectors and directions from logs/exact_bases2.pkl
# Also records whether each direction is an exact unit vector (informational; the membership test
# below does not depend on normalisation, since {x, x_perp} is orthogonal for any nonzero x).
import json
import os
import pickle
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
INST = (
    r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
    r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
)
S_PLUS = list(range(12))


def F(v):
    if isinstance(v, Fraction):
        return v
    if isinstance(v, float):
        return Fraction(v)  # exact binary value
    return Fraction(str(v))


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cconj(a):
    return (a[0], -a[1])


# --- instance: A_i = 2*im - 2i*re, re/im read as in ys_space.load_A (flat[2r+a], flat[40+2r+a]) ---
rec = json.loads(open(INST, encoding="utf-8").readline())
A = {}
for i in S_PLUS:
    flat = [F(v) for v in rec["blocks"][i]]
    assert len(flat) == 80, len(flat)
    Ai = [[None, None] for _ in range(20)]
    for r in range(20):
        for a in range(2):
            re_ = flat[2 * r + a]
            im_ = flat[40 + 2 * r + a]
            Ai[r][a] = (2 * im_, -2 * re_)  # 2*im - 2i*re
    A[i] = Ai

# --- exact directions and bases ---
D = pickle.load(open(os.path.join(STAGE, "logs", "exact_bases2.pkl"), "rb"))
dirs = D["dirs"]
bases = D["bases_exact"]
J = len(dirs)

report = {
    "instance_file_used": INST,
    "n_directions": J,
    "n_basis_vectors_total": 0,
    "membership_failures": 0,
    "unit_norm_directions": 0,
    "first_failure": None,
}

for j in range(J):
    (a0r, a0i), (a1r, a1i) = dirs[j]
    x = [(F(a0r), F(a0i)), (F(a1r), F(a1i))]
    nx = cadd(cmul(x[0], cconj(x[0])), cmul(x[1], cconj(x[1])))[0]
    if nx == 1:
        report["unit_norm_directions"] += 1
    m = len(bases[j])
    for v in range(m):
        report["n_basis_vectors_total"] += 1
        # y[r] = (re, im) of component r of basis vector v; bases[j][v][r] = (re, im)
        y = [(F(bases[j][v][r][0]), F(bases[j][v][r][1])) for r in range(20)]
        for i in S_PLUS:
            # u_alpha = sum_r conj(A_i[r][alpha]) * y_r   (A_i^dagger y)
            u = []
            for al in range(2):
                acc = (Fraction(0), Fraction(0))
                for r in range(20):
                    acc = cadd(acc, cmul(cconj(A[i][r][al]), y[r]))
                u.append(acc)
            # parallel to x:  u0*x1 - u1*x0 = 0
            cross = cadd(cmul(u[0], x[1]), (-cmul(u[1], x[0])[0], -cmul(u[1], x[0])[1]))
            # real lambda:  Im(x^dagger u) = 0
            xh_u = cadd(cmul(cconj(x[0]), u[0]), cmul(cconj(x[1]), u[1]))
            ok = cross == (0, 0) and xh_u[1] == 0
            if not ok:
                report["membership_failures"] += 1
                if report["first_failure"] is None:
                    report["first_failure"] = {"direction": j, "basis": v, "constraint_i": i}
                break

report["membership_exact_pass"] = report["membership_failures"] == 0
out_path = os.path.join(STAGE, "logs", "audit_ys_exact.json")
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=1, ensure_ascii=False)
print(json.dumps(report, indent=1, ensure_ascii=False), flush=True)
sys.exit(0 if report["membership_exact_pass"] else 1)
