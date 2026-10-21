# Leaks

Places where Candy's implementation lets Python show through, or takes a shortcut that
Candy's design will need to fix later. Each one is acceptable for bootstrapping. Each entry
says what leaks, and what a proper fix might be. Add to this list whenever a hack goes in.
Shortcuts that are too small to matter to Candy's design go in `doc/tech_debt.md` instead.

**Earlier leaks still apply.** They are archived by branch:

- `doc/archive/leaks_imvp_py_translator.md`: the iMVP Python translator (up to tag
  `imvp-py-translator`);
- `doc/archive/leaks_pre_self_host.md`: self-hosting (up to tag `self-host-py`);
- `doc/archive/leaks_self_host_cleanup.md`: `import` and the cleanup (up to tag
  `self-host-cleanup`);
- `doc/archive/leaks_macros.md`: macros (up to tag `macros`);
- `doc/archive/leaks_modules.md`: modules (up to tag `modules`).

Those entries stay in effect until they are fixed. When one is fixed, mark it there (strike
it through and say where it was fixed) rather than copying it here. This file is for leaks
added from branch `system-prelude` on.

- **Built-ins typed `Any`** (`src/cdy/system.cdy`), where Candy can't write the type yet:
  - `print`, `display` and `put` take any number of arguments, which a `Fn` type can't
    say, so they are `Any` and get no arity check;
  - `len`, `at`, `slice` and `in` work on lists, tuples and strings (and `len` on maps):
    their collection parameter is `Any` until Candy has `Collection` (iMVP doc);
  - the regular expressions return Python's match and pattern objects, the symbol table
    is a Python `Mapping`, and macros are Python functions: `Any`, until they get opaque
    Candy types.

  Fix: variadic types, interfaces, and opaque types.
- **Operators have no Candy type:** `+`, `=`, `and`, `not` and the rest are left out of
  `system.cdy`, so only the table describes them (two or more arguments; `not` one). Fix: a
  way to type a function that takes two or more arguments.
- **Special forms are described by the Python table:** `def`, `if`, `match` and the rest
  are entries in `table.py`, which the Candy translator asks whether a name is special
  (`table-is-special`). What the language's own forms are is a front-end fact, the same
  for every target. Fix: a target-neutral table in Candy (`doc/hl_rqmt/multi_target.md`,
  "The symbol table across targets"), or the translator's own list of special forms.
- **The translator's built-ins are every program's built-ins.** `system.cdy` (like
  `table.py` before it) is one flat set. Besides what programs need (`len`, `put`,
  `slurp`, ...), it has what only the translator uses:
  - the symbol table: `initial-table`, `table-is-special`, `table-get-kind` and the rest;
  - writing Python: `py-mangle`, `py-repr`, `get-indent`, `PY_IMPORTS`;
  - macros: `load-macros`, `call-macro`, `module-dir`, `fresh-name`.

  Every program can call them, and a Python backend's helpers appear as Candy built-ins,
  so a second target would have to provide them too. (A program's own definition of one
  of those names wins, so they don't get in its way.) Fix (decided, `doc/hl_rqmt/library.md`,
  "The translator's built-ins become Candy"): drop the unused ones, and rewrite the table
  lookups and the Python-writing helpers as Candy in the translator's own modules. That
  leaves five host built-ins (`initial-table` and the macro four) in `system.cdy`, until a
  declaration file can be imported by the translator alone.
