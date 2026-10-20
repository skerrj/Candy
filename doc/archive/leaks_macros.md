# Leaks (macros, archived)

**Archived** at tag `macros`. These entries still apply until they are fixed; when one is fixed, strike it through here and say where. New leaks go in `doc/leaks.md`. Earlier lists are `doc/archive/leaks_imvp_py_translator.md`, `doc/archive/leaks_pre_self_host.md` and `doc/archive/leaks_self_host_cleanup.md`.

Places where Candy's implementation lets Python show through, or takes a shortcut that
Candy's design will need to fix later, added on branch `macros`.

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
