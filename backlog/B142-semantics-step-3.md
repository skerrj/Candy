# B142: semantics step 3: equality

kind: task
state: review
priority: normal
found: semantics, 2026-11-02
fixed: semantics
where: `src/cdy/emit.cdy`, `src/cdy/check.cdy`, `spec/40-expressions.md`
refs: [[B27]], [[B137]]

Step 3 of `doc/hl_rqmt/semantics.md`. Every record and variant class compares its class too (`__eq__`, `__ne__`, `__hash__`; [[B137]], Question 12); `=` on a function an error; `expr.equality` ([[B27]]).

## Notes

- 2026-11-02, Claude: built; see the HLD's step 3 *Done* note. [[B27]] and [[B137]] done; [[B153]] added; [[B29]] and [[B150]] noted.
