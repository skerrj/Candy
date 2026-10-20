"""Tests for the runtime helpers in ``cdy_rt.table_defs``."""

from pathlib import Path

import pytest

from cdy_rt.table_defs import (
    CandyFail,
    at,
    call_macro,
    fail,
    file_exists,
    file_put_lines,
    fresh_name,
    get_indent,
    hex_char,
    in_,
    is_coll,
    is_decimal,
    is_lit,
    is_neg_int,
    join,
    list_filter,
    list_fold,
    list_map,
    load_macros,
    make_dirs,
    map_get,
    map_has,
    map_keys,
    map_set,
    module_dir,
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
    assert map_keys(map_set(m, "a", 3)) == ("a", "b")


def test_py_render_and_fail() -> None:
    assert py_mangle("set-x!") == "set_x_x"
    assert py_mangle("list") == "list_"
    assert py_repr("a'b") == '"a\'b"'
    assert py_repr(2.0) == "2.0"
    with pytest.raises(CandyFail, match="boom"):
        fail("boom")


HOME = "Form"  # a name the "translator" defines, which load_macros is asked to put back
OTHER = "mine"  # one it isn't


def home() -> None:
    """Stands in for a translator function: load_macros runs a program in its module."""


form__HOME = "prefixed Form"  # pylint: disable=invalid-name  # the same, with modules


def form__home() -> None:
    """Stands in for a function of a translator built with modules (form.cdy's prefix)."""


def test_load_macros() -> None:
    program = (
        "HOME = 'theirs'\nOTHER = 'theirs'\n"
        "def macro__m(args):\n    return (HOME, OTHER, args)\nmacro__n = 1\n"
    )
    macros = load_macros(program, home, {"HOME": True})
    assert set(macros) == {"macro__m", "macro__n"}
    # HOME is the home module's again; OTHER stays the program's.
    assert macros["macro__m"](("a",)) == ("Form", "theirs", ("a",))
    assert "macro__m" not in globals() and OTHER == "mine"  # it ran in a copy
    # With modules, form.cdy's names have home's prefix.
    macros = load_macros(program, form__home, {"HOME": True})
    assert macros["macro__m"](()) == ("prefixed Form", "theirs", ())


def test_fresh_name() -> None:
    load_macros("", home, {})  # restarts the count
    assert (fresh_name("x"), fresh_name("tmp")) == ("x__1", "tmp__2")
    load_macros("", home, {})
    assert fresh_name("x") == "x__1"


def test_call_macro() -> None:
    assert call_macro(len, ("a", "b"), "here: ") == 2

    def failing(_: object) -> None:
        fail("no")

    with pytest.raises(CandyFail, match="^here: no$"):
        call_macro(failing, (), "here: ")
    with pytest.raises(CandyFail, match="^here: IndexError: "):
        call_macro(lambda args: args[3], (), "here: ")


def test_module_dir() -> None:
    assert module_dir(home) == str(Path(__file__).parent)


def test_list_functions() -> None:
    assert list_map(lambda n: n * 2, (1, 2, 3)) == (2, 4, 6)
    assert list_filter(lambda n: n % 2 == 1, (1, 2, 3)) == (1, 3)
    assert list_fold(lambda acc, s: acc + s, "", ("a", "b")) == "ab"
    assert not list_map(str, ())
