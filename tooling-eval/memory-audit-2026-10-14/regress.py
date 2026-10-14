"""Run the config repo's own tests/test_pre_compact.py against ORIGINAL vs PATCHED pre_compact.py in isolated temp copies
(HOME/USERPROFILE redirected so no real ~/.claude path can be written)."""

import filecmp
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path.home() / "claude-cod-top-2026-src"
PATCHED = Path(__file__).resolve().parent / "proposed" / "pre_compact_patched.py"
print(
    "installed hook == repo hook:",
    filecmp.cmp(
        Path.home() / ".claude" / "hooks" / "pre_compact.py",
        SRC / "hooks" / "pre_compact.py",
        shallow=False,
    ),
)


def run(label, use_patch):
    with tempfile.TemporaryDirectory() as t:
        root = Path(t) / "repo"
        shutil.copytree(
            SRC / "hooks",
            root / "hooks",
            ignore=shutil.ignore_patterns("__pycache__", "*.bak*", "*.backup*"),
        )
        (root / "tests").mkdir()
        for f in ("test_pre_compact.py", "conftest.py", "__init__.py"):
            if (SRC / "tests" / f).exists():
                shutil.copy(SRC / "tests" / f, root / "tests" / f)
        for f in ("pyproject.toml", "pytest.ini", "setup.cfg"):
            if (SRC / f).exists():
                shutil.copy(SRC / f, root / f)
        if use_patch:
            shutil.copy(PATCHED, root / "hooks" / "pre_compact.py")
        home = Path(t) / "home"
        home.mkdir()
        env = dict(os.environ, HOME=str(home), USERPROFILE=str(home), PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_pre_compact.py",
                "-q",
                "-p",
                "no:cacheprovider",
                "--no-header",
            ],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        tail = [ln for ln in r.stdout.splitlines() if ln.strip()][-8:]
        wrote_home = [str(p.relative_to(home)) for p in home.rglob("*") if p.is_file()]
        print(
            f"=== {label}: rc={r.returncode}\n"
            + "\n".join(tail)
            + f"\n(files written under temp HOME: {wrote_home[:5]})"
        )


run("ORIGINAL hook", False)
run("PATCHED hook", True)
