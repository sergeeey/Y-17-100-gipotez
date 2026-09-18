"""
Independent re-derivation: does plugging Bandeira et al. 2025's Theorem 1
upper bound E[theta(G)] <= C*sqrt(n*log(log(n))) into this project's own
established inequality V_n <= 2*(E[theta]/sqrt(n) - 1) give anything close
to the headline claim V_n = O(1/n)?

Also checks the field's own best OPEN conjecture (Conjecture 1: E[theta(G)]
= (1+o(1))*sqrt(n)) under the most optimistic reading.
"""

import math


def g_n_bound_from_theorem1(n, C):
    """g_n = E[theta] - sqrt(n) upper bound via Bandeira Thm 1."""
    sqrt_n = math.sqrt(n)
    e_theta_bound = C * math.sqrt(n * math.log(math.log(n)))
    return e_theta_bound - sqrt_n


def v_n_bound(g_n, n):
    """V_n <= 2*g_n/sqrt(n), this project's own Point 94 inequality."""
    return 2.0 * g_n / math.sqrt(n)


header = (
    f"{'n':>8} {'sqrt(n)':>10} {'loglogn':>10} "
    f"{'g_n bound (C=1)':>18} {'V_n bound (C=1)':>16} {'target O(1/n)':>14}"
)
print(header)
for n in [509, 1021, 2039, 8191, 100000, 10**9]:
    C = 1.0  # order-1 constant, qualitative check -- exact constant not given in abstract
    g = g_n_bound_from_theorem1(n, C)
    v = v_n_bound(g, n)
    target = 1.0 / n
    row = (
        f"{n:>8} {math.sqrt(n):>10.2f} {math.log(math.log(n)):>10.4f} "
        f"{g:>18.4f} {v:>16.6f} {target:>14.8f}"
    )
    print(row)

print()
print("Conclusion check: does V_n bound via Theorem 1 shrink with n at all?")
print("(if it GROWS or stays ~constant, Theorem 1 alone cannot establish V_n=O(1/n))")
print()

print("--- Best-case: field's own OPEN Conjecture 1 (E[theta]=(1+o(1))sqrt(n)) ---")
print("Even if PROVEN with the loosest possible o(1) factor eps_n = 1/log(n):")
for n in [509, 2039, 8191, 100000]:
    eps_n = 1.0 / math.log(n)
    g_n = math.sqrt(n) * eps_n
    v_bound = v_n_bound(g_n, n)
    target = 1.0 / n
    print(
        f"n={n:>8}: eps_n=1/ln(n)={eps_n:.4f}, g_n bound={g_n:.3f}, "
        f"V_n bound={v_bound:.6f}, target 1/n={target:.8f}, "
        f"ratio V_bound/target = {v_bound / target:.1f}x too loose"
    )

print()
print("What g_n needs to be for V_n=O(1/n) via this inequality: g_n = O(n^-0.5)")
print("i.e. E[theta(G_n)] = sqrt(n) + O(n^-0.5) -- additive precision far beyond")
print("even the sharp Conjecture 1's own o(sqrt(n)) claim.")
