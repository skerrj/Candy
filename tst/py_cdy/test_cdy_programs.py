"""Golden tests for Candy programs: each ``tst/cdy/NAME.cdy`` is translated, run, and its
output compared with ``tst/cdy/NAME.out``; the generated Python must pass ``mypy --strict``.

Programs run from the repository root, so ``slurp`` finds files on ``SEARCH_PATH``.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from mypy import api as mypy_api

from translate_cdy import translate

ROOT = Path(__file__).resolve().parents[2]
PROGRAMS = sorted((ROOT / "tst" / "cdy").glob("*.cdy"))


def translated(program: Path, tmp_path: Path) -> Path:
    """``program`` translated to Python, written under ``tmp_path``."""
    out = tmp_path / f"{program.stem}.py"
    out.write_text(translate(program.read_text(encoding="utf-8")), encoding="utf-8")
    return out


@pytest.mark.parametrize("program", PROGRAMS, ids=[p.stem for p in PROGRAMS])
def test_output(program: Path, tmp_path: Path) -> None:
    done = subprocess.run(
        [sys.executable, str(translated(program, tmp_path))],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout == program.with_suffix(".out").read_text(encoding="utf-8")


@pytest.mark.parametrize("program", PROGRAMS, ids=[p.stem for p in PROGRAMS])
def test_mypy_strict(program: Path, tmp_path: Path) -> None:
    stdout, _, status = mypy_api.run(
        ["--strict", "--no-incremental", str(translated(program, tmp_path))]
    )
    assert status == 0, stdout
