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
- **`match` subjects that aren't simple get a temporary** in `lower`, only because the
  Python chain tests the subject more than once.

- **The Candy translator (T1) is simpler than the Python one in places**, to be closed
  slice by slice (see `doc/hl_rqmt/self_hosting_primo.md`): every operator is
  parenthesised; `if` in tail position stays an `if` statement (no conditional-expression
  merge); a local is renamed only when a top-level name took its spelling; `and`/`or`
  whose later arguments need statements don't short-circuit those statements; built-in
  arity isn't checked.
- **`self_host.py` raises the recursion limit** (to 20,000) while T1 runs, since T1 walks
  lists by recursion.

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
