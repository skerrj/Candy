# B5: A record field `_x` translates, and fails at run time

kind: defect
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/core.cdy`
refs: [[types.records]]

`NamedTuple` forbids field names that start with `_` (and `-`, which mangles to `_`), so
`(deft V ((_x Int)))` translates and fails when it runs, with Python's `ValueError`. The
iMVP's leak list says such a field "can't" be written, but nothing rejects it. Fix: reject
it in `core.cdy` (or mangle field names). From `doc/archive/leaks_imvp_py_translator.md`;
the audit's defect 4 (`doc/hl_rqmt/tracking.md`).

## Repro

The translator should fail:

```candy error
(deft V ((_x Int)))
(put 1)
```
```expect-error
_x
```
