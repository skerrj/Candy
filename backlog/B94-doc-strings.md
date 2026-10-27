# B94: Doc strings and other metadata

kind: idea
state: open
priority: low
found: macros, 2026-10-18
fixed:
where:
refs: [[syntax.comments]]

How should a definition carry its documentation, and other data about it? Today docs are
`;;` comments, which the reader drops.

- **Where a doc string goes:** in the definition (`(defn f (x) "doc" body)`, though `defn`
  takes one body form), on the `sig` (`(sig f "doc" (Fn (Int) Int))`), or a comment
  directly above a definition?
- **General metadata,** as Clojure's `^{...}` maps: a doc string as one key among others
  (deprecated, inline, test, since), with a reader shorthand, joining the reader macros
  planned for `'`.
- **Who reads it:** a doc generator, the editor (hover), the translator (an inline or
  deprecated flag), macros, and what a module exports. Forms already carry one piece of
  metadata, `Pos`.

From `doc/brainstorm.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an idea to think about later.
