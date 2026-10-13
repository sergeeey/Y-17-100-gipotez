"""Run the masked (weaker-symmetry) searches strictly one after another with a 45 s cooling pause (hardware rule 7c)."""
import subprocess, sys, time
PY = "C:/Users/serge/miniconda3/envs/ape311/python3.exe"
LOW = "../../scripts/lowprio.py"
for mask, seed0 in (("z3", 200000), ("w001", 300000), ("z2", 400000)):
    with open("d3_%s.log" % mask, "w") as lg:
        subprocess.run([PY, LOW, "run_serial.py", "d3_" + mask, mask, "700", str(seed0), "200", "near_flip,near_id,gauss", "150"], stdout=lg, stderr=subprocess.STDOUT)
    print("finished", mask, flush=True)
    time.sleep(45)
print("BATCH-DONE", flush=True)
