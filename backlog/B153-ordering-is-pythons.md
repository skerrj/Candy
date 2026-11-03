# B153: `<` and the other orderings are Python's on anything but numbers and strings

kind: leak
state: open
priority: low
found: semantics step 3, 2026-11-02
fixed:
where: `src/cdy/check.cdy`
refs: [[expr.comparisons]], [[expr.equality]]

The checker makes a comparison's arguments one type, but for `<`, `>`, `<=` and `>=` not
which types: on records and lists Python compares tuples item by item (`(< (V 1) (V 2))`
is `true`, `(< (List 1 2) (List 1 3))` too), on `Bool`s `false` is before `true`, and on
`nil` it fails when run (`TypeError: '<' not supported between instances of 'NoneType'
and 'NoneType'`). Fix: decide which types are ordered (numbers, strings, `Char`; lists
and records item by item, as Haskell's derived `Ord`, or not at all until interfaces),
and check it.
