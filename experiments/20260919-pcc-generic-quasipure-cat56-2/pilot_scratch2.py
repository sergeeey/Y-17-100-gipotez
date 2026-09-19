# ruff: noqa  (throw-away pilot, see claim.md registration note)
def lb(k, r, s):
    return r * r + max(s, 2 * k * r - s * r * r) + max(1, k * k - s * (s - 1) // 2 * r * r)


for r in (2, 3, 4):
    first = None
    for k in range(2, 80):
        d = r + k
        m = min((lb(k, r, s), s) for s in range(2, 2 * k * r + 1))
        if m[0] < d and first is None:
            first = (d, k, m)
    print("r", r, "first d where min_s LB<d:", first)
for k, r in [(2, 2), (4, 2), (5, 2), (6, 2), (8, 3), (9, 3)]:
    print(k, r, min((lb(k, r, s), s) for s in range(2, 2 * k * r + 1)), "d=", k + r)
