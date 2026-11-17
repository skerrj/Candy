# B196: A type with the same name as a built-in type can't be shown

kind: defect
state: review
priority: low
found: namespaces step 6, 2026-11-14
fixed: library-layers, 2026-11-16
where: `src/cdy/emit.cdy`, `src/cdy_rt/primitives.py`
refs: [[programs.shadowing]], [[library.show]]

A file may define a type with the same name as a built-in type ([[programs.shadowing]]),
but `show` reads a type by its name, as `emit` writes it (`show-type`): the top module's
`Map` is `'Map'`, the built-in's too, so `cdy_rt`'s `show` takes the record for a map and
fails (`AttributeError: 'Map' object has no attribute 'items'`). Another module's type is
prefixed (`'util__Map'`), so only the top module's (and macro code's) is hit. Before
`namespaces` step 6, when the checker and `emit` read a type by its name alone, the
program didn't translate to valid Python at all (a `SyntaxError`); since then the module
is in Core, so only `show` is left. Fix: `show-type` writes a program's type so that no
built-in's name can be it.

## Notes

- 2026-11-16, Claude: fixed by `library-layers` step 3 ([[B201]]): a built-in type's
  module is `system` in Core, so `show-type` (`emit.cdy`, `show-name`) writes a built-in
  type by its name (`'Map'`) and a program's with its module (`'main.Map'`, or `'.Map'`
  in a module with no stem: a program read from text, or macro code), which no built-in's
  name can be.
  Its example is now [[library.show]]'s. The `## Repro` section it replaced, removed from
  this item (it ran as a strict expected failure until the fix):

  ````text
  ## Repro

  The program should print its record:

  ```candy run
  (deft Map ((x Int)))
  (sig m Map)
  (def m (Map 1))
  (put (get m x))
  (put m)
  ```
  ```expect
  1
  (Map 1)
  ```
  ````
