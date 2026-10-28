# B5: A record field `_x` translates, and fails at run time

kind: defect
state: done
priority: normal
found: py-py-translator, 2026-10-17
fixed: field-checks
where: `src/cdy/core.cdy`
refs: [[types.records]]

`NamedTuple` forbids field names that start with `_` (and `-`, which mangles to `_`), so
`(deft V ((_x Int)))` translates and fails when it runs, with Python's `ValueError`. The
iMVP's leak list says such a field "can't" be written, but nothing rejects it. Fix: reject
it in `core.cdy` (or mangle field names). From `doc/archive/leaks_imvp_py_translator.md`;
the audit's defect 4 (`doc/hl_rqmt/tracking.md`).

## Notes

- 2026-10-27, field-checks step 2: an error at translation (`check-py-fields` in
  `emit.cdy`), rejected rather than mangled (the HLD's Question 1); the limit itself is a
  leak, [[B113]]. The repro is now this row of `[[types.records]]`: `(deft V ((_x Int)))
  => deft V: field _x can't start with _ in Python (_x)`.
