import flint
print("fmpq_mat:", [m for m in dir(flint.fmpq_mat) if not m.startswith('_')])
print("fmpz_mat:", [m for m in dir(flint.fmpz_mat) if not m.startswith('_')])
