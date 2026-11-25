# B233: test-runner step 1: `catch-panic` and `capture-output`

kind: task
state: done
priority: normal
found: test-runner, 2026-11-25
fixed: test-runner, 2026-11-25
where: `src/cdy/translator.cdy`, `src/cdy_rt/spelling.py`, `src/cdy_rt/primitives.py`
refs: 

Step 1 of `doc/hl_rqmt/test_runner.md`. Two translator built-ins ([[B139]]; Questions 2 and 3): `catch-panic`, `(Fn ((Fn (Unit) a)) (Result a String))`, and `capture-output`, `(Fn ((Fn (Unit) a)) (Tup a String))`; `translator.cdy`, `spelling.py`, `primitives.py`, with the runtime's tests; [[library.builtins]] (the translator's seven).

## Notes

- 2026-11-25, Claude: filed on the HLD's acceptance (the owner, 2026-11-25).
- 2026-11-25, Claude: built (the HLD's step 1, "Done"): `catch-panic` Candy over
  `run-caught`.
- 2026-11-25, the owner: ticked in review.
