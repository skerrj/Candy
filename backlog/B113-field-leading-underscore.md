# B113: A field can't start with `_`, because Python's `NamedTuple` can't

kind: leak
state: open
priority: low
found: field-checks, 2026-10-27
fixed:
where: `src/cdy/emit.cdy`
refs: [[types.records]], [[B5]], [[B29]]

A record's or variant's field whose Python name starts with `_` (`_x`, `-x`, or `?x`,
which is `_px`) is an error, `V: field _x can't start with _ in Python (_x)`
(`check-py-fields`), because a `NamedTuple` forbids it. The limit is Python's, not
Candy's. Fix: mangle field names apart from other names (`f_x`), or stop spelling records
as `NamedTuple`s ([[B29]]).
