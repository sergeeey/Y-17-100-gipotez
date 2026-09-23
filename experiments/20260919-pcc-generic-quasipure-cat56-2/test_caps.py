"""Tests for caps.py's resource-cap fallback behaviour.

Regression for the 2026-09-23 external-audit finding: on a machine/container with fewer than
24 logical CPUs, psutil.Process.cpu_affinity() raises a plain ValueError for an out-of-range
core index -- not AttributeError, psutil.Error, or OSError -- so it fell through the module's
try/except uncaught and crashed every script that imports caps.py before doing anything else.

apply() runs at import time (module-level call), so caps is already imported by the time this
test file loads; these tests exercise apply() again directly, with a monkeypatched Process
that reproduces the real failure mode without touching this machine's actual CPU affinity.
"""

from __future__ import annotations

import sys
from pathlib import Path

import psutil
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import caps  # WHY: this experiment dir is not a package; path insert precedes import


def test_apply_swallows_value_error_from_cpu_affinity(monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_value_error(self, cpus=None):
        if cpus is not None:
            raise ValueError("invalid CPU 999")
        return list(range(psutil.cpu_count()))

    monkeypatch.setattr(psutil.Process, "cpu_affinity", _raise_value_error)
    caps.apply()  # must not raise


def test_apply_still_sets_nice_even_if_affinity_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def _raise_value_error(self, cpus=None):
        if cpus is not None:
            raise ValueError("invalid CPU 999")
        return list(range(psutil.cpu_count()))

    def _record_nice(self, value=None):
        if value is not None:
            calls.append(value)
        return psutil.BELOW_NORMAL_PRIORITY_CLASS

    monkeypatch.setattr(psutil.Process, "cpu_affinity", _raise_value_error)
    monkeypatch.setattr(psutil.Process, "nice", _record_nice)
    caps.apply()
    assert calls == [psutil.BELOW_NORMAL_PRIORITY_CLASS]


def test_apply_on_this_real_machine_does_not_raise() -> None:
    """Positive control: on a machine that DOES have cores 16-23 (this one, 24 logical CPUs),
    apply() should set the real affinity without needing the fallback at all."""
    caps.apply()
    p = psutil.Process()
    if psutil.cpu_count() > max(caps.CORES):
        assert p.cpu_affinity() == caps.CORES
