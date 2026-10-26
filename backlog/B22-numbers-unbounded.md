# B22: `Int`, `Long` and `Byte` are unbounded; `Float` is 64-bit

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/emit.cdy`, `doc/hl_rqmt/multi_target.md`
refs: [[syntax.numbers]], [[expr.arithmetic]]

All three integer types are Python `int`s, and `Float` is a 64-bit `float` like `Double`,
with no range checks (`300b` is accepted). A second target will have sizes. From `doc/archive/leaks_imvp_py_translator.md`
("Numbers").
