# B59: Only symbols and lists carry positions

kind: tech-debt
state: done
priority: normal
found: self-host-cleanup, 2026-10-18
fixed: typed-core
where: `src/cdy/form.cdy` (`Pos`)
refs: [[B14]]

Not literals: an error about a literal points at its enclosing list. From `doc/tech_debt.md`. Related:
[[B14]].

## Notes

- 2026-10-31, Claude: fixed by typed-core step 1 ([[B126]]): literal forms have positions.
