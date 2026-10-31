# B125: Run the target's own static checker, as an option

kind: idea
state: open
priority: low
found: master, 2026-10-30
fixed:
where: `src/cdy/cdyc.cdy`, `src/py_cdy/main.py`
refs: [[B15]], [[B75]]

A target may name a static checker for the code it writes, and the driver runs it when
asked (`--check`, say): mypy for Python, as `test_self_host.py` and `test_spec.py` do
today by hand; a C target's compiler warnings; nothing extra for Rust, whose compiler
checks anyway. The checker becomes one more optional entry in the porting surface,
instead of a test-suite special case (`doc/hl_rqmt/python_complete.md`, Question 3,
the `porting-surface` branch).
