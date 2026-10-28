# B6: A record (or variant) with the same field twice translates

kind: defect
state: done
priority: high
found: executable-spec, 2026-10-24
fixed: field-checks
where: `src/cdy/core.cdy`
refs: [[types.records]], [[match.sum-types]]

`(deft V ((x Int) (x Int)))` becomes a one-field Python class; so does a variant with a
field twice. A pattern with a name twice is already an error ("names in a pattern must be
different"). Fix: the same check for fields. From `doc/archive/leaks_executable_spec.md`;
the audit's defect 5 (`doc/hl_rqmt/tracking.md`).

## Notes

- 2026-10-26, the owner: `high` in triage ([[B103]]): silent wrong output.
- 2026-10-27, field-checks step 1: a repeated field is an error (`deft-fields` in
  `core.cdy`), in a record or a variant. The repro is now this row of
  `[[types.records]]`: `(deft V ((x Int) (x Int))) => deft V: field names must be
  different (x)`.
