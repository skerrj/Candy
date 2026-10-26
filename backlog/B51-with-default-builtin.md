# B51: `with-default` is a built-in, not prelude

kind: leak
state: open
priority: normal
found: library, 2026-10-22
fixed:
where: `src/cdy/system.cdy`, `src/cdy/prelude.cdy`
refs: [[programs.prelude]], [[library.lists]], [[B20]]

Built on `Maybe`, it belongs in the prelude, but written in Candy, `(if (= m nil) d m)`
doesn't narrow `m` from `Optional[A]` to `A` for mypy, so the Python fails
`mypy --strict`: the Python checker decides what can be Candy. Fix: move it once Candy
narrows a `Maybe` itself ([[B20]]). From `doc/archive/leaks_library.md`.
