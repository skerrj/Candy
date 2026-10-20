# TODOS

Done and earlier items are in `doc/archive/TODOS_macros.md`,
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

## modules

- [x] Review `doc/hl_rqmt/modules.md`: accepted, MVP scope (only `(import m)`, everything exported, clash at import, cycles an error, `stem__name` in Python).
- [x] Modules step 1: the translator imports what it uses (still inclusion), `Macro` into `form.cdy`.
- [x] Modules step 2: per-module scopes, `stem__name` Python names, errors (clash, cycle, repeated stem, not imported).
- [x] Review step 2 as built (accepted) (`doc/hl_rqmt/modules.md`, step 2's "Done" note), and the new leaks and tech debt.
- [x] Modules step 3: docs (the spec's `import`, CLAUDE.md, leaks and tech debt; done with step 2).
