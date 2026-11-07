# B153: `<` and the other orderings are Python's on anything but numbers and strings

kind: leak
state: done
priority: low
found: semantics step 3, 2026-11-02
fixed: semantics-2
where: `src/cdy/check.cdy`
refs: [[expr.comparisons]], [[expr.equality]]

The checker makes a comparison's arguments one type, but for `<`, `>`, `<=` and `>=` not
which types: on records and lists Python compares tuples item by item (`(< (V 1) (V 2))`
is `true`, `(< (List 1 2) (List 1 3))` too), on `Bool`s `false` is before `true`, and on
`nil` it fails when run (`TypeError: '<' not supported between instances of 'NoneType'
and 'NoneType'`). Fix: decide which types are ordered (numbers, strings, `Char`; lists
and records item by item, as Haskell's derived `Ord`, or not at all until interfaces),
and check it.

## Notes
- 2026-11-06, Claude: fixed in `semantics-2` step 1: the orderings take a number type,
  `String` or `Char`, anything else an error ([[checking.operators]]); lists and records
  aren't ordered until interfaces ([[B124]]).
