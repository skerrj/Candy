# B123: The translator writes its list loops by hand

kind: tech-debt
state: done
priority: normal
found: library, 2026-10-21
fixed: collections-2, 2026-11-11
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
- 2026-11-11, Claude: step 4 ([[B179]]): 25 of `emit.cdy`'s 29 loops are one call; four stay.
- 2026-11-11, Claude: step 5 ([[B180]]): 29 of the last 33 loops are one call; `read.cdy`'s
  four, which walk a text, stay. With steps 1 to 4, 111 loops are calls and 21 stay, each
  for a reason in the HLD's notes.
- 2026-11-11, the owner: closed with step 5. 21 loops are left, *lasting*, each one no list
  operation says better: two lists walked at once (`assigns`, `fill-holes`, `refill`,
  `zip-map`, `typed-all`, `unify-all`, `emit-params`), a text (`format-parts`,
  `mangle-chars`, `escape-chars`, `line-starts`, `read-all`, `read-list`, `read-str`), a
  count (`fresh-types`), an early exit (`find-field`), a work list that grows (`reach`),
  names checked against those bound so far, `_` skipped but counted (`tup-binds`,
  `pattern-binds`), forms taken two at a time (`assoc-fields`), and `emit-match`'s
  `if`/`elif` chain.
