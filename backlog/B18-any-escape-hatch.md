# B18: `Any` turns checking off

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `.cdy` files that use `Any`
refs: [[types.table]], [[B34]], [[B48]], [[B49]]

`Any` is the escape hatch for a type Candy can't write yet: Candy's checker matches it
with every type, both ways ([[checking.any]]), and it becomes Python's `Any`, so mypy
checks nothing that passes through it either. A `get` on a value typed `Any` translates
and, for a field the value lacks, fails when run (`AttributeError`). Every use is a leak; grep `.cdy` files for
`Any` to find them. Fix: the types it stands in for ([[B48]],
[[B34]], [[B49]]). From `doc/archive/leaks_imvp_py_translator.md` ("`Any`").

## Notes

- 2026-10-29, type-checker step 3: Candy's checker skips `Any` too; the text says so.
