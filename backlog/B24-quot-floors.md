# B24: `quot` rounds toward minus infinity

kind: leak
state: open
priority: normal
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy_rt/spelling.py`
refs: [[expr.arithmetic]]

`(quot -7 2)` is `-4`, as Python's `//`; C, Java and Rust truncate (`-3`). Fix: decide
what Candy's is, and spell it per target. From `doc/archive/leaks_executable_spec.md`.
