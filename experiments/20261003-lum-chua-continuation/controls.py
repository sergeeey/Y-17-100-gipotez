"""C3 controls + horizon check."""
import sys, time, json, numpy as np
from multiprocessing import Pool
from scipy.integrate import solve_ivp
from pwl import *

def lien(TL,DL,aL,TR,DR,aR):
    return lienard_zone(TR,DR,aR), lienard_zone(TL,DL,aL)   # (zR, zL)

def one(args):
    TL,DL,aL,TR,DR,aR = args
    zR,zL = lien(*args)
    r = count_cycles(zR,zL,n=2500,dmin=1e-5,dmax=300.0)
    return r["n_sign_changes"], r["ambiguous_gaps"]

if __name__=="__main__":
    # 1. round-1 positive control
    zR,zL = lien(-2.0,5.0,0.5,0.5,1.0,0.5)
    r = count_cycles(zR,zL,n=6000,dmin=1e-5,dmax=300.0)
    print("round-1 positive control: n=",r["n_sign_changes"],[ (x['y0'],x['y1']) for x in r['roots']],"(expect y_Lentry=y1~2.887683)",flush=True)
    # 2. horizon check: for y0 where fast says NaN, does the slow solver find a return up to 12pi/w ?
    zR,zL = hy_zones()
    nb=0; found=0
    for z,side in ((zR,1),(zL,-1)):
        yf=-z.b1/z.a12; sgn=1 if side*z.a12>0 else -1
        ys=yf+sgn*np.logspace(-3,1.5,40)
        y1,_=z.half_return(side,ys)
        for y,yy in zip(ys,y1):
            if np.isfinite(yy): continue
            nb+=1
            sol=solve_ivp(lambda t,s:z.A@s+z.b,[0,12*np.pi/z.w],[0,y],events=lambda t,s:s[0],rtol=1e-11,atol=1e-12,method="DOP853")
            if (sol.t_events[0]>1e-7).any(): found+=1
    print(f"horizon check HY: {nb} NaN starts, {found} have a return within 12pi/w (rest truly never return)",flush=True)
    rng=np.random.default_rng(7)
    def draw(sign_ok):
        while True:
            TL=-rng.uniform(0.05,2.5); TR=rng.uniform(0.05,2.5)
            if not sign_ok: TR=-TR
            DL=TL**2/4+rng.uniform(0.02,4); DR=TR**2/4+rng.uniform(0.02,4)
            a=rng.uniform(-6,6)
            return (TL,DL,a,TR,DR,a)
    cont=[draw(True) for _ in range(800)]
    same=[draw(False) for _ in range(300)]
    t=time.time()
    with Pool(6) as p:
        rc=p.map(one,cont,chunksize=10); rs=p.map(one,same,chunksize=10)
    cc=np.array([x[0] for x in rc]); cs=np.array([x[0] for x in rs])
    print("continuous scan (a_L=a_R), T_L T_R<0: counts histogram",np.bincount(cc),"max",cc.max(),"ambig gaps total",sum(x[1] for x in rc),flush=True)
    print("same-sign traces scan (T_L T_R>0): counts histogram",np.bincount(cs),"max",cs.max(),flush=True)
    print("time",time.time()-t)
    json.dump(dict(cont_hist=np.bincount(cc).tolist(),same_hist=np.bincount(cs).tolist(),horizon_nan=nb,horizon_found=found),open("controls.json","w"))
