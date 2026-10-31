"""Direct check of the 280-element S+ POVM (independent of phi_rows / earlier splus_numerical_check):
 (1) completeness sum_w w |v><v| = I_22
 (2) per-vector direct equation A_i^dag y - lambda_i x = 0 with lambda_i = Re(x^dag w_i)/|x|^2, residual relative to scale
 (3) how many (vector, i) pairs have lambda_i ~ 0 (i.e. w_i = A_i^dag y ~ 0), judged against the residual scale
 (4) F^C vs F^Q computed from probabilities: p = w <v|rho|v>, dp_i = w <v|drho_i|v>, F^C = sum dp_i dp_j / p
Layout assumption (checked below): v = (x in C^2 ; y in C^20), rho = diag(1/3,2/3) + 0, L_i = [[0,A_i^dag],[A_i,0]].
"""

import json

import numpy as np

BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
POVM = BASE + r"\20261028-h-cat56-2-phase3\metrics\inputs\s14_povm_prefix12.npz"
S = list(range(12))

rec = json.loads(open(INST, encoding="utf-8").readline())
A = []
for flat in rec["blocks"]:
    re = np.array([[flat[2 * r + a] for a in range(2)] for r in range(20)], float)
    im = np.array([[flat[40 + 2 * r + a] for a in range(2)] for r in range(20)], float)
    A.append(-2j * (re + 1j * im))

d = np.load(POVM)
w, V = d["weights"], d["vectors"]
n = len(w)
rho = np.zeros((22, 22), complex)
rho[0, 0], rho[1, 1] = 1 / 3, 2 / 3

# (1) completeness
E = sum(w[k] * np.outer(V[k], V[k].conj()) for k in range(n))
print("n", n, " w min/max", w.min(), w.max(), " |sum E - I|max", np.abs(E - np.eye(22)).max())

# (2)/(3) direct equation
xn = np.linalg.norm(V[:, :2], axis=1)
yn = np.linalg.norm(V[:, 2:], axis=1)
print(
    "norm |x| min/max",
    xn.min(),
    xn.max(),
    " |y| min/max",
    yn.min(),
    yn.max(),
    " #(|x|<1e-6):",
    int((xn < 1e-6).sum()),
)
resid_rel = []
rel_w = []
lam_all = []
ny0 = 0
ny0_w = 0.0
for k in range(n):
    x, y = V[k, :2], V[k, 2:]
    if np.linalg.norm(x) < 1e-6:
        continue
    if np.linalg.norm(y) < 1e-12:
        ny0 += 1
        ny0_w += w[k]
        continue
    for i in S:
        wi = A[i].conj().T @ y
        lam = (x.conj() @ wi).real / (x.conj() @ x).real
        r = np.linalg.norm(wi - lam * x)
        scale = np.linalg.norm(y) * np.linalg.norm(A[i], 2)
        resid_rel.append(r / scale)
        rel_w.append(np.linalg.norm(wi) / scale)
        lam_all.append(lam)
print("vectors with y = 0 (support-only, all lambda_i = 0 exactly):", ny0, " total weight", ny0_w)
yq = np.sort(yn[yn > 1e-12])
print(
    "smallest nonzero |y|:", yq[:3], " count 0<|y|<1e-3:", int(((yn > 1e-12) & (yn < 1e-3)).sum())
)
resid_rel = np.array(resid_rel)
rel_w = np.array(rel_w)
print(
    "direct residual |A_i^dag y - lam_i x| / (|y| ||A_i||): max",
    resid_rel.max(),
    " median",
    np.median(resid_rel),
)
print(
    "size of A_i^dag y relative to |y| ||A_i||: min",
    rel_w.min(),
    " 1%-quantile",
    np.quantile(rel_w, 0.01),
    " median",
    np.median(rel_w),
)
for thr in (1e-8, 1e-6, 1e-4, 1e-3, 1e-2):
    print(
        f"  pairs (vector,i) with |A_i^dag y| <= {thr:g} * scale:",
        int((rel_w <= thr).sum()),
        "of",
        len(rel_w),
    )


# (4) classical vs quantum Fisher information, computed independently from probabilities
def drho(i):
    L = np.zeros((22, 22), complex)
    L[:2, 2:] = A[i].conj().T
    L[2:, :2] = A[i]
    return (L @ rho + rho @ L) / 2, L


dr, Ls = zip(*[drho(i) for i in S])
FC = np.zeros((12, 12))
for k in range(n):
    v = V[k]
    p = w[k] * (v.conj() @ rho @ v).real
    dp = np.array([w[k] * (v.conj() @ dr[a] @ v).real for a in range(12)])
    if p > 1e-14:
        FC += np.outer(dp, dp) / p
    else:
        print("null-type element", k, "p", p, "max|dp|", np.abs(dp).max())
FQ = np.array([[np.trace(rho @ Ls[a] @ Ls[b]).real for b in range(12)] for a in range(12)])
Dm = FQ - FC
print("max|FQ|", np.abs(FQ).max(), " max|FC-FQ|/max|FQ|", np.abs(Dm).max() / np.abs(FQ).max())
ev = np.linalg.eigvalsh(0.5 * (Dm + Dm.T))
print("eig(FQ-FC) min/max", ev[0], ev[-1], " min eig FQ", np.linalg.eigvalsh(FQ)[0])
