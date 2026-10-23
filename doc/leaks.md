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
- `doc/archive/leaks_symbol_table.md`: the symbol table (up to tag `symbol-table`).

Those entries stay in effect until they are fixed. When one is fixed, mark it there (strike
it through and say where it was fixed) rather than copying it here. This file is for leaks
added from branch `library` on.

- **`Maybe` is `None`-or-a-value, so `(Maybe (Maybe a))` collapses** (from `library`, step
  4): `find` and `index-of` return `None` for "not found", which is also what a list of
  `Maybe`s holds for "nothing", so `(find f xs)` on such a list can't tell the two apart,
  and `with-default` takes either as missing. Python's `Optional` is the leak. Fix: a
  real `Maybe` sum (`(deft (Maybe a) (Nothing) (Just ((val a))))`), when Candy's types
  are its own.
