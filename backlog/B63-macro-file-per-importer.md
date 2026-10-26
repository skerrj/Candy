# B63: A macro file is compiled once per file that imports it

kind: tech-debt
state: open
priority: normal
found: macros, 2026-10-18
fixed:
where: `src/cdy/expand.cdy`
refs:

And its helpers again in each importer's macro program, with no cache across a
translation. From `doc/tech_debt.md`.
