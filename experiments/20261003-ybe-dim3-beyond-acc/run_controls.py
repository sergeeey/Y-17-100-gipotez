"""Positive / negative controls for the YBE toolkit (claim.md control list). Run: python run_controls.py"""

import numpy as np
from ybe import *

rng = np.random.default_rng(12345)
lines = []


def log(s=""):
    print(s, flush=True)
    lines.append(s)


# ---- 0. Jacobian finite-difference check ------------------------------------------------
N = 3
R0 = rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))
J = jac_F(R0, N)
d = rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))
eps = 1e-6
fd = (braid_residual(R0 + eps * d, N) - braid_residual(R0 - eps * d, N)).reshape(-1) / (2 * eps)
an = J @ d.reshape(-1)
log(
    "[C0] Jacobian check (random R0, random direction): rel err = %.2e"
    % (np.linalg.norm(fd - an) / np.linalg.norm(an))
)

# ---- 1. braid form <-> vertex form equivalence ------------------------------------------
fams = table1_families(rng)
name0 = list(fams)[0]
Rch = fams[name0]
Rv = flip(3) @ Rch  # R_YBE = P * check-R  (P^2=1)
log(
    "[C1] braid residual (family I): %.2e ; vertex-form residual R=P*checkR: %.2e"
    % (np.linalg.norm(braid_residual(Rch, 3)), np.linalg.norm(ybe_residual_R(Rv, 3)))
)
Rp = Rch + 0.3 * rng.normal(size=(9, 9))
log(
    "     perturbed (negative): braid %.2e ; vertex %.2e  (both must be O(1))"
    % (np.linalg.norm(braid_residual(Rp, 3)), np.linalg.norm(ybe_residual_R(flip(3) @ Rp, 3)))
)

# ---- 2. POSITIVE control: all Table-1 families ------------------------------------------
log(
    "\n[C2] Table-1 families of arXiv:2310.03816, random params (rel. residual ||F||/||R||^3, |det R|, dimL, cc-class)"
)
worst = 0
bad = []
for name, R in fams.items():
    r = rel_res(R, 3)
    cc = cc_class(R, 3)
    det = abs(np.linalg.det(R))
    ok = r < 1e-12
    if not ok:
        bad.append(name)
    worst = max(worst, r)
    log(
        "   %-26s res=%.2e  |det|=%.2e  dimL=%d  %s  %s"
        % (name, r, det, cc["dimL"], cc["label"], "" if ok else "<<< FAIL")
    )
log(
    "   worst residual among %d families = %.2e ; failing: %s"
    % (len(fams), worst, bad if bad else "none")
)

# ---- 3. NEGATIVE control: random matrices and parameter-violating perturbations ---------
log("\n[C3] negative controls")
res_rand = [rel_res(rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9)), 3) for _ in range(200)]
log("   200 random complex 9x9: min rel residual = %.3e (must be >> 1e-12)" % min(res_rand))
for name, R in list(fams.items())[:6]:
    Rp = R.copy()
    Rp[2, 2] += 0.05  # break one entry
    log("   %-26s perturbed entry (2,2)+=0.05 -> res=%.2e" % (name, rel_res(Rp, 3)))

# ---- 4. dim-2: Hietarinta families (as printed in arXiv:2409.05375) -------------------------
log("\n[C4] Hietarinta dim-2 families (braided form) residual / invariants")
hf = hiet_families(rng)
for name, R in hf.items():
    r = rel_res(R, 2)
    cc = cc_class(R, 2)
    td, _ = tangent_dim(R, 2)
    log(
        "   %-9s res=%.2e |det|=%.2e dimL=%d %-9s tangent=%d"
        % (name, r, abs(np.linalg.det(R)), cc["dimL"], cc["label"], td)
    )

# ---- 5. conjugation invariance of the L-test; Gaussian (known non-CC) solution -------------
log("\n[C5] L-test: invariance under local conjugation + known cases")
g = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
GG = np.kron(g, g)
for name in ["I   generic (b-branch 0)", "V.2.1", "VI.2.2 w=w"]:
    R = fams[name]
    Rc = GG @ R @ np.linalg.inv(GG)
    log(
        "   %-26s orig: dimL=%d %s | conj by random g(x)g: res=%.1e dimL=%d %s"
        % (
            name,
            cc_class(R, 3)["dimL"],
            cc_class(R, 3)["label"],
            rel_res(Rc, 3),
            cc_class(Rc, 3)["dimL"],
            cc_class(Rc, 3)["label"],
        )
    )
w = np.exp(2j * np.pi / 3)
Xm = np.roll(np.eye(3), 1, axis=0)  # X e_j = e_{j+1}
Zm = np.diag([w**j for j in range(3)])
PS = np.kron(Xm, Zm)
G1 = (np.eye(9) + w * (PS + PS @ PS)) / np.sqrt(3)
eta = np.exp(1j * np.pi / 6)
x = -eta / np.sqrt(3)
y = 1 + x
G2 = x * np.eye(9) + y * PS + y * PS @ PS
log(
    "   Gaussian (1/sqrt3)(I + w(P+P^2)), P=X(x)Z: res=%.2e dimL=%d %s   [2609.38290: only scalar M => expect U1-free]"
    % (rel_res(G1, 3), cc_class(G1, 3)["dimL"], cc_class(G1, 3)["label"])
)
log(
    "   Gaussian x I + y P + y P^2 (x=-eta/sqrt3, y=1+x): res=%.2e dimL=%d %s"
    % (rel_res(G2, 3), cc_class(G2, 3)["dimL"], cc_class(G2, 3)["label"])
)
Pf = flip(3).astype(complex)
log(
    "   flip P (dim3): res=%.2e dimL=%d %s (expect dimL=9)"
    % (rel_res(Pf, 3), cc_class(Pf, 3)["dimL"], cc_class(Pf, 3)["label"])
)
Id = np.eye(9, dtype=complex)
log("   identity: res=%.2e dimL=%d" % (rel_res(Id, 3), cc_class(Id, 3)["dimL"]))

open("controls_output.txt", "w", encoding="utf-8").write("\n".join(lines))
