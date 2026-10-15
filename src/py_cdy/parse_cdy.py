"""S-expressions, using ``fix`` for a self-referential grammar.

Grammar::

    program ::= ignore form*
    form   ::= atom | list | quote
    list   ::= '(' form* ')'
    quote  ::= "'" form
    atom   ::= number | string | symbol | '#t' | '#f'
    string ::= '"' (char | escape)* '"'
    escape ::= '\\' ( '\\' | '/' | '"' | 'b' | 'f' | 'n' | 'r' | 't' | 'u' hex{4} )
    ignore ::= (whitespace | ';' <anything up to end of line>)*

Every token is followed by ``ignore``, so comments can appear wherever whitespace can.
"""

from __future__ import annotations

from typing import NamedTuple

from parsec import (
    Parser,
    between,
    char,
    choice,
    fix,
    many,
    parse,
    pure,
    regex,
    skipMany,
    string,
)


class Symbol(NamedTuple):
    """An identifier, e.g. ``define`` or ``*``."""

    name: str


class Number(NamedTuple):
    """An integer literal."""

    value: int


class Str(NamedTuple):
    """A string literal, with escapes already decoded."""

    value: str


class Bool(NamedTuple):
    """``#t`` or ``#f``."""

    value: bool


class SList(NamedTuple):
    """A parenthesised list of forms."""

    items: tuple[SExpr, ...]


SExpr = Symbol | Number | Str | Bool | SList


# Whitespace and ``;`` comments, ported from the pre-schmuz ``doc/hl_rqmt/src/ignore_parse.py``.
whitespace: Parser[str] = regex(r"\s+")
comment: Parser[str] = regex(r";[^\n]*").label("comment")
ignore: Parser[None] = skipMany(whitespace | comment)


def lexeme(p: Parser[str]) -> Parser[str]:
    """Run ``p`` and skip any trailing whitespace and comments."""
    return p << ignore


number: Parser[SExpr] = (
    lexeme(regex(r"-?\d+(?![^\s();])")).map(lambda s: Number(int(s))).label("number")
)
symbol: Parser[SExpr] = (
    lexeme(regex(r"[^\s()'#\d\";][^\s()'\";]*|[-+](?![\d])")).map(Symbol).label("symbol")
)
# String literals, ported from the pre-schmuz ``doc/hl_rqmt/src/atom_parse.py``.
string_part: Parser[str] = regex(r'[^"\\]+')
string_esc: Parser[str] = char("\\") >> choice(
    [
        char("\\"),
        char("/"),
        char('"'),
        char("b") >> pure("\b"),
        char("f") >> pure("\f"),
        char("n") >> pure("\n"),
        char("r") >> pure("\r"),
        char("t") >> pure("\t"),
        regex(r"u[0-9a-fA-F]{4}").map(lambda s: chr(int(s[1:], 16))),
    ]
).label("escape sequence")
str_lit: Parser[SExpr] = (
    lexeme(between(char('"'), char('"'), many(string_part | string_esc)).map("".join))
    .map(Str)
    .label("string")
)
boolean: Parser[SExpr] = (lexeme(string("#t")) >> pure(Bool(True))) | (
    lexeme(string("#f")) >> pure(Bool(False))
)


def form_from(form: Parser[SExpr]) -> Parser[SExpr]:  # pylint: disable=redefined-outer-name
    """One s-expression, given the parser for nested ones."""
    slist = between(lexeme(char("(")), lexeme(char(")")), many(form)).map(SList)
    quote = (lexeme(char("'")) >> form).map(lambda f: SList((Symbol("quote"), f)))
    return choice([number, str_lit, symbol, boolean, slist, quote])


form: Parser[SExpr] = fix(form_from)

program: Parser[tuple[SExpr, ...]] = ignore >> many(form)


if __name__ == "__main__":
    print(parse(program, '(define (sq x) (* x x)) \'(1 2 #t) (put "hi\\tthere")'))
