"""Tests for the Core AST and ``analyse`` (``core_cdy.py``)."""

import re
from types import MappingProxyType

import pytest
from parsec import parse

from cdy_rt.table import INITIAL_TABLE
from core_cdy import (
    NIL,
    Assoc,
    Call,
    CandyError,
    Clause,
    Def,
    Defn,
    Deft,
    DeftSum,
    Do,
    Expr,
    Fn,
    Format,
    Get,
    Global,
    If,
    Lit,
    Local,
    Match,
    Prim,
    Scope,
    TCon,
    TFn,
    TopLevel,
    Tup,
    TVar,
    Variant,
    analyse_expr,
    analyse_program,
)
from parse_cdy import program

EMPTY = Scope(MappingProxyType({}), frozenset({"g"}), INITIAL_TABLE)


def expr(src: str) -> Expr:
    """The one form in ``src``, analysed as an expression (``g`` is a known global)."""
    (form,) = parse(program, src)
    return analyse_expr(form, EMPTY, 0)[0]


def prog(src: str) -> tuple[TopLevel, ...]:
    """The top-level forms in ``src``, analysed as a program."""
    return analyse_program(parse(program, src))


def test_literals() -> None:
    assert expr("1") == Lit(1, "Int")
    assert expr("1500l") == Lit(1500, "Long")
    assert expr("2b") == Lit(2, "Byte")
    assert expr("3.5f") == Lit(3.5, "Float")
    assert expr("10.0") == Lit(10.0, "Double")
    assert expr("\\e") == Lit("e", "Char")
    assert expr('"hi"') == Lit("hi", "String")
    assert expr("true") == Lit(True, "Bool")


def test_symbols() -> None:
    assert expr("g") == Global("g")
    assert expr("+") == Prim("+")
    assert expr("nil") == Prim("nil")
    with pytest.raises(CandyError, match="unknown name nope"):
        expr("nope")
    with pytest.raises(CandyError, match="special form, not a value"):
        expr("if")


def test_calls_and_arity() -> None:
    assert expr("(g 1)") == Call(Global("g"), (Lit(1, "Int"),))
    assert expr("(+ 1 2 3)") == Call(Prim("+"), (Lit(1, "Int"), Lit(2, "Int"), Lit(3, "Int")))
    with pytest.raises(CandyError, match="at least 2"):
        expr("(+ 1)")
    with pytest.raises(CandyError, match="takes 1"):
        expr("(len 1 2)")
    with pytest.raises(CandyError, match="empty form"):
        expr("()")


def test_if_cond_do() -> None:
    one, two = Lit(1, "Int"), Lit(2, "Int")
    assert expr("(if true 1 2)") == If(Lit(True, "Bool"), one, two)
    assert expr("(if true 1)") == If(Lit(True, "Bool"), one, NIL)
    assert expr("(cond (false 1) (else 2))") == If(Lit(False, "Bool"), one, two)
    assert expr("(cond (false 1) (true 2))") == If(
        Lit(False, "Bool"), one, If(Lit(True, "Bool"), two, NIL)
    )
    with pytest.raises(CandyError, match="last clause"):
        expr("(cond (else 1) (true 2))")
    assert expr("(do)") == NIL
    assert expr("(do 1)") == one
    assert expr("(do 1 2)") == Do((one, two))


def test_let_is_applied_lambdas() -> None:
    x, y = Local("x", 0), Local("y", 1)
    # (let ((x 1) (y x)) y) == ((fn (x) ((fn (y) y) x)) 1)
    assert expr("(let ((x 1) (y x)) y)") == Call(
        Fn((x,), Call(Fn((y,), y), (x,))), (Lit(1, "Int"),)
    )
    assert expr("(let () 1)") == Lit(1, "Int")
    with pytest.raises(CandyError, match="binding must be"):
        expr("(let ((x)) x)")


def test_let_shadowing_gets_new_ids() -> None:
    inner = expr("(let ((x 1)) (let ((x 2)) x))")
    assert isinstance(inner, Call) and isinstance(inner.fn, Fn)
    outer_x = inner.fn.params[0]
    nested = inner.fn.body
    assert isinstance(nested, Call) and isinstance(nested.fn, Fn)
    assert nested.fn.body == nested.fn.params[0] != outer_x


def test_let_destructuring() -> None:
    t, x, y = Local("_tup", 0), Local("x", 1), Local("y", 2)
    at0 = Call(Prim("at"), (t, Lit(0, "Int")))
    at1 = Call(Prim("at"), (t, Lit(1, "Int")))
    assert expr("(let (((x y) g)) y)") == Call(
        Fn((t,), Call(Fn((x,), Call(Fn((y,), y), (at1,))), (at0,))), (Global("g"),)
    )


def test_fn() -> None:
    x = Local("x", 0)
    assert expr("(fn (x) x)") == Fn((x,), x)
    with pytest.raises(CandyError, match="at least one"):
        expr("(fn () 1)")
    with pytest.raises(CandyError, match="exactly one body"):
        expr("(fn (x) x x)")
    with pytest.raises(CandyError, match="must be different"):
        expr("(fn (x x) x)")


def test_tup_get_assoc() -> None:
    g = Global("g")
    assert expr("(tup 1 g)") == Tup((Lit(1, "Int"), g))
    assert expr("(get g x)") == Get(g, "x")
    assert expr("(assoc g x 1 y 2)") == Assoc(g, (("x", Lit(1, "Int")), ("y", Lit(2, "Int"))))
    with pytest.raises(CandyError, match="assoc"):
        expr("(assoc g x)")


def test_format() -> None:
    assert expr('(format "a {g} b {(+ 1 2)}{{c}}")') == Format(
        ("a ", Global("g"), " b ", Call(Prim("+"), (Lit(1, "Int"), Lit(2, "Int"))), "{c}")
    )
    with pytest.raises(CandyError, match="unmatched"):
        expr('(format "a } b")')
    with pytest.raises(CandyError, match="exactly one form"):
        expr('(format "{}")')


def test_definitions_only_at_top_level() -> None:
    for src in ("(fn (x) (def y 1))", "(do (deft P ((x Int))))", "(if true (defn f (x) x))"):
        with pytest.raises(CandyError, match="only allowed at top level"):
            expr(src)
    with pytest.raises(CandyError, match="only allowed at top level"):
        prog("(sig f (Fn (Int) Int)) (defn f (x) (sig y Int))")


def test_skipped_forms() -> None:
    for src in ("(quote x)", "(import m)"):
        with pytest.raises(CandyError, match="not supported in the iMVP"):
            expr(src)


def test_macro_forms_rejected() -> None:
    # The Python translator is frozen: the macro forms (only in the Candy translator) are
    # special forms in the shared table, with no rule here.
    for src in ("(quo x)", "(quasi x)", "(unq x)", "(unq-sp x)", "(defmacro m (a) a)"):
        with pytest.raises(CandyError, match="is a special form, not a value"):
            expr(src)


def test_def_and_defn_with_sigs() -> None:
    int_t = TCon("Int")
    x = Local("x", 0)
    out = prog(
        """
        (sig sq (Fn (Int) Int))
        (sig ten Int)
        (defn sq (x) (* x x))
        (def ten (sq 10))
        (put ten)
        """
    )
    assert out == (
        Defn("sq", (x,), Call(Prim("*"), (x, x)), TFn((int_t,), int_t)),
        Def("ten", Call(Global("sq"), (Lit(10, "Int"),)), int_t),
        Call(Prim("put"), (Global("ten"),)),
    )


def test_forward_reference_and_recursion() -> None:
    out = prog(
        """
        (sig f (Fn (Int) Int)) (sig g (Fn (Int) Int))
        (defn f (n) (g n))
        (defn g (n) (if (< n 1) 0 (f (- n 1))))
        """
    )
    assert isinstance(out[0], Defn) and out[0].body == Call(Global("g"), (Local("n", 0),))


@pytest.mark.parametrize(
    ("src", "message"),
    [
        ("(def x 1)", r"needs a \(sig x Type\)"),
        ("(def x 1) (sig x Int)", "needs a"),
        ("(sig x Int) (def x)", "initial value is required"),
        ("(sig y Int)", "no def or defn of y"),
        ("(sig x Int) (sig x Int) (def x 1)", "more than one sig"),
        ("(sig x Int) (def x 1) (sig x Int) (def x 2)", "defined more than once"),
        ("(sig f Int) (defn f (x) x)", "must be a function type"),
        ("(sig f (Fn (Int Int) Int)) (defn f (x) x)", "takes 1 argument"),
        ("(sig f (Fn (Int) Int)) (defn f () 1)", "at least one"),
        ("(sig x Nope) (def x 1)", "unknown type Nope"),
        ("(sig x (List)) (def x 1)", "bad type"),
        ("(sig x (List Int Int)) (def x 1)", "takes 1 argument"),
        ("(sig x (Fn () Int)) (def x 1)", "bad function type"),
        ("(sig if Int) (def if 1)", "special form name"),
    ],
)
def test_program_errors(src: str, message: str) -> None:
    with pytest.raises(CandyError, match=message):
        prog(src)


def test_types() -> None:
    (out,) = prog("(sig xs (Map String (List (Maybe a)))) (def xs empty-list)")
    assert isinstance(out, Def)
    assert out.sig == TCon("Map", (TCon("String"), TCon("List", (TCon("Maybe", (TVar("a"),)),))))
    (tup_def,) = prog("(sig p (Tup Int Bool)) (def p (tup 1 true))")
    assert isinstance(tup_def, Def) and tup_def.sig == TCon("Tup", (TCon("Int"), TCon("Bool")))


def test_deft() -> None:
    out = prog(
        """
        (deft Vector2 ((x Int) (y Int)))
        (deft (Pair a b) ((first a) (second b)))
        (sig origin Vector2)
        (def origin (Vector2 0 0))
        """
    )
    assert out[0] == Deft("Vector2", (), (("x", TCon("Int")), ("y", TCon("Int"))))
    assert out[1] == Deft("Pair", ("a", "b"), (("first", TVar("a")), ("second", TVar("b"))))
    assert out[2] == Def("origin", Call(Global("Vector2"), (Lit(0, "Int"),) * 2), TCon("Vector2"))
    with pytest.raises(CandyError, match="unknown type variable"):
        prog("(deft Box ((v a)))")
    with pytest.raises(CandyError, match="deft field must be a name"):
        prog("(deft P ((1 Int)))")
    with pytest.raises(CandyError, match="given twice"):
        prog("(deft P ((x Int) (x Int)))")
    with pytest.raises(CandyError, match="takes 2 argument"):
        prog("(deft (Pair a b) ((f a) (s b))) (sig p (Pair Int)) (def p 1)")


SHAPES = """
(deft Shape (Circle ((r Double))) (Rect ((w Double) (h Double))) (Dot))
(sig s Shape)
(def s (Circle 1.0))
"""


def test_deft_sum() -> None:
    out = prog("(deft (Tree a) (Leaf) (Node ((l (Tree a)) (v a))))")
    tree = TCon("Tree", (TVar("a"),))
    assert out == (
        DeftSum(
            "Tree", ("a",), (Variant("Leaf", ()), Variant("Node", (("l", tree), ("v", TVar("a")))))
        ),
    )
    # A variant with no fields is a value, built with no arguments.
    (_, dot) = prog(SHAPES + "(put Dot)")[-2:]
    assert dot == Call(Prim("put"), (Call(Global("Dot"), ()),))


def test_match() -> None:
    *_, out = prog(SHAPES + "(match s ((Circle r) r) ((Rect _ h) h) ((Dot) 0.0))")
    r, h = Local("r", 0), Local("h", 1)
    assert out == Match(
        Global("s"),
        (
            Clause("Circle", (("r", r),), r),
            Clause("Rect", (("h", h),), h),
            Clause("Dot", (), Lit(0.0, "Double")),
        ),
        None,
    )
    *_, with_else = prog(SHAPES + "(match s ((Dot) 1) (else 2))")
    assert isinstance(with_else, Match) and with_else.default == Lit(2, "Int")


@pytest.mark.parametrize(
    ("src", "message"),
    [
        ("(match s ((Circle r) r))", "no clause for Dot, Rect"),
        ("(match s ((Circle r) r) ((Circle r) r) (else 1))", "more than one clause for Circle"),
        ("(match s ((Circle) 1) (else 2))", "needs 1 name"),
        ("(match s ((Rect a a) a) (else 2))", "must be different"),
        ("(match s (else 1))", "after a pattern"),
        ("(match s (else 1) ((Dot) 2))", "must be the last clause"),
        ("(match s ((Nope x) x))", "not a variant"),
        ("(match s (x 1))", "pattern must be"),
        ("(match s)", "expected (match"),
        ("(put (Dot))", "it is a value"),
        ("(put (Rect 1.0))", "takes 2 field"),
    ],
)
def test_match_errors(src: str, message: str) -> None:
    with pytest.raises(CandyError, match=re.escape(message)):
        prog(SHAPES + src)


def test_match_mixing_sums() -> None:
    with pytest.raises(CandyError, match="mix variants"):
        prog(SHAPES + "(deft B (T) (F)) (match s ((Dot) 1) ((T) 2) (else 3))")


def test_deft_sum_errors() -> None:
    with pytest.raises(CandyError, match="defined more than once: Box"):
        prog("(deft Box (Box ((v Int))))")
    with pytest.raises(CandyError, match="variant names are Capitalised"):
        prog("(deft S (A) (b))")
    with pytest.raises(CandyError, match="variant must be"):
        prog("(deft S (A ()))")
    with pytest.raises(CandyError, match="unknown type variable"):
        prog("(deft S (A ((x a))))")
    with pytest.raises(CandyError, match="unknown name Shape"):  # a type, not a value
        prog(SHAPES + "(put Shape)")
