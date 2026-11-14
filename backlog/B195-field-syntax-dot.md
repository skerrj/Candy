# B195: Field syntax with `.`, and a local named like a qualifier

kind: idea
state: open
priority: normal
found: namespaces (step 2's review), 2026-11-13
fixed:
where: `src/cdy/core.cdy`, `src/cdy/read.cdy`
refs: [[programs.qualified]], [[checking.records]], [[syntax.names]]

Candy reads a field only as `(get p x)`. A field syntax with `.`, `p.x`, would share the
`.` with qualified names, `m.x` (the `namespaces` HLD, Questions 3 and 8), as Python,
Java and OCaml do. Candy resolves names statically, so `a.b` can be module `a`'s `b` when
`a` is an import's qualifier, and value `a`'s field `b` when `a` is a value (the checker
already solves a `get` on a value of unknown type, a field constraint).

What its design settles:

- a local named like an imported module's qualifier: an error (proposed, so `a.b` never
  means two things in one file), or the local wins (Python's, but a module's names are
  then out of reach there);
- chains, read left to right: `m.p.x`, module `m`'s `p`, then its field `x`;
  `p.q.x`, fields of fields;
- errors that name both readings: `p.x` with `p` neither a value nor an import;
- a field on a call's result, `(f 1).x`, if any, or only on a name;
- whether `p.x` is only reading, and `assoc` stays the way to write one.

## Notes

- 2026-11-13, the owner: in `namespaces` step 2's review, the qualifier's separator
  became `.`, and field syntax needs this rule when it comes. Claude: filed.
