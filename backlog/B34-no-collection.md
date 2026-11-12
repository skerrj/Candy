# B34: No `Collection` interface

kind: leak
state: open
priority: normal
found: py-py-translator, 2026-10-17
fixed:
where: `src/cdy/system.cdy`, `src/cdy_rt/primitives.py`
refs: [[library.lists]], [[library.strings]]

Candy's collection operations are meant to work on an abstract `Collection`; today they
work on whatever Python accepts. `len`, `at`, `slice` and `in` work on lists, tuples and
strings (and `len` on maps), so their collection parameter is `Any` in `system.cdy`, and
`in` works on both strings and lists, as Python's `in`. Candy can't declare the interface
yet. Fix: interfaces. From `doc/archive/leaks_imvp_py_translator.md` ("No `Collection` interface yet", "`in` works on both")
and `doc/archive/leaks_system_prelude.md` ("Built-ins typed `Any`").
- 2026-11-10, Claude: narrowed by [[B166]] (`collections` step 6): each collection has
  its own typed operations, *for now*: `len`, `at`, `slice`, `contains` a list's;
  `str-len`, `char-at`, `substring`, `str-contains` a string's; `map-size` a map's; `in`
  is gone ([[library.builtins]]). What stays: one name for them all, which needs
  interfaces.
- 2026-11-11, the owner: a Candy syntax for constraints, a `where` in the `sig` (`(sig same
  (Fn (a a) Bool) (where (equatable a)))`), waits for interfaces; the names stay till then.
  Claude: two things it should answer, found in `collections-2` step 7: a variable has one
  constraint (an `equatable` that meets an `appendable` keeps only the `appendable`, and
  the end-of-definition check makes up the rest), and any type variable named for a
  constraint gets it, a `deft`'s too (`(deft (Box number) ...)`, unspecified, which fails
  mypy).
