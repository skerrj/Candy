# B184: An empty list or map as a `fold`'s or `map-acc`'s start fails mypy

kind: defect
state: open
priority: normal
found: collections-2 step 3, 2026-11-11
fixed:
where: `src/cdy/emit.cdy`
refs: [[library.lists]], [[library.map-acc]], [[B123]], [[B125]]

A program that type-checks must pass `mypy --strict` too ([[B125]]), but an empty literal
in a generic call's argument, with nothing in Python around it to say its type, doesn't:
mypy types `()` as `tuple[()]` and `{}` as `dict[Never, Never]`, and then the `fn`'s
parameter, typed with what the checker inferred, doesn't match. Seen as a `fold`'s start
`(Tup 0 empty-list)` (a tuple holding the empty list), and as a `map-acc`'s start
`empty-map` whose result a `Tup` pattern takes apart (an unannotated temporary). A `fold`
from `empty-map` straight into a function's result passes: the `def`'s return type is
mypy's context.

The translator works around it (`collections-2` step 3): such a start is a parameter, typed
by the `sig`, its callers passing it empty (`solve-each`'s `left`, `check-order`'s `start`).

Fix: `emit` writes an empty literal the checker typed with that type
(`cast(tuple[int, ...], ())`, or an annotated temporary), as it annotates a `let`-bound
`fn`.

## Repro

This prints `(Tup 6 (List 1 3 6))`, as it should, and fails `mypy --strict`: argument 1 to
`list_fold` has an incompatible type, the start typed `tuple[int, tuple[()]]`. A repro's `candy run` block isn't run through mypy (`test_spec.py` runs mypy on
the spec's files only), so it is a plain `candy` block, not run; once fixed, it goes into
[[library.lists]]'s examples, where mypy checks it.

```candy
(sig sums (Fn ((List Int)) (Tup Int (List Int))))
(defn sums (xs)
  (fold (fn (acc x) (let (((n ys) acc)) (Tup (+ n x) (++ ys (List (+ n x)))))) (Tup 0 empty-list) xs))

(put (sums (List 1 2 3)))
```

## Notes

- 2026-11-11, Claude: found converting `check.cdy`'s loops (`collections-2` step 3,
  [[B178]]): `solve-each`'s `fold` from `(Tup start empty-list)` and `check-order`'s
  `map-acc` from `empty-map` failed T2's `mypy --strict`. Worked around as above; the
  repro fails only at mypy (it prints the right thing).
