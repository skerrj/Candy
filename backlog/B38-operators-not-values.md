# B38: Operators can't be values

kind: leak
state: open
priority: low
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/core.cdy`
refs: [[expr.calls]], [[expr.operator-arity]]

`(put +)`, or passing `<` to a function, is an error; wrap it: `(fn (a b) (< a b))`.
From `doc/archive/leaks_imvp_py_translator.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an easy workaround, or rare.
