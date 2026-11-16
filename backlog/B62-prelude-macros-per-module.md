# B62: Every module compiles the prelude's macros

kind: tech-debt
state: open
priority: normal
found: modules, 2026-10-19
fixed:
where: `src/cdy/expand.cdy`
refs:

With `form.cdy`, and again for each macro file it loads: each module is expanded on its
own, with nothing shared. From `doc/tech_debt.md`.

## Notes
- 2026-11-15, Claude: measured (`library_layers.md`, step 1): compiling the prelude's
  macros per module is 39% of a four-module translation, under a profiler (overlapping
  [[B66]], since each macro program reads the built-ins again). To fix in `stdlib`.
