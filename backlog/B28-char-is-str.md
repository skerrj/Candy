# B28: A `Char` is a one-character `str`

kind: leak
state: open
priority: low
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/emit.cdy`
refs: [[syntax.chars]]

Nothing stops a `Char` and a `String` being mixed: Python's `str` comparison lets a
`Char` (`(at text pos)`) be compared with a one-character `String`. From `doc/archive/leaks_imvp_py_translator.md` ("`Char`
is a one-character `str`", "Forms are `Any`").

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): matters once there is a second target.
