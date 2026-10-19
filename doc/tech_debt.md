# Tech debt

Small shortcuts in the implementation (the Python translator, the runtime, tests and
tooling) that a Candy user can't see. They don't affect Candy's design, so they don't
belong in `doc/leaks.md`, but they are worth cleaning up some day. Add to the list when you
take one, and remove an entry once it is fixed.

## Translator

- **`retail` calls `self_call` twice** (once in the `case` guard, once in the body) and
  then `assert`s the result. It would be simpler without the guard (`lower_cdy.py`).
- **Raised pylint limits** (`max-returns` 15, `max-branches` 15, `max-locals` 20 in
  `pyproject.toml`) to fit the big `match` dispatches. Splitting those functions would let
  the defaults come back.

- **`match` is an `isinstance` chain in Python**, not Python's `match`, because mypy (2.4)
  loses a generic variant's type arguments in a class pattern (`case Node(l, v, r):` makes
  `v` `Any`). pyright handles class patterns; switch back if mypy catches up
  (`emit_match` in `emit_py.py`).
- **Every `match` subject gets a temporary** in `lower`, only because the Python chain
  tests the subject more than once. The temporary is typed `object` for a non-generic sum,
  to keep mypy fast (`doc/hl_rqmt/sum_types.md`), so mypy no longer checks that a chain is
  exhaustive or that its variants belong to the subject's sum (`analyse` checks both).

- **The Candy translator (T1) is simpler than the Python one in places**, to be closed
  slice by slice (see `doc/hl_rqmt/self_hosting_primo.md`): every operator is
  parenthesised; `if` in tail position stays an `if` statement (no conditional-expression
  merge); a nested scope's locals avoid every outer name, so T1 renames more than the
  Python translator; `format` is a `str()` concatenation, not an f-string. None of these
  change what a program does. (`and`/`or` whose later arguments needed statements used to
  run those statements regardless, which did; fixed on `self-host-cleanup`.)
- **Two readers:** `parse_cdy.py` (the frozen Python translator's) and `src/cdy/read.cdy`
  (the Candy translator's). Tests still check they agree; the first syntax change, which
  goes into `read.cdy` only, will have to drop or narrow those tests. The Candy reader
  builds strings and lists by appending one item at a time (quadratic, but fast enough: it
  reads the whole translator in about 0.02s).
- **A few errors have no position:** a brace inside a `format` hole, `main`'s type (its
  `Top` has no position), and the internal errors of `lower` and `emit`. Errors inside a
  `format` hole point at the `(format ...)` form, since forms read from a hole have no
  positions of their own (the hole's text is part of a string).
- **Only symbols and lists carry positions** (`Pos` in `form.cdy`), not literals: an error
  about a literal points at its enclosing list.
- **Programs only the Candy translator handles** go in `tst/cdy/cdyc/`, which the frozen
  Python translator skips; files they import live in subdirectories (`lib/`), so they
  aren't taken for programs.
- **A `cond` of about 200 clauses used as a value, with simple arms, doesn't compile:**
  it becomes nested conditional expressions (`a if t else (b if ...)`), and Python allows
  200 nested parentheses. The frozen Python translator fails there too (`ast.unparse`
  runs out of recursion). Written as statements (in a tail, or with arms that need
  statements) a `cond` of any length is fine: an `if`/`elif` chain.

## Runtime

- **`mangle` lives in the runtime** (`py_mangle`, with `PY_RESERVED`) so the self-hosted
  translator can use it; `emit_py.mangle` now calls it.
- **`slurp` is duplicated** in `src/py_cdy/reader.py` and `src/cdy_rt/table_defs.py`, on
  purpose for the iMVP (pylint's `duplicate-code` is disabled in `reader.py`).
- **`at` and `slice_` helpers are only used as values** now that `at` and `slice` are
  emitted as subscripts. They still return `object`/`Sequence`, so passing them as values
  loses the element type.

## Tests and tooling

- **Golden tests run mypy once per program** (`tst/py_cdy/test_cdy_programs.py`). That's
  fine with two programs, but one mypy run over all of them would be faster.
- **Repo naming.** The default branch is `master`, while some notes and tools assume
  `main`.
