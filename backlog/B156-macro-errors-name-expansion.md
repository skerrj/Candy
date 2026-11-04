# B156: An error in a macro's expansion names the expansion's forms

kind: idea
state: open
priority: low
found: semantics step 5, 2026-11-03
fixed:
where: `src/cdy/expand.cdy`, `src/cdy/check.cdy`
refs: [[macros.cond]], [[checking.if]], [[B155]], [[B42]]

A type error in a macro call's expansion is reported in the expansion's words: `(cond
(false 1))` says `if: with no else, the then is Int, not Unit`, naming an `if` the
program never wrote. The position is the call's (the forms a macro builds carry where
they came from), but the words are the expansion's. Ways to go: a macro's forms remember
the call they came from, and the checker names it (`cond: ...`, or `in cond: if: ...`);
or the messages that matter for the prelude's macros are written for them. Undecided:
how far it should go for user macros, whose expansions a user may want to see.
