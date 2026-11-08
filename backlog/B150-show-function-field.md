# B150: A record with a function field is shown when run, not refused when translated

kind: defect
state: done
priority: low
found: semantics step 2, 2026-11-02
fixed: semantics-2
where: `src/cdy/emit.cdy`, `src/cdy_rt/primitives.py`
refs: [[library.show]]

A function can't be shown, an error when translated ([[library.show]]), but `emit`'s
`show-type` sees only the type it is given: a record or variant is its name and type
arguments, so a function among its fields (`field-show-type` writes it `"Fn"`) is found
only by the runtime's `show`, which fails when the program runs (`CandyFail: show: a
function can't be shown`). Fix: `show-type` looks through a record's and variant's
fields (the `deft`s are in `emit`'s input), as far as the type's own recursion allows.

## Notes

- 2026-11-02, Claude: semantics step 3: `=` likewise: the checker refuses comparing a function, or a type holding one (`has-fn`), but doesn't look into a record's fields, so a record with a function field compares its functions by identity, as Python does.
- 2026-11-06, Claude: fixed in `semantics-2` step 2: `emit`'s `show-type` looks into a
  record's or variant's fields, and a sum's variants (`holds-fn`, over `Env`'s `fields`),
  and the checker's `has-fn` likewise for `=` (`fields-have-fn`, over `Ctx`'s shapes),
  each with the types already seen, so a recursive type ends. The repro moved to
  [[library.show]], as an error table's row; it was:

  ````text
  ## Repro

  ```candy error
  (deft F ((f (Fn (Int) Int))))
  (put (F (fn (n) n)))
  ```
  ```expect-error
  show: a function can't be shown
  ```
  ````
