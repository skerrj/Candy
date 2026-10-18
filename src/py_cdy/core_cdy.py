"""Core AST and ``analyse``: parsed Candy forms, checked and resolved, for any target.

This is the first of the translator's three steps (see "Layers" in
``doc/hl_rqmt/iMVP_py_translator.md``): ``analyse`` turns the parser's generic ``SList``s
into one node per form and checks their shape. It also:

- expands ``cond`` into nested ``If``s;
- checks ``match`` clauses against the ``deft`` sum type they take apart (one clause per
  variant, or an ``else``);
- desugars ``let`` into nested applied ``Fn``s, as in Scheme, so Core has no ``Let`` node
  (``lower`` turns them back into assignments); a destructuring binding ``((x y) e)``
  becomes a binding for ``e`` and one ``at`` call per name;
- resolves every symbol to a ``Local`` (with a unique id), a ``Global`` (a top-level name
  in this file) or a ``Prim`` (an entry in the ``cdy_rt`` table);
- checks the ``sig`` rules (required, before its definition) and attaches each signature
  to its definition;
- allows definitions (``def``, ``defn``, ``deft``, ``sig``) only at top level: they are
  ``TopLevel`` nodes, and ``Expr``, what ``analyse_expr`` returns, has no definition nodes.

Nothing here knows about Python. Errors are ``CandyError``s, without source positions.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from functools import reduce
from types import MappingProxyType
from typing import NamedTuple

from parsec import ParseFailure, parse

from cdy_rt.table import INITIAL_TABLE, Table
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


class CandyError(Exception):
    """A Candy program that isn't valid: a malformed form, an unknown name, a missing sig."""


# --- types (from ``sig`` and ``deft``) ---


class TCon(NamedTuple):
    """A named type, possibly applied to arguments: ``Int``, ``(List Int)``, ``Vector2``."""

    name: str
    args: tuple[CdyType, ...] = ()


class TVar(NamedTuple):
    """A type variable: a lowercase name such as ``a``."""

    name: str


class TFn(NamedTuple):
    """A function type: ``(Fn (A B) R)``."""

    params: tuple[CdyType, ...]
    ret: CdyType


CdyType = TCon | TVar | TFn  # a Candy type (pylint rejects alias names starting with "Type")

# Built-in type names and how many arguments each takes (``None``: one or more).
BUILTIN_TYPES: Mapping[str, int | None] = MappingProxyType(
    {
        "Int": 0,
        "Long": 0,
        "Byte": 0,
        "Float": 0,
        "Double": 0,
        "Bool": 0,
        "Char": 0,
        "String": 0,
        "Unit": 0,
        "Any": 0,
        "Maybe": 1,
        "List": 1,
        "Map": 2,
        "Tup": None,
    }
)


# --- expressions ---


class Lit(NamedTuple):
    """A literal, with its Candy type name. ``nil``/missing values are ``Lit(None, "Unit")``."""

    value: int | float | bool | str | None
    ctype: str


class Local(NamedTuple):
    """A local binding (parameter or ``let``); ``id`` tells same-named bindings apart."""

    name: str
    id: int


class Global(NamedTuple):
    """A top-level name defined in this file (``def``, ``defn`` or a ``deft`` constructor)."""

    name: str


class Prim(NamedTuple):
    """A built-in from the ``cdy_rt`` table, by its Candy name: ``+``, ``slurp``, ``nil``."""

    name: str


class Call(NamedTuple):
    """``(f a b)``."""

    fn: Expr
    args: tuple[Expr, ...]


class If(NamedTuple):
    """``(if test then other)``; a missing ``other`` is ``nil``."""

    test: Expr
    then: Expr
    other: Expr


class Do(NamedTuple):
    """``(do e1 ... en)``, with two or more expressions."""

    body: tuple[Expr, ...]


class Fn(NamedTuple):
    """``(fn (params+) body)``; also what ``let`` desugars into."""

    params: tuple[Local, ...]
    body: Expr


class Tup(NamedTuple):
    """``(tup a b)``."""

    items: tuple[Expr, ...]


class Format(NamedTuple):
    """``(format "x: {x}")``: literal text and holes, in order."""

    parts: tuple[str | Expr, ...]


class Get(NamedTuple):
    """``(get obj field)``."""

    obj: Expr
    field: str


class Assoc(NamedTuple):
    """``(assoc obj field value ...)``: a copy of ``obj`` with fields replaced."""

    obj: Expr
    fields: tuple[tuple[str, Expr], ...]


class Clause(NamedTuple):
    """One ``((Variant a b) body)`` clause of a ``match``: each bound name with its field
    (``_`` binds nothing)."""

    variant: str
    binds: tuple[tuple[str, Local], ...]
    body: Expr


class Match(NamedTuple):
    """``(match subject clause+ (else expr)?)``; ``default`` is the ``else``, if any."""

    subject: Expr
    clauses: tuple[Clause, ...]
    default: Expr | None


Expr = Lit | Local | Global | Prim | Call | If | Do | Fn | Tup | Format | Get | Assoc | Match


# --- top-level forms ---


class Def(NamedTuple):
    """``(def name init)``, with the type from its ``sig``."""

    name: str
    init: Expr
    sig: CdyType


class Defn(NamedTuple):
    """``(defn name (params+) body)``, with the function type from its ``sig``."""

    name: str
    params: tuple[Local, ...]
    body: Expr
    sig: TFn


class Deft(NamedTuple):
    """``(deft Name ((field Type)+))`` or ``(deft (Name a b) (...))``: a record type."""

    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, CdyType], ...]


class Variant(NamedTuple):
    """One variant of a sum type: ``(Circle ((r Double)))``, or ``(Leaf)`` with no fields."""

    name: str
    fields: tuple[tuple[str, CdyType], ...]


class DeftSum(NamedTuple):
    """``(deft Name variant+)`` or ``(deft (Name a b) variant+)``: a sum type."""

    name: str
    tvars: tuple[str, ...]
    variants: tuple[Variant, ...]


TopLevel = Def | Defn | Deft | DeftSum | Expr

LIT_TYPES: Mapping[type, str] = MappingProxyType(
    {
        Int: "Int",
        Long: "Long",
        Byte: "Byte",
        Float: "Float",
        Double: "Double",
        Char: "Char",
        Str: "String",
        Bool: "Bool",
    }
)
NIL = Lit(None, "Unit")
TOP_ONLY = frozenset({"def", "defn", "deft", "sig"})
NOT_IN_IMVP = frozenset({"import", "quote"})
DEFINERS = frozenset({"def", "defn", "deft"})


class VariantInfo(NamedTuple):
    """What ``match`` and calls need to know about a variant, before its ``deft`` is analysed."""

    sum_name: str
    fields: tuple[str, ...]


NO_VARIANTS: Mapping[str, VariantInfo] = MappingProxyType({})


class Scope(NamedTuple):
    """What a symbol can refer to at one point in the program."""

    env: Mapping[str, Local]  # local bindings in scope
    top: frozenset[str]  # top-level value names defined anywhere in this file
    table: Table  # built-ins
    variants: Mapping[str, VariantInfo] = NO_VARIANTS  # sum type variants in this file


def show(form: SExpr) -> str:
    """``form`` written back as Candy source (for error messages)."""
    match form:
        case Symbol(name):
            return name
        case SList(items):
            return "(" + " ".join(show(item) for item in items) + ")"
        case Str(value):
            return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
        case Char(value):
            return "\\" + value
        case Bool(value):
            return "true" if value else "false"
        case Long(value):
            return f"{value}l"
        case Byte(value):
            return f"{value}b"
        case Float(value):
            return f"{value}f"
        case Int(value) | Double(value):
            return str(value)


# --- types ---


def analyse_type(form: SExpr, known: Mapping[str, int | None]) -> CdyType:
    """The type written as ``form``; ``known`` maps type names to their argument counts."""
    match form:
        case Symbol(name) if name[:1].islower():
            return TVar(name)
        case Symbol(name):
            check_type_arity(name, 0, known)
            return TCon(name)
        case SList((Symbol("Fn"), SList(params), ret)) if params:
            return TFn(tuple(analyse_type(p, known) for p in params), analyse_type(ret, known))
        case SList((Symbol("Fn"), *_)):
            raise CandyError(f"bad function type {show(form)}: expected (Fn (Arg+) Ret)")
        case SList((Symbol(name), *args)) if name[:1].isupper() and args:
            check_type_arity(name, len(args), known)
            return TCon(name, tuple(analyse_type(a, known) for a in args))
        case _:
            raise CandyError(f"bad type {show(form)}")


def check_type_arity(name: str, count: int, known: Mapping[str, int | None]) -> None:
    """Fail unless ``name`` is a known type that takes ``count`` arguments."""
    if name not in known:
        raise CandyError(f"unknown type {name}")
    expected = known[name]
    if expected is None:
        if count == 0:
            raise CandyError(f"type {name} needs at least one argument")
    elif count != expected:
        raise CandyError(f"type {name} takes {expected} argument(s), not {count}")


def type_vars(t: CdyType) -> frozenset[str]:
    """The type variables used in ``t``."""
    match t:
        case TVar(name):
            return frozenset({name})
        case TCon(_, args):
            return frozenset().union(*(type_vars(a) for a in args))
        case TFn(params, ret):
            return frozenset().union(type_vars(ret), *(type_vars(p) for p in params))


# --- expressions ---


def analyse_expr(form: SExpr, scope: Scope, n: int) -> tuple[Expr, int]:
    """``form`` as a Core expression. ``n`` is the next free ``Local`` id; returns the new one."""
    match form:
        case Symbol(name):
            return resolve(name, scope), n
        case SList(()):
            raise CandyError("empty form (): use empty-list for an empty list")
        case SList((Symbol(head), *rest)) if head in SPECIAL and head not in scope.env:
            return SPECIAL[head](tuple(rest), scope, n)
        case SList(items):
            check_variant_call(items[0], len(items) - 1, scope)
            fn, n = analyse_expr(items[0], scope, n)
            args_e, n = analyse_all(items[1:], scope, n)
            check_call(fn, args_e, scope.table)
            return Call(fn, args_e), n
        case (
            Int(value)
            | Long(value)
            | Byte(value)
            | Float(value)
            | Double(value)
            | Char(value)
            | Str(value)
            | Bool(value)
        ):
            return Lit(value, LIT_TYPES[type(form)]), n


def analyse_all(forms: Sequence[SExpr], scope: Scope, n: int) -> tuple[tuple[Expr, ...], int]:
    """Each of ``forms`` as a Core expression, in order."""

    def step(acc: tuple[tuple[Expr, ...], int], form: SExpr) -> tuple[tuple[Expr, ...], int]:
        expr, m = analyse_expr(form, scope, acc[1])
        return (*acc[0], expr), m

    start: tuple[tuple[Expr, ...], int] = ((), n)
    return reduce(step, forms, start)


def resolve(name: str, scope: Scope) -> Expr:
    """What the symbol ``name`` refers to: a local, then a top-level name, then the table."""
    if name in scope.env:
        return scope.env[name]
    if name in scope.top:
        info = scope.variants.get(name)
        if info is not None and not info.fields:
            return Call(Global(name), ())  # a variant with no fields is a value: Leaf
        return Global(name)
    if name in scope.table:
        if scope.table[name].kind == "special":
            raise CandyError(f"{name} is a special form, not a value")
        return Prim(name)
    raise CandyError(f"unknown name {name}")


def check_variant_call(head: SExpr, count: int, scope: Scope) -> None:
    """Fail if ``head`` names a variant that is called with the wrong number of fields."""
    if not isinstance(head, Symbol) or head.name in scope.env or head.name not in scope.variants:
        return
    fields = scope.variants[head.name].fields
    if not fields:
        raise CandyError(
            f"{head.name} has no fields, so it is a value: write {head.name}, not ({head.name})"
        )
    if count != len(fields):
        raise CandyError(f"({head.name} ...) takes {len(fields)} field(s), got {count}")


def check_call(fn: Expr, args: tuple[Expr, ...], table: Table) -> None:
    """Fail if ``fn`` is a built-in called with the wrong number of arguments."""
    if not isinstance(fn, Prim):
        return
    entry = table[fn.name]
    if entry.kind in ("binop", "compare", "boolop") and len(args) < 2:
        raise CandyError(f"({fn.name} ...) needs at least 2 arguments, got {len(args)}")
    if entry.arity is not None and len(args) != entry.arity:
        raise CandyError(f"({fn.name} ...) takes {entry.arity} argument(s), got {len(args)}")


def binder(form: SExpr, what: str, table: Table) -> str:
    """The name bound by ``form`` (a parameter, ``let`` name, field or definition)."""
    if not isinstance(form, Symbol):
        raise CandyError(f"{what} must be a name, not {show(form)}")
    if form.name in table and table[form.name].kind == "special":
        raise CandyError(f"{what} can't be the special form name {form.name}")
    return form.name


def bind_params(
    forms: Sequence[SExpr], what: str, scope: Scope, n: int
) -> tuple[tuple[Local, ...], Scope, int]:
    """Fresh ``Local``s for the parameter names ``forms``, and the scope that includes them."""
    names = tuple(binder(f, what, scope.table) for f in forms)
    if not names:
        raise CandyError(f"{what}s: at least one is needed")
    if len(set(names)) != len(names):
        raise CandyError(f"{what}s must be different: {' '.join(names)}")
    params = tuple(Local(name, n + i) for i, name in enumerate(names))
    env = {**scope.env, **{p.name: p for p in params}}
    return params, scope._replace(env=MappingProxyType(env)), n + len(params)


def with_local(scope: Scope, local: Local) -> Scope:
    """``scope`` with ``local`` bound."""
    return scope._replace(env=MappingProxyType({**scope.env, local.name: local}))


def nest(pairs: Sequence[tuple[Local, Expr]], body: Expr) -> Expr:
    """Sequential bindings as nested applied lambdas: ``((fn (a) ((fn (b) body) e2)) e1)``."""

    def wrap(inner: Expr, pair: tuple[Local, Expr]) -> Expr:
        return Call(Fn((pair[0],), inner), (pair[1],))

    return reduce(wrap, reversed(pairs), body)


# --- special forms (expression position) ---

Special = Callable[[tuple[SExpr, ...], Scope, int], tuple[Expr, int]]


def an_if(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(if test then other?)``."""
    if len(rest) not in (2, 3):
        raise CandyError("if: expected (if test then else?)")
    parts, n = analyse_all(rest, scope, n)
    return If(parts[0], parts[1], parts[2] if len(parts) == 3 else NIL), n


def an_cond(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(cond (test expr)+ (else expr)?)``, as nested ``If``s."""
    if not rest:
        raise CandyError("cond: needs at least one (test expr) clause")
    clauses: list[tuple[SExpr, SExpr]] = []
    for i, clause in enumerate(rest):
        if not isinstance(clause, SList) or len(clause.items) != 2:
            raise CandyError(f"cond: clause must be (test expr), not {show(clause)}")
        if clause.items[0] == Symbol("else") and i != len(rest) - 1:
            raise CandyError("cond: (else expr) must be the last clause")
        clauses.append((clause.items[0], clause.items[1]))
    if clauses[-1][0] == Symbol("else"):
        other, n = analyse_expr(clauses.pop()[1], scope, n)
    else:
        other = NIL
    for test_f, expr_f in reversed(clauses):
        test, n = analyse_expr(test_f, scope, n)
        expr, n = analyse_expr(expr_f, scope, n)
        other = If(test, expr, other)
    return other, n


def an_do(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(do expr*)``."""
    body, n = analyse_all(rest, scope, n)
    if not body:
        return NIL, n
    return (body[0] if len(body) == 1 else Do(body)), n


def an_let(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(let ((name init)*) body)``: sequential, desugared into nested applied ``Fn``s."""
    if len(rest) != 2 or not isinstance(rest[0], SList):
        raise CandyError("let: expected (let ((name init)*) body)")
    pairs: list[tuple[Local, Expr]] = []
    for binding in rest[0].items:
        if not isinstance(binding, SList) or len(binding.items) != 2:
            raise CandyError(f"let: binding must be (name init), not {show(binding)}")
        target, init_f = binding.items
        init, n = analyse_expr(init_f, scope, n)
        if isinstance(target, SList):  # destructuring: ((x y) e)
            tup_local = Local("_tup", n)
            n += 1
            pairs.append((tup_local, init))
            names, _, _ = bind_params(target.items, "let name", scope, n)
            for i, name in enumerate(names):
                local = Local(name.name, n)
                n += 1
                pairs.append((local, Call(Prim("at"), (tup_local, Lit(i, "Int")))))
                scope = with_local(scope, local)
        else:
            local = Local(binder(target, "let name", scope.table), n)
            n += 1
            pairs.append((local, init))
            scope = with_local(scope, local)
    body, n = analyse_expr(rest[1], scope, n)
    return nest(pairs, body), n


def an_fn(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(fn (params+) body)``."""
    if len(rest) != 2 or not isinstance(rest[0], SList):
        raise CandyError("fn: expected (fn (args+) body), with exactly one body form")
    params, inner, n = bind_params(rest[0].items, "fn argument", scope, n)
    body, n = analyse_expr(rest[1], inner, n)
    return Fn(params, body), n


def an_tup(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(tup expr+)``."""
    if not rest:
        raise CandyError("tup: needs at least one item")
    items, n = analyse_all(rest, scope, n)
    return Tup(items), n


# ``{{`` and ``}}`` are literal braces; ``{form}`` is a hole; anything else is text.
FORMAT_TOKEN = re.compile(r"\{\{|\}\}|\{([^{}]*)\}|([^{}]+)|([{}])")


def an_format(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(format "text {form} ...")``: an f-string whose holes hold Candy forms (from smz)."""
    if len(rest) != 1 or not isinstance(rest[0], Str):
        raise CandyError("format: expected one string literal")
    parts: list[str | Expr] = []
    for m in FORMAT_TOKEN.finditer(rest[0].value):
        hole, text, brace = m.groups()
        if brace is not None:
            raise CandyError(f"format: unmatched {brace} (write {brace}{brace} for a brace)")
        if hole is None:
            piece = text if text is not None else m.group()[0]
            if parts and isinstance(parts[-1], str):
                parts[-1] += piece
            else:
                parts.append(piece)
            continue
        try:
            forms = parse(program, hole)
        except ParseFailure as err:
            raise CandyError(f"format: can't parse {{{hole}}}: {err}") from err
        if len(forms) != 1:
            raise CandyError(f"format: {{{hole}}} must hold exactly one form")
        expr, n = analyse_expr(forms[0], scope, n)
        parts.append(expr)
    return Format(tuple(parts)), n


def an_get(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(get obj field)``."""
    if len(rest) != 2:
        raise CandyError("get: expected (get obj field)")
    obj, n = analyse_expr(rest[0], scope, n)
    return Get(obj, binder(rest[1], "get field", scope.table)), n


def an_assoc(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(assoc obj field value ...)``."""
    if len(rest) < 3 or len(rest) % 2 == 0:
        raise CandyError("assoc: expected (assoc obj field value ...)")
    obj, n = analyse_expr(rest[0], scope, n)
    names = tuple(binder(f, "assoc field", scope.table) for f in rest[1::2])
    if len(set(names)) != len(names):
        raise CandyError(f"assoc: a field is given twice: {' '.join(names)}")
    values, n = analyse_all(rest[2::2], scope, n)
    return Assoc(obj, tuple(zip(names, values, strict=True))), n


def an_match(rest: tuple[SExpr, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    """``(match subject ((Variant name*) expr)+ (else expr)?)``."""
    if len(rest) < 2:
        raise CandyError("match: expected (match subject ((Variant name*) expr)+ (else expr)?)")
    subject, n = analyse_expr(rest[0], scope, n)
    clauses: list[Clause] = []
    default: Expr | None = None
    sums: set[str] = set()
    for i, clause in enumerate(rest[1:], start=1):
        if not isinstance(clause, SList) or len(clause.items) != 2:
            raise CandyError(f"match: clause must be (pattern expr), not {show(clause)}")
        pattern, body_f = clause.items
        if pattern == Symbol("else"):
            if i != len(rest) - 1 or not clauses:
                raise CandyError("match: (else expr) must be the last clause, after a pattern")
            default, n = analyse_expr(body_f, scope, n)
            continue
        variant, names = match_pattern(pattern, scope)
        if any(c.variant == variant for c in clauses):
            raise CandyError(f"match: more than one clause for {variant}")
        sums.add(scope.variants[variant].sum_name)
        fields = scope.variants[variant].fields
        named = [(field, name) for field, name in zip(fields, names, strict=True) if name != "_"]
        binds = tuple((field, Local(name, n + j)) for j, (field, name) in enumerate(named))
        n += len(binds)
        inner = reduce(with_local, (local for _, local in binds), scope)
        body, n = analyse_expr(body_f, inner, n)
        clauses.append(Clause(variant, binds, body))
    if len(sums) > 1:
        raise CandyError(f"match: clauses mix variants of {', '.join(sorted(sums))}")
    if default is None:
        sum_name = next(iter(sums))
        missing = sorted(
            v
            for v, info in scope.variants.items()
            if info.sum_name == sum_name and all(c.variant != v for c in clauses)
        )
        if missing:
            raise CandyError(
                f"match on {sum_name}: no clause for {', '.join(missing)} (or add else)"
            )
    return Match(subject, tuple(clauses), default), n


def match_pattern(pattern: SExpr, scope: Scope) -> tuple[str, tuple[str, ...]]:
    """The variant and the names bound by a ``(Variant name*)`` pattern."""
    match pattern:
        case SList((Symbol(variant), *binds)) if variant in scope.variants:
            fields = scope.variants[variant].fields
            if len(binds) != len(fields):
                raise CandyError(
                    f"match: {variant} has {len(fields)} field(s), so the pattern needs "
                    f"{len(fields)} name(s), not {len(binds)}"
                )
            names = tuple(binder(b, "match name", scope.table) for b in binds)
            real = [name for name in names if name != "_"]
            if len(set(real)) != len(real):
                raise CandyError(f"match: names in a pattern must be different: {show(pattern)}")
            return variant, names
        case SList((Symbol(variant), *_)):
            raise CandyError(f"match: {variant} is not a variant of a sum type")
        case _:
            raise CandyError(f"match: pattern must be (Variant name*) or else, not {show(pattern)}")


def top_only(name: str) -> Special:
    """A handler for a definition form found inside an expression."""

    def fail(_rest: tuple[SExpr, ...], _scope: Scope, _n: int) -> tuple[Expr, int]:
        raise CandyError(f"{name} is only allowed at top level")

    return fail


def not_in_imvp(name: str) -> Special:
    """A handler for a form the iMVP skips."""

    def fail(_rest: tuple[SExpr, ...], _scope: Scope, _n: int) -> tuple[Expr, int]:
        raise CandyError(f"{name} is not supported in the iMVP")

    return fail


SPECIAL: Mapping[str, Special] = MappingProxyType(
    {
        "if": an_if,
        "cond": an_cond,
        "do": an_do,
        "let": an_let,
        "fn": an_fn,
        "tup": an_tup,
        "format": an_format,
        "get": an_get,
        "assoc": an_assoc,
        "match": an_match,
        **{name: top_only(name) for name in TOP_ONLY},
        **{name: not_in_imvp(name) for name in NOT_IN_IMVP},
    }
)


# --- top level ---


class Program(NamedTuple):
    """The state while analysing a file's top-level forms in order."""

    out: tuple[TopLevel, ...]
    sigs: Mapping[str, CdyType]  # signatures seen so far
    defined: frozenset[str]  # value names defined so far
    n: int  # next free Local id


class Names(NamedTuple):
    """The top-level names a file defines, found before analysing it."""

    values: frozenset[str]  # def, defn, deft constructor and variant names
    sig_names: frozenset[str]  # names that need a sig: def and defn
    types: Mapping[str, int | None]  # built-in and deft type names, with argument counts
    variants: Mapping[str, VariantInfo] = NO_VARIANTS  # sum type variants


def is_sum(body: Sequence[SExpr]) -> bool:
    """Whether a ``deft`` body (what follows the name) lists variants, not one field list.

    A product's field list starts with a list, ``((x Int) ...)``; each variant starts with a
    symbol, ``(Circle ...)`` or ``(Leaf)``.
    """
    return bool(body) and all(
        isinstance(v, SList) and bool(v.items) and isinstance(v.items[0], Symbol) for v in body
    )


def variant_forms(body: Sequence[SExpr]) -> tuple[tuple[SExpr, tuple[SExpr, ...]], ...]:
    """Each variant of a sum ``deft`` body: its name form and its field forms."""
    out: list[tuple[SExpr, tuple[SExpr, ...]]] = []
    for form in body:
        assert isinstance(form, SList)
        match form.items:
            case (name,):
                out.append((name, ()))
            case (name, SList(fields)) if fields:
                out.append((name, fields))
            case _:
                raise CandyError(
                    f"deft: variant must be (Name) or (Name ((field Type)+)), not {show(form)}"
                )
    return tuple(out)


def field_names(fields: Sequence[SExpr]) -> tuple[str, ...]:
    """The names of ``(field Type)`` forms, as far as they can be read (checked later)."""
    return tuple(
        f.items[0].name
        if isinstance(f, SList) and f.items and isinstance(f.items[0], Symbol)
        else "?"
        for f in fields
    )


def top_names(forms: Sequence[SExpr], table: Table) -> Names:
    """Every name defined at top level in ``forms``; fails if one is defined twice."""
    found: list[tuple[str, str, int]] = []  # (form, name, type parameter count)
    variants: dict[str, VariantInfo] = {}
    for form in forms:
        match form:
            case SList((Symbol("deft" as head), name_f, *body)):
                head_forms = name_f.items if isinstance(name_f, SList) else (name_f,)
                if not head_forms:
                    raise CandyError("deft: expected (deft Name ((field Type)+))")
                name = binder(head_forms[0], "deft name", table)
                found.append(("sum" if is_sum(body) else head, name, len(head_forms) - 1))
                if is_sum(body):
                    for v_name_f, fields in variant_forms(body):
                        v_name = binder(v_name_f, "deft variant name", table)
                        found.append(("variant", v_name, 0))
                        variants[v_name] = VariantInfo(name, field_names(fields))
            case SList((Symbol(head), name, *_)) if head in DEFINERS:
                found.append((head, binder(name, f"{head} name", table), 0))
            case _:
                pass
    # A sum type's name is a type, not a value, but in Python it is a name like the others.
    names = [name for _, name, _ in found]
    twice = sorted({name for name in names if names.count(name) > 1})
    if twice:
        raise CandyError(f"defined more than once: {', '.join(twice)}")
    deft_types = {name: count for head, name, count in found if head in ("deft", "sum")}
    return Names(
        values=frozenset(name for head, name, _ in found if head != "sum"),
        sig_names=frozenset(name for head, name, _ in found if head in ("def", "defn")),
        types=MappingProxyType({**BUILTIN_TYPES, **deft_types}),
        variants=MappingProxyType(variants),
    )


def analyse_program(forms: Sequence[SExpr], table: Table = INITIAL_TABLE) -> tuple[TopLevel, ...]:
    """A whole Candy file's top-level forms, analysed in order."""
    names = top_names(forms, table)
    scope = Scope(MappingProxyType({}), names.values, table, names.variants)

    def step(prog: Program, form: SExpr) -> Program:
        match form:
            case SList((Symbol("sig"), *rest)):
                return top_sig(tuple(rest), prog, names)
            case SList((Symbol("def"), *rest)):
                return top_def(tuple(rest), prog, scope)
            case SList((Symbol("defn"), *rest)):
                return top_defn(tuple(rest), prog, scope)
            case SList((Symbol("deft"), *rest)):
                return top_deft(tuple(rest), prog, names)
            case _:
                expr, n = analyse_expr(form, scope, prog.n)
                return prog._replace(out=(*prog.out, expr), n=n)

    start = Program((), MappingProxyType({}), frozenset(), 0)
    return reduce(step, forms, start).out


def top_sig(rest: tuple[SExpr, ...], prog: Program, names: Names) -> Program:
    """``(sig name Type)``: record the signature for a later ``def`` or ``defn``."""
    if len(rest) != 2 or not isinstance(rest[0], Symbol):
        raise CandyError("sig: expected (sig name Type)")
    name = rest[0].name
    if name not in names.sig_names:
        raise CandyError(f"sig for {name}, but no def or defn of {name} in this file")
    if name in prog.defined:
        raise CandyError(f"sig for {name} comes after its definition")
    if name in prog.sigs:
        raise CandyError(f"more than one sig for {name}")
    sig = analyse_type(rest[1], names.types)
    return prog._replace(sigs=MappingProxyType({**prog.sigs, name: sig}))


def needs_sig(name: str, prog: Program) -> CdyType:
    """The signature for ``name``, which must come before its definition."""
    if name not in prog.sigs:
        raise CandyError(f"{name} needs a (sig {name} Type) before its definition")
    return prog.sigs[name]


def top_def(rest: tuple[SExpr, ...], prog: Program, scope: Scope) -> Program:
    """``(def name init)``."""
    if len(rest) != 2:
        raise CandyError("def: expected (def name init); the initial value is required")
    name = binder(rest[0], "def name", scope.table)
    sig = needs_sig(name, prog)
    init, n = analyse_expr(rest[1], scope, prog.n)
    return prog._replace(out=(*prog.out, Def(name, init, sig)), defined=prog.defined | {name}, n=n)


def top_defn(rest: tuple[SExpr, ...], prog: Program, scope: Scope) -> Program:
    """``(defn name (args+) body)``."""
    if len(rest) != 3 or not isinstance(rest[1], SList):
        raise CandyError("defn: expected (defn name (args+) body), with exactly one body form")
    name = binder(rest[0], "defn name", scope.table)
    sig = needs_sig(name, prog)
    if not isinstance(sig, TFn):
        raise CandyError(f"defn {name}: its sig must be a function type (Fn (Arg+) Ret)")
    params, inner, n = bind_params(rest[1].items, "defn argument", scope, prog.n)
    if len(params) != len(sig.params):
        raise CandyError(
            f"defn {name} takes {len(params)} argument(s), but its sig has {len(sig.params)}"
        )
    body, n = analyse_expr(rest[2], inner, n)
    return prog._replace(
        out=(*prog.out, Defn(name, params, body, sig)), defined=prog.defined | {name}, n=n
    )


def top_deft(rest: tuple[SExpr, ...], prog: Program, names: Names) -> Program:
    """A record, ``(deft Name ((field Type)+))``, or a sum, ``(deft Name variant+)``.

    Either can be generic: ``(deft (Name a b) ...)``.
    """
    usage = "deft: expected (deft Name ((field Type)+)) or (deft Name (Variant ((field Type)+))+)"
    if len(rest) < 2:
        raise CandyError(usage)
    head = rest[0].items if isinstance(rest[0], SList) else (rest[0],)
    name = binder(head[0], "deft name", INITIAL_TABLE)
    tvars = tuple(binder(t, "deft type variable", INITIAL_TABLE) for t in head[1:])
    if not name[:1].isupper() or not all(t[:1].islower() for t in tvars):
        raise CandyError(f"deft {name}: type names are Capitalised, type variables lowercase")
    body = rest[1:]
    if is_sum(body):
        variants: list[Variant] = []
        for v_name_f, field_forms in variant_forms(body):
            v_name = binder(v_name_f, "deft variant name", INITIAL_TABLE)
            if not v_name[:1].isupper():
                raise CandyError(f"deft {name}: variant names are Capitalised, not {v_name}")
            variants.append(
                Variant(v_name, deft_fields(f"deft {name} {v_name}", field_forms, tvars, names))
            )
        defined = prog.defined | {name} | {v.name for v in variants}
        return prog._replace(
            out=(*prog.out, DeftSum(name, tvars, tuple(variants))), defined=defined
        )
    if len(rest) != 2 or not isinstance(rest[1], SList) or not rest[1].items:
        raise CandyError(usage)
    fields = deft_fields(f"deft {name}", rest[1].items, tvars, names)
    return prog._replace(out=(*prog.out, Deft(name, tvars, fields)), defined=prog.defined | {name})


def deft_fields(
    what: str, forms: Sequence[SExpr], tvars: tuple[str, ...], names: Names
) -> tuple[tuple[str, CdyType], ...]:
    """The ``(field Type)`` forms of a record or a variant."""
    fields: list[tuple[str, CdyType]] = []
    for field in forms:
        if not isinstance(field, SList) or len(field.items) != 2:
            raise CandyError(f"{what}: field must be (name Type), not {show(field)}")
        field_type = analyse_type(field.items[1], names.types)
        unknown = type_vars(field_type) - set(tvars)
        if unknown:
            raise CandyError(f"{what}: unknown type variable(s) {', '.join(sorted(unknown))}")
        fields.append((binder(field.items[0], "deft field", INITIAL_TABLE), field_type))
    field_list = [f for f, _ in fields]
    if len(set(field_list)) != len(field_list):
        raise CandyError(f"{what}: a field is given twice")
    return tuple(fields)
