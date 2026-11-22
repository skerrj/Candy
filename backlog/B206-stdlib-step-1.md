# B206: stdlib step 1: Declaration modules from the spellings, built-ins keyed by module

kind: task
state: done
priority: normal
found: stdlib, 2026-11-18
fixed: stdlib, 2026-11-18
where: `src/cdy/include.cdy`, `src/cdy/core.cdy`, `src/cdy_rt/spelling.py`, `tst/py_cdy/test_bootstrap.py`
refs: [[programs.import]]

Step 1 of `doc/hl_rqmt/stdlib.md`. `DECLARATION_MODULES` gone; `Builtin` and the spellings keyed by `global-key`; the index test over every declaration module.

## Notes

- 2026-11-18, Claude: filed on the HLD's acceptance (the owner, 2026-11-18).
- 2026-11-18, Claude: built (the HLD's step 1, "Done"): the declaration modules are
  those the spellings' keys name, not found by reading each library file; staged
  `old-runtime`.
- 2026-11-19, the owner: the deviation kept; the title reworded to match. It was:

  ```text
  # B206: stdlib step 1: Declaration modules by what they hold, built-ins keyed by module
  ```
- 2026-11-21, the owner: ticked in review.
