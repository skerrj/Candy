# Leaks (pre-self-host, archived)

**Archived** at tag `self-host-py`. These entries still apply until they are fixed; when one is fixed, strike it through here and say where. New leaks go in `doc/leaks.md`. The iMVP's list is `doc/archive/leaks_imvp_py_translator.md`.

Places where Candy's implementation lets Python show through, or takes a shortcut that
Candy's design will need to fix later, added on branch `pre-self-host`. Each one is
acceptable for bootstrapping. Each entry says what leaks, and what a proper fix might be.

## Hacked-in forms

- ~~**The self-hosted translator is several files joined into one** (`TRANSLATOR_FILES` in
  `src/py_cdy/self_host.py`), because Candy has no `import` yet. Top-level names can be
  used before their definition, so the order only matters for reading. Fix: `import`.~~
  Fixed on `self-host-cleanup`: `src/cdy/cdyc.cdy` imports the other files (`import` as
  inclusion, which has its own leak in `doc/leaks.md`).
- **`fail` stands in for errors.** Candy has no exceptions; `(fail "msg")` raises
  `CandyFail` from the runtime, and its result is typed as anything (`NoReturn`).

## Types

- **Sum types are Python unions of `NamedTuple`s.** Two variants of different sums with
  the same fields compare equal (`==` is tuple equality), as records already do (see the
  archived list). A variant is also a tuple, so Python's tuple operations work on it.
- **`get` after `match` is checked by mypy, not Candy.** `(get s r)` on a `Shape` that
  might be a `Rect` translates; mypy rejects it in strict mode, but Candy itself doesn't.

## Python semantics showing through

- **The symbol table is an opaque `Any`** in the self-hosted translator, read only through
  the `table-*` built-ins. Candy has no type for it, nor for `TableEntry`.
- **Python-specific helpers in the runtime** (`py-mangle`, `py-repr`) are the Candy
  translator's Python backend; `py-repr` writes Python literals with Python's `repr`.

## Translator shortcuts

- **Types and values share one namespace.** A sum type's name and its variants are all
  Python names, so a variant can't have its type's name (`(deft Box (Box ...))` is
  "defined more than once"), and no other top-level name can reuse a sum type's name.
  Candy keeps types and values apart in principle.
