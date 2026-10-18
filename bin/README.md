# bin

Checked-in Candy translators, one directory per target (`bin/py/` for Python; later
targets get their own, see `doc/hl_rqmt/multi_target.md`).

- `py/cdy_translator.py`: the self-hosted translator, generated; don't edit it. It is the
  Candy translator (`src/cdy/cdyc.cdy` and the files it imports) translated by itself.
  Use it with `python src/py_cdy/main.py FILE.cdy --translator bin`. It needs only the
  runtime `cdy_rt` (it has its own reader), and it rebuilds itself (both tested).

**Rebuilding.** After changing `src/cdy/`, run `python src/py_cdy/self_host.py`:

1. this translator translates `src/cdy/cdyc.cdy` into T1 (`output/t1/`), which has the
   change but was built by the old translator;
2. T1 translates it into T2 (`output/t2/`), built by the new translator;
3. T2 must translate it into itself again (T3 = T2) and pass `mypy --strict`; only then
   does T2 replace `py/cdy_translator.py`.

`tst/py_cdy/test_self_host.py` fails while the copy here is stale. A feature that
`src/cdy/` itself uses takes two rebuilds: add it, rebuild, then use it, rebuild again.

**Bootstrapping.** The Python translator (`src/py_cdy/`) is frozen at tag `self-host-py`
and can't build today's `src/cdy/` (it has no `import`). To rebuild from nothing, check out
`self-host-py`, where it builds the translator from its files joined into one program, and
move forward from there.
