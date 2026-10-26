# B3: `a-b` and `a_b` are one Python name

kind: defect
state: open
priority: normal
found: py-py-translator, 2026-10-15
fixed:
where: `src/cdy/emit.cdy` (`py-mangle`)
refs: [[syntax.names]], [[B12]]

`py-mangle` turns `-` into `_`, so `a-b` and `a_b` become one Python name, and the second
definition silently replaces the first: wrong output, with no error. The iMVP's leak list
said the translator reports it; that was the Python translator's check, which the Candy
translator never had. Fix: reject two names that mangle alike in one scope, or mangle
injectively. From `doc/archive/leaks_imvp_py_translator.md` ("Name mangling can
collide"); the audit's defect 1 (`doc/hl_rqmt/tracking.md`). Related: [[B12]].

## Repro

Prints `2 2`. Whether the fix is an error or a renaming is still to decide, so this repro is text:

```candy
(sig a-b Int)
(def a-b 1)
(sig a_b Int)
(def a_b 2)
(put a-b a_b)
```
