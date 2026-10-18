"""Tests for the command-line entry point, ``main.py``."""

from pathlib import Path

import pytest

from main import main, out_path
from parse_cdy import Int, SList, Symbol


def test_out_path() -> None:
    assert out_path("src/x/prog.cdy") == Path("output/prog.py")


def test_main_prints_forms(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    src = tmp_path / "p.cdy"
    src.write_text("(put 1) ; hi\n", encoding="utf-8")
    assert main([str(src)]) == 0
    assert repr(SList((Symbol("put"), Int(1)))) in capsys.readouterr().out


def test_main_errors(tmp_path: Path) -> None:
    bad = tmp_path / "bad.cdy"
    bad.write_text("(a b", encoding="utf-8")
    assert main([]) == 2
    assert main([str(tmp_path / "missing.cdy")]) == 1
    assert main([str(bad)]) == 1
