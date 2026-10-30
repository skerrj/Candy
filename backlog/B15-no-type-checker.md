# B15: Candy's type checker is an MVP, with mypy as a second check

kind: leak
state: in-progress
priority: high
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/check.cdy`
refs: [[types.checking]], [[expr.unit]]

Candy has a type checker (`src/cdy/check.cdy`, `spec/25-checking.md`), an MVP. What it
leaves:

- **mypy still checks the Python** ([[types.checking]]): two checkers, which may disagree;
  a later branch decides whether mypy stays.
- **No let-polymorphism:** a `fn` bound by `let` has one type ([[checking.locals]]).
- **What is known when:** a `get` or `assoc` on a value whose type isn't known yet is an
  error, not a constraint solved later ([[checking.order]], [[B120]]).
- **No narrowing in a `match` clause:** the subject is still the sum there ([[B121]]).
- **One error:** translation stops at the first type error.

Items of their own: `Any` ([[B18]]), `Maybe` ([[B20]]), macro code ([[B42]]), the
nested `fn`s' types ([[B19]]). It said: "`sig`s become Python annotations and `mypy
--strict` checks the translation; Candy has no type checker of its own", from
`doc/archive/leaks_imvp_py_translator.md` ("Type checking in the iMVP", "Using a `Unit`
value") and `doc/archive/leaks_executable_spec.md` ("What the translator doesn't check").

## Notes

- 2026-10-26, the owner: `high` in triage ([[B103]]): the root of [[B18]], [[B19]], [[B25]], [[B30]], [[B42]], [[B51]], [[B53]].
- 2026-10-29, type-checker step 3: narrowed to what the checker leaves; it was "Types are
  checked by mypy, not by Candy".
- 2026-10-29, type-checker step 3: "what is known when" has its own item, [[B120]], and
  narrowing in a clause [[B121]].
