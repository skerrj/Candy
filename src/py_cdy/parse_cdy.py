"""S-expressions, using ``fix`` for a self-referential grammar.

Grammar::

    form   ::= atom | list | quote
    list   ::= '(' form* ')'
    quote  ::= "'" form
    atom   ::= number | symbol | '#t' | '#f'
"""

from __future__ import annotations

from typing import NamedTuple, Union

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
    spaces,
    string,
)


class Symbol(NamedTuple):
    name: str


class Number(NamedTuple):
    value: int


class Bool(NamedTuple):
    value: bool


class SList(NamedTuple):
    items: tuple[SExpr, ...]


SExpr = Union[Symbol, Number, Bool, SList]


def lexeme(p: Parser[str]) -> Parser[str]:
    return p << spaces


number: Parser[SExpr] = lexeme(regex(r"-?\d+(?![^\s()])")).map(lambda s: Number(int(s))).label("number")
symbol: Parser[SExpr] = lexeme(regex(r"[^\s()'#\d][^\s()']*|[-+](?![\d])")).map(Symbol).label("symbol")
boolean: Parser[SExpr] = (lexeme(string("#t")) >> pure(Bool(True))) | (lexeme(string("#f")) >> pure(Bool(False)))


def form_from(form: Parser[SExpr]) -> Parser[SExpr]:
    """One s-expression, given the parser for nested ones."""
    slist = between(lexeme(char("(")), lexeme(char(")")), many(form)).map(SList)
    quote = (lexeme(char("'")) >> form).map(lambda f: SList((Symbol("quote"), f)))
    return choice([number, symbol, boolean, slist, quote])


form: Parser[SExpr] = fix(form_from)

program: Parser[tuple[SExpr, ...]] = spaces >> many(form)


if __name__ == "__main__":
    print(parse(program, "(define (sq x) (* x x)) '(1 2 #t)"))
