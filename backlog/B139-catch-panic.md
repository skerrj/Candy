# B139: A `catch-panic` for tools

kind: idea
state: done
priority: low
found: semantics HLD, 2026-11-02
fixed: test-runner, 2026-11-25
where: `src/cdy/system.cdy`, `src/cdy_rt/primitives.py`
refs: [[B39]]

The semantics HLD (Question 11) makes `fail` a panic, which Candy can't catch, and an
expected failure a `Result`. A runner written in Candy (the epic's `test-runner`) then
can't catch the translator's panics: each `candy error` example runs as its own process,
slow for hundreds of examples. A narrow built-in, `(catch-panic f)`, running `f` and
giving `(Ok v)` or `(Err msg)` with the panic's message, documented as for test runners
and REPLs and not for program logic, would let it run them in-process with the
translator unchanged (Rust's `std::panic::catch_unwind`, Go's `recover`). For
`test-runner` to take up if the process cost bites.

## Notes

- 2026-11-02, the owner: noted with Question 11's answer, panic and `Result`.
- 2026-11-25, Claude: taken up by `test-runner` (`test_runner.md`, Question 2, the owner's
  answer): `catch-panic` in `translator.cdy`, for tools, step 1 ([[B233]]).
- 2026-11-25, Claude: built in `test-runner` step 1: `translator.catch-panic`, Candy over
  the host's `run-caught`, for tools; a program reaches it only by importing
  `translator`.
- 2026-11-25, the owner: ticked in review.
