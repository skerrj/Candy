# B131: Python-name errors have no position, and a format hole's column can be off

kind: defect
state: open
priority: low
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/emit.cdy`, `src/cdy/core.cdy`
refs: [[B14]], [[library.format]]

What [[B14]] left. `emit`'s checks that two names are one Python name (`add-globals`) and
that a record's fields can be spelled (`check-py-fields`) say no `file:line:col`: a
`TDeft` has no position, and the globals are checked by name only. And forms read from a
`format` hole are placed from the string's value, not its source text, so an escape
(`\"`, `\n`) before a hole on its line puts the column one short per escape
(`text-pos` in `core.cdy`).
