*Archived 2026-10-31, from the Claude Code session that built branch `type-checker`
(2026-10-29 to 2026-10-30; HLD `doc/hl_rqmt/type_checker.md`, tag `type-checker`), by
`script/chat_archive.py`.* The owner's messages and Claude's replies on the branch,
verbatim; each tool call is a one-line marker, and thinking and tool output are left out.
Archived after the fact, with `typed-core`'s, at the start of the epic
(`doc/hl_rqmt/python_complete.md`). What came of it: Candy's own type checker
(`src/cdy/check.cdy`, `spec/25-checking.md`), [[B15]] narrowed, and [[B119]] to [[B122]]
found. A side conversation from step 3 is archived on its own,
`doc/archive/chat_get_on_sums.md`.

# type-checker

## Claude Code

*ran: `python3 - <<'EOF'`*

The HLD is accepted, and the start of branch `type-checker` (made off master) is ready to commit.

**The `process.md` note:**
- **Lifecycle step 1:** a language HLD also says which rules of the stable files change. You go over those spec changes, along with the questions, before accepting it.
- **"Design docs" → Layout:** an HLD that changes the language has "The spec" in its Proposal. That section holds its draft spec file's rules (each id, in a table) and the stable rules it changes.
- **The Log:** a 2026-10-28 entry for this.

**The start of the branch:**
- **The HLD** is marked accepted (2026-10-28), with its answers and its spec changes.
- **One task per step,** all `open`:
  - B115 is step 1, the survey;
  - B116 is step 2, positions in Core (refs B14);
  - B117 is step 3, the checker on (refs B25, B10, B30, B17);
  - B118 is step 4, docs.
- **B15** is `in-progress`.
- **Also included:**
  - the draft `spec/25-checking.md` and its row in `spec/README.md`;
  - the B19 note;
  - the B36 note and refs;
  - the "Open: showing values" section in `multi_target.md`;
  - the host note in `macros.md`.

The full test run gives 435 passed, 35 xfailed and 12 xpassed. Everything is staged. On "gawc" I'll commit it as "Start branch type-checker: Candy's own type checker (B15)". None of the changes are your own edits; they're all mine from this conversation.

## Owner

> gawc

## Claude Code

*ran: `git status --short | grep -v "^[MA] " && M=/tmp/claude-1000/-home-skerrj-dev-exp`*

The start of branch `type-checker` is committed as `5a4ff9b`. There were none of your own edits. Nothing is pushed.

Step 1, the survey, is next. It's a first `check.cdy`, written to report what it would reject rather than fail. I'll run it over the translator, the test programs and the spec, and sort what it finds into three groups:
- the checker's own bugs;
- rules that need to change, such as mixing number types, or how often the "isn't known here" error fires;
- real type errors, which get fixed or recorded as items.

It's the step where most of the checker gets written, so it will take a while. Say "go ahead with step 1" when you want it started.

## Owner

> push, then go ahead with step 1

## Claude Code

*ran: `git push origin refs/heads/type-checker:refs/heads/type-checker 2>&1 | tail -2`*

Pushed: `type-checker` is on origin. Starting step 1. First I'll read Core and the driver closely, since the checker walks Core.

*read: `src/cdy/core.cdy`*

*read: `src/cdy/core.cdy`*

*read: `src/cdy/core.cdy`*

*read: `src/cdy/core.cdy`*

*read: `src/cdy/cdyc.cdy`*

*ran: `cat src/cdy/prelude.cdy && grep -n "defn library-builtins" -A12 src/cdy/expand.c`*

Writing `check.cdy` now: unification over Core's `CType`, collecting messages instead of failing.

*wrote: `src/cdy/check.cdy`*

*ran: `grep -n -A2 "^(sig [A-Z_]* (List String))" src/cdy/*.cdy | head && grep -n "TYPE`*

A few fixes before building. Candy's patterns are flat, so there's no nested `(Lit (IntLit _))` and no literal `(TCon "Any" _)`. And my `join` would shadow the string built-in `join`.

*ran: `python3 - <<'EOF'`*

*ran: `python3 - <<'EOF'`*

*ran: `python -c "`*

*ran: `sed -i 's/^(import core)$/(import form)\n(import core)/' src/cdy/check.cdy && he`*

`check.cdy`'s names clash with other modules', because `cdyc` sees every module's names unqualified (B108's flat namespace). Listing every clash at once:

*ran: `python3 - <<'EOF'`*

*ran: `sed -i 's/(field-types /(fields-types /g && s/(sig field-types /(sig fields-type`*

*ran: `sed -i 's/^(defn field-types (fields)/(defn fields-types (fields)/' src/cdy/chec`*

T1 builds with the checker in it. Next, a scratch survey script: it runs `type_survey` over the translator, every test program and every spec `candy run` example.

*ran: `grep -n "^def examples\|^class Example\|^def load\|^FILES\|^ITEMS\|^TEXTS" -A6 t`*

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

*ran: `grep -n "survey\|def check__check_program" output/t1/cdy_translator.py | head &&`*

`build_t1` wrote to a relative `output/`, and I ran it from `src/py_cdy`. So T1 landed in `src/py_cdy/output/`. I'll remove that stray copy and rebuild from the repo root.

*ran: `ls src/py_cdy/output/ && rm -r src/py_cdy/output && git status --short && python`*

*ran: `sed -n 50,170p /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b2`*

*ran: `python3 - <<'EOF'`*

Just 7 messages across the translator, the test programs and the spec. That's few enough to suspect the checker is too lenient, so I'll test it against the draft spec's own error rows too.

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

*ran: `grep -n "defn emit-lit" -A14 src/cdy/emit.cdy | grep -n "py-str\|CharLit" && gre`*

*ran: `python3 - <<'EOF'`*

*ran: `sed -n 690,760p src/cdy/check.cdy`*

*ran: `python3 - <<'EOF'`*

A bug in the new `Do` case: it passes a `Res` where a `St` is expected. The checker will catch mistakes like this in its own code once step 3 turns it on.

*ran: `python3 - <<'EOF'`*

*ran: `python3 - <<'EOF'`*

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

The checker catches each bad case, with one gap: `(tup 1 "a")` passes as a `(List Int)`, because a mixed tuple becomes `(List Any)`. I'll check each item against the list's type instead.

*ran: `python3 - <<'EOF'`*

*ran: `grep -n "checking.operators" -A22 spec/25-checking.md | head -30 && grep -n "als`*

*ran: `python3 - <<'EOF'`*

*ran: `grep -n -i "(+ \|joins\|concaten" spec/60-library.md | head`*

*ran: `grep -n "^1\. \*\*A survey" -A5 doc/hl_rqmt/type_checker.md && grep -n "def test`*

*ran: `sed -n 1,66p tst/py_cdy/test_self_host.py | grep -n "^ROOT\|^CDY\|^PROGRAMS\|^SR`*

*ran: `sed -n 36,66p tst/py_cdy/test_self_host.py`*

*ran: `grep -n "^TRANSLATOR\|^CDY_DIR" src/py_cdy/self_host.py && python3 - <<'EOF'`*

Now the step's *Done* note, and the variant question for you:

*ran: `python3 - <<'EOF'`*

*ran: `grep -c "Tried and dropped" doc/hl_rqmt/type_checker.md && python3 - <<'EOF'`*

Step 1, the survey, is done and ready to commit. The checker exists and has been run over the translator, every test program and every spec example. It isn't on yet: nothing it finds stops a translation.

**What's built:**
- **`src/cdy/check.cdy`** (791 lines): unification over Core's types. It checks against the expected type where there is one (an `if`'s branches, a `let`'s body, a `fn` passed to a function) and infers otherwise. For now it returns its messages instead of failing, each naming the definition (`defn f: ...`), since there are no positions until step 2.
- **`type-survey`** in `cdyc.cdy` runs it over a file. I split `program-tops` out of `translate-modules` for this; translation itself doesn't call the checker yet.
- **Two tests:** `test_the_translator_type_checks`, and `test_programs_type_check`, which keeps the two known messages listed below.

**What it found:**
1. **One real error in the translator,** which mypy can't see: `emit-lit` passed a `Char` to `py-str`, a `String` function. It's fixed.
2. **Two rules had to change, and are now in the draft spec:**
   - `+` joins lists too. The translator does it everywhere, and the stable spec says only strings, so step 3 adds it to `[[expr.arithmetic]]`.
   - A `(Tup t ...)` whose items have one type is accepted as a `(List t)`, *for now* (B29), because there's no list literal. A new rule, `checking.tup-lists`, says so.
3. **Two answers held up:** checking `fn` arguments last was enough (the "isn't known here" error never fires), and no program mixes number types.
4. **For step 3:** `(or false nil)` in `tst/cdy/t1/basics.cdy` relies on truthiness (B25). And 16 of the draft spec's 31 error rows differ from the checker's messages in wording only; every row is caught.
5. **Tried and dropped:** making a variant its own type, as mypy does. It needs variance: `(List SAssign)` where `(List Stmt)` is expected, which happens in 60 places in the translator.

**A new question for you** (Question 8 in the HLD): `get` on a variant's value. A constructor gives the sum, so `(get (Rect 4 5) h)` is `get` on a `Shape`, and not every `Shape` has an `h`. The spec shows exactly this (`30-match.md:42`), and so does `tst/cdy/sums.cdy`.
- **A.** `get` on a sum needs a field every variant has; the example and the test read the field inside a `match` instead. *Lasting*: a sum's value is one of its variants, unknown until it's matched.
- **B.** A variant is its own type, which means variance in the checker.
- **C.** A for now, and B later.

I propose A.

**Status:** B115 is in `review`. `bin` changes by about 1,000 lines, mostly the checker, unused for now. The full test run gives 447 passed, 36 xfailed and 13 xpassed, and the linters are clean.

The survey scripts are in the scratchpad and won't be committed: `/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/scratchpad/survey.py` (and `rows.py`, `neg.py` next to it).

On "gawc" I'll commit it as "type-checker step 1: the checker, as a survey" and tag the rebuild `boot/41`.

*(The context was summarised here; the turns before it are above.)*

## Owner

> A, gawc

## Claude Code

*ran: `grep -n "Question 8\|From the survey\|^8\.\|Proposed: A\*\*\|step 3\|Step 3\|^3\`*

*ran: `sed -n 210,266p doc/hl_rqmt/type_checker.md`*

*ran: `python3 - <<'EOF'`*

*ran: `sed -n 188,200p doc/hl_rqmt/type_checker.md && ls backlog | grep -E "B11[5-8]" &`*

Question 8 is answered in the HLD. Now the tests, then the commit.

*ran: `python script/backlog.py >/dev/null && pytest -q -x tst/py_cdy/test_doc_links.py`*

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

*ran: `python script/bootstrap.py --step HEAD 2>&1 | tail -3 && python script/bootstrap`*

I've committed step 1 as `41ecf41` ("type-checker step 1: the checker, as a survey") and tagged it `boot/41`. The bootstrap check passed on that commit, and the tag is annotated. Every file in the commit was one of the step's own; you had no edits of your own in the tree.

Question 8 is recorded in the HLD as answered A (*lasting*): `get` on a sum needs a field that every variant has. The spec example (`30-match.md:42`) and `tst/cdy/sums.cdy` change in step 3, when the checker is turned on. Step 1's notes already list it among the things to settle there.

The doc-link and backlog tests pass after the HLD edit. I didn't rerun the full suite for that edit, because it only changed text; the last full run was 447 passed. Nothing is pushed; the branch and `boot/41` go up on "push". Step 2, positions in Core, is next.

## Owner

> go ahead with step 2

## Claude Code

*ran: `sed -n 1,209p doc/hl_rqmt/type_checker.md`*

*ran: `grep -n "deft Expr" -A 22 core.cdy && grep -n "deft Pos\|deft (Pos\|(deft Sym\|(`*

*ran: `grep -nE "\((Call|If|Lambda|Field|Assoc|MatchE|Tuple|Fmt) " core.cdy lower.cdy e`*

*ran: `grep -rnE "core__(Call|If|Lambda|Field|Assoc|MatchE|Tuple|Fmt)\b" tst src/py_cdy`*

*read: `src/cdy/core.cdy`*

Step 2 is under way: I'm adding a `pos` to the eight Core variants, starting in `core.cdy`, then `lower`, `emit` and `check`.

*ran: `sed -n 1,18p src/cdy/core.cdy && sed -n 720,760p src/cdy/core.cdy && grep -n "La`*

*ran: `python3 - <<'EOF'`*

*ran: `python3 - <<'EOF'`*

Now `lower.cdy`:

*ran: `sed -n 40,130p src/cdy/lower.cdy && sed -n 140,300p src/cdy/lower.cdy`*

*ran: `sed -n 340,395p src/cdy/lower.cdy && sed -n 465,495p src/cdy/lower.cdy && sed -n`*

*ran: `python3 - <<'EOF'`*

Now `emit.cdy` and `check.cdy`:

*ran: `sed -n 308,330p src/cdy/emit.cdy && grep -n "^(import" src/cdy/emit.cdy src/cdy/`*

*ran: `python3 - <<'EOF'`*

*ran: `grep -nE "[^(]\((Call|If|Lambda|Tuple|Fmt|Field|Assoc|MatchE) " src/cdy/emit.cdy`*

*ran: `sed -n 1,10p src/cdy/lower.cdy`*

*ran: `sed -i '8s/^(import core)$/(import form)\n(import core)/' src/cdy/lower.cdy && p`*

T1 builds and passes mypy. Now checking that output doesn't change, by comparing old `bin` against the new T1 on every test program and the translator itself:

*ran: `rm -rf tmp/cmp && mkdir -p tmp/cmp/a tmp/cmp/b && n=0 && d=0 && for f in $(find `*

*ran: `diff tmp/cmp/a/tst_cdy_loops.cdy.py tmp/cmp/b/tst_cdy_loops.cdy.py | head -20 &&`*

*ran: `python tmp/t1.py tst/cdy/loops.cdy tmp/x.py 2>&1 | tail -3 && sed -n 1,40p src/p`*

*ran: `mkdir -p tmp/t1d && mv tmp/t1.py tmp/t1d/ && for f in form.cdy prelude_macros.cd`*

Identical output on every program and on the translator itself (`quoting.cdy` is a macro file, which neither translates on its own). Now the rebuild and the full suite:

*ran: `python src/py_cdy/self_host.py 2>&1 | tail -3 && git diff --stat bin && pytest -`*

*ran: `pytest -q 2>&1 | tail -3`*

Same results as before step 2: 447 passed, 36 xfailed, 13 xpassed. Now the *Done* note and B116:

*ran: `python3 - <<'EOF'`*

Step 2 is done but not committed. Eight of Core's expression nodes now record where their form is in the source: `Call`, `If`, `Lambda`, `Tuple`, `Fmt`, `Field`, `Assoc` and `MatchE`. The translator's output doesn't change.

**What changed:**
- **`core.cdy`:** each of those nodes gets a `pos` as its last field, like `Sym` and `Lst` have. Analysis fills it with the position of the form it came from.
- **Nodes the translator makes itself:**
  - A `let`'s applied `Lambda`s and a `tup` pattern's `at` reads take the position of the `let` or the `match`.
  - The nodes that build a quoted form get no position, like the forms they build. In step 3, an error inside one reports its parent's position.
- **`lower.cdy`:** a node it rebuilds keeps its position. The `not` it makes for an `or` has none. It now imports `form`, for the `Pos` type.
- **`emit.cdy` and `check.cdy`:** each pattern gets an extra `_`. The checker starts using the positions in step 3.

A missed pattern would have failed the build, because the translator checks that a pattern names all of a variant's fields.

**Checks:**
- **Same output:** the old `bin` and the new T1 write byte-identical Python for every test program and for the translator. `quoting.cdy` is the exception only because it's a macro file, which neither one translates on its own.
- **Tests:** after the rebuild, the full run gives the same as before: 447 passed, 36 xfailed, 13 xpassed. No Python changed, so I didn't rerun the linters.

The HLD has step 2's *Done* note, and B116 is in `review`. On "gawc" I'll commit it as "type-checker step 2: positions in Core" and tag the rebuild `boot/42`.

## Owner

> gawc, push

## Claude Code

*ran: `git status --short && S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c87`*

*ran: `python script/bootstrap.py --step HEAD 2>&1 | tail -2 && python script/bootstrap`*

I've committed step 2 as `ef0e5bb` ("type-checker step 2: positions in Core") and tagged it `boot/42`. The bootstrap check passed on it, and the tag is annotated.

The push is done: `type-checker` now includes steps 1 and 2 on origin, along with the `boot/41` and `boot/42` tags.

Step 3 turns the checker on: type errors stop translation and show positions, and the error messages are settled.

## Owner

> go ahead with step 3

## Claude Code

*read: `src/cdy/check.cdy`*

*ran: `grep -n "deft Top" -A8 src/cdy/core.cdy && grep -n "pos-text" -A4 src/cdy/form.c`*

*ran: `sed -n 54,70p src/cdy/form.cdy && sed -n 140,180p tst/py_cdy/test_spec.py && gre`*

*ran: `cat src/cdy/cdyc.cdy | sed -n 1,146p`*

*ran: `sed -n 1180,1200p src/cdy/core.cdy && sed -n 1330,1416p src/cdy/core.cdy && sed `*

I'm wiring the checker into translation: first, positions for `def` and `defn` themselves, so an error in a bare literal value has somewhere to point.

*ran: `grep -n "TDef \|TDefn \|(TDef\b\|(TDefn\b" src/cdy/*.cdy tst/py_cdy/*.py | grep `*

*ran: `python3 - <<'EOF'`*

Now the checker itself: a position in its context in place of the definition's name, and a `check-types` that fails translation:

*ran: `python3 - <<'EOF'`*

Re-indenting the two bodies I wrapped in a `let`:

*ran: `python3 - <<'EOF'`*

Now the two test programs and the spec example the survey flagged:

*ran: `grep -n "or false nil" -B3 -A3 tst/cdy/t1/basics.cdy && grep -n "get" tst/cdy/su`*

*ran: `sed -n 1,30p spec/30-match.md && grep -n "None\|False" tst/cdy/t1/basics.out && `*

*ran: `python3 - <<'EOF'`*

Building T1 with the checker on, then having it translate itself (so the checker runs over the translator):

*ran: `python bin/py/cdy_translator.py src/cdy/cdyc.cdy tmp/t1d/t1.py 2>&1 | tail -2 &&`*

The unqualified-imports limit (B108) again: `core` already has a `check-types`. Renaming mine `type-check`:

*ran: `grep -n "check-types" src/cdy/core.cdy | head -2 && sed -i 's/(check-types /(typ`*

T1 type-checks the translator and every test program. Tidying the comment I lengthened, then the rebuild and full suite:

*ran: `sed -n 23,28p src/cdy/cdyc.cdy`*

*ran: `python3 - <<'EOF'`*

The survey tests call `type-survey`, which is gone now that the checker runs in every translation; I'll remove them. First, the expected failures that remain:

*ran: `sed -n "$(grep -n 'SURVEY_KNOWN' tst/py_cdy/test_self_host.py | head -1 | cut -d`*

*ran: `pytest -q -rxX tst/py_cdy/test_spec.py 2>&1 | grep -E "^(XFAIL|XPASS)"`*

13 of the draft's error rows still differ. Seeing what the checker says for each:

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

Most misses are wording; I'll settle them on one shape, "X: expected A, got B", plus "the test is A, not B" for an `if`'s test and a `match`'s subject, as the draft has it:

*ran: `grep -n "join-types\|join-all\|\"if: the test\"\|match: the subject" src/cdy/che`*

*ran: `sed -n 425,480p src/cdy/check.cdy && sed -n 738,765p src/cdy/check.cdy`*

*ran: `python3 - <<'EOF'`*

*ran: `python3 - <<'EOF'`*

All rows match now. A verbose look at the checking file, to make sure the messages read well with their positions:

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

Good. Now removing the survey tests, adding a `get`-on-a-sum row to `checking.records`, and running everything:

*ran: `python3 - <<'EOF'`*

*ran: `python src/py_cdy/self_host.py 2>&1 | tail -1 && pytest -q -rX 2>&1 | grep -E "F`*

Everything passes except B10's repro, which the checker now catches, so B10 can close. Reading the four items step 3 closes or narrows:

*ran: `for b in B10 B25 B30 B17 && do echo "=== $b" && cat backlog/$b-*.md && done`*

*ran: `cat backlog/B15-*.md && grep -rn "B25\]\]\|B10\]\]\|B30\]\]\|B17\]\]" spec doc/h`*

B10, B25 and B30 close; B17 and B15 narrow. Next, the stable spec's rules that step 3 changes:

*ran: `for id in types.checking types.records expr.conditionals expr.arithmetic expr.un`*

*ran: `sed -n 155,180p spec/20-types.md && grep -n "^<a id\|^## \|type" spec/50-macros.`*

*ran: `sed -n 40,57p spec/50-macros.md && sed -n 55,80p spec/20-types.md && grep -n "ch`*

*ran: `python3 - <<'EOF'`*

B42 says macro code runs without mypy, so my sentence was wrong. Fixing it:

*ran: `python3 - <<'EOF'`*

Now the backlog. Checking how B6's closing note was worded, to match:

*ran: `sed -n '/## Notes/,$p' backlog/B6-*.md backlog/B112-*.md`*

*ran: `python3 - <<'EOF'`*

*ran: `sed -n 10,20p backlog/B10-*.md && grep -n "B15\]\]" spec/*.md | head`*

Now narrowing B15 to what's left. Checking whether `backlog.py` ties an item's file name to its title:

*ran: `grep -n "slug" script/backlog.py tst/py_cdy/test_backlog.py | head`*

*ran: `python3 - <<'EOF'`*

*ran: `sed -i 's/^where: 'src\/cdy\/core.cdy', 'src\/cdy\/emit.cdy'$/where: 'src\/cdy\/`*

Now step 3's *Done* note in the HLD:

*ran: `python3 - <<'EOF'`*

All tests pass. Linting the test file I edited (`PROGRAMS` and `IDS` may now be unused):

*ran: `ruff check src tst script 2>&1 | tail -3 && ruff format --check src tst script 2`*

*ran: `ruff format --diff src tst script 2>&1 | head -20 && git stash -q && ruff format`*

A leftover section heading and comment from the survey tests; removing them:

*ran: `python3 - <<'EOF'`*

Step 3 is done but not committed. The checker is on: a type error now stops translation, with its position, before any Python is written. The translator passes its own checker, and so do all the test programs. The full suite passes: 435 passed, 4 xfailed, 45 xpassed; the 45 are the draft spec's examples, which now pass. The linters are clean.

**What changed in the translator:**
- `translate-modules` runs `type-check` after analysis and fails on the **first** type error (*for now*). Macro code isn't checked, as planned (B42).
- An error starts with the innermost position the checker has. `def` and `defn` got a position too, so `(def x "a")` has somewhere to point.
- `type-survey` and its two tests are gone, since every translation is checked now.
- One rename: `check-types` was already taken in `core.cdy`, so the entry point is `type-check`.

**The messages** use one main shape: `what: expected A, got B`, for example `argument 2 of pick:`, `def x:`, `assoc: field x of V:` or `+:`. For an operator, its first argument sets the type. Three other shapes cover the rest:
- **A test or a subject:** `if: the test is Int, not Bool`.
- **Two types that must be one:** `if: the branches are Int and String`.
- **Too many fields for a constructor:** `(V ...) takes 1 field(s), got 2`, the message variants already had.

I changed three of the draft's rows to fit:
- `assoc: field x of V: expected Int, got String`;
- `a (Tup Int Int) has 2 items, not 3`, without `match:`, because a `let` takes tuples apart too;
- `+`'s message now says it takes "a number, String or a list".

**The spec:**
- **Your answer A to Question 8:** `checking.records` now says `get` on a sum needs a field every variant has, and has a row for it. The example at `30-match.md:42` now reads a shared field with `get` and the other field inside `match`; `tst/cdy/sums.cdy` reads `h` inside `match`.
- **The stable rules:**
  - `[[types.checking]]`: the translator checks types, and mypy checks again as a second check;
  - `[[types.records]]` points to `[[checking.records]]`;
  - `[[expr.conditionals]]` and `[[expr.unit]]` point to their checking rules;
  - `[[expr.arithmetic]]`: `+` joins lists, with an example;
  - `[[match.tup]]`: a pattern names as many items as the tuple has;
  - `[[macros.macro-code]]`: macro code isn't type-checked, by Candy or by mypy.
- **`basics.cdy`:** `(or false nil)` became `(or false true)`, and its expected output changes from `None` to `True`.

**The backlog:**
- **Done:** B10 (its repro is now a row of `[[checking.records]]`), B25 and B30.
- **B17 narrowed:** what's left is taking a record apart as a tuple, and parameters as patterns.
- **B15 narrowed and retitled** "Candy's type checker is an MVP, with mypy as a second check". What it lists as left: mypy still runs, there's no let-polymorphism, `get` or `assoc` on a type not yet known is an error, and only one error is reported. Its state is still `in-progress`, and its priority is still `high`; the review can decide whether either should change.
- **B117** is in `review`.

The HLD has step 3's *Done* note. On "gawc" I'll commit it as "type-checker step 3: the checker on" and tag the rebuild `boot/43`.

## Owner

> i'm still reading the above, so forgive me if it's in there, is there a leak for any cases todo with the get type stuff?

## Claude Code

*ran: `sed -n 1,25p backlog/B18-*.md && grep -ln "get" backlog/B*.md | head -30`*

Partly. Three cases come out of the `get` work, and only one has a proper item:

1. **`get` on a value whose type isn't known yet** gives the error "get: the type of p isn't known here (name)". It's *for now* (`[[checking.order]]`, Question 4), but its only record is a bullet in B15's narrowed text and the link from the spec rule. It has no item of its own. Since it's a shortcut a user can hit, CLAUDE.md's rule says it should be a `leak` item. The survey found it never fires on the translator or the tests, so I'd make it `low`.

2. **`get` on a value typed `Any`** isn't checked at all. B18 covers this, and B30's closing note points to it. But B18's text still says only that *mypy* checks nothing that passes through `Any`. Now that Candy's checker exists, the text should say Candy's checker skips it too. That's a small edit.

3. **`get` on a sum needs a field that every variant has.** This was your answer A to Question 8, recorded as *lasting*, so it isn't a leak and has no item. The alternative, variants as their own types (which needs variance), was tried in the survey and dropped. If you'd like that kept as a possibility for later, it could go in as an `idea`. Otherwise the HLD's Question 8 is the only record of it.

My suggestion:
- add **B119** as a `low` leak for case 1, with B15's bullet pointing to it;
- fix B18's text for case 2;
- leave case 3 as it is.

Both changes would go into the step 3 commit. Should I make them?

## Owner

> ya, the question was about the get on a sum type: so, if you do a get on a valid field of a type (that's part of a sum type), but it's on a field that's not in every type of the sum type, the type checker fails and what else happens, does it let thru to lower and we cross our fingers?

## Claude Code

*ran: `mkdir -p tmp/q && printf '(deft S (A ((x Int))) (B ((y Int))))\n(put (get (A 1) `*

No. The checker runs after analysis and before `lower`, and its first error stops translation, so nothing reaches `lower` or `emit` and no Python is written. I tried it with the rebuilt `bin`:

```
(deft S (A ((x Int))) (B ((y Int))))
(put (get (A 1) x))
```
```
candy: a.cdy:2:6: get: S has no field x
```

It exits with status 1 and no output file. That's the rule from your answer A to Question 8: `(A 1)` has type `S`, and `x` isn't a field of every `S`. To read `x`, take the value apart with `match`.

The case that does still get through is a value typed `Any`, which the checker doesn't check at all:

```
(deft S (A ((x Int))) (B ((y Int))))
(sig s Any)
(def s (B 2))
(put (get s x))
```

This translates, and fails when it runs, with Python's `AttributeError: 'B' object has no attribute 'x'`. mypy doesn't catch it either, because the type is `Any` in Python too. That's B18, whose text still mentions only mypy (the fix I suggested). A value gets typed `Any` by writing it in a `sig`, or by using a built-in that returns `Any`, such as `at` on a list.

The two fixes I suggested still stand: B119 for the "isn't known here" error, and the B18 text. Should I make them?

## Owner

> i guess the question is: there's a chance that a valid get on a sum type is going to fail? currently...

## Claude Code

*ran: `printf '(deft S (A ((x Int))) (B ((y Int))))\n(sig f (Fn (S) Int))\n(defn f (s) `*

Yes, in one direction. The checker turns away some `get`s that would have worked when run. It never accepts a `get` on a sum that then fails when run, unless the value is typed `Any`.

**What it accepts is safe.** It accepts `get` on a sum only when every variant has that field with the same type. Then whichever variant the value turns out to be, the field is there.

**What it rejects that would have worked.** All of these stop translation; none reaches Python. I ran each with the rebuilt `bin`:

1. **The variant is obvious from the code:** `(get (A 1) x)` gives `get: S has no field x`. This is the rule you chose, *lasting*. The way to write it is `match`.

2. **Inside the clause that matched it:**
   ```
   (defn f (s) (match s ((A _) (get s x)) (else 0)))
   ```
   This also gives `get: S has no field x`. The checker doesn't narrow, so `s` is still an `S` inside the `(A _)` clause. You can write `((A x) x)` and use the bound name instead. Still, this cuts against the reason recorded for A ("unknown until matched"): here it *has* been matched. I think this one deserves an item: narrowing the subject inside its clause, an `idea` or a `leak` for you to choose. B20 covers narrowing only for `Maybe` (after `(= m nil)`), not for sums.

3. **A shared field with different types:**
   ```
   (deft S (A ((id Int) (x Int))) (B ((id String))))
   (put (get (A 1 2) id))
   ```
   This gives `get: S has no field id`. Rejecting it is right, but the message is wrong: every variant *has* `id`, just not with one type. It should say something like `get: field id of S has different types in its variants`. That's a small fix in `sum-field` and `field-type` in `check.cdy`, plus a spec row, and it belongs in step 3.

Counting what's pending now:
- the message fix (case 3), in step 3;
- an item for narrowing inside a clause (case 2);
- B119 for the "isn't known here" error;
- the B18 text.

Should I do all four?

## Owner

> have another question: the error is on the get (which has to be inside a match...) why isn't the error on the `deft`?

## Claude Code

Because the `deft` isn't wrong. Variants of one sum having different fields is the normal case: `Circle` has `r`, `Rect` has `w` and `h`. What's wrong is the `get`, which assumes a field that only some of the values have, so that's where the error points.

One correction to the question: `get` doesn't have to be inside a `match`. Outside one, `get` works on any field every variant has, which is what the new example in `30-match.md` shows (`(get (Rect "a" 4 5) id)`). Inside a clause, you'd normally use the names the pattern binds; `get` on the subject there fails only because the checker doesn't narrow (case 2 above).

For case 3, the same field name with different types in different variants, the error could go on the `deft`: "variants of S give `id` different types". But the translator itself does this. In Core's `Expr`, `Do` has `(body (List Expr))` and `Lambda` has `(body Expr)`. A rule on the `deft` would reject the translator's own types, and every program that reuses a field name the way records reuse `name`. So it's left legal, and only a `get` across those variants is an error, since no one type fits there.

If you'd prefer the stricter rule, it's a real choice. It would rename fields in `core.cdy` and probably elsewhere, and I'd suggest a backlog item for it rather than doing it in this branch.

The four pending changes are unchanged: the case 3 message fix, an item for narrowing inside a clause, B119, and the B18 text.

## Owner

> so what's are the test cases for `Shape`... in all tests?

## Claude Code

*ran: `grep -rn "Shape" spec tst/cdy backlog/*.md tst/py_cdy --include=*.md --include=*`*

`Shape` appears in four test programs and the spec's examples. It's always a sum with a few variants, and almost every test of it uses `match`. The `get`-on-a-sum rule is tested twice in all of that.

**Test programs (`tst/cdy/`):**

| File | `Shape` | What it tests |
|---|---|---|
| `sums.cdy` | `Circle r`, `Rect w h`, all `Double` | `area` and `describe` by `match`, and a generic tree. Line 67 was `(get (Rect 4.0 5.0) h)`; it now reads `h` inside `match` |
| `t1/sums_1c.cdy` | the same | `area` and `describe` by `match` (T1's copy) |
| `cdyc/lib/shapes.cdy`, used by `cdyc/modules.cdy` | `Circle r`, `Square s` | a sum defined in an imported module, and `match` on it there |

**The spec:**

| Where | What it tests |
|---|---|
| `30-match.md:25` (`[[match.sum-types]]`) | declaring a sum, `match` on it with `Dot`, a variant with no fields |
| `30-match.md:46` | **`get` on a sum:** `id` is in both variants and is read with `get`, while `h` is read inside `match`. This is new in step 3 |
| `30-match.md:81–82` | constructor errors: too few fields, `(Dot)` called |
| `30-match.md:94–159` | `match` clauses, `else`, exhaustiveness ("no clause for Rect, Dot"), mixing two sums' variants |
| `30-match.md:201` | a `tup` pattern mixed with variant patterns |
| `20-types.md:60` | `(Shape Int)` when `Shape` isn't generic |
| `25-checking.md:212` (`[[checking.match]]`) | `Circle` and `Sq` in `match`, the clauses' one type |

The second `get`-on-a-sum test isn't on `Shape`. It's the new row in `[[checking.records]]`: `(deft S (A ((x Int))) (B ((y Int)))) (put (get (A 1) x)) => get: S has no field x`.

**What no test covers for `get` on a sum:**
- **Case 3:** a field in every variant but with different types (and the misleading message);
- **Case 2:** `get` on the subject inside its own clause, since there's no narrowing;
- **A field-less variant:** with a variant like `Dot`, no field is shared, so any `get` on the sum fails;
- **A generic sum:** a shared field whose type is a type variable, such as `(deft (T a) (L ((v a))) (N ((v a))))`. I believe the checker handles it, but nothing tests it.

I'd add rows to `[[checking.records]]` for case 3 (with the message fix), case 2 and the generic sum, as part of the four pending changes. Should I go ahead?

*(The context was summarised here; the turns before it are above.)*

## Owner

> i need help on this, "The second get-on-a-sum test isn't on Shape. It's the new row in [[checking.records]]: (deft S (A ((x Int))) (B ((y Int)))) (put (get (A 1) x)) => get: S has no field x.": how can you access `A`, which is part of a sum type, directly (i.e without a match or some sort of reference to `S`?

## Claude Code

*ran: Check variant constructor use and variant as a type*

A variant's name is a constructor: a global function, unqualified like every top-level name. Any code can call it without a `match` and without naming `S`. Haskell and ML work the same way: you write `Just 1` without mentioning `Maybe`. So `(A 1)` is just a call that builds a value. What that call does *not* give you is an `A` type.

- **The value's type is `S`, not `A`.** This is question 8's answer A: the constructor's type is `(Fn (Int) S)`. After `(A 1)`, the checker only knows "some `S`" and has forgotten which variant built it. So `(get (A 1) x)` gets the sum rule: `x` isn't in `B`, so the `get` is rejected. That row tests exactly this. You're right that you can't reach `A`'s fields through `A` itself, and that's the rule. The row only shows that building the value with `A` doesn't get around it.
- **`A` isn't a type name.** A sum's variants are constructors only; `S` is the only type. I checked with `bin` (the step-3 build):
  - `(sig a S) (def a (A 1))` translates, and the Python is `a: S = A(1)` with `type S = A | B`.
  - `(sig a A)` is rejected.

So the only way to read a field that isn't in every variant is `match`, where the clause binds the field to a name: `((A x) x)`.

**Something new this turned up:** the error for `(sig a A)` is wrong.

```
candy: bad.cdy:2:1: A is not defined here; bad defines it, but this file doesn't import bad
```

It's a one-file program, so `bad` is the file itself. The message comes from the type-name check's "defined in another module" path, which mistakes a variant for a type defined elsewhere. It should say something like "A is a variant of S, not a type." This is a `defect` and not part of step 3. I'd add it as B119 and move the "isn't known here" leak to B120, alongside the other pending changes.

Shall I go ahead with those, plus the test rows from before?

## Owner

> can you archive this conversation from "i'm still reading the above..." (maybe `side-conversations`... not sure where... and note it); and then go ahead with all of them

## Claude Code

*ran: Look at doc layout and where notes go*

*ran: Find where the side conversation starts in the transcript*

*ran: Read the where-notes-go table and the existing chat archive*

*ran: List the user and assistant text turns in the side conversation*

*ran: Extract the side conversation as Markdown*

*ran: Find the sum field lookup code in the checker*

*ran: Read the field lookup code*

I've saved the side conversation's text. Next I'm fixing the message for a shared field with different types in `check.cdy`, then the backlog items and spec rows.

*ran: Add the different-types message for a shared sum field*

*ran: Add the spec rows and find the backlog items to edit*

*ran: Read B15, B18 and B30 and links to B15*

*ran: Look at an existing defect repro and the message source*

*ran: Read the type-name check that gives the message*

*ran: Check the message for a value name used as a type*

The message fix is in and the spec rows are written. Now I'm writing B119, B120 and B121 and editing B15, B18 and the HLD.

*ran: Write the three new items and edit B15 and B18*

*ran: Point the HLD at B120 and list type rule ids*

*ran: Fix the B18 notes spacing and B119's ref*

Now the archive file and its row in `doc/process.md`.

*ran: Write the chat archive, note it in the process doc, regenerate the backlog index*

*ran: Reword the archive note, regenerate the index, rebuild bin*

*ran: Run the full test suite*

*ran: Check why the new ids aren't seen*

*ran: See how the link test finds documents*

Tracked files only, so the new files need `git add -N`, which is not a commit.

*ran: Mark the new files intent-to-add and run all tests*

*ran: Confirm the new rows pass and the linters are clean*

All of it is done and nothing is committed. The full suite passes (435 passed, 5 xfailed, 48 xpassed), and ruff and mypy are clean.

**The archive** is `doc/archive/chat_get_on_sums.md`. I used `doc/archive/` rather than a new `side-conversations` directory, because that's where the earlier chat archive (`chat_spec_by_example.md`) already lives.
- It has every turn from "i'm still reading the above..." on, verbatim, under a note saying when and where the conversation happened and what came of it.
- It doesn't include this request itself or the "continued session" summary.
- I noted the convention in `doc/process.md`: a new row in "Where notes go" and a Log entry for 2026-10-29.
- The earlier turns call the "isn't known here" leak B119; the note at the top says it ended up as B120.

**The checker:** a field that every variant has, but with different types, now gives `get: field id of S has different types in its variants`. Before, it said "has no field". The fix is a new `in-every-variant` in `check.cdy`, and `bin` is rebuilt.

**Spec rows in `[[checking.records]]`** (they pass; the file is still a draft):
- **A generic sum:** a `run` example with `(deft (T a) (L ((v a))) (N ((v a) (n Int))))` that prints `4 b`.
- **Three error rows:** a variant with no fields, the different-types message, and `get` on the subject inside its own clause.
- **New text** saying the subject isn't narrowed inside a clause (*for now*: B121).

**Backlog:**
- **B119** (`defect`, `low`): a variant or value written as a type gets the misleading import message. It also happens for `(sig X Int) (def X 1) (sig a X)`. The cause is that `check-type` treats this file's own top-level names as defined somewhere else. Its repro is the strict xfail.
- **B120** (`leak`, `low`): "isn't known here". `[[checking.order]]` and the HLD now point to it instead of B15.
- **B121** (`leak`, `low`): no narrowing inside a `match` clause. I made it a `leak` rather than an `idea`, because the spec now marks it *for now*.
- **B15** links both and has a dated note. **B18**'s text now says Candy's checker skips `Any` too.

The four new files are marked `git add -N`, because the doc-link test only sees tracked files. That's still not a commit.

The step 3 commit would now also include `doc/process.md`, the archive and the three new items. It's ready for "gawc".

## Owner

> gawc

## Claude Code

*ran: Check the working tree for the owner's own edits*

No edits of the owner's own are in the tree; every changed file is from this step.

*ran: Stage step 3 and commit it*

*ran: Check the bootstrap step and tag boot/43*

Step 3 is committed as `29c6cc5` "type-checker step 3: the checker on", tagged `boot/43`.

- **Bootstrap:** `bootstrap.py --step HEAD` gave `ok 43`, and `boot/43` is an annotated tag.
- **Your edits:** there were none in the tree, so the commit holds only this step's changes, including the archive of the side conversation and B119–B121.
- **Not pushed.**

Next is step 4, the docs:
- update CLAUDE.md, the iMVP doc and `multi_target.md`;
- mark `spec/25-checking.md` stable.

Then comes review, and the merge into master after `pytest -m bootstrap`.

## Owner

> go ahead with step 4

## Claude Code

*ran: Read step 4's item and plan*

*ran: Outline the HLD*

*ran: Read the HLD's status and steps 3–4*

*ran: Find docs that describe type checking*

*ran: Read the iMVP doc's type-checking passages*

*ran: Read multi_target.md's type-checking passages*

*ran: See how the previous docs step edited the iMVP doc*

I'm updating the docs for step 4: CLAUDE.md, the iMVP doc, `multi_target.md`, and the spec's status. First I'm checking a few facts so the docs say them right.

*ran: Check type-check's result, status formats and B17*

Now the edits.

*ran: Update CLAUDE.md, the iMVP doc, multi_target.md, and mark the checking spec stable*

*ran: Fix the Core node name and look for leftover draft mentions*

*ran: See when the previous HLD was marked done*

*ran: Add the HLD's done notes, move B118 to review, run all tests*

Step 4 is done but not committed; it's ready for "gawc". The full suite passes: 484 passed, and the 5 xfails are backlog repros, B119's among them. With `25-checking.md` now stable, its examples run as real tests instead of non-strict xfails, and all of them pass.

**CLAUDE.md:**
- `check.cdy` is in the list of translator files.
- A new "Type checking" bullet under "How the translator works" says where the checker runs, its rules, the `pos` field on Core nodes, and that macro code isn't checked (B42).
- The `sig` decision now says the translator checks types against the `sig`s and mypy is a second check (B15). Before, it said mypy checks "until Candy has its own type checker".
- The `tup` pattern's note says the checker checks the arity, instead of "only by mypy".
- A "History" sentence for the branch, which names tag `type-checker` before the merge, as `field-checks` did.

**The iMVP doc:** in the five places that expected a Candy type checker later, a short note in brackets says it came on this branch. The new text of the iMVP doc stays as it was, as with `field-checks`.

**`multi_target.md`:** the checker is listed as a front-end stage that runs on Core before any backend, so every target gets it. Two places now say that the types it infers aren't kept in Core yet. That matters for choosing `show` from the static type.

**The spec:** `25-checking.md` is `status: stable`, and the "(draft)" is gone from `spec/README.md`.

**The HLD:** step 4 has its *Done* note. Step 3's note now also lists what came out of the `get`-on-sums questions, linking the archive and B119–B121.

**Backlog:** B118 is `review`, and the index is regenerated.

After the commit, the review goes through B117 (step 3) and B118 (step 4) one at a time. Then comes the merge into master, after `pytest -m bootstrap`.

## Owner

> commit and review?

## Claude Code

*ran: Commit step 4*

*ran: Check the step items' states*

*ran: Read steps 1 and 2's done notes*

**B115, step 1: the checker, as a survey.** Commit `41ecf41`, tag `boot/41`.

What it built:
- **`check.cdy`:** unification over Core's `CType`.
  - The checker's own variables are flexible (`?N`, shown as `t1`); a `sig`'s variables are rigid.
  - It checks against an expected type where there is one, such as an `if`'s branches or a `fn` given a function type, and infers otherwise.
- **The survey** ran it over the whole translator (4,000 lines), every test program and every spec example.

What the survey found:
- **One real error in the translator, which mypy couldn't see:** `emit-lit` passed a `Char` to `py-str`, which takes a `String`. It's fixed.
- **Two rules changed to fit the translator's code:**
  - `+` joins lists;
  - a `(Tup t ...)` whose items are all `t`s is accepted as a `(List t)` (*for now*, B29).
- **Two rules confirmed:**
  - checking `fn` arguments last is enough: "isn't known here" never fired;
  - no program mixes number types.
- **Tried and dropped:** variants as types of their own. That needs variance, and would have meant 60 changes in the translator. This led to Question 8.

Later steps changed some of this:
- `type-survey` and its two tests were removed in step 3, since every translation is checked now.
- The "isn't known here" leak is now B120.

**Tick?**

## Owner

> tick

## Claude Code

*ran: Tick B115: done, fixed on type-checker, with a note*

B115 is ticked: `done`, `fixed: type-checker`, with a note dated 2026-10-29.

**B116, step 2: positions in Core.** Commit `ef0e5bb`, tag `boot/42`.

- **`core.cdy`:**
  - `Call`, `If`, `Lambda`, `Tuple`, `Fmt`, `Field`, `Assoc` and `MatchE` end with a `pos`, the form's own position (`scope here`), as `Sym` and `Lst` already did.
  - A `let`'s `Lambda`s and a `tup` pattern's `at` reads take the `let`'s or the `match`'s position.
  - The `Expr`s that build quoted forms are `NOWHERE`, so an error inside one takes its parent's position.
- **`lower.cdy`:** a node it rebuilds keeps its `pos`, and the `not` it makes for an `or` is `NOWHERE`. It now imports `form`, for `Pos`.
- **`emit.cdy` and `check.cdy`:** each pattern gained a `_` for the new field.
- **No output change:** the old `bin` and the new T1 wrote the same Python, byte for byte, for every test program and for the translator itself.
- **Step 3 added more:** `TDef` and `TDefn` also got a `pos`, for a definition whose value is a leaf, like `(def x "a")`.

**Tick?**

## Owner

> expand on step 3 added more... including on "...whose value is a leaf..."

## Claude Code

*ran: List Core's Expr nodes and the checker's position helpers*

*ran: Show where errors land for leaf and non-leaf definition values*

A "leaf" is a Core node with nothing inside it, and in Core the leaves are also the nodes without a position.

**Which nodes have one.** Step 2 gave a `pos` only to the compound `Expr` nodes: `Call`, `If`, `Lambda`, `Tuple`, `Fmt`, `Field`, `Assoc` and `MatchE`. The leaves have none:
- `Lit`, a literal. It holds a `Form`, but only `Sym` and `Lst` forms carry a `Pos`; `Txt`, `IntLit` and the other literal forms don't.
- `Local` and `Global`, a name.
- `Prim`, a built-in such as `nil`.

`Do`, `Temp` and `Clause` have none either.

**How the checker finds a position.** As it walks into an expression, `at-node` (`check.cdy:180`) updates the context's `here` whenever the node has a position. An error is reported at the innermost enclosing node that has one. That works for a leaf inside something: in `(+ s 1)`, the bad `s` is reported at the `+` call.

**The gap step 3 closed.** A definition's whole value can be a leaf, with no compound node above it. Before step 3, `TDef` and `TDefn` had no position either, so nothing above the leaf had one. The error came out at `NOWHERE`, with no `file:line:col`, unlike every other translator error. Step 3 gave both a `pos`, the `def` or `defn` form's position, which `check-top` starts from. I ran the three cases with `bin`:

| Program | Error |
|---|---|
| `(sig x Int)` / `(def x` / `  "a")` | `l1.cdy:2:1: def x: expected Int, got String` |
| `(sig f (Fn (Int) String))` / `(defn f (n)` / `  n)` | `l2.cdy:2:1: defn f: expected String, got Int` |
| the same, with the body `(+ n 1)` on line 3 | `l3.cdy:3:3: defn f: expected String, got Int` |

In the first two the value is a leaf, so the error falls back to the `def`'s position (2:1). In the third the body is a `Call`, so the error is at the body itself (3:3).

**What's still imprecise.** A leaf's error points at the nearest compound node or definition above it, never at the leaf itself. In the first case the culprit `"a"` is at 3:3, but the message says 2:1. That's usually close enough, because the message names the definition. Pointing at the leaf would need a `pos` on `Lit`, `Local` and `Global`, and a position on the literal forms in the reader. That means changing many more patterns than step 2 did. I'd record it as a low-priority `leak` (B122) rather than do it in this branch. Should I add it?

**B116, step 2:** tick?

## Owner

> Tick

## Claude Code

*ran: Tick B116: done, fixed on type-checker, with a note*

B116 is ticked. I haven't added B122, the item for an error inside a leaf being reported at its parent; say if you want it.

**B117, step 3: the checker on.** Commit `29c6cc5`, tag `boot/43`.

- **On:** `translate-modules` runs `type-check` on the analysed program, before `lower`. The first type error stops translation, with `file:line:col`, so no Python is written. Macro code isn't checked (B42). The survey and its two tests are gone.
- **Positions:** an error is reported at the innermost node with a position, and `TDef` and `TDefn` gained one (as above).
- **Messages,** in a few shapes, each naming the types:
  - `what: expected A, got B`, as in `argument 2 of pick:`, `def x:`, `assoc: field x of V:` and `+:`;
  - for a test or subject, which has one right type: `if: the test is Int, not Bool`;
  - for two types that must be one: `if: the branches are Int and String`;
  - for an arity: `(V ...) takes 1 field(s), got 2` and `a (Tup Int Int) has 2 items, not 3`;
  - for `get` on a sum: `get: S has no field x`, and `get: field id of S has different types in its variants`.
- **Question 8 (A):** a variant's constructor gives the sum, and `get` on a sum needs a field every variant has, with one type. This is in `[[checking.records]]`, with rows for a variant with no fields, `get` inside a clause, and a generic sum. `[[match.sum-types]]`'s example reads a shared field with `get`.
- **Spec:** `25-checking.md` has 34 error rows and its `run` examples, all passing. The stable files were updated to match:
  - `[[types.checking]]` says the translator checks and mypy is a second check;
  - `[[types.records]]`, `[[expr.conditionals]]`, `[[expr.arithmetic]]` (`+` joins lists) and `[[expr.unit]]` point at the checking rules;
  - `[[match.tup]]` gives the arity rule;
  - `[[macros.macro-code]]` says macro code isn't checked.
- **Test programs:** `(or false nil)` became `(or false true)` (B25), and `sums.cdy` reads `h` inside a `match`.
- **Backlog:**
  - B10, B25 and B30 are done;
  - B15 and B17 are narrowed;
  - B18's text now covers Candy's checker;
  - new: B119 (a variant written as a type gets a wrong message), B120 ("isn't known here") and B121 (no narrowing inside a clause).
- **Process:** side conversations go in `doc/archive/chat_<topic>.md`; this one is `chat_get_on_sums.md`.
- **Bootstrap:** one rebuild, and the translator type-checks itself.

**Tick?**

## Owner

> Add b122, tick

## Claude Code

*ran: Add B122, tick B117, regenerate the index and check links*

B122 is added as a `low` leak: an error in a leaf is reported at its parent, with the `(def x "a")` example. B117 is ticked, and its note links B122. The backlog and link tests pass.

**B118, step 4: the docs.** Commit `a63cec8`.

- **CLAUDE.md:**
  - `check.cdy` is in the list of translator files;
  - a new "Type checking" bullet says where the checker runs and gives its rules: no let-polymorphism, `Any` gradual, the `Maybe` and `Tup`-as-`List` rules, `fn` arguments last, `get` on a sum;
  - the same bullet lists the Core nodes with a `pos`, and says macro code isn't checked;
  - the `sig` decision says the translator checks types and mypy is a second check (B15);
  - the `tup` pattern's arity is checked by the checker now, not only by mypy;
  - "History" has a sentence for the branch.
- **The iMVP doc:** a short note in brackets in each of its five "Candy's type checker later" passages says it came on `type-checker`. The rest of the doc stays as it was.
- **`multi_target.md`:** the checker is a front-end stage, run on Core before any backend, so every target gets it. Two places say the types it infers aren't kept in Core yet, which matters for choosing `show` by static type.
- **The spec:** `25-checking.md` is `stable`, so its examples are now strict tests, and they all pass. The "(draft)" is gone from `spec/README.md`.
- **The HLD:** step 4 has its *Done* note, and step 3's note lists what came out of the questions on `get` on sums.

**Tick?** After that, the remaining steps are:
1. commit the review;
2. mark the HLD done;
3. run `pytest -m bootstrap`;
4. merge into master, with tag `type-checker`.

## Owner

> Tick and go

## Claude Code

*ran: Look at the previous branch's review commit, merge and tag*

*ran: See how the HLD status was marked done and whether an HLD index exists*

Now I'm ticking B118, marking the HLD done, and committing the review.

*ran: Tick B118, mark the HLD done, commit the review*

The review is committed. Next I'm running the full suite and the bootstrap chain before the merge.

*ran: Run the full suite and the bootstrap chain*

While it runs, here's the merge message I've drafted:

*ran: Write the merge commit message*

The merge waits on the test runs.

## Owner

> <task-notification>
> <task-id>b5t0ne2m3</task-id>
> <tool-use-id>toolu_01PVgagzpQbU9CxNCdBsLEeM</tool-use-id>
> <output-file>/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/tasks/b5t0ne2m3.output</output-file>
> <status>completed</status>
> <summary>Background command "Run the full suite and the bootstrap chain" completed (exit code 0)</summary>
> </task-notification>

## Claude Code

*ran: Read the test results*

*ran: Read the full suite's summary line*

The suite and the bootstrap chain both pass. Now the merge and the tag.

*ran: Merge type-checker into master and tag it*
