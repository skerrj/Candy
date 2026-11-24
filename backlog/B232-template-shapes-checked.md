# B232: A `quasi` template's special forms checked against their shapes

kind: idea
state: open
priority: low
found: host-macros, 2026-11-23
fixed:
where: `src/cdy/core.cdy`, `src/cdy/syntax.cdy`
refs: [[macros.quoting]], [[macros.errors-at-call]], [[B156]], [[B42]]

What a macro returns is a `Form`, a syntax tree, so checking macro code (`host-macros`
step 2, [[B42]]) checks that a macro returns a form, not what the form says: a template
with a mistake in it, `(quasi (if (unq test)))` missing its `then`, is found only when
something calls the macro, reported at the call in the expansion's words ([[B156]]).

`syntax.cdy` already declares each special form's shape (`special.cdy`: `if`'s test,
then and optional else; `let`'s bindings; `import`'s list). When a `quasi` template is
analysed, its special forms could be checked against them at the `defmacro`, an
`(unq e)` counted as one form and an `(unq-sp e)` as any number: a wrong number of
parts, or a malformed binding, then an error at the template, where the macro's author
wrote it. It checks shapes only: not types, not an ordinary function's arguments, and
nothing that depends on what fills the holes, which stay checked at each use.

## Notes

- 2026-11-23, the owner: from the `host-macros` step 2 discussion
  (`doc/hl_rqmt/host_macros.md`, "What checking macro code checks"); filed for later,
  with the typed-code option in `doc/brainstorm.md`.
