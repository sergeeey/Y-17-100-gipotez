"""C1: validate closed-form half-return vs scipy solve_ivp (DOP853, rtol 1e-12)."""
import time, json, numpy as np
from scipy.integrate import solve_ivp
from pwl import *

def slow_half(zone, side, y0, tmax):
    A, b = zone.A, zone.b
    def rhs(t, z): return A @ z + b
    def ev(t, z): return z[0]
    ev.terminal = False
    sol = solve_ivp(rhs, [0, tmax], [0.0, y0], events=ev, method="DOP853",
                    rtol=1e-12, atol=1e-13)
    te, ye = sol.t_events[0], sol.y_events[0]
    m = te > 1e-7
    if not m.any(): return np.nan, np.nan
    i = np.argmax(m)
    return ye[i, 1], te[i]

rng = np.random.default_rng(1)
cases = []
zR, zL = hy_zones(); cases.append(("HY_R", zR, +1)); cases.append(("HY_L", zL, -1))
# round-1 Lienard control: TL=-2,DL=5,aL=aR=0.5,TR=0.5,DR=1.0 ; L zone is x<0, R is x>0
cases.append(("L1_Lz", lienard_zone(-2.0, 5.0, 0.5), -1))
cases.append(("L1_Rz", lienard_zone(0.5, 1.0, 0.5), +1))
for k in range(6):
    # random focus zone with general b, random orientation
    while True:
        A = rng.normal(size=(2, 2)) * 1.2
        tr = A[0,0]+A[1,1]; det = np.linalg.det(A)
        if det > 0.05 and tr**2 < 4*det*0.95 and abs(A[0,1]) > 0.3: break
    b = rng.normal(size=2)
    side = +1 if k % 2 == 0 else -1
    cases.append((f"rand{k}", Zone(A, b), side))

out = []
worst = 0.0
tf = ts = 0.0
for name, z, side in cases:
    # y0 values with side*xdot>0
    yf = -z.b1 / z.a12
    sgn = 1 if side * z.a12 > 0 else -1
    ys = yf + sgn * np.logspace(-2, 1.3, 25)
    t0 = time.time(); y1f, tf_ = z.half_return(side, ys); tf += time.time() - t0
    t0 = time.time()
    y1s = []; tts = []
    tmax = 4 * np.pi / z.w
    for y in ys:
        a_, b_ = slow_half(z, side, y, tmax); y1s.append(a_); tts.append(b_)
    ts += time.time() - t0
    y1s = np.array(y1s); tts = np.array(tts)
    both = np.isfinite(y1f) & np.isfinite(y1s)
    nanmis = int((np.isfinite(y1f) != np.isfinite(y1s)).sum())
    err = np.max(np.abs(y1f[both] - y1s[both]) / np.maximum(1, np.abs(y1s[both]))) if both.any() else np.nan
    errt = np.max(np.abs(tf_[both] - tts[both])) if both.any() else np.nan
    worst = max(worst, err if np.isfinite(err) else 0)
    print(f"{name:7s} side={side:+d} n_both={both.sum():2d}/{len(ys)} nan_mismatch={nanmis} max_rel_err_y1={err:.2e} max_err_t={errt:.2e}", flush=True)
    out.append(dict(name=name, side=side, n_both=int(both.sum()), n=len(ys), nan_mismatch=nanmis, err_y1=float(err), err_t=float(errt)))
print(f"worst rel err {worst:.3e};  fast total {tf:.3f}s vs slow {ts:.3f}s  speedup {ts/max(tf,1e-9):.0f}x")
json.dump(dict(cases=out, worst=worst, t_fast=tf, t_slow=ts), open("validate_fast.json", "w"), indent=1)
