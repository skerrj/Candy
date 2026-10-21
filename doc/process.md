# Process

How work on Candy is done: the branch lifecycle, commits and tags, design docs, and where
notes go. The owner reviews everything before it goes into history; Claude Code does most
of the writing. Changes to the process itself go in the log at the end.

## The branch lifecycle

One branch per piece of work, named for it (`macros`, `modules`, `system-prelude`), off
`master`.

1. **HLD draft.** A design doc in `doc/hl_rqmt/` (see "Design docs"), often written on the
   branch before (the follow-up of its work). Its questions are answered by the owner,
   usually with "the simplest option for the MVP".
2. **Start the branch.** The first commit, "Start branch X: ...":
   - marks the HLD accepted (with its scope);
   - archives the previous branch's lists: `doc/leaks.md` to
     `doc/archive/leaks_<previous>.md` and `TODOS.md` to
     `doc/archive/TODOS_<previous>.md`, each starting fresh with a pointer to the
     archives;
   - often also does step 1.
3. **Steps.** One commit per step of the HLD ("X step N: ..."). Each step:
   - ends with every test passing and the linters clean (`pytest`, `ruff`, `pylint`,
     `mypy`, `pyright`; see CLAUDE.md, "Running"), and the fixpoint holding after a
     rebuild of `bin`;
   - adds a *Done. As built:* note under the step in the HLD: what was built, how it
     differs from the plan, its bootstrap, its tests;
   - records new hacks as leaks or tech debt (see "Where notes go");
   - adds a review item to `TODOS.md` (`- [ ] Review step N as built`).
   A step that turns out not to be wanted is struck through and marked *Dropped*, with why.
4. **Docs.** A last step brings CLAUDE.md, the spec (`src/cdy/candy-special.md`), the iMVP
   doc and the other HLDs up to date.
5. **Review.** The owner works through the review items in `TODOS.md`; fixes are more
   commits. The HLD's status becomes *done*, with its scope.
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
- **Before a merge into `master`:** `python script/bootstrap.py --from-scratch`.
- **The bootstrap hazard:** the checked-in `bin` reads the live `table.py` and its own copy
  of the library (`bin/py/system.cdy` and the rest). A change that adds built-ins
  therefore copies the new `src/cdy/system.cdy` into `bin/py/` before the rebuild. An HLD
  step that changes how `bin` is built says how in a "Bootstrap" section.

## Design docs

HLDs live in `doc/hl_rqmt/`, one per piece of work, named for it.

- **Layout:** a status line; "Where things stand"; "Goals" (and "Not goals"); "Proposal"
  (or "Design"); "Steps"; "Questions". Larger ones add "After the MVP" for what is
  deliberately left out.
- **Status words:** *draft* (being written), *proposal* (written, questions open),
  *accepted* (questions answered; the branch can start), *done* (built, with its scope).
  The status line says which branch it belongs to and which decisions are in.
- **Decisions** are marked in the heading ("(decided)") or the Questions list.
  - Questions offer options and a recommendation; the owner answers in plain text.
  - An answer taken as the simplest for the MVP says *for now* and points at the leak,
    tech debt or follow-up entry that tracks it; one meant to stay says *lasting*.
- **Steps** carry their *Done. As built:* notes (see the lifecycle), so the HLD records
  what was built, not just what was planned.
- `doc/hl_rqmt/iMVP_py_translator.md` is the iMVP's requirements and decisions; keep it up
  to date as decisions are made.

## Where notes go

| What | Where |
|---|---|
| A hack, or a place where Python shows through into Candy | `doc/leaks.md` (earlier branches' in `doc/archive/leaks_*.md`; they still apply until struck through) |
| A shortcut a Candy user can't see (translator, runtime, tests, tooling) | `doc/tech_debt.md` (remove it when fixed) |
| An undecided design idea | `doc/brainstorm.md` (move it to an HLD when it becomes work, leaving a pointer) |
| An optimization or mutation idea | `doc/hl_rqmt/mutation_optimization.md` |
| Something to do or review on this branch | `TODOS.md` (earlier branches' in `doc/archive/TODOS_*.md`) |
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
