# B188: namespaces step 1: one table of names

kind: task
state: open
priority: normal
found: namespaces, 2026-11-12
fixed:
where: `src/cdy/core.cdy`
refs: [[B40]]

Step 1 of `doc/hl_rqmt/namespaces.md`. The seven maps of what a file sees (`top`, `variants`, `sums`, `types`, `names`, `elsewhere`, `Seen`'s `from`) one map from a name to an `Entry`; `core.cdy` only, the Python output byte for byte the same; mypy's T2 check and the build measured (a record with a kind field if the sum is slow).

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
