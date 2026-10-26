# B68: The whole prelude goes into every program

kind: tech-debt
state: open
priority: normal
found: system-prelude, 2026-10-19
fixed:
where: `src/cdy/include.cdy`, `src/cdy/emit.cdy`
refs: [[programs.prelude]]

Used or not, and it is read and expanded again for every translation. From `doc/tech_debt.md`.
