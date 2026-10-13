import numpy as np
from pwl import *
zR,zL = hy_zones()
yg = y_grid(zR, 3000, 1e-5, 200.0)
y1,y2,tR,tL = compose(zR,zL,yg)
g = y2-yg
fin = np.isfinite(g)
idx = np.nonzero(fin)[0]
print("valid", len(idx), "range y0", yg[idx].min(), yg[idx].max())
# segments
segs=[]; s=idx[0]; p=idx[0]
for i in idx[1:]:
    if i!=p+1: segs.append((s,p)); s=i
    p=i
segs.append((s,p))
for a,b in segs:
    print("seg y0 [%.6g, %.6g] G ends %.4g %.4g, y1 ends %.6g %.6g"%(yg[a],yg[b],g[a],g[b],y1[a],y1[b]))
# print G around the end near y0->0.2 (largest y0 values)
for i in list(range(segs[0][0], segs[0][0]+5)):
    print(yg[i], y1[i], g[i])
