# B29: Records and variants are `NamedTuple`s

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/emit.cdy`
refs: [[types.records]], [[match.sum-types]], [[types.tuples]]

Two `deft` types (records, or variants of different sums) with the same field values
compare equal, and a record or variant also behaves as a tuple (indexing, iterating,
unpacking, a `tup` pattern). mypy accepts a `(Tup Int Int)` (`tuple[int, int]`) where a
`(List Int)` (`tuple[int, ...]`) is expected. From `doc/archive/leaks_imvp_py_translator.md` ("Records are `NamedTuple`s",
"`tup` destructuring") and `doc/archive/leaks_pre_self_host.md` ("Sum types are Python
unions of `NamedTuple`s").
