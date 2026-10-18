"""The Python backend, ``emit_py``: lowered IR to a Python ``ast`` module, then to source text.

This is the last of the translator's three steps, and the only one that knows about Python
(see "Layers" in ``doc/hl_rqmt/iMVP_py_translator.md``). It is mostly one IR node to one
``ast`` node. It also:

- picks Python spellings. Candy names are mangled (``-`` to ``_``, ``?`` to ``_p``, ``!`` to
  ``_x``, other characters to ``_uXXXX``); a name that is a Python keyword or built-in, or
  a module the generated code imports, gets a trailing ``_``. A local keeps its name unless
  that spelling is already visible (a global, an enclosing local, or an earlier binding in
  the same Python function); then it becomes ``_cdy_<name>_<id>``. Generated names start
  with ``_cdy_``; a user name that does too gets a trailing ``_``, so they can't collide.
- maps each built-in through the ``cdy_rt`` table: operators become ``ast`` operators, calls
  and values become the entry's Python name or expression;
- turns ``sig`` types into annotations (``Int`` to ``int``, ``(List a)`` to
  ``tuple[A, ...]``, type variables to PEP 695 type parameters).

The generated module imports only the standard library and ``cdy_rt``.
"""

from __future__ import annotations

import ast
import builtins
import keyword
from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import NamedTuple

from cdy_rt.table import IMPORTS, INITIAL_TABLE, Table
from core_cdy import CandyError, CdyType, Global, Local, Prim, TCon, TFn, TVar, type_vars
from lower_cdy import (
    Assign,
    AssocE,
    CallE,
    CondE,
    Const,
    Continue,
    ExprStmt,
    FormatE,
    FuncDef,
    GetE,
    IfStmt,
    IrExpr,
    LambdaE,
    Loop,
    MatchStmt,
    Op,
    Rebind,
    RecordDef,
    Return,
    Stmt,
    Stmts,
    SumDef,
    Temp,
    TupleE,
)

# Names the generated code needs from ``typing``/``collections.abc``, imported under these
# aliases so that they can't clash with user names.
ANY, CALLABLE, MAPPING, NAMED_TUPLE = "_cdy_Any", "_cdy_Callable", "_cdy_Mapping", "_cdy_NamedTuple"
HEADER = f"""\
from __future__ import annotations

from collections.abc import Callable as {CALLABLE}, Mapping as {MAPPING}
from typing import Any as {ANY}, NamedTuple as {NAMED_TUPLE}
"""

# Python names a user name must not take: keywords, built-ins (the generated code uses
# ``print``, ``len``, ``int``, ``tuple``, ...) and the modules it imports.
RESERVED = frozenset(
    {*keyword.kwlist, *dir(builtins), *(module.split(".", maxsplit=1)[0] for module in IMPORTS)}
)

BINOPS: Mapping[str, type[ast.operator]] = MappingProxyType(
    {"+": ast.Add, "-": ast.Sub, "*": ast.Mult, "/": ast.Div}
)
COMPARES: Mapping[str, type[ast.cmpop]] = MappingProxyType(
    {"==": ast.Eq, "!=": ast.NotEq, "<": ast.Lt, ">": ast.Gt, "<=": ast.LtE, ">=": ast.GtE}
)
BOOLOPS: Mapping[str, type[ast.boolop]] = MappingProxyType({"and": ast.And, "or": ast.Or})
UNARYOPS: Mapping[str, type[ast.unaryop]] = MappingProxyType({"not": ast.Not})

BASE_TYPES: Mapping[str, str] = MappingProxyType(
    {
        "Int": "int",
        "Long": "int",
        "Byte": "int",
        "Float": "float",
        "Double": "float",
        "Bool": "bool",
        "Char": "str",
        "String": "str",
        "Any": ANY,
    }
)


# --- names ---


def mangle(name: str) -> str:
    """A Candy name as a Python identifier (see the module docstring)."""
    special = {"-": "_", "?": "_p", "!": "_x"}
    out = "".join(
        ch
        if (ch.isascii() and (ch.isalnum() or ch == "_"))
        else special.get(ch, f"_u{ord(ch):04x}")
        for ch in name
    )
    if out in RESERVED or out.startswith("_cdy_"):
        out += "_"
    return out


class Env(NamedTuple):
    """What names mean at one point in the generated code."""

    table: Table
    globals_: Mapping[str, str]  # Candy top-level name -> Python name
    locals_: Mapping[int, str]  # Local id -> Python name
    taken: frozenset[str]  # Python names visible here, which a new local must not reuse


def global_names(stmts: Stmts) -> Mapping[str, str]:
    """Python names for the program's top-level names; fails if two mangle to the same one."""
    names: list[str] = []
    for stmt in stmts:
        match stmt:
            case Assign(Global(name), _, _) | FuncDef(Global(name), _, _, _) | RecordDef(name):
                names.append(name)
            case SumDef(name, _, variants):
                names.extend((name, *(v for v, _ in variants)))
            case _:
                pass
    spelled: dict[str, str] = {}
    for name in names:
        py = mangle(name)
        clash = [other for other, other_py in spelled.items() if other_py == py and other != name]
        if clash:
            raise CandyError(f"{clash[0]} and {name} both become the Python name {py}")
        spelled[name] = py
    return MappingProxyType(spelled)


def bound_locals(stmts: Stmts) -> tuple[Local, ...]:
    """The locals assigned in ``stmts``, in order (not looking inside nested functions)."""
    out: list[Local] = []
    for stmt in stmts:
        match stmt:
            case Assign(Local() as local, _, _) if local not in out:
                out.append(local)
            case IfStmt(_, then, other):
                out.extend(local for local in bound_locals((*then, *other)) if local not in out)
            case Loop(body):
                out.extend(local for local in bound_locals(body) if local not in out)
            case MatchStmt(_, cases, default):
                binds = [local for c in cases for _, local in c.binds]
                bodies = [s for c in cases for s in c.body] + list(default or ())
                found = (*binds, *bound_locals(tuple(bodies)))
                out.extend(local for local in found if local not in out)
            case _:
                pass
    return tuple(out)


def with_locals(env: Env, locals_: Sequence[Local]) -> Env:
    """``env`` with Python names chosen for ``locals_``, which are bound in a new scope."""
    spelled = dict(env.locals_)
    taken = set(env.taken)
    for local in locals_:
        base = mangle(local.name)
        py = base if base not in taken else f"_cdy_{base}_{local.id}"
        spelled[local.id] = py
        taken.add(py)
    return env._replace(locals_=MappingProxyType(spelled), taken=frozenset(taken))


def free_names(stmts: Stmts, env: Env) -> frozenset[str]:
    """Python names of the bindings outside ``stmts`` that ``stmts`` refer to (at any depth).

    A local in a new function may reuse any other spelling: only these, and the names the
    function binds itself, would be shadowed.
    """
    used: set[str] = set()

    def visit(node: object) -> None:
        match node:
            case Local(_, local_id) if local_id in env.locals_:
                used.add(env.locals_[local_id])
            case Global(name):
                used.add(env.globals_[name])
            case tuple():  # a tuple of nodes, or any IR node (they are all NamedTuples)
                for item in node:
                    visit(item)
            case _:
                pass

    visit(stmts)
    return frozenset(used)


def name_of(name: Local | Global | Temp, env: Env) -> str:
    """The Python name for a Core or IR name."""
    match name:
        case Local(_, local_id):
            return env.locals_[local_id]
        case Global(candy):
            return env.globals_[candy]
        case Temp(temp_id):
            return f"_cdy_t{temp_id}"


def load(name: str) -> ast.Name:
    """A Python name, read."""
    return ast.Name(name, ast.Load())


def store(name: str) -> ast.Name:
    """A Python name, assigned."""
    return ast.Name(name, ast.Store())


def py_expr(source: str) -> ast.expr:
    """A table entry's Python expression (``math.pi``, ``None``, ``cdy_rt.table_defs.at``)."""
    return ast.parse(source, mode="eval").body


# --- types ---


def annotation(t: CdyType, env: Env) -> ast.expr:
    """A Candy type as a Python annotation."""
    match t:
        case TVar(name):
            return load(mangle(name))
        case TFn(params, ret):
            args = ast.List([annotation(p, env) for p in params], ast.Load())
            return subscript(load(CALLABLE), [args, annotation(ret, env)])
        case TCon("Unit", ()):
            return ast.Constant(None)
        case TCon(name, ()) if name in BASE_TYPES:
            return load(BASE_TYPES[name])
        case TCon("Maybe", (arg,)):
            return ast.BinOp(annotation(arg, env), ast.BitOr(), ast.Constant(None))
        case TCon("List", (arg,)):
            return subscript(load("tuple"), [annotation(arg, env), ast.Constant(...)])
        case TCon("Tup", args):
            return subscript(load("tuple"), [annotation(a, env) for a in args])
        case TCon("Map", (key, val)):
            return subscript(load(MAPPING), [annotation(key, env), annotation(val, env)])
        case TCon(name, ()):
            return load(env.globals_[name])
        case TCon(name, args):
            return subscript(load(env.globals_[name]), [annotation(a, env) for a in args])
    raise CandyError(f"can't write type {t} in Python")


def subscript(value: ast.expr, items: Sequence[ast.expr]) -> ast.expr:
    """``value[a]`` or ``value[a, b]``."""
    index = items[0] if len(items) == 1 else ast.Tuple(list(items), ast.Load())
    return ast.Subscript(value, index, ast.Load())


def type_params(types: Sequence[CdyType]) -> list[ast.type_param]:
    """PEP 695 type parameters for the type variables in ``types``."""
    names = sorted(frozenset().union(*(type_vars(t) for t in types)))
    return [ast.TypeVar(mangle(name)) for name in names]


# --- expressions ---


def emit_expr(expr: IrExpr, env: Env) -> ast.expr:
    """An IR expression as a Python expression."""
    match expr:
        case Const(v, _):
            return ast.Constant(v)
        case Local() | Global() | Temp():
            return load(name_of(expr, env))
        case Prim(name):
            return emit_prim(name, env)
        case CallE(fn, args):
            return ast.Call(emit_expr(fn, env), [emit_expr(a, env) for a in args], [])
        case Op(prim, args):
            return emit_op(prim, [emit_expr(a, env) for a in args], env)
        case CondE(test, then, other):
            return ast.IfExp(emit_expr(test, env), emit_expr(then, env), emit_expr(other, env))
        case LambdaE(params, body):
            return emit_lambda(params, body, env)
        case TupleE(items):
            return ast.Tuple([emit_expr(i, env) for i in items], ast.Load())
        case FormatE(parts):
            return ast.JoinedStr(
                [
                    ast.Constant(p)
                    if isinstance(p, str)
                    else ast.FormattedValue(emit_expr(p, env), -1)
                    for p in parts
                ]
            )
        case GetE(obj, field):
            return ast.Attribute(emit_expr(obj, env), field_name(field), ast.Load())
        case AssocE(obj, fields):
            replace = ast.Attribute(emit_expr(obj, env), "_replace", ast.Load())
            return ast.Call(
                replace, [], [ast.keyword(field_name(f), emit_expr(v, env)) for f, v in fields]
            )


def emit_lambda(params: tuple[Local, ...], body: IrExpr, env: Env) -> ast.expr:
    """A lambda, whose parameters are a new scope."""
    inner = with_locals(env, params)
    args = ast.arguments(args=[ast.arg(name_of(p, inner)) for p in params])
    return ast.Lambda(args, emit_expr(body, inner))


def emit_prim(name: str, env: Env) -> ast.expr:
    """A built-in used as a value: its Python name or expression."""
    entry = env.table[name]
    if entry.kind in ("call", "value", "index", "slice"):
        return py_expr(entry.py)
    raise CandyError(f"the operator {name} can't be used as a value yet; wrap it in a fn")


def emit_op(prim: str, args: list[ast.expr], env: Env) -> ast.expr:
    """A built-in operator applied to ``args``."""
    entry = env.table[prim]
    match entry.kind:
        case "binop":
            op = BINOPS[entry.py]
            result = args[0]
            for arg in args[1:]:
                result = ast.BinOp(result, op(), arg)
            return result
        case "compare":
            return ast.Compare(args[0], [COMPARES[entry.py]() for _ in args[1:]], args[1:])
        case "boolop":
            return ast.BoolOp(BOOLOPS[entry.py](), args)
        case "unary":
            return ast.UnaryOp(UNARYOPS[entry.py](), args[0])
        case "index":
            return ast.Subscript(args[0], args[1], ast.Load())
        case "slice":
            return ast.Subscript(args[0], ast.Slice(args[1], args[2]), ast.Load())
    raise CandyError(f"{prim} is not an operator")


def field_name(field: str) -> str:
    """The Python name of a record field. ``NamedTuple`` fields can't start with ``_``."""
    py = mangle(field)
    if py.startswith("_"):
        raise CandyError(f"field {field} becomes {py}, but record fields can't start with _")
    return py


# --- statements ---


def emit_stmts(stmts: Stmts, env: Env) -> list[ast.stmt]:
    """IR statements as Python statements (never empty: ``pass`` if there are none)."""
    out = [py for stmt in stmts for py in emit_stmt_list(stmt, env)]
    return out or [ast.Pass()]


def emit_stmt_list(stmt: Stmt, env: Env) -> list[ast.stmt]:
    """One IR statement as Python statements: a sum type takes several, the rest one."""
    if isinstance(stmt, SumDef):
        return emit_sum(stmt, env)
    return [emit_stmt(stmt, env)]


def emit_stmt(stmt: Stmt, env: Env) -> ast.stmt:
    """One IR statement as a Python statement."""
    match stmt:
        case Assign():
            target = store(name_of(stmt.target, env))
            if stmt.sig is None:
                return ast.Assign([target], emit_expr(stmt.value, env))
            return ast.AnnAssign(target, annotation(stmt.sig, env), emit_expr(stmt.value, env), 1)
        case ExprStmt():
            return ast.Expr(emit_expr(stmt.expr, env))
        case Return():
            return ast.Return(emit_expr(stmt.value, env))
        case IfStmt():
            orelse = emit_stmts(stmt.other, env) if stmt.other else []
            return ast.If(emit_expr(stmt.test, env), emit_stmts(stmt.then, env), orelse)
        case FuncDef():
            name = name_of(stmt.name, env)
            return emit_funcdef(name, stmt.params, stmt.body, stmt.sig, env)
        case RecordDef():
            return emit_record(stmt, env)
        case Loop(body):
            return ast.While(ast.Constant(True), emit_stmts(body, env), [])
        case Rebind(targets, values):
            if len(targets) == 1:
                return ast.Assign([store(name_of(targets[0], env))], emit_expr(values[0], env))
            lhs = ast.Tuple([store(name_of(t, env)) for t in targets], ast.Store())
            return ast.Assign([lhs], ast.Tuple([emit_expr(v, env) for v in values], ast.Load()))
        case Continue():
            return ast.Continue()
        case MatchStmt():
            return emit_match(stmt, env)
        case SumDef():
            raise CandyError("a sum type is only allowed at top level")


def emit_record(record: RecordDef, env: Env) -> ast.stmt:
    """A ``deft`` record as a ``NamedTuple`` class."""
    fields: list[ast.stmt] = [
        ast.AnnAssign(store(field_name(f)), annotation(t, env), None, 1) for f, t in record.fields
    ]
    return ast.ClassDef(
        env.globals_[record.name],
        bases=[load(NAMED_TUPLE)],
        body=fields or [ast.Pass()],  # a variant with no fields
        type_params=[ast.TypeVar(mangle(t)) for t in record.tvars],
    )


def emit_sum(sum_def: SumDef, env: Env) -> list[ast.stmt]:
    """A ``deft`` sum type: one ``NamedTuple`` class per variant, and a type alias for their
    union. A variant is generic only in the type variables its fields use."""
    out: list[ast.stmt] = []
    members: list[ast.expr] = []
    for v_name, fields in sum_def.variants:
        used = frozenset().union(*(type_vars(t) for _, t in fields))
        tvars = tuple(t for t in sum_def.tvars if t in used)
        out.append(emit_record(RecordDef(v_name, tvars, fields), env))
        cls = load(env.globals_[v_name])
        members.append(subscript(cls, [load(mangle(t)) for t in tvars]) if tvars else cls)
    union = members[0]
    for member in members[1:]:
        union = ast.BinOp(union, ast.BitOr(), member)
    alias = ast.TypeAlias(
        store(env.globals_[sum_def.name]),
        [ast.TypeVar(mangle(t)) for t in sum_def.tvars],
        union,
    )
    return [*out, alias]


def emit_match(stmt: MatchStmt, env: Env) -> ast.stmt:
    """``match`` as an ``isinstance`` chain, with each field bound by attribute.

    Not Python's ``match``: mypy loses a generic variant's type arguments in a class pattern
    (``case Node(l, v, r)`` makes ``v`` ``Any``), but keeps them when ``isinstance`` narrows.
    """
    subject = emit_expr(stmt.subject, env)
    orelse: list[ast.stmt] = emit_stmts(stmt.default, env) if stmt.default is not None else []
    for case in reversed(stmt.cases):
        test = ast.Call(load("isinstance"), [subject, load(name_of(case.variant, env))], [])
        binds: list[ast.stmt] = [
            ast.Assign(
                [store(name_of(local, env))], ast.Attribute(subject, field_name(f), ast.Load())
            )
            for f, local in case.binds
        ]
        body = binds + emit_stmts(case.body, env) if case.body else binds or [ast.Pass()]
        orelse = [ast.If(test, body, orelse)]
    return orelse[0]


def emit_funcdef(
    name: str, params: tuple[Local, ...], body: Stmts, sig: TFn | None, env: Env
) -> ast.stmt:
    """A function: typed from its ``sig``, or with ``Any`` for a nested ``fn``."""
    scope = env._replace(taken=RESERVED | free_names(body, env))
    inner = with_locals(scope, (*params, *bound_locals(body)))
    if sig is None:
        anns: list[ast.expr] = [load(ANY) for _ in params]
        returns: ast.expr = load(ANY)
        tparams: list[ast.type_param] = []
    else:
        anns = [annotation(t, env) for t in sig.params]
        returns = annotation(sig.ret, env)
        tparams = type_params((*sig.params, sig.ret))
    args = ast.arguments(
        args=[ast.arg(name_of(p, inner), ann) for p, ann in zip(params, anns, strict=True)]
    )
    return ast.FunctionDef(
        name, args, emit_stmts(body, inner), returns=returns, type_params=tparams
    )


# --- module ---


def emit_module(stmts: Stmts, table: Table = INITIAL_TABLE) -> ast.Module:
    """A whole lowered program as a Python module (without the import header)."""
    globals_ = global_names(stmts)
    env = Env(table, globals_, MappingProxyType({}), RESERVED | frozenset(globals_.values()))
    env = with_locals(env, bound_locals(stmts))
    module = ast.Module(emit_stmts(stmts, env) if stmts else [], [])
    return ast.fix_missing_locations(module)


def py_source(stmts: Stmts, table: Table = INITIAL_TABLE) -> str:
    """A whole lowered program as Python source text, imports included."""
    imports = "".join(f"import {module}\n" for module in IMPORTS)
    return f"{HEADER}{imports}\n{ast.unparse(emit_module(stmts, table))}\n"
