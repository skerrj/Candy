"""Command-line entry point: ``python src/py_cdy/main.py FILE.cdy [--run] [--translator t1]``.

Modelled on schmuz's ``src/py_smz/main.py``: like its ``run_2_out``, it translates a Candy
file to ``output/<name>.py``; with ``--run`` it then runs that file, like ``run_as_main``.
With ``--translator t1`` the self-hosted translator (``self_host.py``) does the translating
instead of the Python one.
"""

import subprocess
import sys
from pathlib import Path

from parsec import ParseFailure

from cdy_rt.table_defs import CandyFail
from core_cdy import CandyError
from reader import slurp
from self_host import translate_t1
from translate_cdy import translate

OUTPUT_DIR = Path("output")
USAGE = "usage: main.py FILE.cdy [--run] [--translator py|t1]"
TRANSLATORS = {"py": translate, "t1": translate_t1}


def out_path(name: str) -> Path:
    """Where the translated Python for ``name`` goes: ``output/<stem>.py``."""
    return OUTPUT_DIR / f"{Path(name).stem}.py"


def translate_file(name: str, translator: str = "py") -> Path:
    """Translate the Candy file ``name`` and write the Python; returns where it went."""
    out = out_path(name)
    source = TRANSLATORS[translator](slurp(name))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(source, encoding="utf-8")
    return out


def main(args: list[str]) -> int:
    """Translate the file named in ``args`` and, with ``--run``, run the result."""
    rest = list(args)
    translator = "py"
    if "--translator" in rest:
        at = rest.index("--translator")
        translator = rest[at + 1] if at + 1 < len(rest) else ""
        del rest[at : at + 2]
    files = [a for a in rest if a != "--run"]
    if len(files) != 1 or len(rest) - len(files) > 1 or translator not in TRANSLATORS:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        out = translate_file(files[0], translator)
    except (FileNotFoundError, ParseFailure, CandyError, CandyFail) as err:
        print(f"candy: {err}", file=sys.stderr)
        return 1
    print(f"candy: {files[0]} -> {out}", file=sys.stderr)
    if "--run" in rest:
        return subprocess.run([sys.executable, str(out)], check=False).returncode
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
