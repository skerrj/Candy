# B188: namespaces step 1: one table of names

kind: task
state: done
priority: normal
found: namespaces, 2026-11-12
fixed: namespaces, 2026-11-12
where: `src/cdy/core.cdy`
refs: [[B40]]

Step 1 of `doc/hl_rqmt/namespaces.md`. The seven maps of what a file sees (`top`, `variants`, `sums`, `types`, `names`, `elsewhere`, `Seen`'s `from`) one map from a name to an `Entry`; `core.cdy` only, the Python output byte for byte the same; mypy's T2 check and the build measured (a record with a kind field if the sum is slow).

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
- 2026-11-12, Claude: built (the HLD's step 1 *Done* note): one `Entry` table in `core.cdy`,
  the output unchanged but for one error made right (a sum's name used as a value). In
  review.
- 2026-11-12, the owner: ticked in review.
