# B104: `up`, `down`, `down*` and `meta-template` for the quoting forms

kind: idea
state: open
priority: low
found: macros, 2026-10-18
fixed:
where: `src/cdy/special.cdy`, `src/cdy/expand.cdy`
refs: [[macros.quoting]]

A straight replacement of the quoting forms' names, naming the direction between levels
(stages, as in MetaML) rather than the mechanism:

| New | Replaces | Lisp |
|---|---|---|
| `up` | `quo` | quote, `'` |
| `meta-template` | `quasi` | quasiquote, `` ` `` |
| `down` | `unq` | unquote, `,` |
| `down*` | `unq-sp` | unquote-splicing, `,@` |

`up` lifts code a level with no holes; a `meta-template` is code a level up, with holes;
`down` goes back down a level and evaluates there, and `down*` splices the result into the
list around it. Same meaning as today's forms, new names only. From `doc/brainstorm.md`,
and the owner's side conversation ([[B82]]).
