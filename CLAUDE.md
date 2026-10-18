# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

"Candy" (`.cdy`) is an early-stage experimental language. Right now the code is the runtime package `src/cdy_rt/` (see below), a file reader `src/py_cdy/reader.py`, an entry point `src/py_cdy/main.py` (translates a file to `output/<name>.py`; `--run` runs it), the three translator steps, `src/py_cdy/core_cdy.py` (Core AST and `analyse`), `src/py_cdy/lower_cdy.py` (the lowered IR and `lower`) and `src/py_cdy/emit_py.py` (Python `ast` and source text), chained by `src/py_cdy/translate_cdy.py` (`translate`: Candy text to Python text), and the parser `src/py_cdy/parse_cdy.py`, which parses an S-expression surface syntax into typed AST nodes: `Symbol`, `SList`, `Str`, and one node per literal type (`Int` `100`, `Long` `1500l`, `Float` `3.14f`, `Double` `10.0`, `Byte` `1b`, `Bool` `true`/`false`, `Char` `\e`). Literals must end at a delimiter (whitespace, a paren, `;` or end of input). Quoting is the special form `(quote x)`, but `quote` is **skipped for the iMVP** (no macros), so the translator rejects it, like `import`. There is no `'` shorthand yet: `'` is reserved (a parse error) because the shorthand will come later as a Clojure-style reader macro. `README.md` is empty. These directories are empty placeholders: `bin/py/` (now git-ignored), `script/`. `tst/cdy/` holds Candy programs with their expected output (`NAME.cdy` + `NAME.out`), run as golden tests by `tst/py_cdy/test_cdy_programs.py`, which also checks the generated Python with `mypy --strict`. Python tests for `src/py_cdy` live in `tst/py_cdy/`, and for `src/cdy_rt` in `tst/cdy_rt/` (which import `cdy_rt.table` etc. through the editable install); `pyproject.toml` puts `src/py_cdy` on the import path for every tool (pytest, mypy, pyright, ruff, pylint), so tests do `from parse_cdy import ...`. `pyproject.toml` holds tool config: line length 100 for ruff and pylint, `mypy --strict`, and pylint exempts `test_*` functions from docstrings. Its only packaging config is for the runtime package `cdy_rt` (see the translator section).

## Candy → Python translator (branch `py-py-translator`)

The special forms are specified informally in `src/cdy/candy-special.md`. The full iMVP requirements, decisions, open questions and next steps are in `doc/hl_rqmt/iMVP_py_translator.md`; keep it up to date as decisions are made. The first translator, written in Python, turns Candy into Python. It is an **MVP path to bootstrapping Candy**: its job is to get the language running so it can later implement itself. Favour the simplest thing that works over completeness or performance, and expect parts to be replaced. For example, the spec says `defn` and `cond` will become macros.

Decisions that fill gaps in the spec:
- `let` bindings are `(name init)`: `(let ((x 1) (y 2)) (+ x y))`. They are sequential, like Scheme's `let*`: each `init` sees the names bound before it. Semantically `let` is an applied lambda, as in Scheme: `analyse` desugars it into nested applied `fn`s (Core has no `Let` node) and `lower` turns those back into plain assignments. `lower` also turns a top-level `defn` that calls itself in tail position into a loop (`loop_tail_calls`), unless it makes a closure.
- `cond`'s `(else expr)` clause is optional. If no test matches, the result is `None`.
- Missing values are `None`. This covers an `if` with no else whose test is false, a `cond` with no match, and the value of a `def` form itself.
- `def` must have an initial value: `(def x init)`. `(def x)`, `(def)` and a bare `def` are errors. `def` and `deft` are only allowed at top level; inside a function they are errors (proposed: `analyse` is split into `analyse_top` and `analyse_expr`, and only the former accepts definitions).
- `defn` and `fn` need at least one argument (`(defn f () ...)` is an error), and their body is exactly one form: a literal or an expression (use `do` for several). A function with no real input takes a `Unit` argument, as in ML (decided): `(defn run (_) ...)`, called as `(run nil)`.
- Operators and builtins (`+`, `*`, `=`, …) are not hard-coded in the translator. They come from `src/cdy_rt/table.py` and `src/cdy_rt/table_defs.py` (drafted from smz and accepted by the owner for now; `table.py` is modelled on `~/dev/smz/smz-core/src/py_smz/table.py` and `table_defs.py` starts from `~/dev/smz/smz-core/src/py_smz/smztils.py`), which map Candy symbols to Python operators and helper definitions and set up the initial symbol table. Later, `system.cdy` and `prelude.cdy` take this over: in `system.cdy` and every file it imports, a `sig` with no definition declares a runtime built-in, like Carp's `register` (no separate `register` form); `prelude.cdy` holds ordinary Candy definitions. Not in the iMVP.
- `~/dev/smz/smz-core` ("schmuz") is a rough, untyped prototype of this same approach, and it is already self-hosting. Its Python version (`src/py_smz/`: `table.py` op table, `render.py` → Python source text) compiled the Scheme-syntax version (`src/smz/*.scm`), which then compiled itself. Use it as a reference, not as a style guide: it is imperative and untyped. Candy will be strongly typed.
- Candy is a **strongly and statically typed** language. Types are declared in a separate **signature statement**, not inline in `def`/`defn`/`fn`, so the special-form syntax above stays as it is. It is `(sig name Type)`, from Carp's `register`/`sig`: **required** for every top-level `def`/`defn`, allowed anywhere at top level before its definition, with `Any` as the escape hatch (`(sig f (Fn (Any Any) Any))`). The type names are decided: `String`, `Unit` (value `nil`), `(Maybe a)`, `(Fn (Int) Int)`, `(List a)`, `(Tup a b)`, `(Map k v)`, `Any`, lowercase type variables; see "Signature statement" in the iMVP doc. `(List a)` is a Python `tuple[A, ...]`; at the Candy level it will be one kind of abstract `Collection` (an interface, after the iMVP). A `fn` that becomes a nested Python `def` gets `Any` annotations. Possible iMVP approach: translate signatures into Python annotations and let mypy/pyright check the generated code until Candy has its own type checker.
- Candy literal types map to the simplest Python types for now: `Int`/`Long`/`Byte` → `int`, `Float`/`Double` → `float`, `Bool` → `bool`, `Char`/`String` → `str`. No `NewType`s: Python won't be the only target, so type distinctions belong to Candy's front end and type checker, not the Python backend. Keep a target-independent stage (parser → typed AST) separate from the Python lowering. Translation strategy A is decided (build Python's `ast`). The layering is `SExpr` → Core AST (`analyse`, in `core_cdy.py`) → lowered IR, a "pseudo-AST" (`lower`) → Python `ast` (`emit_py`); the IR is its own layer (decided). See "Layers" in the iMVP doc. See `doc/hl_rqmt/multi_target.md` (a placeholder HLD for future targets).
- Mutation (for example of `deft` records, which are immutable `NamedTuple`s) and optimizations are skipped for the iMVP; ideas go in `doc/hl_rqmt/mutation_optimization.md` (a placeholder HLD).
- **Generated Python must depend only on `table.py` and `table_defs.py`** (the runtime, which started as smz's `smztils.py`), never on the rest of `py_cdy` (parser, translator). Keep those two modules self-contained: they import only each other and the standard library. They live in their own package, `src/cdy_rt/`, which is the only thing `pyproject.toml` packages. It is installed editable in strict mode (see Running), so only `cdy_rt`, not `py_cdy`, becomes importable outside the repo. Strict mode links each file into `build/`: edits show up immediately, but after **adding or removing a module** in `cdy_rt`, reinstall.
- `format` is hacked in, copying smz (an f-string with Candy forms in `{...}` holes). `tup` builds a Python tuple, as in smz; only its destructuring is a stopgap (only in `let`, rewritten into `at` calls). Every such shortcut, and every place Python semantics leak into Candy, is recorded in `doc/leaks.md`: add to it whenever a hack goes in.
- For the initial MVP (iMVP), `reader.py` just slurps a whole Candy file into a string, which then goes to the parser. Its `slurp` is copied from `cdy_rt.table_defs` on purpose (pylint's `duplicate-code` is disabled there).
- Error positions are skipped for the iMVP: only parse errors have a line and column.

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
pip install -e . --config-settings editable_mode=strict   # (re)install cdy_rt, editable
python src/py_cdy/main.py FILE.cdy --run   # translate to output/FILE.py, then run it
python src/py_cdy/parse_cdy.py         # parses a sample program and prints the AST

mypy src/py_cdy src/cdy_rt tst      # type-check (both checkers currently clean)
pyright src tst
ruff check src tst                  # lint
ruff format src tst                 # format
pylint src/py_cdy src/cdy_rt tst
pytest                              # all tests (testpaths = tst)
pytest tst/py_cdy/test_parse_cdy.py::test_atoms   # run a single test
```

`.gitignore` excludes `output/`, `tmp/` and `bin/`, so put generated artifacts there.
