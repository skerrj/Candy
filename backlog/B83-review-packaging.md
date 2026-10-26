# B83: Review the `cdy_rt` packaging

kind: task
state: review
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `pyproject.toml`, `.gitignore`
refs:

The editable install, strict mode and `py.typed` in `pyproject.toml`, and the
`.gitignore` change (`lib/` no longer ignored). Carried over in `TODOS.md` for the owner's review.
