# TODOS

Done and earlier items are in `doc/archive/TODOS_imvp_py_translator.md`.

## Carried over from the iMVP (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` (was `doc/leaks.md`): check the list of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `src/cdy/candy-special.md`: Claude marked `### quote [SKIP]`; `sig`, `deft`, `get`/`assoc` are not in the spec yet. Add them?
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.

## pre-self-host

- [ ] Review `doc/hl_rqmt/sum_types.md` (draft): sum types now or `Any` plus predicates, syntax, nullary variants, exhaustiveness, `Maybe`, and the other open questions.
