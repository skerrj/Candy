# B10: A record constructor's number of arguments isn't checked

kind: defect
state: open
priority: normal
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/core.cdy`
refs: [[types.records]], [[match.constructors]]

`(V 1 2)` for a one-field record translates, and fails only in mypy or at run time
(`TypeError`); a variant's constructor is checked ("(C ...) takes 1 field(s), got 2").
From `doc/archive/leaks_executable_spec.md`; the audit's defect 9 (`doc/hl_rqmt/tracking.md`).

## Repro

The translator should fail:

```candy error
(deft V ((x Int)))
(put (V 1 2))
```
```expect-error
(V ...) takes 1 field(s), got 2
```
