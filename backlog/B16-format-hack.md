# B16: `format` is an f-string hack, from smz

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/core.cdy`, `src/cdy/special.cdy`
refs: [[library.format]], [[B36]]

`(format "x: {x} sum: {(+ x y)}")` is read as one string, and the translator finds each
`{...}` hole in it, reads the hole's text as one Candy form, and joins the parts. So a
hole is not real syntax: a `}` inside a string inside a hole ends the hole early, a hole
can't hold a nested `format`, and errors in a hole can't point inside it. Literal braces
are `{{` and `}}`, as in Python. `format` is a special form only because its holes are
forms in a string (`doc/archive/leaks_symbol_table.md`). How a value is shown is
[[B36]]. Fix: holes as part of the grammar, or a reader macro, or a macro.
From `doc/archive/leaks_imvp_py_translator.md` ("`format` (from smz)").
