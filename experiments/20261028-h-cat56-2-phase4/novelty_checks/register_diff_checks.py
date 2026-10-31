"""OB-1 spot checks for claims of the ChatGPT register that are not in FULL_RESULTS_REGISTER_VERIFIED.md.

P07: A_14^H A_15 = [[136, 144i], [-144i, -132]] (Hermitian) for the pair (14, 15).
N08: for E = {I2 (+) 0, 0 (+) I20} all of F^Q sits in the kernel outcome (N_k = Re tr(E_k L_a rho L_b),
     with L_a = [[0, A_a^H], [A_a, L_kk]], rho = Q (+) 0 at theta = 0).
"""

import sys

import numpy as np

BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
sys.path.insert(0, BASE + r"\20261027-h-cat56-2-discovery\code")
import s8_admissible_span as sa  # noqa: E402

INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
As = sa.load_A(INST)
Q = np.diag([1 / 3, 2 / 3])

M = As[14].conj().T @ As[15]
print("A_14^H A_15 =")
print(np.array2string(M, precision=6))
print("Hermitian defect:", float(np.abs(M - M.conj().T).max()))
print(
    "Claimed [[136,144j],[-144j,-132]]:",
    bool(np.allclose(M, np.array([[136, 144j], [-144j, -132]]))),
)

# N08: build L_a at theta = 0 with L_kk = 0 and compare the two-outcome N_k with F^Q
rng = np.random.default_rng(0)
d = 22
rho = np.zeros((d, d), complex)
rho[:2, :2] = Q
Ls = []
for a in range(16):
    L = np.zeros((d, d), complex)
    L[:2, 2:] = As[a].conj().T
    L[2:, :2] = As[a]
    Ls.append(L)
FQ = np.array(
    [[np.real(np.trace(Q @ As[a].conj().T @ As[b])) for b in range(16)] for a in range(16)]
)
for name, E in (
    ("I2+0", np.diag([1.0] * 2 + [0.0] * 20)),
    ("0+I20", np.diag([0.0] * 2 + [1.0] * 20)),
):
    N = np.array(
        [[np.real(np.trace(E @ Ls[a] @ rho @ Ls[b])) for b in range(16)] for a in range(16)]
    )
    print(
        f"N_E[{name}]: trace = {np.trace(N):.6f}, |N - FQ|max = {np.abs(N - FQ).max():.3e}, |N|max = {np.abs(N).max():.3e}"
    )
print(f"tr F^Q (16x16) = {np.trace(FQ):.6f}")
# kernel L_kk perturbation: N for E = 0+I20 must not depend on L_kk
Lk = rng.normal(size=(20, 20)) + 1j * rng.normal(size=(20, 20))
Lk = (Lk + Lk.conj().T) / 2
E = np.diag([0.0] * 2 + [1.0] * 20)
Ls2 = []
for a in range(16):
    L = Ls[a].copy()
    L[2:, 2:] = Lk
    Ls2.append(L)
N2 = np.array(
    [[np.real(np.trace(E @ Ls2[a] @ rho @ Ls2[b])) for b in range(16)] for a in range(16)]
)
N0 = np.array(
    [[np.real(np.trace(E @ Ls[a] @ rho @ Ls[b])) for b in range(16)] for a in range(16)]
)
print(f"with random Hermitian L_kk: |N2 - N(L_kk=0)|max = {np.abs(N2 - N0).max():.3e}; "
      f"|N2 - FQ|max = {np.abs(N2 - FQ).max():.3e} (float residual of the formula)")
print("note: F^Q above is the formula Re tr(Q A_a^H A_b); the N08 identity is therefore partly definitional")
