# B48: Operators, `tup` and `put` have no Candy type

kind: leak
state: open
priority: normal
found: system-prelude, 2026-10-19
fixed:
where: `src/cdy/special.cdy`, `src/cdy/system.cdy`
refs: [[expr.operator-arity]], [[library.builtins]], [[types.tuples]], [[B99]]

A `Fn` type can't say "two or more arguments" (or any number), so the arithmetic and
comparison operators are `(op name variadic)` in `special.cdy` with no type, `tup` is a
special form, and `print`, `display` and `put` are typed `Any` in `system.cdy`, with no
arity check. `not` is a one-argument function, typable today. Fix: variadic types
([[B99]]), then move what they let be typed into `system.cdy`. From
`doc/archive/leaks_system_prelude.md` ("Operators have no Candy type", "Built-ins typed
`Any`") and `doc/archive/leaks_symbol_table.md`.
