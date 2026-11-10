# B176: Host records: a built-in type with fields

kind: idea
state: open
priority: low
found: collections step 3's review, 2026-11-09
fixed:
where: `src/cdy/system.cdy`, `src/cdy/core.cdy`, `src/cdy_rt/spelling.py`
refs: [[types.records]], [[types.exist]], [[B175]]

A built-in type (`system.cdy`'s bodiless `deft`) has no fields, so a host value that is a
record, such as `py-spellings`' `Spelling` (a Python `NamedTuple`: `py`, `kind`,
`value`), is a tuple to Candy, read by position ([[B175]]). A `deft` with fields in
`system.cdy`, spelled as the host's class (`cdy_rt.spelling.Spelling`), would let
`get` read it by name, `(get s kind)`, and the checker type its fields.

## Notes

- 2026-11-09, Claude: filed with [[B175]] (option B there), bigger than its problem.
