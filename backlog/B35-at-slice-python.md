# B35: `at` and `slice` behave as Python's subscripts

kind: leak
state: done
priority: normal
found: py-py-translator, 2026-10-17
fixed: semantics-2
where: `src/cdy/emit.cdy`
refs: [[library.lists]], [[B71]]

`at` and `slice` are emitted as `coll[i]` and `coll[i:j]`, so mypy keeps the element type,
and their behaviour (negative indexes, out-of-range slices) is Python's. From `doc/archive/leaks_imvp_py_translator.md`.
Related: [[B71]].

## Notes
- 2026-11-06, Claude: fixed in `semantics-2` step 2: `at` and `slice` out of range are a
  panic, negative indexes too, through the runtime's checked `at` and `slice_`;
  `(at xs 0)`, a literal index that can't be negative, stays `xs[0]`, whose
  `IndexError` covers the high side ([[library.bounds]]).
