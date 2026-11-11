# B175: A spelling is read by position, and `and`/`or` by name

kind: tech-debt
state: done
priority: low
found: collections step 3's review, 2026-11-09
fixed: collections, 2026-11-09
where: `src/cdy/core.cdy` (`spelling-kind`), `src/cdy/emit.cdy`, `src/cdy/lower.cdy`
refs: [[expr.operator-values]], [[expr.logic]], [[B165]], [[B173]], [[B176]]

`py-spellings` is a map of `(Tup String String String)`, Python's `Spelling` (`py`,
`kind`, `value`), and the translator reads it by position, `(at entry 0)` for the
Python text, `1` for the kind, `2` for an operator's value, in seven places
(`spelling-kind` in `core.cdy`; `emit-prim`, `emit-call`, `emit-tcon` in `emit.cdy`).
And `lower.cdy` knows `and` and `or` short-circuit by their names (`(tup "and" "or")`),
where the spelling's kind, `boolop`, says so.

Fix: accessors in `core.cdy`, `spelling-py`, `spelling-kind`, `spelling-value`, in place
of the positions; `lower` tests the kind. With `collections` step 5 ([[B165]]), which
touches the same files. The translator's other names: `"at"` for a `tup` pattern goes in
step 5, `"="`/`"!="` with [[B173]]; `"show"` stays (it needs its argument's type), and
`"not"` and `"++"`, calls the translator writes itself, are data. A record type for a
spelling is [[B176]].

## Notes

- 2026-11-09, the owner: asked, after step 3, whether the triple could have a type and
  the hard-coded names go; Claude: filed this and [[B176]], the owner leaving it to
  Claude's suggestion.
- 2026-11-09, Claude: fixed with [[B165]]: `spelling-py`, `spelling-kind` and
  `spelling-value` in `core.cdy`, each a `Tup` pattern on the entry, read a spelling in
  `emit-prim`, `emit-prim-call` and `emit-tcon`. `lower`'s `and`/`or` stay by name, not
  by the `boolop` kind: `lower` doesn't see the spellings, and short-circuiting is the
  language's ([[expr.logic]]), which any target's spelling must keep, not Python's.
