# TODOS

Done and earlier items are in `doc/archive/TODOS_imvp_py_translator.md`.

## Carried over from the iMVP (for owner review)

- [ ] `doc/archive/leaks_imvp_py_translator.md` (was `doc/leaks.md`): check the list of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `src/cdy/candy-special.md`: Claude marked `### quote [SKIP]`; `sig`, `deft`, `get`/`assoc` are not in the spec yet. Add them?
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, and confirming that `defn` and `sig` are top-level only and that a top-level `do` isn't spliced.

## pre-self-host

- [x] `doc/hl_rqmt/sum_types.md`: all seven questions decided (variants in `deft`; nullary variants are values; exhaustive `match`; `Maybe` stays `A | None`; `get` after `match`; global variant names), and implemented (stage 0).
- [ ] `src/cdy/candy-special.md`: add `deft` (records and sums) and `match` to the spec, with `sig`, `get` and `assoc` (see the carried-over item above).
- [ ] Review `doc/hl_rqmt/self_hosting_primo.md` (draft staging plan): the translator in Candy with the Python parser borrowed, the T1 = T2 fixpoint, then the parser in Candy. Forms at the boundary: A, `deft` variants plus conversion (decided). Decided: Candy source in `src/cdy/`, T1/T2 generated into git-ignored `output/`. Driver: a `main.py` mode, for now (decided). Proposed, to confirm: the fixpoint compares the files T1 and T2 up to formatting (`ast.dump`) and their output byte for byte.
