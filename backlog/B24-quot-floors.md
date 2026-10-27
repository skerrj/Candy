# B24: `quot` rounds toward minus infinity

kind: leak
state: kept
priority: normal
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy_rt/spelling.py`
refs: [[expr.arithmetic]]

`(quot -7 2)` is `-4`, as Python's `//`; C, Java and Rust truncate (`-3`). Fix: decide
what Candy's is, and spell it per target. From `doc/archive/leaks_executable_spec.md`.

## Notes

- 2026-10-26, the owner: kept in triage ([[B103]]): rounding down is Candy's rule, as Haskell's `div`;
  `spec/40-expressions.md` states it as lasting, and a target that truncates spells it
  otherwise.
