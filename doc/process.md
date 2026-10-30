# Process

How work on Candy is done: the branch lifecycle, commits and tags, design docs, the spec,
and where notes go. The owner reviews everything before it goes into history; Claude Code
does most of the writing. Changes to the process itself go in the log at the end.

## The branch lifecycle

One branch per piece of work, named for it (`macros`, `modules`, `system-prelude`), off
`master`.

1. **HLD draft.** A design doc in `doc/hl_rqmt/` (see "Design docs"), often written on the
   branch before (the follow-up of its work). Its questions are answered by the owner,
   usually with "the simplest option for the MVP". An HLD for a language feature includes,
   or points at, the feature's spec file, `status: draft` (see "The spec"), whose
   examples say what the feature will do, and says which rules of the stable files change.
   The owner goes over those spec changes, with the questions, before accepting it.
2. **Start the branch.** The first commit, "Start branch X: ...":
   - marks the HLD accepted (with its scope);
   - adds a `task` item for each of the HLD's steps to the backlog (see "The backlog"),
     `open`, and for a language feature its `feature` item, if it has none yet;
   - often also does step 1.

   Nothing is archived: an item stays in the backlog until it is closed.
3. **Steps.** One commit per step of the HLD ("X step N: ..."). Each step:
   - ends with every test passing and the linters clean (`pytest`, `ruff`, `pylint`,
     `mypy`, `pyright`; see CLAUDE.md, "Running"), and the fixpoint holding after a
     rebuild of `bin`;
   - adds a *Done. As built:* note under the step in the HLD: what was built, how it
     differs from the plan, its bootstrap, its tests;
   - records what it finds as backlog items: a hack as a `leak` or `tech-debt`, a bug as a
     `defect` (with a repro where the fix is clear); a step's own fix of an item closes it
     (`done`, `fixed:` the branch);
   - changes the spec with the language: a step that adds or changes a rule adds or
     changes its examples in `spec/` (a draft file's examples pass as the steps build
     the feature);
   - moves its `task` to `review`, and writes the index (`python script/backlog.py`).
   A step that turns out not to be wanted is struck through and marked *Dropped*, with why
   (and its task `dropped`).
4. **Docs.** A last step brings CLAUDE.md, the spec (`spec/`), the iMVP doc and the
   other HLDs up to date, and marks the branch's spec files `stable`, `since:` the
   branch's tag.
5. **Review.** The owner works through the items in `review` (`backlog/README.md`); the
   verdict goes in the item's notes ("looks ok for now"), which becomes `done` (`fixed:` the
   branch), or goes back to `in-progress`; fixes are more commits. The HLD's status
   becomes *done*, with its scope.
6. **Merge and tag.** `git merge --no-ff refs/heads/X` into `master`, with the message
   "Merge X: <summary>", and an annotated tag `X` on the merge, with a one-line summary.
   Both are pushed (see "Commits, tags and pushing").

## Commits, tags and pushing

- **Commit only on "gawc"** ("go ahead with commit"). It approves the work shown so far,
  not a push. "gawcnp" is gawc and push.
- **The owner's own edits:** the owner may edit files too (`doc/brainstorm.md`, say).
  Either the owner says so, or Claude Code finds them with `git status` before a commit:
  they go into the commit, and the report names them. A checkout or merge that they
  block is done with a stash, which is popped afterwards.
- **Push only when asked.** `origin` (GitHub, `skerrj/Candy`) is a backup, not a place for
  collaboration, so there are no pull requests.
- **Full refs**, because a branch and its tag share a name: `git merge refs/heads/X`,
  `git push origin refs/heads/X:refs/heads/X refs/tags/X:refs/tags/X`.
- **Tags are annotated** (`-a`, with a message), branch and `boot/NN` tags alike: `git tag
  -a X <merge commit> -m "X: <summary>"`, never a bare `git tag X`. Before pushing,
  `git cat-file -t refs/tags/X` must say `tag` (a lightweight one says `commit`). A
  lightweight tag already pushed can only be replaced by a force-push of the tag, which
  the owner does. (The `library` tag went out lightweight.)
- **A tag's message is one line,** and `git tag -n1` shows only its first: when pasting a
  tag command, check the terminal didn't wrap the `-m` text. The `library` tag's message
  has a line break after "operations as", from a wrapped paste in its re-tagging (left
  as it is: `git tag -l --format='%(contents)' library` shows all of it).
- **Commit messages** start with what was done ("X step N: ..."), then a body on why and
  what it touches, and end with the attribution trailers Claude Code adds.
- **Bootstrap tags** (`doc/hl_rqmt/bootstrap.md`, "Tags and history"): a commit that
  changes `bin` gets the next annotated `boot/NN` tag (message: the Python version and
  any staging the rebuild needed); `boot/00` is `self-host-py`. *A commit that changes
  `bin`* changes any file in `bin/<target>/`: the translator, or a library copy next to it
  (which alone counts: the translator reads them as it runs). `bin/README.md` alone
  doesn't.
- **History is never rewritten** unless the owner asks. Before a rewrite, the old tip is
  tagged `archive/<branch>-<YYYY-MM-DD>` and the tag pushed first. `boot/*` and
  `archive/*` tags are never deleted.

## Rebuilding `bin`

- After a change to `src/cdy/`, rebuild with `python src/py_cdy/self_host.py`; the tests
  check the fixpoint and that `bin` is T2 (`bin/README.md`).
- **After committing a new `bin`:** `python script/bootstrap.py --step HEAD` checks that
  the previous step's `bin` builds it; then `--tag` gives it the next `boot/NN`. If it
  needed staging by hand, the tag's message says how (`doc/hl_rqmt/bootstrap.md`).
- **Before a merge into `master`:** `pytest -m bootstrap` (or `python script/bootstrap.py
  --from-scratch`, which is equivalent): the old steps can only break if the environment
  drifts (Python, mypy, parsec, or the script), and a merge is the checkpoint for that.
- **The bootstrap hazard:** the checked-in `bin` reads the live `spelling.py` and its own copy
  of the library (`bin/py/system.cdy` and the rest). A change that adds built-ins
  therefore copies the new `src/cdy/system.cdy` into `bin/py/` before the rebuild. An HLD
  step that changes how `bin` is built says how in a "Bootstrap" section.

## Design docs

HLDs live in `doc/hl_rqmt/`, one per piece of work, named for it.

- **Kinds:** most HLDs design the language or the translator. A *process HLD* designs how
  work is done (the lifecycle, the spec and its tests, reviews): its title says
  "(process HLD)" and its status line starts "**Kind: process**" (`executable_spec.md`,
  `tracking.md`). Its changes land in this file, and its log.

- **Layout:** a status line; "Where things stand"; "Goals" (and "Not goals"); "Proposal"
  (or "Design"); "Pros and cons" (with the timing: why now, or why wait); "Steps";
  "Questions". Larger ones add "After the MVP" for what is deliberately left out. One
  that changes the language has "The spec" in its Proposal: its draft spec file (each
  rule's id, in a table), and the rules of the stable files it changes.
- **Status words:** *draft* (being written), *proposal* (written, questions open),
  *accepted* (questions answered; the branch can start), *done* (built, with its scope).
  The status line says which branch it belongs to and which decisions are in.
- **Decisions** are marked in the heading ("(decided)") or the Questions list.
  - Questions offer options and a recommendation; the owner answers in plain text.
  - An answer taken as the simplest for the MVP says *for now* and links to the backlog
    item that tracks it (`[[B12]]`); one meant to stay says *lasting*.
- **Steps** carry their *Done. As built:* notes (see the lifecycle), so the HLD records
  what was built, not just what was planned.
- `doc/hl_rqmt/iMVP_py_translator.md` is the iMVP's requirements and decisions; keep it up
  to date as decisions are made.

## The spec

`spec/` is the language as it is now, rule by rule, each with examples that the tests run
(`spec/README.md` says how to read and write it; the design is
`doc/hl_rqmt/executable_spec.md`). The HLDs are the record of how it got there: their
decisions and what each branch built. So a rule's current form is looked up in the spec,
and its reasons in the HLDs (the spec file's `since:` names the branch).

- **A spec file's status:** `draft` (written with its HLD; its examples may fail),
  `stable` (they must pass; set by the docs step), `deprecated` (they pass until the
  feature goes).
- **The spec says what the translator does.** A gap found writing it (a check missing, a
  form accepted that shouldn't be, Python showing through) isn't fixed in passing: the
  rule says *for now* and links to its backlog item (a `defect` or a `leak`), to be fixed
  on a branch of its own.
- **Every rule has an id,** an anchor (`<a id="match.exhaustive"></a>`), and an example
  or a *Tested in* (`spec/README.md`); anything else refers to it as `[[match.exhaustive]]`.
- **What stays in `tst/`:** programs of several files, whole programs, the translator's
  own tests (its parts, its driver, the fixpoint and the bootstrap chain), and most
  checks of where an error points (a spec row gives the position only for a rule about
  it). How these test levels are defined is open (`executable_spec.md`, "Test levels").

## The backlog

Everything not done yet is an item in `backlog/`, one file each, `B<n>-<slug>.md`; the
format is in `script/backlog.py`, and why in `doc/hl_rqmt/tracking.md`.

- **Kind:** `defect` (wrong by Candy's own rules), `leak` (a shortcut where Python shows
  through), `tech-debt` (a shortcut a Candy user can't see), `feature` (agreed to, not
  built), `task` (work to do: a step, a follow-up, a decision), `idea` (not agreed to).
- **State:** `open` → `in-progress` → `review` → `done`, or `dropped` (with why), or
  `kept`: a leak kept on purpose, whose rule the spec then states as lasting (a kept
  tech-debt item keeps its reason in the item).
- **Priority:** `high`, `normal` or `low`, set by the owner (Claude Code may propose one).
- **Notes:** an item's history goes in a `## Notes` section at its end, apart from its
  text: dated bullets, oldest first, each saying who (`- 2026-10-25, the owner: ...`). A
  review's verdict goes there, and a `dropped` or `kept` item's reason (checked).
- **Ids** are never reused. A new item takes the next one (`backlog/README.md` says
  which); then `python script/backlog.py` rewrites the index, which a test checks is
  current.
- **Links:** `[[B12]]` or `[[match.exhaustive]]`, in any tracked `.md`, outside code; a
  test fails on one to nothing. The test reads the files git tracks, so `git add` a new
  item (or doc) before its id counts as a link target. A renamed id keeps the old one as an alias, the anchor
  after the first on its line, and the live links move to the new one (a warning names
  an id that is gone since `master`).
- **A defect's repro** is a `candy run` or `candy error` block of what *should* happen,
  run as a strict expected failure: once it passes, the example moves into its spec file
  and the item is `done`.

## Where notes go

| What | Where |
|---|---|
| A defect, a leak, tech debt, a task, an agreed feature, a written-up idea | an item in `backlog/` (see "The backlog") |
| A quick, undecided thought | `doc/brainstorm.md` (once written up, it moves to the backlog as an `idea`) |
| An optimization or mutation idea | `doc/hl_rqmt/mutation_optimization.md` |
| History: the lists before the backlog | `doc/archive/leaks_*.md`, `doc/archive/TODOS_*.md` (each entry open on 2026-10-25 is an item) |
| History: a side conversation worth keeping (the owner asks for it) | `doc/archive/chat_<topic>.md`, verbatim, with a note at its top: when, where, and what came of it |
| A language rule, with its examples | `spec/`, the file for its feature (`spec/README.md` lists them) |
| A design, its decisions and what was built | its HLD in `doc/hl_rqmt/` |
| Guidance for Claude Code (layout, commands, conventions) | `CLAUDE.md` |

## Working with Claude Code

- **Questions in plain text,** never the multiple-choice picker: options, the recommended
  one marked, and the owner types an answer. An answer that looks off-plan is confirmed
  before acting on it. (The picker once started work on an option chosen by accident.)
- **Claude Code's memory** (outside the repo) keeps only how to work with the owner; the
  process lives here.

## Log

Changes to the process, newest first.

- **2026-10-29:** a side conversation worth keeping is archived in `doc/archive/chat_*.md`
  ("Where notes go").
- **2026-10-28:** an HLD that changes the language says how the spec changes ("The spec":
  its draft file's rules, the stable rules it changes), and the owner goes over that
  with the questions, before accepting it.
- **2026-10-25:** the backlog and ids (`doc/hl_rqmt/tracking.md`): `backlog/`, one file
  per item, replaces `doc/leaks.md`, `doc/tech_debt.md` and `TODOS.md`, and nothing is
  archived when a branch starts; a step's review is its task going to `review`; spec
  rules have ids, and docs link by id; "The backlog", and "Where notes go" redone.
- **2026-10-24:** the executable spec (`doc/hl_rqmt/executable_spec.md`): "The spec"; a
  language feature's HLD comes with its draft spec file, its steps change the spec with
  the language, and the docs step marks it stable; a row for the spec in "Where notes
  go".
- **2026-10-23:** HLDs get a "Pros and cons" section; process HLDs, marked apart from design HLDs ("Design docs", "Kinds").
- **2026-10-22:** tags are annotated, with the command and a check before pushing.

- **2026-10-20:**
  - this file;
  - the owner's own edits are found before a commit, included and named;
  - HLD answers marked *for now* or *lasting*;
  - bootstrap tags `boot/NN`, `archive/` tags before a rewrite, and history never
    rewritten unasked;
  - no multiple-choice picker for questions.
- **2026-10-17:** `origin` added as a backup; branches merged with `--no-ff` and tagged;
  each branch's leaks and TODOS archived when the next branch starts (from
  `pre-self-host` on), and `doc/tech_debt.md` started.
