# B139: A `catch-panic` for tools

kind: idea
state: open
priority: low
found: semantics HLD, 2026-11-02
fixed:
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
