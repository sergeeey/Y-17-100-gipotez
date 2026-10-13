import importlib
for m in ["numpy","scipy","sympy","networkx","mpmath","pynauty","itertools","cdd","igraph"]:
    try:
        mod=importlib.import_module(m); print(m,"OK",getattr(mod,"__version__",""))
    except Exception as e: print(m,"MISSING",type(e).__name__)
