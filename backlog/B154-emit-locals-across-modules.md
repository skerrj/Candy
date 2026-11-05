# B154: emit bound one module's locals into another's functions

kind: defect
state: done
priority: high
found: semantics step 4, 2026-11-02
fixed: semantics
where: `src/cdy/emit.cdy`, `src/cdy/cdyc.cdy`
refs: [[B143]], [[programs.import]]

`python-of` (`src/cdy/cdyc.cdy`) put every module's top-level locals' Python names into
one map, but a local's id is unique only within its module: a top-level function's
parameter could take another module's local's name. The prelude's `rest` had its `xs`
written `v` once the prelude's new `with-default` bound a `v`; it predates the branch
(boot/47's translator does it too). No `candy run` repro: the program still ran, since
the name it took was the same local's, only spelled as another module's.

## Notes

- 2026-11-02, Claude: fixed in semantics step 4: `emit-func` binds a function's locals
  from an empty map (`(assoc env locals empty-map)`), so a function sees only its own.
