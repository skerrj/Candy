# B61: `expand.cdy` knows the shape of some special forms

kind: tech-debt
state: open
priority: normal
found: macros, 2026-10-18
fixed:
where: `src/cdy/expand.cdy`
refs: [[B11]]

`defn`, `fn`, `let`, `match`, `cond`, and the forms with no expressions, to leave binding
positions unexpanded. It duplicates a little of `analyse`'s syntax, and gets malformed
forms past to `analyse` only roughly. (Its variant check is [[B11]].)
From `doc/tech_debt.md`.
