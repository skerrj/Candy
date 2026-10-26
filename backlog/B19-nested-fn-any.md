# B19: A nested `fn` gets `Any` annotations

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/emit.cdy`
refs: [[expr.functions]]

`sig` covers only top-level definitions, so a `fn` that has to become a nested Python
`def` gets `Any` annotations, for `mypy --strict` to accept it. Fix: Candy infers types.
From `doc/archive/leaks_imvp_py_translator.md`.
