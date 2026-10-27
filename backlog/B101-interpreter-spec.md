# B101: An interpreter, and what it does to the spec

kind: idea
state: open
priority: low
found: executable-spec, 2026-10-24
fixed:
where:
refs:

(From *dump*: interpreter, repl, jit; 2026-10-24.) The spec's examples vs the programs in
`tst/cdy/` isn't a cost line, so an interpreter wouldn't erase it: an example states one
rule, and the programs test whole things (modules, `main` with arguments, macro files,
the self-host), integration tests (`doc/hl_rqmt/executable_spec.md`, question 11). What it
would change:

- REPL-style examples (`> (+ 1 2)` then `3`), an expression at a time, like doctests;
- a printer in Candy syntax (question 12's deferred show built-in), retiring the
  numbers-and-text rule;
- a second implementation: every example runs on both, and the spec becomes a conformance
  suite (as for more targets, `doc/hl_rqmt/multi_target.md`).

It wouldn't type-check: until Candy has a checker, mypy on the translation is the check.
A JIT is speed only, and speed isn't the problem (the whole suite is about 20 s). From `doc/brainstorm.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an idea to think about later.
