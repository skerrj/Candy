# B159: `isspace-at` and `is-neg-int` count a negative index from the end

kind: leak
state: open
priority: low
found: semantics-2 step 2, 2026-11-06
fixed:
where: `src/cdy_rt/primitives.py`
refs: [[library.bounds]], [[B35]]

`at` and `slice` panic on an index out of range ([[library.bounds]]), but two string
built-ins that take an index are still Python's subscripts: `(isspace-at text pos)` is
`text[pos]`, so a negative `pos` counts from the end and a `pos` past it fails with
Python's `IndexError`; `(is-neg-int text pos)` reads `text[pos : pos + 1]`, so `pos` -2
looks at the last two characters. The translator's reader, their only user, calls them
with `pos` in range. Fix: check the index as `at` does (both are lookaheads, so past the
end could be `false`, but a negative index a panic); or drop them once `at` on a `String`
gives a `Char` the reader can test ([[B18]]).

## Notes

- 2026-11-06, Claude: found while listing, for the owner, the built-ins that stop at a
  list's end instead of panicking (in [[library.bounds]]).
