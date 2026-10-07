# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

"Candy" (`.cdy`) is an early-stage experimental language. Right now the only code is a Python reader, `src/py_cdy/parse_cdy.py`, which parses an S-expression surface syntax into typed AST nodes (`Symbol`, `Number`, `Bool`, `SList`; `'x` desugars to `(quote x)`). `README.md` is empty. These directories exist but are empty placeholders (git does not track them): `bin/py/`, `script/`, `tst/cdy/` (presumably for Candy-language tests) and `tst/py_cdy/` (presumably for Python tests of `src/py_cdy`). There is no `pyproject.toml` or other build/tool config yet.

## Dependency: parsec.py v4 (not the PyPI release)

`parse_cdy.py` imports `parsec`, but that means the **v4 functional rewrite** of sighingnow/parsec.py (branch `functional-rewrite`), not PyPI `parsec` 3.x. The PyPI release lacks `fix`, the camelCase combinators and the typed `Parser[T]`. The rewrite is installed in the **`py_cdy` conda environment** (Python 3.14). `import parsec` loads directly from the local checkout at `~/dev/exp/parsec.py/src`, so edits to the library show up here immediately. It is not in the system Python, so run everything inside that environment.

`doc/hl_rqmt/deps/parsec-py-DESIGN-COPY.md` is a copy of that library's design notes. Read it before writing parser code. Its conventions also set the style for this repo:

- **No decorators anywhere.** That includes `@dataclass`, `@property` and `@overload`. Use `typing.NamedTuple` for immutable records.
- **Pure functional style.** Repetition results are immutable tuples.
- **Statically typed grammar rules** (`Parser[T]` that yields typed AST nodes, checked with mypy/pyright). Python 3.10+.
- **Recursive rules** use `fix(lambda self: ...)` or `lazy(lambda: ...)`, as `form = fix(form_from)` does here.
- **Choice is Parsec-style:** `p | q` tries `q` only if `p` failed without consuming input. Use `try_(p)` to backtrack. `string` and `regex` are atomic.
- **Operators and names:** `>>` is `*>`, `<<` is `<*`, and the methods are `.map`, `.bind` and `.label`. Combinators use Haskell camelCase names (`sepBy`, `many1`, `chainl1`).
- **Running parsers:** `parse(p, text)` requires the whole input to be consumed and raises `ParseFailure`. `runParser` returns `Success`/`Failure` without raising.
- **Lexing:** the lexeme convention is `p << spaces` (see `lexeme` in `parse_cdy.py`).

## Running

```
source ~/dev/activate-conda && conda activate py_cdy   # conda is not on PATH by default
python src/py_cdy/parse_cdy.py         # parses a sample program and prints the AST

mypy src/py_cdy                     # type-check (both checkers currently clean)
pyright src/py_cdy
pytest tst                          # no tests exist yet
pytest tst/py_cdy/test_x.py::test_name   # run a single test
```

`.gitignore` excludes `output/` and `tmp/`, so put generated artifacts there.
