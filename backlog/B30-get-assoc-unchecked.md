# B30: `get` and `assoc` field names are checked by mypy, not Candy

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/core.cdy`
refs: [[types.records]], [[match.form]]

`get` works on any Python object with that attribute, not only records; a field the
record doesn't have, or `(get s r)` on a `Shape` that might be a `Rect` (after no
`match`), translates, and mypy (with a `sig`) or the run (`AttributeError`) rejects it.
`get` and `assoc` are special forms because they take a field's name, not a value (Candy
can't name a field). From `doc/archive/leaks_imvp_py_translator.md`, `doc/archive/leaks_pre_self_host.md` ("`get` after
`match`"), `doc/archive/leaks_symbol_table.md` and `doc/archive/leaks_executable_spec.md`.
