# B109: field-checks step 1: repeated names

kind: task
state: review
priority: normal
found: field-checks, 2026-10-27
fixed:
where: `doc/hl_rqmt/field_checks.md`
refs: [[B6]]

Step 1 of `doc/hl_rqmt/field_checks.md`. A `deft` whose fields (a record's, or a variant's) or type variables repeat a name is an error (`top-deft` in `core.cdy`); [[B6]]'s repro moves into the spec.
