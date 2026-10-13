"""Run a Python script with a low CPU footprint (laptop-friendly).

Usage:  python scripts/lowprio.py path/to/script.py [script args...]

WHY: on 2026-10-03 five parallel research workers (multiprocessing pools, default
BLAS threading) overheated the machine and powered it off. This wrapper makes any
heavy script polite: BLAS/OpenMP limited to LOWPRIO_THREADS (default 2) threads,
process priority BELOW_NORMAL, and the target runs as __main__ in this process
(so no extra process is spawned). It cannot stop a script from creating its own
multiprocessing pool -- do not use Pool/n_jobs>1 in throttled runs.
"""

import ctypes
import os
import runpy
import sys

THREADS = os.environ.get("LOWPRIO_THREADS", "2")
for var in (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ[var] = THREADS

BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
if os.name == "nt":
    # WHY explicit types: without them ctypes passes the 64-bit pseudo-handle as a
    # 32-bit int and SetPriorityClass silently fails (found by the self-test).
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    kernel32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint]
    kernel32.SetPriorityClass.restype = ctypes.c_int
    if not kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS):
        print("lowprio: WARNING could not lower priority", file=sys.stderr)

if len(sys.argv) < 2:
    sys.exit("usage: python scripts/lowprio.py script.py [args...]")

script = os.path.abspath(sys.argv[1])
sys.argv = [script, *sys.argv[2:]]
sys.path.insert(0, os.path.dirname(script))
runpy.run_path(script, run_name="__main__")
