# B37: Only self tail calls are loops

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/lower.cdy`
refs: [[expr.tail-calls]], [[B98]]

Recursion that isn't a self tail call in a top-level `defn` (mutual recursion,
`(+ 1 (f ...))`, or any recursion in a function that makes a `fn`) uses the Python stack,
so about 1000 levels deep it fails with `RecursionError`. From `doc/archive/leaks_imvp_py_translator.md`. Related:
[[B98]].

## Notes

- 2026-11-22, Claude: the interpreter (`interp.cdy`, interpreter step 3) runs every tail
  call as a loop (`apply`'s trampoline), mutual ones too, but other recursion goes only
  138 calls deep there, about seven Python frames a call, against about 1000 on the
  Python target; [[expr.tail-calls]] now says the depth is an implementation's.
