# B141: semantics step 2: `show`, and the `List` and `Tup` constructors

kind: task
state: review
priority: normal
found: semantics, 2026-11-02
fixed: semantics
where: `src/cdy/system.cdy`, `src/cdy/emit.cdy`, `src/cdy_rt/`, `spec/`
refs: [[B36]]

Step 2 of `doc/hl_rqmt/semantics.md`. Every type's name is its constructor (`List` and `Tup` variadic built-ins, `tup` an alias for now); `show` gives a value as its constructor applied to its parts (Question 2), by its static type, a type variable an error (Question 3) and `Any` the run-time show; `put` and `format` write text unquoted; the spec's examples print anything ([[B36]]).

## Notes

- 2026-11-02, Claude: built; see the HLD's step 2 *Done* note. [[B36]] done; [[B150]], [[B151]] and [[B152]] added.
