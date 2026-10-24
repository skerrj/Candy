# Spec by example (process HLD)

**Kind: process** (how work is done: the spec, its tests, the lifecycle), not a design of
the language or translator. **Status: proposal (2026-10-23), questions open.** For a
branch `spec-by-example`, after tag `runtime-names`. From a chat with the owner
(2026-10-23, "Twine, spec-by-example, and the HLD plan"), mapped onto what Candy already
has; where the chat and the process or the code disagree, the conflict is flagged here
(**Conflict**) rather than settled. It also takes in `doc/brainstorm.md`'s "An SRS for the
current design" (its open format question).

## The idea (from the chat)

Docs, spec and tests become one artifact: every claim in the spec is an example that the
test runner executes. A spec file is plain Markdown; its prose explains, and its fenced
blocks are normative:

````markdown
## Exhaustive match

A `match` over a sum must cover every variant, unless it has an `else`.

```candy run
(deft Shape (Circle ((r Int))) (Square ((s Int))))
(put (match (Square 2) ((Circle r) r) ((Square s) (* s s))))
```
```expect
4
```

```candy error
(deft Shape (Circle ((r Int))) (Square ((s Int))))
(put (match (Circle 1) ((Square s) s)))
```
```expect-error
match on Shape: no clause for Circle
```
````

The runner extracts each `candy run` and `candy error` block, translates it with the real
translator, runs it, and compares with the `expect` block. (Both examples are checked
against today's translator: the first prints `4`; the second fails with
`2:6: match on Shape: no clause for Circle (or add else)`.)

The chat's other points: test behaviour, not translated text; the spec suite as the
bootstrap gate (stage 0, 1, 2 and a fixpoint); a per-feature lifecycle (`draft`, `stable`,
`deprecated`, `since`) tied to the bootstrap; a runner not written in Candy at first; coded
errors (`E0012`) for `expect-error`; `grammar.ebnf` as the only syntax authority; a
`CHANGELOG.md` that only links to the spec; doc generation (mdBook) for free.

**Conflict (syntax):** the chat's examples were in an ML-like syntax
(`deft Shape = Circle(r) | Square(s)`); Candy is S-expressions. The examples above are
rewritten in Candy.

## Where things stand

| The chat's piece | What Candy has |
|---|---|
| A spec | `src/cdy/candy-special.md`: informal, one section per special form, with grammar lines (`> (match *expr* ...)`) and no runnable examples. The HLDs record decisions branch by branch, not the whole language (`doc/brainstorm.md`, "An SRS"). |
| Examples as tests | `tst/cdy/**/NAME.cdy` + `NAME.out`: 18 whole programs, run through T1 (output and `mypy --strict`), and T1 and T2 must agree on each (`tst/py_cdy/test_self_host.py`). Errors are tested in Python: tables of `(source, message)` pairs (`test_errors`, `test_macro_errors`, `test_match_errors`, ...), matched as substrings. |
| Test behaviour, not text | Already so: the programs are run and their output compared; the translator's own text is checked only by the fixpoint (T2 reproduces itself, and is `bin`). |
| Stage 0, 1, 2 and a fixpoint | Already so: `bin` (stage 0) builds T1, T1 builds T2, T2 must reproduce itself and pass `mypy --strict`, and `bin` becomes T2 (`src/py_cdy/self_host.py`). Beyond the chat: the bootstrap chain, `boot/00` to `boot/31`, checks every past promotion (`doc/hl_rqmt/bootstrap.md`). |
| A runner not in Candy | Already so: pytest, in Python. |
| Coded errors | None: errors are `file:line:col: msg` (`fail`, about 116 calls in `src/cdy/`). |
| A grammar | None written down: the reader is hand-written (`src/cdy/read.cdy`); the literal rules are in CLAUDE.md and the iMVP doc. |
| Feature lifecycle | HLD statuses (*draft*, *proposal*, *accepted*, *done*) per branch (`doc/process.md`); no per-feature status, and no versions. |
| A changelog | None: the history is CLAUDE.md ("History and branches"), the feature tags and the HLDs. |

## Goals

- **One spec, whose examples run:** a Markdown spec of the language, one file per feature,
  where each example is a test, so the spec can't drift from the translator.
- **The spec in the gate:** the examples run wherever the test programs run (T1, and T1
  and T2 agreeing), so a `bin` that breaks the spec never becomes `bin`.
- **A home for a feature's lifecycle:** what is settled, what is a draft, what is going.
- **The process says when the spec is written** (a feature's examples with its HLD, or
  before its code).
- **A better way to review items and tasks:** its own HLD, `doc/hl_rqmt/review.md`
  (question 9).

**Not goals (for now):** generated docs (mdBook or the like: "After the MVP"); porting the
runner to Candy; a second target's runner (`doc/hl_rqmt/multi_target.md`).

## Proposal

### Layout

```
spec/
  README.md            how to read and write the spec; the block kinds
  00-syntax.md         literals, comments, the reader's rules (question 6)
  10-bindings.md       def, let, fn, defn, sig
  20-types.md          the type names, deft, get, assoc
  30-match.md          sum types and match
  ...                  one file per feature, in candy-special.md's order
tst/py_cdy/test_spec.py   extracts and runs every example in spec/*.md
```

`spec/` at the top level, beside `doc/`, since it is normative and tested (question 1).

### Blocks

- ` ```candy run ` then ` ```expect `: a whole program; its standard output must equal
  the `expect` block.
- ` ```candy error ` then ` ```expect-error `: translating it must fail, with a message
  that contains the `expect-error` text (as the Python error tables match today), without
  the `file:line:col: ` prefix unless the block gives it (question 4).
- ` ```candy ` alone: an illustration, not run (grammar lines, fragments).
- Each example is its own program, in its own temporary file, with the prelude and the
  prelude macros as every program has them. A multi-module example is out of scope at
  first: those stay in `tst/cdy/cdyc/` (question 3).

### The runner

`tst/py_cdy/test_spec.py`, beside `test_self_host.py`, whose T1 and T2 fixtures it reuses:

- extracts the blocks from `spec/*.md` (a small Markdown fence scanner, not a Markdown
  library: fences are all it needs);
- one pytest case per example, named `file:line` (so a failure points at the spec), run
  through T1, and checked with `mypy --strict` like the test programs;
- the fixpoint's "T1 and T2 agree" covers the examples too.

Written in Python (the chat's point 4, *lasting* while the translator could break it).

### Feature lifecycle

Each spec file starts with a status line: `status: draft | stable | deprecated` and
`since: <tag>`, where the tag is the feature branch that brought it (`since: macros`),
since Candy has no versions (question 5).

- **draft:** its examples may fail (pytest `xfail`, so a passing one is reported); written
  with the HLD, before the code.
- **stable:** its examples must pass. A branch's docs step makes its features stable.
- **deprecated:** its examples still pass until the feature goes; the file says what
  replaces it.

**The bootstrap rule** (the chat's point 3: the translator may use a feature only once it
is stable and in stage 0): Candy already enforces the mechanical half, since `bin` has to
translate the translator's source, and the chain checks every step (a step that needs the
new feature before `bin` has it needs staging, `doc/hl_rqmt/bootstrap.md`). The policy
half, *stable* before the translator uses it, is new (question 5).

### Migration

1. The runner, and `spec/README.md`.
2. One feature, `deft` and `match` (the chat's choice: well specified, exhaustiveness
   errors already tested), moved from `candy-special.md` into `spec/30-match.md` with
   examples, and `test_match_errors`' table turned into `candy error` blocks.
3. The rest of `candy-special.md`, a file at a time; it then goes, leaving a pointer
   (question 2). The Python error tables move into the spec where they are language
   rules (not the driver's or the bootstrap's).

## Process changes (`doc/process.md`)

- **The lifecycle:** an HLD for a language feature includes (or points at) its draft spec
  file; the steps make its examples pass; the docs step marks it stable. Today's docs step
  updates `candy-special.md`; it would update `spec/` instead.
- **"Where notes go":** a row for the spec: *a language rule, with its examples* →
  `spec/`.
- **Design docs:** the HLDs stay the record of decisions and what was built; the spec is
  the current whole (the SRS idea: the HLDs aren't its functional specs, the spec files
  are).

## Reviewing items and tasks

Its own HLD: `doc/hl_rqmt/review.md` (draft; question 9). A spec example could be what a
step's review points at, as that step's tests.

## Conflicts with the process and the code (flagged)

- **Stage 0 promotion:** the chat promotes stage 2 to stage 0 at a release; Candy
  promotes at every commit that changes `bin` (each a `boot/NN` step). No change
  proposed: the spec just joins the existing gate.
- **`since: 0.x`:** Candy has no versions; a feature tag stands in (question 5).
- **Coded errors:** every `fail` would need a code, about 116 calls; the substring match
  does the job without them (question 4).
- **`grammar.ebnf` as the only syntax authority:** checking examples against an EBNF needs
  a parser generator (a new test dependency), and the reader is the real authority today
  (question 6).
- **`CHANGELOG.md`:** the history already lives in CLAUDE.md, the tags and the HLDs; a
  fourth place would drift (question 7).
- **`candy-special.md` is "the spec"** for CLAUDE.md, the docs step and the editor
  grammar test (`test_editor_grammar.py` lists the special forms from `special.cdy`, not
  from it, so that test is unaffected).

## Steps (sketch)

1. **The runner** (`tst/py_cdy/test_spec.py`) and `spec/README.md`, with one example to
   prove it.
2. **`deft` and `match`** as the first spec file; `test_match_errors` moves into it.
3. **The other features**, from `candy-special.md`, one commit per file or two;
   `candy-special.md` goes.
4. **The process** (`doc/process.md`): the lifecycle, "Where notes go", design docs.
5. **Docs:** CLAUDE.md (the spec, the tests), the iMVP doc, `doc/brainstorm.md` (the SRS
   entry moves here, leaving a pointer).

No `bin` change: the translator is untouched, so no chain steps.

## After the MVP

- Generated docs from `spec/` (mdBook or similar), with the examples' outputs.
- Coded errors, if messages start changing under the tests.
- A grammar file checked against the reader (or generating it).
- Multi-module examples (a block that names its file), so `tst/cdy/cdyc/` can shrink.
- The runner in Candy, as dogfooding, once it can't hide a translator bug.
- Tutorials outside `spec/` whose code blocks run through the same extractor.

## Questions

1. **Where the spec lives:** `spec/` at the top (proposed), `doc/spec/`, or
   `src/cdy/spec/` beside `candy-special.md`?
   *Proposed:* `spec/`: it is neither design history (`doc/`) nor the translator's input.
2. **`candy-special.md`:** migrate it into `spec/` and remove it (proposed), or keep it as
   a one-page summary that links into `spec/`?
3. **`tst/cdy/` programs:** keep them as they are (proposed: whole, multi-module and
   translator-scale programs), or move the small ones into the spec?
4. **`expect-error`:** a substring of the message (proposed, as the Python tables do
   today), or error codes (`E0012`) now?
   *Proposed:* substrings *for now*; codes after the MVP.
5. **Lifecycle:** per-file `status`/`since` with a feature tag for `since` (proposed);
   and is "the translator uses only stable features" a rule, or is the bootstrap chain's
   mechanical check enough?
   *Proposed:* the status line yes; the translator rule no (the chain enforces what
   matters), revisited if a draft feature gets into the translator.
6. **The grammar:** an `00-syntax.md` in prose and examples, with the reader as the
   authority (proposed), or a `grammar.ebnf` checked by a parser generator?
7. **A changelog:** none (proposed: CLAUDE.md's history and the tags are it), or
   `CHANGELOG.md` linking to spec sections?
8. **The branch:** its own branch `spec-by-example` after `runtime-names` (proposed)?
9. **Reviewing items and tasks:** part of this HLD, or an HLD of its own?
   *Answered (2026-10-23):* its own, `doc/hl_rqmt/review.md`, linked from here.
