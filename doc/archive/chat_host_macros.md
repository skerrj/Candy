*Archived 2026-11-25, from the Claude Code session that built branch `host-macros`
(2026-11-23 to 2026-11-25; HLD `doc/hl_rqmt/host_macros.md`, tag `host-macros`), by
`script/chat_archive.py`, before the merge.* The owner's messages and Claude's replies,
verbatim; each tool call is a one-line marker, and thinking and tool output are left
out. The session had built and merged `interpreter` first (`chat_interpreter.md`); this
starts where the owner asked for this branch's HLD, drafted on `master`, and goes on
with the branch from its creation to the tick of its tasks. The session's context was
summarized on the way (the harness's, not shown).

What came of it: macro code analysed, type-checked and run on the interpreter, with the
prelude, through a bridge of forms as values (`interp_macros.cdy`); a macro file a module
of macro code, loaded once per translation; a template's built-in and prelude names
qualified ([[macros.hygiene]]); `load-macros` and the `exec` gone, step 6 as two
unstaged commits; [[B224]] (expand and include as one loop) and [[B232]] (a template's
special forms checked) as ideas, and typed code for macros in `doc/brainstorm.md`;
`boot/96` to `boot/103`, and the boot tags sorted by number.

# host-macros

## Owner

> Go

## Claude Code

*ran: Read the epic's host-macros branch and its mentions*

*ran: Read the epic's macro passage and the branch's backlog items*

*ran: Find what the interpreter HLD says about macros*

*ran: Read the interpreter HLD's opening, pros, bootstrap and after-MVP sections*

Now the macro machinery itself: how `expand.cdy` compiles and runs macro code today.

*ran: Outline expand.cdy and the macro files*

*ran: Read expand.cdy's header, loading and macro program code*

*ran: Read the driver's macro compile and the runtime's load and call*

*ran: Read macro-imports, translator.cdy and form.cdy*

*ran: List open macro backlog items and the modules HLD's macro passage*

*ran: Find every macro in use and the macros HLD's outline*

Reading the macros HLD's account of how macro code runs today, then drafting the new HLD.

*ran: Read the macros HLD's terms, running and staging sections*

*ran: Read the prelude and test macros, count cond uses, check prelude for macros*

*ran: Count cond and put uses, and time a cond-like expansion on the interpreter*

*ran: Read the macro spec's rules and mentions of the host and prelude*

*ran: Read the macro-code, errors, gensym and import-macros rules*

*ran: Read the bootstrap staging options and a past HLD's bootstrap section*

*ran: Check system and prelude qualification, put with text shadowed, and the next id*

*ran: Check that operators and prelude names can be qualified*

*ran: Read the interpreter HLD's goals and questions format*

*wrote: `doc/hl_rqmt/host_macros.md`*

*ran: Tidy two passages, check line lengths and doc links*

Rewrapping two long lines in the new HLD.

*ran: Read the passage with the long lines*

*ran: Rewrap both passages and recheck*

*ran: Rewrap the hygiene paragraph and recheck the links*

I've drafted the HLD for the epic's seventh branch, `host-macros`, as `doc/hl_rqmt/host_macros.md`. It's on `master` and not committed, and the doc-link test passes. I'll create the branch once you've answered its questions.

**The idea:** macros run on the interpreter instead of being translated to Python and run with `exec`. A file's macros become a small program, as today, but now:
1. It is analysed and type-checked like any program, so a macro that returns the wrong kind of value is an error at its `defmacro`.
2. It is loaded on the interpreter.
3. Each macro call converts the argument forms into interpreter values and the result back into a form.

The first measurement looks cheap. A four-clause `cond`-like expansion runs on the interpreter in about 0.2 ms, so the translator's 145 `cond`s and `put`s would add a few hundredths of a second. Step 1 will check the whole suite's time against today's.

**Steps:**
1. Macros on the interpreter.
2. Macro code type-checked (B42, a macro's result isn't checked).
3. The prelude for macro code (B52, macro code doesn't get the prelude).
4. Macro files as modules (B45, macro files still use inclusion), each loaded once per translation.
5. Hygiene for built-ins (B46, macro templates aren't hygienic).
6. `load-macros` dropped. This is the only step that needs bootstrap staging: the `bin` before still uses it.
7. The docs.

**Questions:**
1. **Scope.**
   - **In:** B41 (macros run with `exec`), B42, B52, B45, B63 (a macro file compiled per importer), B70 (`load-macros` finds names by Python name), the second half of B197 (macro code's module), and B46 for built-ins only.
   - **Out:** B43 (`gensym` is impure), B44 (a macro can't expand into `import`), B61 (`expand.cdy` knows special forms' shapes) and B64 (`form.cdy` copied next to every translator). Each is low priority or not about how macros run.
   - **Recommended: as listed.** B44 would change the order of the translator's passes, a branch's worth of work on its own.
2. **Hygiene.** Today a file that defines its own `text` breaks every `put` in it; I checked, and it does.
   - **(a)** In a template, write a name that means a built-in or a prelude function qualified, so `(text x)` becomes `(system.text x)`. A template that calls its own macro file's helper stays as it is.
   - **(b)** Clojure's whole rule: every free name in a template is qualified. Macro files would then have to be imported by the program too, not only while translating.
   - **(c)** Leave B46 open.
   - **Recommended: (a).** It fixes the case that bites, every program's `put`, with a small change to `quasi`. I checked that `system.++` and `prelude.rest` already work.
3. **Error positions.** Today `call-macro` puts the call's position in front of a macro's error message.
   - Keep it, with generic types in place of `Any`. Its Python is unchanged, so no staging.
   - Or make the interpreter return a panic as a value, which rewrites every `eval` and slows it.
   - Or drop the position, which gives worse errors.
   - **Recommended: keep it.** One visible change either way: an `at` out of range in a macro reads `f: at: index out of range: 5, for length 0` instead of `f: IndexError`, so that spec row changes.
4. **Forms crossing over.**
   - Copy each form both ways on each call.
   - Or give the interpreter a value kind that holds the translator's own form. Then `match`, `get`, `=` and `show` each need a second kind of record.
   - **Recommended: copy.** The copies are small.
5. **`gensym`.**
   - Keep the host's counter (`fresh-name`) in the interpreter's table, for macro code only.
   - Or make it pure now, with every macro taking and returning a counter.
   - **Recommended: the table entry.** B43 is low priority, and the pure version changes every macro's type.
6. **Where the conversion lives.**
   - A new `interp_macros.cdy`, next to the interpreter's two files.
   - Or `expand.cdy`, which would then import the interpreter.
   - **Recommended: `interp_macros.cdy`**, so `expand.cdy` stays about forms.

Once you've answered, I'll mark the HLD accepted, file the step tasks starting at B224 and create the branch, all in its first commit.

## Owner

> So, a translated product will get the expanded macros?.... Without needing to run the interpreter...

## Claude Code

Yes. Macros run only while the program is being translated, and the Python file that comes out holds only what they expanded into. Nothing in it calls a macro, so nothing in it needs the interpreter.

What changes is where the expansion happens, inside the translator:
- **Today:** the translator compiles a file's macros to Python, runs them with `exec`, and splices the forms they return into the program.
- **With this branch:** the translator runs the same macros on its own interpreter and splices in the same forms.

The interpreter is already a module of the translator (`interp.cdy`, in `bin` since the last branch), so the translator gains no new dependency. The translated program still depends only on the runtime, `cdy_rt`, as CLAUDE.md requires.

So a translated program should come out byte for byte as it does today. The checks already test that:
- the `cmp3` comparison of all 108 programs against the previous `bin`;
- the self-hosting fixpoint, which needs the translator, its source full of `cond`s, to translate itself into the same text.

The differences are all at translation time:
- **Macro errors:** an out-of-range `at` in a macro reads as the spec's message instead of `IndexError`.
- **New errors:** a type error in macro code is caught at its `defmacro`.
- **Hygiene (step 5):** a program that defines its own `text` gets a working `put` instead of an error.

That last one is the only case where translated output differs from today's, and only for programs that failed to translate before.

I can add that to the HLD's Goals: translated output unchanged, checked by `cmp3` at each step.

## Owner

> Ok add that, then put up the hld again

## Claude Code

*ran: Add the unchanged-output goal to the HLD*

*read: `doc/hl_rqmt/host_macros.md`*

I've added a goal, "Translated programs unchanged", to `doc/hl_rqmt/host_macros.md` (lines 52–59), and the doc-link test still passes. It says macros run inside the translator while it translates, so a translated program holds only their expansions, never needs the interpreter, and still depends on `cdy_rt` alone. Its Python stays byte for byte today's, which the comparison with the previous `bin` and the fixpoint check at every step. The only differences are at translation time:
- a macro's error messages read differently;
- a type error in macro code is a new error;
- from step 5, a program that defines its own `text` translates, where today it fails.

Here is the HLD again. It's still a draft, not committed.

**What it does:** macros run on the interpreter instead of being translated to Python and run with `exec` (B41).
- A file's macros still become one small program. It is now analysed and type-checked like any program, then loaded on the interpreter.
- Each call converts the argument forms into interpreter values and the result back into a form. The conversion goes in a new module, `interp_macros.cdy`.
- `cdyc.cdy` hands the expander a loading function, so `expand.cdy` doesn't import the interpreter.

**Goals:**
- **No `exec`:** `load-macros` goes, and with it the trick of putting `form.cdy`'s names back to the translator's own.
- **Macro code checked** (B42, a macro's result isn't checked): a macro that returns an `Int` is an error at its `defmacro`. A macro's function gets a real type, not `Any`.
- **The prelude for macro code** (B52, macro code doesn't get the prelude): `rest`, `Maybe` and `find` become usable in macros, and `form.cdy`'s `rest-of` goes.
- **Macro files as modules** (B45, macro files still use inclusion):
  - a macro file's `import`s become real imports;
  - macro code's module becomes its file's name, not `""` (B197, the second half);
  - each macro file is loaded once per translation (B63, a macro file compiled per importer).
- **Translated programs unchanged:** the new goal above.
- **Hygiene for built-ins** (B46, macro templates aren't hygienic): a template's built-in and prelude names are written qualified, so a file's own `text` no longer breaks `put`.

**Not goals:**
- **B43 (`gensym` is impure):** `gensym` keeps the host's counter.
- **B44 (a macro can't expand into `import`):** stays.
- **B61 (`expand.cdy` knows special forms' shapes):** stays.
- **B64 (`form.cdy` copied next to every translator):** stays, now as the source of macro code's `form` module.
- **B46 (the helper case):** a template calling its own macro file's helper stays as it is.
- **Speed:** a four-clause `cond`-like expansion takes about 0.2 ms on the interpreter.

**Errors:**
- **Still reported at the call:** a macro's errors still start with the call's position and the macro's name, and `call-macro` still adds them, now with generic types in place of `Any`.
- **One spec row changes:** an `at` out of range in a macro reads `f: at: index out of range: 5, for length 0` instead of `f: IndexError`.

**Bootstrap:** only step 6 is staged, because the `bin` before it still uses `load-macros`.

**Steps:**
1. **Macros on the interpreter:** the program still flat and unchecked, as today. The suite's time is compared with today's.
2. **Macro code checked** (B42).
3. **The prelude for macro code** (B52).
4. **Macro files as modules** (B45, B63, B197).
5. **Hygiene for built-ins** (B46, narrowed).
6. **`load-macros` dropped** (B41, B70): staged. B49 (host objects have no Candy type) narrows to `module-dir`.
7. **Docs and "Looking back".**

**Questions:**
1. **Scope:**
   - **In:** B41, B42, B52, B45, B63, B70, the second half of B197, and B46 for built-ins.
   - **Out:** B43, B44, B61 and B64.
   - **Recommended: as listed.** B44 changes the order of the translator's passes, a branch on its own.
2. **Hygiene:**
   - (a) A template's names that mean built-ins or prelude functions are written qualified, `system.text`.
   - (b) Clojure's whole rule, every free name qualified, which would make macro files part of the program too.
   - (c) Leave B46 open.
   - **Recommended: (a).** It fixes every program's `put` with a small change to `quasi`.
3. **Errors at the call:**
   - Keep `call-macro`, retyped. Its Python is unchanged, so no staging.
   - Or make the interpreter return panics as values, which rewrites every `eval`.
   - Or drop the position.
   - **Recommended: keep it.**
4. **Forms crossing over:**
   - Copy each form both ways on each call.
   - Or give the interpreter a value kind that holds the translator's own form, which `match`, `get`, `=` and `show` would each have to know.
   - **Recommended: copy.**
5. **`gensym`:**
   - Keep the host's counter in the interpreter's table, for macro code only.
   - Or make it pure now, which changes every macro's type.
   - **Recommended: the table entry.**
6. **Where the conversion lives:**
   - A new `interp_macros.cdy`.
   - Or inside `expand.cdy`.
   - **Recommended: `interp_macros.cdy`.**

## Owner

> So, B44 is just saying that a macro can't create any import statements?

## Claude Code

Mostly, yes, and it covers a little more than `import`. B44 (a macro can't expand into `import`, `import-macros` or `defmacro`) says a macro's expansion can't contain any of those three forms. Any other top-level form is fine: a macro can expand into a `defn`, a `sig`, a `deft`, or a `do` of several of them. `deftest` already does that, expanding into a `sig` and a `def`.

**Why:** the translator works in a fixed order: read, then `include`, then expand, then analyse.
- **Imports are handled before any macro runs:** `include` has already found every `import` and read the modules.
- **Macros are collected before any macro runs:** expansion gathers every `defmacro` and `import-macros` first, to know which macros exist.
- **So a generated one comes too late:** when a macro returns `(import util)`, it reaches `analyse`, which fails with "import is only allowed at top level". A generated `defmacro` fails the same way.

**Where it bites:** a macro that wants to set things up for its user. The test module is the example in hand:
- **Today:** `test_macros.cdy`'s `deftest` and `check` expand into `test.Test`, `test.Pass` and `test.Fail`. So every file that uses them must also write `(import test ())` itself, next to `(import-macros test_macros)`. The macro file's comment says so ("a file using them imports it, by convention").
- **With B44 fixed:** a single `(use-tests)` macro could expand into both lines.

The workaround is just to write the `import` yourself, which is why B44 is marked low.

**Why I left it out:** the fix is Racket's and Clojure's approach, expanding the top-level forms one at a time and handling an `import` when expansion produces it. That merges `include` and expand into one loop, which changes how the translator reads a program, not how macros run. That's why I'd keep it for a later branch.

One connection to this HLD: Question 2's hygiene option (a) only qualifies built-in and prelude names. A macro whose template names another module's definitions, as `deftest` names `test.Test`, still needs its user to import that module. B44 is what would remove that last bit of boilerplate.

## Owner

> Is the include/expand loop merge stuff in the backlog anywhere?

## Claude Code

*ran: Search the backlog and docs for the include/expand merge*

*ran: Read B44's fields and where the docs mention it*

Only as one line: B44's own suggested fix ("Fix: expand top-level forms before `include`, one at a time (as Racket and Clojure do); until then, a better error"). Nothing in the backlog, `doc/brainstorm.md` or the HLDs describes merging the loop as a design: what each pass would become, or what it costs. `macros.md` only records today's order, read → `include` → expand → `analyse` (line 263).

I also missed something when I drafted Question 1: the epic gives B44 to this branch. `python_complete.md:398` lists "the macro leaks that remain (B43, B44)" for `host-macros`, and its triage table (line 628) agrees. So leaving B44 out goes against the epic's plan, and the HLD should say so.

If you agree to leave it out, I'd make it a proper item rather than leave it as one line:
- **File an idea:** "expand and include as one loop", with what it involves:
  - expanding the top-level forms one at a time;
  - an `import` met during expansion read as a module then;
  - a `defmacro` or `import-macros` produced by a macro taking effect for the forms after it.
- **Point to it:** B44's fix line refers to the new idea.
- **The epic:** its line 398 and the B44 row say B44 moved to a later branch.
- **The HLD:** Question 1 says it's a departure from the epic, not just a scope choice.

Or we take B44 into this branch. It fits better once macro files are modules, which is step 4, since an `import` met during expansion would use the same module reading. That makes the branch bigger: I'd estimate one more step, about the size of step 4.

My recommendation is still to leave it out and file the idea. It changes how the translator reads a program, and a merged loop is easier to design once macro files are modules here.

## Owner

> Agree, leave it out and file it for later.... Agree with all recommendations

## Claude Code

*ran: Read an idea item and a step task for their format*

*ran: See what the interpreter branch's first commit touched*

## Claude Code

Filing the idea, the step tasks, and the HLD's answers:

*ran: Create the branch, file B224 and B225-B231, record the answers*

*ran: Look at the long lines*

*ran: Rewrap the two lines and recheck*

I've created the `host-macros` branch from `master`, and its first commit is ready. Nothing is committed yet.

**The HLD** (`doc/hl_rqmt/host_macros.md`) is marked accepted, with your answer under each question: all six as recommended, B44 left out.

**Filed:**
- **B224 (expand and include as one loop):** an idea, low priority. It describes:
  - expanding the top-level forms one at a time;
  - an `import` resolved when expansion meets it, and a `defmacro` or `import-macros` taking effect for the forms after it;
  - the questions it raises: whether a macro can be used above its `defmacro`, as it can today, and cycles found partway through a module.

  It also says it fits once macro files are modules (this branch's step 4), and gives `(use-tests)` as the example of what it would allow.
- **B225 to B231:** the seven step tasks, `open`:

  | Task | Step |
  |---|---|
  | B225 | Macros on the interpreter |
  | B226 | Macro code checked |
  | B227 | The prelude for macro code |
  | B228 | Macro files as modules |
  | B229 | Hygiene for built-ins |
  | B230 | `load-macros` dropped (staged) |
  | B231 | The docs |

**Updated:**
- **B44 (a macro can't expand into `import`, `import-macros` or `defmacro`):** its fix line points to B224, and a dated note says it was left out of this branch although the epic gave it to `host-macros`.
- **The epic** (`python_complete.md`): the seventh branch's entry says what's planned. Its B44 row says "left out: B224, later".

The doc-link and backlog tests pass, and the token scan is clean.

On "gawc" I'll commit as "Start branch host-macros: HLD accepted, B225-B231 its tasks". Then step 1, B225 (host-macros step 1: macros on the interpreter), on "go".

## Owner

> Gawc, go

## Claude Code

*ran: Commit the branch start*

*ran: Read interpret, run-top, the key functions and Macro's uses*

*ran: Read the BUILTINS table's shape and imports*

*ran: Find gensym uses and the macro compile path's callers*

*ran: Read interp's header area and the builtins file's ends*

*ran: Add load-tops and call-global, MACRO_BUILTINS, and the bridge module*

*ran: Find expand.cdy's uses of the compile path*

*ran: Hand expand.cdy a loader in place of compile and load-macros*

*ran: Type macro-list's lookup and read form.cdy's Macro*

*ran: Type Macro and call-macro, give cdyc the loader, build T1*

Building step 1; fixing an import clash (`Value` is in both `core` and `interp`).

*ran: List only what interp_macros needs from core, rebuild T1*

T1 builds. Now T1 expands with the interpreter; checking the macro tests and the spec's macro file:

*ran: Translate the macros test program with T1, and run the macro spec*

*ran: Find how core.cdy analyses quoting*

*ran: Read quoted and quasi-list*

*ran: Quote lists of forms as ListOf, rebuild T1, retest the macros*

The one failure is the row the HLD said would change. Updating the spec:

*ran: Update the spec row and run the whole suite*

*ran: Read test_interp's imports and find read-source*

*ran: Add a round-trip test of the bridge*

Rebuilding `bin`, then the suite, the checkers and the comparison with `boot/95`:

*ran: Rebuild bin, run everything, compare with boot/95*

Everything passes, and `boot/95`'s `bin` gives the same output for all 108 programs. Timing the translator translating itself, old `bin` against new:

*ran: Time the old and new bin on the translator and a macro program*

Speed is unchanged: 1.02 s against 0.98 s to translate the translator, and the same for `macros.cdy`. Writing the step's notes:

*ran: Write step 1's Done note, adjust step 6, move B225 to review*

Step 1 is built: macros now run on the interpreter, and B225 (host-macros step 1: macros on the interpreter) is in review. Nothing is committed. All 853 tests pass, the checkers are clean, and `boot/95`'s `bin` gives the same output for all 108 programs, so the translated Python is unchanged.

**What changed:**
- **The interpreter** (`interp.cdy`): two new functions, `load-tops`, which runs a program's definitions without calling `main`, and `call-global`, which calls one of its functions by name.
- **The conversion** (the new `interp_macros.cdy`):
  - `form-value` and `value-form` convert a form to an interpreter value and back.
  - `macro-runner` loads a macro program once and turns each `macro__NAME` into a function on forms.
- **The loading** (`cdyc.cdy`): `macro-loader` analyses the macro program and hands it to `macro-runner`. It replaces `compile-macros` and the `exec`.
- **Macro code's built-ins** (`interp_builtins.cdy`): `MACRO_BUILTINS`, the interpreter's table plus `gensym`'s `fresh-name`.
- **Types:** a macro's function is now typed `(Fn ((List Form)) Form)`, and `call-macro` is generic instead of `Any`, with its Python unchanged.
- **The spec:** the `IndexError` row is now `f: at: index out of range: 5, for length 0`.

**Two things the HLD missed:**
- **Quoting built a list of forms as a tuple** in Core. On Python a list and a tuple are spelled the same, but the interpreter keeps them apart. `core.cdy` now builds a list. Only macro code quotes, so no program's Python changes.
- **`gensym`'s counter restart.** `load_macros` restarted the counter on every load, so a translation's `x__1` names don't depend on what was translated before it. To keep that, `macro-loader` calls `load-macros` with no code, purely for the restart. It's a temporary hack, marked *for now*: step 6 replaces it with a built-in of its own, and B230 (host-macros step 6) says so.

**Speed:** unchanged.
- The suite takes 56 s, against 57–59 s before.
- Translating the translator takes 1.02 s, against 0.98 s with the old `bin`.

**Tests:** a new `test_forms_cross_to_the_interpreter_and_back` checks that every kind of form, with its position, comes back the same.

**Tagging:** no staging is needed. On "gawc" I'll commit and tag `boot/96`. Then step 2, macro code type-checked.

## Owner

> Gawc

## Claude Code

*ran: Commit step 1, check its bootstrap step and tag boot/96*

Step 1 is committed as `d0a5ef5` ("host-macros step 1: macros on the interpreter") and tagged `boot/96`. `bootstrap.py --step` passed with no staging, `boot/96` is an annotated tag, and the tree is clean.

Next is step 2, B226 (host-macros step 2: macro code checked): the macro program gets type-checked before it loads, so a macro that returns something other than a form is an error at its `defmacro`. Every macro in use has to pass the checker, which may turn up something. The spec's `macros.macro-code` rule will then say macro code is checked, with an error example.

Not pushed: `host-macros` and `boot/96` are local only. Say "go" for step 2.

## Owner

> "the macro program gets type-checked before it loads"... Can we expand this.... It can't go deeper than form?

## Claude Code

The check goes deeper than the result, but it stops at the form. There are two levels.

**1. The macro code itself is checked, all of it.** The macro program is checked like any program:
- each `macro__NAME`, with its `sig` `(Fn ((List Form)) Form)`;
- every helper it calls;
- `form.cdy`'s definitions.

So every expression inside a macro's body is checked, whether or not the macro is ever called:
- `(+ 1 "a")` in a macro is a type error.
- `(list-items "x")`, a `String` where a `Form` goes, is a type error.
- A helper called with the wrong number of arguments is an error.
- A body that returns an `Int` is an error: it should be a `Form`.
- Inside a `quasi`, an `(unq e)` must give a `Form`, and an `(unq-sp e)` a `(List Form)`. The checker sees this, because a template is analysed into calls of the `Form` constructors.

All of these are reported at the macro's code, with its position, when the file is translated. Today none of this is checked:
- **Before step 1:** a bug showed only when the macro ran, as a Python error.
- **Since step 1:** it shows as an interpreter error at the call. A macro that returns an `Int`, for example, gives "internal error: interp: a macro gave a value that isn't a Form".

**2. What a form *contains* isn't checked there.** `Form` is just a syntax tree: a `Lst` of `Sym`s and literals. The type says "this is a form", not "this is a well-formed `if`" or "this is an expression of type `Int`". So the checker can't see that `(quasi (if (unq test)))` is missing its `then`, or that a template adds a `String` to an `Int`.

That's still caught, one stage later:
1. The expansion goes back into the program and is analysed and type-checked as the program's code.
2. The error is reported at the macro's call. That's `macros.errors-at-call`'s row `(defmacro bad () (quo (if)))`, which fails with "if: expected (if test then else?)".

So there are two checks:
- **The macro's own code:** at its definition, from this step.
- **What it produced:** at each use, already today.

Going deeper, a typed form such as `(Code Int)` whose templates are checked as code when the macro is defined (as MetaOCaml and typed Template Haskell do), would be a different design. It isn't in this HLD or the backlog.

## Owner

> "What a form contains isn't checked there"... This was what i was asking about

## Claude Code

Got it: you're asking whether a macro's output could be checked when the macro is defined, not only when it's used. There are several levels it could go to.

**Today, and after step 2:** a template is checked only through its uses. Each call's expansion goes back into the program and is analysed and type-checked there.
- **Upside:** it's simple and always right, because the checker sees real code with real types.
- **Downsides:**
  - a mistake in a template shows up only once something calls the macro, and a rarely used macro can hide one;
  - the error is reported at the call, in terms of the expanded code, which the user didn't write (B156, an error in a macro's expansion names the expansion's forms).

**Option 1, shapes in templates.** `syntax.cdy` already declares each special form's shape: `(if test then else?)`, `let`'s bindings, `import`'s list. When a `quasi` template is analysed, its special forms could be checked against those shapes, with each `(unq e)` counted as one form and an `(unq-sp e)` as any number.
- **Would catch at the definition:** `(quasi (if (unq test)))`, missing its `then`; a `let` with a malformed binding.
- **Wouldn't catch:** types, a wrong argument to an ordinary function, or anything that depends on what the holes turn out to be.
- **Cost:** small, since the shapes exist, so I'd call it modest and safe.

**Option 2, typed code.** Templates would have types: `(quasi (+ (unq x) 1))` would be a `(Code Int)` when `x` is a `(Code Int)`. The whole template would be type-checked at the definition, with each hole typed. That's MetaOCaml and typed Template Haskell. It fits Lisp macros badly, though:
- **Not all syntax is an expression:** many macros take or produce something other than an expression. `cond` takes clauses, and `deftest` produces a `sig` and a `def`, which are top-level forms.
- **Names mean the use site's:** a template's names are resolved where it expands, and hygiene depends on that.
- **Two kinds of macro:** you'd end up with typed macros for expressions and untyped `Form` macros for everything else.

It's a big language design, a branch or more, and it changes what a macro is.

**Option 3, check by example.** A macro's author tests it on sample uses, with `deftest` expanding them. Nothing is needed from the language; it's a matter of practice.

My suggestion:
- **Option 1:** file it as an idea for after this branch. It's cheap and catches the common slip.
- **Option 2:** a line in `doc/brainstorm.md`, with the reasons it doesn't fit, rather than a backlog item.
- **Scope:** neither goes into `host-macros`. Step 2 checks the macro code itself, the first level.

Should I file those two, or would you rather look closer at one of them first?

## Owner

> Ok let's stick with today's plan, note it's details, and note the two options

## Claude Code

*ran: Read brainstorm.md's format and B156*

*ran: File B232, add the typed-code brainstorm entry, and note the details in the HLD*

*ran: Rewrap B232's note*

I've written down the plan's details and filed both options. Nothing is committed; these notes can go in with step 2's commit.

- **The HLD** has a new section, "What checking macro code checks (step 2)" (`doc/hl_rqmt/host_macros.md`, before "The prelude for macro code"). It covers both levels:
  - **Checked at the `defmacro`:** every expression of macro code, whether or not the macro is ever called. The section lists the examples.
  - **Checked later:** what a form contains, one stage later at each call, as today, in the expansion's words (B156, an error in a macro's expansion names the expansion's forms).

  It then names the two ways to check more, both for later and not this branch's, with your decision dated today.
- **B232 (a `quasi` template's special forms checked against their shapes):** filed as an idea, low priority. It's option 1: each special form in a template checked against `syntax.cdy`'s declared shape, `(unq e)` counted as one form and `(unq-sp e)` as any number. It checks shapes only, not types.
- **`doc/brainstorm.md`:** a "typed code for macros" entry, option 2, with why it fits Lisp macros badly (clauses and top-level forms aren't expressions, hygiene, two kinds of macro). It points to B232 as the cheap half.

The doc-link and backlog tests pass. Say "go" when you want step 2, B226 (host-macros step 2: macro code checked).

## Owner

> Go

## Claude Code

*ran: Find how the driver calls the type checker*

*ran: Type-check the macro program before it loads; try the macro programs*

Every macro in use passes the checker. Running the suite:

*ran: Run the suite and try ill-typed macros*

*ran: Find the checker's defn and list-item messages*

*ran: Read the checker's defn check and imports*

*ran: Name a macro's defn as defmacro in errors, give templates positions*

Both read well now. Updating the spec's `macros.macro-code` rule, with error rows:

*ran: Add the macros.checked rule with its error rows*

*ran: See how a fixed leak was closed before, and B42's mentions*

*ran: Find B42's other mentions*

*ran: Search the sources and checker docs for B42*

*ran: Read the B42 mentions in CLAUDE.md, core.cdy and emit.cdy*

*ran: Write step 2's notes, rebuild bin, run everything, compare with boot/96*

*ran: Check whether B42's long line is old*

Step 2 is built and checked; rewrapping one note line.

*ran: Rewrap B42's note and recheck*

Step 2 is built: macro code is now type-checked before it runs. B226 (host-macros step 2: macro code checked) is in review, and so is B42 (a macro's result isn't checked). Nothing is committed.

All 857 tests pass and the checkers are clean. `boot/96`'s `bin` gives the same output for all 108 programs, so no program's Python changed.

**What changed:**
- **The check:** `macro-loader` (`cdyc.cdy`) runs the type checker on the macro program before loading it. Every macro in use passed as it was: the prelude's, the test module's and the test programs'.
- **Two error messages fixed, which read badly for macro code:**
  - A macro's body error now names it `defmacro m`, not `defn macro__m`, the internal function it becomes (`check.cdy`'s new `defn-label`).
  - A template's list now carries the template's position, not the `defmacro`'s (`core.cdy`'s `quasi-list`, `close-run` and `join-parts`).
- **The spec:** a new rule, `macros.checked`, with four error rows:

  | Macro | Error |
  |---|---|
  | `(defmacro m (a) 5)` | `line 1, column 17: defmacro m: expected Form, got Int` |
  | `(defmacro m (a) (list-items "x"))` | `argument 1 of list-items: expected Form, got String` |
  | `(defmacro m (a) (quasi (+ (unq 1) 2)))` | `line 1, column 24: List: an item: expected Form, got Int` |
  | `(defmacro m (a) (quasi (f (unq-sp a))))` | `argument 2 of ++: expected (List Form), got Form` |

  The rule says what a form contains is still checked at the call, and points to B232 (a `quasi` template's special forms checked against their shapes). `macros.macro-code` loses its *for now* about B42.
- **CLAUDE.md:** "macro code isn't checked" is now "is checked too, before it runs on the interpreter".

The third message still says `List: an item` for a template's hole, which describes the analysed template, not what the author wrote. It's the same kind of problem as B156 (an error in a macro's expansion names the expansion's forms), so I left it.

This commit also carries the notes from our discussion: B232, the brainstorm entry and the HLD's "What checking macro code checks" section.

`bin` changed, so on "gawc" I'll commit and tag `boot/97`. Then step 3, the prelude for macro code.

## Owner

> Gawc

## Claude Code

*ran: Commit step 2, check its bootstrap step and tag boot/97*

Step 2 is committed as `3becb0c` ("host-macros step 2: macro code checked") and tagged `boot/97`. `bootstrap.py --step` passed with no staging, `boot/97` is an annotated tag, and the tree is clean. The commit also carries B232 (a `quasi` template's special forms checked against their shapes), the typed-code brainstorm entry, and the HLD's new section.

Next is step 3, B227 (host-macros step 3: the prelude for macro code):
- **The import:** macro code imports the prelude implicitly, so `rest`, `Maybe`, `find`, `index-of` and `with-default` become usable in macros.
- **`rest-of` goes:** `form.cdy`'s `rest-of` is replaced by `rest` in its three uses, two in `core.cdy` and one in `test_macros.cdy`.
- **The spec:** `macros.macro-code` drops its *for now* about the prelude.

`prelude.cdy` uses no macros, so loading it for macro code creates no cycle with the prelude's macros.

Not pushed: `host-macros` and `boot/96` to `boot/97` are local only. Say "go" for step 3.

## Owner

> Go

## Claude Code

*ran: Read how the driver reads, expands and analyses modules*

*ran: Find how the prelude becomes a module and analyse-program's shape*

Macro code's program is analysed on its own, so the prelude has to come in as a module: its Core definitions loaded with the macros, and its exports imported. Checking what `prelude.cdy` imports:

*ran: Check the prelude's imports and rest-of's uses*

`rest-of` is used only by `test_macros.cdy` (the two in `core.cdy` are a local, `rest-of-type`), and the prelude imports nothing. Writing it:

*ran: Start the expander change and look for a pair accessor*

No pair accessors; a `Tup` pattern in the `let` does it. Writing the rest properly:

*ran: Analyse the prelude once for macro code and load it with each macro program*

*ran: Read the loader's comment and macro-imports as they stand*

*ran: Import the prelude in macro code and use rest in test_macros*

*ran: Drop rest-of, rebuild T1, try macros that use the prelude*

The prelude works in macro code (`find`, `with-default`, `rest`). Two test files still use `rest-of`; checking how the quoting test builds its macro code:

*ran: Read the quoting test's macro-code translation*

The quoting test still translates macro code to Python, through `macro-imports`, so it needs the prelude's exports now. Fixing it and the two `rest-of`s:

*ran: Fix the quoting test and two rest-of uses, and the spec's list*

*ran: Rewrite the macro-code rule with a prelude example and run it*

My example was wrong: the second call expands to `b`, which the program never defines. Giving it one:

*ran: Fix the example and run the suite*

*ran: See why the bin driver's macro test fails*

That one is `bin` running the new `macros.cdy` before `bin` is rebuilt, which fixes it. Rebuilding, then everything and the comparison with `boot/97`:

*ran: Rebuild bin, run everything, compare with boot/97*

*ran: Compare the old bin on the old files with the new bin on the new*

*ran: Show how test_test's translation differs*

The only difference is the file path I gave each `bin`, relative in one and not the other, so both programs translate the same. Timing, since every macro load now checks the prelude too:

*ran: Time the old and new bin on the translator and a small program*

Unchanged. Writing the step's notes:

*ran: Write step 3's notes, move B227 and B52 to review, check*

*ran: Fix B52's notes and find CLAUDE.md's prelude sentence*

*ran: Update CLAUDE.md's prelude sentence and recheck*

Step 3 is built: macro code now gets the prelude, and B227 (host-macros step 3: the prelude for macro code) is in review, along with B52 (macro code doesn't get the prelude). Nothing is committed. All 857 tests pass and the checkers are clean.

**What changed:**
- **The prelude, read once:** `macro-prelude` (`cdyc.cdy`) reads and analyses `prelude.cdy` once per translation. It imports nothing and uses no macros, so it needs no expanding and there's no cycle with the prelude's macros.
- **Imported and loaded:** macro code imports the prelude as a program does. Its definitions are type-checked and loaded with each macro program.
- **`rest-of` is gone:** `form.cdy`'s `rest-of` is replaced by `rest` in `test_macros.cdy` and two test files (`macros.cdy`, and the quoting test, which uses `drop`).
- **The spec:** `macros.macro-code` says macro code sees the prelude and runs on the interpreter, so what it prints is Candy's `show` and `text`. A new example uses `find`, `with-default` and `rest` in a macro.
- **A test fix:** `test_quoting_in_macro_code` still translates macro code to Python, so it now passes the prelude's exports.
- **CLAUDE.md:** "macro code doesn't get the prelude" becomes "gets the prelude too".

**The comparison with `boot/97`:** 104 of the 108 programs give the same output.
- **The other four:** they use the prelude in macro code, so the old `bin` can't run them: `macros.cdy`, `test_test.cdy` through `test_macros.cdy`, and two spec examples.
- **Checked another way:** I ran the old `bin` on the old versions of `macros.cdy` and `test_test.cdy` and the new `bin` on the new ones. They translate the same, apart from the file path I passed each `bin`.

**Speed:** unchanged. Translating the translator takes 1.04 s with either `bin`, and the suite took 61 s, against about 60 s before.

On "gawc" I'll commit and tag `boot/98`. I expect no staging: building T1 only uses the prelude's macros, which don't change. Then step 4, macro files as modules, the largest step.

## Owner

> Gawc

## Claude Code

*ran: Commit step 3, check its bootstrap step and tag boot/98*

Step 3 is committed as `e8c4cf4` ("host-macros step 3: the prelude for macro code") and tagged `boot/98`. `bootstrap.py --step` passed with no staging, as expected, `boot/98` is an annotated tag, and the tree is clean.

Next is step 4, B228 (host-macros step 4: macro files as modules), the largest step:
- **Real imports:** `import-macros` reads a macro file as a module, so its `import`s become real imports instead of pasting files in.
- **Real modules:** macro code's module becomes its file's name, with `form` imported as a module, so quoting builds `form.Sym` (B197, the second half). That replaces the flat program with module `""`.
- **Loaded once:** each macro module is loaded once per translation (B63, a macro file compiled per importer).

Before writing code I'll look at how `include.cdy` and `expand.cdy` handle macro files today, and I'll say if the step should split in two.

Not pushed: `host-macros` and `boot/96` to `boot/98` are local only. Say "go" for step 4.

## Owner

> Go

## Claude Code

*ran: Read expand-file and the macro-file import code*

This step is bigger than the others, so I'm reading how `include.cdy` reads a program and a macro file before deciding its shape.

*ran: Outline include.cdy*

*ran: Read include.cdy's module reading, inclusion and module list*

*ran: Read the rest of include.cdy*

*ran: Find every use of the macro-file machinery*

*ran: Read the macro file tests and their library files*

I have the shape. Checking a few signatures before writing:

*ran: Check signatures, Python forward references and the quoting test*

Writing `expand.cdy`'s side first:

*ran: Read expand.cdy's header and loading section as they stand*

*ran: Rewrite expand.cdy's macro files as modules of the macro world*

Macro files' helpers today expand with the prelude's macros too (`cond`), so `expand-macro-file` must start from them as `expand-file` does:

*ran: Start macro files from the prelude's macros; read cdyc's loader*

Now the driver's side, `cdyc.cdy`: the macro world's base, and the two loaders.

*ran: Read cdyc's expander, macro-prelude, loader and macro-imports*

*ran: Write the macro world in cdyc.cdy: base, file and own loaders*

Now the rest: `macro-runner` by key with `form`'s module, quoting's module, and the comments.

*ran: Key macro-runner by global key, and list quoting's module-less globals*

*ran: Make quoting build form module's Forms*

*ran: Build T1*

*ran: Try the macro test programs with T1*

`macro-list` already adds the `macro__` prefix, so my callers doubled it:

*ran: Drop the doubled prefix, rebuild, retry*

*ran: Run the quoting test as macro code on the interpreter*

Now removing inclusion from `include.cdy`, since nothing reads a file that way any more:

*ran: Remove inclusion from include.cdy*

*ran: Remove the now unused imported-name, rebuild, run the macro tests*

*ran: Find the test expecting the inclusion error*

*ran: Read the import-list error test's macro file case*

That error is gone by design: a macro file's `import` can list names now, as any module's can, so the same files now give the import's own error. Updating the row:

*ran: Update the test row and run the suite*

*ran: See why the quoting test fails*

*ran: Quote a literal with its field's type, rebuild, rerun the quoting test*

*ran: Read the quoting test around the failing def*

The test program itself built a list with `Tup`, which only Python let through. Fixing the test to `List`:

*ran: Build the test's list with List, and rerun*

The quoting test passes on the interpreter. Adding a test of what's new: a macro file whose helper module comes in by a real `import`, with a name list and a qualified name:

*ran: Add a test of a macro file as a module*

*ran: Analyse a macro file's imported modules as macro code*

Now the full suite, and the spec's `macros.import-macros`, which still says a macro file's `import` is inclusion:

*ran: Run the suite and find the spec's inclusion wording*

*ran: Read the two spec passages about macro files' imports*

*ran: Update the spec's account of macro files' imports*

Rebuilding `bin`, then everything and the comparison with `boot/98`:

*ran: Rebuild bin, run everything, compare with boot/98, time it*

*ran: Format, and see pylint's finding*

Formatting fixed one test line. Now the notes; first the other places that say macro files use inclusion:

*ran: Find the docs and comments about inclusion and module ""*

*ran: Read the module "" comments in core.cdy and CLAUDE.md*

*ran: Write 4a's notes, docs and backlog notes, and check*

*ran: Check whether the long backlog lines are mine*

*ran: Rewrap the two notes*

Step 4a is built: a macro file is now a module of macro code. Nothing is committed. All 858 tests pass, the checkers are clean, and `boot/98`'s `bin` gives the same output for all 108 programs.

I split step 4 in two, as I said I might. **4a** is the modules. **4b** will load each macro file once per translation, B63 (a macro file is compiled once per file that imports it). B228 (host-macros step 4) stays open until 4b.

**What changed:**
- **Real imports:** `import-macros` reads the file with `read-modules`, so a macro file's `import`s work as any module's: name lists, qualified names (`h.wrap`) and private names.
- **The modules it imports are macro code too:** they run only while translating, so they can quote and see `Form`. That was true when they were pasted in, and it keeps it.
- **Its module:** the macro file is analysed as macro code of its own module, its stem, with its `defmacro`s as `macro__NAME` functions there.
- **A file's own `defmacro`s** are a small program of their own, of no module (`""`), like a top module's names. So they can never clash with an imported macro file's stem. They still call that file's helpers unqualified.
- **A shared base:** both start from the prelude and `form`, analysed once per translation. `form` is now a real module, so quoting builds `form.Sym`, which closes B197 (the built-ins' module, and macro code's).
- **Inclusion is gone** from `include.cdy`, with `macro-prelude`, `macro-loader` and `translate-expanded`.

**The checker found two old slips in macro code:**
- **Quoting a literal:** quoting `2l`, `3b` or `1.5f` put a `Long`, `Byte` or `Float` into a field that holds an `Int` or a `Double`. Python never noticed. Quoting now converts the value to the field's type (`core.cdy`'s `field-literal`).
- **A list built as a tuple:** the quoting test built a `(List Form)` with `Tup`. Fixed to `List`.

**Tests:**
- **The quoting test:** `test_quoting_in_macro_code` now loads its file as macro code on the interpreter (`load-macro-code`), instead of translating it to Python.
- **New:** `test_macro_file_is_a_module` covers a helper module imported with a name list, a qualified name and a private name.
- **Changed:** one existing error row now gives the import's own error. The old "a macro file's import lists no names" no longer exists.

**Docs:**
- **The spec:** `macros.import-macros` and `programs.import` say a macro file's `import` is a module's.
- **CLAUDE.md and `core.cdy`'s comments:** they no longer say macro code's module is `""` *for now*.
- **The backlog:** B45 (macro files still use inclusion) and B197 are in review.

**Speed:** unchanged. Translating the translator takes 1.06 s, against 1.05 s.

On "gawc" I'll commit 4a and tag `boot/99`. Then 4b, the cache.

## Owner

> Gawc

## Claude Code

*ran: Commit 4a, check its bootstrap step and tag boot/99*

Step 4a is committed as `cbdd1da` ("host-macros step 4a: macro files as modules") and tagged `boot/99`. `bootstrap.py --step` passed with no staging, `boot/99` is an annotated tag, and the tree is clean.

Next is 4b, which finishes B228 (host-macros step 4: macro files as modules) and fixes B63 (a macro file is compiled once per file that imports it). Each macro file will be loaded once per translation:
- **Where the cache lives:** the expander keeps the macro files loaded so far. It's passed from module to module through the translation, instead of being made fresh for each.
- **What to measure:** a program whose modules import one macro file, before and after.

Not pushed: `host-macros` and `boot/96` to `boot/99` are local only. Say "go" for 4b.

## Owner

> Go

## Claude Code

Each step that can load a macro file now hands back the Expander with that file cached. Where the functions are called:

*ran: Find every call of the expanding functions*

*ran: Read the code to thread the cache through*

*ran: Hand the Expander, with its loaded macro files, through expansion*

*ran: Fix the extra paren, rebuild*

*ran: Read program-tops as it stands*

*ran: Fix the paren on the right line, rebuild*

T1 builds with the cache. Now measuring the gain: a program whose modules import one macro file, counted by how often it loads.

*ran: Time a program of eight modules importing one macro file*

*ran: Time the eight-module program with boot/99's bin and with T1*

0.20 s to 0.15 s for eight modules sharing one macro file. A test that pins it: a macro file's top-level `put` runs each time it loads, so its output counts the loads.

*ran: Add a test that a macro file loads once*

Checking that the test means something: `boot/99`'s `bin`, without the cache, on the same files:

*ran: Count the loads with and without the cache*

*ran: Write the test's files and count the loads with each translator*

Three loads before, one now. Updating the spec's "once per importer", then rebuilding and checking everything:

*ran: Update the spec, rebuild bin, run everything, compare with boot/99*

*ran: Update the spec, rebuild bin, run the suite and checkers*

`self_host.py` didn't write `bin`: the translated translator fails `mypy --strict`. Seeing why:

*ran: Run mypy on T1*

B184 (a fold from an empty start fails mypy) again: the fold's start `(Tup empty-list ex)` is typed by its shape, `tuple[()]`. The usual fix, a typed empty list:

*ran: Start the fold from a typed empty list, rebuild, mypy T1*

*ran: Rebuild bin, run the suite and checkers*

*ran: Clear the comparison's scratch folders*

*ran: Compare with boot/99 and time the translator*

Everything passes and the 108 programs agree with `boot/99`. Writing 4b's notes, B63 and B228 to review:

*ran: Write 4b's notes and move B63 and B228 to review*

*(The context was summarised here; the turns before it are above.)*

## Claude Code

*ran: Check B228's long line*

Step 4b is built: each macro file now loads once per translation, however many modules import it. Nothing is committed. All 859 tests pass, the checkers are clean, and `boot/99`'s `bin` gives the same output for all 108 programs.

- **How:** the expander keeps the macro files it has loaded so far. Expansion now passes it from module to module (`expand-modules` folds over the modules instead of mapping), so a second importer reuses the file it already loaded. That is safe because a macro file's expansion doesn't depend on who imports it.
- **Gain:** a program of eight modules sharing one macro file translates in 0.15 s instead of 0.20 s. Translating the translator itself is unchanged, at 1.06 s, since it has no macro files.
- **Test:** `test_macro_file_loads_once` uses a macro file whose top-level `put` runs each time it loads. With the same files, `boot/99`'s `bin` writes the line three times and the new one once.
- **A mypy failure on the way:** the new fold started from an empty list, which mypy typed as an empty tuple. It's the same problem as B184 (a fold from an empty start fails mypy). I fixed it the usual way, with a typed empty list, `NO_READY`.
- **Docs:**
  - The spec's `macros.import-macros` now says once per translation, not once per importer.
  - The HLD has 4b's *Done* note.
  - B63 (a macro file is compiled once per file that imports it) and B228 (host-macros step 4) are in review.

On "gawc" I'll commit 4b and tag `boot/100`. Step 5 is next: hygiene for built-ins.

## Owner

> "Translating the translator itself is unchanged, at 1.06 s, since it has no macro file".... ?

## Claude Code

*ran: Check whether the translator imports or defines macros*

*ran: Find top-level macro imports and defmacros in the translator*

You're right to question it. It was loosely worded and partly wrong. The translator does use macros: `cond` and `put` appear throughout it, and both come from `prelude_macros.cdy`, which every file gets.

The real reason its time didn't change is that `prelude_macros.cdy` was already loaded only once before 4b. The expander loads it once when it's created and every file starts from that copy (`new-expander`, `expand.cdy`). Apart from that, none of the translator's modules has an `import-macros` or a `defmacro` of its own. The only top-level `defmacro`s under `src/cdy/` are in `prelude_macros.cdy` and `test_macros.cdy`, and the translator imports neither by `import-macros`. So 4b had nothing new to share there.

The corrected sentence: "Translating the translator itself is unchanged, at 1.06 s: its only macro file is the prelude's, which was already loaded once per translation." I'll put that wording in the commit message too; the HLD's *Done* note doesn't make the claim. 4b is still waiting for "gawc".

## Owner

> Gawc

## Claude Code

*ran: Commit 4b, check its bootstrap step and tag boot/100*

Step 4b is committed as `4d927cc` and tagged `boot/100`. `bootstrap.py --step` passed with no staging, the tag is annotated, and the tree is clean.

The commit message has the corrected wording: the translator's only macro file is the prelude's, which was already loaded once per translation.

Next is step 5, hygiene for built-ins. Nothing is pushed: `host-macros` and `boot/96` to `boot/100` are local only. Say "go" for step 5.

## Owner

> go

## Claude Code

*ran: Read the HLD's step 5 and the hygiene sections*

*ran: Read the hygiene design, B46 and the spec's for-now*

*ran: Read the shadowing rule, quasi in core.cdy and the prelude macros*

*ran: Read Entry, Scope and quasi-form*

*ran: Find how core resolves a symbol*

*ran: Read resolve, global-of and is-everyones*

Hygiene goes in `quasi-form` in `core.cdy`. When a template symbol names a `system` built-in or a prelude value, as the macro's own module sees it, it gets quoted qualified. Writing it:

*ran: Check entry-module, a prelude constant and quoted*

*ran: Read quoted and find where the prelude's name is spelled*

*ran: Qualify a template's built-in and prelude names, rebuild, try a program with its own text*

Nested patterns aren't supported in `match`. Rewriting with a plain test:

*ran: Rewrite without a nested pattern, rebuild, try again*

`put` now uses `system.text` even when the file defines its own `text`. Checking a prelude name, and that a macro's own helper stays unqualified:

*ran: Try a prelude name in a template, and a file's own macro*

The prelude case works, but a file's own `defmacro` left `len` unqualified. Seeing what the macro code's table has for `len`:

*ran: Read load-own-macros*

The macro code imports `string` with an empty name list, so `len` has an `Unlisted` entry, which gives way to the built-in. Hygiene should treat it, and `Elsewhere`, as no entry:

*ran: Let Unlisted and Elsewhere entries give way, rebuild, retry both*

Both cases work. Now the spec: `programs.shadowing` loses its *for now*, and the quoting rule gets the hygiene rule and an example.

*ran: List the macro rules and mentions of B46*

*ran: Read the quoting and gensym rules*

*ran: Specify hygiene in the spec and run those spec files*

The error's real wording is clearer than my guess. Using it:

*ran: Fix the error row and rerun*

Rebuilding `bin`, then the suite, the checkers and the comparison with `boot/100`. The translated Python should be the same, since a qualified built-in is spelled as the bare one:

*ran: Rebuild bin, run the suite and checkers*

*ran: Clear the comparison's scratch folders*

*ran: See why the boot tag test fails*

`boot/100` is the first three-digit tag, and this test sorts the tag names as strings. Reading it:

*ran: Read the tag test and how bootstrap.py names and lists tags*

*ran: Read tagged_steps*

*ran: Sort the boot tags by number and rerun the bootstrap tests*

The chain lists in order now, `boot/100` last. Comparing with `boot/100`'s `bin`:

*ran: Compare with boot/100, time it, recheck the script*

The one difference is the new spec example, which `boot/100`'s `bin` gets wrong, as expected. Both timings are higher than before, so it's the machine. Retiming a few times:

*ran: Time the translator three times with each bin*

*ran: Write step 5's notes and backlog notes, and check*

Step 5 is built: a macro template now quotes built-in and prelude names qualified, so a file's own `text` no longer changes what `put` calls. Nothing is committed. All 862 tests pass and the checkers are clean.

**How it works** (`core.cdy`'s `hygienic`, called on each symbol in a `quasi` template), judged by what the macro's own module sees:
- **A built-in every file sees** is written qualified: `text` becomes `system.text`, `++` becomes `system.++`.
- **A prelude value** is written qualified: `rest` becomes `prelude.rest`.
- **Everything else stays as written:** a name the macro's module defines or imports, a special form, a macro, a type and a variant.
- **One wrinkle I hit:** macro code imports `string` with an empty name list, which leaves `len` with a "qualified-only" entry. That entry gives way to the built-in, as it does everywhere else, so `len` is qualified too.

**Spec:**
- **New rule, `macros.hygiene`:** with an example where a file's own `len` and `text` don't change a macro's `len` or `put`.
- **Its error row:** a template that binds `len` now binds `system.len`, which is an error (`gensym` is the way).
- **`programs.shadowing`:** its *for now* about `put` and `text` is gone.

**Checks:**
- **Same output:** a qualified built-in is spelled in Python as the bare one, so against `boot/100`'s `bin` 108 of 109 programs translate the same. The one that differs is the new example, which the old `bin` gets wrong, as it should.
- **Speed:** translating the translator takes the same time under both, about 1.21 s. The machine is slower today than when I measured 1.06 s.

**A fix on the way:** `boot/100` is the first three-digit tag. `script/bootstrap.py` listed the tags in git's name order, which puts `boot/100` after `boot/10`, so `test_tags_cover_the_steps` failed. It now sorts them by number. The tags themselves were fine.

**Backlog:** B229 (host-macros step 5) is in review. B46 (macro templates aren't hygienic across modules) stays open with a note: a template that calls a macro file's own helper still needs that helper where the macro is used.

On "gawc" I'll commit step 5 and tag `boot/101`. Step 6 is next: dropping `load-macros`, which needs `old-runtime` staging.

## Owner

> go

## Claude Code

"Go" isn't "gawc", so I haven't committed step 5. It's still uncommitted in the tree, waiting to be tagged `boot/101`.

Step 6 needs its own commit, because it's the staged one (`old-runtime`). It drops `load-macros` from the runtime, which the `bin` before it still calls. If I build it on top of an uncommitted step 5, both land in one staged commit with one boot tag, and step 5's harmless change would get tangled with step 6's staging.

I recommend committing step 5 first as `boot/101`, then building step 6. Say "gawc, go" and I'll do both. Or say "go" again and I'll start step 6 on top of the uncommitted step 5, and keep the two apart when we commit.

## Owner

> gawc

## Claude Code

*ran: Commit step 5, check its bootstrap step and tag boot/101*

Step 5 is committed as `c2e1bc5` ("host-macros step 5: hygiene for built-ins") and tagged `boot/101`. `bootstrap.py --step` passed with no staging, the tag is annotated, and the tree is clean.

The commit includes the fix to `script/bootstrap.py`, so the boot tags now sort by number.

Next is step 6, which drops `load-macros` and needs `old-runtime` staging. Say "go" to start it. Not pushed: `host-macros` and `boot/96` to `boot/101` are local only.

## Owner

> go

## Claude Code

*ran: Find every use of load-macros and call-macro*

*ran: Read the runtime's macro primitives, the HLD on the reset, translator.cdy and B41, B70, B49*

Step 6 removes a runtime function the current `bin` calls, so first I'm checking how an earlier `old-runtime` step rebuilt `bin`:

*ran: See how old-runtime staging works and how bin was rebuilt before*

*ran: Read how old-runtime staging runs, and the last old-runtime step*

*ran: See how self_host.py can start from another translator*

*ran: Read the bridge and self_host's build functions*

*ran: Read the translator spellings and the spec's account of them*

*ran: Add restart-fresh-names and use it in place of load-macros*

*ran: Find where the five translator built-ins are listed*

*ran: Update CLAUDE.md's count and build T1*

*ran: Put the new library next to bin, rebuild bin, check what it calls*

*ran: Rebuild bin and show its output*

mypy rejects binding the result of a function that returns `None`. Calling it in a `do` instead:

*ran: Call the restart in a do, rebuild bin*

`bin` now calls `restart_fresh_names` and no longer calls `load_macros`. Adding a runtime test, then the suite:

*ran: Read test_primitives' imports and the load_macros test*

*ran: Test restart_fresh_names and run the suite*

*ran: Sort the imports, run the suite and checkers*

*ran: Clear the comparison's scratch folders*

*ran: Compare every program's translation with boot/101's bin*

All 109 programs translate the same. Writing 6a's notes:

*ran: Read step 6 and the staging passages in the HLD*

*ran: Write 6a's note in the HLD*

*ran: Note the split in the HLD's Bootstrap section, and check*

Step 6a is built and nothing is committed. All 862 tests pass, the checkers are clean, and `boot/101`'s `bin` gives the same output for all 109 programs.

**Why step 6 is two commits:** the plan was one commit with `old-runtime` staging, but that can't work. In the bootstrap's step tree, the old `bin` reads the step's new `translator.cdy` and checks it against its own runtime's `spelling.py`. The new built-in has no spelling there, so the check stops with "declared in none of ...". Split in two, neither half needs staging:
- **6a (now)** adds the built-in and uses it, and keeps `load-macros`. The old `bin` still calls `load-macros`, and the runtime still has it. The suite's `test_newest_step_reads_the_library` runs exactly this case (`boot/101` with today's library and runtime) and passes.
- **6b (next)** drops `load-macros`, which the 6a `bin` no longer calls.

**What 6a changes:**
- **The new built-in:** `translator.restart-fresh-names`, of type `(Fn (Unit) Unit)`, is the runtime's `restart_fresh_names`. It restarts `gensym`'s count.
- **Its caller:** `cdyc.cdy`'s `load-macro-tops` calls it in a `do`, where it used to call `load-macros` with no Python. A `let` binding didn't work: mypy rejects binding the result of a call that returns `None`.
- **The translator's built-ins** are six until 6b. The spec's `library.builtins` and `programs.shadowing` and CLAUDE.md say so.
- **`test_fresh_name`** restarts the count with the new built-in.
- **`bin/py/translator.cdy`** changes too. The checked-in `bin` reads the library copies next to it, so I copied the new library there before rebuilding. That's what the bootstrap's step tree has anyway.

**Docs:** the HLD has 6a's note, and its Bootstrap section says step 6 was built as two unstaged commits. B230 (host-macros step 6) stays open until 6b.

On "gawc" I'll commit 6a and tag `boot/102`. 6b is next:
- **Out:** `load-macros` from `translator.cdy`, `spelling.py` and `primitives.py`.
- **Closes:** B41 (macros run with Python's `exec`) and B70 (`load-macros` finds `form.cdy`'s names from a Python name).
- **Narrows:** B49 (host objects have no Candy type) to `module-dir`.
- **History:** `macros.md`'s account of `exec` gets marked as history.

## Owner

> Gawc

## Claude Code

*ran: Commit 6a, check its bootstrap step and tag boot/102*

Step 6a is committed as `450505d` and tagged `boot/102`. `bootstrap.py --step` passed with no staging, so the split worked. The tag is annotated and the tree is clean.

6b is next: it drops `load-macros`, closes B41 (macros run with Python's `exec`) and B70 (`load-macros` finds `form.cdy`'s names from a Python name), and narrows B49 (host objects have no Candy type) to `module-dir`. Say "go" for it. Nothing is pushed: `host-macros` and `boot/96` to `boot/102` are local only.

## Owner

> Go

## Claude Code

*ran: Drop load-macros from the runtime, its spelling and its declaration*

*ran: Read the load_macros test's fixtures*

*ran: Drop the load_macros test, and find what still names it*

*ran: Read the passages that list load-macros*

*ran: Update the spec and CLAUDE.md, rebuild bin*

Rebuilding `bin`; it reads its old library copy first, so I'm copying the new library next to it, as for 6a:

*ran: Put the new library next to bin, rebuild, run the suite and checkers*

*ran: Clear the comparison's scratch folders*

*ran: Compare with boot/102, and check the runtime's leftover imports*

`bin`'s Python doesn't change: dropping a declaration changes nothing it emits. All 109 programs agree with `boot/102`. Now the docs. First, `macros.md`'s account of `exec`:

*ran: Read macros.md's header and its load-macros sections*

*ran: Mark macros.md's exec account as history*

*ran: Move B41, B70 and B230 to review, narrow B49, write 6b's note*

*ran: Check whether any long line is one I added*

*ran: Rewrap B49's note*

Step 6b is built: `load-macros` is gone, so macro code no longer touches Python's `exec` anywhere. Nothing is committed. All 861 tests pass, the checkers are clean, and `boot/102`'s `bin` gives the same output for all 109 programs.

**What's out:**
- **The declaration:** `load-macros` from `translator.cdy`.
- **The runtime:** its spelling from `spelling.py`, and `load_macros` from `primitives.py`.
- **Its test:** `test_load_macros` and its fixtures.

**What doesn't change:** `bin`'s Python is the same as 6a's, because removing a declaration changes no Python. As in 6a, I copied the new library next to `bin` before rebuilding. 6b needs no staging, since 6a's `bin` never calls `load-macros`.

**Docs:**
- **Built-in lists:** the translator has five built-ins again: `py-spellings`, `call-macro`, `module-dir`, `fresh-name` and `restart-fresh-names`. The spec's two lists and CLAUDE.md say so.
- **CLAUDE.md's "Macros":** now says how macros run: analysed and checked, macro files as modules loaded once, run on the interpreter, and built-in names hygienic.
- **`macros.md`:** its account of how `load-macros` ran macro code, and its rejection of an interpreter, are marked as history and kept as built.

**Backlog:**
- **To review:** B41 (macros run with Python's `exec`), B70 (`load-macros` finds `form.cdy`'s names from a Python name) and B230 (host-macros step 6).
- **Narrowed:** B49 (host objects have no Candy type) now covers only `module-dir`, the one translator built-in still typed `Any`. Its old text is kept in a note.

On "gawc" I'll commit 6b and tag `boot/103`. Then step 7, the docs, closes the branch.

## Owner

> Gawc

## Claude Code

*ran: Commit 6b, check its bootstrap step and tag boot/103*

Step 6b is committed as `5f9f61a` ("host-macros step 6b: load-macros dropped") and tagged `boot/103`. `bootstrap.py --step` passed with no staging, the tag is annotated, and the tree is clean. Step 6 is complete, and macro code no longer depends on Python's `exec`.

Step 7, the docs, is last. It covers:
- CLAUDE.md's "Macros" and "The interpreter".
- `modules.md`'s "Macro modules on the host".
- The epic marking its seventh branch *done*.
- The HLD's "Looking back".

After that, merging into `master` needs a `pytest -m bootstrap` run and your "gawc". Say "go" for step 7. Nothing is pushed: `host-macros` and `boot/96` to `boot/103` are local only.

## Owner

> Go

## Claude Code

*ran: Read the HLD's top and sections, and B231*

*ran: Read interpreter.md's Looking back and status, modules.md's section and the epic*

*ran: Read the epic's branch list and its table rows for this branch's items*

*ran: Read CLAUDE.md's interpreter bullet and the history's last sentence*

*ran: Read the start of modules.md's After-the-MVP list*

*ran: Read the epic's macro rows, status, and CLAUDE.md's file list*

*ran: Check CLAUDE.md's file list wording, and read B64 and B61*

Writing step 7's docs: the HLD's status and "Looking back", the epic's seventh branch *done*, `modules.md`, and CLAUDE.md.

*ran: Write step 7's docs and move B231 to review*

Checking two numbers I wrote in "Looking back" against the code:

*ran: Count the bridge's lines and the items this branch fixed*

*ran: Correct the counts and run the suite*

Step 7 is written: only docs changed, nothing is committed, and all 861 tests pass.

- **The HLD** (`host_macros.md`):
  - Its status says steps 1 to 7 are built, to review.
  - Step 7 has its *Done* note.
  - There's a new "Looking back" with six lessons:
    - the interpreter found a second user;
    - checking macro code found two old slips;
    - a cache needs a value passed along;
    - hygiene is about where a name is looked up;
    - plan staging, then check it;
    - `boot/100` sorted after `boot/10`.
- **The epic** (`python_complete.md`): its seventh branch is marked *done*. Its table marks each of this branch's items:
  - **Done:** B41, B42, B45, B52, B63 and B70.
  - **Narrowed:** B46 (built-ins done, a macro file's helpers later) and B49 (`module-dir` only).
  - **Left:** B43, B61 and B64.
- **`modules.md`:** "Macro modules on the host" is marked done. The hygiene item says what remains open: a plain `import` bringing `defmacro`s, and a template's calls of a macro file's helpers.
- **CLAUDE.md:**
  - The file list includes `interp_macros.cdy`.
  - "The interpreter" says it runs macro code too, and how.
  - The history has a sentence for the seventh branch.
- **Backlog:** B231 (host-macros step 7) is in review.

In "Looking back" I first wrote that the bridge was about 60 lines and closed six items. Counting showed 67 lines and seven items (B41, B42, B45, B52, B63, B70 and B197), so it now says "under 70" and "seven".

On "gawc" I'll commit step 7. It has no boot tag, since `bin` doesn't change. After that, merging into `master` needs:
- your review and ticks of the items in review (B225 to B231, B41, B42, B45, B52, B63, B70 and B197);
- the chat archived to `doc/archive/`;
- a `pytest -m bootstrap` run;
- the merge itself and the `host-macros` tag, which need another "gawc".

## Owner

> Gawc

## Claude Code

*ran: Commit step 7*

Step 7 is committed as `ad4571b` ("host-macros step 7: docs"), with no boot tag since `bin` didn't change. The tree is clean, and all seven steps of `host-macros` are built.

Before the merge into `master`:
1. **Review:** these items are in review, waiting for your "tick":
   - B225–B231: the step tasks.
   - B41: macros run with Python's `exec`.
   - B42: a macro's result isn't checked.
   - B45: macro files use inclusion.
   - B52: macro code has no prelude.
   - B63: a macro file is compiled once per file that imports it.
   - B70: `load-macros` finds `form.cdy`'s names from a Python name.
   - B197: the built-ins' module, and macro code's.
2. **Archive:** the branch's chat to `doc/archive/`, scrubbed for tokens.
3. **Check:** a `pytest -m bootstrap` run.
4. **Merge:** with a `--no-ff` merge commit and the annotated `host-macros` tag, which needs your "gawc".

Nothing is pushed: `host-macros` and `boot/96` to `boot/103` are local only.

## Owner

> Tick all

## Claude Code

*ran: Tick every item in review*

*ran: Check what branch fixed B62 and B66*

I ticked all 16 items that were in review, not the 14 I'd listed. All 16 are now `done`, each with "the owner: ticked in review" noted. The backlog index is rewritten and its checks pass.

The two I hadn't listed were left in review by the `stdlib` branch, fixed on 2026-11-19:
- B62 (every module compiles the prelude's macros)
- B66 (`special.cdy` and `system.cdy` are read for every translation)

"Tick all" covered them too. Say so if you'd rather review those two first, and I'll put them back.

The ticks aren't committed yet. Next is the merge preparation:
- archive the branch's chat to `doc/archive/`, scrubbed for tokens;
- run `pytest -m bootstrap`.

I'll commit the ticks and the archive together on your "gawc". The merge and the `host-macros` tag need another "gawc" after that.

## Owner

> Gawc

## Claude Code

I'll do the archive first, so the ticks and the archive go in one commit as I said. Checking how the last branch's archive was made:

*ran: Read chat_archive.py's usage and the last archive's commit*

*ran: See how the interpreter chat was archived*

*ran: See what --since and --until match*

*ran: Read chat_archive.py's selection*

The script takes one branch, and the HLD was drafted on `master` before the branch existed. Finding where this branch's chat starts:

*ran: List the owner's messages since the interpreter merge, with branch and time*
