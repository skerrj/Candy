# The frozen Python translator in its own repo (HLD)

**Status: proposal (draft).** Written on branch `system-prelude`; proposed as its own branch
after that one is merged, before or alongside the library branch
(`doc/hl_rqmt/library.md`), whose table work it makes simpler.

## Where things stand

- **The Python translator is frozen** at tag `self-host-py` (`src/py_cdy/`: `parse_cdy`,
  `core_cdy`, `lower_cdy`, `emit_py`, `translate_cdy`). It can't build today's
  `src/cdy/`; the checked-in `bin/py/cdy_translator.py` builds each new translator.
- **It still runs here,** and keeps code in step with it:
  - its own tests (`test_parse_cdy.py`, `test_core_cdy.py`, `test_lower_cdy.py`,
    `test_emit_py.py`), and the golden tests in `test_cdy_programs.py`, which translate
    `tst/cdy/` with it;
  - `main.py` translates with it unless given `--translator bin` or `t1`;
  - `self_host.py` uses `parse_cdy` to check that the Candy reader (`read.cdy`) reads
    what `parse_cdy` reads (`to_form`, `parse_forms`);
  - it reads the live `table.py`, so `table.py` keeps `arity` for it alone
    (`doc/hl_rqmt/system_prelude.md`, step 2 dropped; `doc/tech_debt.md`).
- **It is the only way to build Candy from scratch,** from a language that isn't Candy.
  Today that bootstrap is only implicit, in the history: each commit's `bin` was built by
  the one before.

## Goals

1. **This repo holds only Candy and its runtime:** `src/cdy/`, `src/cdy_rt/`, `bin/`, and
   the Python driver pieces (`self_host.py`, `main.py`, `reader.py`).
2. **The bootstrap is explicit and checked:** a separate repo can build Candy from the
   Python translator to today's `bin`, and says how.
3. **The runtime is free to change:** `table.py` loses `arity`, and nothing frozen reads
   it.

Not goals: a bootstrap from anything but Python; making old commits build faster.

## Proposal

### The bootstrap repo (`candy-bootstrap`, say)

- **Holds:** the Python translator as at tag `self-host-py`, with its tests; its own copy
  of the runtime (`cdy_rt`) as at that tag; and the parsec v4 dependency (as a pinned
  commit of the `functional-rewrite` branch).
- **A chain script** builds Candy from beginning to end:
  1. the Python translator builds `src/cdy/` at `self-host-py` (from this repo, checked
     out at that tag): T1;
  2. T1 builds the same source again: T2, which should equal the `bin` checked in there;
  3. each translator then builds the next step's `src/cdy/`, with that step's runtime,
     and the result is compared with that step's `bin`, up to `master`.
- **The steps are a list of commits, not just the tags:** some rebuilds needed staging
  (macros step 5; `system-prelude` step 5 copied the new `system.cdy` into `bin/py/`
  first), so a jump from one tag to the next may not build. The list records each step
  and any staging it needs.
- **Unverified:** that every step in the chain builds as recorded. Finding the steps is
  the first job, and the script checks them from then on.

### This repo, after the move

- **Removed:** `parse_cdy`, `core_cdy`, `lower_cdy`, `emit_py`, `translate_cdy` and their
  tests.
- **`test_cdy_programs.py`:** translates `tst/cdy/` with `bin` (as `test_self_host.py`
  already does with T1 and T2), still checked with `mypy --strict`.
- **`main.py`:** translates with `bin` by default; `--translator` keeps `t1`.
- **`self_host.py`:** the reader check against `parse_cdy` goes. The Candy reader is
  checked by its own tests (`tst/cdy/`, the error tests in `test_self_host.py`); the
  agreement test was for porting the reader, which is done.
- **`table.py`:** drops `arity` (the dropped step 2), and the tech debt entry goes.
- **Docs:** CLAUDE.md, `bin/README.md` and the iMVP doc point at the bootstrap repo;
  `doc/leaks.md` and the archives keep the Python translator's leaks as history.

## Steps (sketch)

1. **Find the chain:** walk the commits from `self-host-py` to `master`, building each
   `bin` with the one before; record the steps and any staging.
2. **The bootstrap repo:** the Python translator, its runtime, the pinned parsec and the
   chain script; it passes from scratch.
3. **Remove it here:** the files, tests and the `main.py` default; `test_cdy_programs.py`
   on `bin`.
4. **`table.py` without `arity`.**
5. **Docs.**

## Questions (open)

1. **Repo or history:** a separate repo (proposed), or a chain script in this repo that
   checks out old commits (less work, the bootstrap less visible)?
2. **Name:** `candy-bootstrap`?
3. **The reader agreement check:** drop it (proposed), or move it to the bootstrap repo?
4. **parsec v4:** pin a commit in the bootstrap repo, or vendor a copy?
5. **Order:** before the library branch, or with it?
