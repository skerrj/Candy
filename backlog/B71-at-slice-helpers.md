# B71: The `at` and `slice_` helpers are only used as values

kind: tech-debt
state: done
priority: low
found: pre-self-host, 2026-10-17
fixed: semantics-2
where: `src/cdy_rt/primitives.py`
refs: [[B35]]

Since `at` and `slice` are emitted as subscripts ([[B35]]). They still return
`object`/`Sequence`, so passing them as values loses the element type. From `doc/tech_debt.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): cosmetic or harmless.
- 2026-11-06, Claude: fixed in `semantics-2` step 2: the helpers are every `at` and
  `slice` call now, but an `at` on a literal index ([[library.bounds]]); `at` keeps the
  item's type, and `slice_` its argument's (a string's slice is a `str`, a list's a
  `tuple`), so passing them as values keeps it too.
