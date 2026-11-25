# B62: Every module compiles the prelude's macros

kind: tech-debt
state: done
priority: normal
found: modules, 2026-10-19
fixed: stdlib, 2026-11-19
where: `src/cdy/expand.cdy`
refs:

With `form.cdy`, and again for each macro file it loads: each module is expanded on its
own, with nothing shared. From `doc/tech_debt.md`.

## Notes
- 2026-11-15, Claude: measured (`library_layers.md`, step 1): compiling the prelude's
  macros per module is 39% of a four-module translation, under a profiler (overlapping
  [[B66]], since each macro program reads the built-ins again). To fix in `stdlib`.
- 2026-11-19, Claude: the prelude's macros compiled and loaded once per translation
  (`stdlib` step 2, the HLD's "Done": `new-expander`), not per module.
- 2026-11-24, the owner: ticked in review.
