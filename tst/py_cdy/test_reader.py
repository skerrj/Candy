"""Tests for the Candy file reader, ``reader.py``."""

from pathlib import Path

import pytest

from reader import find_path, get_path, slurp


def test_slurp_given_path(tmp_path: Path) -> None:
    src = tmp_path / "a.cdy"
    src.write_text("(put 1)\n", encoding="utf-8")
    assert slurp(str(src)) == "(put 1)\n"


def test_slurp_searches_path(tmp_path: Path) -> None:
    (tmp_path / "lib" / "deep").mkdir(parents=True)
    (tmp_path / "lib" / "deep" / "m.cdy").write_text("x", encoding="utf-8")
    assert slurp("m", (str(tmp_path / "lib"),)) == "x"


def test_find_path_skips_tmp(tmp_path: Path) -> None:
    (tmp_path / "tmp").mkdir()
    (tmp_path / "tmp" / "m.cdy").write_text("x", encoding="utf-8")
    assert find_path("m", (str(tmp_path),)) is None


def test_get_path_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        get_path("nope", (str(tmp_path),))


def test_find_path_root_under_tmp(tmp_path: Path) -> None:
    # pytest's tmp_path is itself under /tmp: only ``tmp`` below the root is skipped.
    (tmp_path / "m.cdy").write_text("x", encoding="utf-8")
    assert find_path("m", (str(tmp_path),)) == tmp_path / "m.cdy"
