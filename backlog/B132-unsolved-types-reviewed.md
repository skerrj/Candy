# B132: Go over the types the checker leaves unsolved

kind: task
state: open
priority: normal
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/check.cdy`, `src/cdy/emit.cdy`, `tst/py_cdy/test_self_host.py`
refs: [[B18]], [[B19]]

After `typed-core`, as the owner asked: a type variable the checker never solves (`?N`)
stays in Core and Python writes it `Any` (`doc/hl_rqmt/typed_core.md`, Question 2), but
no test covers it; `test_every_node_is_typed` checks only that every node was reached.
Go over the cases, with a test for each (the type in Core, and its Python):

- **`Any` meets a variable:** `Any` unifies with anything and binds nothing, so a
  generic built-in on an `Any`-typed value keeps its variable. All eight unsolved nodes
  in the translator's own Core (2026-10-31) are this: `map-keys` on a map whose values
  are `Any` (`core.cdy`, three calls), and `map-get` on `loaded`, a `(Map String Any)`
  (`expand.cdy`, `run` and the `fn` around it).
- **Nothing fixes it:** a `fn` never called, an `empty-list` never added to, `(put
  empty-list)`.

Then decide whether `Any` should bind a variable it meets (to `Any`), which overlaps
cutting `Any` down ([[B18]], `semantics`).
