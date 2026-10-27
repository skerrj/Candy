# B58: The reader builds strings and lists one item at a time

kind: tech-debt
state: open
priority: low
found: bootstrap, 2026-10-20
fixed:
where: `src/cdy/read.cdy`
refs:

Quadratic, but fast enough (it reads the whole translator in about 0.02 s). From `doc/tech_debt.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): cosmetic or harmless.
