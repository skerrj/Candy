# B2: `(sig x (List))` crashes the translator

kind: defect
state: open
priority: normal
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/emit.cdy` (`emit-tcon`)
refs: [[types.table]]

A type constructor's arguments aren't counted, so `(List)`, with none, reaches `emit-tcon`,
which fails with Python's `IndexError` instead of a Candy error. A wrong count that isn't
zero, `(Maybe Int Int)`, translates, and only mypy rejects it. Found writing the spec
(`doc/hl_rqmt/executable_spec.md`, step 3); the audit's defect 2
(`doc/hl_rqmt/tracking.md`).

## Repro

The translator should fail, naming the type:

```candy error
(sig x (List))
(def x 1)
```
```expect-error
List
```

## Notes

- 2026-10-25, the owner: the repro's message (`List`) is a placeholder; whoever fixes this
  writes the real one, and tightens the `expect-error` when the example moves into the
  spec.
