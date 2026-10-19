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


def test_main_translator_t1(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    Path("p.cdy").write_text('(put "via t1")\n', encoding="utf-8")
    assert main(["p.cdy", "--run", "--translator", "t1"]) == 0
    assert capfd.readouterr().out == "via t1\n"
    assert Path("output/t1/cdy_translator.py").exists()
    assert main(["p.cdy", "--translator"]) == 2
    assert main(["p.cdy", "--translator", "nope"]) == 2
    Path("bad.cdy").write_text("(put nope)\n", encoding="utf-8")
    assert main(["bad.cdy", "--translator", "t1"]) == 1
    assert "unknown name nope" in capfd.readouterr().err


def test_main_translator_bin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    Path("p.cdy").write_text('(put "via bin")\n', encoding="utf-8")
    assert main(["p.cdy", "--run", "--translator", "bin"]) == 0
    assert capfd.readouterr().out == "via bin\n"


def test_main_translator_bin_import(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    Path("sub").mkdir()
    Path("sub/lib.cdy").write_text('(sig who String)\n(def who "lib")\n', encoding="utf-8")
    Path("sub/p.cdy").write_text("(import lib)\n(put who)\n", encoding="utf-8")
    assert main(["sub/p.cdy", "--run", "--translator", "bin"]) == 0  # found next to p.cdy
    assert capfd.readouterr().out == "lib\n"
