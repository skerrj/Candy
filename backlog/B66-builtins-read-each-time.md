# B66: `special.cdy` and `system.cdy` are read for every translation

kind: tech-debt
state: done
priority: normal
found: symbol-table, 2026-10-21
fixed: stdlib, 2026-11-19
where: `src/cdy/expand.cdy` (`library-builtins`)
refs:

And again for every macro program, and checked against `spelling.py` each time. Nothing
caches them. From `doc/tech_debt.md`.

## Notes
- 2026-11-15, Claude: measured (`library_layers.md`, step 1): for a program of four modules
  (with the prelude), reading `special.cdy` and `system.cdy` is 62% of the translation,
  under a profiler: `library-builtins` runs 11 times, per module and per macro program.
  The biggest of the three costs; to fix in `stdlib` (Question 7).
- 2026-11-19, Claude: the built-ins read once per translation (`stdlib` step 2, the
  HLD's "Done"): `library-builtins` runs once, against 11 times for `modules.cdy`; 0.219 s
  to 0.119 s.
- 2026-11-24, the owner: ticked in review.
