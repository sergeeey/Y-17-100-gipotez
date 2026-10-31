import flint
A = flint.arb_mat(2, 2, [1, 2, 3, 4])
print([m for m in dir(A) if not m.startswith('_')])
