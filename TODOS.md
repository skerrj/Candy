# TODOS

- [x] Add pytest tests for `src/py_cdy/parse_cdy.py` under `tst/py_cdy/` (`tst/py_cdy/test_parse_cdy.py`; run `pytest` in the `py_cdy` conda env)
- [x] **Review `src/cdy_rt/table.py` and `src/cdy_rt/table_defs.py`**: the owner skimmed them and accepted them for now. The points that were listed for review, kept for reference:
  - `rest` is not included (schmuz defined it in `parse.scm`); add it to `table_defs`?
  - `empty-list` now renders as `()`, since `List` is a Python tuple (changed).
  - Behaviour changes from smz: `spit(path, text)` order, `is_str` is a type check (was a quoted-token check), `is_coll` accepts tuples, `slurp` raises `FileNotFoundError` and searches `*.cdy`.
  - Renames: `slice` → `slice_`, `in_it` → `in_`, `join_it` → `join`, `op-tab-*` → `table-*`.
  - Dropped: `true`/`false` and char constants (`LF`, `DQ`, `BS`, `ES`, ...) now that Candy has literals and escapes; `m_table_*` wrappers; `parse_string_help*` leftovers.
  - The self-hosted compiler must pass the table along (`table-add-fun` returns a new table).
- [x] Move `table.py` and `table_defs.py` to the runtime package `src/cdy_rt/`, with `RUNTIME_MODULE`/`TABLE_MODULE` set to `cdy_rt.table_defs`/`cdy_rt.table`.
- [x] Make `cdy_rt` importable: editable install of just `cdy_rt` in strict mode (`pip install -e . --config-settings editable_mode=strict`), with a `py.typed` marker so mypy and pyright use it.
- [x] Un-ignore `lib/` in `.gitignore`: `SEARCH_PATH` in `table.py` searches a `lib` directory for Candy files.
- [x] Run ruff, pylint, mypy and pyright on them and add tests in `tst/cdy_rt/`. Fixes from the first run: `in_` typed as `Sequence[object]` (a `str` is a `Sequence`), explicit UTF-8 for file I/O, and `find_path` only skips `tmp` *below* a search root (it used to skip every file under `/tmp`).
- [x] `src/py_cdy/reader.py` (`slurp` copied from `table_defs`) and `src/py_cdy/main.py` (modelled on smz's), with tests.

## For owner review (from the design session after `36ca66e`)

- [x] `sig` type names in `doc/hl_rqmt/iMVP_py_translator.md` ("Signature statement"): confirm `String`, `Unit` (value `nil`), `(Maybe a)`, `(Fn (A B) R)`, `(Tup a b)`, `(Map k v)`. (`List` is decided: one kind of abstract `Collection` later.)
- [x] `(List a)` is Python `tuple[A, ...]` (decided). **To do with the table review:** change `empty-list` in `src/cdy_rt/table.py` from `[]` to `()`.
- [x] `Any` for nested `fn`s that become Python `def`s (iMVP doc, `sig` open item 2).
- [ ] `doc/leaks.md` (new): check the list of hacks and Python leaks, including `format` (a hack) and `tup` destructuring (a stopgap), both from smz.
- [ ] `src/cdy/candy-special.md`: Claude marked `### quote [SKIP]`; `sig`, `deft`, `get`/`assoc` are not in the spec yet. Add them?
- [ ] `cdy_rt` packaging in `pyproject.toml` (editable install, strict mode, `py.typed`) and the `.gitignore` change (`lib/` no longer ignored).
- [ ] Open items summary in the iMVP doc ("Open items (summary)"): `deft` (proposed), literal parser rules, strategy A/B and IR layering, and the proposals for where to catch `def`/`deft` inside a function (`analyse_top`/`analyse_expr`; also `defn` and `sig`; no top-level `do` splicing).
