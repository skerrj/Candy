# B31: A top-level value used before its `def` fails at run time

kind: leak
state: open
priority: normal
found: executable-spec, 2026-10-24
fixed:
where: `src/cdy/core.cdy`
refs: [[types.sig]]

A function can call one defined after it, but a value is only there once its `def` has
run, so using it earlier fails with Python's `NameError`. Fix: a definition-order check
for values. From `doc/archive/leaks_executable_spec.md`.
