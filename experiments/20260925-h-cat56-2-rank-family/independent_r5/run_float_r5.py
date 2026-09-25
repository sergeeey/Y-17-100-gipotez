# ruff: noqa
"""Thin driver: calls the blind implementer's float pipeline UNCHANGED for (41,5,14) and (41,5,15)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "independent_r3"))
from run_float import run  # noqa: E402

for d, r, s, seed in ((41, 5, 14, 1), (41, 5, 14, 2), (41, 5, 15, 1)):
    print("=== FLOAT d=%d r=%d s=%d seed=%d" % (d, r, s, seed))
    run(d, r, s, seed)
    sys.stdout.flush()
