from flint import arb, ctx
import flint
ctx.prec = 192
print("flint", flint.__version__)
x = arb("0.5 +/- 0.1"); y = arb("2 +/- 0.1")
print("uncertain 0.5+/-0.1 > 0 :", bool(x > 0))
print("uncertain 0.5+/-0.1 < 0 :", bool(x < 0))
print("2+/-0.1 > 0 :", bool(y > 0), "| 2+/-0.1 < 1 :", bool(y < 1))
print("x == x (uncertain):", bool(x == x))
z = arb("1e-12")
print("arb('1e-12') as float", float(z), "| mid str", z.str(30))
w = arb(1e-12)
print("arb(1e-12) float exact?", (w - arb("1e-12")).str(10))
print("nan check lower<=0<=upper for exact zero:", bool(arb(0).lower() <= 0 <= arb(0).upper()))
