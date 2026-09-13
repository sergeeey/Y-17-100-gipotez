"""Verify the asymptotic derivation for why s_2(L) ~ c*sqrt(L):

z_0 = (L+3)/(L-1) = 1 + 4/(L-1) =: 1+eps
T_s(1+eps) = cosh(s * arccosh(1+eps)), and arccosh(1+eps) ~ sqrt(2*eps) for small eps.
=> A_s ~ cosh(s*sqrt(2*eps)) = cosh(s*sqrt(8/(L-1)))

cert_bound = (A_s+1)/(A_s-1) = 2  <=>  A_s = 3  <=>  s*sqrt(8/(L-1)) = arccosh(3)

s_2(L) ~ arccosh(3) * sqrt((L-1)/8)
"""

import numpy as np
from numpy.polynomial import chebyshev as C

arccosh3 = np.arccosh(3.0)
coeff = arccosh3 / np.sqrt(8)
print(f"arccosh(3) = {arccosh3:.6f}")
print(f"predicted coefficient c in s_2(L) ~ c*sqrt(L): {coeff:.6f}")
print()

for L in (100, 250, 500, 1000):
    predicted = coeff * np.sqrt(L - 1)
    # exact: find s where cert_bound crosses 2
    x = (L + 3) / (L - 1)
    prev_bound = None
    crossing = None
    for s in range(1, 40):
        coeffs = np.zeros(s + 1)
        coeffs[s] = 1.0
        A_s = C.chebval(x, coeffs)
        bound = (A_s + 1) / (A_s - 1)
        if prev_bound is not None and prev_bound > 2 >= bound:
            crossing = s
            break
        prev_bound = bound
    print(f"L={L:5d}: predicted s_2~{predicted:.2f}  exact crossing at s={crossing}")
