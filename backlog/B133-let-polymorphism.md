# B133: A `fn` bound by `let` isn't generic

kind: idea
state: open
priority: low
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/check.cdy`
refs: [[checking.locals]], [[checking.any]], [[B15]]

The checker has no let-polymorphism: a local has one type, so a `fn` bound by `let` is
used at one type, `(let ((id (fn (x) x))) (do (id 1) (id "a")))` is an error
([[checking.locals]]); a top-level `defn` with a generic `sig` is generic. The standard
answer is Hindley-Milner's: generalise a `let`'s type over the variables its context
doesn't fix. After the epic (`doc/hl_rqmt/python_complete.md`); it blocks no target. Split
out of [[B15]].

## Notes

- 2026-11-03, Claude, in B140's review: a type variable that meets nothing (a `fn` never
  called, an `empty-list` never added to) stays unsolved, which Python writes `Any`;
  [[checking.any]] called that *lasting*, now *for now*, linking here. It said:

  ```text
  (a `fn` never called, an `empty-list` never added to) stays a type variable, which
  Python writes `Any` (*lasting*).
  ```

  The answers: generalise it (this item: `(Fn (t) t)` for any `t`, an empty list a
  `(List t)`); an error, `can't infer the type of y` (Elm, Rust; OCaml only when such a
  type escapes a module's interface); or a default (`Unit`, as Haskell defaults
  numbers). A variable that met only `Any` defaulting to `Any` stays *lasting*.
