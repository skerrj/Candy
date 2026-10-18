"""Command-line entry point: ``python src/py_cdy/main.py FILE.cdy [--run]``.

Modelled on schmuz's ``src/py_smz/main.py``: like its ``run_2_out``, it translates a Candy
file to ``output/<name>.py``; with ``--run`` it then runs that file, like ``run_as_main``.
"""

import subprocess
import sys
from pathlib import Path

from parsec import ParseFailure

from core_cdy import CandyError
from reader import slurp
from translate_cdy import translate

OUTPUT_DIR = Path("output")
USAGE = "usage: main.py FILE.cdy [--run]"


def out_path(name: str) -> Path:
    """Where the translated Python for ``name`` goes: ``output/<stem>.py``."""
    return OUTPUT_DIR / f"{Path(name).stem}.py"


def translate_file(name: str) -> Path:
    """Translate the Candy file ``name`` and write the Python; returns where it went."""
    out = out_path(name)
    source = translate(slurp(name))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(source, encoding="utf-8")
    return out


def main(args: list[str]) -> int:
    """Translate the file named in ``args`` and, with ``--run``, run the result."""
    files = [a for a in args if a != "--run"]
    if len(files) != 1 or len(args) - len(files) > 1:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        out = translate_file(files[0])
    except (FileNotFoundError, ParseFailure, CandyError) as err:
        print(f"candy: {err}", file=sys.stderr)
        return 1
    print(f"candy: {files[0]} -> {out}", file=sys.stderr)
    if "--run" in args:
        return subprocess.run([sys.executable, str(out)], check=False).returncode
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
