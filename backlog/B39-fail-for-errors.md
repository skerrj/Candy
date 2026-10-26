# B39: `fail` stands in for errors

kind: leak
state: open
priority: normal
found: pre-self-host, 2026-10-17
fixed:
where: `src/cdy_rt/primitives.py`
refs: [[library.builtins]]

Candy has no exceptions; `(fail "msg")` raises `CandyFail` from the runtime, and its
result is typed as anything (`NoReturn`). From `doc/archive/leaks_pre_self_host.md`.
