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
  `self-host-cleanup`).

Those entries stay in effect until they are fixed. When one is fixed, mark it there (strike
it through and say where it was fixed) rather than copying it here. This file is for leaks
added from branch `macros` on.

- **Macros run with Python's `exec`** (`load_macros` in `cdy_rt/table_defs.py`): the
  translator translates the macro code into Python and executes it inside its own module
  namespace, so Candy's macros depend on the translator running on Python, and on Python
  module namespaces (the macro program's copy of `form.cdy` is replaced by the
  translator's names after it runs). The steps are in `doc/hl_rqmt/macros.md`, "How
  `load-macros` runs macro code". Fix: with modules, the macro program could import
  the translator's `form` module instead of copying it; a translator on another host
  needs another way to run macro code (or an interpreter).
- **A macro's result isn't checked to be a `Form`:** Candy has no type checker yet, and
  macro code is executed without `mypy`, so a macro that returns, say, an `Int` gives a
  confusing error (or none) later. Fix: Candy's type checker; meanwhile `call_macro` could
  check the result's class.
- **`gensym` is impure:** a counter in the runtime (`fresh_name`), restarted when a
  program's macros are loaded. It is the only built-in with state besides I/O. Fix: pass a
  counter through expansion, or take names from a supply in the expansion's context.
