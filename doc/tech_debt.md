# Tech debt

Small shortcuts in the implementation (the translator, the runtime, tests and
tooling) that a Candy user can't see. They don't affect Candy's design, so they don't
belong in `doc/leaks.md`, but they are worth cleaning up some day. Add to the list when you
take one, and remove an entry once it is fixed.

## Translator

- **`(sig x (List))` crashes the translator** with Python's `IndexError` (in `emit-tcon`,
  `emit.cdy`), instead of failing with a Candy error: a type constructor's arguments
  aren't counted. Found writing the spec (`doc/hl_rqmt/executable_spec.md`, step 3).
- **`(def (x) 1)` says " needs a (sig  Type) before its definition"**, with no name: a
  `def` whose name isn't a name gets the missing-`sig` message. Found as above.
- **`match` is an `isinstance` chain in Python**, not Python's `match`, because mypy (2.4)
  loses a generic variant's type arguments in a class pattern (`case Node(l, v, r):` makes
  `v` `Any`). pyright handles class patterns; switch back if mypy catches up
  (`emit-match` in `emit.cdy`).
- **Every `match` subject gets a temporary** in `lower`, only because the Python chain
  tests the subject more than once. The temporary is typed `object` for a non-generic sum,
  to keep mypy fast (`doc/hl_rqmt/sum_types.md`), so mypy no longer checks that a chain is
  exhaustive or that its variants belong to the subject's sum (`analyse` checks both).

- **The Candy translator's output is plainer than the Python translator's was** (that
  translator is at tag `self-host-py`; `doc/hl_rqmt/self_hosting_primo.md`): every operator
  is parenthesised; `if` in tail position stays an `if` statement (no conditional-expression
  merge); a nested scope's locals avoid every outer name, so it renames more than it must;
  `format` is a `str()` concatenation, not an f-string. None of these change what a
  program does. (`and`/`or` whose later arguments needed statements used to
  run those statements regardless, which did; fixed on `self-host-cleanup`.)
- **The reader builds strings and lists by appending one item at a time** (`read.cdy`):
  quadratic, but fast enough (it reads the whole translator in about 0.02s).
- **A few errors have no position:** a brace inside a `format` hole, `main`'s type (its
  `Top` has no position), and the internal errors of `lower` and `emit`. Errors inside a
  `format` hole point at the `(format ...)` form, since forms read from a hole have no
  positions of their own (the hole's text is part of a string).
- **Only symbols and lists carry positions** (`Pos` in `form.cdy`), not literals: an error
  about a literal points at its enclosing list.
- **Three directories of test programs** (`tst/cdy/t1/`, `tst/cdy/`, `tst/cdy/cdyc/`) for
  what used to be three audiences: `cdyc/` held the programs only the Candy translator
  could handle, which the Python translator skipped. With that translator gone
  (`doc/hl_rqmt/bootstrap.md`) the split means nothing; they could be one directory. Files
  the programs import live in subdirectories (`lib/`), so they aren't taken for programs.
- **A `cond` of about 200 clauses used as a value, with simple arms, doesn't compile:**
  it becomes nested conditional expressions (`a if t else (b if ...)`), and Python allows
  200 nested parentheses. Written as statements (in a tail, or with arms that need
  statements) a `cond` of any length is fine: an `if`/`elif` chain.

- **`expand.cdy` knows the shape of some special forms** (`defn`, `fn`, `let`, `match`,
  `cond`, and the forms with no expressions), to leave binding positions unexpanded. It
  duplicates a little of `analyse`'s syntax, and gets malformed forms past to `analyse`
  only roughly. A deft's variant named like a macro is not rejected.
- **Every module compiles the prelude's macros** (with `form.cdy`), and again for each
  macro file it loads: each module is expanded on its own, with nothing shared.
- **A macro file is compiled once per file that imports it** (and its helpers again in
  each importer's macro program), with no cache across a translation.
- **`form.cdy` is copied next to every translator** (`bin/py/form.cdy`,
  `self_host.copy_library`) for macros to compile with; a translator copied elsewhere on
  its own can't expand macros (it says so).

- **Module prefixes can collide with mangled names:** `util__greet` (module `util`'s
  `greet`) is also what `py-mangle` makes of a top module's `util--greet`. Nothing checks.
- **A type from a module the file doesn't import isn't caught** by the translator: a `sig`
  naming it keeps the bare name, and `mypy` (or Python) reports it in the output.
- **Translator internals are reached by prefixed names in Python** (`t1.form__Sym`,
  `t1.read__read_forms`; `self_host.to_form`, `test_self_host.py`), so moving a function
  to another file changes its Python name.

- **`special.cdy` and `system.cdy` are read for every translation, and again for every
  macro program** (`library-builtins` in `expand.cdy`), and checked against the table each
  time. Nothing caches them.
- **The built-ins' types are read but not used** beyond arity: there is no type checker,
  and mypy still gets the runtime's types from `primitives.py`'s annotations.

- **The whole prelude goes into every program's Python file**, used or not, and it is
  read and expanded again for every translation.
- **Building a list is quadratic:** `(+ acc (to-list x))` copies the whole tuple. `map`,
  `filter` and `fold` are built-ins to avoid it, but the translator's own accumulator
  loops (about 94 `defn`s) still pay it. Long-term fix: in `mutation_optimization.md`.

## Runtime

- **`load-macros` finds the translator's `form.cdy` names from `home`'s Python name:**
  `form__sym_name` gives the prefix `form__` (none for a translator built before
  modules, which the bootstrap needed).

- **`slurp` falls back to searching `src/`, `tst/` and `lib/` by file stem** (from smz's
  `get_path`), relative to the current directory. That can hide a wrong path: it found
  `form.cdy` for a translator that had none next to it, until `expand.cdy` checked with
  `file-exists` first.

- **`mangle` lives in the runtime** (`py_mangle`, with `PY_RESERVED`) so the self-hosted
  translator could use it (the library HLD moves it into `emit.cdy`, as Candy).
- **`at` and `slice_` helpers are only used as values** now that `at` and `slice` are
  emitted as subscripts. They still return `object`/`Sequence`, so passing them as values
  loses the element type.

## Tests and tooling

- **parsec.py v4 isn't published:** the bootstrap chain's first step (the Python
  translator, at tag `self-host-py`) needs it, but it exists only as a local copy on the
  owner's machine; upstream sighingnow/parsec.py has only `master`. So the chain can't run
  from scratch anywhere else yet. Fix: publish it (and record where), or vendor a copy
  (MIT) that the script puts on the path for that step.

- **Test programs run mypy once each** (`test_mypy_strict` in `tst/py_cdy/test_self_host.py`).
  One mypy run over all of them would be faster.
- **Repo naming.** The default branch is `master`, while some notes and tools assume
  `main`.
- **`py-str` is close to `repr`, not equal** (`emit.cdy`, `doc/hl_rqmt/library.md` step
  1a): it escapes control characters (below 32, and 127 to 160) but leaves other
  characters Python's `repr` would escape (such as U+00AD or U+2028) as they are, since
  Candy can't ask whether a character is printable. The output is still valid Python.
- **The test programs' `mypy --strict` runs one program at a time**
  (`test_mypy_strict` in `tst/py_cdy/test_self_host.py`): about 8.7 s for 17 programs.
  One batched run, as `tst/py_cdy/test_spec.py` does per spec file, measured 0.4 s for 40
  small files (`doc/hl_rqmt/executable_spec.md`, step 1); a failure then names the run,
  not the program.
- **`PY_RESERVED` is Python 3.14's** keywords and built-ins, written out in `emit.cdy`;
  `test_py_reserved_is_this_python` fails when another Python adds one.
