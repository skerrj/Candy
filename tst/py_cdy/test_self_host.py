"""Tests for the self-hosted translator (``self_host.py``, ``src/cdy/cdyc.cdy``).

T1, the Candy translator built by the checked-in one (``bin``), is built once per test
session. Each test program (``tst/cdy/t1/NAME.cdy``, ``tst/cdy/NAME.cdy`` and
``tst/cdy/cdyc/NAME.cdy``) is translated by T1, and all but those in ``tst/cdy/cdyc/`` also
by the Python translator, which is frozen (``cdyc/`` holds programs that use what only the
Candy translator has, such as ``import``). Every result must run and print ``NAME.out``,
and T1's must pass ``mypy --strict``. T1 itself must pass ``mypy --strict`` too: that
type-checks the Candy translator's own code.

T1 reads with its own reader (``src/cdy/read.cdy``), which must accept exactly what
``parse_cdy`` accepts, and read it into the same forms.

The fixpoint: T1 translates the Candy translator into T2. T2 must pass ``mypy --strict``,
translate the translator into the very same text (T3 = T2), and translate every test
program exactly as T1 does. The checked-in translator ``bin/py/cdy_translator.py`` must be
that same T2: after changing the Candy translator, rebuild it with
``python src/py_cdy/self_host.py``. Run as a program (its driver, ``main`` in
``cdyc.cdy``), it must rebuild itself, and translate other files, with neither ``parsec``
nor ``py_cdy`` importable.
"""

import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
from mypy import api as mypy_api
from parsec import ParseFailure

from cdy_rt.table_defs import CandyFail
from self_host import (
    BIN_PATH,
    CDY_DIR,
    TRANSLATOR,
    build_t1,
    build_with,
    load,
    parse_forms,
    translate_file_with,
    translate_with,
)
from translate_cdy import translate

ROOT = Path(__file__).resolve().parents[2]
CDYC_ONLY = ROOT / "tst" / "cdy" / "cdyc"
PROGRAMS = [
    *sorted((ROOT / "tst" / "cdy" / "t1").glob("*.cdy")),
    *sorted((ROOT / "tst" / "cdy").glob("*.cdy")),
    *sorted(CDYC_ONLY.glob("*.cdy")),
]
IDS = [p.stem for p in PROGRAMS]


@pytest.fixture(name="t1_path", scope="session")
def fixture_t1_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """T1, built once for the session."""
    return build_t1(tmp_path_factory.mktemp("t1"))


@pytest.fixture(name="t1", scope="session")
def fixture_t1(t1_path: Path) -> ModuleType:
    """T1, loaded."""
    return load(t1_path)


@pytest.fixture(name="t2", scope="session")
def fixture_t2(t1_path: Path, tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, str]:
    """T2 (T1's translation of the translator) written to a file, and its source text."""
    path = build_with(t1_path, tmp_path_factory.mktemp("t2"))
    return path, path.read_text(encoding="utf-8")


def run(source: str, tmp_path: Path, name: str) -> subprocess.CompletedProcess[str]:
    """Write ``source`` to ``tmp_path/name.py`` and run it from the repository root."""
    path = tmp_path / f"{name}.py"
    path.write_text(source, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(path)], capture_output=True, text=True, check=False, cwd=ROOT
    )


def test_t1_passes_mypy_strict(t1_path: Path) -> None:
    stdout, _, status = mypy_api.run(["--strict", "--no-incremental", str(t1_path)])
    assert status == 0, stdout


@pytest.mark.parametrize("program", PROGRAMS, ids=IDS)
def test_output(program: Path, t1: ModuleType, tmp_path: Path) -> None:
    expected = program.with_suffix(".out").read_text(encoding="utf-8")
    sources = [("t1", translate_file_with(t1, program))]
    if program.parent != CDYC_ONLY:
        sources.append(("py", translate(program.read_text(encoding="utf-8"))))
    for name, source in sources:
        done = run(source, tmp_path, name)
        assert done.returncode == 0, f"{name}: {done.stderr}"
        assert done.stdout == expected, name


@pytest.mark.parametrize("program", PROGRAMS, ids=IDS)
def test_mypy_strict(program: Path, t1: ModuleType, tmp_path: Path) -> None:
    out = tmp_path / f"{program.stem}.py"
    out.write_text(translate_file_with(t1, program), encoding="utf-8")
    stdout, _, status = mypy_api.run(["--strict", "--no-incremental", str(out)])
    assert status == 0, stdout


@pytest.mark.parametrize(
    ("src", "message"),
    [
        ("(put nope)", "unknown name nope"),
        ("(def x 1)", "x needs a (sig x Type)"),
        ("(put (if 1))", "if: expected"),
        ("(put (cond (else 1) (true 2)))", "must be the last clause"),
        ("(put ())", "empty form"),
        ("(put if)", "special form, not a value"),
        ("(put (quote x))", "not supported by the Candy translator yet"),
        ("(put (+ 1))", "needs at least 2 arguments"),
        ("(put (len 1 2))", "takes 1 argument(s), got 2"),
        ("(sig y Int)", "no def or defn of y"),
        ("(sig x Int) (def x 1) (sig x Int)", "comes after its definition"),
        ("(sig x Int) (sig x Int) (def x 1)", "more than one sig"),
        ("(sig x Int) (def x 1) (def x 2)", "defined more than once: x"),
        ("(deft Box (Box ((v Int))))", "defined more than once: Box"),
        ("(put (let ((x)) x))", "binding must be"),
        ("(put (let (((a b))) a))", "binding must be"),
        ("(put (fn () 1))", "at least one"),
        ("(put (tup))", "at least one item"),
        ("(put (get 1))", "expected (get obj field)"),
        ("(put (assoc 1 x))", "expected (assoc obj field value"),
        ("(put (assoc 1 x 2 y))", "expected (assoc obj field value"),
        ('(put (format "a } b"))', "unmatched }"),
        ('(put (format "a { b"))', "unmatched {"),
        ('(put (format "{1 2}"))', "exactly one form"),
        ("(sig f (Fn (Int) Int)) (defn f (x y) x)", "one type per argument"),
        ("(put (do (sig x Int)))", "only allowed at top level"),
        ("(import)", "expected (import name)"),
        ('(import "x")', "expected (import name)"),
        ("(import a b)", "expected (import name)"),
        ("(import nope)", "can't find nope.cdy in ."),
        ("(put (do (import x)))", "only allowed at top level"),
        ("(sig main Int) (def main 1)", "main must be a defn"),
        ("(sig main (Fn (Int) Int)) (defn main (n) n)", "main must be typed"),
    ],
)
def test_errors(src: str, message: str, t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match=re.escape(message)):
        translate_with(t1, src)


SHAPES = """
(deft Shape (Circle ((r Double))) (Rect ((w Double) (h Double))) (Dot))
(sig s Shape)
(def s (Circle 1.0))
"""


@pytest.mark.parametrize(
    ("src", "message"),
    [
        ("(put (match s ((Circle r) r)))", "no clause for Rect, Dot"),
        (
            "(put (match s ((Circle r) r) ((Circle r) r) (else 1)))",
            "more than one clause for Circle",
        ),
        ("(put (match s ((Circle) 1) (else 2)))", "pattern needs that many names"),
        ("(put (match s ((Rect a a) a) (else 2)))", "must be different"),
        ("(put (match s (else 1)))", "after a pattern"),
        ("(put (match s (else 1) ((Dot) 2)))", "must be the last clause"),
        ("(put (match s ((Nope x) x)))", "not a variant"),
        ("(put (match s (x 1)))", "pattern must be"),
        ("(put (match s))", "expected (match"),
        ("(put (Dot))", "it is a value"),
        ("(put (Rect 1.0))", "takes 2 field"),
        (
            "(deft B (T) (F)) (put (match s ((Dot) 1) ((T) 2) (else 3)))",
            "mix variants of Shape and B",
        ),
        ("(deft S2 (A) (b))", "variant names are Capitalised"),
        ("(deft S2 (A ()))", "variant must be"),
    ],
)
def test_match_errors(src: str, message: str, t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match=re.escape(message)):
        translate_with(t1, SHAPES + src)


def test_fixpoint_t2_passes_mypy_strict(t2: tuple[Path, str]) -> None:
    stdout, _, status = mypy_api.run(["--strict", "--no-incremental", str(t2[0])])
    assert status == 0, stdout


def test_fixpoint_t2_reproduces_itself(t2: tuple[Path, str]) -> None:
    path, source = t2
    assert translate_file_with(load(path), TRANSLATOR) == source  # T3 == T2


@pytest.mark.parametrize("program", PROGRAMS, ids=IDS)
def test_fixpoint_t1_and_t2_agree(program: Path, t1: ModuleType, t2: tuple[Path, str]) -> None:
    assert translate_file_with(load(t2[0]), program) == translate_file_with(t1, program)


def test_bin_is_t2(t2: tuple[Path, str]) -> None:
    assert BIN_PATH.read_text(encoding="utf-8") == t2[1], (
        "bin/py/cdy_translator.py is stale: run python src/py_cdy/self_host.py"
    )


BLOCKED_IMPORTS = """
import runpy
import sys
from importlib.abc import MetaPathFinder

class Block(MetaPathFinder):
    def find_spec(self, name, path, target=None):
        if name.split(".")[0] in ("parsec", "parse_cdy", "core_cdy", "translate_cdy"):
            raise ImportError(f"blocked: {name}")
        return None

sys.meta_path.insert(0, Block())
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""


def run_bin(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run the checked-in translator as a program (its driver, ``main`` in ``cdyc.cdy``),
    with ``parsec`` and ``py_cdy`` blocked."""
    return subprocess.run(
        [sys.executable, "-c", BLOCKED_IMPORTS, str(BIN_PATH), *args],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
    )


def test_bin_rebuilds_itself_without_python_translator(tmp_path: Path) -> None:
    done = run_bin([str(TRANSLATOR), "bin.py"], tmp_path)
    assert done.returncode == 0, done.stderr
    assert done.stderr == f"candy: {TRANSLATOR} -> bin.py\n"
    assert (tmp_path / "bin.py").read_text(encoding="utf-8") == BIN_PATH.read_text(encoding="utf-8")


def test_bin_driver(tmp_path: Path) -> None:
    program = ROOT / "tst" / "cdy" / "sums.cdy"
    done = run_bin([str(program)], tmp_path)
    assert done.returncode == 0, done.stderr
    out = tmp_path / "output" / "sums.py"
    assert run(out.read_text(encoding="utf-8"), tmp_path, "sums").stdout == (
        program.with_suffix(".out").read_text(encoding="utf-8")
    )
    assert run_bin([], tmp_path).returncode == 2
    assert run_bin(["a.cdy", "b.py", "c"], tmp_path).returncode == 2
    (tmp_path / "bad.cdy").write_text("(put nope)\n", encoding="utf-8")
    done = run_bin(["bad.cdy"], tmp_path)
    assert (done.returncode, done.stderr) == (1, "candy: unknown name nope\n")
    done = run_bin(["missing.cdy"], tmp_path)
    assert done.returncode == 1 and done.stderr.startswith("candy: can't find")


# --- the reader ---

SOURCES = PROGRAMS + sorted(CDY_DIR.glob("*.cdy"))


def read_both(t1: ModuleType, text: str) -> tuple[str, str]:
    """What each reader makes of ``text``: the forms' repr (which shows each variant), or
    ``"error"``."""
    try:
        theirs = repr(parse_forms(t1, text))
    except ParseFailure:
        theirs = "error"
    try:
        mine = repr(t1.read_forms(text))
    except CandyFail:
        mine = "error"
    return mine, theirs


@pytest.mark.parametrize("source", SOURCES, ids=[p.stem for p in SOURCES])
def test_reader_agrees_on_files(source: Path, t1: ModuleType) -> None:
    mine, theirs = read_both(t1, source.read_text(encoding="utf-8"))
    assert mine == theirs


@pytest.mark.parametrize(
    "text",
    [
        "",
        " ; only a comment",
        "(a (b c) ()) d",
        "100 -7 1500l 1b -2b 3.14f 10.0 -0.5",
        "\\e \\( \\;",
        "true false trueish true1",
        "- + -x +5 -5x a#b a.b ->",
        '"" "a b" "\\n\\t\\"\\\\\\/\\b\\f\\r" "\\u0041\\u00e9"',
        'a"b"c',
        "a\\b",
        "(a)(b)",
        "x;c\ny",
        "\u0663\u0662",
        "12x",
        "1.5l",
        "1.",
        ".5",
        "#a",
        "'a",
        "a'b",
        "\\ab",
        "\\",
        "\\ x",
        '"abc',
        '"\\q"',
        '"\\u00g1"',
        "(a",
        "a)",
        ")",
        "\u00b2",
    ],
)
def test_reader_agrees(text: str, t1: ModuleType) -> None:
    mine, theirs = read_both(t1, text)
    assert mine == theirs


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("(put\n  (a b)", "line 1, column 1: ( is never closed"),
        ('(put "a\n', "line 1, column 6: string is never closed"),
        ("x\n  )", "line 2, column 3: unexpected )"),
        ("(a 12x)", "line 1, column 4: unexpected 1"),
        ('"\\q"', "line 1, column 2: bad escape sequence"),
        ("\\ab", "line 1, column 1: a char is"),
    ],
)
def test_reader_errors(text: str, message: str, t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match="parse error at " + re.escape(message)):
        t1.read_forms(text)
