# B11: A `deft` variant with the same name as a macro isn't rejected

kind: defect
state: done
priority: normal
found: macros, 2026-10-18
fixed: namespaces, 2026-11-13
where: `src/cdy/expand.cdy`
refs: [[macros.binding]], [[match.sum-types]], [[B61]]

A macro's name can't be bound or defined, but a variant can take it:
`(defmacro M (a) a) (deft S (M ((x Int))))` translates, and a later `(M 1)` is expanded as
the macro. From `doc/tech_debt.md` (in the `expand.cdy` entry, [[B61]]);
the audit's defect 10 (`doc/hl_rqmt/tracking.md`).

## Notes

- 2026-11-13, Claude: fixed by `namespaces` step 5 ([[B192]]): a `deft`'s type and
  variants with the same name as a macro are "M is a macro, so it can't be defined", at the `deft`
  (`analyse-top`, `macro-named`), as a `def` or `defn` was.
- 2026-11-13, Claude: its repro moved to the spec, `macros.binding` (the same error, and
  two rows more: a record's name, a generic type's); it was:

  ````text
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
  ````
- 2026-11-14, the owner: "with the same name as a macro", not "named like a macro".
  Claude: the title reworded; it was:

  ```text
  # B11: A `deft` variant named like a macro isn't rejected
  ```
