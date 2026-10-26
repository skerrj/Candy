# B98: Trampolines, or `loop`/`recur`, for deep recursion

kind: idea
state: open
priority: normal
found: symbol-table, 2026-10-21
fixed:
where: `src/cdy/lower.cdy` (`loop-tail-calls`), `src/py_cdy/self_host.py`
refs: [[expr.tail-calls]], [[B37]]

Should Candy get a trampoline, or a Clojure-style `loop`/`recur` form, for mutual and deep
recursion ([[B37]])? And could `self_host.py`'s raise of the recursion limit
(to 20,000) go once T1 no longer recurses so deeply? See
`doc/hl_rqmt/mutation_optimization.md` ("Tail calls"). From `doc/brainstorm.md`.
