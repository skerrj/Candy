# B6: A record (or variant) with the same field twice translates

kind: defect
state: open
priority: high
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/core.cdy`
refs: [[types.records]], [[match.sum-types]]

`(deft V ((x Int) (x Int)))` becomes a one-field Python class; so does a variant with a
field twice. A pattern with a name twice is already an error ("names in a pattern must be
different"). Fix: the same check for fields. From `doc/archive/leaks_executable_spec.md`;
the audit's defect 5 (`doc/hl_rqmt/tracking.md`).

## Repro

The translator should fail:

```candy error
(deft V ((x Int) (x Int)))
(put 1)
```
```expect-error
must be different
```

## Notes

- 2026-10-26, the owner: `high` in triage ([[B103]]): silent wrong output.
