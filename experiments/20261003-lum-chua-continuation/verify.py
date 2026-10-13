"""Independent verification of a claimed crossing limit cycle (no use of pwl.py closed form).
Method A: scipy.linalg.expm + scipy.optimize.fsolve on the 3 unknowns (tR, tL, y0) with
          unknown-time formulation (Llibre-Ponce eq. (2) style): x_R(tR)=0, x_L(tL)=0, y_L(tL)=y0.
Method B: DOP853 simulation of the full piecewise system (rtol 1e-13), event-based, from (0,y0)
          over one period; reports closure error and the x'-signs at both crossings (transversality).
Systems are given as (A_R,b_R,A_L,b_L) in coordinates where the line is x=0."""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp

def flow(A, b, z0, t):
    # z' = A z + b  ->  augmented matrix exponential (no inverse of A needed)
    M = np.zeros((3, 3)); M[:2, :2] = A; M[:2, 2] = b
    E = expm(M * t)
    return E[:2, :2] @ z0 + E[:2, 2]

def method_A(AR, bR, AL, bL, y0, tR0, tL0):
    def F(u):
        tR, tL, y = u
        zr = flow(AR, bR, np.array([0.0, y]), tR)
        zl = flow(AL, bL, np.array([0.0, zr[1]]), tL)
        return [zr[0], zl[0], zl[1] - y]
    sol, info, ier, msg = fsolve(F, [tR0, tL0, y0], full_output=True, xtol=1e-14)
    return sol, np.max(np.abs(F(sol))), ier

def method_B(AR, bR, AL, bL, y0, tmax=200.0):
    def rhs(t, z):
        return (AR @ z + bR) if z[0] > 0 else (AL @ z + bL)
    def ev(t, z): return z[0]
    ev.terminal = False
    sol = solve_ivp(rhs, [0, tmax], [1e-12, y0], events=ev, method="DOP853", rtol=1e-13, atol=1e-14,
                    max_step=0.05)
    te, ye = sol.t_events[0], sol.y_events[0]
    # starting point sits at x=1e-12 inside R; crossings: 1st (R->L), 2nd (L->R) = one period
    return te, ye

def verify_cycle(AR, bR, AL, bL, y0, tR0, tL0):
    sol, res, ier = method_A(AR, bR, AL, bL, y0, tR0, tL0)
    tR, tL, y = sol
    zr = flow(AR, bR, np.array([0.0, y]), tR)
    y1 = zr[1]
    # transversality: x' on the line at the 2 crossing points, in both zones
    xd = lambda A, b, yy: A[0, 1] * yy + b[0]
    trans = dict(R_at_y0=xd(AR, bR, y), L_at_y0=xd(AL, bL, y), R_at_y1=xd(AR, bR, y1), L_at_y1=xd(AL, bL, y1))
    ok = (trans["R_at_y0"] > 0 and trans["L_at_y0"] > 0 and trans["R_at_y1"] < 0 and trans["L_at_y1"] < 0)
    # also confirm first-return property: x_R(t)>0 on (0,tR), x_L(t)<0 on (0,tL)
    ts = np.linspace(1e-9, 1, 2000)
    xr = np.array([flow(AR, bR, np.array([0.0, y]), tR * s)[0] for s in ts[:-1]])
    xl = np.array([flow(AL, bL, np.array([0.0, y1]), tL * s)[0] for s in ts[:-1]])
    first_return = bool((xr > -1e-12).all() and (xl < 1e-12).all())
    te, ye = method_B(AR, bR, AL, bL, y)
    closure = None
    if len(te) >= 2:
        closure = float(abs(ye[1, 1] - y))
    return dict(tR=tR, tL=tL, y0=y, y1=y1, resA=res, ier=ier, transversal=ok, trans=trans,
                first_return=first_return, simB_events=len(te), simB_closure=closure,
                simB_period=float(te[1] - te[0]) if len(te) >= 2 else None, tR_plus_tL=tR + tL)

if __name__ == "__main__":
    from pwl import HY_AP, HY_AM, hy_zones
    zR, zL = hy_zones()
    for (y0, tR, tL) in [(0.16382622762708182, 3.9178, 6.2201), (-0.0889140809428, 8.5668, 5.0431),
                         (-0.4860616491266, 14.8663, 4.6014)]:
        r = verify_cycle(zR.A, zR.b, zL.A, zL.b, y0, tR, tL)
        print({k: (round(v, 12) if isinstance(v, float) else v) for k, v in r.items() if k != 'trans'}, r["trans"])
