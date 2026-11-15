# B65: Tests reach translator internals by prefixed Python names

kind: tech-debt
state: done
priority: normal
found: modules, 2026-10-19
fixed: namespaces
where: `src/py_cdy/self_host.py`, `tst/py_cdy/test_self_host.py`
refs:

`t1.form__Sym`, `t1.read__read_forms`, `self_host.to_form`: moving a function to another
file changes its Python name. From `doc/tech_debt.md`.

## Notes

- 2026-11-14, Claude: fixed in `namespaces` step 6: `candy(t1, "form.Pos")` in
  `tst/py_cdy/test_self_host.py` reaches a translator's name as Candy writes it, through
  `emit.cdy`'s `py-global-name`, which is the one name a test reaches by its Python
  spelling. `self_host.to_form` is gone, and `self_host.py` reaches only the top module's
  `translate-text` and `translate-file`, which have no prefix.
