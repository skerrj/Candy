# B71: The `at` and `slice_` helpers are only used as values

kind: tech-debt
state: open
priority: low
found: pre-self-host, 2026-10-17
fixed:
where: `src/cdy_rt/primitives.py`
refs: [[B35]]

Since `at` and `slice` are emitted as subscripts ([[B35]]). They still return
`object`/`Sequence`, so passing them as values loses the element type. From `doc/tech_debt.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): cosmetic or harmless.
