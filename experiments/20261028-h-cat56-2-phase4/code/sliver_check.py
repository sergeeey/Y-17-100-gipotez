"""Coverage check of the parameter-space seams used by the cell certificate (S-, c3d).

For leaves touching theta = float(pi) and leaves touching phi = 2*pi (float), the true seam points
(theta = pi exactly, or phi = 0 = 2*pi) must lie within du of the leaf centre u0, where
  du = h_th/2 + sin(th_hi/2) h_ph + 1e-12   (the same formula as c3d_cell_certificate_adapted.py, line 107).
Reports max |u(seam point) - u0| / du; a value < 1 means the seam point is covered by the lemma (L2).
Usage: python -I sliver_check.py <n_leaves_each> <seed>
"""

import math
import sys

import numpy as np

N = int(sys.argv[1])
SEED = int(sys.argv[2])


def u_of(th, ph):
    return np.array(
        [math.cos(th / 2), 0.0, math.sin(th / 2) * math.cos(ph), math.sin(th / 2) * math.sin(ph)]
    )


def du_of(th_lo, th_hi, ph_lo, ph_hi):
    h_th = 0.5 * (th_hi - th_lo)
    h_ph = 0.5 * (ph_hi - ph_lo)
    return 0.5 * h_th + math.sin(min(th_hi, math.pi) / 2) * h_ph + 1e-12


rng = np.random.default_rng(SEED)
worst_pole = 0.0
worst_seam = 0.0
for _ in range(N):
    # polar leaf: theta_hi = float pi (true pi lies 1.2e-16 beyond the leaf)
    hth = 10 ** rng.uniform(-12, -2)
    hph = 10 ** rng.uniform(-12, -2)
    th_hi = math.pi
    th_lo = th_hi - 2 * hth
    ph_lo = rng.uniform(0, 2 * math.pi)
    ph_hi = ph_lo + 2 * hph
    du = du_of(th_lo, th_hi, ph_lo, ph_hi)
    u0 = u_of(0.5 * (th_lo + th_hi), 0.5 * (ph_lo + ph_hi))
    for ph in np.linspace(ph_lo, ph_hi, 5):
        worst_pole = max(worst_pole, np.linalg.norm(u_of(math.pi, ph) - u0) / du)

    # seam leaf: phi_hi = 2 pi (float), seam point phi = 0 (= 2 pi)
    hth = 10 ** rng.uniform(-12, -2)
    hph = 10 ** rng.uniform(-12, -2)
    th_lo = rng.uniform(0.0, math.pi - 2 * hth)
    th_hi = th_lo + 2 * hth
    ph_hi = 2 * math.pi
    ph_lo = ph_hi - 2 * hph
    du = du_of(th_lo, th_hi, ph_lo, ph_hi)
    u0 = u_of(0.5 * (th_lo + th_hi), 0.5 * (ph_lo + ph_hi))
    for th in np.linspace(th_lo, th_hi, 3):
        worst_seam = max(worst_seam, np.linalg.norm(u_of(th, 0.0) - u0) / du)

print(f"leaves per family: {N}, seed {SEED}")
print(f"max |u(pi,phi)-u0|/du  (polar seam, theta=pi):   {worst_pole:.12f}")
print(f"max |u(theta,0)-u0|/du (phi seam, phi=2pi=0):    {worst_seam:.12f}")
print("covered by L2 (ratio < 1):", worst_pole < 1 and worst_seam < 1)
