# B96: "No code changes" commits

kind: idea
state: open
priority: low
found: executable-spec, 2026-10-23
fixed:
where: `doc/process.md`
refs:

Tabled (2026-10-23; revisit when needed): a docs-only commit says so and skips the
rebuild, `boot/NN`, linters and tests. Pitfalls found: a file in `bin/<target>/` (even a
`.md`) changes `bin`; `spec/` is tests, not docs; and the label must come from the
commit's files (`git diff --cached --name-only`), since it skips checks. From `doc/brainstorm.md`.

## Notes

- 2026-10-26, the owner: `low` in triage ([[B103]]): an idea to think about later.
