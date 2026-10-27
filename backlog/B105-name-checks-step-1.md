# B105: name-checks step 1: Python-name clashes

kind: task
state: done
priority: normal
found: name-checks, 2026-10-26
fixed: name-checks
where: `doc/hl_rqmt/name_checks.md`
refs: [[B3]], [[B12]]

Step 1 of `doc/hl_rqmt/name_checks.md`. A Candy name that mangles like another, at top level or across modules, is an error (`add-globals` in `emit.cdy`); [[B3]] and [[B12]]'s repros move into the spec.

## Notes

- 2026-10-26, the owner: ticked in review, after one change: a module's name in the
  message is `greet (from module util)`, not `greet (in util)`, which read like part of
  the source.
