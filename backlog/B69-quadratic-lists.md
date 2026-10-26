# B69: Building a list is quadratic

kind: tech-debt
state: open
priority: normal
found: system-prelude, 2026-10-19
fixed:
where: `src/cdy/`
refs:

`(+ acc (to-list x))` copies the whole tuple. `map`, `filter` and `fold` are built-ins to
avoid it, but the translator's own accumulator loops (about 94 `defn`s) still pay it.
Long-term fix: in `doc/hl_rqmt/mutation_optimization.md`. From `doc/tech_debt.md`.
