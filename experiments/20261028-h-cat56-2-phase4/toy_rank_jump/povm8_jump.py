import numpy as np, importlib.util, sys
spec=importlib.util.spec_from_file_location("m","rank_jump_check.py")
src=open("rank_jump_check.py").read().split("K0=K(")[0]
exec(src)
E=[np.diag([1,1,0,0,0]).astype(complex)]+[np.outer(e,e).astype(complex) for e in np.eye(d)[ds:]]
def FE(th,jump):
    r=rho(th,jump); F=np.zeros((P,P))
    for Ek in E:
        p=np.real(np.trace(r@Ek)); g=np.array([np.real(np.trace(drho(th,jump,a)@Ek)) for a in range(P)])
        if p>1e-15: F+=np.outer(g,g)/p
    return F
K0=K(np.zeros(P),False); FQ0=sum(N(K0,e) for e in np.eye(d))
h=np.array([1.,0.5,-0.3]); h/=np.linalg.norm(h)
for s in [1e-1,1e-2,1e-3]:
    for jump in [False,True]:
        F=FE(s*h,jump); Ks=K(s*h,jump); FQ=sum(N(Ks,e) for e in np.eye(d))
        print(f"s={s:g} jump={jump}: trFE={np.trace(F):.4f} trFQ(s)={np.trace(FQ):.4f} trFQ(0)={np.trace(FQ0):.4f} hFEh={h@F@h:.4f} hFQ0h={h@FQ0@h:.4f}")
