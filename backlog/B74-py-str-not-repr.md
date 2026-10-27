# B74: `py-str` is close to `repr`, not equal

kind: tech-debt
state: open
priority: low
found: library, 2026-10-22
fixed:
where: `src/cdy/emit.cdy`
refs: [[syntax.strings]]

It escapes control characters (below 32, and 127 to 160) but leaves others Python's
`repr` would escape (U+00AD, U+2028) as they are, since Candy can't ask whether a
character is printable. The output is still valid Python (`doc/hl_rqmt/library.md`, step
1a). From `doc/tech_debt.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): cosmetic or harmless.
