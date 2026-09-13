"""Does X itself (point 11's own established odd-Fourier-parity claim) actually hold at
COMPOSITE n, or was that claim (implicitly) only ever verified at prime n? Direct full-cube WHT
check, independent of the second-difference script."""

import importlib.util
from pathlib import Path

import numpy as np

HERE = Path(
    r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez"
    r"\experiments\20260910-lovasz-theta-variance-scaling-cat31-3"
)
spec = importlib.util.spec_from_file_location("nm2", HERE / "check_necklace_orbit_reduction.py")
nm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nm)


def fwht(a):
    a = a.astype(np.float64).copy()
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a


def popcount(x):
    return bin(x).count("1")


def check(n):
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    xhat = fwht(x) / len(x)
    even_e = sum(xhat[t] ** 2 for t in range(len(xhat)) if popcount(t) % 2 == 0)
    odd_e = sum(xhat[t] ** 2 for t in range(len(xhat)) if popcount(t) % 2 == 1)
    total = even_e + odd_e
    is_prime = all(n % p != 0 for p in range(2, int(n**0.5) + 1)) if n > 1 else False
    print(
        f"n={n:3d} (prime={is_prime}) m={m}: X odd_fraction={odd_e / total:.6f} "
        f"even_fraction={even_e / total:.2e} (point 11 predicts odd~1.0)"
    )


if __name__ == "__main__":
    for n in (13, 15, 17, 19, 21, 23):
        check(n)
