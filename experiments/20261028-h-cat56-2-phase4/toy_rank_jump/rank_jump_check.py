import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(1)
ds,dk,P=2,3,3
d=ds+dk
Q=np.diag([1/3,2/3])
rho0=np.zeros((d,d),complex); rho0[:ds,:ds]=Q
Gs=[rng.normal(size=(dk,ds))+1j*rng.normal(size=(dk,ds)) for _ in range(P)]
Xs=[]
for G in Gs:
    X=np.zeros((d,d),complex); X[ds:,:ds]=G; X[:ds,ds:]=-G.conj().T; Xs.append(X)
tau=np.diag([0,0,.2,.3,.5]).astype(complex)
def rho(th, jump):
    U=expm(sum(t*X for t,X in zip(th,Xs)))
    r2=float(np.dot(th,th))
    base=(1-r2)*rho0+r2*tau if jump else rho0
    return U@base@U.conj().T
def drho(th,jump,a,eps=1e-6):
    e=np.zeros(P); e[a]=eps
    return (rho(th+e,jump)-rho(th-e,jump))/(2*eps)
def K(th,jump):
    r=rho(th,jump); w,V=np.linalg.eigh(r); w=np.clip(w,0,None)
    Ks=[]
    for a in range(P):
        D=V.conj().T@drho(th,jump,a)@V
        L=np.zeros((d,d),complex)
        for i in range(d):
            for j in range(d):
                if w[i]+w[j]>1e-12: L[i,j]=2*D[i,j]/(w[i]+w[j])
        Ks.append(np.diag(np.sqrt(w))@L@V.conj().T)  # rho^{1/2} L in eigbasis rows, acting on original v
    return Ks
def N(Ks,v):
    kv=[k@v for k in Ks]
    return np.array([[np.real(np.vdot(kv[a],kv[b])) for b in range(P)] for a in range(P)])
K0=K(np.zeros(P),False)
vs=[ (lambda z: z/np.linalg.norm(z))(rng.normal(size=d)+1j*rng.normal(size=d)) for _ in range(300)]
# add vectors near kernel-only
vs+= [ (lambda z: z/np.linalg.norm(z))(np.concatenate([1e-3*rng.normal(size=ds),rng.normal(size=dk)])+0j) for _ in range(100)]
h=rng.normal(size=P); h/=np.linalg.norm(h)
for s in [1e-1,3e-2,1e-2,3e-3]:
    Ks=K(s*h,True)
    worst_mineig=min(np.linalg.eigvalsh(N(Ks,v)-N(K0,v))[0] for v in vs)
    worst_f=min(np.linalg.eigvalsh(N(Ks,v))[1]-np.linalg.eigvalsh(N(K0,v))[1] for v in vs)
    FQs=sum(N(Ks,e) for e in np.eye(d)); FQ0=sum(N(K0,e) for e in np.eye(d))
    print(f"s={s:g}  min_v lmin(N_s-N_0)={worst_mineig:+.3e}  min_v (f_s-f_0)={worst_f:+.3e}  trFQ(s)-trFQ(0)={np.trace(FQs)-np.trace(FQ0):+.4f}  hFQh jump={h@(FQs-FQ0)@h:+.4f}")
