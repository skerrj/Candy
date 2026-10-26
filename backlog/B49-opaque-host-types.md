# B49: Host objects have no Candy type

kind: leak
state: open
priority: normal
found: system-prelude, 2026-10-19
fixed:
where: `src/cdy/system.cdy`
refs: [[library.builtins]], [[library.strings]]

The regular expressions return Python's match and pattern objects, and macros are Python
functions, so their built-ins are typed `Any`. Fix: opaque types. From
`doc/archive/leaks_system_prelude.md` ("Built-ins typed `Any`").
