# B30: `get` and `assoc` field names are checked by mypy, not Candy

kind: leak
state: done
priority: normal
found: py-py-translator, 2026-10-15
fixed: type-checker
where: `src/cdy/core.cdy`
refs: [[types.records]], [[match.form]], [[checking.records]]

`get` works on any Python object with that attribute, not only records; a field the
record doesn't have, or `(get s r)` on a `Shape` that might be a `Rect` (after no
`match`), translates, and mypy (with a `sig`) or the run (`AttributeError`) rejects it.
`get` and `assoc` are special forms because they take a field's name, not a value (Candy
can't name a field). From `doc/archive/leaks_imvp_py_translator.md`, `doc/archive/leaks_pre_self_host.md` ("`get` after
`match`"), `doc/archive/leaks_symbol_table.md` and `doc/archive/leaks_executable_spec.md`.

## Notes

- 2026-10-29, type-checker step 3: `get` and `assoc` name a field of the record, or a
  field every variant of a sum has (`check.cdy`): `(deft V ((x Int))) (put (get (V 1) z))
  => get: V has no field z`, and `(put (get 1 x)) => get: Int has no fields`, rows of
  `[[checking.records]]`. A value typed `Any` is still unchecked ([[B18]]).
