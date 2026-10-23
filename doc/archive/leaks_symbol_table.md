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
- `doc/archive/leaks_modules.md`: modules (up to tag `modules`);
- `doc/archive/leaks_system_prelude.md`: `system.cdy` and the prelude (up to tag
  `system-prelude`);
- `doc/archive/leaks_bootstrap.md`: the bootstrap chain (up to tag `bootstrap`; none).

Those entries stay in effect until they are fixed. When one is fixed, mark it there (strike
it through and say where it was fixed) rather than copying it here. This file is for leaks
added from branch `symbol-table` on.

- **Some of `special.cdy`'s entries are there for want of a type** (`src/cdy/special.cdy`,
  `doc/hl_rqmt/symbol_table.md`). Its file and its special forms are *lasting*, but:
  - **arithmetic and comparison** (`+`, `-`, `*`, `/`, `quot`, `=`, `!=`, `<`, `>`, `<=`,
    `>=`) are ordinary functions, declared as `(op name variadic)` only because a `Fn`
    type can't say "two or more arguments" (the leak "Operators have no Candy type",
    `doc/archive/leaks_system_prelude.md`); *for now*: once Candy has variadic types they
    move to `system.cdy`, with `sig`s. `not` is a one-argument function, typable today;
  - **`and` and `or`** short-circuit, so they can't be plain functions, but that needn't make
    them lasting operators either (undecided): they could be macros over `if`, as in Scheme
    and as `cond` already is (`prelude_macros.cdy`; the backend would write nested `if`
    expressions, unless it learns to spot the pattern); or functions whose later arguments are lazy (thunks, or a
    by-name parameter type, if Candy gets one);
  - **`tup`** builds a tuple of any length, the same gap (its destructuring is a stopgap
    too: `doc/archive/leaks_imvp_py_translator.md`, "`tup` destructuring");
  - **`get` and `assoc`** take a field name, not a value, so they can't be functions until
    Candy has a way to name a field (their checking leaks: `get` in
    `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_pre_self_host.md`);
  - **`format`** is special because its holes are Candy forms in a string (its leak:
    `doc/archive/leaks_imvp_py_translator.md`, "`format` (from smz)"); it could become a
    macro or a reader feature.

  Fix: variadic types (to revisit: `doc/brainstorm.md`), then move what they let be
  typed into `system.cdy`; decide `get`, `assoc` and `format` with records and macros.
