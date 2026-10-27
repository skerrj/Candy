# B44: A macro can't expand into `import`, `import-macros` or `defmacro`

kind: leak
state: open
priority: low
found: modules, 2026-10-19
fixed:
where: `src/cdy/include.cdy`, `src/cdy/expand.cdy`
refs: [[programs.import]], [[macros.import-macros]], [[macros.defmacro]]

The pipeline is read → include → expand → analyse: imports are resolved, and `defmacro`s
collected, before any macro runs. So a macro that returns `(import util)` reaches
`analyse`, which says "import is only allowed at top level", and the same goes for a
generated `defmacro`. Fix: expand top-level forms before `include`, one at a time (as
Racket and Clojure do); until then, a better error. From `doc/archive/leaks_modules.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an easy workaround, or rare.
