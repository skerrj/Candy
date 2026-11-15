# B51: `with-default` is a built-in, not prelude

kind: leak
state: done
priority: normal
found: library, 2026-10-22
fixed: semantics, 2026-11-15
where: `src/cdy/system.cdy`, `src/cdy/prelude.cdy`
refs: [[programs.prelude]], [[library.lists]], [[B20]]

Built on `Maybe`, it belongs in the prelude, but written in Candy, `(if (= m nil) d m)`
doesn't narrow `m` from `Optional[A]` to `A` for mypy, so the Python fails
`mypy --strict`: the Python checker decides what can be Candy. Fix: move it once Candy
narrows a `Maybe` itself ([[B20]]). From `doc/archive/leaks_library.md`.

## Notes

- 2026-11-15, Claude: stale: `with-default` has been the prelude's, written in Candy with
  `match`, since `semantics` step 4 (`144f19b`, `Maybe` a sum). The owner:
  `library_layers.md` Question 8, closed as done.
