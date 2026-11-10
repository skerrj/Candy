# B38: Operators can't be values

kind: leak
state: done
priority: low
found: py-py-translator, 2026-10-17
fixed: collections
where: `src/cdy/core.cdy`
refs: [[expr.calls]], [[expr.operator-arity]]

`(put +)`, or passing `<` to a function, is an error; wrap it: `(fn (a b) (< a b))`.
From `doc/archive/leaks_imvp_py_translator.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an easy workaround, or rare.
- 2026-11-09, Claude: fixed by `collections` step 3 ([[B163]]): an operator as a value is
  its function of two arguments ([[expr.operator-values]]), `(fold + 0 xs)`.
