"""The self-hosted translator: Candy's own translator, reader included.

See ``doc/hl_rqmt/self_hosting_primo.md``. The translator is written in Candy, in the files
``TRANSLATOR_FILES`` under ``src/cdy/``. ``build_t1`` translates them with the Python
translator into one module, T1, under ``output/t1/``. ``translate_t1`` then hands a Candy
program's text to T1's ``translate_text``, which reads it with the Candy reader
(``read.cdy``, stage 3) and translates it.

Until stage 3, the driver parsed with ``parse_cdy`` and converted its nodes into T1's
``Form`` variants. ``parse_forms`` still does that, so tests can check that the two readers
agree.

Candy has no ``import`` yet, so the translator's files are joined into one program (a
stopgap, listed in ``doc/leaks.md``).

The checked-in translator ``bin/py/cdy_translator.py`` is T2, T1's translation of the
translator's own source (the fixpoint: it translates that source into itself). Running this
file rebuilds it: ``python src/py_cdy/self_host.py``. ``translate_bin`` translates with it,
so Candy runs without the Python translator or its parser.
"""

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any, cast

from parsec import parse

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
from translate_cdy import translate

ROOT = Path(__file__).resolve().parents[2]
CDY_DIR = ROOT / "src" / "cdy"
TRANSLATOR_FILES = ("form", "read", "core", "lower", "emit")
T1_DIR = Path("output") / "t1"
T1_MODULE = "cdy_translator"
BIN_PATH = ROOT / "bin" / "py" / f"{T1_MODULE}.py"

# The translator recurses once per item of each list it walks (only self tail calls loop).
RECURSION_LIMIT = 20_000


def translator_source() -> str:
    """The Candy translator's files, joined into one program."""
    parts = [(CDY_DIR / f"{name}.cdy").read_text(encoding="utf-8") for name in TRANSLATOR_FILES]
    return "\n".join(parts)


def build_t1(out_dir: Path = T1_DIR) -> Path:
    """Translate the Candy translator with the Python translator; returns the module's path."""
    out = out_dir / f"{T1_MODULE}.py"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(translate(translator_source()), encoding="utf-8")
    return out


def load(path: Path) -> ModuleType:
    """The Python module at ``path``."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"can't load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def to_form(node: SExpr, t1: ModuleType) -> Any:
    """A ``parse_cdy`` node as the matching ``Form`` variant of the translator module ``t1``."""
    variant: Callable[..., Any]
    match node:
        case Symbol(name):
            return t1.Sym(name)
        case SList(items):
            return t1.Lst(tuple(to_form(item, t1) for item in items))
        case Str(val):
            variant = t1.Txt
        case Int(val):
            variant = t1.IntLit
        case Long(val):
            variant = t1.LongLit
        case Byte(val):
            variant = t1.ByteLit
        case Float(val):
            variant = t1.FloatLit
        case Double(val):
            variant = t1.DoubleLit
        case Char(val):
            variant = t1.CharLit
        case Bool(val):
            variant = t1.BoolLit
    return variant(val)


def parse_forms(t1: ModuleType, text: str) -> tuple[Any, ...]:
    """``text`` parsed by ``parse_cdy``, as ``t1``'s ``Form`` variants (to compare readers)."""
    return tuple(to_form(node, t1) for node in parse(program, text))


def translate_with(t1: ModuleType, text: str) -> str:
    """The Candy program ``text`` as Python source, read and translated by ``t1``."""
    limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(limit, RECURSION_LIMIT))
    try:
        return cast(str, t1.translate_text(text))
    finally:
        sys.setrecursionlimit(limit)


def translate_t1(text: str) -> str:
    """The Candy program ``text`` as Python source, translated by a freshly built T1."""
    return translate_with(load(build_t1()), text)


def build_bin(path: Path = BIN_PATH) -> Path:
    """Rebuild the checked-in translator: T1's translation of the translator's source."""
    path.write_text(translate_with(load(build_t1()), translator_source()), encoding="utf-8")
    return path


def translate_bin(text: str) -> str:
    """The Candy program ``text`` as Python source, translated by the checked-in translator."""
    return translate_with(load(BIN_PATH), text)


if __name__ == "__main__":
    print(f"wrote {build_bin()}")
