# B27: `=` is Python's `==`

kind: leak
state: done
priority: normal
found: py-py-translator, 2026-10-15
fixed: semantics
where: `src/cdy_rt/spelling.py`
refs: [[expr.comparisons]], [[B29]]

Equality is structural, and across types: `1 == 1.0` is true, and so are a `Tup`, a `List`
and a record with the same items ([[B29]]). From `doc/archive/leaks_imvp_py_translator.md`.

## Notes

- 2026-11-02, Claude: semantics step 3: `=` is structural on one type ([[expr.equality]], *lasting*): the checker already makes both sides one type, and records and variants now compare their class too ([[B137]]), so a record isn't equal to a tuple with its fields, even through `Any`. A `Tup` and a `List` with the same items, met through `Any`, are still equal (both Python tuples): [[B18]]'s.
