# B49: Host objects have no Candy type

kind: leak
state: open
priority: normal
found: system-prelude, 2026-10-19
fixed:
where: `src/cdy/translator.cdy`
refs: [[library.builtins]], [[checking.any]]

`translator.cdy`'s `module-dir` takes a host function, the one whose module's directory it
gives, so it is typed `(Fn (Any) String)`. Fix: opaque types. From
`doc/archive/leaks_system_prelude.md` ("Built-ins typed `Any`").

## Notes

- 2026-11-16, Claude: narrowed to the macros (library-layers step 4, [[B202]]): the
  regular expressions were dropped ([[B32]]). `where`, `refs` and the text were:

  ```text
  where: `src/cdy/system.cdy`
  refs: [[library.builtins]], [[library.strings]]

  The regular expressions return Python's match and pattern objects, and macros are Python
  functions, so their built-ins are typed `Any`. Fix: opaque types. From
  `doc/archive/leaks_system_prelude.md` ("Built-ins typed `Any`").
  ```
- 2026-11-24, Claude: narrowed to `module-dir` (`host-macros`): a macro is a Candy
  function, `(Fn ((List Form)) Form)`, `call-macro` is generic (step 1), and
  `load-macros` is gone (step 6b). The text was:
  ```text
  Macros are Python functions, so the built-ins that take or give one (`translator.cdy`'s
  `load-macros`, `call-macro` and `module-dir`) are typed `Any`. Fix: opaque types. From
  `doc/archive/leaks_system_prelude.md` ("Built-ins typed `Any`").
  ```
