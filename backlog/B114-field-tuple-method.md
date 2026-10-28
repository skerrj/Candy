# B114: A field named like a tuple method fails mypy

kind: leak
state: open
priority: low
found: field-checks, 2026-10-27
fixed:
where: `src/cdy/emit.cdy`
refs: [[types.records]], [[B29]]

A record is a `NamedTuple`, so a field named `count` or `index` overrides `tuple`'s
method: `(deft V ((count Int)))` translates and runs, but fails `mypy --strict`
("Incompatible types in assignment (expression has type "int", base class "tuple"
defined the type as "Callable[[Any], int]")"). Fix: with [[B29]] (records that aren't
tuples), or reject the names as [[B113]] does a leading `_`.
