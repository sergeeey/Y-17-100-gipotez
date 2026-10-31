# WHY: contract STAGE_D step 1 (exact completeness) and step 2 (positive weights), in ball arithmetic.
# The 280 vectors and weights are exact binary doubles, so the certificate is for THIS exact candidate.
# Hermitian sum M = sum_k w_k v_k v_k^H is split as Re M = sum w (a a^T + b b^T),
# Im M = sum w (b a^T - a b^T) with v = a + i b; all in arb, prec 192 bits.
import json
import numpy as np
from flint import arb, arb_mat, ctx

ctx.prec = 192
P = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz"
z = np.load(P)
w = z["weights"]
V = z["vectors"]
K, d = V.shape  # 280, 22
a = V.real
b = V.imag

ReM = [[arb(0)] * d for _ in range(d)]
ImM = [[arb(0)] * d for _ in range(d)]
for k in range(K):
    wk = arb(float(w[k]))
    for i in range(d):
        ai, bi = float(a[k, i]), float(b[k, i])
        for j in range(d):
            aj, bj = float(a[k, j]), float(b[k, j])
            ReM[i][j] += wk * (arb(ai) * arb(aj) + arb(bi) * arb(bj))
            ImM[i][j] += wk * (arb(bi) * arb(aj) - arb(ai) * arb(bj))

# residual R = M - I: real part diagonal minus 1, imaginary part as is
max_rad_re = arb(0)
max_rad_im = arb(0)
max_mid = 0.0
for i in range(d):
    for j in range(d):
        r = ReM[i][j] - (arb(1) if i == j else arb(0))
        m = ImM[i][j]
        max_rad_re = max(max_rad_re, r.rad()) if False else max_rad_re
        rr = float(abs(r).upper())
        mi = float(abs(m).upper())
        max_mid = max(max_mid, rr, mi)
        if float(r.rad()) > float(max_rad_re.upper()):
            max_rad_re = r.rad()
        if float(m.rad()) > float(max_rad_im.upper()):
            max_rad_im = m.rad()

# certified upper bound on max_ij |residual| (sup over entries of upper bound of abs)
cert_upper = 0.0
covers_zero = True
for i in range(d):
    for j in range(d):
        r = ReM[i][j] - (arb(1) if i == j else arb(0))
        m = ImM[i][j]
        cert_upper = max(cert_upper, float(abs(r).upper()), float(abs(m).upper()))
        if not (float(r.lower()) <= 0.0 <= float(r.upper())):
            covers_zero = False
        if not (float(m.lower()) <= 0.0 <= float(m.upper())):
            covers_zero = False

w_min = float(w.min())
w_min_lo = min(float(arb(float(x)).lower()) for x in w)
print("K =", K, "d =", d)
print("covers zero (all entries of Re/Im residual):", covers_zero)
print("certified upper bound on max |residual| entry:", cert_upper)
print("w_min (exact double):", w_min)
print("all weights strictly positive as exact doubles:", bool(np.all(w > 0)))
print("criterion: certified residual < w_min ->", cert_upper < w_min)
print("ratio cert_upper / w_min:", cert_upper / w_min)
out = {
    "K": K, "d": d, "prec_bits": 192,
    "covers_zero": covers_zero,
    "cert_upper_max_abs_residual": cert_upper,
    "w_min": w_min,
    "weights_all_positive": bool(np.all(w > 0)),
    "criterion_residual_lt_wmin": bool(cert_upper < w_min),
}
with open(r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261028-h-cat56-2-phase4\stage_d\metrics_completeness.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
