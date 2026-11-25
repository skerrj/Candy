# B224: Expand and include as one loop

kind: idea
state: open
priority: low
found: host-macros, 2026-11-22
fixed:
where: `src/cdy/include.cdy`, `src/cdy/expand.cdy`, `src/cdy/cdyc.cdy`
refs: [[B44]], [[programs.import]], [[macros.import-macros]], [[macros.defmacro]]

The translator reads a program in a fixed order: read, `include` (every `import` and
`import-macros` resolved, every module read), expand (every `defmacro` collected, then
every call expanded), analyse. So nothing a macro returns can add a module or a macro
([[B44]]). Racket and Clojure instead expand a module's top-level forms one at a time,
in order:

- each top-level form is expanded until its head is a special form;
- an `import` met then is resolved and its module read at that point, its names visible
  to the forms after it;
- an `import-macros` or a `defmacro` met then (written, or returned by a macro) loads
  its macros for the forms after it, not before;
- a top-level `do` is spliced as it is met ([[programs.top-do]]).

`include` and expand become one loop over a module's forms, with the module table and the
macros so far as its state. Questions it raises: whether a macro can be used above its
`defmacro` (today it can, since all are collected first; one at a time, it can't),
whether an import's position then matters for the names it brings, and cycles found
mid-module. It fits once macro files are modules (`doc/hl_rqmt/host_macros.md`, step 4),
whose module reading it would reuse. Then a macro can set up its user's imports: a
`(use-tests)` expanding into `(import test ())` and `(import-macros test_macros)`.

## Notes

- 2026-11-22, the owner: left out of `host-macros` (its HLD's Question 1), filed for
  later.
