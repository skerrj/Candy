# B11: A `deft` variant named like a macro isn't rejected

kind: defect
state: open
priority: normal
found: macros, 2026-10-18
fixed:
where: `src/cdy/expand.cdy`
refs: [[macros.names]], [[match.sum-types]], [[B61]]

A macro's name can't be bound or defined, but a variant can take it:
`(defmacro M (a) a) (deft S (M ((x Int))))` translates, and a later `(M 1)` is expanded as
the macro. From `doc/tech_debt.md` (in the `expand.cdy` entry, [[B61]]);
the audit's defect 10 (`doc/hl_rqmt/tracking.md`).

## Repro

The translator should fail:

```candy error
(defmacro M (a) a)
(deft S (M ((x Int))))
(put 1)
```
```expect-error
M is a macro, so it can't be defined
```
