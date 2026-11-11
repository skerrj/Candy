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

## Notes

- 2026-10-31, Claude, in typed-core's review: maps too. `map-set` copies the whole dict,
  so a map built or updated one key at a time is quadratic as a list is. `typed-core`
  step 2 worked around it: the types the checker records are kept in a map of their own
  (`St`'s `types`), not in the substitution, which every unification reads and extends.
  The fix is the same as for lists (`doc/hl_rqmt/mutation_optimization.md`: persistent
  maps, or mutation behind the language).
- 2026-11-09, Claude: since `collections` step 4 the pattern is `(++ acc (to-list x))`:
  `++` joins lists, `+` adds numbers only ([[expr.append]]).
