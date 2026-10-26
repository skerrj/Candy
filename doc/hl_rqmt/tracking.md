# Rule ids, links, and one backlog (process HLD)

**Kind: process** (how work is done), not a design of the language or translator.
**Status: draft (2026-10-25), questions open.** For a branch `tracking`, after
`executable-spec` (this file was `backlog.md`). Two sources:

- **The backlog,** from the owner (2026-10-25): "we could just have an open backlog, with
  `leaks`, `tech_debt`, `defect`, `task`, and others... `open` being a `state` of the
  item". It takes in `review.md` (a draft with a goal only: "an improved way to review
  items and tasks"), which it replaces, since a review becomes a state of an item.
- **Ids and links,** from an updated chat with the owner
  (`doc/archive/chat_spec_by_example.md`, section 4b, "machine spec + generated human
  spec", 2026-10-24, with a prototype, `tools/specbook.py`, not kept): every rule has a stable id, and everything refers to it by id,
  never by file path. That chat couldn't see the repo, so its examples aren't Candy (fields
  without types, `_` for `else`), and some of it reopens questions the executable spec
  answered; those are flagged here ("Left out of the chat"), not taken.

The two belong together: a backlog item needs an id, and so do the rules it is about.

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

**References are file paths.** The spec's *for now* lines point at `doc/leaks.md` and
`doc/archive/leaks_*.md`, the HLDs at each other's sections by heading, and nothing checks
any of it. So moving a leak (as the backlog's migration would) means finding and rewriting
every pointer to it, and a pointer that goes stale stays stale. `executable-spec` moved
`candy-special.md` this way, by `git grep`.

## Goals

- One backlog: each item has a **kind** and a **state**, kept apart.
- Nothing archived by branch: an item is open until it is done, and says where it was found
  and where it was fixed.
- Reviews as a state of an item, not items of their own (the goal of `review.md`).
- Cheap for Claude Code to read (the scale lesson of `doc/hl_rqmt/executable_spec.md`):
  finding an item doesn't mean reading them all.
- Checked: a test that every item has a known kind and state.
- **Stable ids** for spec rules, backlog items and HLD sections, and links by id
  (`[[match.exhaustive]]`) instead of by file path, checked by a test: an unknown id is an
  error.
- From a rule, its open items: the defects, leaks and tasks against it.

## Proposal

### Ids and links

- **A spec rule's id** is an anchor on its heading in the existing `spec/` files:
  `## Exhaustive {#match.exhaustive}`. The files stay as they are (prose and examples
  together, `candy errors` tables one line a case); a block belongs to the rule whose
  heading it is under. Ids are dotted, by feature (`match.exhaustive`, `syntax.char`).
- **An HLD section's id** is an anchor on its heading too (`{#design.sum-types}`), only
  where something links to it.
- **A backlog item's id** is its number (`B12`, "An item").
- **A link** is `[[id]]`, anywhere in `spec/`, `doc/` and the backlog. A test reads them
  all and fails on an id nothing defines, or one defined twice; an id that is renamed
  keeps the old one as an alias (question 9).
- **The checks from the chat that fit:** an unknown id, a duplicate id, a stable rule with
  no example (an error); a rule no HLD links to (a warning: missing rationale?).

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
- **where:** the files involved; **refs:** the ids it is about (`[[match.exhaustive]]`,
  `[[B3]]`), so a rule's open items can be listed from the rule.
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

### Left out of the chat (section 4b)

- **One rule per file, examples as separate `.cdy` + `.out`/`.err` files.** The spec has
  201 examples, many a one-line row of a `candy errors` table: that would be hundreds of
  files, with a rule's prose in one folder and its examples in another (a con the chat
  lists itself). Ids on the headings of today's files give the links without the move.
  Real `.cdy` files would get the editor's highlighting; so would a Markdown injection in
  `editors/vscode-candy/` (question 10).
- **Four conflicts with the executable spec's answers** (`doc/hl_rqmt/executable_spec.md`),
  each a question here, not taken:
  - `grammar.ebnf` as the syntax authority: question 6 there, the reader is the authority,
    *for now* (question 11);
  - coded errors (`E0012`): question 4 there, substrings, *for now* (question 11);
  - a `CHANGELOG.md` for each rule's history: question 7 there, none, *lasting*; a rule's
    history can be the HLDs that link to it, and its `since:` (question 11);
  - examples printing values (`Square(2)`): question 12 there, numbers and text, *for
    now* (question 11).
- **The stage 0/1/2 gate** is what Candy has: `bin` (stage 0), T1 and T2, the fixpoint,
  and the bootstrap chain (`doc/hl_rqmt/bootstrap.md`).
- **The generated book** (a page per rule: the rule, its syntax, examples, "why" from the
  HLDs that link to it, history, backlinks): later, once the ids exist; the check matters
  more than the site (question 12).

## Pros and cons

**Pros:**

- A kind and a state that can be checked, instead of a file and a strike-through.
- No archiving, so nothing open is lost in an archive (ten leak files today).
- Defects get a name, and with a repro, a test.
- Reviews have a place in the lifecycle that isn't a list carried from branch to branch.
- Links that can't go stale unnoticed, and a move that rewrites no pointers: an id stays
  where its target goes.
- A rule's page (or a search for its id) finds its rationale and its open items.

**Cons:**

- A migration: every open entry (well over a hundred) becomes an item, and the pointers
  move with them (the spec's *for now* lines, CLAUDE.md, `doc/process.md`, recent HLDs).
  The old HLDs keep theirs, as history.
- A new format for both the owner and Claude Code to learn, and a test to keep.
- Option B is more files to navigate by hand.
- Id discipline: naming, no reuse, aliases for renames (a con the chat lists too).
- Two migrations at once (ids on the spec and HLDs, and the backlog), though the ids make
  the backlog's cheaper.

**Timing:** after `executable-spec` merges, as its own branch. The spec now cites leaks by
file; doing this before more features cite more of them keeps the move small, and ids
first means the backlog's migration rewrites each pointer once, to an id. The defects
found on `executable-spec` (above) are the first items.

## Steps (sketch)

1. Ids and links: the anchors on the spec's headings (and the HLD sections linked to),
   and the test that checks every `[[id]]`.
2. The backlog's format, and the test that checks it.
3. The migration: leaks (current and archived), tech debt, TODOS, with the audit's
   corrections (the defects reclassified); every pointer to them becomes a link.
4. The process (`doc/process.md`): the lifecycle's review step, "Where notes go", the
   start of a branch (no more archiving), ids and links.
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
7. **Rule ids:** anchors on the headings of today's spec files (proposed), or the chat's
   one rule per file with front matter?
8. **What gets an id:** every spec section, or only those something links to? Every
   section makes "a stable rule with no example" checkable everywhere.
9. **Renames:** keep the old id as an alias (the chat's `aliases:`), or rewrite the links
   (a test finds them all)?
10. **Examples as `.cdy` files** for highlighting, or a Markdown injection for `candy`
    fences in `editors/vscode-candy/`?
11. **The four conflicts** ("Left out of the chat"): `grammar.ebnf`, error codes, a
    changelog, printing values. Proposed: keep the executable spec's answers; reopen one
    only on its own (each has a *for now* to revisit).
12. **The book:** in this HLD's steps, or later?
