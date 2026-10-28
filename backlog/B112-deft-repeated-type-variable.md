# B112: A `deft` with the same type variable twice fails in Python

kind: defect
state: done
priority: normal
found: field-checks, 2026-10-27
fixed: field-checks
where: `src/cdy/core.cdy`
refs: [[types.records]], [[B6]]

`(deft (P a a) ((x a)))` translated, and failed when it ran, with Python's `SyntaxError:
duplicate type parameter 'a'`. Found writing `doc/hl_rqmt/field_checks.md`.

## Notes

- 2026-10-27, field-checks step 1: an error (`top-deft` in `core.cdy`), `deft: type
  variables must be different (a)`; a row of `[[types.records]]`.
