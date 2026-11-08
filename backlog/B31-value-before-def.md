# B31: A top-level value used before its `def` fails at run time

kind: leak
state: done
priority: normal
found: executable-spec, 2026-10-24
fixed: semantics-2
where: `src/cdy/check.cdy`
refs: [[types.sig]]

A function can call one defined after it, but a value is only there once its `def` has
run, so using it earlier fails with Python's `NameError`. Fix: a definition-order check
for values. From `doc/archive/leaks_executable_spec.md`.

## Notes
- 2026-11-06, Claude: fixed in `semantics-2` step 3: a `def`'s initial value and a
  top-level expression may use only the top-level names defined before them, values,
  functions and constructors alike, and those that the bodies of the functions they use
  reach (`check-order` in `check.cdy`; [[programs.def-order]]): `y is used before its
  def, through f`. A function's own body can still use any name.
