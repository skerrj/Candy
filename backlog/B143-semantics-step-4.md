# B143: semantics step 4: `Maybe` a sum, missing values gone

kind: task
state: open
priority: normal
found: semantics, 2026-11-02
fixed:
where: `src/cdy/prelude.cdy`, `src/cdy/check.cdy`, `spec/`
refs: [[B20]], [[B21]], [[B138]]

Step 4 of `doc/hl_rqmt/semantics.md`. `(deft (Maybe a) (Some ((v a))) (None))` in the prelude (Question 6); the checker's `Maybe` rules out; `find`, `index-of` and `with-default` on the sum; an `if` or `cond` without `else` only for `Unit` (Question 7, for now: [[B138]]).
