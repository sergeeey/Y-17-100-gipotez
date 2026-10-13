import json, re, sys
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
t = d["markdown"]
print("len", len(t))
for pat in [r"walk dimension", r"2\.09", r"numerical(ly)?", r"\rho_F ?\approx|ρ.{0,3}≈|1\.25"]:
    ms = list(re.finditer(pat, t))
    print("PATTERN", pat, "count", len(ms))
    for m in ms[:4]:
        print("   ...", t[max(0, m.start()-150):m.start()+250].replace("\n", " "))
