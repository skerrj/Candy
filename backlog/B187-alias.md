# B187: `alias`, a renaming at translation time, for modules, types and values

kind: idea
state: open
priority: normal
found: namespaces (HLD), 2026-11-12
fixed:
where: `src/cdy/core.cdy`, `src/cdy/special.cdy`
refs: [[programs.import]], [[B40]], [[B171]]

One special form, `(alias new old)`, giving anything a name stands for a second name:

```text
(alias u lib/util)                 ; a module's qualifier: u/greet
(alias Point (Tup Double Double))  ; a type synonym
(alias (Pair a) (Tup a a))         ; a generic one
(alias sum-all total)              ; a function or value
(alias out text)                   ; a shadowed built-in, reached again
```

Resolved in analysis, with nothing in the output, so every target has it as it is. Types
and values share one namespace (`python_complete.md`, Question 10), so an alias is one
more name there, under the same clash and shadowing rules. It gives Candy type synonyms
(Haskell's and Rust's `type`), and takes the place of an alias in `import`, which
`namespaces` leaves out: two modules with one stem (`util`, `lib/util`), or a long stem.

What its design settles: whether `old`'s form (a module path, a type, a value) decides
the kind; a module alias living where qualifiers do, since a module isn't a value; a
generic type alias's parameters, as a `deft`'s; aliases and private names (exported?
of a private name?); messages naming the alias as written, so the checker's types keep
it for display; macros, not aliasable while they are global.

## Notes

- 2026-11-12, the owner: in the `namespaces` HLD's review, an alias for more than module
  names, a special form of its own, later; `import` gets none. Claude: filed. Where it
  goes: after `namespaces`, before `library` (whose modules make long stems), or with
  interfaces (where type synonyms matter most).
