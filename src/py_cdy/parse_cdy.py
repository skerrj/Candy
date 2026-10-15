r"""S-expressions, using ``fix`` for a self-referential grammar.

Grammar::

    program ::= ignore form*
    form   ::= atom | list
    list   ::= '(' form* ')'
    atom   ::= number | string | char | bool | symbol
    number ::= float | double | long | byte | int
    float  ::= '-'? digit+ '.' digit+ 'f'        ; 3.14f
    double ::= '-'? digit+ '.' digit+            ; 10.0
    long   ::= '-'? digit+ 'l'                   ; 1500l
    byte   ::= '-'? digit+ 'b'                   ; 1b
    int    ::= '-'? digit+                       ; 100
    char   ::= '\\' <one non-space character>   ; \e
    bool   ::= 'true' | 'false'
    string ::= '"' (char | escape)* '"'
    escape ::= '\\' ( '\\' | '/' | '"' | 'b' | 'f' | 'n' | 'r' | 't' | 'u' hex{4} )
    ignore ::= (whitespace | ';' <anything up to end of line>)*

Every token is followed by ``ignore``, so comments can appear wherever whitespace can.

Numbers, chars and booleans must end at a delimiter (whitespace, ``(``, ``)``, ``;`` or the
end of input), so ``12x``, ``\ab`` and ``1.5l`` are errors and ``trueish`` is a symbol.

``'`` is reserved: it is not allowed in symbols and has no syntax yet. Quoting will come
later as a reader macro, as in Clojure.
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
)


class Symbol(NamedTuple):
    """An identifier, e.g. ``define`` or ``*``."""

    name: str


class Int(NamedTuple):
    """An ``Int`` literal: ``100``."""

    value: int


class Long(NamedTuple):
    """A ``Long`` literal: ``1500l``."""

    value: int


class Byte(NamedTuple):
    """A ``Byte`` literal: ``1b``."""

    value: int


class Float(NamedTuple):
    """A ``Float`` literal: ``3.14f``."""

    value: float


class Double(NamedTuple):
    """A ``Double`` literal: ``10.0``."""

    value: float


class Char(NamedTuple):
    """A ``Char`` literal: ``\\e``."""

    value: str


class Str(NamedTuple):
    """A string literal, with escapes already decoded."""

    value: str


class Bool(NamedTuple):
    """``true`` or ``false``."""

    value: bool


class SList(NamedTuple):
    """A parenthesised list of forms."""

    items: tuple[SExpr, ...]


SExpr = Symbol | Int | Long | Byte | Float | Double | Char | Str | Bool | SList


# Whitespace and ``;`` comments, ported from the pre-schmuz ``doc/hl_rqmt/src/ignore_parse.py``.
whitespace: Parser[str] = regex(r"\s+")
comment: Parser[str] = regex(r";[^\n]*").label("comment")
ignore: Parser[None] = skipMany(whitespace | comment)


def lexeme[T](p: Parser[T]) -> Parser[T]:
    """Run ``p`` and skip any trailing whitespace and comments."""
    return p << ignore


# A literal must be followed by a delimiter: whitespace, a paren, a comment or end of input.
END = r"(?![^\s();])"

number_literals: tuple[Parser[SExpr], ...] = (
    regex(rf"-?\d+\.\d+f{END}").map(lambda s: Float(float(s[:-1]))),
    regex(rf"-?\d+\.\d+{END}").map(lambda s: Double(float(s))),
    regex(rf"-?\d+l{END}").map(lambda s: Long(int(s[:-1]))),
    regex(rf"-?\d+b{END}").map(lambda s: Byte(int(s[:-1]))),
    regex(rf"-?\d+{END}").map(lambda s: Int(int(s))),
)
number: Parser[SExpr] = lexeme(choice(number_literals)).label("number")
char_lit: Parser[SExpr] = lexeme(regex(rf"\\\S{END}")).map(lambda s: Char(s[1])).label("char")
boolean: Parser[SExpr] = (
    lexeme(regex(rf"(?:true|false){END}")).map(lambda s: Bool(s == "true")).label("boolean")
)
symbol: Parser[SExpr] = (
    lexeme(regex(r"[^\s()'#\d\";\\][^\s()'\";\\]*|[-+](?![\d])")).map(Symbol).label("symbol")
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


def form_from(form: Parser[SExpr]) -> Parser[SExpr]:  # pylint: disable=redefined-outer-name
    """One s-expression, given the parser for nested ones."""
    slist = between(lexeme(char("(")), lexeme(char(")")), many(form)).map(SList)
    return choice([number, str_lit, char_lit, boolean, symbol, slist])


form: Parser[SExpr] = fix(form_from)

program: Parser[tuple[SExpr, ...]] = ignore >> many(form)


if __name__ == "__main__":
    demo = (
        ";; demo\n(define (sq x) (* x x)) ; square\n"
        '(1 1500l 3.14f 10.0 1b true \\e) (put "hi\\tthere")'
    )
    print(parse(program, demo))
