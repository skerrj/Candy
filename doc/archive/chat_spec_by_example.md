*Archived 2026-10-25, from `tmp/` (untracked).* The chat behind two process HLDs: sections 1 to 4 (2026-10-23) are the source of `doc/hl_rqmt/executable_spec.md`; section 4b (added 2026-10-24) of `doc/hl_rqmt/tracking.md`. Its prototype, `candy-spec-proto.zip` (`tools/specbook.py`), isn't kept: its example programs aren't Candy (fields without types, `_` for `else`). The chat couldn't see the repo, so where it and Candy differ, the HLDs say how.

# Candy: Twine, spec-by-example, and the HLD plan

*Chat archive, 2026-10-23*

---

## 1. Is Twine a good idea for project docs / a spec language?

**Question:** Investigate whether using the Twine language for a software project's documents is a good idea. Could we consider it a spec language for documentation?

**Answer (summary):** Not as the main documentation format, and not a spec language.

- **What Twine is:** an interactive-fiction tool. Its plain-text source format is **Twee** (Twee 3 is formally specified). A document is a graph of named passages joined by `[[links]]`, plus macros from a story format (Harlowe, SugarCube).
- **Good for:** branching, decision-shaped docs (troubleshooting trees, onboarding paths, runbooks, "choose your setup"); plain text that diffs in git; compiles to a single self-contained HTML file.
- **Bad for general docs:** no heading hierarchy, tables, admonitions, code cross-references or API reference generation; no doc-site tooling (search, versioning, link checking, doc tests); contributors already know Markdown; awkward to read linearly or print.
- **Not a spec language:** a spec language needs checkable semantics about the *system* (types, contracts, invariants, grammars, state machines), e.g. TLA+, Alloy, OpenAPI/JSON Schema, EBNF, literate tests. Twee only has semantics about the document itself.
- **Suggestion:** Markdown/reST for main docs, a real spec tool where it fits, Twee only for one or two branching guides.

Sources: [Twee 3 Specification](https://github.com/iftechfoundation/twine-specs/blob/master/twee-3-specification.md), [IFTF: Three Twine specs formalized](https://blog.iftechfoundation.org/2020-03-04-three-twine-specs.html)

---

## 2. For Candy: lifecycle management and doc generation "collapsing on itself"

**Idea:** make docs, spec and tests one artifact. Every claim in the docs is an example the test runner executes.

### Layout

```
spec/
  grammar.ebnf            # the only normative syntax
  10-literals.md
  20-bindings.md
  30-deft-and-match.md    # one file per feature
  ...
tests/
  run_spec                # extracts + runs every example in spec/*.md
```

### Spec file format

Plain Markdown. Prose explains; fenced blocks are normative.

````markdown
## Exhaustive match

A `match` over a `deft` type must cover every variant.

```candy run
deft Shape = Circle(r) | Square(s)
match Square(2) { Circle(r) -> r, Square(s) -> s * s }
```
```expect
4
```

```candy error
match Circle(1) { Square(s) -> s }
```
```expect-error
non-exhaustive match: missing Circle
```
````

The runner extracts each `candy run` / `candy error` block, runs it through the real translator, and diffs against the `expect` block. CI fails on mismatch.

### Why it helps

- **Spec = docs = tests.** A feature is written once.
- **Lifecycle has a home:** each file carries `status: draft | stable | deprecated` and `since: 0.x`. Draft examples may fail; stable must pass; deprecated keep tests until removal.
- **Reviewable:** changing semantics means changing an `expect` block in a PR.
- **Doc generation is trivial:** feed `spec/` into mdBook or similar.

### Keep separate on purpose

- `grammar.ebnf` is the single syntax authority; a test parses every example with it.
- `CHANGELOG.md` only *links* to spec sections.
- Tutorials/guides live outside `spec/` but their code blocks run through the same extractor.

### Build order

1. Write the extractor/runner (~100 lines).
2. Convert `deft`/`match` to this format; get CI green.
3. Migrate other features one file at a time; new features need a spec file first.

Precedents: Rust doctests, Python doctest, the CommonMark spec (one Markdown file whose examples are the test suite).

---

## 3. Candy is a self-hosting translator (`*.cdy` → target language)

Implications:

1. **Test behavior, not translated text.** Runner = translate, then run target code, compare stdout/error. Keep a few golden codegen tests for regressions, outside `spec/`.
2. **The spec is the bootstrap gate.** Stages: stage 0 (pinned, known-good), stage 1 (current source built by stage 0), stage 2 (current source built by stage 1). Release check:
   - stage 1 passes the full spec suite
   - stage 2 passes the full spec suite
   - stage 1 and stage 2 produce identical output when translating the translator (fixpoint)
   - then promote stage 2 → new stage 0
3. **Feature lifecycle maps onto stages.** draft → stable; the translator source may only use a feature once it is `stable` *and* present in the pinned stage 0 (avoids implementing a feature with itself).
4. **Runner not written in Candy** (initially) — a translator bug shouldn't break the diagnostic tool. Port it to Candy later as dogfooding.
5. **Stable error format:** coded diagnostics like `E0012 non-exhaustive match: missing Circle`; `expect-error` matches code + key phrase so messages can be reworded freely.

Open inputs needed for the runner: the target language and the translate/run commands (e.g. `candyc foo.cdy -o foo.js && node foo.js`).

---

## 4. Turning this into an HLD inside Candy

Goal: write the above as a High-Level Design doc integrated with Candy's existing docs, including the process doc.

The repo wasn't reachable from the chat (no attached files, chat not linked to the local machine, no GitHub account connected). Ways in: give the GitHub `owner/repo`; open the chat in the Claude desktop app on the machine with the repo; or attach the docs.

Planned HLD contents: spec-by-example format, extractor/runner, stage 0/1/2 bootstrap gate with fixpoint check, draft/stable/deprecated lifecycle tied to stage promotion, coded errors for `expect-error`, `grammar.ebnf` as sole syntax authority, CHANGELOG-links-only — structured to match the existing process doc, flagging conflicts rather than overriding.

---

## 4b. HLD direction (revised): machine spec + generated human spec

**Goal:** one precise, parseable (still readable) machine spec; a generated human-readable spec with links, so nobody has to read multiple spec, design and process files to find something. This supersedes "spec files are Markdown with fenced blocks": Markdown becomes the *output* and the commentary layer.

### Layer 1 — machine spec (sole source of rules)

Every rule has a stable ID; everything refers to rules by ID, never by file path.

**The spec format belongs to the tooling, not to Candy.** Candy has no `rule` operator and no metadata syntax, so an earlier s-expression draft (`(rule … :status …)`) was dropped: it looked like Candy but Candy couldn't evaluate it. Chosen instead (options 1 + 4 from the discussion):

```
spec/rules/match.exhaustive.md          one rule per file
spec/examples/match.exhaustive/*.cdy    real Candy example programs
                              *.out     expected output (must succeed)
                              *.err     expected error code (must fail)
spec/grammar.ebnf                       productions tagged (* @id grammar.x *)
```

`spec/rules/match.exhaustive.md`:

```markdown
---
id: match.exhaustive
status: stable
since: 0.3
syntax: grammar.match-expr
see: design.sum-types, errors.E0012
aliases:            # optional: old IDs that still resolve
---
A `match` over a `deft` type must cover every variant, or include `_`.
```

- Example programs are ordinary `.cdy` files: real highlighting, no escaping, runnable on their own. The runner executes them → the spec is the test suite.
- Alternatives considered: plain quoted Candy data (`up`, positional fields — fragile, depends on quoting design); adding metadata to Candy (elegant, but its own HLD). If Candy later gains metadata, rules can move into Candy forms without changing IDs or the book.

### Layer 2 — existing docs tag IDs

Design notes, brainstorming, process doc, changelog stay Markdown; they add anchors `{#design.sum-types}` and references `[[match.exhaustive]]`.

### Generator — one page per rule

Rule prose · syntax · examples marked verified/failing/not run · "Why" (design/process sections that reference the ID, inlined) · history (changelog) · status/since · backlinks · index + glossary of all IDs.

### CI checks

- unknown ID in any `[[…]]`, `see:` or `syntax:` → error
- stable rule with no examples; example folder for an unknown rule; example missing `.out`/`.err` → error
- failing example → error for stable/deprecated rules, warning for draft
- duplicate IDs or aliases → error
- rule no doc references → warning (missing rationale)

Bootstrap gate and stage rules (section 3) unchanged; the generated book doubles as release notes per stage promotion.

### Prototype

`candy-spec-proto.zip` — `tools/specbook.py` (Python, no dependencies), README, and a sample `spec/`, `docs/` and `CHANGELOG.md` for `deft`/`match`. Run `python3 tools/specbook.py` → `book/`. Set `CANDY_RUN` to a command that translates and runs a `.cdy` file to verify examples. Sample Candy code and output formats (`Square(2)`, `E0012`) are placeholders.

### Pros

- **One place to look:** each rule page gathers rule, syntax, examples, rationale, history and backlinks.
- **Docs can't silently go stale:** examples run, links are checked by ID, stable rules need examples.
- **Spec = test suite:** rule examples are what gate stage promotion.
- **Stable IDs survive refactors:** moving files or sections doesn't break links; aliases cover renames.
- **Examples are real `.cdy` files:** normal editing, highlighting, and they run on their own.
- **Lifecycle visible per rule:** status and since tie directly to the stage 0/1/2 feature rule.
- **Gaps get flagged:** "no doc references this rule" exposes missing rationale.
- **Low churn for existing docs:** they stay Markdown and only gain anchors and `[[id]]` links.

### Cons

- **Spec format isn't Candy:** no dogfooding until Candy has quoting or metadata; one more format to learn.
- **Two layers plus a generated one:** contributors must know rules vs. commentary, and not edit `book/`.
- **Rule and example are separate files:** a rule's prose and its examples live in different folders.
- **A tool to maintain:** if the generator breaks, docs and the release gate stop together.
- **ID discipline required:** naming conventions, no reuse, aliases for renames.
- **Strict CI can slow work:** mitigated by letting draft examples fail.
- **Exact-output checks are brittle:** formatting changes ripple; error checks need a stable error-code scheme.
- **Rationale can still drift:** execution keeps examples honest, nothing verifies a "why" paragraph.
- **Up-front migration cost:** every feature must be converted before the book is complete.
- **Pages can get noisy:** mitigated by truncating long "Why" excerpts with a link.

### Verdict

Worth doing. The switch to tooling-owned front matter plus real `.cdy` examples removes the biggest friction (code inside strings) and the false "this is Candy" impression. Revisit the format once Candy has a metadata HLD.

---

## 5. Opening this in the CLI

Try Claude Code's teleport (works for Claude Code web sessions; not confirmed for this chat):

```bash
cd ~/path/to/candy
claude --teleport
```

Fallback: start fresh in the repo with `claude` and use this seed prompt:

> Read our process doc and existing design docs. Write an HLD for "spec-by-example": every spec/docs claim is a fenced `candy run` / `candy error` block with `expect` output, executed by a runner (not written in Candy) that translates .cdy → target and runs it. Include: stage0/1/2 bootstrap gate (stage1 and stage2 pass the spec suite, stage1/stage2 translator output identical, then promote), feature lifecycle draft/stable/deprecated tied to stage promotion (the translator may only use features stable in stage0), coded errors (E0012-style) for expect-error, grammar.ebnf as sole syntax authority, CHANGELOG links only. Match the process doc's structure and flag conflicts with it.

Sources: [What is Teleport in Claude Code](https://www.claudelog.com/faqs/what-is-teleport-in-claude-code/), [Syncing web sessions to local CLI](https://dev.to/proflead/claude-code-tutorial-syncing-web-sessions-to-local-cli-34e0)

**Tip:** you can also hand this file to the CLI directly — `claude "Read candy-spec-by-example-chat.md and our process doc, then write the HLD described in section 4."`
