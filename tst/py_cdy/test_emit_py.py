"""Tests for the Python backend (``emit_py.py``) and the whole translator (``translate_cdy``)."""

import subprocess
import sys
from pathlib import Path

import pytest
from mypy import api as mypy_api

from core_cdy import CandyError
from emit_py import mangle
from translate_cdy import translate

SQ = "(sig sq (Fn (Int) Int)) (defn sq (n) (* n n))\n"


def body(src: str) -> str:
    """The translated Python for ``src``, without the import header."""
    return translate(src).split("import cdy_rt.table_defs\n", 1)[1].strip()


def run(src: str, tmp_path: Path) -> str:
    """What the translated program prints."""
    out = tmp_path / "prog.py"
    out.write_text(translate(src), encoding="utf-8")
    done = subprocess.run([sys.executable, str(out)], capture_output=True, text=True, check=True)
    return done.stdout


def test_mangle() -> None:
    assert mangle("a-b") == "a_b"
    assert mangle("empty?") == "empty_p"
    assert mangle("set!") == "set_x"
    assert mangle("a*b") == "a_u002ab"
    assert mangle("if") == "if_"
    assert mangle("len") == "len_"
    assert mangle("math") == "math_"
    assert mangle("_cdy_t1") == "_cdy_t1_"


def test_functions_and_operators() -> None:
    assert body(SQ) == "def sq(n: int) -> int:\n    return n * n"
    assert body("(put (+ 1 2 3)) (put (< 1 2 3)) (put (and true (not false)))") == (
        "print(1 + 2 + 3)\nprint(1 < 2 < 3)\nprint(True and (not False))"
    )


def test_unit_function_has_no_return() -> None:
    assert body("(sig hi (Fn (String) Unit)) (defn hi (s) (put s))") == (
        "def hi(s: str) -> None:\n    print(s)"
    )


def test_annotations() -> None:
    src = """
    (deft (Pair a b) ((first a) (second b)))
    (sig a (List Int)) (def a empty-list)
    (sig b (Maybe String)) (def b nil)
    (sig c (Map String Double)) (def c (initial-table))
    (sig d (Fn (Int) Bool)) (def d (fn (x) (< x 1)))
    (sig e (Tup Int Char)) (def e (tup 1 \\c))
    (sig f (Pair Int Bool)) (def f (Pair 1 true))
    (sig ident (Fn (a) a)) (defn ident (x) x)
    """
    out = body(src.replace("(initial-table)", "initial-table"))
    assert "class Pair[a, b](_cdy_NamedTuple):\n    first: a\n    second: b" in out
    assert "a: tuple[int, ...] = ()" in out
    assert "b: str | None = None" in out
    assert "c: _cdy_Mapping[str, float] = cdy_rt.table.INITIAL_TABLE" in out
    assert "d: _cdy_Callable[[int], bool] = lambda x: x < 1" in out
    assert "e: tuple[int, str] = (1, 'c')" in out
    assert "f: Pair[int, bool] = Pair(1, True)" in out
    assert "def ident[a](x: a) -> a:" in out


def test_local_names() -> None:
    # An inner let reuses no name it would shadow: the outer x is renamed only when needed.
    src = "(sig f (Fn (Int) Int)) (defn f (x) (let ((y x)) (let ((x (+ y 1))) (+ x y))))"
    assert body(src) == (
        "def f(x: int) -> int:\n    y = x\n    _cdy_x_2 = y + 1\n    return _cdy_x_2 + y"
    )
    # A function local may reuse the name of a global it doesn't refer to.
    src = "(sig x Int) (def x 1) (sig g (Fn (Int) Int)) (defn g (n) (let ((x n)) x))"
    assert body(src).endswith("def g(n: int) -> int:\n    x = n\n    return x")


def test_name_errors() -> None:
    with pytest.raises(CandyError, match="both become the Python name a_b"):
        translate("(sig a-b Int) (def a-b 1) (sig a_b Int) (def a_b 2)")
    with pytest.raises(CandyError, match="can't start with _"):
        translate("(deft P ((_x Int)))")
    with pytest.raises(CandyError, match="can't be used as a value"):
        translate("(put +)")


PROGRAM = """
(sig fact (Fn (Int) Int))
(defn fact (n) (if (<= n 1) 1 (* n (fact (- n 1)))))
(deft Vector2 ((x Int) (y Int)))
(sig origin Vector2)
(def origin (Vector2 0 0))
(sig pair (Fn (Int) (Tup Int Int)))
(defn pair (n) (tup n (* n n)))
(sig empty? (Fn (String) Bool))
(defn empty? (s) (= (len s) 0))
(sig twice (Fn ((Fn (Int) Int) Int) Int))
(defn twice (f x) (f (f x)))
(put (format "fact 5 = {(fact 5)}, moved = {(assoc origin x 3)}"))
(put (let (((a b) (pair 7))) (+ a b)))
(put (if (empty? "") (do (put "was empty") "yes") "no"))
(put (get (assoc origin y 9) y))
(put (twice (fn (v) (let ((w (* v 2))) (+ w 1))) 3))
(put (cond ((< 2 1) "a") ((< 1 2) "b") (else "c")))
"""


def test_program_runs(tmp_path: Path) -> None:
    assert run(PROGRAM, tmp_path).splitlines() == [
        "fact 5 = 120, moved = Vector2(x=3, y=0)",
        "56",
        "was empty",
        "yes",
        "9",
        "15",
        "b",
    ]


def test_program_passes_mypy_strict(tmp_path: Path) -> None:
    out = tmp_path / "prog.py"
    out.write_text(translate(PROGRAM), encoding="utf-8")
    stdout, _, status = mypy_api.run(["--strict", "--no-incremental", str(out)])
    assert status == 0, stdout
