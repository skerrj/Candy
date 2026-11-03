# B136: A `match` pattern names every field

kind: idea
state: open
priority: normal
found: typed-core, 2026-10-31
fixed:
where: `src/cdy/core.cdy`, `src/cdy/lower.cdy`, `spec/30-match.md`
refs: [[B69]], [[B121]], [[match.sum-types]]

A variant pattern binds each field by position, so it has to name all of them:
`((Call callee args _ _) ...)`. Adding a field to a variant then touches every clause
that takes it apart, even those that only want one field. On the translator's Core this
is the main cost of growing it: `type-checker` added a `pos` to the compound nodes,
`typed-core` a `pos` to the leaves and then a `t` to every node, each about 180 sites in
`core.cdy`, `check.cdy`, `lower.cdy` and `emit.cdy` (`typed-core` step 2 used a
throwaway script that read the files as forms). Later branches that grow Core
(`semantics`, a second backend) will pay it again.

Ways out, from other languages:

- **A rest wildcard:** `(Call callee ..)` binds the first fields and ignores the rest
  (Rust's `..`, Erlang records' `_ = '_'`).
- **Fields by name:** `(Call :callee c)`, binding only the fields named (OCaml's `{ x;
  _ }`, Elm's record patterns, Rust's `Call { callee, .. }`); positional patterns stay.
- **`get` on the subject in the clause:** works today for a field every variant has, but
  not for one variant's own fields, since the subject isn't narrowed ([[B121]]).

Found in `typed-core`'s review ("Looking back" in `doc/hl_rqmt/typed_core.md`).

## Notes

- 2026-10-31, the owner and Claude: term rewriting systems (OBJ3, Maude, Pure) meet the
  same problem, a rule's left side naming every argument of a constructor, and answer it
  two ways, both worth weighing here:
  - **Matching modulo a theory (OBJ3, Maude):** an operator declared `assoc comm id:` is
    matched modulo those equations. Maude's objects, `< O : C | a1 : v1, a2 : v2 >`, keep
    their attributes in an associative-commutative set, so a rule writes `< A : Account
    | bal : N, Atts >`, `Atts` matching the other attributes in any order; Full Maude's
    object-oriented modules let a rule leave out the attributes it doesn't touch. A
    fourth option for Candy: a record's fields as a set of (name, value) pairs, matched
    modulo order, with a variable for the rest (`((Call (callee c) . rest) ...)`); fields
    by name and the rest wildcard in one, and an `assoc`-like update with it.
  - **Generic traversal (Stratego's strategies; Haskell's "Scrap Your Boilerplate",
    Uniplate):** much of the churn isn't clauses that want a field but passes that walk
    the whole tree and rebuild each node (`retype` and its helpers in `check.cdy`,
    `has-lambda` in `lower.cdy`, `bound-locals` in `emit.cdy`). Strategic rewriting
    separates the rules from the traversal: one rule for the node that matters, and a
    combinator (`all`, `topdown`, `bottomup`) for the rest, which never names their
    fields. Maybe an `idea` of its own later. (Not counted yet: how many of the ~180
    sites are traversals.)
  - **Pure** (evaluation as term rewriting) has positional constructor patterns, as
    Candy does: the problem, not a fix. Candy already rewrites in two places, macros
    (forms to forms) and `lower` (Core to the lowered IR, close to a set of rewrite
    rules), so these ideas would serve the translator as much as programs.
- 2026-11-01, the owner: the semantics HLD (Question 8) narrows a `match` clause's subject
  local to its variant ([[B121]]) *for now*; the ML way, no narrowing, with patterns that
  needn't name every field (this item) and as-patterns (Haskell's `s@(A x)`), is the
  alternative to revisit with this item.
