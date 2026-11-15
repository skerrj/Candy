# B108: The built-ins are one flat namespace

kind: idea
state: open
priority: normal
found: name-checks, 2026-10-26
fixed:
where: `src/cdy/system.cdy`, `src/cdy/prelude.cdy`
refs: [[library.builtins]], [[programs.import]], [[B47]], [[B95]], [[B97]]

`system.cdy` is one flat set of built-ins (`cos`, `split`, `map-get`, `slurp`, ...), and
every file sees all of them unqualified (`doc/hl_rqmt/library.md`: "one flat set of
built-ins that every file sees"). There is no `math` module to import, and no `math/cos`,
as Python's `import math; math.cos(x)` has. The idea: split the built-ins (and the prelude)
into library modules, `math`, `string`, `list`, `map`, `io`, imported and qualified like a
program's own once modules have qualified names ([[B47]]; `doc/hl_rqmt/modules.md`,
"After the MVP": `util/greet`), with a few (the prelude, perhaps the operators) seen
everywhere. It would shape the I/O refactor ([[B95]]) and a library per target
([[B97]]). Raised by the owner after `name-checks`.

## Notes

- 2026-11-14, Claude: `namespaces` gave modules qualified names (`m.name`, with `.`, not
  the `/` above, [[programs.qualified]]) and name lists, so the split this item wants is
  `library`'s to do; the built-ins stay one flat set, with no module, until then
  ([[B197]]: their module is `""` in Core, *for now*).
