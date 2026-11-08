# B151: A float with no Candy literal is shown as Python writes it

kind: leak
state: done
priority: low
found: semantics step 2, 2026-11-02
fixed: semantics-2
where: `src/cdy_rt/primitives.py`
refs: [[library.show]], [[syntax.numbers]]

`show` gives a value as an expression that evaluates to it, but a number has digits on
both sides of its `.` ([[syntax.numbers]]), so `1e+20`, `inf` and `nan` have no literal:
`show_float` writes Python's `repr` (`(put big)` prints `1e+20`). Fix: an exponent in
Candy's number syntax, and names for infinity and not-a-number, or a shown form for them
(`(/ 1.0 0.0)`, once [[B23]]'s `/` is settled).

## Notes
- 2026-11-06, Claude: fixed in `semantics-2` step 1: Candy's float literals have an
  exponent (`1.0e20`, `1.5e-3`; [[syntax.numbers]]), and `show` writes one where
  Python's `repr` does ([[library.show]]). Infinity and not-a-number, which still have no
  literal, moved to [[B158]].
