# TODOS

Done and earlier items are in `doc/archive/TODOS_runtime_names.md`,
`doc/archive/TODOS_library.md`, `doc/archive/TODOS_symbol_table.md`,
`doc/archive/TODOS_bootstrap.md`, `doc/archive/TODOS_system_prelude.md`,
`doc/archive/TODOS_modules.md`, `doc/archive/TODOS_macros.md`,
`doc/archive/TODOS_self_host_cleanup.md`, `doc/archive/TODOS_pre_self_host.md` and
`doc/archive/TODOS_imvp_py_translator.md`.

## Carried over (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_pre_self_host.md`: check the lists of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.
- [ ] Review `doc/hl_rqmt/self_hosting_primo.md` (stages 0–3 done, as built).
- [ ] Review `import` step A as built (`doc/hl_rqmt/self_host_cleanup.md`, "Step A as built"), and its leak (now in `doc/archive/leaks_self_host_cleanup.md`).
- [ ] Review the `main` entry-point convention (`doc/hl_rqmt/self_host_cleanup.md`, "The driver as built"; `spec/10-programs.md`, "main").
- [ ] Add the up, down, down*, meta-template side conversation to `doc/brainstorm.md` (owner to supply the gist).
- [ ] system-prelude: review step 1 as built (`doc/hl_rqmt/system_prelude.md`, its "Done" note; `src/cdy/system.cdy`'s types), and the new leaks and tech debt.
- [ ] system-prelude: review step 3 as built (`doc/hl_rqmt/system_prelude.md`, its "Done" note; `src/cdy/prelude.cdy`).
- [ ] system-prelude: review step 5 as built (`doc/hl_rqmt/system_prelude.md`, its "Done" note).
- [ ] Review `doc/hl_rqmt/review.md` (draft HLD, a goal only): a better way to review items and tasks.

## executable-spec

- [x] Review step 1 as built (`doc/hl_rqmt/executable_spec.md`, its "Done" note: the runner, `spec/README.md`, the fixtures in `conftest.py`, and the mypy measurement).
- [x] **Checkpoint:** review how `spec/30-match.md` reads (step 2's "Done" note), before step 3 writes the rest of the spec in its style. Step 3 is `doc/hl_rqmt/executable_spec.md` → "Steps (sketch)" → "3. The other features" (migrating the rest of `candy-special.md`); review its proposed file list and the tuples note there too.
- [ ] Review step 3, commit 1 as built (`spec/00-syntax.md`, `spec/10-programs.md`; the HLD's step 3 "As built, commit 1" note, with its one change to the table: `import-macros` in `50-macros.md`).
- [ ] Review step 3, commit 2 as built (`spec/20-types.md`, `spec/40-expressions.md`; the HLD's "As built, commit 2" note), and the new leaks (`doc/leaks.md`) and tech debt (two bugs).
- [ ] Review step 3, commit 3 as built (`spec/50-macros.md`, `spec/60-library.md`; the HLD's "As built, commit 3" note).
- [ ] Review step 3, commit 4 as built (`candy-special.md` removed, the pointers, `boot/32`; the HLD's "Done. As built, commit 4" note).
- [ ] Review step 4 as built (`doc/process.md`: "The spec", the lifecycle, "Where notes go"; the HLD's step 4 "Done" note).
- [ ] Review step 5 as built (CLAUDE.md's `spec/` entry, history and command; the iMVP doc and `brainstorm.md` pointers; the HLD's step 5 "Done" note).
