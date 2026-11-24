# B45: Macro files still use inclusion

kind: leak
state: review
priority: normal
found: modules, 2026-10-19
fixed: host-macros, 2026-11-23
where: `src/cdy/include.cdy`
refs: [[macros.import-macros]]

In a macro file, `(import name)` pastes `name.cdy` in as helpers, with global names, and
the macro program (`form.cdy`, helpers and `defmacro`s) is one flat program. Fix: macro
programs as modules, which would also let them import the translator's `form` module
instead of copying it. From `doc/archive/leaks_modules.md`.
- 2026-11-23, Claude: a macro file is a module of macro code, its imports real
  (`host-macros` step 4a, [[macros.import-macros]]); inclusion is gone from
  `include.cdy`.
