# One backlog: items with a kind and a state (process HLD)

**Kind: process** (how work is done), not a design of the language or translator.
**Status: draft (2026-10-25), questions open.** For a branch of its own, after
`executable-spec`. From the owner (2026-10-25): "we could just have an open backlog, with
`leaks`, `tech_debt`, `defect`, `task`, and others... `open` being a `state` of the
item". It takes in `review.md` (a draft with a goal only: "an improved way to review items
and tasks"), which it replaces, since a review becomes a state of an item.

## Where things stand

Work that isn't done yet is spread over lists, each its own file, and an entry's kind is
the file it is in:

| List | What | Lifecycle |
|---|---|---|
| `doc/leaks.md` | a shortcut where Python shows through | archived per branch into `doc/archive/leaks_*.md` (ten files), which "still apply until struck through" |
| `doc/tech_debt.md` | a shortcut a Candy user can't see | one file; an entry is removed when fixed |
| `TODOS.md` | tasks, and "Review step N as built" | archived per branch into `doc/archive/TODOS_*.md`, open items carried over (some for several branches) |
| `doc/brainstorm.md` | undecided ideas | one file; an idea moves to an HLD, leaving a pointer |

There is no list for defects: the translator doing something wrong by Candy's own rules.
They are filed as leaks or tech debt, or nowhere.

**An audit (2026-10-25, on `executable-spec`)** found what that costs:

- **Defects filed as leaks or tech debt**, each checked against T1:

  | # | Defect | Filed now |
  |---|---|---|
  | 1 | `a-b` and `a_b` are one Python name: `(def a-b 1)` and `(def a_b 2)` print `2 2`, with no error | an iMVP leak, which said the translator reports it (that was the Python translator; corrected) |
  | 2 | `(sig x (List))` crashes the translator (`IndexError`) | tech debt |
  | 3 | `(def (x) 1)` gets " needs a (sig  Type) before its definition", with no name | tech debt |
  | 4 | a record field `_x` translates, and fails at run time (`ValueError`) | an iMVP leak says it "can't", but nothing rejects it |
  | 5 | a record with the same field twice translates (a one-field class) | `doc/leaks.md` |
  | 6 | a lowercase record name is accepted | `doc/leaks.md` |
  | 7 | `(fn (x x) x)` is accepted | `doc/leaks.md` |
  | 8 | `nil` can be defined | `doc/leaks.md` |
  | 9 | a record constructor's arity isn't checked (a variant's is) | `doc/leaks.md` |
  | 10 | a `deft` variant named like a macro isn't rejected | tech debt (in the `expand.cdy` entry) |
  | 11 | module prefixes can collide with mangled names (`util--greet`) | tech debt |
  | 12 | a `cond` of about 200 clauses, used as a value, doesn't compile | tech debt |
  | 13 | a few errors have no position | tech debt |

- **Fixed, never struck through:** the runtime's `py-mangle` and `py-repr` (fixed on
  `library`), and the opaque symbol table (fixed on `symbol-table`), in
  `leaks_pre_self_host.md` and `tech_debt.md`. Struck (or removed) on `executable-spec`.
- **Partly fixed:** "Forms are `Any`: Candy has no sum types yet" (iMVP): the translator's
  `Form` is a sum; only `tst/cdy/read_sexpr.cdy` still uses `Any`.
- **Duplicated:** the test programs' one-at-a-time mypy, twice in `tech_debt.md`. Merged
  on `executable-spec`.
- **In the wrong list:** `slurp`'s fallback search, and "a type from a module the file
  doesn't import isn't caught", are in the tech debt, but a Candy user sees both.

**Also to track, beyond the audit:** `def`'s mutability is undefined, neither a constant
nor a variable (`doc/hl_rqmt/mutation_optimization.md`, open question 4;
`spec/20-types.md`). The owner (2026-10-25): "this will eventually be an issue... if it's
undefined as either we should track it". A `task` (decide it), open.

The cause is the same each time: an entry's kind is where it is filed, and its state is a
strike-through, so a kind can be wrong and a state can be stale without anything noticing.

## Goals

- One backlog: each item has a **kind** and a **state**, kept apart.
- Nothing archived by branch: an item is open until it is done, and says where it was found
  and where it was fixed.
- Reviews as a state of an item, not items of their own (the goal of `review.md`).
- Cheap for Claude Code to read (the scale lesson of `doc/hl_rqmt/executable_spec.md`):
  finding an item doesn't mean reading them all.
- Checked: a test that every item has a known kind and state.

## Proposal

### An item

- **id:** `B1`, `B2`, ... (never reused), so a spec's *for now*, an HLD or a commit can
  cite it.
- **kind:**
  - `defect`: the translator or runtime gets something wrong by Candy's own rules (the
    spec, the HLDs): a crash, wrong output, a garbled message, a form accepted that a rule
    forbids. Fixed by a fix.
  - `leak`: a deliberate shortcut where Python shows through. Fixed by design.
  - `tech-debt`: a shortcut a Candy user can't see.
  - `feature`: something not implemented that the owner has agreed to implement (the
    owner, 2026-10-25). Its HLD's steps are its tasks.
  - `task`: work to do (an HLD's step, a follow-up, a decision to make).
  - `idea`: a crazy thought, not agreed to (the owner, 2026-10-25): what
    `doc/brainstorm.md` holds. Agreed to, it becomes a `feature`; or it is `dropped`
    (question 3).
- **state:** `open`, `in-progress`, `review` (built; the owner checks it), `done`,
  `dropped` (with why).
- **found:** the branch and date; **fixed:** the branch, once `done`.
- **where:** the files involved; **refs:** the spec file, HLD or other item.
- **repro**, for a defect: the smallest program that shows it. It could be a spec-style
  example of the *correct* behaviour, run as an expected failure until the defect is fixed,
  so a fix is reported as it lands (question 4).

A step's review is the step's `task` going to `review`: "Review step N as built" is no
longer an item of its own. The owner's verdict ("looks ok for now") goes on the item.

### Where it lives (question 1)

- **A.** One file, `doc/backlog.md`, a section per item. Simple; over a hundred items, read
  whole.
- **B.** A directory, `backlog/`, one small file per item (`B12-sig-list-crash.md`, with
  its fields at the top), and an index generated from them (by kind and state), which a
  test checks is current. Scales; more files.

### What it replaces (question 2)

`doc/leaks.md` and its archives, `doc/tech_debt.md`, and `TODOS.md`. Not
`doc/brainstorm.md`, unless its entries move in as `idea`s (question 3).
The archives stay as history; their open entries become items.

## Pros and cons

**Pros:**

- A kind and a state that can be checked, instead of a file and a strike-through.
- No archiving, so nothing open is lost in an archive (ten leak files today).
- Defects get a name, and with a repro, a test.
- Reviews have a place in the lifecycle that isn't a list carried from branch to branch.

**Cons:**

- A migration: every open entry (well over a hundred) becomes an item, and the pointers
  move with them (the spec's *for now* lines, CLAUDE.md, `doc/process.md`, recent HLDs).
  The old HLDs keep theirs, as history.
- A new format for both the owner and Claude Code to learn, and a test to keep.
- Option B is more files to navigate by hand.

**Timing:** after `executable-spec` merges, as its own branch. The spec now cites leaks by
file; doing this before more features cite more of them keeps the move small. The defects
found on `executable-spec` (above) are the first items.

## Steps (sketch)

1. The format, and the test that checks it.
2. The migration: leaks (current and archived), tech debt, TODOS, with the audit's
   corrections (the defects reclassified).
3. The pointers: the spec, CLAUDE.md, `doc/process.md`.
4. The process (`doc/process.md`): the lifecycle's review step, "Where notes go", the
   start of a branch (no more archiving).
5. Docs.

## Questions

1. **One file or a directory** (A or B, "Where it lives")?
2. **What it replaces:** leaks, tech debt and TODOS (proposed), or also `brainstorm.md`?
3. **`brainstorm.md`:** move its entries in as `idea`s (so an idea agreed to becomes a
   `feature` in place), or keep it as a file of its own?
4. **Defect repros as expected failures:** run them (a `candy defect` block, or spec
   examples marked by item id), or keep them as text?
5. **States:** are `open`, `in-progress`, `review`, `done` and `dropped` the right ones?
6. **Ids:** a plain number (`B12`), or a prefix by kind (`D3`, `L12`)? A prefix says the
   kind, but an item reclassified (as the audit's defects are) would change its id.
