# B100: `and` and `or` as macros

kind: idea
state: open
priority: normal
found: symbol-table, 2026-10-22
fixed:
where: `src/cdy/special.cdy`
refs: [[expr.logic]]

Short-circuiting needn't make them operators: macros over `if` (as in Scheme, and like
`cond`; the backend would write nested `if` expressions unless it learns to spot the
pattern), or functions whose later arguments are lazy (thunks, or a by-name parameter
type). From `doc/brainstorm.md` and `doc/archive/leaks_symbol_table.md`.
