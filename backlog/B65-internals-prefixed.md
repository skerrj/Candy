# B65: Tests reach translator internals by prefixed Python names

kind: tech-debt
state: open
priority: normal
found: modules, 2026-10-19
fixed:
where: `src/py_cdy/self_host.py`, `tst/py_cdy/test_self_host.py`
refs:

`t1.form__Sym`, `t1.read__read_forms`, `self_host.to_form`: moving a function to another
file changes its Python name. From `doc/tech_debt.md`.
