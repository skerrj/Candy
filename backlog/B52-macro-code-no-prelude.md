# B52: Macro code doesn't get the prelude

kind: leak
state: open
priority: normal
found: library, 2026-10-22
fixed:
where: `src/cdy/expand.cdy`, `src/cdy/form.cdy`
refs: [[macros.macro-code]], [[programs.prelude]]

A macro program gets the built-ins and `form.cdy`, but not `prelude.cdy`, so macro code
can't call `rest` or `map-update`, and has `form.cdy`'s `rest-of` instead: macro code sees
a different library from a program's, further behind as the prelude grows. What code that
runs while translating can see is a phase question (Racket's
`(require (for-syntax ...))`). Fix: give macro programs the prelude, or let them import
it (`doc/hl_rqmt/modules.md`, "Macro modules on the host"); then `rest-of` can go. From
`doc/archive/leaks_library.md`.
