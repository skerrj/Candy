# B133: A `fn` bound by `let` isn't generic

kind: idea
state: open
priority: low
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/check.cdy`
refs: [[checking.locals]], [[B15]]

The checker has no let-polymorphism: a local has one type, so a `fn` bound by `let` is
used at one type, `(let ((id (fn (x) x))) (do (id 1) (id "a")))` is an error
([[checking.locals]]); a top-level `defn` with a generic `sig` is generic. The standard
answer is Hindley-Milner's: generalise a `let`'s type over the variables its context
doesn't fix. After the epic (`doc/hl_rqmt/python_complete.md`); it blocks no target. Split
out of [[B15]].
