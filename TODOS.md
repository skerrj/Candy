# TODOS

Done and earlier items are in `doc/archive/TODOS_modules.md`, `doc/archive/TODOS_macros.md`,
`doc/archive/TODOS_self_host_cleanup.md`, `doc/archive/TODOS_pre_self_host.md` and
`doc/archive/TODOS_imvp_py_translator.md`.

## Carried over (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` and `doc/archive/leaks_pre_self_host.md`: check the lists of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.
- [ ] Review `doc/hl_rqmt/self_hosting_primo.md` (stages 0–3 done, as built).
- [ ] Review `import` step A as built (`doc/hl_rqmt/self_host_cleanup.md`, "Step A as built"), and its leak (now in `doc/archive/leaks_self_host_cleanup.md`).
- [ ] Review the `main` entry-point convention (`doc/hl_rqmt/self_host_cleanup.md`, "The driver as built"; `src/cdy/candy-special.md`, "programs").
- [ ] Add the up, down, down*, meta-template side conversation to `doc/brainstorm.md` (owner to supply the gist).

## system-prelude

- [x] Review `doc/hl_rqmt/system_prelude.md`: accepted, MVP scope (operators left out, variadic built-ins `Any`, prelude an ordinary import, emitted whole).
- [x] Step 1: `system.cdy`, read and checked against the table; arity from its `sig`s.
- [ ] Review step 1 as built (`doc/hl_rqmt/system_prelude.md`, its "Done" note; `src/cdy/system.cdy`'s types), and the new leaks and tech debt.
- [x] ~~Step 2: `table.py` without arities~~ dropped: the frozen Python translator still reads them (kept, as tech debt).
- [x] Step 3: `prelude.cdy` (`rest`, `map`, `filter`, `fold`), imported into every file.
- [ ] Review step 3 as built (`doc/hl_rqmt/system_prelude.md`, its "Done" note; `src/cdy/prelude.cdy`).
- [x] Step 4: docs (the iMVP doc, `multi_target.md`, the macros HLD's pointer).
- [ ] Review `doc/hl_rqmt/library.md` (draft HLD, the follow-up branch): system, translator-only and prelude layers, and its questions.
