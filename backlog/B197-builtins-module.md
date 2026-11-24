# B197: The built-ins' module, and macro code's

kind: idea
state: review
priority: low
found: namespaces step 6's review, 2026-11-14
fixed: host-macros, 2026-11-23
where: `src/cdy/core.cdy`, `src/cdy/check.cdy`, `src/cdy/emit.cdy`
refs: [[B42]], [[B45]], [[programs.qualified]]

Since `namespaces` step 6, Core carries each name's module, and `""` is "no module" for
two things: a built-in type (`(TCon "" "Int" ...)`, declared by `system.cdy`, which no
program imports), and macro code (a macro program is analysed on its own, with module
`""`, and quoting makes `(Global "" "Sym" ...)`). Inside the checker and `emit` a name's
key is `global-key`, so a macro program's own type `Map` has the built-in `Map`'s key.
Harmless *for now*: macro code isn't checked ([[B42]]), and its Python was already
unprefixed.

What settling it needs:

- the built-ins' module or modules, which `library` decides (one `system`, or `list`,
  `string`, `map`), and whether a program can qualify them (`system.map`); every check
  for a built-in type (`is-any`, `is-rest`, `returns-unit`, the constraints) then reads
  it, and `emit` spells it through `spelling.py`;
- macro code's own module, when it is checked ([[B42]]) or runs on the host ([[B45]]).

## Notes

- 2026-11-14, the owner: in step 6's review, not now, written down *for now*. Claude:
  filed.
- 2026-11-16, Claude: its first half done by `library-layers` step 3 ([[B201]]): a
  built-in type's module is `system` in Core (`SYSTEM`, `core.cdy`), and every built-in
  is `system.name` too ([[programs.sees]]); `emit` spells a `system` type through
  `spelling.py`, and `show` tells a program's `Map` from the built-in's ([[B196]]). Macro
  code's module stays `""`: the second half, with [[B42]] and [[B45]].
- 2026-11-23, Claude: its second half done by `host-macros` step 4a: a macro file's code
  is of its own module, its stem, and a file's own defmacros of `""`, as a top module's
  names have no prefix; `form` is a module, so quoting builds `form.Sym` (`core.cdy`'s
  `FORM`).
