# B18: `Any` turns checking off

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `.cdy` files that use `Any`
refs: [[types.names]], [[B34]], [[B48]], [[B49]]

`Any` is the escape hatch for a type Candy can't write yet, and becomes Python's `Any`, so
mypy checks nothing that passes through it. Every use is a leak; grep `.cdy` files for
`Any` to find them. Fix: the types it stands in for ([[B48]],
[[B34]], [[B49]]). From `doc/archive/leaks_imvp_py_translator.md` ("`Any`").
