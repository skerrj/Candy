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
- `doc/archive/leaks_bootstrap.md`: the bootstrap chain (up to tag `bootstrap`; none);
- `doc/archive/leaks_symbol_table.md`: the symbol table (up to tag `symbol-table`);
- `doc/archive/leaks_library.md`: the library (up to tag `library`);
- `doc/archive/leaks_runtime_names.md`: the runtime's names (up to tag `runtime-names`;
  none).

Those entries stay in effect until they are fixed. When one is fixed, mark it there (strike
it through and say where it was fixed) rather than copying it here. This file is for leaks
added from branch `executable-spec` on.

## Found writing the spec (`executable-spec` step 3)

- **What the translator doesn't check, which fails only in mypy or at run time** (with
  Python's error, `TypeError`, `AttributeError` or `NameError`): a record constructor's
  number of arguments, and a field `get` or `assoc` names that the record doesn't have
  (a variant's constructor is checked: `spec/30-match.md`); a top-level value used before
  its `def` has run; a value called as a function. Fix: Candy's type checker, and a
  definition-order check for values. (`spec/20-types.md`)
- **What the translator accepts and shouldn't:** a record with the same field twice
  (`(deft V ((x Int) (x Int)))`, a one-field Python class), a lowercase record name, a
  function with the same argument twice (`(fn (x x) x)`), and a definition of `nil`. Fix:
  small checks in `core.cdy`, as for variants and patterns.
- **`quot` rounds toward minus infinity** (`(quot -7 2)` is `-4`), as Python's `//`
  does; C, Java and Rust truncate (`-3`). Fix: decide what Candy's is, and spell it per
  target. (`spec/40-expressions.md`)
