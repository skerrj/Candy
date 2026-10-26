# B1: Highlight `candy` fences in Markdown, in the VS Code extension

kind: task
state: open
priority: low
found: tracking, 2026-10-25
fixed:
where: `editors/vscode-candy/`
refs: [[editor.not-yet]]

The spec's examples are fenced blocks (`candy run`, `candy error`, `candy errors`) in
`spec/*.md`, so they aren't highlighted, as `.cdy` files are. A Markdown injection grammar
in `editors/vscode-candy/` would highlight them in VS Code (GitHub won't either way). The
alternative, examples as separate `.cdy` files, was not taken (`doc/hl_rqmt/tracking.md`,
question 10).
