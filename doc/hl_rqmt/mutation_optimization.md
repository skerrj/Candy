# Candy mutation and optimization (placeholder)

**Status: placeholder.** Neither topic is in the iMVP (see `doc/hl_rqmt/iMVP_py_translator.md`).
This document collects ideas and questions so they aren't lost, and so the iMVP doesn't
design them out by accident. Nothing here is decided.

## Mutation

### Where the iMVP stands

- **`def`'s mutability is undefined.** `candy-special.md` called it "not immutable... for
  now", but no form changes a `def`'s value, and defining a name twice is an error, so a
  `def` is neither a constant nor a variable yet (`spec/20-types.md` says it is open). It
  becomes an issue once a form that changes a value arrives, or a target where the two
  differ (a C constant, a JavaScript `const`): open question 4, and an item for the
  backlog (`doc/hl_rqmt/tracking.md`).
- `deft` records are immutable. They are Python `NamedTuple`s, and `assoc` returns a copy.
  Mutating a record (Carp's `set-x!`) is **skipped for the iMVP**.

### Ideas

- **Mutable records.** A `set!`-style form (`(set! v x 3)`, say) that changes a field in
  place. In Python this needs a class other than `NamedTuple`, such as a plain class with
  `__slots__`. It also needs a way to say which records are mutable: per type
  (`deft` versus a `deft!`) or per value.
- **Ownership, as in Carp.** Carp tracks ownership and borrowing statically, so mutation is
  safe and memory is freed without a garbage collector. This matters most for a target
  without GC, such as C (see `doc/hl_rqmt/multi_target.md`).
- **Transients, as in Clojure.** Values are immutable by default. A local, temporarily
  mutable copy is used for batches of updates and then frozen again.
- **`def` itself.** Should `def` become immutable once the bootstrap is done, with a
  separate form for mutable variables?

### Open questions

1. Is mutation part of the language, or only an optimization (see below)?
2. How does the type checker see mutability: in the type, in the signature statement, or
   not at all?
3. Which targets constrain the answer? Python can do anything; C needs memory management.
4. **Is a `def` a constant?** (the owner, 2026-10-25: "this will eventually be an issue...
   if it's undefined as either we should track it"). Today it is undefined: decide it
   before any form changes a value, and say so in `spec/20-types.md`.

## Optimization

The iMVP favours the simplest translation that works. Optimizations come later, and most
belong in Core → Core passes or in `lower`, so every target benefits.

### Ideas

- **In-place `assoc`.** When the old value can't be reached any more, `assoc` can update it
  in place instead of copying it. Koka (Perceus) and Lean do this with reference counts;
  Carp's ownership tracking gives the same information statically. This would make
  immutable records about as cheap as mutable ones.
- **Tail calls.** Python has no tail-call optimization and limits recursion depth, which
  matters for a self-hosted compiler written in a recursive style. Options:
  - turn a self tail call into a `while` loop in `lower`;
  - use trampolines for mutual recursion;
  - add a `loop`/`recur` form, as in Clojure.
- **Applied lambdas.** `let` is already defined as an applied lambda and turned back into
  assignments by `lower` (a beta-reduction). The same rule could apply to applied `fn`s
  that the user writes.
- **Lists that are cheap to add to.** `(List a)` is a Python tuple, so `(+ acc (to-list
  x))` copies it and a loop that builds a list is quadratic (`map` in Candy took 506 ms
  for 16000 items; built in, 0.67 ms). Options: a cons list or a persistent vector
  (Clojure's) as the runtime's list, or in-place appends where the old list can't be
  reached any more (as for `assoc`, above). Until then, `map`, `filter` and `fold` are
  built-ins (`doc/hl_rqmt/system_prelude.md`, step 5).
- **Inlining and constant folding**, for small functions and constant arithmetic.
- **Fewer temporaries.** `lower` adds temporaries to keep evaluation order. An analysis of
  which expressions have no side effects would let it skip more of them.

### Open questions

1. Which optimizations does the self-hosted compiler need just to run? Tail calls are the
   likeliest.
2. Where does each one run: in Core (shared by every target), in `lower` (shared by
   statement-based targets), or in a backend?
