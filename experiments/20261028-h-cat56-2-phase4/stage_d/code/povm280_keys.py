# WHY: first look at the candidate file layout before writing any interval check.
import numpy as np
P = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz"
z = np.load(P, allow_pickle=True)
for k in z.files:
    a = z[k]
    print(k, a.dtype, a.shape)
