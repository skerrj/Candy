"""Tests for the runtime helpers in ``cdy_rt.table_defs``."""

from pathlib import Path

from cdy_rt.table_defs import (
    at,
    file_put_lines,
    get_indent,
    in_,
    is_coll,
    is_lit,
    is_neg_int,
    join,
    replace,
    slice_,
    spit,
    to_list,
)


def test_collections() -> None:
    assert at((1, 2, 3), 1) == 2
    assert slice_((1, 2, 3, 4), 1, 3) == (2, 3)
    assert join(("a", "b"), ", ") == "a, b"
    assert is_coll((1,)) and is_coll([1]) and not is_coll("ab")
    assert is_lit(3) and not is_lit(())
    assert to_list(5) == [5]
    assert in_(2, (1, 2)) and in_("b", "abc")


def test_strings() -> None:
    assert is_neg_int("x-3", 1)
    assert not is_neg_int("x-", 1)
    assert not is_neg_int("-", 0)
    assert replace("a-a", "a", "b") == "b-a"
    assert get_indent(2) == " " * 8


def test_files(tmp_path: Path) -> None:
    out = tmp_path / "o.txt"
    spit(str(out), "hi")
    assert out.read_text(encoding="utf-8") == "hi"
    file_put_lines(str(out), ("a\n", "b\n"))
    assert out.read_text(encoding="utf-8") == "a\nb\n"
