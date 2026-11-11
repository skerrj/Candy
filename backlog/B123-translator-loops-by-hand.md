# B123: The translator writes its list loops by hand

kind: tech-debt
state: open
priority: normal
found: library, 2026-10-21
fixed:
where: `src/cdy/`
refs: [[B19]], [[B69]]

The translator calls `map` 10 times, `fold` twice, `filter` and `find` never (2026-10-29);
most of its list work is `defn`s with an `acc` argument, about 94 when counted on branch
`library`, many of them a `map`, `filter`, `any` or `fold` written out. `library.md`
(question 6) kept them *for now*: a `fn` becomes a nested Python `def` typed `Any`
([[B19]]), so `map` and `fold` would cost the fixpoint's `mypy --strict` checking, and many
loops thread a counter or a scope as well (`analyse-all`, `let-bindings`,
`bind-params`, `destructure` return `(tup acc n)`), which needs a `fold` over a tuple or
a `map-acc`. Revisit once `fn`s are typed. Built-in list operations would also take the
translator off the quadratic copies ([[B69]]).
- 2026-11-10, Claude: `collections-2` step 1 ([[B167]]): the 12 loops that thread a state are
  `map-acc` calls; the rest are steps 2 to 5 (`collections_2.md`).
- 2026-11-11, Claude: step 2 ([[B177]]): 31 of `core.cdy`'s and `lower.cdy`'s 38 loops are one
  call; seven stay, each for a reason in the HLD's note.
- 2026-11-11, Claude: step 3 ([[B178]]): 14 of `check.cdy`'s 20 loops are one call; six stay.
