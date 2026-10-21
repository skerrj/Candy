# Leaks (modules, archived)

**Archived** at tag `modules`. These entries still apply until they are fixed; when one is fixed, strike it through here and say where. New leaks go in `doc/leaks.md`. Earlier lists are `doc/archive/leaks_imvp_py_translator.md`, `doc/archive/leaks_pre_self_host.md`, `doc/archive/leaks_self_host_cleanup.md` and `doc/archive/leaks_macros.md`.

Places where Candy's implementation lets Python show through, or takes a shortcut that
Candy's design will need to fix later, added on branch `modules`.

- **A macro can't expand into `import`, `import-macros` or `defmacro`** (found on
  `macros`, recorded here). The pipeline is read → include → expand → analyse: imports are
  resolved, and `defmacro`s collected, before any macro runs. So a top-level `(use util)`
  whose macro returns `(import util)` reaches `analyse` unresolved, which rejects it with
  a misleading `import is only allowed at top level`, and the same goes for a generated
  `defmacro`. It also means the import spellings can't be prelude macros over one base
  import form. Fix: expand top-level forms before `include` handles them, one form at a
  time, so that a form a macro produces can still be an import or a `defmacro` (as
  Racket and Clojure do); until then, a better error ("a macro can't produce import").
- **Macro files still use inclusion:** in a macro file, `(import name)` pastes `name.cdy` in
  as helpers, with step A's global names, and the macro program (`form.cdy`, helpers and
  `defmacro`s) is one flat program. Fix: macro programs as modules, which would also let
  them import the translator's `form` module instead of copying it.
- **Macro templates aren't hygienic across modules:** a template's symbols mean whatever
  the use site sees (`doc/hl_rqmt/macros.md`, "Rework point"). A macro whose expansion
  calls a helper of the macro's own module only works where that helper is imported. Fix:
  qualify a template's free symbols, as Clojure's syntax-quote does, once qualified names
  exist.
- **Only `(import m)`, everything unqualified** (the MVP of `doc/hl_rqmt/modules.md`):
  there are no qualified names, `import-as` or `import-from`, and no private names, so two
  modules that both define a name can't be imported into the same file. Fix: "After the
  MVP" in the HLD.
