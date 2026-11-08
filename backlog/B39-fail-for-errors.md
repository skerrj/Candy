# B39: `fail` stands in for errors

kind: leak
state: done
priority: normal
found: pre-self-host, 2026-10-17
fixed: semantics-2
where: `src/cdy_rt/primitives.py`, `src/cdy/prelude.cdy`
refs: [[library.builtins]], [[library.errors]]

Candy has no exceptions; `(fail "msg")` raises `CandyFail` from the runtime, and its
result is typed as anything (`NoReturn`). From `doc/archive/leaks_pre_self_host.md`.

## Notes

- 2026-11-06, Claude: fixed in `semantics-2` step 4: `fail` is a panic, *lasting*, which
  Candy can't catch: a program stops with `candy: ` and the message, and exits with 1,
  with or without `main` (`panic_hook` and `stop_on_panic` in `primitives.py`, called
  first by every translated program); an expected failure is the prelude's `Result`
  ([[library.errors]]). Python's other errors are [[B160]].
