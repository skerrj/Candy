# B60: Three directories of test programs

kind: tech-debt
state: open
priority: normal
found: bootstrap, 2026-10-20
fixed:
where: `tst/cdy/`
refs:

`tst/cdy/t1/`, `tst/cdy/` and `tst/cdy/cdyc/` were three audiences: `cdyc/` held the
programs only the Candy translator could handle. With the Python translator gone
(`doc/hl_rqmt/bootstrap.md`) the split means nothing; they could be one directory. Files
the programs import live in subdirectories (`lib/`). From `doc/tech_debt.md`.
