# B148: semantics step 9: errors: panics and `Result`

kind: task
state: open
priority: normal
found: semantics, 2026-11-02
fixed:
where: `src/cdy/prelude.cdy`, `spec/60-library.md`
refs: [[B39]], [[B139]]

Step 9 of `doc/hl_rqmt/semantics.md`. `fail` a panic; `(deft (Result a e) (Ok ((v a))) (Err ((err e))))` in the prelude (Question 11; `catch-panic` left to `test-runner`: [[B139]]).
