# B110: field-checks step 2: Python names

kind: task
state: open
priority: normal
found: field-checks, 2026-10-27
fixed:
where: `doc/hl_rqmt/field_checks.md`
refs: [[B5]]

Step 2 of `doc/hl_rqmt/field_checks.md`. Two fields that are one Python name, and a field that starts with `_` or `-`, are errors (`emit.cdy`); [[B5]]'s repro moves into the spec.
