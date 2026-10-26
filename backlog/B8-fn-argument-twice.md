# B8: A function with the same argument twice is accepted

kind: defect
state: open
priority: normal
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/core.cdy`
refs: [[expr.functions]]

`(fn (x x) x)` and `(defn f (x x) x)` translate (Python then rejects the duplicate
argument). A pattern with a name twice is an error already. From
`doc/archive/leaks_executable_spec.md`; the audit's defect 7 (`doc/hl_rqmt/tracking.md`).

## Repro

The translator should fail:

```candy error
(sig f (Fn (Int Int) Int))
(defn f (x x) x)
```
```expect-error
must be different
```
