# B3: `a-b` and `a_b` are one Python name

kind: defect
state: done
priority: high
found: py-py-translator, 2026-10-15
fixed: name-checks
where: `src/cdy/emit.cdy` (`py-mangle`)
refs: [[syntax.names]], [[B12]]

`py-mangle` turns `-` into `_`, so `a-b` and `a_b` become one Python name, and the second
definition silently replaces the first: wrong output, with no error. The iMVP's leak list
said the translator reports it; that was the Python translator's check, which the Candy
translator never had. Fix: reject two names that mangle alike in one scope, or mangle
injectively. From `doc/archive/leaks_imvp_py_translator.md` ("Name mangling can
collide"); the audit's defect 1 (`doc/hl_rqmt/tracking.md`). Related: [[B12]].

## Notes

- 2026-10-26, the owner: `high` in triage ([[B103]]): silent wrong output.
- 2026-10-26, Claude Code: fixed on `name-checks` (step 1): a clash is an error,
  [[syntax.python-names]].
