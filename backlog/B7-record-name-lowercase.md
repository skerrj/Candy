# B7: A lowercase record name is accepted

kind: defect
state: open
priority: normal
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/core.cdy`
refs: [[types.records]], [[types.names]]

`(deft v ((x Int)))` translates, though type names are Capitalised (a variant's name is
checked: "deft: variant names are Capitalised, not c"). From
`doc/archive/leaks_executable_spec.md`; the audit's defect 6 (`doc/hl_rqmt/tracking.md`).

## Repro

The translator should fail:

```candy error
(deft v ((x Int)))
(put 1)
```
```expect-error
Capitalised, not v
```
