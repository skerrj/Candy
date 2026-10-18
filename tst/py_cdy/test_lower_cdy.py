"""Tests for the lowered IR and ``lower`` (``lower_cdy.py``)."""

from types import MappingProxyType

from parsec import parse

from cdy_rt.table import INITIAL_TABLE
from core_cdy import Expr, Global, Local, Prim, Scope, TCon, TFn, analyse_expr, analyse_program
from lower_cdy import (
    PY_CAPS,
    Assign,
    AssocE,
    CallE,
    Caps,
    Case,
    CondE,
    Const,
    Continue,
    Ctx,
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
    Stmts,
    SumDef,
    Temp,
    TupleE,
    effect,
    lower_program,
    tail,
    value,
)
from parse_cdy import program

SCOPE = Scope(MappingProxyType({}), frozenset({"f", "g", "n", "v"}), INITIAL_TABLE)
CTX = Ctx(INITIAL_TABLE, PY_CAPS)
N, F, G, PUT = Global("n"), Global("f"), Global("g"), Prim("put")


def core(src: str) -> Expr:
    """``src`` analysed as an expression; ``f``, ``g``, ``n`` and ``v`` are globals."""
    (form,) = parse(program, src)
    return analyse_expr(form, SCOPE, 0)[0]


def val(src: str, ctx: Ctx = CTX) -> tuple[Stmts, IrExpr]:
    """``src`` lowered in value mode: its statements and its expression."""
    stmts, result, _ = value(core(src), ctx, 0)
    return stmts, result


def tl(src: str, ctx: Ctx = CTX) -> Stmts:
    """``src`` lowered in tail mode."""
    return tail(core(src), ctx, 0)[0]


def eff(src: str) -> Stmts:
    """``src`` lowered in effect mode."""
    return effect(core(src), CTX, 0)[0]


def c(v: int) -> Const:
    """An ``Int`` constant."""
    return Const(v, "Int")


def test_simple_values() -> None:
    assert val("1") == ((), c(1))
    assert val("(+ n 1 2)") == ((), Op("+", (N, c(1), c(2))))
    assert val("(< 1 n)") == ((), Op("<", (c(1), N)))
    assert val("(not true)") == ((), Op("not", (Const(True, "Bool"),)))
    assert val("(f n)") == ((), CallE(F, (N,)))
    assert val("(if n 1 2)") == ((), CondE(N, c(1), c(2)))


def test_let_becomes_assignments() -> None:
    # (put (let ((m (* n 2))) (+ m 1)))  ->  m = n * 2; print(m + 1)
    m = Local("m", 0)
    assert eff("(put (let ((m (* n 2))) (+ m 1)))") == (
        Assign(m, Op("*", (N, c(2)))),
        ExprStmt(CallE(PUT, (Op("+", (m, c(1))),))),
    )


def test_sequential_let_in_tail_mode() -> None:
    # The doc's f2: x = n + 1; y = m + 3; return x if x < y else y
    x, y = Local("x", 0), Local("y", 1)
    assert tl("(let ((x (+ n 1)) (y (+ x 3))) (if (< x y) x y))") == (
        Assign(x, Op("+", (N, c(1)))),
        Assign(y, Op("+", (x, c(3)))),
        Return(CondE(Op("<", (x, y)), x, y)),
    )


def test_evaluation_order_uses_a_temporary() -> None:
    # (f (g n) (let ((x 1)) x))  ->  t = g(n); x = 1; f(t, x)
    x = Local("x", 0)
    assert val("(f (g n) (let ((x 1)) x))") == (
        (Assign(Temp(0), CallE(G, (N,))), Assign(x, c(1))),
        CallE(F, (Temp(0), x)),
    )
    # A simple earlier argument needs no temporary.
    assert val("(f n (let ((x 1)) x))") == ((Assign(x, c(1)),), CallE(F, (N, x)))


def test_if_in_value_position_with_statements() -> None:
    # (put (if (< n 0) (do (put "neg") "neg") "ok"))
    neg, ok = Const("neg", "String"), Const("ok", "String")
    assert eff('(put (if (< n 0) (do (put "neg") "neg") "ok"))') == (
        IfStmt(
            Op("<", (N, c(0))),
            (ExprStmt(CallE(PUT, (neg,))), Assign(Temp(0), neg)),
            (Assign(Temp(0), ok),),
        ),
        ExprStmt(CallE(PUT, (Temp(0),))),
    )


def test_if_in_tail_position_with_statements() -> None:
    x = Local("x", 0)
    assert tl("(if n (let ((x 1)) x) 2)") == (
        IfStmt(N, (Assign(x, c(1)), Return(x)), (Return(c(2)),)),
    )


def test_no_conditional_expression_cap() -> None:
    no_cond = Ctx(INITIAL_TABLE, Caps(cond_expr=False, lambda_expr=True))
    assert val("(if n 1 2)", no_cond) == (
        (IfStmt(N, (Assign(Temp(0), c(1)),), (Assign(Temp(0), c(2)),)),),
        Temp(0),
    )
    assert tl("(if n 1 2)", no_cond) == (IfStmt(N, (Return(c(1)),), (Return(c(2)),)),)


def test_effect_mode() -> None:
    assert eff("1") == ()
    assert eff("n") == ()
    assert eff("(do (put 1) 2 (put 3))") == (
        ExprStmt(CallE(PUT, (c(1),))),
        ExprStmt(CallE(PUT, (c(3),))),
    )
    assert eff("(if n (put 1))") == (IfStmt(N, (ExprStmt(CallE(PUT, (c(1),))),), ()),)
    assert eff("(if (f n) 1 2)") == (ExprStmt(CallE(F, (N,))),)


def test_fn_lambda_or_nested_def() -> None:
    x, y = Local("x", 0), Local("y", 1)
    assert val("(fn (x) (+ x 1))") == ((), LambdaE((x,), Op("+", (x, c(1)))))
    assert val("(fn (x) (let ((y x)) y))") == (
        (FuncDef(Temp(0), (x,), (Assign(y, x), Return(y)), None),),
        Temp(0),
    )


def test_boolop_with_statements_short_circuits() -> None:
    # (and n (let ((x 1)) x))  ->  t = n; if t: x = 1; t = x
    x = Local("x", 0)
    assert val("(and n (let ((x 1)) x))") == (
        (Assign(Temp(0), N), IfStmt(Temp(0), (Assign(x, c(1)), Assign(Temp(0), x)), ())),
        Temp(0),
    )
    stmts, result = val("(or n (let ((x 1)) x))")
    assert result == Temp(0) and isinstance(stmts[1], IfStmt)
    assert stmts[1].test == Op("not", (Temp(0),))
    assert val("(and n f)") == ((), Op("and", (N, F)))


def test_records_tuples_format() -> None:
    assert val("(tup 1 n)") == ((), TupleE((c(1), N)))
    assert val("(get v x)") == ((), GetE(Global("v"), "x"))
    assert val("(assoc v x 1)") == ((), AssocE(Global("v"), (("x", c(1)),)))
    assert val('(format "n={n}!")') == ((), FormatE(("n=", N, "!")))


def test_program() -> None:
    int_t = TCon("Int")
    n0 = Local("n", 0)
    out = lower_program(
        analyse_program(
            parse(
                program,
                """
                (deft P ((x Int)))
                (sig sq (Fn (Int) Int))
                (defn sq (n) (* n n))
                (sig ten Int)
                (def ten (sq 10))
                (put ten)
                """,
            )
        )
    )
    assert out == (
        RecordDef("P", (), (("x", int_t),)),
        FuncDef(Global("sq"), (n0,), (Return(Op("*", (n0, n0))),), TFn((int_t,), int_t)),
        Assign(Global("ten"), CallE(Global("sq"), (c(10),)), int_t),
        ExprStmt(CallE(PUT, (Global("ten"),))),
    )


def lowered(src: str) -> Stmts:
    """A whole program lowered."""
    return lower_program(analyse_program(parse(program, src)))


def test_self_tail_call_becomes_loop() -> None:
    n, acc = Local("n", 0), Local("acc", 1)
    (func,) = lowered(
        """
        (sig f (Fn (Int Int) Int))
        (defn f (n acc) (if (= n 0) acc (f (- n 1) acc)))
        """
    )
    assert isinstance(func, FuncDef)
    assert func.body == (
        Loop(
            (
                IfStmt(
                    Op("=", (n, c(0))),
                    (Return(acc),),
                    (Rebind((n,), (Op("-", (n, c(1))),)), Continue()),
                ),
            )
        ),
    )


def test_unit_loop_ends_with_return() -> None:
    (func,) = lowered("(sig f (Fn (Int) Unit)) (defn f (n) (if (> n 0) (f (- n 1))))")
    assert isinstance(func, FuncDef) and isinstance(func.body[0], Loop)
    assert func.body[0].body[-1] == Return(Const(None, "Unit"))


def test_no_loop_without_a_tail_call_or_with_a_closure() -> None:
    (plain,) = lowered("(sig f (Fn (Int) Int)) (defn f (n) (if (= n 0) 0 (+ 1 (f (- n 1)))))")
    assert isinstance(plain, FuncDef) and not isinstance(plain.body[0], Loop)
    (closure,) = lowered(
        "(sig f (Fn (Int) Any)) (defn f (n) (if (= n 0) (fn (x) (+ x n)) (f (- n 1))))"
    )
    assert isinstance(closure, FuncDef) and not isinstance(closure.body[0], Loop)


SUM = "(deft Opt (No) (Yes ((v Int)))) "


def test_match_in_tail_and_value_modes() -> None:
    s, v = Local("s", 0), Local("v", 1)
    *_, func = lowered(SUM + "(sig f (Fn (Opt) Int)) (defn f (s) (match s ((No) 0) ((Yes v) v)))")
    assert func == FuncDef(
        Global("f"),
        (s,),
        (
            MatchStmt(
                s,
                (
                    Case(Global("No"), (), (Return(c(0)),)),
                    Case(Global("Yes"), (("v", v),), (Return(v),)),
                ),
                None,
            ),
        ),
        TFn((TCon("Opt"),), TCon("Int")),
    )
    # In value position, each case assigns a temporary; a call as subject is stored first.
    *_, put = lowered(
        SUM + "(sig g (Fn (Int) Opt)) (defn g (x) No) (put (match (g 1) ((No) 0) (else 1)))"
    )
    assert put == ExprStmt(CallE(PUT, (Temp(0),)))
    assert lowered(
        SUM + "(sig g (Fn (Int) Opt)) (defn g (x) No) (put (match (g 1) ((No) 0) (else 1)))"
    )[2] == (Assign(Temp(1), CallE(Global("g"), (c(1),))))


def test_sum_def() -> None:
    (out,) = lowered(SUM)
    assert out == SumDef("Opt", (), (("No", ()), ("Yes", (("v", TCon("Int")),))))
