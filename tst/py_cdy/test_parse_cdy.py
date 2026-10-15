"""Tests for the Candy s-expression reader."""

import pytest
from parsec import ParseFailure, parse

from parse_cdy import (
    Bool,
    Byte,
    Char,
    Double,
    Float,
    Int,
    Long,
    SExpr,
    SList,
    Str,
    Symbol,
    program,
)


def test_atoms() -> None:
    assert parse(program, "42 -7 foo + true false") == (
        Int(42),
        Int(-7),
        Symbol("foo"),
        Symbol("+"),
        Bool(True),
        Bool(False),
    )


def test_nested_list() -> None:
    assert parse(program, "(sq (* x x)) ()") == (
        SList((Symbol("sq"), SList((Symbol("*"), Symbol("x"), Symbol("x"))))),
        SList(()),
    )


@pytest.mark.parametrize("source", ["'x", "'(1 2)", "a'b"])
def test_single_quote_is_reserved(source: str) -> None:
    with pytest.raises(ParseFailure):
        parse(program, source)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ('""', ""),
        ('"hello world"', "hello world"),
        (r'"a\nb\tc"', "a\nb\tc"),
        (r'"say \"hi\""', 'say "hi"'),
        (r'"back\\slash"', "back\\slash"),
        (r'"\/\b\f\r"', "/\b\f\r"),
        (r'"\u00e9"', "é"),
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
    assert parse(program, source) == (SList((Symbol("def"), Symbol("x"), Int(42))),)


def test_comment_inside_list() -> None:
    assert parse(program, "(a ; comment\n b)") == (SList((Symbol("a"), Symbol("b"))),)


def test_comment_ends_a_token() -> None:
    assert parse(program, "42;c\nfoo;c\ntrue;c\n1.5;c\n\\x;c") == (
        Int(42),
        Symbol("foo"),
        Bool(True),
        Double(1.5),
        Char("x"),
    )


def test_semicolon_in_string_is_not_a_comment() -> None:
    assert parse(program, '"a ; b"') == (Str("a ; b"),)


def test_only_comments() -> None:
    assert parse(program, "; nothing here\n;; or here\n") == ()


def test_quote_special_form_is_a_plain_list() -> None:
    assert parse(program, '(quote (a 1 "b"))') == (
        SList((Symbol("quote"), SList((Symbol("a"), Int(1), Str("b"))))),
    )


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("100", Int(100)),
        ("-100", Int(-100)),
        ("1500l", Long(1500)),
        ("3.14f", Float(3.14)),
        ("10.0", Double(10.0)),
        ("-0.5", Double(-0.5)),
        ("1b", Byte(1)),
        ("true", Bool(True)),
        ("false", Bool(False)),
        (r"\e", Char("e")),
        (r"\(", Char("(")),
        ("\\\\", Char("\\")),
        ('\\"', Char('"')),
    ],
)
def test_typed_literals(source: str, expected: SExpr) -> None:
    assert parse(program, source) == (expected,)


def test_literals_in_a_list() -> None:
    assert parse(program, r"(f 1 2l 3.0 4.0f 5b \x true)") == (
        SList(
            (
                Symbol("f"),
                Int(1),
                Long(2),
                Double(3.0),
                Float(4.0),
                Byte(5),
                Char("x"),
                Bool(True),
            )
        ),
    )


@pytest.mark.parametrize("source", ["trueish", "falsey", "true?", "-", "+", "-x"])
def test_symbols_that_look_like_literals(source: str) -> None:
    assert parse(program, source) == (Symbol(source),)


@pytest.mark.parametrize("source", ["12x", "1.5l", "1.5b", "1.", "3f", r"\ab", "\\", "#t", "1500L"])
def test_bad_literals(source: str) -> None:
    with pytest.raises(ParseFailure):
        parse(program, source)
