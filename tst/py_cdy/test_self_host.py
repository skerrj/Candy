"""Tests for the self-hosted translator, T1 (``self_host.py``, ``src/cdy/*.cdy``).

T1 is built once per test session. Each ``tst/cdy/t1/NAME.cdy`` is translated by T1 and by
the Python translator; both results must run and print ``NAME.out``, and T1's must pass
``mypy --strict``. T1 itself must pass ``mypy --strict`` too: that type-checks the Candy
translator's own code.
"""

import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
from mypy import api as mypy_api

from cdy_rt.table_defs import CandyFail
from self_host import build_t1, load, translate_with
from translate_cdy import translate

ROOT = Path(__file__).resolve().parents[2]
PROGRAMS = sorted((ROOT / "tst" / "cdy" / "t1").glob("*.cdy"))
IDS = [p.stem for p in PROGRAMS]


@pytest.fixture(name="t1_path", scope="session")
def fixture_t1_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """T1, built once for the session."""
    return build_t1(tmp_path_factory.mktemp("t1"))


@pytest.fixture(name="t1", scope="session")
def fixture_t1(t1_path: Path) -> ModuleType:
    """T1, loaded."""
    return load(t1_path)


def run(source: str, tmp_path: Path, name: str) -> subprocess.CompletedProcess[str]:
    """Write ``source`` to ``tmp_path/name.py`` and run it from the repository root."""
    path = tmp_path / f"{name}.py"
    path.write_text(source, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(path)], capture_output=True, text=True, check=False, cwd=ROOT
    )


def test_t1_passes_mypy_strict(t1_path: Path) -> None:
    stdout, _, status = mypy_api.run(["--strict", "--no-incremental", str(t1_path)])
    assert status == 0, stdout


@pytest.mark.parametrize("program", PROGRAMS, ids=IDS)
def test_output(program: Path, t1: ModuleType, tmp_path: Path) -> None:
    text = program.read_text(encoding="utf-8")
    expected = program.with_suffix(".out").read_text(encoding="utf-8")
    for name, source in (("t1", translate_with(t1, text)), ("py", translate(text))):
        done = run(source, tmp_path, name)
        assert done.returncode == 0, f"{name}: {done.stderr}"
        assert done.stdout == expected, name


@pytest.mark.parametrize("program", PROGRAMS, ids=IDS)
def test_mypy_strict(program: Path, t1: ModuleType, tmp_path: Path) -> None:
    out = tmp_path / f"{program.stem}.py"
    out.write_text(translate_with(t1, program.read_text(encoding="utf-8")), encoding="utf-8")
    stdout, _, status = mypy_api.run(["--strict", "--no-incremental", str(out)])
    assert status == 0, stdout


@pytest.mark.parametrize(
    ("src", "message"),
    [
        ("(put nope)", "unknown name nope"),
        ("(def x 1)", "x needs a (sig x Type)"),
        ("(put (if 1))", "if: expected"),
        ("(put (cond (else 1) (true 2)))", "must be the last clause"),
        ("(put ())", "empty form"),
        ("(put if)", "special form, not a value"),
        ("(put (match 1 (else 2)))", "not supported by the Candy translator yet"),
        ("(deft S (A) (B))", "sum types are not supported"),
        ("(put (let ((x)) x))", "binding must be"),
        ("(put (let (((a b))) a))", "binding must be"),
        ("(put (fn () 1))", "at least one"),
        ("(put (tup))", "at least one item"),
        ("(put (get 1))", "expected (get obj field)"),
        ("(put (assoc 1 x))", "expected (assoc obj field value"),
        ("(put (assoc 1 x 2 y))", "expected (assoc obj field value"),
        ('(put (format "a } b"))', "unmatched }"),
        ('(put (format "a { b"))', "unmatched {"),
        ('(put (format "{1 2}"))', "exactly one form"),
        ("(sig f (Fn (Int) Int)) (defn f (x y) x)", "one type per argument"),
        ("(put (do (sig x Int)))", "only allowed at top level"),
    ],
)
def test_errors(src: str, message: str, t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match=re.escape(message)):
        translate_with(t1, src)
