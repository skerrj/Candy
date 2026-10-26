# B45: Macro files still use inclusion

kind: leak
state: open
priority: normal
found: modules, 2026-10-19
fixed:
where: `src/cdy/include.cdy`
refs: [[macros.import-macros]]

In a macro file, `(import name)` pastes `name.cdy` in as helpers, with global names, and
the macro program (`form.cdy`, helpers and `defmacro`s) is one flat program. Fix: macro
programs as modules, which would also let them import the translator's `form` module
instead of copying it. From `doc/archive/leaks_modules.md`.
