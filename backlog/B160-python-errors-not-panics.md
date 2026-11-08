# B160: Python's own errors aren't panics: its traceback, and its words

kind: leak
state: open
priority: low
found: semantics-2 step 4, 2026-11-06
fixed:
where: `src/cdy_rt/primitives.py`, `src/cdy/emit.cdy`
refs: [[library.errors]], [[library.bounds]], [[B39]]

A panic stops the program with `candy: ` and its message ([[library.errors]]), through
the runtime's `panic_hook`, which handles a `fail` (`CandyFail`) and Python's
`IndexError`. Two leaks remain:

- **Python's words:** `(at xs 0)`, an index written as a number, is Python's `xs[0]`
  ([[library.bounds]]), so out of range it says `candy: tuple index out of range`, not
  `at: index out of range: 0, for length 0`.
- **Python's other errors:** an integer divided by zero (`quot`, `mod`), a missing map
  key (`map-get`), and a recursion too deep stop with Python's traceback and exception
  (`ZeroDivisionError`, `KeyError`, `RecursionError`). Which of them is a panic, and what
  it says, isn't in the spec.

Fix: decide each in the spec as a panic, with Candy's message (a checked `quot` and
`map-get`, as `at` is), and let the hook take the rest; a traceback kept behind a flag,
for debugging the translator.

## Notes

- 2026-11-06, Claude: found building step 4 of `semantics-2`: the hook handles only the
  panics Candy defines, so that a bug in the translator keeps its traceback.
