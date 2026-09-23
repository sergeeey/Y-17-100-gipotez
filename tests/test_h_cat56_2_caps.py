"""Tests for experiments/20260919-pcc-generic-quasipure-cat56-2/caps.py's resource-cap fallback.

Regression for the 2026-09-23 external-audit finding: on a machine/container with fewer than
24 logical CPUs, psutil.Process.cpu_affinity() raises a plain ValueError for an out-of-range
core index -- not AttributeError, psutil.Error, or OSError -- so it fell through the module's
try/except uncaught and crashed every script that imports caps.py before doing anything else.

A copy of these tests also lives at experiments/20260919-pcc-generic-quasipure-cat56-2/test_caps.py
(written first, then found to be unreachable: `testpaths = ["tests"]` excludes experiments/** from
the default pytest run -- see this file's own presence in the fix as evidence for that finding).
This is the copy that is actually enforced.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import psutil
import pytest

_CAPS_PATH = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260919-pcc-generic-quasipure-cat56-2"
    / "caps.py"
)
_SPEC = importlib.util.spec_from_file_location("h_cat56_2_caps", _CAPS_PATH)
caps = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(
    caps
)  # runs apply() once at import time, same as every script that uses it


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
