# B215: `deftest` doesn't register its tests

kind: idea
state: open
priority: low
found: stdlib, 2026-11-19
fixed:
where: `src/cdy/test_macros.cdy`, `src/cdy/test.cdy`
refs: [[library.test]]

A program names its tests to `test.run`, so a test left out of the list never runs, and
nothing says so. A module can't collect its own definitions: a macro writing a
module-level list can't add to it, since a `def` is a constant. A macro over the whole
module (`(deftests ...)`, its tests and the list together), or the translator listing a
module's `test.Test`s, would let `deftest` register them (the `stdlib` HLD's Question 7:
listed, *for now*).

## Notes

- 2026-11-19, Claude: filed with `stdlib` step 3 (the HLD's "Done").
