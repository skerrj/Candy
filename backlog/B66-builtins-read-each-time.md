# B66: `special.cdy` and `system.cdy` are read for every translation

kind: tech-debt
state: open
priority: normal
found: symbol-table, 2026-10-21
fixed:
where: `src/cdy/expand.cdy` (`library-builtins`)
refs:

And again for every macro program, and checked against `spelling.py` each time. Nothing
caches them. From `doc/tech_debt.md`.
