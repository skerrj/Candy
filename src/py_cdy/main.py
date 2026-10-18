"""Command-line entry point: ``python src/py_cdy/main.py FILE.cdy``.

Modelled on schmuz's ``src/py_smz/main.py`` (``run_2_out``). For now it runs the stages that
exist, reader then parser, and prints the parsed forms. Once the translator exists, this is
where the forms get translated and written to ``output/<name>.py``.
"""

import sys
from pathlib import Path

from parsec import ParseFailure, parse

from parse_cdy import SExpr, program
from reader import slurp

OUTPUT_DIR = Path("output")


def read_forms(name: str) -> tuple[SExpr, ...]:
    """The top-level forms of the Candy file ``name``."""
    return parse(program, slurp(name))


def out_path(name: str) -> Path:
    """Where the translated Python for ``name`` will go: ``output/<stem>.py``."""
    return OUTPUT_DIR / f"{Path(name).stem}.py"


def main(args: list[str]) -> int:
    """Read and parse the file named by ``args[0]``, and print its forms."""
    if len(args) != 1:
        print("usage: main.py FILE.cdy", file=sys.stderr)
        return 2
    name = args[0]
    print(f"candy: {name} -> {out_path(name)} (translator not written yet)")
    try:
        forms = read_forms(name)
    except (FileNotFoundError, ParseFailure) as err:
        print(f"candy: {err}", file=sys.stderr)
        return 1
    for form in forms:
        print(form)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
