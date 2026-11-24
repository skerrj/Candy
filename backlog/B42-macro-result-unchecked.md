# B42: A macro's result isn't checked to be a `Form`

kind: leak
state: review
priority: normal
found: macros, 2026-10-18
fixed: host-macros, 2026-11-23
where: `src/cdy_rt/primitives.py` (`call_macro`)
refs: [[macros.defmacro]]

Macro code runs without mypy, so a macro that returns, say, an `Int` gives a confusing
error (or none) later. Fix: Candy's type checker; meanwhile `call_macro` could check the
result's class. From `doc/archive/leaks_macros.md`.
- 2026-11-23, Claude: macro code type-checked before it runs on the interpreter
  (`host-macros` step 2, [[macros.checked]]): a macro is `(Fn ((List Form)) Form)`, so
  a result that isn't a `Form` is an error at the `defmacro` (`defmacro m: expected
  Form, got Int`). What a form contains is still checked at the call, in the expansion
  ([[B232]]).
