"""Tests for the Candy s-expression reader."""

import pytest
from parsec import ParseFailure, parse

from parse_cdy import Bool, Number, SList, Str, Symbol, program


def test_atoms() -> None:
    assert parse(program, "42 -7 foo + #t #f") == (
        Number(42),
        Number(-7),
        Symbol("foo"),
        Symbol("+"),
        Bool(True),
        Bool(False),
    )


def test_nested_list_and_quote() -> None:
    assert parse(program, "(sq (* x x)) 'y") == (
        SList((Symbol("sq"), SList((Symbol("*"), Symbol("x"), Symbol("x"))))),
        SList((Symbol("quote"), Symbol("y"))),
    )


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ('""', ""),
        ('"hello world"', "hello world"),
        (r'"a\nb\tc"', "a\nb\tc"),
        (r'"say \"hi\""', 'say "hi"'),
        (r'"back\\slash"', "back\\slash"),
        (r'"\/\b\f\r"', "/\b\f\r"),
        (r'"é"', "é"),
        ('"(not a list)"', "(not a list)"),
    ],
)
def test_string_literals(source: str, expected: str) -> None:
    assert parse(program, source) == (Str(expected),)


def test_string_in_list() -> None:
    assert parse(program, '(put "x: {x}")') == (SList((Symbol("put"), Str("x: {x}"))),)


def test_symbol_stops_at_quote() -> None:
    assert parse(program, 'abc"def"') == (Symbol("abc"), Str("def"))


@pytest.mark.parametrize("source", ['"unterminated', r'"bad \q escape"', r'"\u12"'])
def test_bad_strings(source: str) -> None:
    with pytest.raises(ParseFailure):
        parse(program, source)


def test_comments_are_ignored() -> None:
    source = """;;; section header
;; standalone comment
(def x 42) ; inline comment
; trailing comment with no newline"""
    assert parse(program, source) == (SList((Symbol("def"), Symbol("x"), Number(42))),)


def test_comment_inside_list() -> None:
    assert parse(program, "(a ; comment\n b)") == (SList((Symbol("a"), Symbol("b"))),)


def test_comment_ends_a_token() -> None:
    assert parse(program, "42;c\nfoo;c\n#t;c") == (Number(42), Symbol("foo"), Bool(True))


def test_semicolon_in_string_is_not_a_comment() -> None:
    assert parse(program, '"a ; b"') == (Str("a ; b"),)


def test_only_comments() -> None:
    assert parse(program, "; nothing here\n;; or here\n") == ()
