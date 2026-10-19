"""Tests for the runtime helpers in ``cdy_rt.table_defs``."""

from pathlib import Path

import pytest

from cdy_rt.table_defs import (
    CandyFail,
    at,
    fail,
    file_exists,
    file_put_lines,
    get_indent,
    hex_char,
    in_,
    is_coll,
    is_decimal,
    is_lit,
    is_neg_int,
    join,
    make_dirs,
    map_get,
    map_has,
    map_set,
    path_dir,
    path_join,
    path_resolve,
    path_stem,
    put_err,
    py_mangle,
    py_repr,
    replace,
    run_main,
    slice_,
    spit,
    to_float,
    to_list,
)


def test_collections() -> None:
    assert at((1, 2, 3), 1) == 2
    assert slice_((1, 2, 3, 4), 1, 3) == (2, 3)
    assert join(("a", "b"), ", ") == "a, b"
    assert is_coll((1,)) and is_coll([1]) and not is_coll("ab")
    assert is_lit(3) and not is_lit(())
    assert to_list(5) == (5,)
    assert in_(2, (1, 2)) and in_("b", "abc")


def test_strings() -> None:
    assert is_neg_int("x-3", 1)
    assert not is_neg_int("x-", 1)
    assert not is_neg_int("-", 0)
    assert replace("a-a", "a", "b") == "b-a"
    assert get_indent(2) == " " * 8
    assert to_float("-1.5") == -1.5
    assert is_decimal("09") and not is_decimal("") and not is_decimal("\u00b2")
    assert hex_char("0041") == "A"


def test_files(tmp_path: Path) -> None:
    out = tmp_path / "o.txt"
    spit(str(out), "hi")
    assert out.read_text(encoding="utf-8") == "hi"
    file_put_lines(str(out), ("a\n", "b\n"))
    assert out.read_text(encoding="utf-8") == "a\nb\n"
    assert file_exists(str(out)) and not file_exists(str(tmp_path))
    assert path_dir(path_join(str(tmp_path), "o.txt")) == str(tmp_path)
    assert path_resolve(path_join(str(tmp_path / "x"), "../o.txt")) == str(out.resolve())
    make_dirs(str(tmp_path / "a" / "b"))
    make_dirs(str(tmp_path / "a" / "b"))  # already there
    assert (tmp_path / "a" / "b").is_dir()
    assert path_stem("src/x/prog.cdy") == "prog"


def test_put_err_and_run_main(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    put_err("oops")
    assert capsys.readouterr().err == "oops\n"
    monkeypatch.setattr("sys.argv", ["prog", "a", "b"])
    with pytest.raises(SystemExit) as done:
        run_main(len)
    assert done.value.code == 2

    def failing(_: tuple[str, ...]) -> int:
        fail("no good")

    with pytest.raises(SystemExit) as done:
        run_main(failing)
    assert done.value.code == 1
    assert capsys.readouterr().err == "candy: no good\n"


def test_maps() -> None:
    m = map_set({"a": 1}, "b", 2)
    assert m == {"a": 1, "b": 2}
    assert map_get(m, "b") == 2
    assert map_has(m, "a") and not map_has(m, "c")


def test_py_render_and_fail() -> None:
    assert py_mangle("set-x!") == "set_x_x"
    assert py_mangle("list") == "list_"
    assert py_repr("a'b") == '"a\'b"'
    assert py_repr(2.0) == "2.0"
    with pytest.raises(CandyFail, match="boom"):
        fail("boom")
