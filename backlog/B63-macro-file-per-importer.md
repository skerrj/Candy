# B63: A macro file is compiled once per file that imports it

kind: tech-debt
state: review
priority: normal
found: macros, 2026-10-18
fixed: host-macros, 2026-11-23
where: `src/cdy/expand.cdy`
refs:

And its helpers again in each importer's macro program, with no cache across a
translation. From `doc/tech_debt.md`.

## Notes

- 2026-11-23, Claude: each macro file loaded once per translation, kept in the Expander,
  which expansion hands on from module to module (`host-macros` step 4b,
  [[macros.import-macros]]); eight modules importing one: 0.20 s to 0.15 s.
