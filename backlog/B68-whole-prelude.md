# B68: The whole prelude goes into every program

kind: tech-debt
state: open
priority: normal
found: system-prelude, 2026-10-19
fixed:
where: `src/cdy/include.cdy`, `src/cdy/emit.cdy`
refs: [[programs.prelude]]

Used or not, and it is read and expanded again for every translation. From `doc/tech_debt.md`.

## Notes
- 2026-11-15, Claude: measured (`library_layers.md`, step 1): about 5 ms of a translation
  (2%), but 49 lines of every program's Python (`(put 1)`: 80 lines, 31 without the
  prelude). To fix in `stdlib`, whose modules make it grow.
