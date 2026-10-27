# B9: `nil` can be defined

kind: defect
state: open
priority: low
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/core.cdy`
refs: [[expr.unit]], [[syntax.literals]]

`(sig nil Int) (def nil 1)` translates. `true` and `false` are literals; `nil` is a name
the translator knows. Whether `nil` is a literal (so it can't be defined) or a reserved
name is a decision, so the repro is text until it is made. From
`doc/archive/leaks_executable_spec.md`; the audit's defect 8 (`doc/hl_rqmt/tracking.md`).

## Repro

Translates, and prints `1`:

```candy
(sig nil Int)
(def nil 1)
(put nil)
```

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): waits on a decision (a literal, or a reserved name).
