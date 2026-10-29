# B15: Types are checked by mypy, not by Candy

kind: leak
state: in-progress
priority: high
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/core.cdy`, `src/cdy/emit.cdy`
refs: [[types.checking]], [[expr.unit]]

`sig`s become Python annotations and `mypy --strict` checks the translation; Candy has no
type checker of its own. So a type error, an unknown type name, a value called as a
function, or using a `Unit` value (`(put (put 1))`) translates, and only mypy or the run
rejects it; and what mypy can't see, because Python's types are looser than Candy's
(`Char` and `String` are both `str`), nothing checks. Fix: Candy's type checker. From
`doc/archive/leaks_imvp_py_translator.md` ("Type checking in the iMVP", "Using a `Unit` value") and
`doc/archive/leaks_executable_spec.md` ("What the translator doesn't check").

## Notes

- 2026-10-26, the owner: `high` in triage ([[B103]]): the root of [[B18]], [[B19]], [[B25]], [[B30]], [[B42]], [[B51]], [[B53]].
