# B204: library-layers step 6: each built-in specified

kind: task
state: open
priority: normal
found: library-layers, 2026-11-15
fixed:
where: `spec/60-library.md`, `tst/py_cdy/test_doc_links.py`
refs: [[library.builtins]]

Step 6 of `doc/hl_rqmt/library_layers.md`. A rule per group in `spec/60-library.md`, each naming its built-ins with their types and their edge cases, with examples that run; `library.builtins`' table the index; a test that every `sig` in a declaration module is named in a `candy run` example.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
