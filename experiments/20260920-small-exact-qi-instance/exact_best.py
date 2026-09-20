# ruff: noqa
import sys, json
sys.set_int_max_str_digits(0)
import explore_a2 as e
import exact_certify as ec
seed, m, c = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
blocks, curve = e.build(seed, m, c, 400)
print("float dimV", e.float_dimv(blocks), "max abs", max(abs(v) for x in blocks for v in x))
ec.build_blocks = lambda k, r, s, sd, lll: (blocks, [0] * s)
res = ec.certify(20, 2, 16, seed, True)
print({k: res[k] for k in ("pcc_exact_zero", "lyapunov_exact_zero", "qfim_det_nonzero", "rank_mod_p", "exact_certified_dimVperp_lt_d")})
json.dump({"seed": seed, "m": m, "c": c, "blocks": blocks}, open(f"metrics/best_tuple_{seed}.json", "w"))
