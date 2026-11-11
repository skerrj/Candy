# B170: Brackets for a list literal

kind: idea
state: open
priority: low
found: collections, 2026-11-07
fixed:
where: `src/cdy/read.cdy`
refs:

`[1 2 3]` as sugar for `(List 1 2 3)`, as Clojure's vector. Decided with the map's
literal and the reader macros (`'`), which may want the brackets for something else;
not in `collections` (`doc/hl_rqmt/collections.md`, Question 3, *for now*).

## Notes

- 2026-11-07, the owner: none now (Question 3).
- 2026-11-08, the owner: brainstormed quoting as the list literal, `(quo (1 2 3))` or
  `'(1 2 3)` a `(List Int)`, with no `List` constructor, as Lisp. Claude's notes, to
  weigh with the brackets: `quo` is already the macro form, a `Form` (code as data),
  which a statically typed list can't also be; a quote doesn't evaluate its items
  (`'(1 x)` holds the name `x`), so a computed list still needs a constructor (or
  `quasi` and `unq`), as Lisp keeps `list` beside `'`; and `semantics` made the type's
  name its constructor, *lasting* ([[types.constructors]]), which this would reopen.
