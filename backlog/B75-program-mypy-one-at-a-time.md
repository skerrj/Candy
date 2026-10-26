# B75: The test programs' `mypy --strict` runs one at a time

kind: tech-debt
state: open
priority: normal
found: executable-spec, 2026-10-23
fixed:
where: `tst/py_cdy/test_self_host.py` (`test_mypy_strict`)
refs:

About 8.7 s for 17 programs. One batched run, as `tst/py_cdy/test_spec.py` does per spec
file, measured 0.4 s for 40 small files (`doc/hl_rqmt/executable_spec.md`, step 1); a
failure then names the run, not the program. From `doc/tech_debt.md`.
