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

## Runtime

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
- **`.vscode/` is untracked** and not in `.gitignore`.
