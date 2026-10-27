"""Tests for the self-hosted translator (``self_host.py``, ``src/cdy/cdyc.cdy``).

T1, the Candy translator built by the checked-in one (``bin``), is built once per test
session. Each test program (``tst/cdy/t1/NAME.cdy``, ``tst/cdy/NAME.cdy`` and
``tst/cdy/cdyc/NAME.cdy``) is translated by T1; the result must run and print ``NAME.out``,
and pass ``mypy --strict``. T1 itself must pass ``mypy --strict`` too: that type-checks the
Candy translator's own code.

T1 reads with its own reader (``src/cdy/read.cdy``). The edge cases it accepts and rejects
are those the Python translator's parser did, when it was here (``doc/hl_rqmt/bootstrap.md``).

The fixpoint: T1 translates the Candy translator into T2. T2 must pass ``mypy --strict``,
translate the translator into the very same text (T3 = T2), and translate every test
program exactly as T1 does. The checked-in translator ``bin/py/cdy_translator.py`` must be
that same T2: after changing the Candy translator, rebuild it with
``python src/py_cdy/self_host.py``. Run as a program (its driver, ``main`` in
``cdyc.cdy``), it must rebuild itself, and translate other files, with neither ``parsec``
nor ``py_cdy`` importable.
"""

import builtins
import keyword
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest
from mypy import api as mypy_api

from cdy_rt.primitives import CandyFail
from cdy_rt.spelling import SPELLINGS
from self_host import (
    BIN_PATH,
    CDY_DIR,
    LIBRARY,
    TRANSLATOR,
    copy_library,
    load,
    translate_file_with,
    translate_with,
)

ROOT = Path(__file__).resolve().parents[2]
CDYC_ONLY = ROOT / "tst" / "cdy" / "cdyc"
PROGRAMS = [
    *sorted((ROOT / "tst" / "cdy" / "t1").glob("*.cdy")),
    *sorted((ROOT / "tst" / "cdy").glob("*.cdy")),
    *sorted(CDYC_ONLY.glob("*.cdy")),
]
IDS = [p.stem for p in PROGRAMS]


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
    done = run(translate_file_with(t1, program), tmp_path, "t1")
    assert done.returncode == 0, done.stderr
    assert done.stdout == expected


@pytest.mark.parametrize("program", PROGRAMS, ids=IDS)
def test_mypy_strict(program: Path, t1: ModuleType, tmp_path: Path) -> None:
    out = tmp_path / f"{program.stem}.py"
    out.write_text(translate_file_with(t1, program), encoding="utf-8")
    stdout, _, status = mypy_api.run(["--strict", "--no-incremental", str(out)])
    assert status == 0, stdout


@pytest.mark.parametrize(
    ("imported", "message"),
    [
        ('(def x "open\n', "lib/b.cdy:1:8: parse error: string is never closed"),
        ("(import nope)", "lib/b.cdy:1:1: import: can't find nope.cdy in lib"),
        ("\n  (import)", "lib/b.cdy:2:3: import: expected (import name)"),
        ("(put\n  (f 1))", "lib/b.cdy:2:4: unknown name f"),
        ("(sig x Int)\n(def x (+ 1))", "lib/b.cdy:2:8: (+ ...) needs at least 2 arguments"),
        ("(def x 1)", "lib/b.cdy:1:1: x needs a (sig x Type)"),
        ("(sig x Int) (def x 1)\n(sig y Int) (def x 2)", "lib/b.cdy:2:18: defined more than once"),
        ("(sig f (Fn (Int) Int))\n(defn f (n) (if 1))", "lib/b.cdy:2:13: if: expected"),
        ("(sig x (Fn Int)) (def x 1)", "lib/b.cdy:1:8: bad function type"),
        ("(deft T (A) (b))", "lib/b.cdy:1:13: deft: variant names are Capitalised"),
    ],
)
def test_errors_say_where(
    imported: str, message: str, t1: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    Path("lib").mkdir()
    Path("main.cdy").write_text("(import lib/a)\n", encoding="utf-8")
    Path("lib/a.cdy").write_text("(import b)\n", encoding="utf-8")  # next to a.cdy
    Path("lib/b.cdy").write_text(imported, encoding="utf-8")
    with pytest.raises(CandyFail, match="^" + re.escape(message)):
        translate_file_with(t1, Path("main.cdy"))
    Path("main.cdy").write_text("(put\n", encoding="utf-8")
    with pytest.raises(CandyFail, match=r"^main.cdy:1:1: parse error: \( is never closed"):
        translate_file_with(t1, Path("main.cdy"))


@pytest.mark.parametrize(
    ("files", "message"),
    [
        (
            {
                "main.cdy": "(import a)\n(import b)",
                "a.cdy": "(sig x Int) (def x 1)",
                "b.cdy": "(sig x Int) (def x 2)",
            },
            "main.cdy:2:1: import: a and b both define x",
        ),
        (
            {"main.cdy": "(import a)", "a.cdy": "(import b)", "b.cdy": "(import a)"},
            "b.cdy:1:1: import: cycle a -> b -> a",
        ),
        ({"main.cdy": "(import main)"}, "main.cdy:1:1: import: cycle main -> main"),
        (
            {"main.cdy": "(import util)\n(import lib/util)", "util.cdy": "", "lib/util.cdy": ""},
            "import: two modules are named util: util.cdy and lib/util.cdy",
        ),
        (
            {
                "main.cdy": "(import a)\n(put (f 1))",
                "a.cdy": "(import b)",
                "b.cdy": "(sig f (Fn (Int) Int)) (defn f (n) n)",
            },
            "main.cdy:2:7: f is not defined here; b defines it, but this file doesn't import b",
        ),
        (
            {"main.cdy": "(import a)", "a.cdy": "(sig rest Int) (def rest 1)"},
            "main.cdy:1:1: import: prelude and a both define rest",
        ),
        (
            # A module's prefix against a mangled name (backlog B12).
            {
                "main.cdy": "(import a) (sig a--x Int) (def a--x 1)",
                "a.cdy": "(sig x Int) (def x 2)",
            },
            "x (in a) and a--x are one name in Python (a__x)",
        ),
    ],
)
def test_module_errors(
    files: dict[str, str],
    message: str,
    t1: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    Path("lib").mkdir()
    for name, text in files.items():
        Path(name).write_text(text + "\n", encoding="utf-8")
    with pytest.raises(CandyFail, match="^" + re.escape(message)):
        translate_file_with(t1, Path("main.cdy"))


LONG = 150  # Python allows 100 levels of indentation


@pytest.mark.parametrize(
    "src",
    [
        # As statements: the clauses become if/elif.
        "(sig f (Fn (Int) Int))\n(defn f (x) (cond {clauses} (else -1)))\n(put (f 140))",
        # As a value whose clauses need statements: one if/elif chain into one Temp.
        "(sig x Int) (def x 140)\n(put (cond {clauses} (else -1)))",
    ],
    ids=["tail", "value"],
)
def test_long_cond(src: str, t1: ModuleType, tmp_path: Path) -> None:
    clauses = " ".join(f"((= x {i}) (do (put {i}) (* 2 {i})))" for i in range(LONG))
    done = run(translate_with(t1, src.format(clauses=clauses)), tmp_path, "cond")
    assert (done.returncode, done.stdout) == (0, "140\n280\n"), done.stderr


def translate_macro_code(t1: ModuleType, forms: tuple[Any, ...]) -> str:
    """``forms`` as Python, translated as macro code (where quoting is allowed), as
    ``expand.cdy`` translates a macro program."""
    return cast(str, t1.translate_expanded(forms, t1.read__read_forms, {}, True))


def test_quoting_in_macro_code(t1: ModuleType, tmp_path: Path) -> None:
    program = CDYC_ONLY / "macro_code" / "quoting.cdy"
    done = run(
        translate_macro_code(t1, t1.include__read_program(str(program))), tmp_path, "quoting"
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout == program.with_suffix(".out").read_text(encoding="utf-8")


MACRO_FILE = """(defmacro twice (e) (quasi (+ (unq e) (unq e))))
(sig helper (Fn (Form) Form))
(defn helper (f) f)
"""


@pytest.mark.parametrize(
    ("src", "message"),
    [
        # A macro file's helpers run only while translating.
        ("(import-macros mac)\n(put (helper 1))", "p.cdy:2:7: unknown name helper"),
        ("(import-macros mac)\n(defmacro twice (a) a)", "p.cdy:2:1: defmacro: twice is already a"),
        ("(import-macros cycle)", "cycle.cdy:1:1: import-macros: cycle.cdy imports itself"),
    ],
)
def test_macro_file_errors(
    src: str, message: str, t1: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    Path("mac.cdy").write_text(MACRO_FILE, encoding="utf-8")
    Path("cycle.cdy").write_text("(import-macros cycle)\n", encoding="utf-8")
    Path("p.cdy").write_text(src, encoding="utf-8")
    with pytest.raises(CandyFail, match=re.escape(message)):
        translate_file_with(t1, Path("p.cdy"))


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
    for name in LIBRARY:
        assert (BIN_PATH.parent / name).read_bytes() == (CDY_DIR / name).read_bytes(), (
            f"bin/py/{name} is stale: run python src/py_cdy/self_host.py"
        )


BLOCKED_IMPORTS = """
import runpy
import sys
from importlib.abc import MetaPathFinder

class Block(MetaPathFinder):
    def find_spec(self, name, path, target=None):
        if name.split(".")[0] in ("parsec", "main", "self_host"):
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
    assert (done.returncode, done.stderr) == (1, "candy: bad.cdy:1:6: unknown name nope\n")
    done = run_bin(["missing.cdy"], tmp_path)
    assert done.returncode == 1 and done.stderr.startswith("candy: can't find")


def test_bin_driver_expands_macros(tmp_path: Path) -> None:
    # Run away from the repository, so form.cdy can only come from next to the translator.
    program = CDYC_ONLY / "macros.cdy"
    done = run_bin([str(program), "macros.py"], tmp_path)
    assert done.returncode == 0, done.stderr
    assert run((tmp_path / "macros.py").read_text(encoding="utf-8"), tmp_path, "m").stdout == (
        program.with_suffix(".out").read_text(encoding="utf-8")
    )


# --- the Python spellings, in Candy (emit.cdy; doc/hl_rqmt/library.md) ---


@pytest.mark.parametrize(
    ("name", "py"),
    (
        ("set-x!", "set_x_x"),
        ("empty?", "empty_p"),
        ("list", "list_"),
        ("_cdy_x", "_cdy_x_"),
        ("aéb", "a_u00e9b"),
        ("x😀", "x_u1f600"),
        ("def", "def_"),
        ("math", "math_"),
        ("ok_1", "ok_1"),
    ),
)
def test_py_mangle(t1: ModuleType, name: str, py: str) -> None:
    assert t1.emit__py_mangle(name) == py


def test_py_reserved_is_this_python(t1: ModuleType) -> None:
    live = {*keyword.kwlist, *dir(builtins)}
    assert set(t1.emit__PY_RESERVED) == live | {"math", "re", "cdy_rt"}, (
        "emit.cdy's PY_RESERVED is Python 3.14's; update it for this Python"
    )


def test_py_imports_cover_the_spellings(t1: ModuleType) -> None:
    modules = set(t1.emit__PY_IMPORTS)
    for entry in SPELLINGS.values():
        if entry.kind == "type":  # a type's text is a template (tuple[{}, ...])
            continue
        head = entry.py.split("(", 1)[0]
        if "." in head:
            assert head.rsplit(".", 1)[0] in modules, entry.py


@pytest.mark.parametrize(
    "text",
    ("", "a", "a'b", 'a"b', "a'\"b", "back\\slash", "\n\r\t", "\x00\x1f\x7f\x9f\xa0", "\u00e9"),
)
def test_py_str_is_repr(t1: ModuleType, text: str) -> None:
    assert t1.emit__py_str(text) == repr(text)


@pytest.mark.parametrize("name", ("py-mangle", "py-repr", "get-indent", "PY_IMPORTS"))
def test_programs_cant_see_the_python_helpers(t1: ModuleType, name: str) -> None:
    with pytest.raises(CandyFail, match=f"unknown name {name}"):
        translate_with(t1, f"(put {name})")


def test_list_functions_are_built_in(t1: ModuleType) -> None:
    # Fast: the runtime's, not Candy loops that copy the list for each item.
    source = translate_with(t1, "(put (map (fn (n) n) (tup 1)) (filter (fn (n) true) (tup 1)))")
    assert "cdy_rt.primitives.list_map(" in source and "cdy_rt.primitives.list_filter(" in source


def test_translator_needs_its_library(t1_path: Path, tmp_path: Path) -> None:
    translator = tmp_path / t1_path.name
    shutil.copyfile(t1_path, translator)  # without form.cdy, system.cdy, ...
    with pytest.raises(CandyFail, match="^the translator needs .* next to it"):
        translate_with(load(translator), "(put 1)")


@pytest.mark.parametrize(
    ("file", "change", "message"),
    [
        (
            "system.cdy",
            ("(sig slurp (Fn (String) String))\n", ""),
            "spelling.py: slurp is declared in neither special.cdy nor system.cdy",
        ),
        (
            "system.cdy",
            ("", "(sig nope Int)\n"),
            "system.cdy: nope has no Python mapping in spelling.py",
        ),
        ("system.cdy", ("", "(sig + (Fn (Int Int) Int))\n"), "system.cdy: + is already declared"),
        ("system.cdy", ("", "(sig len (Fn (Any) Int))\n"), "system.cdy: len is already declared"),
        ("system.cdy", ("", "(def x 1)\n"), "system.cdy: expected (sig name Type) or (deft Name)"),
        (
            "system.cdy",
            ("(deft Bool)\n", ""),
            "spelling.py: Bool is declared in neither special.cdy nor system.cdy",
        ),
        ("system.cdy", ("", "(deft Nope)\n"), "system.cdy: Nope has no Python type in spelling.py"),
        ("system.cdy", ("", "(deft (List a))\n"), "system.cdy: List is already declared"),
        (
            "system.cdy",
            ("", "(deft (Pair A))\n"),
            "system.cdy: expected (deft Name) or (deft (Name",
        ),
        (
            "special.cdy",
            ("(op not unary)\n", ""),
            "spelling.py: not is declared in neither special.cdy nor system.cdy",
        ),
        (
            "special.cdy",
            ("", "(special len)\n"),
            "special.cdy: len is a special form, so spelling.py can't spell it",
        ),
        (
            "special.cdy",
            ("", "(op len variadic)\n"),
            "special.cdy: len has no variadic entry in spelling.py",
        ),
        (
            "special.cdy",
            ("", "(op len unary)\n"),
            "special.cdy: len has no unary entry in spelling.py",
        ),
        ("special.cdy", ("", "(special if)\n"), "special.cdy: if is declared more than once"),
        ("special.cdy", ("", "(op - binary)\n"), "special.cdy: expected (special name), (op name"),
    ],
)
def test_library_errors(
    file: str, change: tuple[str, str], message: str, t1_path: Path, tmp_path: Path
) -> None:
    translator = tmp_path / t1_path.name
    shutil.copyfile(t1_path, translator)
    copy_library(tmp_path)
    declared = tmp_path / file
    old, extra = change
    text = declared.read_text(encoding="utf-8")
    assert old in text
    declared.write_text(text.replace(old, "") + extra, encoding="utf-8")
    with pytest.raises(CandyFail, match=re.escape(message)):
        translate_with(load(translator), "(put 1)")


def test_special_forms_are_declared(t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match="if is a special form, not a value"):
        translate_with(t1, "(put if)")
    with pytest.raises(CandyFail, match="defmacro: if is a special form"):
        translate_with(t1, "(defmacro if (a) a)\n(put 1)")


def test_builtin_arity_comes_from_system(t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match=re.escape("(slurp ...) takes 1 argument(s), got 2")):
        translate_with(t1, '(put (slurp "a" "b"))')
    with pytest.raises(CandyFail, match=re.escape("(not ...) takes 1 argument(s), got 2")):
        translate_with(t1, "(put (not true false))")
    assert "print(1, 2, 3)" in translate_with(t1, "(put 1 2 3)")  # put is Any: any number


# --- the reader ---


def reads(t1: ModuleType, text: str) -> bool:
    """Whether T1's reader accepts ``text``."""
    try:
        t1.read__read_forms(text)
    except CandyFail:
        return False
    return True


@pytest.mark.parametrize(
    ("text", "accepted"),
    [
        ("", True),
        (" ; only a comment", True),
        ("(a (b c) ()) d", True),
        ("100 -7 1500l 1b -2b 3.14f 10.0 -0.5", True),
        ("\\e \\( \\;", True),
        ("true false trueish true1", True),
        ("- + -x +5 -5x a#b a.b ->", True),
        ('"" "a b" "\\n\\t\\"\\\\\\/\\b\\f\\r" "\\u0041\\u00e9"', True),
        ('a"b"c', True),
        ("a\\b", True),
        ("(a)(b)", True),
        ("x;c\ny", True),
        ("\u0663\u0662", True),
        ("\u00b2", True),
        (".5", True),
        ("12x", False),
        ("1.5l", False),
        ("1.", False),
        ("#a", False),
        ("'a", False),
        ("a'b", False),
        ("\\ab", False),
        ("\\", False),
        ("\\ x", False),
        ('"abc', False),
        ('"\\q"', False),
        ('"\\u00g1"', False),
        ("(a", False),
        ("a)", False),
        (")", False),
    ],
)
def test_reader_accepts(text: str, accepted: bool, t1: ModuleType) -> None:
    assert reads(t1, text) == accepted


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("(put\n  (a b)", "line 1, column 1: parse error: ( is never closed"),
        ('(put "a\n', "line 1, column 6: parse error: string is never closed"),
        ("x\n  )", "line 2, column 3: parse error: unexpected )"),
        ("(a 12x)", "line 1, column 4: parse error: unexpected 1"),
        ('"\\q"', "line 1, column 2: parse error: bad escape sequence"),
        ("\\ab", "line 1, column 1: parse error: a char is"),
        ("(a b__c)", "line 1, column 4: parse error: a name can't contain __"),
    ],
)
def test_reader_errors(text: str, message: str, t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match="^" + re.escape(message)):
        t1.read__read_forms(text)


def test_reader_positions(t1: ModuleType) -> None:
    forms = t1.read__read_source("f.cdy", "(a\n  (b c))\n x")
    pos = t1.form__form_pos
    assert pos(forms[0]) == t1.form__Pos("f.cdy", 1, 1)
    assert [pos(f) for f in forms[0].items] == [
        t1.form__Pos("f.cdy", 1, 2),
        t1.form__Pos("f.cdy", 2, 3),
    ]
    assert pos(forms[0].items[1].items[1]) == t1.form__Pos("f.cdy", 2, 6)
    assert pos(forms[1]) == t1.form__Pos("f.cdy", 3, 2)
    assert pos(t1.read__read_forms("x")[0]) == t1.form__NOWHERE  # read_forms gives no positions
