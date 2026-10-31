import numpy as np, json, scipy.linalg as sl
rng=np.random.default_rng(7)
Q=np.diag([1/3,2/3]); rho=np.zeros((22,22),complex); rho[:2,:2]=Q
def Lof(A):
    L=np.zeros((22,22),complex); L[:2,2:]=A.conj().T; L[2:,:2]=A; return L
def stats(m,L):
    p=np.trace(rho@m).real; a=np.trace(rho@L@m).real; q=np.trace(rho@L@m@L).real
    return p,a,q
def G(m,L):  # q*p - a^2 form
    p,a,q=stats(m,L); return q*p-a*a, p
def run(As,tag):
    n=len(As); Ls=[Lof(A) for A in As]
    # random PSD, random c
    worst=1e9; cnt=0
    for t in range(20000):
        r=rng.integers(1,23); V=rng.normal(size=(22,r))+1j*rng.normal(size=(22,r))
        # sometimes sparse in support to hit p small
        if t%5==0: V[:2]*=1e-3
        m=V@V.conj().T*rng.exponential()
        c=rng.normal(size=n); L=sum(ci*Li for ci,Li in zip(c,Ls))
        g,p=G(m,L); sc=np.trace(rho@L@m@L).real*p+1e-300
        worst=min(worst,g/sc); cnt+=1
    print(tag,"min normalized G over",cnt,"random PSD m:",worst)
    # admissible rank-one: unknown y (40 real), lam (n real); eq A_i^† y - lam_i x =0 (complex -> 2 real each)
    x=rng.normal(size=2)+1j*rng.normal(size=2)
    rows=[]
    for i,A in enumerate(As):
        M=A.conj().T  # 2x20
        blk=np.zeros((4,40+n))
        Mr=np.block([[M.real,-M.imag],[M.imag,M.real]])  # acts on [yr;yi]
        blk[:,:40]=Mr
        xv=np.concatenate([x.real,x.imag]); blk[:,40+i]=-xv
        rows.append(blk)
    Phi=np.vstack(rows)
    ns=sl.null_space(Phi); print(tag,"null dim (y,lam):",ns.shape[1],"expected >= ",40+n-4*n)
    v=ns@rng.normal(size=ns.shape[1]); y=v[:20]+1j*v[20:40]
    pi=np.concatenate([x,y]); m=np.outer(pi,pi.conj())
    mx=0
    for _ in range(200):
        c=rng.normal(size=n); L=sum(ci*Li for ci,Li in zip(c,Ls))
        g,p=G(m,L); sc=np.trace(rho@L@m@L).real*p
        mx=max(mx,abs(g)/sc)
    print(tag,"admissible rank-one: max |G|/(q p) over 200 c:",mx, " |y|=",np.linalg.norm(y))
    # non-real lambda: y' with A_i^† y' = (lam+ i mu) x  -> use x -> i x trick: pi=(x; i y) gives A^† (i y)= i lam x : complex
    pi2=np.concatenate([x,1j*y]); m2=np.outer(pi2,pi2.conj()); mn=1e9
    for _ in range(200):
        c=rng.normal(size=n); L=sum(ci*Li for ci,Li in zip(c,Ls))
        g,p=G(m2,L); sc=np.trace(rho@L@m2@L).real*p
        mn=min(mn,g/sc)
    print(tag,"imaginary-lambda rank-one: min G/(q p):",mn)
    # two admissible pieces with different x, y (separate kernels): pieces G=0 but sum G>0?
    x2=rng.normal(size=2)+1j*rng.normal(size=2)
    rows=[]
    for i,A in enumerate(As):
        M=A.conj().T; blk=np.zeros((4,40+n)); blk[:,:40]=np.block([[M.real,-M.imag],[M.imag,M.real]])
        blk[:,40+i]=-np.concatenate([x2.real,x2.imag]); rows.append(blk)
    ns2=sl.null_space(np.vstack(rows)); v2=ns2@rng.normal(size=ns2.shape[1]); y2=v2[:20]+1j*v2[20:40]
    pi3=np.concatenate([x2,y2]); m3=np.outer(pi3,pi3.conj())
    ms=m+m3; mg=0; mg_pieces=0
    for _ in range(200):
        c=rng.normal(size=n); L=sum(ci*Li for ci,Li in zip(c,Ls))
        g,p=G(ms,L); sc=np.trace(rho@L@ms@L).real*p
        mg=max(mg,g/sc)
        g1,_=G(m,L); g2,_=G(m3,L)
        # Lemma 2: G(m)>=sum of piece G (in q - a^2/p form)
        p1=stats(m,L)[0];p2=stats(m3,L)[0]
        lhs=g/p; rhs=g1/p1+g2/p2
        assert lhs>=rhs-1e-9*abs(lhs)-1e-9, (lhs,rhs)
    print(tag,"two admissible pieces summed: max G/(q p) =",mg,"(pieces each 0; Lemma 2 inequality held on all 200 c)")
    # null non-pure: x=0, random y -> G>0
    pi4=np.concatenate([np.zeros(2),rng.normal(size=20)+1j*rng.normal(size=20)]); m4=np.outer(pi4,pi4.conj())
    c=rng.normal(size=n); L=sum(ci*Li for ci,Li in zip(c,Ls)); print(tag,"null nonpure: q_c =",np.trace(rho@L@m4@L).real)
# random instance
As=[rng.normal(size=(20,2))+1j*rng.normal(size=(20,2)) for _ in range(12)]
run(As,"random12")
# file instance, S={4..15}
d=json.loads(open("E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261027-h-cat56-2-submission-package-v1/data/instance_d22_r2_s16.jsonl").readline())
Af=[]
for b in d["blocks"]:
    b=np.array(b,float); re=b[:40].reshape(20,2); im=b[40:].reshape(20,2); Af.append((re+1j*im)*(-2j))
run(Af[4:16],"file S-")
