# B10: A record constructor's number of arguments isn't checked

kind: defect
state: done
priority: normal
found: executable-spec, 2026-10-24
fixed: type-checker
where: `src/cdy/core.cdy`
refs: [[types.records]], [[match.constructors]], [[checking.records]]

`(V 1 2)` for a one-field record translates, and fails only in mypy or at run time
(`TypeError`); a variant's constructor is checked ("(C ...) takes 1 field(s), got 2").
From `doc/archive/leaks_executable_spec.md`; the audit's defect 9 (`doc/hl_rqmt/tracking.md`).

## Notes

- 2026-10-29, type-checker step 3: the type checker checks a record constructor's
  arguments (`check.cdy`), with the message a variant's had. The repro is now this row of
  `[[checking.records]]`: `(deft V ((x Int))) (put (get (V 1 2) x)) => (V ...) takes 1
  field(s), got 2`.
