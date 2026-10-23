# The runtime's names (HLD)

**Status: accepted (2026-10-23), with the proposed answers to its questions
(`primitives` for `prims`).** Branch `runtime-names`, after tag
`library`. From `doc/tech_debt.md`, "The runtime's module names are out of date" (noted in
the review of `library`, where the module names were agreed).

## Where things stand

The runtime's names date from when `table.py` was the translator's symbol table. Since
`symbol-table` (`doc/hl_rqmt/symbol_table.md`) it holds only each built-in's Python
spelling and rendering kind; what a built-in *is* lives in `special.cdy` and `system.cdy`.

- **`src/cdy_rt/table.py`:** the spellings. `INITIAL_TABLE` (a `Table`, a mapping of
  `TableEntry(py, kind)`), grouped as `MATH`, `BOOL`, ..., `META_TABLE` (only
  `initial-table`); the helpers `call`, `runtime` and `value`; the module names
  `RUNTIME_MODULE` and `TABLE_MODULE`; and `SEARCH_PATH`, which only `slurp` uses.
- **`src/cdy_rt/table_defs.py`:** the primitives generated code calls (`list_map`,
  `slurp`, `run_main`, `CandyFail`, ...). It imports `SEARCH_PATH` from `table.py`.
- **In Candy:** `system.cdy`'s `(sig initial-table ...)`, read by `cdyc.cdy` and
  `expand.cdy`; `emit.cdy`'s `Env` field `table`, and `core.cdy`'s parameter `table` in
  `read-builtins` and the rest, whose errors name `table.py`; `PY_IMPORTS` and `emit-main`
  name both modules.
- **Elsewhere:** every generated file imports both modules by name (`bin`'s translator
  refers to them 388 times); `src/py_cdy/main.py` and `tst/py_cdy/test_self_host.py`
  import them; their tests are `tst/cdy_rt/test_table.py` and `test_table_defs.py`.

## Goals

- Names that say what the modules hold: the Python **spellings**, and the **primitives**.
- No change in behaviour: every program translates to the same Python, apart from the
  names.
- The bootstrap chain unbroken, with no staging.

**Not goals:** moving the spellings into Candy, or a second target's runtime
(`doc/hl_rqmt/multi_target.md`); changing the kinds.

## Proposal

The first three renames were agreed in `library`'s review (`prims.py` became
`primitives.py` in answering this HLD); the rest follow from them (question 1).

| Now | Becomes | |
|---|---|---|
| `cdy_rt/table.py` | `cdy_rt/spelling.py` | agreed |
| `cdy_rt/table_defs.py` | `cdy_rt/primitives.py` | agreed |
| `INITIAL_TABLE` / `initial-table` | `SPELLINGS` / `py-spellings` | agreed |
| `TableEntry` / `Table` | `Spelling` / `Spellings` | proposed |
| `TABLE_MODULE` / `RUNTIME_MODULE` | `SPELLING_MODULE` / `PRIMITIVES_MODULE` | proposed |
| `runtime(name)` (an entry calling a primitive) | `primitive(name)` | proposed |
| `META_TABLE` (the translator's one entry) | `TRANSLATOR` | proposed |
| `SEARCH_PATH`, in `table.py` | in `primitives.py`, beside `slurp` | proposed (question 2) |
| `emit.cdy`'s `table` field, `core.cdy`'s `table` parameter | `spellings` | proposed |
| errors naming `table.py` | name `spelling.py` | follows |
| `test_table.py` / `test_table_defs.py` | `test_spelling.py` / `test_primitives.py` | follows |

## Bootstrap

`script/bootstrap.py` runs each step against its own commit's runtime, with the `bin`
before it. So, at the step that renames, the `bin` before runs on the new runtime, and it
imports `cdy_rt.table` and `cdy_rt.table_defs` by name (`cdy_rt.table.INITIAL_TABLE`
directly). It needs nothing else old: its built-ins come from the step's own
`bin/py/system.cdy` and the live spellings, which agree (`py-spellings` in both, copied
into `bin/py/` before the rebuild).

- **The renaming step** keeps `table.py` and `table_defs.py` as re-exports of the new
  modules (`INITIAL_TABLE` as another name for `SPELLINGS`). A chain step (`boot/31`), no
  staging.
- **The removing step** deletes them. Its `bin` is the same (the renaming step's names
  only), so it is **not** a chain step: `doc/tech_debt.md`'s "two chain steps" was one
  too many.
- **Reinstall** the editable runtime after each (`pip install -e . --config-settings
  editable_mode=strict`), since each adds or removes a module.

## Steps

1. **Rename** (the table above), with `table.py` and `table_defs.py` as re-exports;
   `system.cdy` copied into `bin/py/`, `bin` rebuilt, `boot/31`; reinstall.
2. **Remove** `table.py` and `table_defs.py`; reinstall. `pytest -m bootstrap` checks the
   older steps still build on their own runtimes.
3. **Docs:** CLAUDE.md, `bin/README.md`, `src/cdy_rt/__init__.py`, the
   comments in `special.cdy`, `system.cdy` and `emit.cdy`, `doc/hl_rqmt/multi_target.md`
   and the iMVP doc (question 3); the tech-debt entry goes.

## Questions (answered: the proposals, 2026-10-23)

1. **The other names** (the "proposed" rows above): as proposed, or keep `TableEntry`,
   `Table` and the rest (only the agreed three change)?
   *Proposed:* as above; a `Table` of `TableEntry`s would leave "table" where the module
   no longer says it. *Lasting* (with `primitives`, not `prims`).
2. **`SEARCH_PATH`:** move it to `primitives.py`?
   *Proposed:* yes; only `slurp` uses it, and then neither module imports the other.
   *Lasting.*
3. **Older HLDs** (`symbol_table.md`, `library.md`, `bootstrap.md`, ...) name `table.py`
   and `table_defs.py`: rewrite them, or leave them as history?
   *Proposed:* leave them (they record what was built when); the iMVP doc, which is kept
   up to date, gets a note in "Symbol table: `table.py` and `table_defs.py`" saying
   where the two are now. *Lasting.* The HLDs that use the old names, as history:
   `self_host_cleanup.md`, `macros.md`, `system_prelude.md`, `bootstrap.md`,
   `symbol_table.md` and `library.md` (`table.py` is `spelling.py`, `table_defs.py` is
   `primitives.py`, and `initial-table` is `py-spellings`, from this branch on).
