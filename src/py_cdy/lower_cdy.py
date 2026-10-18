"""The lowered IR (the "pseudo-AST") and ``lower``: Core expressions split into statements.

This is the second of the translator's three steps (see "Layers" in
``doc/hl_rqmt/iMVP_py_translator.md``). In Candy every form is an expression; in the
statement-based targets (Python, C, Java, ...) many things are statements. ``lower`` turns
each Core expression into the statements that must run first plus an expression for its
value, in one of three modes:

- ``value``: an expression is needed (an argument, an init, a test);
- ``tail``: the last form of a function body, which ``return``s its value;
- ``effect``: the value is thrown away (top-level forms, all but the last form of a ``do``).

Temporaries (``Temp``) appear only where Candy nests a statement inside an expression, and
keep the evaluation order. ``let``, which arrives from Core as applied ``Fn``s, becomes plain
assignments again. Names are still Core bindings (``Local`` ids, ``Global``, ``Prim``);
choosing target spellings is the backend's job. ``Caps`` says which expressions the target
has; the IR itself is target-neutral.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import NamedTuple

from cdy_rt.table import INITIAL_TABLE, Table
from core_cdy import (
    Assoc,
    Call,
    CdyType,
    Def,
    Defn,
    Deft,
    Do,
    Expr,
    Fn,
    Format,
    Get,
    Global,
    If,
    Lit,
    Local,
    Prim,
    TFn,
    TopLevel,
    Tup,
)


class Caps(NamedTuple):
    """What a target's expressions can hold; ``lower`` falls back to statements otherwise."""

    cond_expr: bool  # a conditional expression, like Python's ``a if t else b``
    lambda_expr: bool  # an anonymous function whose body is one expression


PY_CAPS = Caps(cond_expr=True, lambda_expr=True)


# --- IR expressions ---


class Temp(NamedTuple):
    """A temporary made by ``lower``; the backend names it (``_cdy_t1``, ...)."""

    id: int


class Const(NamedTuple):
    """A constant, with its Candy type name."""

    value: int | float | bool | str | None
    ctype: str


class CallE(NamedTuple):
    """A call: ``fn(args...)``."""

    fn: IrExpr
    args: tuple[IrExpr, ...]


class Op(NamedTuple):
    """A built-in operator (``binop``, ``compare``, ``boolop`` or ``unary`` table entry)."""

    prim: str
    args: tuple[IrExpr, ...]


class CondE(NamedTuple):
    """A conditional expression: ``then if test else other``."""

    test: IrExpr
    then: IrExpr
    other: IrExpr


class LambdaE(NamedTuple):
    """An anonymous function whose body is one expression."""

    params: tuple[Local, ...]
    body: IrExpr


class TupleE(NamedTuple):
    """A tuple."""

    items: tuple[IrExpr, ...]


class FormatE(NamedTuple):
    """A format string: literal text and expressions, in order."""

    parts: tuple[str | IrExpr, ...]


class GetE(NamedTuple):
    """A record field: ``obj.field``."""

    obj: IrExpr
    field: str


class AssocE(NamedTuple):
    """A copy of a record with fields replaced."""

    obj: IrExpr
    fields: tuple[tuple[str, IrExpr], ...]


Name = Local | Global | Temp
IrExpr = Name | Prim | Const | CallE | Op | CondE | LambdaE | TupleE | FormatE | GetE | AssocE


# --- IR statements ---


class Assign(NamedTuple):
    """``target = value``; ``sig`` is the declared type, for a top-level ``def``."""

    target: Name
    value: IrExpr
    sig: CdyType | None = None


class ExprStmt(NamedTuple):
    """An expression run for its effect."""

    expr: IrExpr


class Return(NamedTuple):
    """``return value``."""

    value: IrExpr


class IfStmt(NamedTuple):
    """``if test: then else: other``; either branch may be empty."""

    test: IrExpr
    then: tuple[Stmt, ...]
    other: tuple[Stmt, ...]


class FuncDef(NamedTuple):
    """A named function. ``sig`` is ``None`` for a nested ``fn`` (the backend uses ``Any``)."""

    name: Name
    params: tuple[Local, ...]
    body: tuple[Stmt, ...]
    sig: TFn | None


class RecordDef(NamedTuple):
    """A ``deft`` record type."""

    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, CdyType], ...]


Stmt = Assign | ExprStmt | Return | IfStmt | FuncDef | RecordDef
Stmts = tuple[Stmt, ...]

OPERATOR_KINDS = frozenset({"binop", "compare", "boolop", "unary"})


class Ctx(NamedTuple):
    """What ``lower`` needs besides the expression: the table and the target's ``Caps``."""

    table: Table
    caps: Caps


def is_simple(expr: IrExpr) -> bool:
    """Whether ``expr`` can be evaluated later, out of order, with the same result."""
    return isinstance(expr, Const | Local | Global | Prim | Temp)


def applied_fn(expr: Expr) -> tuple[tuple[tuple[Local, Expr], ...], Expr] | None:
    """For ``((fn (a b) body) x y)``, as ``let`` desugars to: ``((a, x), (b, y))`` and ``body``."""
    match expr:
        case Call(Fn(params, body), args) if len(params) == len(args):
            return tuple(zip(params, args, strict=True)), body
        case _:
            return None


# --- value mode ---


def value(expr: Expr, ctx: Ctx, n: int) -> tuple[Stmts, IrExpr, int]:
    """Statements to run first, and an expression for ``expr``'s value. ``n``: next Temp id."""
    bound = applied_fn(expr)
    if bound is not None:
        stmts, n = bind(bound[0], ctx, n)
        body_stmts, result, n = value(bound[1], ctx, n)
        return stmts + body_stmts, result, n
    match expr:
        case Lit():
            return (), Const(expr.value, expr.ctype), n
        case Local() | Global() | Prim():
            return (), expr, n
        case Call():
            return value_call(expr.fn, expr.args, ctx, n)
        case If():
            return value_if(expr.test, expr.then, expr.other, ctx, n)
        case Do():
            return value_do(expr.body, ctx, n)
        case Fn():
            return value_fn(expr.params, expr.body, ctx, n)
        case Tup():
            stmts, out, n = value_seq(expr.items, ctx, n)
            return stmts, TupleE(out), n
        case Format():
            return value_format(expr.parts, ctx, n)
        case Get():
            stmts, obj_e, n = value(expr.obj, ctx, n)
            return stmts, GetE(obj_e, expr.field), n
        case Assoc():
            return value_assoc(expr.obj, expr.fields, ctx, n)


def value_call(fn: Expr, args: tuple[Expr, ...], ctx: Ctx, n: int) -> tuple[Stmts, IrExpr, int]:
    """A call: an ``Op`` for a built-in operator, otherwise a ``CallE``."""
    kind = ctx.table[fn.name].kind if isinstance(fn, Prim) else "call"
    if isinstance(fn, Prim) and kind == "boolop":
        return value_boolop(fn.name, args, ctx, n)
    if isinstance(fn, Prim) and kind in OPERATOR_KINDS:
        stmts, items, n = value_seq(args, ctx, n)
        return stmts, Op(fn.name, items), n
    stmts, items, n = value_seq((fn, *args), ctx, n)
    return stmts, CallE(items[0], items[1:]), n


def value_do(body: tuple[Expr, ...], ctx: Ctx, n: int) -> tuple[Stmts, IrExpr, int]:
    """``do``: all but the last form for effect, then the last one's value."""
    stmts, n = effect_all(body[:-1], ctx, n)
    last_stmts, result, n = value(body[-1], ctx, n)
    return stmts + last_stmts, result, n


def value_format(parts: tuple[str | Expr, ...], ctx: Ctx, n: int) -> tuple[Stmts, IrExpr, int]:
    """``format``: the holes in value mode, in order; the text as is."""
    stmts, out, n = value_seq(tuple(p for p in parts if not isinstance(p, str)), ctx, n)
    holes = iter(out)
    return stmts, FormatE(tuple(p if isinstance(p, str) else next(holes) for p in parts)), n


def value_assoc(
    obj: Expr, fields: tuple[tuple[str, Expr], ...], ctx: Ctx, n: int
) -> tuple[Stmts, IrExpr, int]:
    """``assoc``: the record, then the new field values, in order."""
    stmts, out, n = value_seq((obj, *(v for _, v in fields)), ctx, n)
    names = tuple(f for f, _ in fields)
    return stmts, AssocE(out[0], tuple(zip(names, out[1:], strict=True))), n


def value_seq(exprs: Sequence[Expr], ctx: Ctx, n: int) -> tuple[Stmts, tuple[IrExpr, ...], int]:
    """Each of ``exprs`` in value mode, keeping left-to-right evaluation order.

    If a later expression needs statements, those statements would run before the earlier
    expressions are evaluated, so each earlier one that isn't simple is stored in a
    temporary first.
    """
    lowered: list[tuple[Stmts, IrExpr]] = []
    for expr in exprs:
        stmts, result, n = value(expr, ctx, n)
        lowered.append((stmts, result))
    out_stmts: list[Stmt] = []
    out: list[IrExpr] = []
    for i, (stmts, result) in enumerate(lowered):
        out_stmts.extend(stmts)
        if not is_simple(result) and any(later for later, _ in lowered[i + 1 :]):
            temp = Temp(n)
            n += 1
            out_stmts.append(Assign(temp, result))
            out.append(temp)
        else:
            out.append(result)
    return tuple(out_stmts), tuple(out), n


def value_boolop(name: str, args: Sequence[Expr], ctx: Ctx, n: int) -> tuple[Stmts, IrExpr, int]:
    """``and``/``or``: an ``Op`` unless a later argument needs statements.

    ``and`` and ``or`` short-circuit, so a later argument's statements can't simply be moved
    in front. Then ``(and a b)`` becomes ``t = a; if t: t = b``, and ``or`` tests ``not t``.
    """
    lowered: list[tuple[Stmts, IrExpr]] = []
    for arg in args:
        stmts, result, n = value(arg, ctx, n)
        lowered.append((stmts, result))
    if not any(stmts for stmts, _ in lowered[1:]):
        return lowered[0][0], Op(name, tuple(r for _, r in lowered)), n
    temp = Temp(n)
    first_stmts, first = lowered[0]
    rest: Stmts = ()
    for stmts, result in reversed(lowered[1:]):
        rest = (*stmts, Assign(temp, result), *(() if not rest else (guard(name, temp, rest),)))
    return (*first_stmts, Assign(temp, first), guard(name, temp, rest)), temp, n + 1


def guard(name: str, temp: Temp, body: Stmts) -> IfStmt:
    """Run ``body`` only if ``and``/``or`` hasn't already decided its result in ``temp``."""
    test: IrExpr = temp if name == "and" else Op("not", (temp,))
    return IfStmt(test, body, ())


def value_if(test: Expr, then: Expr, other: Expr, ctx: Ctx, n: int) -> tuple[Stmts, IrExpr, int]:
    """``if`` in value mode: a conditional expression if possible, otherwise a temporary."""
    test_stmts, test_e, n = value(test, ctx, n)
    then_stmts, then_e, n = value(then, ctx, n)
    other_stmts, other_e, n = value(other, ctx, n)
    if ctx.caps.cond_expr and not then_stmts and not other_stmts:
        return test_stmts, CondE(test_e, then_e, other_e), n
    temp = Temp(n)
    branch = IfStmt(
        test_e, (*then_stmts, Assign(temp, then_e)), (*other_stmts, Assign(temp, other_e))
    )
    return (*test_stmts, branch), temp, n + 1


def value_fn(params: tuple[Local, ...], body: Expr, ctx: Ctx, n: int) -> tuple[Stmts, IrExpr, int]:
    """``fn``: a lambda if its body is one expression, otherwise a nested function."""
    body_stmts, n = tail(body, ctx, n)
    match body_stmts:
        case (Return(result),) if ctx.caps.lambda_expr:
            return (), LambdaE(params, result), n
        case _:
            temp = Temp(n)
            return (FuncDef(temp, params, body_stmts, None),), temp, n + 1


def bind(pairs: Sequence[tuple[Local, Expr]], ctx: Ctx, n: int) -> tuple[Stmts, int]:
    """Assignments for the bindings of an applied ``Fn`` (a ``let``)."""
    stmts, values, n = value_seq(tuple(v for _, v in pairs), ctx, n)
    assigns = tuple(Assign(local, v) for (local, _), v in zip(pairs, values, strict=True))
    return stmts + assigns, n


# --- tail and effect modes ---


def tail(expr: Expr, ctx: Ctx, n: int) -> tuple[Stmts, int]:
    """Statements that end by returning ``expr``'s value (the last form of a function)."""
    bound = applied_fn(expr)
    if bound is not None:
        stmts, n = bind(bound[0], ctx, n)
        body_stmts, n = tail(bound[1], ctx, n)
        return stmts + body_stmts, n
    match expr:
        case If(test, then, other):
            test_stmts, test_e, n = value(test, ctx, n)
            then_stmts, n = tail(then, ctx, n)
            other_stmts, n = tail(other, ctx, n)
            match then_stmts, other_stmts:
                case ((Return(a),), (Return(b),)) if ctx.caps.cond_expr:
                    return (*test_stmts, Return(CondE(test_e, a, b))), n
                case _:
                    return (*test_stmts, IfStmt(test_e, then_stmts, other_stmts)), n
        case Do(body):
            stmts, n = effect_all(body[:-1], ctx, n)
            last, n = tail(body[-1], ctx, n)
            return stmts + last, n
        case _:
            stmts, result, n = value(expr, ctx, n)
            return (*stmts, Return(result)), n


def effect(expr: Expr, ctx: Ctx, n: int) -> tuple[Stmts, int]:
    """Statements that run ``expr`` for its effect only."""
    bound = applied_fn(expr)
    if bound is not None:
        stmts, n = bind(bound[0], ctx, n)
        body_stmts, n = effect(bound[1], ctx, n)
        return stmts + body_stmts, n
    match expr:
        case Lit() | Local() | Global() | Prim():
            return (), n
        case If(test, then, other):
            test_stmts, test_e, n = value(test, ctx, n)
            then_stmts, n = effect(then, ctx, n)
            other_stmts, n = effect(other, ctx, n)
            if not then_stmts and not other_stmts:
                return (*test_stmts, *(() if is_simple(test_e) else (ExprStmt(test_e),))), n
            return (*test_stmts, IfStmt(test_e, then_stmts, other_stmts)), n
        case Do(body):
            return effect_all(body, ctx, n)
        case _:
            stmts, result, n = value(expr, ctx, n)
            return (*stmts, *(() if is_simple(result) else (ExprStmt(result),))), n


def effect_all(exprs: Sequence[Expr], ctx: Ctx, n: int) -> tuple[Stmts, int]:
    """Each of ``exprs`` in effect mode, in order."""
    out: Stmts = ()
    for expr in exprs:
        stmts, n = effect(expr, ctx, n)
        out += stmts
    return out, n


# --- top level ---


def lower_program(
    tops: Sequence[TopLevel], table: Table = INITIAL_TABLE, caps: Caps = PY_CAPS
) -> Stmts:
    """A whole analysed Candy file as IR statements, in order."""
    ctx = Ctx(table, caps)
    out: Stmts = ()
    n = 0
    for top in tops:
        match top:
            case Def(name, init, sig):
                stmts, result, n = value(init, ctx, n)
                out += (*stmts, Assign(Global(name), result, sig))
            case Defn(name, params, body, sig):
                body_stmts, n = tail(body, ctx, n)
                out += (FuncDef(Global(name), params, body_stmts, sig),)
            case Deft(name, tvars, fields):
                out += (RecordDef(name, tvars, fields),)
            case _:
                stmts, n = effect(top, ctx, n)
                out += stmts
    return out
