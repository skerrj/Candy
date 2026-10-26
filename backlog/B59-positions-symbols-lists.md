# B59: Only symbols and lists carry positions

kind: tech-debt
state: open
priority: normal
found: self-host-cleanup, 2026-10-18
fixed:
where: `src/cdy/form.cdy` (`Pos`)
refs: [[B14]]

Not literals: an error about a literal points at its enclosing list. From `doc/tech_debt.md`. Related:
[[B14]].
