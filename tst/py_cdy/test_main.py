"""Tests for the command-line entry point, ``main.py``."""

from pathlib import Path

import pytest

from main import main, out_path, translate_file


def test_out_path() -> None:
    assert out_path("src/x/prog.cdy") == Path("output/prog.py")


def test_translate_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    Path("p.cdy").write_text("(put 1) ; hi\n", encoding="utf-8")
    out = translate_file("p.cdy")
    assert out == Path("output/p.py")
    assert out.read_text(encoding="utf-8").endswith("print(1)\n")


def test_main_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    Path("p.cdy").write_text('(put "hi")\n', encoding="utf-8")
    assert main(["p.cdy", "--run"]) == 0
    assert capfd.readouterr().out == "hi\n"


def test_main_errors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    Path("bad.cdy").write_text("(a b", encoding="utf-8")
    Path("nosig.cdy").write_text("(def x 1)", encoding="utf-8")
    assert main([]) == 2
    assert main(["a.cdy", "b.cdy"]) == 2
    assert main(["missing.cdy"]) == 1
    assert main(["bad.cdy"]) == 1
    assert main(["nosig.cdy"]) == 1
