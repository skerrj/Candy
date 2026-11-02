# B137: Two variants of one sum with the same fields are equal

kind: defect
state: open
priority: normal
found: master, 2026-11-01
fixed:
where: `src/cdy/emit.cdy`
refs: [[B27]], [[match.sum-types]]

A variant is a Python `NamedTuple`, and `NamedTuple`s compare as plain tuples, so `(A 1)`
and `(B 1)`, two variants of one sum each with one `Int` field, are `=`: Python's `==`
doesn't look at the class. Found writing `doc/hl_rqmt/semantics.md` (its "Equality";
step 3 fixes it). Two records of different types can't meet at `=` (the checker makes
both sides one type), except through `Any`.

## Repro

The program should print `different`:

```candy run
(deft S (A ((x Int))) (B ((x Int))))
(sig a S)
(def a (A 1))
(sig b S)
(def b (B 1))
(put (if (= a b) "equal" "different"))
```
```expect
different
```
