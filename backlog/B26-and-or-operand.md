# B26: `and` and `or` return an operand, not a `Bool`

kind: leak
state: done
priority: normal
found: py-py-translator, 2026-10-15
fixed: semantics
where: `src/cdy_rt/spelling.py`
refs: [[expr.logic]], [[B100]]

`(or x 5)` can be `5`, as in Python. From `doc/archive/leaks_imvp_py_translator.md`. Related: [[B100]].

## Notes

- 2026-11-02, Claude: semantics step 1: closed with no code change; the checker makes every argument of `and` and `or` a `Bool` (`or: expected Bool, got Int`), so the operand Python's `or` gives is a `Bool`. Stated in [[expr.logic]], *lasting*, with an errors table; what `Any` lets through is [[B18]]'s.
