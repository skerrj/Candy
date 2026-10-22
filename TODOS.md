# TODOS

Done and earlier items are in `doc/archive/TODOS_bootstrap.md`,
`doc/archive/TODOS_system_prelude.md`, `doc/archive/TODOS_modules.md`,
`doc/archive/TODOS_macros.md`, `doc/archive/TODOS_self_host_cleanup.md`,
`doc/archive/TODOS_pre_self_host.md` and `doc/archive/TODOS_imvp_py_translator.md`.

## Carried over (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_pre_self_host.md`: check the lists of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.
- [ ] Review `doc/hl_rqmt/self_hosting_primo.md` (stages 0–3 done, as built).
- [ ] Review `import` step A as built (`doc/hl_rqmt/self_host_cleanup.md`, "Step A as built"), and its leak (now in `doc/archive/leaks_self_host_cleanup.md`).
- [ ] Review the `main` entry-point convention (`doc/hl_rqmt/self_host_cleanup.md`, "The driver as built"; `src/cdy/candy-special.md`, "programs").
- [ ] Add the up, down, down*, meta-template side conversation to `doc/brainstorm.md` (owner to supply the gist).
- [ ] system-prelude: review step 1 as built (`doc/hl_rqmt/system_prelude.md`, its "Done" note; `src/cdy/system.cdy`'s types), and the new leaks and tech debt.
- [ ] system-prelude: review step 3 as built (`doc/hl_rqmt/system_prelude.md`, its "Done" note; `src/cdy/prelude.cdy`).
- [ ] system-prelude: review step 5 as built (`doc/hl_rqmt/system_prelude.md`, its "Done" note).
- [ ] Review `doc/hl_rqmt/library.md` (draft HLD, a later branch): two layers, the translator's built-ins become Candy, and its questions.

## symbol-table

- [ ] Review step 1 as built (`doc/hl_rqmt/symbol_table.md`, its "Done" note).
- [ ] Review step 2 as built (`doc/hl_rqmt/symbol_table.md`, its "Done" note; `src/cdy/special.cdy`).
- [ ] Review step 3 as built (`doc/hl_rqmt/symbol_table.md`, its "Done" note).
- [ ] Review step 4 as built (`doc/hl_rqmt/symbol_table.md`, its "Done" note; the plan's step 4 split in two).
- [ ] Review step 5 as built (`doc/hl_rqmt/symbol_table.md`, its "Done" note).
