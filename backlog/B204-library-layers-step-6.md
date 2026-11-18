# B204: library-layers step 6: each built-in specified

kind: task
state: review
priority: normal
found: library-layers, 2026-11-15
fixed: library-layers, 2026-11-17
where: `spec/60-library.md`, `tst/py_cdy/test_doc_links.py`
refs: [[library.builtins]]

Step 6 of `doc/hl_rqmt/library_layers.md`. A rule per group in `spec/60-library.md`, each naming its built-ins with their types and their edge cases, with examples that run; `library.builtins`' table the index; a test that every `sig` in a declaration module is named in a `candy run` example.

## Notes

- 2026-11-15, Claude: filed on the HLD's acceptance (the owner, 2026-11-15).
- 2026-11-17, Claude: built (the HLD's step 6, "Done"). The test checks `system.cdy`'s
  built-ins, not `translator.cdy`'s, and counts a `candy panic` example as well as a
  `candy run` one (for `fail`). `isspace-at` is now bounds-checked. The reader no longer
  uses it, nor the prelude's `index-of` `elem-index`: the owner asked for those two and
  `is-digit` to go (2026-11-17), in the next commit, which this one's `bin` can read.
