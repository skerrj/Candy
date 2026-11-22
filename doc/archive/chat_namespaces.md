*Archived 2026-11-21, late, after the merge (it was missed before it), from the Claude
Code session that built branch `namespaces` (2026-11-12 to 2026-11-14; HLD
`doc/hl_rqmt/namespaces.md`, tag `namespaces`), by `script/chat_archive.py`.* The owner's
messages and Claude's replies on the branch, verbatim; each tool call is a one-line
marker, and thinking and tool output are left out. The branch began on `master` (the HLD
was drafted and accepted there). A notice of a background job finishing, which the
harness writes as the owner's turn, is left out. What came of it: the names a file sees
one table ([[B188]]); qualified names, `m.name` ([[B189]]); `import`'s name list
([[B190]]); `(private ...)` ([[B191]]); the naming rules written down ([[B192]]); the
module in Core ([[B193]], [[B65]]); [[B187]], [[B195]], [[B196]] and [[B197]] found; and
"Looking back".

# namespaces

## Claude Code

I've committed the HLD on master as `763ba9a` and created the `namespaces` branch from it, which is now checked out.

**In the commit:**
- `doc/hl_rqmt/namespaces.md` is accepted (2026-11-12), with your answers to all eight questions. Q7 (one task per step) and Q8 (`.` for fields left to later) are as proposed.
- B187 (`alias`, a renaming at translation time, for modules, types and values) is filed as an idea.
- B188 to B194 are the seven step tasks, all `open`:
  1. B188: one table of names;
  2. B189: qualified names;
  3. B190: the name list, and `import`'s shape declared;
  4. B191: private names;
  5. B192: the rules written down;
  6. B193: the module in Core;
  7. B194: docs.
- `backlog/README.md` is regenerated.

The doc-link and backlog tests pass. `git status` showed only my files, none of yours.

Nothing is pushed: master, with the `collections-2` merge and tag and now this commit, and the new branch are all local. Say "go" to start step 1, the table of names.

## Owner

> Go

## Claude Code

*ran: Read core.cdy's first part*

*ran: Find every read of the name maps in core.cdy*

*ran: Read top-names, find-variants, Exports and check-type*

*ran: Read top-names and find users of Exports elsewhere*

*ran: Count Scope field reads and writes*

Step 1 is underway: I've mapped every read of the seven maps in `core.cdy` (and `cdyc.cdy`'s use of `Exports`), and I'm now writing the `Entry` table to replace them.

*ran: Count Scope fields read, and read the match analysis*

*ran: List lines to change and check for name conflicts*

*ran: Show Builtin's variant naming and VInfo uses*

*ran: Check the new names are free*

*ran: Find related error tests and try a sum used as a value*

*ran: Find callers of the helpers being replaced*

*ran: Read analyse-program and put-all's surroundings*

Now the edits, as one script so each replacement is checked to occur once.

*ran: Rewrite core.cdy's name maps as one Entry table*

*ran: Check what lies between type-arities and analyse-program*

Good, the first cut covers all three. I'll drop the redundant lines and type the rename helpers too.

*ran: Prepare a script path*

*wrote: `/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/scratchpad/table.py`*

*ran: Guard the lookups, apply the rewrite, check nothing old remains*

*ran: Build T1 and run the modules test with it*

*ran: Rebuild T1, T2 and bin*

*ran: Add the spec row and run the whole test suite*

The table works: all 634 tests pass and `bin` is rebuilt. Next I'm checking that the Python output is unchanged on every test program, old `bin` against new, and measuring the build and mypy times.

*ran: Compare old and new bin's output on every test program*

*ran: Count the test programs*

*ran: Compare old and new bin on every spec and backlog example*

Only the intended message changed, across 379 examples, 11 programs and the translator itself. Now timing.

*ran: Time the build and mypy, old bin against new*

*ran: Run the linters and type checkers*

*ran: Look at the Done-note format and step 1's text*

*ran: Write step 1's Done note, move B188 to review, rerun checks*

*ran: Get line numbers for the summary*

Step 1 is built and in review. The seven name maps in `core.cdy` are now one table, and the generated Python is unchanged except for one error message I fixed. Nothing is committed yet.

**What changed:**
- **The table:** `Entry` (`core.cdy:103`) has five kinds:
  - `Value`;
  - `Record`, which is both a type and its constructor;
  - `Sum`;
  - `VariantOf`, named that way because Core already has a `Variant`;
  - `Elsewhere`, a name another module defines that this file doesn't import.

  The HLD's `Clash` kind isn't there yet; it arrives in step 2, when a clash stops being reported at the import.
- **How it's filled:** `module-names` (`core.cdy:1091`, with `add-deft` at `:1107`) builds each module's table straight from its forms. `Scope` and `Exports` each now hold just that one table.
- **Removed:** `VInfo`, `Seen`, `find-variants`, `add-variants`, `type-arities`, `prefixed` and `blank-scope`.
- **Imports:** `analyse-module` (`:1143`) starts from the `Elsewhere` entries, adds the imports (`import-names`, `:1161`, which still reports a clash at the import), then the file's own names.
- **Lookups:** about 70 reads became small helper functions: `is-top-value`, `is-sum`, `type-arity`, `variant-sum`, and so on.
- **One behaviour difference:** a file's own definition now replaces an imported name's whole entry. Before, each map was merged separately. It only matters in odd edge cases, and none of the tests reach it.

**The one change you'll see:** using a sum's name as a value, `(deft S (A) (B)) (put S)`, used to say "S is not defined here; m defines it, but this file doesn't import m", even in the file that defines `S`. It now says "S is a type, not a value" (`core.cdy:201`). I added that case to the spec's error table (`spec/20-types.md`, `types.exist`).

**Checked:**
- **Output, against `boot/70`'s `bin`:** identical Python for the 11 test programs, for the translator itself, and for 378 of the 379 spec and backlog examples. The other one is that error.
- **Speed:** the translator builds itself in 0.90 s, against 0.88 s before. mypy on the translator takes 1.62 s, against 1.64 s. The sum-type `Entry` doesn't slow mypy down, so the record fallback isn't needed.
- **Tests:** `pytest` gives 634 passed and 4 xfailed. ruff, mypy, pyright and pylint are clean, and `bin` is rebuilt.

**Docs:** the HLD has step 1's *Done (2026-11-12). As built:* note. B188 is in `review`, and the backlog index is regenerated.

On "gawc" I'll commit this with `boot/71`.

## Owner

> Gawc

## Claude Code

*ran: Check status and how bootstrap.py tags a step*

*ran: Commit step 1 and tag boot/71*

I committed step 1 on `namespaces` as `1e476d8` and tagged it `boot/71`, an annotated tag that needed no staging. The tag script built the step from `boot/70` without problems. The commit holds only my files: no edits of yours were in the tree.

Nothing is pushed. B188 (namespaces step 1: one table of names) stays in `review` until you tick it.

Next is step 2, B189: qualified names `m/name`, and a clash reported only where the name is used. That's where the table gets its `Clash` kind. Say "go" when ready.

## Owner

> Tick, go

## Claude Code

*ran: Tick B188, and read analyse-list*

*ran: Find the import rules in the spec*

*ran: Read the import rule and the module error tests*

*ran: Read the module error cases*

*ran: Read the module test programs and their libraries*

*ran: Find field checks and local binding sites*

*ran: Read the field-name check and bind-params*

*wrote: `/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/scratchpad/qual.py`*

*ran: Simplify the clash message and apply step 2's edits*

Now a test program for qualified names, and a quick T1 run on it.

*ran: Write a qualified-names test program and run it with T1*

*ran: Find the subject-type error*

*ran: Search the checker for the message*

*ran: Look for how the checker displays global names*

*ran: Read rename-top and how sigs flow*

*ran: Translate a small qualified-type program with T1*

The step 2 code is in, but a sig's qualified type (`shapes/Pt`) isn't being renamed to its global name before the check, so I'm debugging that.

*ran: Inspect T1's generated global_name and rename_type*

*ran: See how the checker collects the top-level types*

*ran: Read analyse-type and is-lower*

*ran: Treat a qualified type name as a type, and rerun*

Working now. Next I'm checking the errors from the command line before writing them into the spec.

*ran: Try the qualified-name errors and uses with T1*

*ran: Read the symbols rule in the syntax spec*

*ran: List the syntax spec's rule ids*

*ran: Read the names rule*

*ran: Write the spec: names, import, prelude, and qualified names*

Now the multi-file error cases in `test_self_host.py`, and the own-name case in `qualified.cdy`.

*ran: Update the module error tests, rebuild bin, run the tests*

*ran: Regenerate the index and show the mypy errors*

This is the mypy problem B184 tracks (mypy types an empty-map literal as `dict[Never, Never]`). The workaround is to start the fold from a typed parameter:

*ran: Fold the qualifiers from a typed start, rebuild, test*

*ran: Check the new program is tested, and run the linters*

*ran: Show the pylint warning*

*ran: Wrap the long test line and recheck*

Tests pass. Next I'm checking that the Python output for everything else is unchanged against `boot/71`'s `bin`.

*ran: Compare boot/71's bin and the new bin on every example*

Only the 12 new examples differ. Now the HLD's Done note and B189 (namespaces step 2: qualified names).

*ran: Write step 2's Done note, move B189 to review*

I've ticked B188 (namespaces step 1: one table of names); it's `done`. Step 2 is built and in review, nothing committed.

**What works now:**
- **Qualified names:** every import puts each of its names into the table twice, as `greet` and as `util/greet`. So `m/name` works for values and functions, types (`(sig p shapes/Pt)`), constructors and patterns, with no new lookup code. The prelude is reachable too: `prelude/rest`, `prelude/Some`.
- **A clash is reported only where the name is used** (`import-entry`, `core.cdy:1246`):
  - Two imports defining one name make a `Clash` entry. A use of it as a value, a call, a type or a pattern is an error: "x is defined by a and b: write a/x or b/x" (`clash-error`, `:133`).
  - A file's own definition still wins over a clash.
- **The `/` rule** (`has-slash`, `:105`): a name a program defines (top-level, local, field or variant) can't hold a `/`, except the operator `/` itself.
- **Errors for a qualified name that doesn't resolve** (`qualified-error`, `:121`): a malformed name (`a/b/c`, `/x`), a module the file doesn't import, or a name the module doesn't define.

**Two fixes beyond the table:**
- `analyse-type` read `shapes/Shape` as a type variable, because it starts lowercase (`:871`).
- `match` now compares clauses by their bare names, so `(prelude/Some v)` and `(Some w)` together is "more than one clause". A variant also now carries its sum's variant list, for the exhaustiveness check.
- The qualifiers fold starts from a typed parameter, to get around B184 (mypy types an empty-literal start too narrowly).

**Spec and tests:**
- Spec: `programs.qualified` is new; `programs.import` and `programs.prelude` now say a clash is an error where the name is used; `syntax.names` gets the `/` rule.
- New program `tst/cdy/cdyc/qualified.cdy`, with two modules that both define `label`.
- `test_module_errors`: the old "a and b both define x" at the import became the error where the name is used. It also has a clashing type, a module that's only imported indirectly, and the prelude's clash.

**Checked:**
- Against `boot/71`'s `bin`: the translator's output is the same, and of 391 examples only the 12 new ones differ.
- The build takes 0.94 s, up from 0.92 s.
- `pytest`: 651 passed, 4 xfailed. All the linters are clean.

**Docs:** the HLD has step 2's *Done (2026-11-12). As built:* note. I fixed its spec table, which said `syntax.symbols` where the id is `syntax.names`. B189 is in `review`, and the backlog index is regenerated.

On "gawc" I'll commit this with `boot/72`.

*(The context was summarised here; the turns before it are above.)*

## Owner

> how are these a malformed names (a/b/c, /x)?... guessing `/x` beacuse its starts w/ `/`... but not sure about the other...

## Claude Code

You're right about `/x`: the qualifier before the `/` is empty. `x/` is malformed the same way, because the name after it is empty.

`a/b/c` is malformed because a qualifier is the imported module's **stem**, its file name without the path. `(import lib/shapes)` gives the qualifier `shapes`, so you write `shapes/label`, not `lib/shapes/label` (`import-names` sets `stem/name`, `core.cdy:1246`). With one `/` in the name, a second `/` can't mean anything:
- **`a/b` + `c`:** `a/b` isn't a qualifier, because a stem never holds a `/`.
- **`a` + `b/c`:** `b/c` isn't a name, because the `/` rule stops a definition from holding a `/` (`has-slash`, `:105`).

So `qualified-error` (`:121`) rejects any name that doesn't split into exactly two non-empty parts.

The other way to do it was to allow the path, `lib/shapes/label`, as a second spelling. That would be a way to tell apart two imports with one stem (`util` and `lib/util`). The HLD left that case to B187 (`alias`, a renaming at translation time), and for now two imports with one stem get one qualifier.

The current message, "a qualified name is m/name, one / between a module and a name", doesn't say that `m` is the stem, which is exactly what `lib/shapes/label` gets wrong. I'd sharpen it to:

> `lib/shapes/label`: a qualified name is m/name, with `m` the module's file name without its path (`shapes/label`)

It's a one-line change, plus the matching rows in `spec/00-syntax.md` and `spec/10-programs.md`. Should I make it before the commit? I recommend yes.

## Owner

> do lets move to `.`'s

## Claude Code

*ran: Check how the reader treats dots and whether names use them*

*ran: Read the reader's number scanning and py-mangle*

*ran: Find dotted symbols and every slash use in the translator*

*ran: Check built-ins for dots and find files using slash qualifiers*

*ran: List slash mentions in the namespaces HLD*

*ran: Read HLD questions 3 and 8 and the epic's separator decision*

*ran: Show the qualified-name helpers and slash uses in the backlog items*

*ran: Switch core.cdy's qualifier from slash to dot*

*ran: Fix the remaining slash comments in core.cdy*

Now the spec, the tests and the program.

*ran: Show the step's spec changes, test program and test cases*

*ran: Read the names rule around its a.b example*

*ran: Read the names rule's examples*

*ran: Rewrite the spec rules and examples for the dot qualifier*

*ran: Update the qualified test program and module error tests*

*ran: Rewrap the program's comment and rebuild bin*

The rebuild worked. Next I'm running the full test suite and the linters.

*ran: Run the test suite*

*ran: Inspect the failing syntax example*

`.5` used to be an ordinary (unknown) name. Now it's a malformed qualified name, so I'm updating that row and its sentence:

*ran: Fix the .5 example and rerun the tests*

Tests pass. Now the linters, and then the docs: the HLD's Q3, Q8 and step 2 note, B189 (namespaces step 2: qualified names), B187, and the epic.

*ran: Run all linters and type checkers*

*ran: Read the HLD and B189 passages that mention the slash*

*ran: Switch the HLD's qualified names to dots, keeping Q3's record*

*ran: Record the separator change in the HLD's Q3, Q8 and step 2 note*

*ran: Note the change in B189, B187 and the epic, then check doc links*

I've switched the qualifier to `.` and made the message sharper. Nothing is committed, and B189 (namespaces step 2: qualified names) is still in review.

**What changed in the translator** (`src/cdy/core.cdy`):
- `has-slash` and `slash-error` are now `has-dot` and `dot-error` (`core.cdy:103`). A name the program defines can't hold a `.`, and the lone `/` no longer needs an exception.
- An import adds `stem.name` to the table (`:1239`). The clash message now says "write a.x or b.x".
- A malformed name now says `a.b.c: a qualified name is m.name, one . between a module (its file name, without its path) and a name` (`:126`).
- The reader is unchanged: it already reads `shapes.label` as one symbol and still reads `3.14f` as a number. Nothing in the translator, the library, the tests or the spec had a `.` in a name.

**Two things changed for programs:**
- **A `/` in a name is ordinary again**, as it was before this branch. `syntax.names` now has a running example with `a/b`. Import paths like `lib/util` are unaffected.
- **`.5` is now an error:** "a qualified name with no module". It used to be an ordinary name, and only one spec row wrote it (`spec/00-syntax.md:99`). I updated that row and the sentence above it.

**Docs:**
- In the HLD, Q3 keeps its original answer, followed by a dated *Changed (2026-11-13)* note. Q8 gets a line saying field syntax will now need a rule for a local named like a qualifier. Step 2's Done note records the change. The proposal text now uses `.` throughout. The "Today" table and Q3's own text still show `/`, because they record what was true then.
- B189 and B187 (`alias`, a renaming at translation time, for modules, types and values) each have a note. B187's old example line is kept verbatim.
- The epic's "Qualified names" entry in `python_complete.md` has a *Changed* note.

**Checked:** `pytest` gives 651 passed and 4 xfailed. All the linters are clean, the doc-link and backlog tests pass, and `bin` is rebuilt.

On "gawc" I'll commit this with `boot/72`.

## Owner

> so, no `/` or `\` in symbol names... and symbol names can't start or have a `.` ...?

## Claude Code

Not quite, on `/`. Here's where each one stands:

- **`\`:** a name can't hold one. That rule is older than this branch: a name runs up to a `'`, `"` or `\` (`syntax.names`), so `a\b` reads as the name `a` followed by the character literal `\b`. A name can't start with one either, because a `\` starts a character.
- **`.`:** a name a program defines can't hold one anywhere, at the start, the middle or the end. That covers top-level names, locals, fields and variants (`dot-error`). A name a program *uses* can hold exactly one `.`, as `m.name`. Anything else with a `.` (`a.b.c`, `.x`, `x.`, `.5`) is an error saying "a qualified name is m.name". A `.` inside a number is still the number's (`3.14f`).
- **`/`:** a name can hold one again (`a/b`, `->a/b`), as it could before this branch. The lone `/` is just the division operator. Import paths (`lib/util`) aren't names, so they're unaffected either way.

So the question is whether `/` should be ordinary or reserved:

1. **Ordinary (what's built now):** nothing changes from before the branch. But `a/b` looks like a Clojure-qualified name or a path, and it isn't one.
2. **Reserved:** a name can't hold a `/`, except the lone operator. This brings back step 2's `/` rule (it was `has-slash`), but with an error that doesn't mention qualifiers: "a name can't hold a /". It's about 3 lines in `core.cdy` and the 4 spec rows again.

I recommend 2. Reserving it now is cheap, it keeps `/` free for later, and it avoids names that look like paths. Un-reserving later breaks nothing, but reserving later could break programs that already use `/` in names.

## Owner

> 2, reserve `/`

## Claude Code

*ran: Find the dot checks at definition sites and any slash names*

*ran: Generalise the definition-site check to reserve the slash*

Now the spec's names rule:

*ran: Reserve the slash in the names rule and examples*

*ran: Read the HLD lines that call the slash ordinary*

*ran: Update the HLD and B189, rebuild bin, run the tests*

*ran: Run all linters and type checkers*

`/` is reserved again: a name a program defines can't hold one, except the operator `/` itself. Nothing is committed yet.

**The rules for names now:**
- **`.`:** a name a program defines can't hold one. A name it uses can hold exactly one, as `m.name`.
- **`/`:** a name a program defines can't hold one. Using an undefined `a/b` gives the usual "unknown name a/b", since nothing can define it. Import paths like `lib/util` aren't names, so they're unaffected.
- **`\`:** a name can't hold one, as before this branch, because a `\` starts a character literal.

**What changed:**
- **The check** (`core.cdy:106`): `dot-error` became `name-error`, which covers both characters. It's used wherever a definition's name is checked: top-level names (`add-entry`), locals (`bind-local`) and fields. A name with a `/` gets "a/b: a name can't hold a /, which is reserved".
- **The spec:**
  - `syntax.names` says a `/` is reserved and gets 3 new error rows. The `a/b` example I'd added last round is gone.
  - `programs.qualified` says a `/` is no qualifier: it's an import's path, and a name can't hold one.
- **The docs:** the HLD's Proposal, its Q3 *Changed* note and its step 2 Done note, and the B189 (namespaces step 2: qualified names) note, now say `/` stays reserved.

**Checked:** `bin` is rebuilt. `pytest` gives 654 passed and 4 xfailed, and all the linters are clean.

On "gawc" I'll commit this with `boot/72`.

## Owner

> i miss read it... can we go back to "
>
> <pasted_content id="cd30">
> a/b/c is malformed because a qualifier is the imported module's stem, its file name without the path. (import lib/shapes) gives the
>   qualifier shapes, so you write shapes/label, not lib/shapes/label (import-names sets stem/name, core.cdy:1246). With one / in the name,
>   a second / can't mean anything:
>   - a/b + c: a/b isn't a qualifier, because a stem never holds a /.
>   - a + b/c: b/c isn't a name, because the / rule stops a definition from holding a / (has-slash, :105).
> </pasted_content id="cd30">
>
> " (don't change anything you've done) just want to understand it?

## Claude Code

Sure. It comes down to how a qualified name is split. I'll explain it with `/`, as it was then; it works the same way now with `.`.

**A qualified name has two parts, a module and a name:**

```
shapes/label
^^^^^^ ^^^^^
module  name
```

The translator splits at the `/`. The left part has to be an imported module's **qualifier** and the right part has to be a **name that module defines**.

**The qualifier is just the file's name, with no folders.** Take this import:

```
(import lib/shapes)
```

`lib/shapes` is a path to `lib/shapes.cdy`. The qualifier is only the last piece, `shapes`, so you write `shapes/label`, never `lib/shapes/label`.

**So what could `a/b/c` mean?** With two `/`s there are two places to split, and both fail:

| Split | Left (the module) | Right (the name) | Why it fails |
|---|---|---|---|
| `a/b` + `c` | `a/b` | `c` | A qualifier is a file name without folders, so it never has a `/` in it. |
| `a` + `b/c` | `a` | `b/c` | No module can define a name with a `/` in it, because that's an error at the definition. |

Neither reading can ever name anything, so the translator calls it malformed instead of looking it up.

**`/x` and `x/` fail for a simpler reason:** one side is empty. `/x` has no module, and `x/` has no name.

**With `.` today it's the same:** `a.b.c` can't be `a.b` + `c`, because a qualifier never holds a `.`. It can't be `a` + `b.c` either, because no definition can hold a `.`. `.x`, `x.` and `.5` each have an empty side.

The one way `a/b/c` could have meant something was as a path plus a name (`lib/shapes/label`). The HLD decided against that: a qualifier is always the short file name, and B187 (`alias`, a renaming at translation time) is the planned way to handle two files with the same name.

## Owner

> Tick this "Errors for a qualified name that doesn't resolve (qualified-error, :121): a malformed name (a/b/c, /x), a module the file doesn't import, or a name the module doesn't define."

## Claude Code

*ran: Record the partial tick in B189's notes*

I've recorded your tick on that part in B189's notes, dated 2026-11-13 (`backlog/B189-namespaces-step-2.md`). It covers `qualified-error`'s three errors: a malformed name, a module the file doesn't import, and a name the module doesn't define.

B189 (namespaces step 2: qualified names) itself stays `review`, because the rest of the step hasn't been ticked yet:
- `m.name` resolving through the table;
- a clash being an error only where the name is used;
- the `.` and `/` rules for names;
- `match` comparing variants by their bare names;
- `.5` now being an error.

Say "tick" for the whole step and I'll set it to `done`. On "gawc" I'll commit, then tag `boot/72`.

## Owner

> Let's review pros/cons of moving from `/` to `.`

## Claude Code

The switch costs almost nothing now, since nothing is committed and no program wrote either form. The real trade-off is how each choice sits with field syntax, which Candy doesn't have yet (only `(get p x)`).

### For `.`
- **It's familiar.** Python, Java, OCaml, JavaScript and C# all write `module.name`, so most readers will parse `shapes.label` instantly.
- **It looks different from an import path.** With `/`, `(import lib/shapes)` and then `shapes/label` look like the same kind of thing, a path, and they aren't. That's the confusion over `a/b/c` from earlier. With `.`, paths use `/` and qualified names use `.`, so the two can't be mixed up.
- **No exception for division.** `/` was both the operator and the separator, so `has-slash` needed a special case for the lone `/`. Now `/` is only division (and reserved in names).
- **One meaning for fields and modules is possible.** If Candy gets field syntax, `p.x` and `m.x` can share the `.`, as in Python and OCaml (Q8).
- **It suits deeper module trees.** If the `library` branch ever qualifies by a path instead of a stem (`collections.list.map`), dots read naturally, as in Python's `os.path.join`.

### Against `.`
- **It collides with future field syntax.** This is the real cost. If `p.x` ever means a field, `a.b` becomes ambiguous to the reader: is it a module's name or a value's field? The translator can still tell them apart statically, but it needs rules:
  - What happens to a local named like a qualifier? Is it an error, or does the local win?
  - How do chains like `m.p.x` read?
  - Errors get vaguer. "this file doesn't import a module p" is unhelpful when you meant a field.

  With `/`, modules and fields would be told apart just by how they're written.
- **The Lisp tradition is `/`.** Clojure, the closest S-expression relative, uses `ns/name` and keeps `.` for host interop. The epic chose `/` for that reason.
- **Lisps have used `.` for other things.** Scheme uses it for dotted pairs and rest arguments, as in `(a . b)`. Candy has `(Rest t)` and no pairs, so this costs nothing today, but it rules those uses out later.
- **`.5` is now an error.** It used to be just an unknown name, so this is minor.
- **Numbers and names share a character.** The reader already tells them apart (`3.14f` is a number, `a.b` a name), so this costs nothing in practice.

### Recommendation
Keep `.`. Its biggest benefit, not looking like an import path, applies to every program today. Its biggest cost only arrives with field syntax, which isn't designed yet. And since Candy resolves names statically, the ambiguity can be handled with one rule: a local named like an imported module's qualifier is an error. OCaml's convention, uppercase modules and lowercase values, is another way out, but it doesn't fit Candy's lowercase stems.

To make sure this isn't forgotten, I can add a `doc/brainstorm.md` entry, or an `idea` backlog item, for "field syntax with `.`, and a local named like a qualifier", linked from the HLD's Q8.

## Owner

> So 0.5 works but .5 fails?

## Claude Code

Yes, and `.5` wasn't a number before this branch either. The only thing that changed is the error message.

| Written | Before this branch | Now |
|---|---|---|
| `0.5` | the `Double` 0.5 | the `Double` 0.5 |
| `.5` | the *name* `.5`, so `unknown name .5` | `.5: a qualified name is m.name` |
| `5.` | error: `unexpected 5` | the same |

`syntax.numbers` (`spec/00-syntax.md:88`) says a number has digits on *both* sides of its `.`, as in Kotlin and Rust. So `.5` and `5.` were never numbers. `5.` is a number error because it starts with a digit, and `.5` read as a name, so you got "unknown name .5". Now a `.` in a name means a qualifier, so `.5` reads as a qualified name with no module.

If the old message is the one you'd rather keep, I could special-case it: a name that starts with `.` followed by a digit could say `.5: a number needs a digit before its . (0.5)`. It's a few lines in `qualified-error` and a change to one spec row. I'd recommend it, since it tells the reader how to fix it rather than talking about modules.

## Owner

> Ok add error and idea

## Claude Code

*ran: Find the next backlog id, priorities, and qualified-error*

*ran: Add the number hint for .5 and its spec rows*

Now the idea item, B195:

*wrote: `backlog/B195-field-syntax-dot.md`*

*ran: Link B195, note the hint, rebuild bin and run the tests*

*ran: Run all linters and type checkers*

I added both: `.5` now gets a number error, and the field-syntax question is filed as B195. Nothing is committed yet.

**The error:**
- `.5` now says `.5: a number needs a digit before its . (0.5)`, and `-.5` gets the same with `(-0.5)`.
- A new Candy `defn`, `number-hint` (in `core.cdy`, just above `clash-error`), recognises a word with an optional `-`, then a `.`, then a digit. `qualified-error` checks it before its other cases.
- Something like `.x` still says "a qualified name is m.name".
- `syntax.numbers` (`spec/00-syntax.md:88`) has rows for `.5`, `-.5` and `.x`, and its sentence says the error now names the problem.

**The idea:** B195 (field syntax with `.`, and a local named like a qualifier), in `backlog/B195-field-syntax-dot.md`, kind `idea`, state `open`. It lists what that design must settle:
- a local named like an imported module's qualifier: an error (my proposal) or the local wins;
- chains like `m.p.x` and `p.q.x`, read left to right;
- an error that names both readings, when `p` is neither a value nor an import;
- whether `(f 1).x` works, or only `name.x`;
- whether `p.x` only reads a field, with `assoc` still the way to write one.

The HLD's Q8 note now links to B195, the Q3 *Changed* note mentions `number-hint`, and B189 (namespaces step 2: qualified names) has a dated note. I ran `git add -N` on B195 and regenerated the backlog index.

**Checked:** `bin` is rebuilt. `pytest` gives 656 passed and 4 xfailed, and all the linters are clean.

B189 is still in `review`, with only the `qualified-error` part ticked. On "tick" I'll set it to `done`, and on "gawc" I'll commit with `boot/72`.

## Owner

> Put up 189

## Claude Code

*ran: Show the B189 backlog item*

Here's `backlog/B189-namespaces-step-2.md` as it stands:

```markdown
# B189: namespaces step 2: qualified names

kind: task
state: review
priority: normal
found: namespaces, 2026-11-12
fixed: namespaces, 2026-11-12
where: `src/cdy/core.cdy`, `spec/10-programs.md`, `spec/00-syntax.md`
refs: [[B47]]

Step 2 of `doc/hl_rqmt/namespaces.md`. `m/name` for a module `(import m)` imports, for values,
types and variants, and in patterns; the `/` rule in names (a lone `/` the operator); two
imports that define one name an error only where it is used unqualified; `programs.qualified`
(new), `programs.import`, `syntax.symbols`.

## Notes

- 2026-11-12, Claude: filed on the HLD's acceptance (the owner, 2026-11-12).
- 2026-11-12, Claude: built (the HLD's step 2 *Done* note): `m/name`, the `/` rule, and a
  clash an error only where the name is used. In review.
- 2026-11-13, the owner: in review, the separator `.`, not `/` (the HLD's Question 3,
  changed), and a `/` in a name still an error, reserved. Claude: rebuilt with `.`
  (`has-dot`, and `name-error` for a definition's `.` or `/`); `.5` is now an error, a
  qualified name with no module. In review.
- 2026-11-13, the owner: ticked in review, the errors for a qualified name that doesn't
  resolve (`qualified-error`): a malformed name, a module the file doesn't import, a name
  the module doesn't define. The rest of the step is still in review.
- 2026-11-13, the owner: `.5` should say it is a number with no digit before its `.`.
  Claude: `number-hint`, for `.5` and `-.5` (`syntax.numbers`); field syntax with `.`
  filed as [[B195]].
```

The description paragraph is out of date in two places:
- It still says `m/name` and "the `/` rule in names (a lone `/` the operator)", from before the switch to `.`.
- It names `syntax.symbols`, but that rule's id is `syntax.names`. I fixed the same mistake in the HLD but missed it here.

I suggest rewriting the paragraph to say `m.name`, "the `.` rule in names, and `/` reserved", and `syntax.names`. The old paragraph would go verbatim into a dated note, as the backlog rule says. Should I do that?

## Owner

> Ya

## Claude Code

*ran: Rewrite B189's text and keep the old one in a note*

I've rewritten B189's description (`backlog/B189-namespaces-step-2.md:11`):

> Step 2 of `doc/hl_rqmt/namespaces.md`. `m.name` for a module `(import m)` imports, for values, types and variants, and in patterns; the `.` rule in names, and `/` reserved (a lone `/` the operator); two imports that define one name an error only where it is used unqualified; `programs.qualified` (new), `programs.import`, `syntax.names`.

The old paragraph is kept word for word in a `text` fence, in a new dated note at the end (`:31`). I regenerated the backlog index, and the backlog and doc-link tests pass.

B189 (namespaces step 2: qualified names) is still `review`. On "tick" I'll set it to `done`, and on "gawc" I'll commit with `boot/72`.

## Owner

> Tick, gawc

## Claude Code

*ran: Tick B189, check status and how boot/71 was tagged*

Every changed file is mine; I don't see any edits from you in the tree. Committing:

*ran: Commit namespaces step 2*

*ran: Tag boot/72 and verify it is annotated*

I ticked B189 (namespaces step 2: qualified names) and committed step 2 as `ccee846`, "namespaces step 2: qualified names". Nothing is pushed.

- **What's in the commit:**
  - the translator change (`core.cdy`) and the rebuilt `bin`;
  - the spec changes (`programs.qualified`, `programs.import`, `programs.prelude`, `syntax.names`, `syntax.numbers`);
  - the new test program `qualified.cdy` and the updated `test_module_errors`;
  - the HLD's step 2 note and the Q3 and Q8 changes, plus the epic's note;
  - the backlog: B188 and B189 `done`, B195 (field syntax with `.`) filed, B187's note.

  I checked `git status` first: every changed file was mine, none of yours.
- **The tag:** `bootstrap.py --tag` checked step 72 and tagged `boot/72` on `ccee846` (staging: none). `git cat-file -t refs/tags/boot/72` gives `tag`, so it's annotated.
- **Not pushed yet:** master (`05d1632`, `763ba9a`, tag `collections-2`), the `namespaces` branch, and tags `boot/71` and `boot/72`.

Next is step 3, B190 (namespaces step 3: the name list, and `import`'s shape declared): `(import m (a b))`, and `(special import (ModName (Opt (List Name))))` in `special.cdy`. Say "go" and I'll start it.

## Owner

> Go

## Claude Code

*ran: Read B190, the HLD's step 3 and special.cdy*

*ran: Read bootstrap.py's staging documentation*

*ran: Find where import and special forms are handled*

*ran: Read include.cdy's module reading and import parsing*

*ran: Trace how imports flow into analysis*

*ran: Read the driver's module loop and analyse-module*

*ran: Check modules.md's Import record and special.cdy readers*

*ran: Read cdyc's pipeline, include's inclusion and read-builtins*

*ran: Find import-name callers, name clashes and form helpers*

*ran: Read form helpers and include's header*

Writing `src/cdy/syntax.cdy`:

*wrote: `src/cdy/syntax.cdy`*

That first `cond` clause in `read-shape` is muddled. Rewriting it:

*edited: `src/cdy/syntax.cdy`*

*ran: Declare import's shape and accept shapes in read-decls*

Now `include.cdy`:

*ran: Check imports against the shape in include.cdy*

*ran: Find Elsewhere handling in resolve and check-type*

*ran: Read the Entry type and clash-error uses*

*ran: Carry the name list into core's table*

Building:

*ran: Rebuild bin through T1 and T2*

It built first time. Trying the forms by hand:

*ran: Try the name list and its errors by hand*

Everything behaves as intended: the name list, `m.b` for an unlisted name, and each error. Next the spec. Reading `programs.import`:

*ran: Read the programs.import spec section*

The spec examples are single files, so the name list's running example will be a test program with a module next to it. The spec text and the single-file error rows go here:

*ran: Write the name list into programs.import*

*ran: Write and run the name list test program*

*ran: Check for a stray output dir and record the expected output*

*ran: Check when the stray directories were created*

*ran: List the stray output directory*

*ran: Remove my stray output and read test_module_errors*

The name list works, the new test program `import_list.cdy` passes, and the spec text is written. Next I'm adding the multi-file error cases to `test_module_errors`.

*ran: Add the name list's module errors and run them*

*ran: Let the grammar test read a shaped special, run all tests*

*ran: Show the pytest warning*

*ran: List scratch scripts and run the linters*

*ran: Format the test file and look at the long lines*

*ran: Wrap the long line, recheck, and read the compare script*

*ran: Look for the earlier output-comparison script*

*ran: Inspect the earlier per-boot comparison directories*

*ran: Read the earlier example comparison script*

The linters are clean and the tests pass. Next I'm comparing the Python output against `boot/72`'s `bin` on the test programs, the spec examples and the translator itself.

*ran: Compare boot/72's bin and the new bin on every program*

Only the new program differs; `boot/72` can't read its name list. The translator's own Python output is identical. Timing the build:

*ran: Time the translator building itself, old and new*

The build takes about 1.03 s against 1.00 s for `boot/72`. Now the HLD's step 3 note and B190:

*ran: Write step 3's Done note and move B190 to review*

Step 3, B190 (namespaces step 3: the name list, and `import`'s shape declared), is built and in `review`. Nothing is committed.

**What it does:**
- **`(import m (a b))`** makes only `a` and `b` unqualified. Every name the module defines is still reachable as `m.name`, and `(import m ())` makes no name unqualified.
- **Using an unlisted name** says `b: the import of m doesn't list it: write m.b`. This works for a value, a type and a pattern.
- **The name list's errors** point at the bad name: `import: m doesn't define c` and `import: a is listed twice`.
- **`import`'s shape is declared** in `special.cdy` as `(special import (ModName (Opt (List Name))))`. A form that doesn't fit gets an error written from the shape: `import: expected (import ModName [(Name*)])`.
- **A macro file's `import`** is inclusion, so it can't list names, and says so.

**How it's built:**
- **New translator module `src/cdy/syntax.cdy`.** It reads a shape into `Syntax` (`SynName`, `SynModName`, `SynList`, `SynOpt`, with `Opt` allowed only last), checks a form against it (`fits-shape`) and writes the error from it (`shape-text`). I didn't call the type `Shape` because `check.cdy` already has a `Shape` type.
- **`include.cdy`** reads `import`'s shape from `special.cdy` once per module and checks each import with `import-parts`. Its `Imp` now carries the listed names.
- **`core.cdy`:**
  - A new `Import` record passes the list on to analysis; it is `modules.md`'s `Import`, without the alias.
  - Unlisted names go into the table as a new `Unlisted` entry, which any other import's entry for the same name replaces.
  - `clash-error` is renamed `use-error`, because it now handles both cases.
  - `read-decls` checks every shape declared in `special.cdy`.
- **Tests:**
  - new program `tst/cdy/cdyc/import_list.cdy`; it imports `lib/shapes` and `lib/tags` with name lists, and since only one import lists `label`, there's no clash;
  - 4 new cases in `test_module_errors`;
  - `programs.import` in the spec, with the new rule and 7 error rows;
  - `test_editor_grammar`'s pattern now also matches a special form declared with a shape.

**Checked:**
- `pytest`: 666 passed and 4 xfailed. All the linters are clean.
- Against `boot/72`'s `bin`: of 92 programs, only the new one differs. The old translator can't read a name list, and the translator's own Python output is identical.
- The build takes about 1.03 s, against 1.00 s for `boot/72`.

**Staging:** `boot/72`'s translator can't read the new `special.cdy`, and `test_bootstrap` warns about exactly that. So this step needs `old-library` staging. On "gawc", I'll commit, add the commit's hash to `STAGING` in `script/bootstrap.py`, then run `bootstrap.py --tag` for `boot/73`. That `STAGING` line will be the one uncommitted change, and it goes into the next step's commit.

**Not done yet:** CLAUDE.md's module list doesn't mention `syntax.cdy`. That belongs to step 7, B194 (namespaces step 7: docs).

## Owner

> Can we do a recall on `old-library` staging real quick?

## Claude Code

*ran: Read how bootstrap.py runs old-library staging*

Here's how `old-library` staging works.

**Why a step can need it.** The bootstrap chain (`script/bootstrap.py`) re-runs history one step at a time. For each `boot/NN` commit, it takes the *previous* step's translator, puts it in that commit's `bin/py/`, and rebuilds `bin`. The result has to match the checked-in `bin` byte for byte. The translator reads its library files (`special.cdy`, `system.cdy`, `prelude.cdy` and so on) at run time from the directory it sits in. So in a step's checkout, the *old* translator is sitting next to the *new* library. That's fine until a step changes the library in a way the old translator can't parse.

**This step does exactly that.** `boot/72`'s `read-decls` accepts only `(special name)`. It fails on `(special import (ModName (Opt (List Name))))` before translating anything. `test_bootstrap` saw it ahead of time: "boot/72 can't read today's library: the next boot step needs staging old-library".

**What the staging does** (`bootstrap.py:163`). Before the build, it extracts the *parent commit's* library files (`git archive <commit>^ -- bin/*/*.cdy`) next to the old translator. It's a bridge:
1. The old translator, with the old library it understands, translates the step's new translator source.
2. The step's own `self_host.py` then builds as usual from that result: T1, then T2, with the step's own library copied back. It checks the result against the checked-in `bin`.

**Where it's recorded.** A step that needs staging says so in its tag's message, as a `staging: old-library` line. Until the tag exists, the `STAGING` map in `bootstrap.py` holds the line, keyed by the commit's full hash. That's why the hash can only go in after the commit. `--tag` reads the map and writes the line into the tag.

**Used once before:** `f0f062d`, collections step 2 (2026-11-09). There `system.cdy` gained the operators' `sig`s, which the translator before it couldn't read.

**The alternative is two boot steps, with no staging:**
1. a commit that only teaches `read-decls` to accept `(special name shape)`, with a rebuilt `bin`, tagged `boot/73`;
2. a commit that adds the shape to `special.cdy` and everything else, tagged `boot/74`.

That keeps the chain free of bridges, but it splits step 3 into two commits, against the one-commit-per-step rule.

I recommend the staging. B190 (namespaces step 3: the name list, and `import`'s shape declared) planned for it, the mechanism has worked before, and it keeps step 3 one commit. The cost is the `STAGING` line, which gets committed in the next step.

## Owner

> So, it's the "temporary" boot chain thing?

## Claude Code

Partly. The bridge itself is permanent; only where it's written down starts out temporary.

- **The bridge is permanent.** Every future run of the chain (`--check`, `--from-scratch`, `pytest -m bootstrap`) will use the parent's library at this step, because the old translator will never be able to read the new `special.cdy`. The tag records that for good: `boot/73`'s message will say `staging: old-library`.
- **The `STAGING` entry is the temporary part.** It holds the line from the commit until `--tag` writes it into the tag, because the tag can't exist before the commit. Once the tag exists, the tag is the record. In practice the three entries already in `STAGING` have stayed after their tags were made, so this one would stay too.

So nothing gets undone later, and the chain doesn't hit a temporary step that breaks when something is removed. It just carries one more bridge at `boot/73`, as at `f0f062d`. The two-commit route is the one that avoids a bridge entirely.

## Owner

> Gawc

## Claude Code

*ran: Commit namespaces step 3*

Committed as `b98b523`. Now the staging entry and the tag:

*edited: `script/bootstrap.py`*

*ran: Tag boot/73 with old-library staging and verify it*

I've committed step 3 as `b98b523`, "namespaces step 3: the name list, and import's shape declared". Before committing, I checked `git status`: every changed file was mine, none of yours. Nothing is pushed.

- **Tag:** I added `b98b523`'s full hash to `STAGING` as `old-library`, then ran `bootstrap.py --tag`. Step 73 passed through the bridge, and `boot/73` is tagged on `b98b523` with `staging: old-library`. `git cat-file -t refs/tags/boot/73` gives `tag`, so it's annotated.
- **One uncommitted change:** that `STAGING` line in `script/bootstrap.py`. It goes into the next step's commit.
- **B190 (namespaces step 3: the name list, and `import`'s shape declared):** still `review`, waiting for your tick.
- **Not pushed yet:** master (`05d1632`, `763ba9a`, tag `collections-2`), the `namespaces` branch, and tags `boot/71`, `boot/72` and `boot/73`.

Next is step 4, B191 (namespaces step 4: private names), the `(private a b)` form. Say "go" to start it.

## Owner

> Go

## Claude Code

Starting step 4, B191 (namespaces step 4: private names). First the HLD's private-names text, then how top-level forms like `sig` get through expansion and analysis:

*ran: Read B191, analyse-tops and expand's untouched heads*

*ran: Read module-exports, Exports and module-names*

*ran: Check the non-top error, Exports uses, grammar and elsewhere-names*

*ran: Find where the grammar lists definition forms*

Writing the core changes:

*ran: Add private names to core, expand, special.cdy and the grammar*

*ran: Rebuild bin*

*ran: Try private names and their errors by hand*

Everything behaves as intended: private values, functions, types and their variants, both unqualified and as `m.name`, and each error. Now the spec section, a test program and the multi-file errors:

*ran: List the programs spec ids and the HLD's private-name mentions*

*ran: Read the end of programs.qualified and the HLD staging note*

*ran: Write programs.private, the counter module and its test program*

*ran: Add private-name module errors and run all tests*

All 680 pass, with no bootstrap warning this time: `boot/73` reads the new `special.cdy`. Linters, then the comparison against `boot/73`'s `bin`:

*ran: Lint, compare against boot/73's bin, and time the build*

*ran: Show the ruff finding*

This ruff finding is from step 3's line wrap, which is already committed: I didn't rerun `ruff check` after wrapping that line. Fixing it here, in step 4:

*ran: Parenthesise the concatenated string and recheck*

Now the HLD's step 4 note and the backlog:

*ran: Write step 4's Done note and move B191 to review*

Step 4, B191 (namespaces step 4: private names), is built and in `review`. Nothing is committed.

**What it does:**
- **`(private a b)`**, a top-level form, keeps those names in their module. An importer that uses one gets an error, unqualified (`x is private to m`) or as `m.x` (`m.x: x is private to m`). So does listing one in an import (`import: x is private to m`).
- **What can be private:** any name the file defines except a variant on its own. A private type's variants are private with it, and `(private A)` on a variant says `private only with its type: (private S)`.
- **Other errors:** a name the file doesn't define, a name listed twice, something that isn't a name, and `private` anywhere but top level.
- **A private name doesn't clash.** If one import keeps `label` private and another exports it, `label` means the public one.
- **Abstract types work.** A public function can take or return a value of a private type. The importer can hold that value but can't name the type or take it apart. The test program is built on this.

**How it's built:**
- `(special private)` has a rule of its own, not a shape, so no staging is needed: `boot/73` reads it fine. This is because the HLD reserves shapes for `import` in this branch.
- `module-exports` reads the `(private ...)` forms into a new field, `Exports`' `privates` (`private-names`, `add-private`).
- An importer's table gets a `Private` entry for each name, both unqualified and as `m.name`.
- `unlisted-entry` became `hidden-entry`, shared by `Unlisted` and `Private`.
- `elsewhere-names` leaves out private names. So a private name from a module you don't import is just "unknown name", not "b defines it, but this file doesn't import b".
- Expansion leaves the form alone, and the VS Code grammar now highlights `private`.
- The translator itself doesn't use any private names yet.

**Spec and tests:**
- `programs.private` is new, with a running example and 5 error rows.
- New program `tst/cdy/cdyc/private.cdy`, with `lib/counter.cdy`. The counter keeps its type, its helper and its `label` private, and `lib/tags`' public `label` wins.
- 5 new cases in `test_module_errors`.

**A fix to step 3:** `b98b523` left one ruff finding in `test_self_host.py` (ISC004). I wrapped a message line and didn't rerun `ruff check` afterwards. It's fixed in this step, and B190 (namespaces step 3: the name list, and `import`'s shape declared) has a note about it.

**Checked:**
- `pytest`: 680 passed and 4 xfailed. All the linters are clean.
- Against `boot/73`'s `bin`: of 94 programs, only the two new ones differ, because the old translator doesn't know `private`. The translator's own Python output is the same.
- The build still takes about 1.0 s.

The `STAGING` line for `b98b523` in `script/bootstrap.py` will go into this commit. On "gawc" I'll commit with `boot/74`.

## Owner

> Gawc

## Claude Code

*ran: Commit step 4, tag boot/74 and verify*

I've committed step 4 as `ce43e79`, "namespaces step 4: private names". Nothing is pushed.

- **What's in the commit:** private names; step 3's `STAGING` line (`b98b523`, `old-library`); and the fix for step 3's ruff finding. I checked `git status` first: every changed file was mine, none of yours.
- **Tag:** `bootstrap.py --tag` checked step 74 and tagged `boot/74` on `ce43e79` (staging: none). `git cat-file -t refs/tags/boot/74` gives `tag`, so it's annotated.
- **Tree:** clean.
- **Waiting for your tick, still `review`:**
  - B190 (namespaces step 3: the name list, and `import`'s shape declared);
  - B191 (namespaces step 4: private names).
- **Not pushed yet:** master (`05d1632`, `763ba9a`, tag `collections-2`), the `namespaces` branch, and tags `boot/71` to `boot/74`.

Next is step 5, B192 (namespaces step 5: the rules written down). It covers one namespace, what every file sees, shadowing, and making a variant or value named like a macro an error. Say "go" to start it.

## Owner

> Go

## Claude Code

Starting step 5, B192 (namespaces step 5: the rules written down). Reading the item, the HLD's sections it covers, and the backlog items it closes:

*ran: Read B192, the HLD's rules sections and B40, B11, B50*

*ran: Read shadowing, B50's part, programs.top-level and the macros rules*

*ran: Look at a closed defect and a kept item for their shape*

*ran: Reject a deft type or variant named like a macro, rebuild*

Now probing the cases the spec will state, so the rows say what the translator actually does:

*ran: Probe namespace, shadowing and macro-name cases*

*ran: Search the backlog for macro hygiene and read put's expansion*

*ran: Read B46 on macro hygiene*

*ran: Check import vs built-in shadowing and macro reach*

*ran: Read B45 and what the docs say about macro scope*

*ran: Read the import-macros rule and expand-program*

*ran: Write the namespace, sees and shadowing rules and B11's rows*

*ran: Run the programs and macros spec examples*

The examples pass. Next is B11's repro, which `test_spec` runs as a strict expected failure, so it would now fail as an XPASS. Moving it into a note and closing the backlog items:

*ran: Close B11, keep B40, and note B50, B46 and B192*

*ran: Fix the Notes spacing, regenerate the index, run all tests*

All 689 pass. There are 3 xfailed now, because B11's repro is gone. Linters and the comparison against `boot/74`'s `bin`:

*ran: Lint and compare against boot/74's bin*

The Python output is identical on all 97 programs, so this step adds a check and rules without changing what anything translates to. Now the HLD's step 5 note, with the correction about macros:

*ran: Write step 5's Done note and flag the macros correction*

Step 5, B192 (namespaces step 5: the rules written down), is built and in `review`. Nothing is committed.

**The rules**, written into `spec/10-programs.md` under `programs.top-level`, each with a running example:
- **`programs.namespace`:** a module's types, values and variants share one namespace, *lasting*. A record's name is both its type and its constructor. There are 3 error rows: a value named like a type, a variant named like another type, and a variant named like its own type.
- **`programs.sees`:** every file sees the special forms, the built-ins (the operators among them) and the prelude, with no import.
- **`programs.shadowing`:** a name means, innermost first, a local, then the file's own definition, then an unqualified import's, then a built-in or the prelude's. A qualified name is never shadowed. The translator's five host built-ins being every program's is marked *for now* (B50).

**The fix:** B11 (a `deft` variant named like a macro isn't rejected) is fixed. A `deft`'s type or variant named like a macro now says "M is a macro, so it can't be defined", as a `def` or `defn` already did (`analyse-top`, with the new `deft-names` and `macro-named`). Its repro is now 3 rows of `macros.binding`. B11 is `done`, as earlier defects fixed inside a step were (B135); say if you'd rather tick it yourself.

**Backlog:**
- B40 (types and values share one namespace) is `kept`, as a rule, not a leak.
- B50 (the translator's five host built-ins are every program's) gets a note pointing to `programs.shadowing`.

**Two things I found while writing the rules down:**
- **Macros aren't global to a program.** The HLD says a `defmacro` is seen in every module, but a file's macros are its own: its `defmacro`s, the macro files it loads with `import-macros`, and the prelude's (`cond`, `put`). `import` doesn't pass them on (`expand-file`), and the spec's `macros.import-macros` already said so. `programs.sees` states the actual rule. I flagged the HLD's "Macros' names" section as *corrected* and explained in the Done note.
- **Defining `text` breaks `put`.** `put` expands to calls of `text`, so a file's own `(defn text ...)` captures them: `(put (text 1))` fails with a type error inside the expansion. B46 (macro templates aren't hygienic across modules) already covers this kind of capture, so I added this case there as a note. The fix needs qualified built-ins, which come with `library`, so the shadowing rule says *for now*.

Also allowed, and consistent with shadowing: a file can reuse a built-in type's name, as in `(deft List ...)` or `(def Int 1)`.

**Checked:**
- `pytest`: 689 passed and 3 xfailed. All the linters are clean.
- Against `boot/74`'s `bin`: identical Python on all 97 programs. This step adds a check and rules without changing any program's output.

On "gawc" I'll commit with `boot/75`.

## Owner

> "A deft's type or variant named like a macro" what does "named like a macro" mean?

## Claude Code

It means it has the same name as a macro that file can use. "Like" is just my shorthand for "the same as". For example:

```
(defmacro M (a) a)        ; a macro named M
(deft S (M ((x Int))))    ; a variant also named M  -> now an error
```

Before this fix, the `deft` was accepted. But a later `(M 1)` would be expanded as the *macro*, because expansion runs before analysis and sees only the macro. So you could never construct the variant, and nothing told you why. That's B11 (a `deft` variant named like a macro isn't rejected).

The macros a file can use are its own `defmacro`s, the ones it loads with `import-macros`, and the prelude's (`cond`, `put`). So `(deft Shape (cond))` or `(deft put ((x Int)))` is an error too. The same rule already applied to a `def`, `defn` or local named `cond`. The fix extends it to a `deft`'s type name and its variants.

If you'd prefer clearer wording in the spec and the message notes, I can write "with a macro's name" or "with the same name as a macro" instead of "named like a macro". The error message itself, "M is a macro, so it can't be defined", doesn't use the phrase.

## Owner

> "with the same name as a macro"; do we a have table of the all `naming` conventions and rules across the entire lang?

## Claude Code

First the wording. Finding every "named like a macro" I wrote in this branch:

*ran: Find the phrase across spec, HLD, backlog and code*

*ran: Reword the phrase, keeping the old B11 title and B192 text*

*ran: Survey the spec for naming rules*

There isn't one. The naming rules are spread over six spec files, each next to the feature it constrains. Gathered here (`syntax.*` is `00-syntax.md`, `types.*` `20-types.md`, `match.*` `30-match.md`, `programs.*` `10-programs.md`, `macros.*` `50-macros.md`):

| What | Rule | Where |
|---|---|---|
| A name's characters | any word that isn't a literal and doesn't start with a digit, `'`, `#`, `"` or `\`; it ends at a delimiter, `'`, `"` or `\` | `syntax.names` |
| `.` | no defined name holds one; `m.name` is a qualified name | `syntax.names`, `programs.qualified` |
| `/` | reserved in names, except the operator `/` | `syntax.names` |
| `'` | reserved, for a future quote shorthand | `syntax.reserved` |
| Python spellings | two top-level names that are one Python name (`a-b`, `a_b`) are an error, *lasting*; the same goes for fields, and a field can't start with `_` | `syntax.names`, `types.records` |
| Types | Capitalised; a lowercase name in a type is a type variable | `20-types.md:39` |
| Type variables | different within one `deft`; not a constraint's name (`number`, `comparable`, ...) | `types.records`, `checking.constraints` |
| Variants | Capitalised | `match.sum-types` |
| Fields, pattern names | different within one record or pattern | `types.records`, `match` |
| One namespace | a module's types, values and variants share one; a record's name is its type and its constructor | `programs.namespace` |
| Defined once | a top-level name is defined once; a macro too | `programs.top-level`, `macros.binding` |
| Special forms | can't be bound, defined or made a macro | `expr.let`, `macros.binding` |
| Macros' names | can't be bound or defined (value, function, type, variant) | `macros.binding` |
| `main` | a `defn` typed `(Fn ((List String)) Int)` | `programs.main` |
| Shadowing | local, then the file's own, then an import's, then a built-in or the prelude's; a qualified name never | `programs.shadowing` |
| Visibility | `(private ...)`; an import's name list | `programs.private`, `programs.import` |

I recommend adding this as a summary in `spec/00-syntax.md`, after `syntax.names`, as a section "Naming rules, in one place". It would be an index only: each row links to its rule, and no rule moves. With no id of its own, it needs no example (the doc-link test requires one only for a rule that has an id). `test_doc_links` would still check every link in it.

It fits step 5, which is about writing the rules down, so I can add it to this commit. Or it can wait for step 7 (docs).

*(The context was summarised here; the turns before it are above.)*

## Owner

> add it in this step, and fix the qualifier wording too; and a placeholder/note for `Python spellings`... rename to `Target`

## Claude Code

*ran: `grep -n 'named like a qualifier\|named like' -r doc backlog spec src CLAUDE.md |`*

*ran: `sed -n 170,250p spec/00-syntax.md && sed -n 30,50p spec/20-types.md && sed -n 60`*

*ran: `sed -n 120,170p spec/20-types.md && grep -n 'distinct\|different names\|must dif`*

*ran: `sed -n 244,260p spec/00-syntax.md && ls doc/hl_rqmt/multi_target.md && sed -n 1,`*

*ran: `cat >> spec/00-syntax.md <<'EOF'`*

*ran: `python - <<'EOF'`*

The table is appended to `spec/00-syntax.md`. Next I'm tightening the Macros row, then doing the qualifier rewording.

*edited: `spec/00-syntax.md`*

*ran: `sed -i 's/a rule for a local named like a$/a rule for a local with the same name`*

Line 396 is now over 90 chars; rewrapping it, then B195.

*edited: `doc/hl_rqmt/namespaces.md`*

*ran: `f=backlog/B195-field-syntax-dot.md && sed -i '1s/.*/# B195: Field syntax with '.`*

*edited: `backlog/B195-field-syntax-dot.md`*

*ran: `cat >> backlog/B192-namespaces-step-5.md <<'EOF'`*

*ran: `grep -n 'Done (2026-11-14' doc/hl_rqmt/namespaces.md && grep -n -A8 'Done (2026-`*

*ran: `grep -n 'Done (' doc/hl_rqmt/namespaces.md`*

*ran: `sed -n 305,330p doc/hl_rqmt/namespaces.md`*

*edited: `doc/hl_rqmt/namespaces.md`*

*ran: `pytest -q tst/py_cdy/test_doc_links.py 2>&1 | tail -1`*

I added the naming table, renamed the Python row to `Target` and changed the qualifier wording, all in step 5. It's still uncommitted. The doc-link, backlog and `00-syntax` spec tests pass; I didn't rerun the full `pytest`, since only docs changed.

**The table:** it's at the end of `spec/00-syntax.md`, as a section "Naming rules, in one place" (about `:249`). It has 17 rows, and each links to the rule it summarises with `[[id]]`, so `test_doc_links` checks every link. It's an index only: no rule moved, and it has no id, so it needs no example.
- **Target row:** it says a target can add its own limits on names, on top of Candy's.
  - For now Python is the only target: two top-level names or two fields that are one Python name are an error (*lasting*), and a field can't start with `_` (B113, a leak).
  - A field with the same name as a tuple method fails mypy (B114, a leak).
  - It says "Another target adds its row here" and points to `doc/hl_rqmt/multi_target.md`. That sentence is the placeholder.
- **Macros row:** it reads "no local, value, function, type or variant has the same name as a macro".

**Qualifier wording:** "named like a qualifier" is now "with the same name as a qualifier" in two places:
- the HLD's Question 8 (`doc/hl_rqmt/namespaces.md:396,404`);
- B195 (field syntax with `.`): its title and first point. A note there keeps the old text in a `text` fence.

**Notes:**
- I added a line to step 5's *Done* note in the HLD (`:325`) and a note to B192 (namespaces step 5: the rules written down) saying what you asked for.
- I regenerated the backlog index with `python script/backlog.py`.

On "gawc" I'll commit step 5 and tag `boot/75`.

## Owner

> the 'target` row could just say "see target spellings"....?

## Claude Code

*ran: `grep -n '^| Target' spec/00-syntax.md`*

*edited: `spec/00-syntax.md`*

*ran: `sed -i 's/^   place"), its last row a target.s own limits (Python.s, \*for now\*`*

That line is now over 90 characters; rewrapping it.

*edited: `doc/hl_rqmt/namespaces.md`*

I shortened the `Target` row (`spec/00-syntax.md:267`) to say only that. It now reads "see the target's spellings (Python, *for now*)", and its links are `[[syntax.python-names]]` and `[[types.records]]`. The detail it used to repeat is in those two rules already. The doc-link test passes.

I also changed step 5's *Done* note in the HLD (`doc/hl_rqmt/namespaces.md:328`) to say the row points to the target's spellings.

Step 5 is still uncommitted; on "gawc" I'll commit it and tag `boot/75`.

## Owner

> Tick, gawc

## Claude Code

*ran: `git status --short && sed -n 1,12p backlog/B192-namespaces-step-5.md && git diff`*

*ran: `perl -0pi -e 's/Checked\n   against\n   'boot\/74'.s 'bin': the same Python for `*

*ran: `M=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

B192 (namespaces step 5: the rules written down) is ticked, and step 5 is committed as `28f7245` on `namespaces`, tagged `boot/75`. The tag is annotated, with no staging.

Before the commit, the full `pytest` gave 689 passed and 3 xfailed, and `ruff check` and `ruff format --check` were clean. Since step 5's earlier full check, only docs changed, so I didn't rerun mypy, pyright or pylint. Every change in the commit is mine; I saw none of yours in `git status`.

Nothing is pushed: master, the branch `namespaces` and the tags `collections-2` and `boot/71` to `boot/75` are still only local.

B190 (namespaces step 3: the name list and `import`'s shape) and B191 (namespaces step 4: private names) still need your tick. Next is step 6, B193 (namespaces step 6: the module in Core).

## Owner

> Tick both and start 6

## Claude Code

*ran: `for f in backlog/B190-*.md backlog/B191-*.md && do sed -i 's/^state: review$/sta`*

*ran: `sed -n 75,95p doc/hl_rqmt/namespaces.md && sed -n 180,230p doc/hl_rqmt/namespace`*

*ran: `grep -n 'Global' *.cdy | wc -l && grep -n 'Global' *.cdy | head -80 && grep -n '`*

*ran: `sed -n 1,75p core.cdy && sed -n 170,200p core.cdy && grep -n 'defn global-name\|`*

*ran: `sed -n 30,80p cdyc.cdy && sed -n 150,200p emit.cdy && sed -n 1315,1330p check.cd`*

Step 6 is bigger than its title suggests, so I'm surveying where Core holds a module-prefixed string before choosing the shape.

*ran: `for p in '(Global ' '(TCon ' '(Clause ' '(TDef ' '(TDefn ' '(TDeft ' '(TDeftSum `*

*ran: `grep -n 'prefix\|global' core.cdy | grep -v '^\s* && ' | head -80`*

*ran: `sed -n 1160,1300p core.cdy && sed -n 1380,1440p core.cdy`*

*ran: `grep -n 'TCon\|(Global\|(Clause\|TDef\|TDeft\|entry-global\|global-name\|(Value `*

*ran: `grep -n 'TCon\|(Global\|(Clause\|TDef\|shown-name\|own-name\|variant)' check.cdy`*

*ran: `sed -n 160,300p core.cdy`*

*ran: `python - <<'EOF'`*

*ran: `grep -n '^(import' *.cdy && grep -n 'entry-global\|entry-module\|global-name' *.`*

Now the `Entry` and its name helpers.

*ran: `python - <<'EOF'`*

*ran: `python - <<'EOF'`*

*ran: `sed -n 1530,1560p core.cdy && sed -n 1712,1770p core.cdy`*

*ran: `grep -n 'has-main\|is-main' *.cdy | grep -v 'defn\|sig'`*

*ran: `sed -n 80,134p cdyc.cdy && sed -n 820,832p emit.cdy`*

*ran: `python - <<'EOF'`*

`core.cdy` is done. Now `cdyc.cdy` (the prefix and `python-of`'s top module), then `check.cdy`.

*ran: `sed -n 1,30p cdyc.cdy && grep -n 'python-of\|translate-expanded\|analyse-program`*

*ran: `grep -n 'deft Env' -A14 emit.cdy && grep -n 'globals\|TDef\|TCon\|own-name\|cand`*

*ran: `sed -n 1,60p lower.cdy && sed -n 385,470p lower.cdy`*

*ran: `grep -n '(Env \|own-name\|candy-name' *.cdy && grep -rn 'own-name\|candy-name\|g`*

*ran: `sed -n 200,245p emit.cdy && sed -n 300,315p emit.cdy && sed -n 370,445p emit.cdy`*

*ran: `sed -n 20,240p check.cdy`*

*ran: `sed -n 262,380p check.cdy`*

*ran: `grep -n '(TCon "' check.cdy lower.cdy emit.cdy expand.cdy cdyc.cdy && sed -i 's/`*

Now the definitions' tables in `check.cdy` (lines 98–180).

*ran: `python - <<'EOF'`*

*ran: `python - <<'EOF'`*

*ran: `sed -i 's/(map-has (get ctx shapes) (global-of callee))/(map-has (get ctx shapes`*

*ran: `python - <<'EOF'`*

*ran: `python - <<'EOF'`*

*ran: `python - <<'EOF'`*

The checker's definitions, unification, narrowing and messages are converted. Now I'm sweeping its remaining `TCon` sites, then moving on to `lower` and `emit`.

*ran: `grep -n 'TCon' check.cdy | grep -v '(TCon "" \|(TCon m \|(TCon _ _ \|(TCon bm \|`*

*ran: `grep -n 'ctx shapes\|ctx sums\|ctx globals' check.cdy`*

*ran: `grep -n 'get c variant\|global-of\|shown-name' check.cdy && grep -n 'TCon\|Globa`*

*ran: `python - <<'EOF'`*

*ran: `sed -i 's/    ((SDefAssign _ val _) (has-lambda val))/    ((SDefAssign _ _ val _`*

*ran: `sed -n 515,600p emit.cdy && sed -n 700,822p emit.cdy`*

Next is `emit`. Its `Env` gets the top module's stem, and one helper, `spelled`, rebuilds today's `util__greet` from the module and the name, so the Python stays byte for byte the same.

*ran: `sed -n 10,24p emit.cdy && sed -n 280,300p emit.cdy && grep -n 'field-show-type\|`*

*ran: `python - <<'EOF'`*

*ran: `sed -i '156{N && N && s/ && --- names ---\n\n && --- names ---/ && --- names ---`*

*ran: `grep -n 'defn spelling-kind' -A4 emit.cdy && grep -n 'global-names\|python-of\|E`*

*ran: `grep -rn 'spelling-kind' *.cdy | head -3 && grep -n 'defn spelling-kind' -A5 *.c`*

Now `cdyc.cdy`: drop the prefix, and give `python-of` the top module.

*ran: `python - <<'EOF'`*

*ran: `python - <<'EOF'`*

All files are edited. Building T1 with `bin` to see what breaks.

*ran: `mkdir -p tmp/c7/s6 && python bin/py/cdy_translator.py src/cdy/cdyc.cdy tmp/c7/s6`*

*ran: `grep -n 'def \|argv\|argparse' src/py_cdy/self_host.py | head -30`*

*ran: `time python src/py_cdy/self_host.py 2>&1 | tail -15`*

T2 reproduces itself and passes `mypy --strict`, and `bin` is rebuilt. Next I'm comparing every program's Python against `boot/75`'s `bin`.

*ran: `sed -n 1,40p tmp/c7/cmp3.py && ls tmp/c7`*

*ran: `rm -rf tmp/c7/b72/bin tmp/c7/sp3/* && git archive boot/75 bin | tar -x -C tmp/c7`*

All 97 programs (the translator, every test program and every spec example) give the same Python as under `boot/75`. Running the full test suite now.

*ran: `pytest -q -x 2>&1 | tail -30`*

*ran: `grep -rnoE '\b(t1|t2|translator|t|bin_t|mod)\.[a-z][A-Za-z_0-9]*' tst src/py_cdy`*

*ran: `grep -n 'core__\|form__\|"[a-z]*__[A-Za-z]' tst/py_cdy/*.py src/py_cdy/*.py scri`*

*ran: `grep -rn 'to_form\|kind ==\|type(.*).__name__' tst/py_cdy/test_self_host.py src/`*

*ran: `grep -n 't1\.[a-z_]*__\|t1\.translate_expanded\|t1\.program_tops\|core__\|^def \`*

Adding `py-global-name` to `emit.cdy` first.

*ran: `python - <<'EOF'`*

*ran: `grep -n 'def PY_RESERVED\|def PY_IMPORTS\|def NOWHERE\|deft Pos\|defn read-forms`*

*ran: `python - <<'EOF'`*

*ran: `sed -n 478,520p tst/py_cdy/test_self_host.py`*

*ran: `python - <<'EOF'`*

*ran: `cat > shadow.cdy <<'EOF'`*

*ran: `ls backlog | sed 's/-.*//' | sort -V | tail -3 && cat > tmp/c7/s6/rec.cdy <<'EOF`*

*ran: `grep -l '^kind: defect' backlog/*.md | xargs grep -l 'candy run' | head -2 | xar`*

*ran: `cat > backlog/B196-type-shadowing-builtin-show.md <<'EOF'`*

*ran: `pytest -q tst/py_cdy/test_backlog.py tst/py_cdy/test_doc_links.py 2>&1 | tail -1`*

*ran: `sed -n 15,20p src/cdy/check.cdy && sed -n 72,73p src/cdy/check.cdy`*

*ran: `sed -i '72s/.*/ && 'tops', a whole program (every module'"'"'s, each name with i`*

Tidying comments, then the full checks and the step's paperwork (HLD note, B193, B65).

*ran: `python - <<'EOF'`*

*ran: `python src/py_cdy/self_host.py 2>&1 | tail -1 && rm -f tmp/c7/sp3/* && python tm`*

*ran: `head -2 tmp/c7/sp3/e1.cdy && python ../b72/bin/py/cdy_translator.py ../sp3/e1.cd`*

*ran: `pytest -q 2>&1 | tail -2 && ruff check src tst script && ruff format --check src`*

Everything passes: 689 tests passed plus 4 xfailed (the fourth is B196's repro), and the five linters are clean. Now the HLD note and the backlog.

*ran: `grep -n '^6\. \*\*The module in Core' -A4 doc/hl_rqmt/namespaces.md && cat backl`*

*ran: `python - <<'EOF'`*

*ran: `head -8 backlog/B193-*.md | tail -5 && tail -4 backlog/B193-*.md && git diff --s`*

*ran: `tail -3 backlog/B190-*.md backlog/B191-*.md`*

*ran: `for f in backlog/B190-*.md backlog/B191-*.md && do echo "== $f" && tail -n 3 "$f`*

I ticked B190 (namespaces step 3: the name list and `import`'s shape) and B191 (namespaces step 4: private names), and built step 6, B193 (namespaces step 6: the module in Core). It's in review and uncommitted.

All the checks pass: the full `pytest` (689 passed, 4 xfailed), `ruff check`, `ruff format --check`, `mypy`, `pyright` and `pylint`. `bin` is rebuilt, and T2 reproduces itself and passes `mypy --strict`.

**Against `boot/75`'s `bin`:** 97 of 98 programs give the same Python: the translator, every test program and every spec example. The one that differs is the new B196 example (below). The build (0.9 s) and T2's `mypy --strict` (1.7 s) take the same time as before.

**What changed:**
- **Core:** `Global`, `TCon`, `Clause` and the four definitions now carry the module that defines them and the name there (`src/cdy/core.cdy:13-64`). The module is `""` for a built-in type and for macro code. The lowered IR's definitions and `Case`s carry it too (`src/cdy/lower.cdy:11-32`).
- **The table:** an `Entry`'s `global` field is now `name`, and `module-exports` no longer takes a prefix. A Core name is resolved by `global-ref`, and `global-key` turns it into one string, `util.Shape` (`core.cdy:313-332`). This is safe because no name can hold a `.`.
- **Checker:** its tables are keyed by `global-key`, and comparing two types now compares their modules too. Error messages show the name itself.
- **Python:**
  - `emit` turns the module and the name back into `util__greet` (`spelled` and `py-global-name`, `src/cdy/emit.cdy:158-174`). The top module's names and macro code's have no prefix, as before.
  - The top module keeps its stem as its module, so `python-of` and `has-main` now take that stem. Only the top module's `main` runs.
- **The tests (B65, done):** they reach a translator name as Candy writes it, e.g. `candy(t1, "form.Pos")` (`tst/py_cdy/test_self_host.py:57`). The `"core__TVar"` class-name checks are now `isinstance` checks. The one name still reached by its Python spelling is `py-global-name` itself.
- **Bootstrap:** step 6 changes no syntax, so `boot/76` needs no staging.

**A finding, filed as B196 (a type with the same name as a built-in type can't be shown):** a top-module `(deft Map ...)` used to produce Python that didn't parse. Now it translates and passes mypy, but `put` still fails at run time: `show` reads the type by its name, `'Map'`, and takes it for the built-in map. I filed it as a low-priority defect, with its repro as a strict xfail.

**Paperwork:**
- The HLD has a *Done* note for step 6 (`doc/hl_rqmt/namespaces.md:333`).
- B193 is in review with `fixed: namespaces, 2026-11-14`.
- I regenerated the backlog index with `python script/backlog.py`.

`CLAUDE.md` still says the tests reach the translator as `t1.form__Sym`. I've left that for step 7 (docs).

On "gawc" I'll commit step 6 and tag `boot/76`.

## Owner

> "The module is "" for a built-in type and for macro code"... Can you expand?

## Claude Code

`""` means "no module": the name doesn't come from any file in the program. Two kinds of name are like that.

**1. Built-in types.** `Int`, `String`, `List`, `Map`, `Tup`, `Any`, `Unit` and the rest aren't defined by a module. `system.cdy` declares them as bodiless `deft`s, and the translator reads them into its built-ins map, not into a module's table. So when analysis meets `Int` in a `sig`, `global-ref` (`src/cdy/core.cdy:322`) doesn't find it in the module's names and leaves it as `(TCon "" "Int" ...)`. A type a program defines gets its module instead:
- the top module's `(deft Shape ...)` is `(TCon "main" "Shape" ...)` (its stem);
- `util.cdy`'s is `(TCon "util" "Shape" ...)`;
- the prelude's `Maybe` is `(TCon "prelude" "Maybe" ...)`, because the prelude is a real module, imported implicitly. Only `system.cdy`'s types have `""`.

This is what lets the checker tell the built-in `Map` from a program's own `Map`. Before this step both were just `"Map"`, which is why B196's example used to produce broken Python. The built-in operators and functions (`+`, `map`, `len`) aren't `Global`s at all; they're `Prim`s, so they don't need a module.

**2. Macro code.** A `defmacro`'s body, and the macro files `import-macros` loads, aren't analysed as modules. They're combined into one standalone program (still by inclusion), which `analyse-program` analyses with `(module-exports forms "")` (`core.cdy:1282`), so every name defined there gets module `""`. The quoting code makes `(Global "" "Sym" ...)` for the same reason: in macro code `form.cdy`'s `Sym` is included, not imported.

**What `""` does downstream:**
- `global-key` gives no `.`: a built-in's key is `Int`, while a module's is `util.Shape`.
- `emit`'s `spelled` writes no prefix: `Int` goes through `spelling.py`, and macro code's `Sym` stays `Sym`. That matches what the old empty prefix gave, so the Python is unchanged.

**The catch:** one value means two things. Built-in types and macro code share `""`, so a macro program's own type `Map` would have the same key as the built-in `Map`. That doesn't cause trouble today, because macro code isn't type-checked (B42) and its Python was already unprefixed. But it's a shortcut, not a design.

**The alternative:** give each a real module. The built-ins would be `"system"`, which fits where the HLD is heading: they have no qualifier "until `library`" splits them into modules (so `system.map` is possible later). Macro code would get a name of its own. The cost is that `emit` would need to know that `system`'s names are spelled through `spelling.py`, and that macro code has no prefix. Every place that checks for a built-in (`is-any`, `is-rest`, `returns-unit`, the constraint checks) would compare against `"system"` instead of `""`.

I recommend keeping `""` for this step. I'd write it down as *for now*: in a comment on `TCon` and in the step 6 *Done* note, with a backlog idea, "built-ins as module `system`", to do with `library`. Or I can make the change now.

## Owner

> Should we make it now?

## Claude Code

No, I'd wait.

1. **The module `system` would be a name with nothing behind it.** No program can write `system.Int` or `(import system)`, and qualified names don't reach the built-ins (`programs.qualified`). The checker and `emit` would carry `"system"` around, but the language wouldn't have it.
2. **`library` is where this gets decided.** That branch splits the built-ins into modules, maybe several (`list`, `string`, `map`) rather than one `system`. Choosing `system` now is a guess that branch would likely redo, along with every check for a built-in (`is-any`, `is-rest`, `returns-unit`, the constraint checks).
3. **Step 6 is a clean refactor now.** The Python is unchanged for every program but one known case. Adding this widens the step's scope for no visible gain.
4. **Sharing `""` with macro code is harmless for now.** It could only cause a clash where something reads the two by key together, and nothing does: macro code isn't type-checked (B42), and its Python was already unprefixed. It becomes a real problem only if macro code is checked (B42) or macros run on the host (B45). Those items are the right place to give macro code its own module.

What I'd do now is write it down as *for now*, in three places:
- a comment on `TCon` and `Global` in `src/cdy/core.cdy`: `""` is "no module", the built-ins' and macro code's, *for now*, and links B42 and the new item;
- a sentence in step 6's *Done* note in the HLD;
- a backlog idea: "The built-ins' module, and macro code's", to settle with `library`, with B42 and B45 as refs.

Shall I add those to step 6 before the commit?

## Owner

> Yes, tick

## Claude Code

*ran: `python - <<'EOF'`*

I added the *for now* notes, filed B197, and ticked B193 (namespaces step 6: the module in Core), so it's done. Nothing is committed yet.

- **Comments:** on `TCon` and `Global` (`src/cdy/core.cdy:12` and `:25`). They say `""` means "no module", for a built-in type and for macro code, *for now* ([[B197]]). The one on `Global` also says macro code isn't checked ([[B42]]).
- **HLD:** step 6's *Done* note (`doc/hl_rqmt/namespaces.md:336`) now says the same: *for now*, B197, to settle with `library`.
- **B197 (the built-ins' module, and macro code's):** a new low-priority idea. It says what `""` stands for, why it's harmless while macro code isn't checked, and what settling it needs: the built-ins' modules, which `library` decides, and macro code's own module, with B42 (macro code isn't type-checked) or B45 (macros run on the host). It records your decision.
- **B193:** a note on the decision, then your tick.

I regenerated the backlog index. The comments don't change `bin`: rebuilding it gave the same file, and the doc-link, backlog and fixpoint tests pass. Since the last full run only comments and docs changed, so I didn't rerun the whole suite.

On "gawc" I'll commit step 6 and tag `boot/76`. Next is step 7, B194 (namespaces step 7: docs), which includes the `CLAUDE.md` text about `t1.form__Sym`.

*(The context was summarised here; the turns before it are above.)*

## Owner

> Gawc

## Claude Code

*ran: Show working tree status*

No files beyond mine. Running the full checks first.

*ran: Run the full test suite*

*ran: Run the five linters and type checkers*

*ran: Run the full test suite*

*ran: Show last commit message format and scan for tokens*

*ran: Stage step 6 and commit it*

*ran: Tag the bootstrap step and verify the tag*

I committed B193 (namespaces step 6: the module in Core) as `2bcb771` and tagged it `boot/76`. The tag is annotated and points at that commit, with no staging step.

- **Before the commit:** the full `pytest` gave 689 passed, 4 xfailed. `ruff check`, `ruff format --check`, `mypy`, `pyright` and `pylint` were all clean.
- **Files:** the commit has the 15 files I'd changed. None of them had edits of yours.
- **Tokens:** I searched the changed files for `github_pat_` and `ghp_` and found nothing.

Nothing is pushed. Still unpushed: master (`05d1632`, `763ba9a`, tag `collections-2`), branch `namespaces`, and tags `boot/71` to `boot/76`.

Next is step 7, B194 (namespaces step 7: docs). First up is `CLAUDE.md`: it still says the tests reach the translator's internals as `t1.form__Sym` (now `candy(t1, "form.Sym")`) and describes the `__` prefix as Core's (now only `emit` spells it). It should also mention `syntax.cdy` and `global-key`.

## Owner

> Go

## Claude Code

*ran: Read B194 and the HLD's headings*

*ran: Read the HLD's intro, steps and questions*

*ran: Find Looking back sections and the epic's branch list*

*ran: Read the epic's status, namespaces section, branches and triage*

*ran: Check item states and read a Looking back example*

Working on step 7, B194 (namespaces step 7: docs): I've read the HLD and the epic, and now I'm checking the other docs it names.

*ran: Locate the sections and read the items' latest notes*

*ran: Read B47, B108 and the two doc sections*

*ran: Find imports and stale wording in the top docs*

Now the edits. `CLAUDE.md` first: the code list, the history and the Modules bullet.

*ran: Update CLAUDE.md's code list, history and Modules bullet*

*ran: Show the exact collections-2 sentence*

*ran: Show the exact collections-2 sentence*

*ran: Update CLAUDE.md's code list, history, built-ins and Modules bullet*

Now the epic: the fourth branch's *Done* note and its triage rows.

*ran: Add the epic's done note and triage updates*

Next, `modules.md`'s "After the MVP" and `multi_target.md`'s "Modules and output units".

*ran: Add since notes to modules.md and multi_target.md*

Now the HLD: status, step 7's note and "Looking back". First, how `collections_2.md` words its status:

*ran: Read collections_2's status and step 7 note*

*ran: Mark the HLD done and add step 7's note and Looking back*

*ran: Update B47, B108, B194 and regenerate the backlog index*

*ran: Tidy B47's note, check line lengths, run doc tests*

*ran: Show the HLD's status paragraph*

*edited: `doc/hl_rqmt/namespaces.md`*

Docs are written; running the full test suite before reporting.

*ran: Run the full test suite*

I've written step 7, B194 (namespaces step 7: docs). B194 is in `review`, nothing is committed, and the full `pytest` gives 689 passed, 4 xfailed. Only docs and the backlog changed, so `bin` stays as it is.

**`CLAUDE.md`:**
- **Code list:** `syntax.cdy` added (`CLAUDE.md:10`).
- **History:** a sentence for `namespaces` as the epic's fourth branch, citing tag `namespaces` (`:26`). That tag doesn't exist yet; it comes with the merge.
- **The built-ins:** `import`'s declared shape (`:32`).
- **Modules:** rewritten (`:30`). It covers `(import m (a b))`, `m.name`, `(private ...)`, the one table of `Entry`s and the shadowing order. It also covers the module in Core, the `""` meaning *for now* ([[B197]]), `global-key`, the fact that only `emit` spells `util__greet`, and the tests' `candy(t1, "form.Sym")`. The `t1.form__Sym` text is gone.

**The other docs:**
- **`python_complete.md`:** the fourth branch has its *Done* note, and the triage rows for B40, B47, B108, B65 and B11 say how each ended.
- **`modules.md`, "After the MVP":** *done* notes on the import forms, "ambiguous only where used" and the module reaching the backend. They also say what's still open and whose it is (B187, B45, B46).
- **`multi_target.md`, "Modules and output units":** a *Done in part* note. References carry their module; Python is still one file.
- **The HLD:** its status is done, with step 7's *Done* note. "Looking back" is new, with six points:
  - building the table first made each rule small;
  - changing the separator was cheap because no name used one yet;
  - a declared shape needs staging;
  - writing the rules down corrected the HLD's "Macros' names";
  - keying by the Python spelling hid which `Map` was meant (B196);
  - the last `bin` served as the oracle for every step.

**Backlog:**
- **B47 (only `(import m)`, everything unqualified):** it was still `open` although steps 2 to 4 fixed it. I set it to `review` with `fixed: namespaces, 2026-11-14`, plus a note on how the fix differs from "After the MVP": one form, no alias.
- **B108 (the built-ins are one flat namespace):** stays open for `library`, with a note.

To tick B194, and B47 with it, say "tick". After that, merging needs `pytest -m bootstrap`.

## Owner

> Spec updates review?

## Claude Code

*ran: Search the spec for namespace-related wording*

*ran: Read match.namespace, the programs file's head and the spec index*

*ran: Read the programs grammar block and the index rows*

I found four stale places; fixing them:

*ran: Fix the stale spec wording and index rows*

*ran: Record the spec review and run the spec and doc tests*

No, I hadn't checked the spec: step 7 only said "the spec's rules came with their steps". I've now read it through and fixed four places that were out of date. The spec, doc-link and backlog tests pass (466 passed, 4 xfailed), and nothing is committed.

- **`spec/30-match.md:69`:** [[match.namespace]] still said types and values share one namespace *for now*. It now says *lasting* and links [[programs.namespace]], matching step 5.
- **`spec/10-programs.md:5`:** the introduction said the file covers `import` only. It now adds qualified and private names, and lists the new example programs (`qualified`, `import_list`, `private`). The syntax block gains `(import name (name*))` and `(private name+)`.
- **`spec/10-programs.md:21`:** [[programs.top-level]] now says `private` is allowed only at top level, with the definitions and imports.
- **`spec/README.md:18-19`:** the `00-syntax.md` row mentions the naming rules' index, and the `10-programs.md` row lists the new rules: one namespace, what every file sees, shadowing, qualified and private names.

Everything else that mentions names was already current: the rules each step added, the `import` errors, the naming index in `spec/00-syntax.md` and the `util--greet` rule (`spec/00-syntax.md:215`).

I added the spec fixes to step 7's *Done* note in the HLD, and a note on B194 (namespaces step 7: docs) recording your question and the four fixes.

To tick B194 and B47 (only `(import m)`, everything unqualified), say "tick"; "gawc" commits step 7.

## Owner

> New issues added?

## Claude Code

*ran: List backlog items found in the namespaces branch*

Step 7 added no new items. Reading the docs and the spec through turned up only stale wording, which I fixed in place, and nothing that needs tracking.

Over the whole branch, besides the step tasks B188 to B194, four items were filed. All are still open:

| Item | Kind | Found | What |
|---|---|---|---|
| B187 (`alias`, a renaming at translation time, for modules, types and values) | idea | the HLD, 2026-11-12 | why `import` has no alias |
| B195 (Field syntax with `.`, and a local with the same name as a qualifier) | idea | step 2's review, 2026-11-13 | needed once `.` became the separator |
| B196 (A type with the same name as a built-in type can't be shown) | defect | step 6, 2026-11-14 | `show` takes a program's `Map` for the built-in; its repro is a strict xfail |
| B197 (The built-ins' module, and macro code's) | idea | step 6's review, 2026-11-14 | `""` means two things, *for now*, to settle with `library` |

The branch also closed or settled older items:
- **B11 (a variant named like a macro):** done.
- **B65 (tests reach internals by Python names):** done.
- **B40 (types and values share a namespace):** kept, as a rule.
- **B47 (only `(import m)`, everything unqualified):** in review, from step 7.

B50 and B108 have notes and stay open, both for `library`. B46 got a note in step 5: a file's own `text` changes `put`.

One slip: step 6's commit message (`2bcb771`) describes B196 as "a type with the same name as a built-in shows wrong", not by its title. Fixing it would mean rewriting history, so I've left it.

## Owner

> Tick, gawc

## Claude Code

*ran: Tick B194 and B47*

*ran: Regenerate the index, check status and tokens, run all checks*

*ran: Commit step 7*

I ticked B194 (namespaces step 7: docs) and B47 (only `(import m)`, everything unqualified), and committed step 7 as `7b38739`. Nothing is pushed.

- **Before the commit:** the full `pytest` gave 689 passed, 4 xfailed. `ruff check`, `ruff format --check`, `mypy`, `pyright` and `pylint` were all clean.
- **Files:** the commit has the 12 files I'd changed. None of them had edits of yours.
- **Tokens:** I searched the changed files for `github_pat_` and `ghp_` and found nothing.
- **No boot tag:** `bin` didn't change, so `boot/76` is still the latest.

All seven steps of the `namespaces` branch are now committed. Next is the merge into master:
1. Run `pytest -m bootstrap`.
2. Merge with `git merge --no-ff refs/heads/namespaces -F <file>`.
3. Tag `namespaces` (annotated).

Say "go" to start with the bootstrap run.

Still unpushed: master (`05d1632`, `763ba9a`, tag `collections-2`), branch `namespaces`, and tags `boot/71` to `boot/76`.

## Owner

> Go

## Claude Code

*ran: Run the bootstrap chain tests*

While the chain runs, I'll look at how the last merge and its tag were written.

*ran: Read the last merge message and feature tag*

I've read the previous merge message and tag, so I can draft this merge's message the same way. I'll merge once `pytest -m bootstrap` passes.

*ran: Draft the merge commit message*

The merge message is drafted. The bootstrap chain is still running; I'll merge when it finishes.

## Claude Code

*ran: Read the bootstrap test result*

`pytest -m bootstrap` passed: 1 passed, in 4 minutes.

The merge into master is a commit, and I commit only on "gawc", so I've stopped here. The message is drafted in `/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/scratchpad/msg-merge.txt`. Its subject is "Merge namespaces: one table of names, qualified names, import's name list, private names, the module in Core", and its body lists the seven steps and their items.

On "gawc" I'll:
1. check out master and merge with `git merge --no-ff refs/heads/namespaces -F <that file>`;
2. tag the merge `namespaces` (annotated, with the subject as its message);
3. check that `git cat-file -t refs/tags/namespaces` gives `tag`.

There's no `boot/NN` tag: the merge doesn't change `bin` beyond `boot/76`. Nothing gets pushed until you ask.

## Owner

> Gawc, push

## Claude Code

*ran: Merge namespaces into master and tag it*
