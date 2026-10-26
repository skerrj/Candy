# B72: parsec.py v4 isn't published

kind: tech-debt
state: open
priority: normal
found: bootstrap, 2026-10-20
fixed:
where: `script/bootstrap.py`, `README.md`
refs:

The bootstrap chain's first step (the Python translator, at tag `self-host-py`) needs it,
but it exists only as a local copy on the owner's machine; upstream sighingnow/parsec.py
has only `master`. So the chain can't run from scratch anywhere else. Fix: publish it (and
record where), or vendor a copy (MIT) that the script puts on the path for that step.
From `doc/tech_debt.md`.
