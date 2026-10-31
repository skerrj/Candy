# B119: A variant or value written as a type gets a message about imports

kind: defect
state: done
priority: low
found: type-checker, 2026-10-29
fixed: typed-core
where: `src/cdy/core.cdy`
refs: [[match.sum-types]], [[types.exist]]

A sum's variants are constructors, not types, so `(sig a A)` with `A` a variant of `S` is
rejected, which is right; but the message says `A is not defined here; bad defines it,
but this file doesn't import bad`, naming the file itself. `check-type` looks the name up
in the program's `elsewhere` names, which hold every module's top-level values, this
file's too. The same happens for any capitalised value: `(sig X Int) (def X 1) (sig a X)`.
It should say what the name is: `A is a variant of S, not a type`, `X is a value, not a
type`.

## Notes

- 2026-10-31, Claude: fixed by typed-core step 4 ([[B129]]), in `check-type`
  (`src/cdy/core.cdy`): before the import check, it asks whether the name is a variant
  (the scope's `variants` map gives its sum, filled by `find-variants`) or a top-level
  value (`top`). The repro moved into the spec: it is the second-last row of
  [[types.exist]]'s `candy errors` table (`spec/20-types.md`), and the last row is the
  value case:

  ```text
  (deft S (A ((x Int))) (B ((y Int)))) (sig a A) (def a (A 1)) => A is a variant of S, not a type
  (sig X Int) (def X 1) (sig a X) (def a 1) => X is a value, not a type
  ```

  The `## Repro` section it replaced, removed from this item (it ran as a strict expected
  failure until the fix):

  ````text
  ## Repro

  The translator should fail:

  ```candy error
  (deft S (A ((x Int))) (B ((y Int))))
  (sig a A)
  (def a (A 1))
  ```
  ```expect-error
  A is a variant of S, not a type
  ```
  ````

  Run as a file, `b119.cdy`, at tag `boot/46` (before) and with step 4's translator:

  ```text
  before: b119.cdy:2:1: A is not defined here; b119 defines it, but this file doesn't import b119
  after:  b119.cdy:2:1: A is a variant of S, not a type
  ```
