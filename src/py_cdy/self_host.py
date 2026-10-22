"""The self-hosted translator: Candy's own translator, reader included.

See ``doc/hl_rqmt/self_hosting_primo.md`` and ``doc/hl_rqmt/self_host_cleanup.md``. The
translator is written in Candy: ``src/cdy/cdyc.cdy`` and the files it imports. The
checked-in translator ``bin/py/cdy_translator.py`` builds it: ``build_t1`` translates it
with ``bin`` into T1 under ``output/t1/``. ``translate_t1`` hands a Candy file to T1's
``translate_file``, which reads it with the Candy reader (``read.cdy``), includes its
imports (``include.cdy``) and translates it.

``build_bin`` rebuilds ``bin``: T1 translates the translator into T2, which must translate
it into the very same text again (the fixpoint, T3 = T2) and pass ``mypy --strict``; only
then does T2 replace ``bin``. A change to ``src/cdy/`` that ``bin`` can't translate, or that
breaks the result, so never reaches ``bin``, and the previous copy is in git. Run this file
to rebuild: ``python src/py_cdy/self_host.py``.

The Python translator that first built the translator is no longer here: it is at tag
``self-host-py``, and ``script/bootstrap.py`` builds every ``bin`` since from it, through
the history (``doc/hl_rqmt/bootstrap.md``).
"""

import importlib.util
import shutil
from pathlib import Path
from types import ModuleType
from typing import cast

from mypy import api as mypy_api

ROOT = Path(__file__).resolve().parents[2]
CDY_DIR = ROOT / "src" / "cdy"
TRANSLATOR = CDY_DIR / "cdyc.cdy"
T1_DIR = Path("output") / "t1"
T2_DIR = Path("output") / "t2"
T1_MODULE = "cdy_translator"
BIN_PATH = ROOT / "bin" / "py" / f"{T1_MODULE}.py"
# The Candy files a translator reads while it translates, kept next to it: macro code uses
# Form and its helpers, and every file gets the prelude's macros (expand.cdy).
LIBRARY = ("form.cdy", "prelude_macros.cdy", "forms.cdy", "system.cdy", "prelude.cdy")


class FixpointError(Exception):
    """A rebuilt translator doesn't reproduce itself or doesn't pass ``mypy --strict``."""


def load(path: Path) -> ModuleType:
    """The Python module at ``path``."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"can't load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def translate_with(t1: ModuleType, text: str) -> str:
    """The Candy program ``text`` as Python source, read and translated by ``t1``."""
    return cast(str, t1.translate_text(text))


def translate_file_with(translator: ModuleType, path: Path) -> str:
    """The Candy file at ``path`` as Python source, translated by ``translator``, which
    includes the file's imports."""
    return cast(str, translator.translate_file(str(path)))


def build_with(translator: Path, out_dir: Path) -> Path:
    """Translate the Candy translator with the translator module at ``translator`` into
    ``out_dir``, with its ``LIBRARY``; returns the new module's path."""
    out = out_dir / f"{T1_MODULE}.py"
    source = translate_file_with(load(translator), TRANSLATOR)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(source, encoding="utf-8")
    copy_library(out_dir)
    return out


def copy_library(out_dir: Path) -> None:
    """Put the files of ``LIBRARY`` in ``out_dir``, next to a translator."""
    for name in LIBRARY:
        shutil.copyfile(CDY_DIR / name, out_dir / name)


def build_t1(out_dir: Path = T1_DIR) -> Path:
    """T1: the Candy translator, translated by the checked-in one; returns its path."""
    return build_with(BIN_PATH, out_dir)


def translate_t1(path: Path) -> str:
    """The Candy file at ``path`` as Python source, translated by a freshly built T1."""
    return translate_file_with(load(build_t1()), path)


def translate_bin(path: Path) -> str:
    """The Candy file at ``path`` as Python source, translated by the checked-in translator."""
    return translate_file_with(load(BIN_PATH), path)


def build_bin(path: Path = BIN_PATH) -> Path:
    """Rebuild the checked-in translator as T2, T1's translation of the translator, once
    T2 has reproduced itself and passed ``mypy --strict``."""
    t2 = build_with(build_t1(), T2_DIR)
    if translate_file_with(load(t2), TRANSLATOR) != t2.read_text(encoding="utf-8"):
        raise FixpointError(f"{t2} doesn't translate the translator into itself")
    stdout, _, status = mypy_api.run(["--strict", "--no-incremental", str(t2)])
    if status != 0:
        raise FixpointError(f"{t2} fails mypy --strict:\n{stdout}")
    shutil.copyfile(t2, path)
    copy_library(path.parent)
    return path


if __name__ == "__main__":
    print(f"wrote {build_bin()}")
