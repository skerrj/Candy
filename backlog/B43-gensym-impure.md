# B43: `gensym` is impure

kind: leak
state: open
priority: low
found: macros, 2026-10-18
fixed:
where: `src/cdy_rt/primitives.py` (`fresh_name`)
refs: [[macros.gensym]]

A counter in the runtime, restarted when a program's macros are loaded: the only
built-in with state besides I/O. Fix: pass a counter through expansion, or take names from
a supply in the expansion's context. From `doc/archive/leaks_macros.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an easy workaround, or rare.
