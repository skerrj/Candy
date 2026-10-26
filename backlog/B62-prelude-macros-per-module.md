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
