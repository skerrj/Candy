# B171: `List` isn't a value

kind: leak
state: open
priority: low
found: collections step 1, 2026-11-08
fixed:
where: `src/cdy/core.cdy` (`BUILTIN_CONSTRUCTORS`), `src/cdy/system.cdy`, `src/cdy_rt/spelling.py`
refs: [[types.constructors]], [[expr.rest]], [[B161]]

`(List item*)` is the analyser's own constructor (a `ListOf` node), typed as `(Fn ((Rest
a)) (List a))` would be, so `List` alone, as a value, is an unknown name: `(put List)`
fails with `unknown name List`. A record's or variant's constructor is a value; `List`'s
isn't (*for now*, `doc/hl_rqmt/collections.md`, step 1).

An ordinary built-in, `(sig List (Fn ((Rest a)) (List a)))`, needs one name to be both a
built-in type and a built-in value: the built-ins map (`Builtin`) and `spelling.py` have
one entry per name, and `List`'s is its type's. It would gain little: by [[expr.rest]]'s
value rule, `List` as a value is the function of its arguments before the rest, an `(Fn
() (List a))`, so `(map List xs)` wouldn't wrap each item. `Tup` can't be one at all (its
type is its number of items).

Fix: when the symbol table next changes (`namespaces`), a built-in name that is a type
and a value, with a spelling for each, and the call kept a Python tuple literal.

## Notes

- 2026-11-08, the owner: keep `List` the analyser's constructor in step 1 (option A).
