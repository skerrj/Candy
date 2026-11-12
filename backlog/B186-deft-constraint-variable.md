# B186: A `deft`'s type variable named for a constraint gets it, unspecified

kind: defect
state: done
priority: normal
found: collections-2 step 7, 2026-11-11
fixed: collections-2, 2026-11-11
where: `src/cdy/core.cdy` (`top-deft`)
refs: [[types.records]], [[checking.constraints]], [[B34]]

A `deft`'s type variable named for a constraint (`number`, `comparable2`, ...) took the
constraint: `(deft (Box number) ((v number)))` made `(Box "a")` an error ("argument 1 of
Box: expected number, got String"), since the constructor's type is instantiated as any
`sig`'s is (`keep-constraint`). No rule said so, and `(Box 1)`, which runs, failed `mypy
--strict`: `emit` wrote `class Box[number: (int, float)](NamedTuple)`, and mypy rejects a
constrained type variable on a NamedTuple class with `eq-methods`.

Fix: an error, *lasting* (until interfaces, [[B34]]): a constraint is on the functions
that need it, not on the type, as Elm has it and Haskell 2010 decided, removing
`DatatypeContexts` (`data Ord a => Set a`).

## Notes

- 2026-11-11, Claude: found walking through where constraint variables are used; the owner
  chose to make it an error, in `collections-2` step 7 ([[B182]]). Fixed: `top-deft`
  (`core.cdy`) fails with `deft Box: a type variable can't be a constraint (number)`, at
  the variable; two rows of [[types.records]]. In review. No program used it. Its repro
  went straight into the spec; it would have been:

  ````text
  ## Repro

  The translator should fail:

  ```candy error
  (deft (Box number) ((v number)))
  (put (Box 1))
  ```
  ```expect-error
  deft Box: a type variable can't be a constraint (number)
  ```
  ````
- 2026-11-11, the owner: ticked in review.
