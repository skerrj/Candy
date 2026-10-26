# Rule ids, links, and one backlog (process HLD)

**Kind: process** (how work is done), not a design of the language or translator.
**Status: accepted (2026-10-25), with all thirteen questions answered; branch `tracking`.** For a branch `tracking`, after
`executable-spec` (this file was `backlog.md`). Two sources:

- **The backlog,** from the owner (2026-10-25): "we could just have an open backlog, with
  `leaks`, `tech_debt`, `defect`, `task`, and others... `open` being a `state` of the
  item". It takes in `review.md` (a draft with a goal only: "an improved way to review
  items and tasks"), which it replaces, since a review becomes a state of an item.
- **Ids and links,** from an updated chat with the owner
  (`doc/archive/chat_spec_by_example.md`, section 4b, "machine spec + generated human
  spec", 2026-10-24, with a prototype, `tools/specbook.py`, not kept): every rule has a
  stable id, and everything refers to it by id, never by file path. That chat couldn't see
  the repo, so its examples aren't Candy (fields without types, `_` for `else`), and some
  of it reopens questions the executable spec answered; those are flagged here ("Left out
  of the chat"), not taken.

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

- **A spec rule's id** is an anchor in the existing `spec/` files, on the line before a
  heading or a rule's paragraph: `<a id="match.exhaustive"></a>` (invisible when rendered,
  and a browser can link to `30-match.md#match.exhaustive`; the chat's `{#id}` shows
  literally on GitHub). The files stay as they are (prose and examples together,
  `candy errors` tables one line a case); a block belongs to the rule of the anchor above
  it, up to the next. So ids can be finer than headings ("Taking it apart: match" holds
  several rules). Ids are dotted, by feature (`match.exhaustive`, `syntax.char`).
- **An HLD section's id** is an anchor the same way (`<a id="design.sum-types"></a>`),
  only where something links to it.
- **A backlog item's id** is its number (`B12`, "An item").
- **A link** is `[[id]]`, in any tracked Markdown file (`spec/`, `doc/`, `backlog/`,
  CLAUDE.md, the READMEs). A test reads them all and fails on an id nothing defines, or
  one defined twice; an id that is renamed keeps the old one as an alias, for history, and
  the live links move to the new one (question 9).
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
  `dropped` (with why), or `kept`: a leak or shortcut kept on purpose, a *lasting* answer,
  so it describes Candy but isn't work (question 5). A `kept` **leak** is a language rule
  now: the spec states it, without *for now*, as lasting, and the item refers to the rule
  (`[[id]]`; the rule may link back for the reason). A `kept` **tech-debt** item has no
  rule to state (a Candy user can't see it): its reason is in the item. An item goes open → in-progress → review → done (or back to in-progress); no
  `blocked` (a ref says "needs `[[B3]]`") and no `deferred` (`open`, priority `low`).
- **priority:** `high`, `normal` (the default) or `low`; set by the owner (Claude Code may
  propose one); the index sorts by it (question 13). How bad a defect is (severity) is a
  reason for its priority, in its text, not a field.
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

`doc/leaks.md` and its archives, `doc/tech_debt.md`, and `TODOS.md`. `doc/brainstorm.md`
stays, for quick notes; a written-up entry moves in as an `idea` (question 3).
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

1. **Ids and links:** an `<a id>` anchor on every rule in `spec/` (about 60; questions 7
   and 8), and a test that reads every tracked `.md`: an unknown or duplicate id fails, a
   stable rule with no example fails, a block outside any rule fails, an alias used in a
   live doc fails, and an id gone from `master` with no alias warns (question 9).

   *Done. As built:* `script/doc_links.py` reads a doc's fences (moved out of
   `tst/py_cdy/test_spec.py`, which now imports it), its prose (outside fences, with code
   spans blanked), its anchors (the first on a line the id, the rest its aliases) and its
   links, and lists the tracked `.md` files (at a commit too). `spec/` has 51 anchors,
   one before each heading, or before each rule's paragraph in a section with several;
   a rule's examples run to the next anchor. `tst/py_cdy/test_doc_links.py` checks that
   ids are dotted and lowercase and defined once, that links are to ids, and that a live
   doc (not `doc/archive/`) links to an id, not an alias; in `spec/`, that no example
   comes before the first anchor and that each rule of a stable file has an example or
   says where it is "*Tested in*"; and it warns of an id on `master` (the merge base)
   that is gone. The check found four rules with no example: the operators' arity and
   the shape of `fn` got a sentence over their error tables, flat patterns an error
   table, the library's other built-ins a run example, and type checking (mypy) a
   *Tested in*. `spec/README.md` says how ids, aliases and links are written. There are
   no links yet: the backlog (step 2) is the first to use them.
2. **The backlog's format:** `backlog/B<n>-<slug>.md` with its fields (kind, state,
   priority, found, fixed, where, refs), the script that writes `backlog/README.md` (by
   state, kind and priority, and open items by the rule ids they refer to: question 12),
   and the test that checks every item and that the index is current. The spec runner
   also collects defect repros from `backlog/`, as expected failures (question 4).

   *Done. As built:* an item is `backlog/B<n>-<slug>.md`: a title line, `# B<n>: what it
   is`, a blank line, then its seven fields, one `name: value` line each, in order (kind,
   state, priority, found, fixed, where, refs; `fixed` and `where` may be empty, `refs` is
   links only), then its text, like a spec file's status line. `script/backlog.py` reads
   the items (`item`, `items`), and writes `backlog/README.md` (`--check` only checks it):
   the next free id, the open items (open, in-progress, review) by priority, then the
   open items by the ids in their refs, each a link to the rule's file, then the closed
   ones. It fails on a bad file name or title, a missing or out-of-order field, an unknown
   kind, state or priority, a `done` item with no `fixed`, a closed item that still has a
   repro, and two items with one number. `tst/py_cdy/test_backlog.py` checks every item
   and that the index is current; `test_doc_links.py` takes an item's id from its file
   name, so `[[B2]]` is checked like any link; `test_spec.py` runs each item's `candy run`
   and `candy error` blocks as strict expected failures (`xfail(strict=True)`), so a fix
   fails the test until its example moves into the spec. The first two items:
   [[B1]], the Markdown injection (question 10, a `task`, `low`), linked from the
   extension's README (its "Not yet" got an anchor, `editor.not-yet`), and [[B2]], the
   audit's defect 2, `(sig x (List))`, with a repro (its `doc/tech_debt.md` entry now
   points at it). The rest of the migration is step 3.
3. **The migration:** the open entries of `doc/leaks.md` and its archives,
   `doc/tech_debt.md` and `TODOS.md` become items (the audit's defects as `defect`s; every
   leak `open`, unless the owner keeps it, when its rule goes into the spec), and
   `brainstorm.md`'s written-up entries as `idea`s, its settled ones removed (question 3).
   The three files go (question 2); every pointer to them becomes a link. First items
   besides: `def`'s mutability (a `task`), the Markdown injection for `candy` fences (a
   `task`, `low`: question 10), the book (an `idea`: question 12).

   *Done. As built:* 100 items, `B3` to `B102`, written by a one-off script (not kept),
   each with its `found:` from the commit that first recorded it:
   - **12 defects,** the rest of the audit's 13 (`B3` to `B14`); 8 have a repro that runs
     (`B2`, `B4` to `B8`, `B10`, `B11`), whose expected message is what the nearest
     existing check says (`must be different`, `Capitalised, not v`, `takes 1 field(s)`);
     the others are text, since their fix is a decision (`B3`, `B9`) or the repro needs
     two files or 200 lines;
   - **40 leaks** (`B15` to `B54`), merged where two lists said the same thing (records
     and variants as `NamedTuple`s; `Maybe` as `Optional`, with its collapse; the
     operators', `tup`'s and `put`'s missing variadic type; `get` and `assoc`), with the
     two tech-debt entries a user sees (`B53`, `B54`); every one `open`, none kept;
   - **25 tech-debt items** (`B55` to `B79`), with three iMVP leaks a user can't see
     (`B77`, `B78`, and `B79`, what is left of "Forms are `Any`");
   - **13 tasks:** `def`'s mutability (`B80`), the carried-over `TODOS.md` items (`B81` to
     `B87`; the reviews in state `review`), and this HLD's five steps (`B88` to `B92`;
     1 to 3 in `review`). "Check the iMVP's and pre-self-host's leak lists" is in step
     3's review, since every entry in them is now an item;
   - **10 ideas:** `brainstorm.md`'s nine written-up entries (`B93` to `B101`) and the
     book (`B102`).

   `doc/leaks.md`, `doc/tech_debt.md` and `TODOS.md` are removed; `brainstorm.md` keeps
   its one-line notes, loses the three settled entries, and says when an entry moves. The
   pointers in `spec/`, `README.md` and the `.cdy` comments (`system.cdy`, so `bin/py/`'s
   copy too, and `emit.cdy`) are now links to items. `doc/process.md` and CLAUDE.md still
   describe the old lists: steps 4 and 5. Every priority is `normal` (`B1` `low`), for the
   owner to set. The index escapes a `|` in a title.
4. **The process** (`doc/process.md`): the lifecycle's review step (a task goes to
   `review`), starting a branch without archiving, "Where notes go" (the backlog, ids and
   links), and the log.

   *Done. As built:* `doc/process.md`: starting a branch adds a task per HLD step (and a
   language feature's `feature` item) instead of archiving; a step records what it finds
   as items, closes the items it fixes, and moves its task to `review` with the index
   rewritten, instead of a `TODOS.md` item; the review works through the `review` items,
   the verdict on each; a *for now* links to its item; "The spec" says a gap gets an item
   and every rule an id; a new section, "The backlog" (kinds, states, priority, ids,
   links, repros); "Where notes go" points at the backlog and the archives; and the log.
5. **Docs:** CLAUDE.md, `spec/README.md` (anchors), the HLDs that pointed at the lists.

## Questions

1. **One file or a directory** (A or B, "Where it lives")?
   *Answered (2026-10-25):* B, a directory `backlog/`, one file per item, with a generated
   index checked by a test (the scale argument: finding an item doesn't mean reading them
   all). *Lasting.*
2. **What it replaces:** leaks, tech debt and TODOS (proposed), or also `brainstorm.md`?
   *Answered (2026-10-25):* all three: `doc/leaks.md`, `doc/tech_debt.md` and `TODOS.md`
   become items, and the files are removed (no pointers left behind); the archives
   (`doc/archive/leaks_*.md`, `TODOS_*.md`) stay as history, and starting a branch no
   longer archives anything. "What's left on this branch" comes from the index (by
   `found:`, or a branch field). `brainstorm.md` is question 3. *Lasting.*
3. **`brainstorm.md`:** move its entries in as `idea`s (so an idea agreed to becomes a
   `feature` in place), or keep it as a file of its own?
   *Answered (2026-10-25):* both. `brainstorm.md` stays, a scratchpad for quick notes; an
   entry moves into the backlog as an `idea` once it is written up (a second sentence, or
   something links to it), or as a `feature` once the owner agrees to it. The migration
   moves the written-up entries and removes the settled ones (special forms in the symbol
   table, done on `symbol-table`; the SRS and reviews, moved to HLDs). *Lasting.*
4. **Defect repros as expected failures:** run them (a `candy defect` block, or spec
   examples marked by item id), or keep them as text?
   *Answered (2026-10-25):* run them where the correct behaviour is clear: the item holds a
   spec block (`candy run` or `candy error`) of what *should* happen, which the runner
   collects from `backlog/` and marks as an expected failure; when it passes, the fix has
   landed, the example moves into its spec file and the item goes to `done`. Where the fix
   is still a decision (`nil` redefinable), the repro is text until it is decided.
   *Lasting.*
5. **States:** are `open`, `in-progress`, `review`, `done` and `dropped` the right ones?
   *Answered (2026-10-25):* those five, and `kept` (a leak or shortcut kept on purpose, so
   a lasting one isn't open forever); no `blocked` or `deferred`. A leak that goes to
   `kept` becomes a rule in the spec, stated as lasting, which the item refers to (the
   owner, 2026-10-25: "do `kept` items get into the `spec`?"). *Lasting.*
6. **Ids:** a plain number (`B12`), or a prefix by kind (`D3`, `L12`)? A prefix says the
   kind, but an item reclassified (as the audit's defects are) would change its id.
   *Answered (2026-10-25):* a plain number, `B1`, `B2`, ..., never reused; the kind is a
   field, and the file name carries a slug (`B12-sig-list-crash.md`). Item ids (`B` and a
   number) and rule ids (dotted, lowercase) can't collide. The audit's defect numbers
   (1 to 13) get B-numbers in the migration. *Lasting.*
7. **Rule ids:** anchors on the headings of today's spec files (proposed), or the chat's
   one rule per file with front matter?
   *Answered (2026-10-25):* anchors in today's files, as `<a id="..."></a>` before a
   heading or a rule's paragraph (not `{#id}`, which GitHub shows literally); a block
   belongs to the anchor above it. `[[id]]` links stay plain text, checked by the test.
   *Lasting.*
8. **What gets an id:** every spec section, or only those something links to? Every
   section makes "a stable rule with no example" checkable everywhere.
   *Answered (2026-10-25):* links can be written in any tracked `.md` (the test reads them
   all); as targets, every rule in `spec/` has an anchor (about 60), so every stable rule
   has an example (or says where it is tested) and every block belongs to a rule; every
   backlog item has its number; any other doc (HLDs, `process.md`, the archives, the
   READMEs, CLAUDE.md) gets an anchor only where something links to it. *Lasting.*
9. **Renames:** keep the old id as an alias (the chat's `aliases:`), or rewrite the links
   (a test finds them all)?
   *Answered (2026-10-25):* both: the live docs' links are rewritten to the new id, and the
   old id stays as a second anchor beside the new one, so commit messages, chats and
   archives still resolve; the test fails on an alias used in a live doc. (Backlog item
   numbers never change, question 6.) A **rename warning:** a check compares the ids
   defined on `master` (the branch's merge base) with today's, and warns, without failing,
   when one is gone with no alias left, so a rename is always deliberate and visible.
   Rule ids stay readable names, not opaque numbers (`R17` says nothing in a link, and a
   wrong link can't be seen), so renames happen, and the warning and aliases pay for them.
   *Lasting.*
10. **Examples as `.cdy` files** for highlighting, or a Markdown injection for `candy`
    fences in `editors/vscode-candy/`?
    *Answered (2026-10-25):* the injection, later: a `task` in the backlog, priority `low`
    (one of its first items, a small test of the format). GitHub won't highlight Candy
    either way. *For now.*
11. **The four conflicts** ("Left out of the chat"): `grammar.ebnf`, error codes, a
    changelog, printing values. Proposed: keep the executable spec's answers; reopen one
    only on its own (each has a *for now* to revisit).
    *Answered (2026-10-25):* keep all four (the reader as authority, substrings, no
    changelog, numbers and text). One note for when substrings stop being enough
    (`executable_spec.md`, question 4): an error's code could be its rule's id
    (`match.exhaustive: no clause for Rect`), so `expect-error` matches the id and messages
    can be reworded, cheaper than an `E0012` scheme. *Lasting* (each answer keeps its own
    *for now*).
12. **The book:** in this HLD's steps, or later?
    *Answered (2026-10-25):* only its smallest part now: the backlog's generated index also
    lists open items by the rule ids in their refs, so a rule's defects and leaks are in one
    place ("from a rule, its open items"). The book itself (a page per rule) is an `idea`
    in the backlog, for once the ids have been used a while. *For now.*
13. **A priority** (the owner, 2026-10-25)?
    *Answered (2026-10-25):* yes, one field, `high`, `normal` (default) or `low`, set by
    the owner; no separate severity (it is a reason, in the item's text). *For now*: a
    finer scale, or severity, if three values stop being enough.
