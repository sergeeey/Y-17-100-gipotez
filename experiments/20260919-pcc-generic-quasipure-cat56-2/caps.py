"""Resource caps (post-registration, coordinator order after machine overload).

Import this module FIRST in every script (before numpy): single BLAS thread, cores 16-23 only,
BELOW_NORMAL priority. Peak RSS is reported via `peak_rss_mb()`.
"""

from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"

import psutil  # noqa: E402

CORES = list(range(16, 24))


def apply() -> None:
    p = psutil.Process()
    try:
        p.cpu_affinity(CORES)
    # WHY: on a machine/container with fewer than 24 logical CPUs, psutil raises a plain
    # ValueError for an out-of-range core index -- not AttributeError/psutil.Error/OSError,
    # so it was falling through uncaught and crashing every script that imports this module
    # (found 2026-09-23, external audit; reproduced by requesting a nonexistent core).
    except (AttributeError, psutil.Error, OSError, ValueError):
        pass
    try:
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except (AttributeError, psutil.Error, OSError):
        pass


def peak_rss_mb() -> float:
    info = psutil.Process().memory_info()
    peak = getattr(info, "peak_wset", info.rss)
    return peak / 1e6


def state() -> dict:
    p = psutil.Process()
    return {
        "affinity": p.cpu_affinity() if hasattr(p, "cpu_affinity") else None,
        "nice": p.nice(),
        "threads_env": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS")},
        "peak_rss_mb": peak_rss_mb(),
    }


apply()
