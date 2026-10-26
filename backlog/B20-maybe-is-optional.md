# B20: `(Maybe a)` is `a | None`

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/system.cdy`, `src/cdy_rt/primitives.py`
refs: [[types.names]], [[library.lists]], [[B25]], [[B51]]

A `Maybe` is Python's `Optional`, not a sum to be unwrapped: mypy's narrowing
(`if x is not None`) is all there is, and `nil` tests use truthiness
([[B25]]). So `(Maybe (Maybe a))` collapses: `find` and `index-of` return `None` for
"not found", which is also what a list of `Maybe`s holds for "nothing", and `with-default`
takes either as missing. Fix: a real sum, `(deft (Maybe a) (Nothing) (Just ((val a))))`,
once Candy's types are its own. From `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_library.md`. Related:
[[B51]].
