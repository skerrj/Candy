"""Command-line entry point: ``python src/py_cdy/main.py FILE.cdy [--run] [--translator T]``.

Modelled on schmuz's ``src/py_smz/main.py``: like its ``run_2_out``, it translates a Candy
file to ``output/<name>.py``; with ``--run`` it then runs that file, like ``run_as_main``.
The checked-in translator ``bin/py/cdy_translator.py`` does the translating; with
``--translator t1``, the Candy translator freshly built by it does (``self_host.py``).
Either includes the file's imports. (The Python translator, frozen at tag ``self-host-py``,
is no longer here: ``doc/hl_rqmt/bootstrap.md``.)
"""

import subprocess
import sys
from pathlib import Path

from cdy_rt.primitives import CandyFail
from self_host import translate_bin, translate_t1

OUTPUT_DIR = Path("output")
USAGE = "usage: main.py FILE.cdy [--run] [--translator bin|t1]"

TRANSLATORS = {"bin": translate_bin, "t1": translate_t1}


def out_path(name: str) -> Path:
    """Where the translated Python for ``name`` goes: ``output/<stem>.py``."""
    return OUTPUT_DIR / f"{Path(name).stem}.py"


def translate_file(name: str, translator: str = "bin") -> Path:
    """Translate the Candy file ``name`` and write the Python; returns where it went."""
    out = out_path(name)
    source = TRANSLATORS[translator](Path(name))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(source, encoding="utf-8")
    return out


def main(args: list[str]) -> int:
    """Translate the file named in ``args`` and, with ``--run``, run the result."""
    rest = list(args)
    translator = "bin"
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
    except (FileNotFoundError, CandyFail) as err:
        print(f"candy: {err}", file=sys.stderr)
        return 1
    print(f"candy: {files[0]} -> {out}", file=sys.stderr)
    if "--run" in rest:
        return subprocess.run([sys.executable, str(out)], check=False).returncode
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
