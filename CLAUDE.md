# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

"Candy" (`.cdy`) is an early-stage experimental language. Right now the only code is a Python reader, `src/py_cdy/parse_cdy.py`, which parses an S-expression surface syntax into typed AST nodes (`Symbol`, `Number`, `Str`, `Bool`, `SList`; `'x` desugars to `(quote x)`). `README.md` is empty. These directories are empty placeholders: `bin/py/` (now git-ignored), `script/`, `tst/cdy/` (presumably for Candy-language tests). Python tests for `src/py_cdy` live in `tst/py_cdy/`; `pyproject.toml` puts `src/py_cdy` on the import path for pytest, ruff and pyright, so tests do `from parse_cdy import ...`. `pyproject.toml` holds only tool config: line length 100 for ruff and pylint, `mypy --strict`, and pylint exempts `test_*` functions from docstrings. There is no packaging setup.

## Candy → Python translator (branch `py-py-translator`)

The special forms are specified informally in `src/cdy/candy-special.md`. The full iMVP requirements, decisions, open questions and next steps are in `doc/hl_rqmt/iMVP_py_translator.md`; keep it up to date as decisions are made. The first translator, written in Python, turns Candy into Python. It is an **MVP path to bootstrapping Candy**: its job is to get the language running so it can later implement itself. Favour the simplest thing that works over completeness or performance, and expect parts to be replaced. For example, the spec says `defn` and `cond` will become macros.

Decisions that fill gaps in the spec:
- `let` bindings are `(name init)`: `(let ((x 1) (y 2)) (+ x y))`.
- `cond`'s `(else expr)` clause is optional. If no test matches, the result is `None`.
- Missing values are `None`. This covers `(def x)`, an `if` with no else whose test is false, and the value of a `def` form itself.
- `def` needs at least a symbol: `(def x)` is valid, but `(def)` and a bare `def` are errors.
- Operators and builtins (`+`, `*`, `=`, …) are not hard-coded in the translator. They come from `table.py` and `table_defs.py` (to be provided; `table.py` is modelled on `~/dev/smz/smz-core/src/py_smz/table.py` and `table_defs.py` starts from `~/dev/smz/smz-core/src/py_smz/smztils.py`), which map Candy symbols to Python operators and helper definitions and set up the initial symbol table. A Candy prelude may take this over later.
- `~/dev/smz/smz-core` ("schmuz") is a rough, untyped prototype of this same approach, and it is already self-hosting. Its Python version (`src/py_smz/`: `table.py` op table, `render.py` → Python source text) compiled the Scheme-syntax version (`src/smz/*.scm`), which then compiled itself. Use it as a reference, not as a style guide: it is imperative and untyped. Candy will be strongly typed.
- Candy is a **strongly and statically typed** language. Types are declared in a separate **signature statement**, not inline in `def`/`defn`/`fn`, so the special-form syntax above stays as it is. Its syntax is still to be specified. Possible iMVP approach: translate signatures into Python annotations and let mypy/pyright check the generated code until Candy has its own type checker.
- For the initial MVP (iMVP), `reader.py` just slurps a whole Candy file into a string, which then goes to the parser.

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
- **Lexing:** the lexeme convention is `p << ignore`, where `ignore` skips whitespace and `;` comments (see `lexeme` in `parse_cdy.py`). `;` also ends a number or symbol token.

## Running

```
source ~/dev/activate-conda && conda activate py_cdy   # conda is not on PATH by default
python src/py_cdy/parse_cdy.py         # parses a sample program and prints the AST

mypy src/py_cdy tst/py_cdy          # type-check (both checkers currently clean)
pyright src/py_cdy tst/py_cdy
ruff check src tst                  # lint
ruff format src tst                 # format
pylint src/py_cdy tst/py_cdy
pytest                              # all tests (testpaths = tst)
pytest tst/py_cdy/test_parse_cdy.py::test_atoms   # run a single test
```

`.gitignore` excludes `output/`, `tmp/` and `bin/`, so put generated artifacts there.
