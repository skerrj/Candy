# B214: `check`'s text doesn't write a string's escapes back

kind: tech-debt
state: open
priority: low
found: stdlib, 2026-11-19
fixed:
where: `src/cdy/test_macros.cdy` (`form-text`)
refs: [[library.test]]

A failed `check` writes its expression as the program wrote it, by `form-text`, which
writes a string literal as `"` + its value + `"`: a string holding `"`, `\` or a newline
comes out as it reads, not as it was written (`"a\"b"` as `"a"b"`). The reader's escapes
written back, or the form's source text kept, would fix it.

## Notes

- 2026-11-19, Claude: filed with `stdlib` step 3 (the HLD's "Done").
