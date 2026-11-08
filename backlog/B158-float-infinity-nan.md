# B158: Infinity and not-a-number have no literal, and `/` by zero fails

kind: leak
state: open
priority: low
found: semantics-2 step 1, 2026-11-06
fixed:
where: `src/cdy_rt/primitives.py`, `src/cdy_rt/spelling.py`, `src/cdy/read.cdy`
refs: [[library.show]], [[expr.arithmetic]], [[syntax.numbers]], [[B151]]

A `Float` or `Double` is an IEEE 754 number ([[syntax.numbers]]), so it can be infinite
or not a number: `(* 1.0e300 1.0e300)` is infinity. But Candy has no literal for either,
so `show` writes Python's `inf` and `nan`, which don't read back ([[library.show]]); and
`(/ 1.0 0.0)`, infinity in IEEE 754, fails when run, with Python's `ZeroDivisionError`.
Fix: names for them (`Double/inf`, `Double/nan`, once there are modules' names, or
prelude values), shown as those names; and `/` on floats spelled as IEEE 754's (a
helper that gives infinity or not-a-number on a zero divisor), where the cost is one call
per division.

## Notes

- 2026-11-06, Claude: split from [[B151]], whose exponent is done; Candy's float
  literals now read Python's other shown forms back.
