# B185: A `(List x)` in a `match` clause's value can fail mypy

kind: defect
state: open
priority: normal
found: collections-2 step 6, 2026-11-11
fixed:
where: `src/cdy/emit.cdy`
refs: [[types.constructors]], [[B184]], [[B125]]

A `match` whose value is used is a chain of assignments to one temporary in Python, which
`emit` doesn't annotate; mypy types the temporary by its first assignment. `(List x)` is
the tuple literal `(x,)`, which mypy types `tuple[int]` (one item), not the
`tuple[int, ...]` the checker found, so a later clause's `(List 1 2)` or a list of
another length fails `mypy --strict`, though the program type-checks and runs right.
`to-list` (a function returning `tuple[T, ...]`) hid it in the translator until
`collections-2` step 6 replaced it with `(List x)`.

The translator works around it: `read-type` (`core.cdy`) has its clause that gives a whole
list first.

Fix: `emit` annotates the temporary with the `match`'s type, as the checker found it; an
empty literal's start ([[B184]]) wants the same, so one fix may close both.

## Repro

This prints `(List 3) (List 1 2)`, as it should, and fails `mypy --strict`: the
temporary is `tuple[int]`, and `(1, 2)` is assigned to it. As [[B184]]'s, it is a plain
`candy` block, not run (`test_spec.py` runs mypy on the spec's files only).

```candy
(sig f (Fn ((Maybe Int)) (List Int)))
(defn f (m)
  (let ((xs (match m ((Some v) (List v)) ((None) (List 1 2)))))
    xs))

(put (f (Some 3)) (f None))
```

## Notes

- 2026-11-11, Claude: found replacing `to-list` (`collections-2` step 6, [[B181]]):
  `read-type`'s `match` failed T2's `mypy --strict`. Worked around as above.
