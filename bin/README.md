# bin

Checked-in Candy translators, one directory per target (`bin/py/` for Python; later
targets get their own, see `doc/hl_rqmt/multi_target.md`).

- `py/cdy_translator.py`: the self-hosted translator, generated; don't edit it. It is the
  Candy translator (`src/cdy/cdyc.cdy` and the files it imports) translated by itself.
  Run it: `python bin/py/cdy_translator.py FILE.cdy [OUT.py]` translates `FILE.cdy` (and
  its imports) into `OUT.py`, by default `output/FILE.py`; errors print `candy: ...` and
  exit with 1 (usage: 2). `python src/py_cdy/main.py FILE.cdy [--run]` does the same
  through `main.py`, which can also run the result. It needs only the
  runtime `cdy_rt` (it has its own reader), and it rebuilds itself (both tested).
- `py/form.cdy`, `py/prelude_macros.cdy`, `py/special.cdy`, `py/system.cdy` and
  `py/prelude.cdy`: copies of the files in `src/cdy/`, which the translator reads while
  translating: macro code uses `Form` and its helpers, every file gets the prelude's macros
  (`cond`) and the prelude (`rest`), and `special.cdy` and `system.cdy` declare the
  built-ins. `self_host.py` copies them next to every
  translator it builds; don't edit them.

**Rebuilding.** After changing `src/cdy/`, run `python src/py_cdy/self_host.py`:

1. this translator translates `src/cdy/cdyc.cdy` into T1 (`output/t1/`), which has the
   change but was built by the old translator;
2. T1 translates it into T2 (`output/t2/`), built by the new translator;
3. T2 must translate it into itself again (T3 = T2) and pass `mypy --strict`; only then
   does T2 replace `py/cdy_translator.py`.

`tst/py_cdy/test_self_host.py` fails while the copy here is stale. A feature that
`src/cdy/` itself uses takes two rebuilds: add it, rebuild, then use it, rebuild again.
A translator expands macros with its own copy of the prelude, so a new prelude macro that
`src/cdy/` uses must be copied into `py/` by hand before the rebuild (as `cond` was; see
step 5 in `doc/hl_rqmt/macros.md`).

A translator also reads the live `spelling.py`, and checks its own copies of `special.cdy`
and `system.cdy` against it: a change that adds or removes built-ins copies the new files
into `py/` before the rebuild (`doc/process.md`, "Rebuilding `bin`").

**Bootstrapping.** The first translator here was built by a translator written in Python,
at tag `self-host-py` (it is no longer on `master`). `python script/bootstrap.py
--from-scratch` rebuilds every `bin` since from it, through the history, each step checked
byte for byte against the one checked in; each step is a `boot/NN` tag. A commit that
changes anything in `py/` is a new step: after committing it, run `--step HEAD`, then
`--tag` (`doc/hl_rqmt/bootstrap.md`).
