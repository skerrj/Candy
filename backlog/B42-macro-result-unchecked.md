# B42: A macro's result isn't checked to be a `Form`

kind: leak
state: open
priority: normal
found: macros, 2026-10-18
fixed:
where: `src/cdy_rt/primitives.py` (`call_macro`)
refs: [[macros.defmacro]]

Macro code runs without mypy, so a macro that returns, say, an `Int` gives a confusing
error (or none) later. Fix: Candy's type checker; meanwhile `call_macro` could check the
result's class. From `doc/archive/leaks_macros.md`.
