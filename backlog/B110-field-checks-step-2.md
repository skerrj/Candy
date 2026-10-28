# B110: field-checks step 2: Python names

kind: task
state: done
priority: normal
found: field-checks, 2026-10-27
fixed: field-checks
where: `doc/hl_rqmt/field_checks.md`
refs: [[B5]]

Step 2 of `doc/hl_rqmt/field_checks.md`. Two fields that are one Python name, and a field that starts with `_` or `-`, are errors (`emit.cdy`); [[B5]]'s repro moves into the spec.

## Notes

- 2026-10-27, the owner: ticked in review, after one change: the messages start `deft V:`
  and `deft S, variant B:`, as step 1's do.
