"""Tests for the interpreter (``src/cdy/interp.cdy``; ``doc/hl_rqmt/interpreter.md``): a
program run on it, in this process through T1 and through the translator's flag."""

import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from cdy_rt.primitives import CandyFail

# Every kind of Core expression and top-level form: a record and a sum, `get` and `assoc`,
# `match` with an `else`, a rest parameter, recursion, `let` (an applied `fn`), a `Tup`
# pattern, `format`, `and`, `or`, a chained comparison, `cond`, `do`, and `main`.
PROGRAM = """\
(deft Pt ((x Int) (y Int)))
(deft Sh (Dot) (Box ((w Int))))
(sig f (Fn (Sh) Int))
(defn f (s) (match s ((Box w) w) (else 0)))
(sig p Pt)
(def p (Pt 1 2))
(sig sum (Fn (Int (Rest Int)) Int))
(defn sum (a more) (fold (fn (acc n) (+ acc n)) a more))
(sig fact (Fn (Int) Int))
(defn fact (n) (if (= n 0) 1 (* n (fact (- n 1)))))
(put (get p x) (get (assoc p y 5) y) (f Dot) (f (Box 3)))
(put (sum 1 2 3) (fact 10) (let ((a 2) (b (+ a 1))) (* a b)) (match (Tup 4 "z") ((Tup n s) (++ s s))))
(put (format "x={(get p x)} {(and true false)} {(or false true)} {(< 1 2 3)}") (cond ((> 1 2) "no") (else "yes")))
(do (put "a") (put "b"))
(sig main (Fn ((List String)) Int))
(defn main (args) (do (put (len args)) 3))
"""

EXPECTED = "1 5 0 3\n6 3628800 6 zz\nx=1 false true true yes\na\nb\n2\n"


def test_interpret_in_process(
    t1: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "p.cdy"
    path.write_text(PROGRAM, encoding="utf-8")
    assert cast(int, t1.interpret_file(str(path), ("one", "two"))) == 3
    assert capsys.readouterr().out == EXPECTED


def test_interpret_flag(t1_path: Path, tmp_path: Path) -> None:
    path = tmp_path / "p.cdy"
    path.write_text(PROGRAM, encoding="utf-8")
    done = subprocess.run(
        [sys.executable, str(t1_path), "--interpret", str(path), "one", "two"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert (done.returncode, done.stdout) == (3, EXPECTED), done.stderr


def test_interpret_agrees_with_the_python_target(t1: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "p.cdy"
    path.write_text(PROGRAM, encoding="utf-8")
    out = tmp_path / "p.py"
    out.write_text(cast(str, t1.translate_file(str(path))), encoding="utf-8")
    done = subprocess.run(
        [sys.executable, str(out), "one", "two"], capture_output=True, text=True, check=False
    )
    assert (done.returncode, done.stdout) == (3, EXPECTED), done.stderr


def test_interpret_usage(t1_path: Path) -> None:
    done = subprocess.run(
        [sys.executable, str(t1_path), "--interpret"], capture_output=True, text=True, check=False
    )
    assert done.returncode == 2
    assert "--interpret FILE.cdy" in done.stderr


def test_every_declared_builtin_is_interpreted(t1: ModuleType) -> None:
    builtins = dict(t1.expand__library_builtins(None))
    t1.interp_builtins__check_interp_builtins(builtins)
    assert len(t1.interp_builtins__BUILTINS) == 71  # and 4 values: nil, empty-list, ...
    declared: dict[str, Any] = {
        **builtins,
        "zz": t1.core__Typed(t1.core__TFn((), t1.core__ANY), "system"),
    }
    with pytest.raises(CandyFail, match="no built-in for zz"):
        t1.interp_builtins__check_interp_builtins(declared)
    del builtins["len"]
    with pytest.raises(CandyFail, match="a built-in nothing declares: len"):
        t1.interp_builtins__check_interp_builtins(builtins)


# `show` and `text` of every kind of value, by the value (Question 3), against the Python
# target's, by the type: the sizes of number, a float's exponent, a string's escapes and a
# control character, a char, the collections, a record, a generic one, a fieldless
# variant, `Maybe`.
SHOWN = """\
(import map ())
(deft (Box a) ((v a)))
(deft Sh (Dot) (Pt ((x Int) (y Int))))
(sig none (Maybe Int))
(def none None)
(sig empty (List Int))
(def empty empty-list)
(put (show 1) (show -5) (show 1500l) (show 7b) (show 2.5f) (show 10.0) (show 1.0e20) (show true))
(put (show \\a) (show "a \\"b\\"\\n\\t\\\\ \\u0001") (show nil) (show empty) (show none))
(put (show (List 1 2)) (show (Tup 1 "a")) (show (map.from (List (Tup "k" 1)))) (show (Box 3)))
(put (show Dot) (show (Pt 1 2)) (show (Some 4)) (show (Box (List "x"))))
(put \\c "s" 3 1.5 (List "a") (Some \\d))
"""


def test_show_and_text_agree_with_the_python_target(
    t1: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out = tmp_path / "shown.py"
    out.write_text(cast(str, t1.translate_text(SHOWN)), encoding="utf-8")
    done = subprocess.run([sys.executable, str(out)], capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stderr
    assert cast(int, t1.interpret_text(SHOWN, ())) == 0
    assert capsys.readouterr().out == done.stdout


# A self tail call, a mutual one and one in a `match` clause run as loops (expr.tail-calls).
TAIL_CALLS = """\
(sig count (Fn (Int Int) Int))
(defn count (n acc) (if (= n 0) acc (count (- n 1) (+ acc 1))))
(sig even (Fn (Int) Bool))
(defn even (n) (if (= n 0) true (odd (- n 1))))
(sig odd (Fn (Int) Bool))
(defn odd (n) (if (= n 0) false (even (- n 1))))
(sig down (Fn ((Maybe Int)) Int))
(defn down (m) (match m ((Some n) (if (= n 0) 0 (down (Some (- n 1))))) ((None) -1)))
(put (count 100000 0) (even 100001) (down (Some 50000)))
"""


def test_interpret_tail_calls(t1: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    assert cast(int, t1.interpret_text(TAIL_CALLS, ())) == 0
    assert capsys.readouterr().out == "100000 false 0\n"


# A panic: `fail`'s message, `candy: ` first, exit status 1 and no traceback, as a
# translated program's (library.errors); an index out of range is the spec's message.
PANICS = {
    '(put 1)\n(fail "stop here")\n': "candy: stop here\n",
    "(put (at (List 1 2) 5))\n": "candy: at: index out of range: 5, for length 2\n",
}


@pytest.mark.parametrize("source", PANICS)
def test_interpret_panics(source: str, t1_path: Path, tmp_path: Path) -> None:
    path = tmp_path / "p.cdy"
    path.write_text(source, encoding="utf-8")
    done = subprocess.run(
        [sys.executable, str(t1_path), "--interpret", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 1
    assert done.stderr == PANICS[source]


# Every kind of form, with its position, crosses to the interpreter as macro code's Form
# and comes back the same (interp_macros.cdy; doc/hl_rqmt/host_macros.md).
FORMS = '(f (1 2l 3b 1.5f 2.5) "s" \\x true)\n(g)\n'


def test_forms_cross_to_the_interpreter_and_back(t1: ModuleType) -> None:
    forms = t1.read__read_source("t.cdy", FORMS)
    assert len(forms) == 2
    for form in forms:
        value = t1.interp_macros__form_value("form", form)
        assert t1.interp_macros__value_form(value) == form
