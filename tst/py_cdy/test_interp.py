"""Tests for the interpreter (``src/cdy/interp.cdy``; ``doc/hl_rqmt/interpreter.md``): a
program run on it, in this process through T1 and through the translator's flag."""

import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest

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
