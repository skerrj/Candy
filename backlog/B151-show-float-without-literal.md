# B151: A float with no Candy literal is shown as Python writes it

kind: leak
state: open
priority: low
found: semantics step 2, 2026-11-02
fixed:
where: `src/cdy_rt/primitives.py`
refs: [[library.show]], [[syntax.numbers]]

`show` gives a value as an expression that evaluates to it, but a number has digits on
both sides of its `.` ([[syntax.numbers]]), so `1e+20`, `inf` and `nan` have no literal:
`show_float` writes Python's `repr` (`(put big)` prints `1e+20`). Fix: an exponent in
Candy's number syntax, and names for infinity and not-a-number, or a shown form for them
(`(/ 1.0 0.0)`, once [[B23]]'s `/` is settled).
