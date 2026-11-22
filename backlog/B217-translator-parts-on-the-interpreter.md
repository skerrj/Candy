# B217: Parts of the translator on the interpreter

kind: idea
state: open
priority: low
found: interpreter, 2026-11-21
fixed:
where: `src/cdy/interp.cdy`, `tst/py_cdy/`
refs: [[B101]]

The interpreter's tests are the spec's examples and the test programs
(`doc/hl_rqmt/interpreter.md`, Question 1); the translator, a far larger real program,
would take minutes on a tree-walker. Instead, run one of its modules or functions at a
time on the interpreter, when a change needs it, and compare the result with the
compiled one's: the reader (`read.cdy`'s `read-forms`) on every spec file's examples,
`syntax.cdy`'s shape check, `check.cdy`'s unification on the test programs' types. It
needs a way to call one interpreted function from a test (`interp.call`, a global by its
key, with `Value`s in and out), and the translator's modules small enough to load on
their own.

## Notes

- 2026-11-21, the owner: an idea, from the interpreter HLD's Question 1; and when the
  interpreter is optimized, its speed should not be an issue.
- 2026-11-21, the owner, on Claude's view: the whole translator interpreted is of little
  practical use, even optimized (it runs only where the compiled translator already
  does, and the self-host fixpoint tests it compiled); parts only. Removed from the text:

  ```text
  Once the interpreter is optimized (resolved names and slots in place of maps,
  a closure compiled per node rather than a walk of Core each time), speed stops being the
  reason not to, and the whole translator can run on it too.
  ```
