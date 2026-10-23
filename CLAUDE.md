# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

"Candy" (`.cdy`) is an early-stage experimental language: statically typed, with an S-expression syntax, translated to Python by a translator written in Candy. `README.md` covers setup and use; `doc/process.md` covers how work is done (branches, commits and tags, design docs, where notes go). This machine's own setup (the Python environment, local checkouts) is in `CLAUDE.local.md`, which is not tracked.

The code:
- `src/cdy/` is the translator, in Candy: `cdyc.cdy` (its top file and driver) imports `form.cdy`, `read.cdy` (a hand-written reader), `include.cdy` (reads a program as modules), `expand.cdy` (macros), `core.cdy` (analysis into Core), `lower.cdy` (the lowered IR) and `emit.cdy` (Python source). It also reads a library at run time, kept next to it: `special.cdy`, `system.cdy`, `prelude.cdy`, `form.cdy` and `prelude_macros.cdy`. The special forms are declared in `special.cdy` and specified informally in `src/cdy/candy-special.md`.
- `bin/` holds the checked-in translators, one directory per target: `bin/py/cdy_translator.py` is the translator translated by itself (generated; don't edit), with copies of the library files next to it. Rebuild it with `python src/py_cdy/self_host.py` after changing `src/cdy/`, or `test_self_host.py` fails; see `bin/README.md`.
- `src/cdy_rt/` is the runtime: `table.py` (each built-in's Python spelling and rendering kind; special forms have none) and `table_defs.py` (the helpers generated code calls). It is the only package `pyproject.toml` packages.
- `src/py_cdy/` is the Python driver: `main.py` (translates a file to `output/<name>.py` with `bin`, or `--translator t1`; `--run` runs it) and `self_host.py` (builds T1 and T2, and rebuilds `bin`).
- `script/bootstrap.py` checks the bootstrap chain (`doc/hl_rqmt/bootstrap.md`).
- `editors/vscode-candy/` is a VS Code extension that highlights `.cdy` files (a TextMate grammar; install by symlinking, see its README; `tst/py_cdy/test_editor_grammar.py` checks it lists every special form).
- `tst/cdy/` holds Candy programs with their expected output (`NAME.cdy` + `NAME.out`), in `tst/cdy/t1/`, `tst/cdy/` and `tst/cdy/cdyc/`; files they import live in subdirectories (`lib/`). Python tests are in `tst/py_cdy/` and, for the runtime, `tst/cdy_rt/` (which import `cdy_rt.table` etc. through the editable install). `pyproject.toml` puts `src/py_cdy` and `script` on the import path for every tool (pytest, mypy, pyright, ruff, pylint), and holds tool config: line length 100 for ruff and pylint, `mypy --strict`, pylint exempts `test_*` functions from docstrings, and pytest deselects the `bootstrap` marker unless asked (`pytest -m bootstrap`).

Literals are `Int` `100`, `Long` `1500l`, `Float` `3.14f`, `Double` `10.0`, `Byte` `1b`, `Bool` `true`/`false`, `Char` `\e` and strings; they must end at a delimiter (whitespace, a paren, `;` or end of input). Quoting is the special forms `quo`, `quasi`, `unq` and `unq-sp`, for macros (`defmacro`; `doc/hl_rqmt/macros.md`). There is no `'` shorthand yet: `'` is reserved (a parse error) because the shorthand will come later as a Clojure-style reader macro.

## History and branches

Branch `py-py-translator` built the iMVP, a Candy → Python translator written in Python, and was merged into `master` (the default branch) and tagged `imvp-py-translator`. Branch `pre-self-host` wrote the translator in Candy and made it self-hosting on Python (tag `self-host-py`): there the Python translator builds the Candy translator, which then builds itself. Branch `self-host-cleanup` added `import` (as inclusion), a driver in Candy, error positions and tuple patterns, and froze the Python translator (tag `self-host-cleanup`; HLD `doc/hl_rqmt/self_host_cleanup.md`). Branch `macros` added `defmacro`, quoting, expansion, `import-macros` and `cond` as a macro (tag `macros`). Branch `modules` made `import` real modules (MVP: only `(import m)`, everything unqualified; tag `modules`; HLD `doc/hl_rqmt/modules.md`). Branch `system-prelude` declared the built-ins in `system.cdy` and added `prelude.cdy` (tag `system-prelude`; HLD `doc/hl_rqmt/system_prelude.md`).

Branch `bootstrap` added `script/bootstrap.py`, which checks the chain from the Python translator at `self-host-py` to today's `bin`, step by step, each step a `boot/NN` tag; it took the Python translator off `master` (it stays at tag `self-host-py`) and the arities out of `table.py` (tag `bootstrap`; HLD `doc/hl_rqmt/bootstrap.md`). Branch `symbol-table` declared what each built-in is (special form, operator, or typed function or value) in Candy (`special.cdy`, `system.cdy`), read into one map, and left `table.py` only the Python spellings (tag `symbol-table`; HLD `doc/hl_rqmt/symbol_table.md`). Each branch was merged into `master` and tagged with its name. Current work is on branch `library` (HLD `doc/hl_rqmt/library.md`): the translator's Python helpers in Candy, the list, string and map operations as built-ins, and the translator on the prelude's `rest`. The staging plan that got Candy self-hosting is `doc/hl_rqmt/self_hosting_primo.md`; the iMVP's requirements and decisions are in `doc/hl_rqmt/iMVP_py_translator.md` (keep it up to date as decisions are made).

## How the translator works

- **Modules** (`include.cdy`): `(import name)` at top level imports `name.cdy` from the importing file's directory; its top-level names become visible, unqualified. In Python they are prefixed with the module's file stem (`util__greet`), except in the top module, so tests reach the translator's own internals as `t1.form__Sym` or `t1.read__read_forms`. Macro files still use inclusion. Each module is analysed on its own, seeing what it imports (`core.cdy`), and all the modules' definitions are emitted as one Python file.
- **Macros** (`expand.cdy`): the translator compiles a program's `defmacro`s, and those of the macro files it loads with `import-macros`, runs them inside itself with the runtime's `load-macros`, and expands their calls. Every file gets `prelude_macros.cdy`'s macros (such as `cond`).
- **The built-ins** (`doc/hl_rqmt/symbol_table.md`): `special.cdy` declares the special forms (`(special if)`) and the operators (`(op + variadic)`, `(op not unary)`); `system.cdy` gives every other built-in its type, as a bodiless `sig` (like Carp's `register`, with no separate form), and a built-in's arity comes from its type. The translator reads both into one map (`Builtin` in `core.cdy`, by `library-builtins` in `expand.cdy`) and checks it against `table.py` both ways; `emit.cdy` reads `table.py`'s spellings as Candy data (`initial-table`, a map of pairs).
- **The library** (`doc/hl_rqmt/library.md`): a host type's operations are built-ins, all of them, since lists (tuples), strings and maps are the host's: `map`, `filter`, `fold`, `any`, `find`, `take`, `zip`, `split`, `map-from`, `with-default` and the rest (`system.cdy`). `prelude.cdy` is a module every file imports implicitly, for what is built on them: `rest` and `map-update` so far. Macro code doesn't get the prelude (a leak); it has `form.cdy`'s `rest-of`. The translator's helpers for writing Python (`py-mangle`, `py-str`, `indent`, `PY_IMPORTS`) are ordinary Candy in `emit.cdy`, with no Python behind them; the built-ins only the translator needs are the five host ones (`initial-table`, `load-macros`, `call-macro`, `module-dir`, `fresh-name`).
- **Self-hosting** (`self_host.py`): the checked-in `bin` builds T1 (`output/t1/cdy_translator.py`) from `src/cdy/cdyc.cdy`; `build_bin` has T1 build T2, checks T2 reproduces itself and passes `mypy --strict`, and replaces `bin` with it. `tst/py_cdy/test_self_host.py` runs every test program through T1 (output and `mypy --strict`) and checks the fixpoint: T2 passes `mypy --strict`, reproduces itself byte for byte, agrees with T1 on every program, and is `bin`.
- **Errors** use the `fail` built-in (raises `CandyFail`) and say `file:line:col: msg`: `Sym` and `Lst` forms carry a `Pos`.
- **`main`:** a program that defines `main`, typed `(Fn ((List String)) Int)`, runs it when its module is run (not imported), with the command-line arguments, exiting with its result (`run_main` in the runtime); `cdyc.cdy`'s `main` is the translator's driver.
- **Sum types** (`doc/hl_rqmt/sum_types.md`): `(deft Shape (Circle ((r Double))) (Rect ((w Double) (h Double))))`, taken apart with `(match s ((Circle r) ...) ((Rect w h) ...))` (exhaustive unless there is an `else`). In Python a variant is a `NamedTuple`, the sum a `type` alias of their union, and `match` an `isinstance` chain (mypy loses generic type arguments in class patterns) on a temporary typed `object` unless the sum is generic (narrowing a union of `NamedTuple`s makes mypy very slow).

## Decisions that fill gaps in the spec

The translator is an **MVP path to bootstrapping Candy**: favour the simplest thing that works over completeness or performance, and expect parts to be replaced (`cond` is now a macro, and `defn` may become one).

- `let` bindings are `(name init)`: `(let ((x 1) (y 2)) (+ x y))`. They are sequential, like Scheme's `let*`: each `init` sees the names bound before it. Semantically `let` is an applied lambda, as in Scheme: analysis desugars it into nested applied `fn`s (Core has no `Let` node) and `lower` turns those back into plain assignments. `lower` also turns a top-level `defn` that calls itself in tail position into a loop, unless it makes a closure.
- `cond`'s `(else expr)` clause is optional (it is a macro, expanding into nested `if`s). If no test matches, the result is `None`.
- Missing values are `None`. This covers an `if` with no else whose test is false, a `cond` with no match, and the value of a `def` form itself.
- `def` must have an initial value: `(def x init)`. `def` and `deft` are only allowed at top level.
- `defn` and `fn` need at least one argument (`(defn f () ...)` is an error), and their body is exactly one form (use `do` for several). A function with no real input takes a `Unit` argument, as in ML: `(defn run (_) ...)`, called as `(run nil)`.
- Operators and built-ins (`+`, `*`, `=`, …) are not hard-coded in the translator: `special.cdy` and `system.cdy` declare them, and `table.py` maps each to Python (`table.py` and `table_defs.py` started from smz's, see below).
- smz ("schmuz") is a rough, untyped prototype of this same approach, already self-hosting (where it is: `CLAUDE.local.md`). Its Python version (`src/py_smz/`: `table.py` op table, `render.py` → Python source text) compiled its Scheme-syntax version (`src/smz/*.scm`), which then compiled itself. Use it as a reference, not as a style guide: it is imperative and untyped.
- Candy is **strongly and statically typed**. Types are declared in a separate **signature statement**, `(sig name Type)` (from Carp's `register`/`sig`): **required** for every top-level `def`/`defn`, allowed anywhere at top level before its definition, with `Any` as the escape hatch. The type names are `String`, `Unit` (value `nil`), `(Maybe a)`, `(Fn (Int) Int)`, `(List a)`, `(Tup a b)`, `(Map k v)`, `Any`, and lowercase type variables (iMVP doc, "Signature statement"). `(List a)` is a Python `tuple[A, ...]`; it will be one kind of abstract `Collection` (an interface, later). Signatures become Python annotations, and mypy checks the generated code until Candy has its own type checker; a `fn` that becomes a nested Python `def` gets `Any` annotations.
- Candy literal types map to the simplest Python types: `Int`/`Long`/`Byte` → `int`, `Float`/`Double` → `float`, `Bool` → `bool`, `Char`/`String` → `str`. No `NewType`s: Python won't be the only target, so type distinctions belong to Candy's front end, not the Python backend. The layering is forms → Core (`core.cdy`) → the lowered IR (`lower.cdy`) → Python (`emit.cdy`); see "Layers" in the iMVP doc and `doc/hl_rqmt/multi_target.md` (future targets).
- Mutation (for example of `deft` records, which are immutable `NamedTuple`s) and optimizations are skipped for now; ideas go in `doc/hl_rqmt/mutation_optimization.md`.
- **Generated Python must depend only on the runtime** (`cdy_rt`: `table.py` and `table_defs.py`), never on the translator or the driver. Keep those two modules self-contained: they import only each other and the standard library. The runtime is installed editable in strict mode (see Running): strict mode links each file into `build/`, so edits show up immediately, but after **adding or removing a module** in `cdy_rt`, reinstall.
- `format` is hacked in, copying smz (an f-string with Candy forms in `{...}` holes). `tup` builds a Python tuple; its destructuring is a stopgap (only in `let`, rewritten into `at` calls). Every such shortcut, and every place Python semantics leak into Candy, is recorded in `doc/leaks.md`: add to it whenever a hack goes in. Earlier branches' leaks are archived in `doc/archive/leaks_*.md` and still apply until they are fixed (strike them through there). Shortcuts too small to matter to Candy's design go in `doc/tech_debt.md`; undecided design ideas in `doc/brainstorm.md`. In an HLD, an answer taken as the simplest for the MVP says *for now* and points at the leak, tech debt or follow-up entry that tracks it; one meant to stay says *lasting*. The whole process is in `doc/process.md`.

## Python style

From the parsec.py v4 design notes (`doc/hl_rqmt/deps/parsec-py-DESIGN-COPY.md`), which the Python translator's parser was written against; the conventions still set the style for this repo's Python:

- **No decorators anywhere.** That includes `@dataclass`, `@property` and `@overload`. Use `typing.NamedTuple` for immutable records.
- **Pure functional style.** Results are immutable tuples.
- **Statically typed**, checked with mypy (strict) and pyright.

parsec v4 itself is needed only by the bootstrap chain's first step (the Python translator, at tag `self-host-py`); nothing on `master` imports it.

## Running

```
pip install -e . --config-settings editable_mode=strict   # (re)install cdy_rt, editable
python src/py_cdy/main.py FILE.cdy --run   # translate to output/FILE.py with bin, then run it
python src/py_cdy/main.py FILE.cdy --translator t1   # ... with T1, freshly built by bin
python bin/py/cdy_translator.py FILE.cdy [OUT.py]     # the checked-in translator on its own (default output/FILE.py)
python src/py_cdy/self_host.py             # rebuild bin/py/cdy_translator.py
python script/bootstrap.py --from-scratch  # the bootstrap chain, Python translator to bin (--check, --step C)

mypy src/py_cdy src/cdy_rt tst script   # type-check (both checkers currently clean)
pyright src tst script
ruff check src tst script               # lint
ruff format src tst script              # format
pylint src/py_cdy src/cdy_rt tst script
pytest                              # all tests (testpaths = tst)
pytest tst/py_cdy/test_main.py::test_out_path   # run a single test
pytest -m bootstrap                 # the bootstrap chain (deselected by default)
```

Run everything in the project's Python environment (Python 3.14; on this machine, see `CLAUDE.local.md`). `.gitignore` excludes `output/` and `tmp/`, so put generated artifacts there. `bin/` is tracked.
