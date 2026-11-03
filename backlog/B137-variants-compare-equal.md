# B137: Two variants of one sum with the same fields are equal

kind: defect
state: done
priority: normal
found: master, 2026-11-01
fixed: semantics
where: `src/cdy/emit.cdy`
refs: [[B27]], [[match.sum-types]]

A variant is a Python `NamedTuple`, and `NamedTuple`s compare as plain tuples, so `(A 1)`
and `(B 1)`, two variants of one sum each with one `Int` field, are `=`: Python's `==`
doesn't look at the class. Found writing `doc/hl_rqmt/semantics.md` (its "Equality";
step 3 fixes it). Two records of different types can't meet at `=` (the checker makes
both sides one type), except through `Any`.

## Notes

- 2026-11-02, Claude: semantics step 3: every record and variant class gets `__eq__`, `__ne__` and `__hash__` comparing (and hashing) its class too (`eq-methods` in `emit.cdy`), so `(A 1)` and `(B 1)` differ, in `=`, `in`, `index-of` and as map keys. The repro moved to [[expr.equality]] (`(= a (B 1))` prints `false`); it was:

  ````text
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
  ````
