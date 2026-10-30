# B119: A variant or value written as a type gets a message about imports

kind: defect
state: open
priority: low
found: type-checker, 2026-10-29
fixed:
where: `src/cdy/core.cdy`
refs: [[match.sum-types]], [[types.exist]]

A sum's variants are constructors, not types, so `(sig a A)` with `A` a variant of `S` is
rejected, which is right; but the message says `A is not defined here; bad defines it,
but this file doesn't import bad`, naming the file itself. `check-type` looks the name up
in the program's `elsewhere` names, which hold every module's top-level values, this
file's too. The same happens for any capitalised value: `(sig X Int) (def X 1) (sig a X)`.
It should say what the name is: `A is a variant of S, not a type`, `X is a value, not a
type`.

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
