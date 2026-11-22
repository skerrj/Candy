*Archived 2026-11-21, late, after the merge (it was missed before it), from the Claude
Code session that built branch `library-layers` (2026-11-15 to 2026-11-17; HLD
`doc/hl_rqmt/library_layers.md`, tag `library-layers`), by `script/chat_archive.py`.*
The owner's messages and Claude's replies on the branch, verbatim; each tool call is a
one-line marker, and thinking and tool output are left out. A notice of a background job
finishing, which the harness writes as the owner's turn, is left out. What came of it: a
library module found by name ([[B199]]); declaration modules, and `translator.cdy`
([[B200]], [[B50]]); the built-ins a module, `system` ([[B201]], [[B196]]); 14 built-ins
dropped, 75 left ([[B202]], [[B32]]); `slurp` without a search ([[B203]], [[B54]]); each
built-in specified ([[B204]]); [[B198]] (re-export) dropped; and "Looking back".

# library-layers

## Claude Code

*ran: Read include.cdy's module loading*

*ran: Read import-path and how the library is copied*

*ran: Add the library directory to import's lookup*

*ran: Read programs.import and the import error test*

*ran: Survey form.cdy's names and an example program*

*ran: Write the library module example and run it with T1*

T1 runs it and prints what `library_module.out` expects. Now the rule, and the error messages in the spec and the tests:

*ran: Write the library module rule and update the error texts*

`macros.import-macros` already says it finds a file "as `import` does", so it needs no change. Now the edge cases: a program importing the library's own files.

*ran: Try importing each library file from a program*

*ran: Make the library's non-module files a plain error*

*ran: Show the current programs.import text*

*ran: Write the rule's text and the new errors into the spec*

*ran: Show the paragraph to rewrap*

*edited: `spec/10-programs.md`*

*ran: Rebuild bin and run the full test suite*

*ran: Time translations with the full prelude and an empty one*

*ran: Profile one translation by phase*

*ran: Read the comparison script's usage*

*ran: Compare the Python output with boot/76's bin*

The output matches `boot/76`'s `bin` for 98 of 99 programs. The only difference is the new example, which `boot/76` can't find. Now the linters, then the notes:

*ran: Run the linters and show the changed files*

*ran: Write step 1's Done note and the backlog notes*

*ran: Rewrap the HLD's status line*

Step 1, B199 (library-layers step 1: a library module, found by name), is built and in `review`. Nothing is committed, and it needs no staging.

All checks pass: the full `pytest` (694 passed, 4 xfailed), `ruff check`, `ruff format --check`, `mypy`, `pyright` and `pylint`. `bin` is rebuilt. Against `boot/76`'s `bin`, 98 of 99 programs give the same Python; the other is the new example, which the old `bin` can't find.

**What changed:**
- **The lookup:** `import-path` (`src/cdy/include.cdy:207`) tries the importing file's directory first, then the library directory next to the translator. `import-macros` goes through the same function, so it gets the library too.
- **The error:** a missing module now gives "can't find nope.cdy in . or the library".
- **Two library files aren't modules:** `special` and `prelude_macros` are listed in `NOT_MODULES`, and importing them gives "special is the translator's, not a module" (or the same for `prelude_macros`).
- **What else imports:** `(import prelude)` works. `(import system)` still fails on its bodiless `deft`s until steps 2 and 3.
- **The spec:** [[programs.import]] states the lookup, *lasting*, with the two new errors (`spec/10-programs.md:235`).
- **The example:** `tst/cdy/cdyc/library_module.cdy` (new) imports the library's `form`. `form` is the only library file that is an ordinary module today.

**The prelude's costs (Question 7):** they're recorded in the HLD's step 1 *Done* note, and as notes on B66, B62 and B68. In order of size:
- **B66 (`special.cdy` and `system.cdy` read for every translation):** the biggest. Reading them is 62% of the time for `modules.cdy`, a four-module translation, because they're read 11 times: per module and per macro program.
- **B62 (every module compiles the prelude's macros):** 39%. That overlaps the above, since each macro program reads the built-ins again.
- **B68 (the whole prelude goes into every program):** small in time, about 5 ms (2%), but it adds 49 lines to every program's Python: `(put 1)` gives 80 lines, against 31 without the prelude.

You decided these get fixed in `stdlib`. B66 is mostly a matter of reading the files once per translation, so it may be cheap enough to do here, but I've left it to `stdlib` as decided.

"Tick, gawc" ticks and commits step 1. Step 2 then makes declaration modules and moves the translator's five into `host.cdy` (staged).

## Owner

> Tick, gawc

## Claude Code

*ran: Tick B199 and check the tree*

*ran: Commit step 1 and tag its boot step*

*ran: Find how built-ins are read and bodiless sigs rejected*

*ran: Read read-builtins and the spelling check*

*ran: Read Entry and how built-in references appear in Core*

*ran: Read name resolution and analyse-program*

*ran: Read the bootstrap staging mechanism*

Before building step 2 I need a decision from you: as the HLD stands, the translator can't import `host.cdy` from its own source.

**The problem.** The translator's modules live in `src/cdy/`, and `host.cdy` will sit there with them. With the local file first (your Question 3 answer), `(import host)` in `cdyc.cdy` finds `src/cdy/host.cdy` as one of the program's own files. A program's file can't declare built-ins (Question 4), so the translator could only import its own `host` by breaking one of those two rules.

**Options:**
1. **A declaration module always comes from the library (recommended).** `(import host)` and, from step 3, `system` find the library's file even if the program has one with the same name. The local-first rule still holds for ordinary library modules (`form`, and `string` and the rest later). This fits Question 4 well: a target's declarations can't be replaced by a program. When the translator compiles itself, it gets the library's copy of `host.cdy`, which is the same file as `src/cdy/host.cdy`.
2. **Recognise a declaration module by its stem** (`host`, `system`) wherever the file is. This is simpler, but a program could write its own `host.cdy` and reach `load-macros` again, which defeats B50 (the translator's five host built-ins are every program's).
3. **The translator's sources count as library modules,** a special case for the translator. This is murkier, and the bootstrap still needs staging.

**Option 1 also avoids staging,** at the cost of two commits for this step. The step would be built in two parts:
- **2a:** declaration modules, the library-first rule and an empty `host.cdy`. Its `bin` gets `boot/78`.
- **2b:** the five move into `host.cdy` and the translator imports `host`. When 2a's `bin` compiles 2b's source, `(import host)` finds `bin`'s own, empty `host.cdy`, so the five still come from `bin`'s `system.cdy`. No new staging kind is needed.

Done in one commit, the step would need a new staging kind (the source with its `(import host)` lines removed). That keeps one commit per step but adds bootstrap code.

**One more detail:** which library files are declaration modules will be a fixed list, `system` and `host`, *for now*. The runtime has no directory listing.

My recommendation: **option 1, with step 2 as two commits (2a, 2b).** Shall I go ahead?

*(The context was summarised here; the turns before it are above.)*

## Owner

> First question, why does `host.cdy` have to live in `src/cdy`?

## Claude Code

*ran: `ls src/cdy && grep -n "LIBRARY\|src/cdy\|CDY_DIR\|SRC" src/py_cdy/self_host.py |`*

*ran: `grep -n "src/cdy\|CDY_DIR\|LIBRARY\|library" script/bootstrap.py | head -30`*

It doesn't have to. It would be there only because every library file's source is there today: `self_host.py:38` copies `LIBRARY` out of `CDY_DIR` (`src/cdy/`, `self_host.py:30,80`). That's just how it grew. I took that layout for granted, and that's what created the problem.

**The prelude already works the other way.** `prelude-module` (`include.cdy:53`) finds the prelude through `library-path`, never locally. So when `bin` compiles `src/cdy/`, the prelude its modules import is `bin/py/prelude.cdy`, the copy next to the translator doing the compiling. `src/cdy/prelude.cdy` is only the source that gets copied into the next translator's library. `host.cdy` can follow that pattern exactly.

**So the better fix is a separate source directory for the library,** say `src/lib/`, holding `host.cdy` (and later `special`, `system`, `prelude` and `prelude_macros` too):
- **The translator finds it in the library.** `(import host)` in `cdyc.cdy` finds no `src/cdy/host.cdy`, so it falls through to the library: `bin/py/host.cdy` when `bin` builds T1, and `output/t1/host.cdy` when T1 builds T2. The two answers stay as they are: it's a library module, so it may declare built-ins (Question 4), and the local file still comes first (Question 3), unchanged.
- **Option 1's special rule isn't needed.** If a program has its own `host.cdy`, that file is an ordinary module and can't declare anything. The program loses the host built-ins but gains nothing, so B50 isn't weakened.
- **`self_host.py` copies from the new directory.** `bootstrap.py` builds each step with that step's own `self_host.py` (`bootstrap.py:31-34`), so older commits keep their own layout.
- **`form.cdy` stays in `src/cdy/`,** because it's one of the translator's modules and must be compiled from source. It's also copied into the library, as now.

**The bootstrap still needs a step.** `bin` at `boot/77` has no `host.cdy`, so `(import host)` would fail with "can't find host.cdy in … or the library". Either:
- **two commits:** 2a adds declaration modules and an empty `host.cdy` to the library (giving `boot/78`), then 2b moves the five host built-ins there and the translator starts importing `host`; or
- **one staged commit.**

**My recommendation: put the library's source in `src/lib/` and drop option 1.**
- In this step, move only `host.cdy` there, plus the files it needs to sit beside, if any. The other library files can move in step 7 (docs) or when `stdlib` reorganises the library.
- Build the step as the two commits 2a and 2b, since that needs no new staging kind.

Shall I go ahead on that basis?

## Owner

> Still reading; can you display the latest host.cdy?

## Claude Code

*ran: `ls src/cdy/host.cdy 2>&1 && grep -n -B3 "py-spellings\|load-macros\|call-macro\|`*

There's no `host.cdy` yet. Step 2 hasn't changed any files, so `ls src/cdy/host.cdy` finds nothing. The five host built-ins are still declared in `src/cdy/system.cdy:148-156`:

```
;; --- the spellings, for the translator (each built-in's Python text and kind, and an
;; operator's function as a value) ---
(sig py-spellings (Map String (Tup String String String)))

;; --- macros, for the translator (the macros are Python functions on Forms) ---
(sig load-macros (Fn (String Any (Map String Bool)) (Map String Any)))
(sig call-macro (Fn (Any (List Any) String) Any))
(sig module-dir (Fn (Any) String))
(sig fresh-name (Fn (String) String))
```

Under the plan, `host.cdy` would be those same lines moved out of `system.cdy` with a header comment added. It would start empty in 2a and get the lines in 2b. Here is a draft of 2b's version:

```
;;; host: the built-ins only the translator needs, declared for the host it runs on
;;; (doc/hl_rqmt/library_layers.md). A program sees them only if it imports host;
;;; macro programs see them too, since form.cdy's gensym uses fresh-name.

;; --- the spellings (each built-in's Python text and kind, and an operator's function
;; as a value) ---
(sig py-spellings (Map String (Tup String String String)))

;; --- macros (the macros are Python functions on Forms) ---
(sig load-macros (Fn (String Any (Map String Bool)) (Map String Any)))
(sig call-macro (Fn (Any (List Any) String) Any))

;; --- the translator's own directory, where its library is ---
(sig module-dir (Fn (Any) String))

;; --- a name no program has written, for gensym ---
(sig fresh-name (Fn (String) String))
```

## Owner

> Thanks, was just trying to simply define what is in, or in this case ends up in, `host.cdy`.... Which is... "signatures only, mapping to host defined functions".... Please make this better

## Claude Code

One sentence:

> **`host.cdy` declares the built-ins that only the translator needs: each is a bodiless `sig`, typed in Candy and defined by the runtime it runs on.**

Each phrase earns its place:
- **"declares … each is a bodiless `sig`":** the file has types but no definitions, the same form `system.cdy` uses (like Carp's `register`).
- **"the built-ins":** names the analysis resolves to `Prim`, like `system.cdy`'s, not ordinary functions in a module.
- **"only the translator needs":** this is what separates it from `system.cdy`, whose built-ins every program gets. A program sees `host`'s only if it imports `host`.
- **"defined by the runtime it runs on":** the bodies are host code. For Python that means `cdy_rt`: `spelling.py` gives each one's spelling and `primitives.py` its function. Another target would have its own runtime behind the same `sig`s.

Paired with `system.cdy`, so the two read as a set:

> - `system.cdy`: the built-ins every program gets.
> - `host.cdy`: the built-ins only the translator gets.
>
> Both are declaration modules: `sig`s with no bodies, defined by the runtime.

If you want this wording, I'll use it as `host.cdy`'s header comment and in the HLD.

## Owner

> Sounds good, but since I got so stumped, should we rename it (again?)?

## Claude Code

I think it's worth renaming, and better now, while nothing has been built.

**Why "host" misleads:** every built-in is defined by the host, `system.cdy`'s too. So "host" names what the two files share, not what makes this one different. That's probably why the definition was hard to pin down. The one-line definition shows what does make it different: *only the translator needs it*.

**Options:**
1. **`translator` (recommended).** It matches the definition: `system` is every program's, `translator` is the translator's. The project already calls it the translator (`cdy_translator.py`, "the translator's own" in error texts). `(import translator)` in `cdyc.cdy` reads plainly, and macro programs getting `fresh-name` still fits, since they run inside the translator.
2. **`meta`.** It describes the macro-time side well (`load-macros`, `call-macro`, `fresh-name`) but fits `py-spellings` and `module-dir` less well. It also suggests a general metaprogramming library, which this isn't, *for now*.
3. **`compiler`.** It's familiar from other languages, but Candy says "translator" everywhere, so it would be a second word for the same thing.
4. **Keep `host`.** No churn, but the word stays misleading.

**What changes:**
- Question 5 in `doc/hl_rqmt/library_layers.md` gets a dated note: the answer is revised from `host` to `translator`, with the old answer kept verbatim in a `text` fence.
- B200's (library-layers step 2: declaration modules, and `host.cdy`) title changes accordingly, and so does any mention of `host` in the HLD's step list and B50.
- The `src/lib/` question from before is separate and still open.

My recommendation: **`translator`**. Shall I make the rename in the docs, along with the `src/lib/` decision once you've read that?

## Owner

> Sounds good... This is just an "idea" comment... If we had a metadata map, ala clojure's, for symbols and such, would it be worth it .. tagging "translator only" functions... Defined in `system.cdy`...?

## Claude Code

It's a good idea, but I'd use metadata for something else and keep "who sees what" in modules.

**What a tag in `system.cdy` would give you:**
- All built-in declarations in one file.
- A general mechanism that could later carry other properties: `^:deprecated`, a docstring, `^:pure`, the targets a built-in exists on (useful for `multi_target.md`), a spec rule's id. `(private a b)` could even become `^:private`, as in Clojure.

**Why I'd still use a module for "translator only":**
- **Visibility is what modules are for.** Since `namespaces`, what a file sees is decided by its imports: one table, one rule. A tag would add a second mechanism for the same job.
- **The import shows the dependency where it's used.** `(import translator)` at the top of `cdyc.cdy` says this file uses the translator's built-ins, and a grep finds every file that does. With a tag, a program could use `load-macros` freely, and nothing at the call site would show it's special. The analysis would also need a new rule ("refuse a tagged built-in unless …"), which again is just an import in another form.
- **These built-ins are tied to one target.** `py-spellings` is Python's. When a second target comes, a declaration module per target fits better than tags in one shared file.
- **It's a bigger feature.** It needs reader syntax for `^` (alongside the reader macros planned for `'`), a map on every form and name, and analysis that reads it. That's a branch of its own, not part of this step.

**Where metadata would pay off:** properties that cut across visibility: docs, deprecation, purity, which targets have a built-in, and maybe `private`. Note that `private` is a visibility property, so if it moved to metadata, my "modules decide visibility" argument would need another look.

My suggestion: note it now and decide nothing yet. Shall I add it to `doc/brainstorm.md` (quick, undecided), or write it up as a backlog `idea` that links to `multi_target.md` and `[[programs.private]]`?

## Owner

> Brainstorm... Keep your `translator`solution... Documented as "translator only stuff...."

## Claude Code

*ran: `head -40 doc/brainstorm.md && echo ---- && tail -30 doc/brainstorm.md && echo --`*

*ran: `sed -n 80,100p doc/hl_rqmt/library_layers.md && sed -n 185,200p doc/hl_rqmt/libr`*

*ran: `python3 - <<'EOF'`*

*ran: `sed -n 64,72p doc/hl_rqmt/library_layers.md`*

*ran: `sed -i '68s/'(import host)'/'(import translator)'/' doc/hl_rqmt/library_layers.m`*

I've renamed the declaration module from `host` to `translator` in the docs and added the metadata idea to the brainstorm file. The doc-link and backlog tests pass (46 tests); nothing is committed yet.

- **The HLD (`doc/hl_rqmt/library_layers.md`):**
  - The step 2 section is now headed "The translator's built-ins: `translator.cdy`" (`:83`). It opens with the definition you liked: the built-ins only the translator needs, each a bodiless `sig`, typed in Candy and defined by the runtime it runs on. It pairs `system` (every program's) with `translator` (only the translator's).
  - Every other mention of `host` meaning the module is now `translator`, including `(import translator)` (`:68`) and the step list (`:192`).
  - Question 5 keeps its original answer and gets a dated "*Revised (2026-11-15, the owner): `translator`.*" line, with the reason. It also says the metadata tag was weighed and left to the brainstorm (`:241`).
  - These still say "host" on purpose: `host-macros` (B45), B50's (the translator's five host built-ins are every program's) own title, and phrases like "a host `isinstance`".
- **B200 (library-layers step 2: declaration modules, and `translator.cdy`):** I changed the title, `where` and text, and added a note that keeps the old wording verbatim in a `text` fence. I also rewrote `backlog/README.md`.
- **`doc/brainstorm.md`:** a new **metadata on names** entry. It records that "translator only" stays a module because a file sees what its imports give it. It lists what metadata could carry instead: docs, `deprecated`, `pure`, which targets have a built-in, and maybe `private`.

The HLD still places `translator.cdy` in `src/cdy/`, and `:68` claims `(import translator)` finds the library's file. Both depend on the `src/lib/` question you're still reading: with the file in `src/cdy/`, the translator would find its own copy first, as an ordinary module. I'll fix both once you decide.

## Owner

> Can you put the open questions up again?

## Claude Code

Three questions are open for B200 (library-layers step 2: declaration modules, and `translator.cdy`), and the third only matters if you pick `src/lib/` in the first.

**1. Where does `translator.cdy`'s source live?**
Because the local file comes first, a `translator.cdy` in `src/cdy/` would be found by the translator's own `(import translator)` as an ordinary module. Only library modules may declare built-ins, so it couldn't declare the five.
- **a. A separate library source directory, `src/lib/` (recommended).**
  - The translator finds no local `translator.cdy` and falls through to the library: `bin/py/` when `bin` builds T1, `output/t1/` when T1 builds T2. The prelude already works this way (`include.cdy:53`).
  - It needs no new rule. `self_host.py:38,80` would copy the library from the new directory.
- **b. Keep it in `src/cdy/`, and make a declaration module always come from the library,** even when a local file has the same name. That adds an exception to the local-first rule (Question 3) for `system` and `translator`.

**2. Build the step as one commit or two?**
`bin` at `boot/77` has no `translator.cdy`, so `(import translator)` can't be compiled by it.
- **a. Two commits (recommended).**
  - 2a: declaration modules, plus an empty `translator.cdy` in the library. It gets `boot/78`.
  - 2b: the five move into `translator.cdy`, and the translator imports `translator`.
  - No new bootstrap code.
- **b. One staged commit.** This keeps one commit per step, but needs a new staging kind in `script/bootstrap.py` that compiles the source with its `(import translator)` lines removed.

**3. With `src/lib/`, what moves now?**
- **a. Only `translator.cdy` now (recommended).** `special`, `system`, `prelude` and `prelude_macros` move in step 7 (docs) or in `stdlib`.
- **b. All of them now,** so the layout is consistent from this step on.

In every case, `form.cdy` stays in `src/cdy/`, because it's one of the translator's own modules and must be compiled from its source.

There's also one detail to confirm rather than decide: which library files are declaration modules is a fixed list, `system` and `translator`, *for now*. The runtime has no directory listing.

My recommendation: **1a, 2a, 3a.**

## Owner

> So system is in src/cdy and it's ok why?... A rule...

## Claude Code

`system.cdy` is safe in `src/cdy/` because nothing ever looks it up by name. The rule is:

> **Only an explicit `(import m)` looks for a local file first. Everything the translator reaches by itself, it reads from the library: `library-path` (`include.cdy:66`) looks only next to the translator.**

That covers every library file today:
- `special.cdy` and `system.cdy` are read directly by `read-builtins` (`core.cdy:1068`), through `library-builtins` (`expand.cdy:165`). They're never imported.
- `prelude_macros.cdy` is loaded by the expander. `import-path` refuses it as a module (`NOT_MODULES`, `include.cdy:219`), as it does `special`.
- `prelude.cdy` is imported implicitly, through `library-path` (`include.cdy:53`).

So `src/cdy/system.cdy` and `src/cdy/prelude.cdy` are never found locally. They're only the sources that get copied into the next translator's library.

**What's new with `translator.cdy`:** it's the first library file that the translator's own modules reach through an explicit `(import translator)`. That's the only kind of lookup that checks the local directory first, so this is the first time a file in `src/cdy/` gets in the way.

**Step 3 hits the same case for `system`.** It becomes a module, imported implicitly, so it stays safe. But an explicit `(import system (text))` written in `src/cdy/` would find the local copy.

**This changes how option 1b looks.** "A declaration module always comes from the library" isn't a new exception. It extends the existing rule: what the translator supplies comes from the translator, whether it's reached implicitly or by an explicit import. Both options now hold up:
- **1a (`src/lib/`)** keeps one lookup rule for every explicit import, and fixes the problem by moving files. But a declaration module stays shadowable by a local file of the same name. That's harmless, since a local file can't declare anything.
- **1b (the rule)** leaves the source layout alone. It makes `system` and `translator` names a program can't replace, which fits "a target brings its declarations" (Question 4).

Knowing this, I now lean towards **1b**: the rule is already half there, and it also covers `(import system …)` from step 3 on. `src/lib/` remains a reasonable tidy-up for `stdlib`, but this step doesn't need it.

Question 3 (what moves to `src/lib/`) then drops away, and Question 2 (two commits, recommended) stands as before.

## Owner

> So how many `system` calls are in the translator, I.e. all modules in the translator?

## Claude Code

*ran: `cat > /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e`*

The translator uses 69 of `system.cdy`'s 94 built-ins, with about **2,661 references** across its 10 modules, so every module depends on `system` heavily.

| module | references | distinct built-ins |
|---|---:|---:|
| `core` | 1026 | 41 |
| `check` | 449 | 36 |
| `emit` | 341 | 36 |
| `read` | 324 | 28 |
| `lower` | 175 | 19 |
| `expand` | 134 | 35 |
| `include` | 104 | 32 |
| `syntax` | 60 | 17 |
| `cdyc` | 43 | 23 |
| `form` | 5 | 4 |

These are counted tokens, not parsed calls. A built-in passed as a value, as in `(fold + 0 xs)`, counts too. A local or field with the same name as a built-in also counts; `text` (143) probably includes some. Strings and comments are excluded. The script is `/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/scratchpad/count_sys.py`.

- **Most used:** `=` 364, `at` 251, `len` 246, `++` 188, `fail` 160, `text` 143, `+` 112, `empty-list` 106, `map-has` 91, `and` 84.
- **The translator's five:** 6 uses in all. `py-spellings` has 2 (`cdyc` and `expand`); `load-macros`, `call-macro`, `module-dir` and `fresh-name` have 1 each.
- **The 25 the translator doesn't use:**
  - 10 of the 11 that step 4 drops: `re-search`, `re-findall`, `re-compile`, `is-coll`, `is-str`, `is-alpha`, `is-neg-int`, `strip`, `is-empty-str`, `SYS_ARGS`. `file-put-lines` is the 11th; it doesn't appear in the list, so something in the translator matches its name.
  - 4 that step 4 keeps: `PI`, `sin`, `cos`, `tan`.
  - 11 others: `/`, `mod`, `elem-index`, `ends-with`, `is-digit`, `isspace`, `map-size`, `put-line`, `repeat`, `reverse`.

For the open questions, this means the translator's own modules use the five 6 times and `system` thousands of times. So `system` has to stay implicit, as Question 6 already has it, while `translator` can be an explicit import in the 4 modules that use it.

## Owner

> And there no import statement for system?

## Claude Code

*ran: `grep -rn "(import system\|import-macros system" src/cdy tst spec | head`*

Right, nothing imports `system`, anywhere. A search for `(import system` across `src/cdy`, `tst` and `spec` finds nothing.

Today `system` isn't a module at all, so it isn't even imported implicitly the way the prelude is:
- `read-builtins` (`core.cdy:1068`) reads `system.cdy` (and `special.cdy`) into one flat map, the built-ins.
- `resolve` (`core.cdy:289`) checks that map last, after a file's locals, its own names and its imports. Any name found nowhere else becomes a `Prim`.

So every file sees every built-in with no import statement. Shadowing still works because the map is the last place checked.

That's what step 3 changes: `system` becomes a real module that every file imports implicitly, as it does the prelude, so `system.text` becomes a qualified name. Even then, nobody writes `(import system)`; it stays implicit (Question 6, *for now*).

So `translator` will be the first declaration module anyone imports by name, and the first that four of the translator's modules (`cdyc`, `include`, `expand`, `form`) must import explicitly. That's why the local-copy problem shows up only now.

## Owner

> Going in circles, sorry... Why can't `translator. cdy` (or now I'm thinking "system-internal" might be better) just be implicit like system?

## Claude Code

It could be made implicit, but then the step would no longer fix B50 (the translator's five host built-ins are every program's).

**What B50 is about:** today every program sees `load-macros`, `call-macro`, `py-spellings`, `module-dir` and `fresh-name` without asking, because they're in the implicit `system`. If `translator.cdy` were implicit too, every program would still see them, just declared in another file. The visibility problem stays exactly the same.

**The explicit import is the point.** It doesn't make the five secret: any program can still write `(import translator)`, and the HLD allows that. It makes using them opt-in and visible. A program that uses them shows it at the top of the file, and one that doesn't never sees them.

**Implicit for the translator's own modules only?** Then the translator would need a way to tell its own source apart from a user's program, for example:
- the directory the source is in,
- a command-line flag, or
- "the program being compiled is the translator".

Each of these is a special case, the "murkier" option 3 from before. An explicit `(import translator)` in 4 files costs 4 lines.

So the choice is between explicit (and then where the file lives, 1a or 1b) and implicit (leave the five where they are, in `system`). Implicit only for the translator isn't worth its rule.

**On "system-internal":** "internal" suggests hidden or private, but the module is opt-in, not private: any program can import it. It also makes it sound like part of `system`, when the whole point is that it isn't every program's. `translator` says whose the built-ins are. I'd keep `translator`, but the name is your call.

## Owner

> Tracking now... Thanks, all great points

## Claude Code

The two decisions still open for B200 (library-layers step 2: declaration modules, and `translator.cdy`), with my current recommendations:

1. **Where `translator.cdy` lives:** **1b (recommended).** A declaration module (`system`, `translator`) always comes from the library, even when imported by name. It extends the rule that already covers everything the translator supplies itself. The other option is 1a: a `src/lib/` source directory.
2. **Commits:** **two (recommended).** 2a adds declaration modules and an empty `translator.cdy` (`boot/78`), then 2b moves the five there and adds the imports. The other option is one staged commit with a new staging kind.

Uncommitted so far: the rename to `translator` in `doc/hl_rqmt/library_layers.md`, B200's file, `backlog/README.md`, and the metadata entry in `doc/brainstorm.md`.

Tell me which way you want 1 and 2 to go, and I'll update the HLD to match and start on 2a.

## Owner

> Both of your recommendations

## Claude Code

Recording both decisions in the HLD first, then starting 2a.

*ran: `grep -n "Staged\|staged\|Bootstrap\|^## \|^### " doc/hl_rqmt/library_layers.md |`*

*ran: `sed -n 64,101p doc/hl_rqmt/library_layers.md && sed -n 185,200p doc/hl_rqmt/libr`*

*ran: `tail -25 doc/hl_rqmt/library_layers.md`*

*ran: `python3 - <<'EOF'`*

*ran: `python3 - <<'EOF'`*

Docs updated. Now reading the code for 2a.

*ran: `sed -n 170,215p src/cdy/core.cdy && echo ---- && sed -n 270,320p src/cdy/core.cd`*

*ran: `sed -n 1030,1200p src/cdy/core.cdy`*

*ran: `sed -n 1200,1420p src/cdy/core.cdy`*

*ran: `grep -n "library-builtins\|module-exports\|analyse-module\|analyse-program\|read`*

*ran: `sed -n 1,125p src/cdy/cdyc.cdy && sed -n 150,215p src/cdy/expand.cdy`*

*ran: `grep -n "((Value\|((Record\|((Elsewhere\|((Unlisted\|((Clash\|((Private\|(Value `*

*ran: `sed -n 140,170p src/cdy/core.cdy && sed -n 214,269p src/cdy/core.cdy && sed -n 3`*

*ran: `grep -rn "read-builtins\|read_builtins\|library-builtins\|read-sigs\|all-declare`*

*ran: `sed -n 480,640p tst/py_cdy/test_self_host.py`*

*ran: `grep -n "copy_library" -A8 tst/py_cdy/conftest.py tst/py_cdy/test_self_host.py |`*

*ran: `grep -rn "def copy_library" -A10 tst/ && sed -n 80,100p spec/10-programs.md && s`*

*ran: `grep -rn "def copy_library" -A8 src tst script && sed -n 1,40p src/cdy/system.cd`*

Writing `translator.cdy` and moving the five out of `system.cdy`.

*ran: `cat > src/cdy/translator.cdy <<'EOF'`*

*ran: `python3 - <<'EOF'`*

Now `core.cdy`: the `Declared` entry, `resolve`, and `read-builtins` over several declaration files.

*ran: `python3 - <<'EOF'`*

Now `include.cdy`: declaration modules always come from the library.

*ran: `python3 - <<'EOF'`*

Now `cdyc.cdy` and `library-builtins` in `expand.cdy`.

*ran: `python3 - <<'EOF'`*

Building T1 and the fixpoint.

*ran: `time python src/py_cdy/self_host.py 2>&1 | tail -15`*

The fold-with-`empty-map` mypy issue (B184); passing the start as a parameter, as `qualifiers-of` does.

*ran: `python3 - <<'EOF'`*

Fixpoint reached. Trying the new behaviour by hand.

*ran: `mkdir -p tmp/c7/decl && rm -f *.cdy && cat > a.cdy <<'EOF'`*

*ran: `cat > d.cdy <<'EOF'`*

Both as intended for 2a: `translator` imports work, qualified and listed, and a program's own `translator.cdy` is ignored. Now the tests: updating the library-error messages, and adding cases.

*ran: `sed -n 200,258p tst/py_cdy/test_self_host.py`*

*ran: `python3 - <<'EOF'`*

*ran: `python3 - <<'EOF'`*

Tests pass. Now the spec: `programs.import` gets the declaration-module rule, and `programs.shadowing` and `library` say where the five are now.

*ran: `python3 - <<'EOF'`*

Now the other docs that list the library's files.

*ran: `grep -rln "prelude_macros.cdy" --include=*.md . | grep -v "doc/archive\|^./backl`*

*ran: `sed -n 10,17p bin/README.md && sed -n 82,86p README.md`*

*ran: `python3 - <<'EOF'`*

Now the HLD: 2a's refined content, and its Done note.

*ran: `python3 - <<'EOF'`*

*ran: `python3 - <<'EOF'`*

*ran: `pytest -q tst/py_cdy/test_bootstrap.py::test_newest_step_reads_the_library 2>&1 `*

*ran: `sed -n 1,40p tst/py_cdy/test_bootstrap.py | grep -n "import" && sed -n 155,180p `*

`old-library` puts the parent's own `bin/*/*.cdy` next to it, which is exactly how `self_host.py` just built 2a successfully. Fixing the test to skip library files the old commit doesn't have:

*edited: `tst/py_cdy/test_bootstrap.py`*

*ran: `pytest -q tst/py_cdy/test_bootstrap.py 2>&1 | tail -6`*

As expected: `old-library` for the next step. Checking how `--tag` records it:

*ran: `grep -n "staging:\|--tag\|def tag\|--staging" script/bootstrap.py | head -20`*

*ran: `sed -n 255,282p script/bootstrap.py && sed -n 55,70p script/bootstrap.py`*

`STAGING` is keyed by commit hash, so at commit time I'll add 2a's hash to it, run `--tag`, and the tag will record `staging: old-library`. Fixing the Done note, then the full checks.

*ran: `python3 - <<'EOF'`*

*ran: `ruff check src tst script && ruff format --check src tst script && mypy src/py_c`*

*ran: `pylint src/py_cdy src/cdy_rt tst script 2>&1 | grep -v "^\*\|^$\|rated" | head`*

*ran: `sed -n 620,628p tst/py_cdy/test_self_host.py`*

*ran: `python3 - <<'EOF'`*

All checks clean. Now comparing against `boot/77`'s output with `tmp/c7/cmp3.py`.

*ran: `head -30 tmp/c7/cmp3.py`*

*ran: `rm -rf tmp/c7/sp3/* tmp/c7/b72/bin && git archive refs/tags/boot/77 bin | tar -x`*

Every program gives the same Python as with `boot/77`, including the translator itself (99 programs, 0 differ). A last check of the changed files:

*ran: `git status --short && git diff --name-only | xargs grep -lE "github_pat_|ghp_" &`*

Step 2a of B200 (library-layers step 2: declaration modules, and `translator.cdy`) is built and passes every check, but it differs from what you approved in two ways.

**The two differences:**
- **2a already moves the five into `translator.cdy`, instead of adding an empty file.** Every program still sees them until 2b, so nothing changes for programs. Moving them now means the new mechanism is tested in this commit. 2b then only hides them: the translator's modules import `translator`, and macro programs get it.
- **2a needs staging after all, of the existing `old-library` kind.** The bootstrap check runs the newest `boot` translator next to *today's* library, and 2a's `system.cdy` no longer has the five that 77's source calls. `old-library` gives it its own library instead, which is exactly how `self_host.py` built 2a. It's the kind used twice before, so no new bootstrap code. 2b won't need staging.
  - If you'd rather 2a have no staging at all, the alternative is an empty `translator.cdy` in 2a. Then 2a's new mechanism goes untested until 2b.

**What's in 2a:**
- **`src/cdy/translator.cdy` (new):** the five bodiless `sig`s, with the header comment you agreed on. It's added to `LIBRARY` in `self_host.py:38`, and `system.cdy` loses the five.
- **`include.cdy:221`:** `DECLARATION_MODULES` lists `translator`; `system` joins in step 3.
  - `import-path` finds a declaration module in the library before looking anywhere else.
  - `is-declaration` recognises the library's copy by its path, so a top file named `translator.cdy` stays an ordinary module.
  - A declaration module doesn't import the prelude.
- **`core.cdy`:**
  - A new `Entry` kind, `Declared` (`:185`), which `resolve` makes a `Prim` (`:306`). An import's name list, `translator.x` and the namespace errors all work for it, with no extra code.
  - `declared-exports` (`:1232`) builds what the declaration module offers its importers.
  - `read-builtins` (`:1084`) and `read-sigs` (`:1161`) now take several declaration files, and their errors name the file. Only `system.cdy` may declare types, *for now*.
- **`cdyc.cdy`:** `expand-modules` gives a declaration module no definitions, only what it declares. **`expand.cdy`:** `library-builtins` reads every declaration file.
- **Tests:**
  - `test_module_errors` gets three new cases, including the one where a program's own `translator.cdy` is ignored.
  - `test_library_errors` gets four new `translator.cdy` cases, and the "declared in none of …" text is updated.
  - `test_bootstrap.py:55` now skips library files the old commit doesn't have; it used to crash on them.
- **Docs and spec:**
  - The declaration-module rule is in `programs.import`, with an error row.
  - `programs.shadowing` and `60-library.md` say the five are declared in `translator.cdy`; `CLAUDE.md`, `README.md` and `bin/README.md` list it among the library files.
  - The HLD has Questions 9 and 10 answered and step 2's "2a done" note. B200 is `in-progress`.

**Checks:**
- pytest: 702 passed, 4 xfailed.
- ruff, mypy, pyright and pylint are all clean.
- `cmp3` against `boot/77`: all 99 programs give the same Python, the translator included.
- No tokens in the changed files.

Every change in `git status` is mine; there are no owner edits. On "gawc" I'll commit (adding `bin/py/translator.cdy`), put 2a's hash in `STAGING` as `old-library`, run `bootstrap.py --tag` for `boot/78`, and check that the tag is annotated.

## Owner

> what's a "declaration module"/

## Claude Code

A declaration module is a library file that contains only type signatures, with no code. Each signature names a built-in and gives its Candy type, and the runtime supplies the actual function.

`translator.cdy` is a whole declaration module:

```
(sig fresh-name (Fn (String) String))
```

That line says `fresh-name` exists and takes a `String` to a `String`. Its body is Python, `fresh_name` in `cdy_rt/primitives.py`, and `spelling.py` links the two. Normally a `sig` without a definition is an error ("sig without a definition"). Only in a declaration module is that allowed, because the runtime is the definition.

**How it differs from an ordinary module:**

| | ordinary module (`form.cdy`, your `util.cdy`) | declaration module (`translator.cdy`, later `system.cdy`) |
|---|---|---|
| contents | `def`, `defn`, `deft` with bodies | bodiless `sig`s (and in `system.cdy`, bodiless `deft`s) |
| code it produces | Python for each definition | none; uses become `Prim`s, spelled from `spelling.py` |
| where it comes from | your directory first, then the library | the library only, always |
| who may write one | anyone | only the library (a target brings its own) |

**Why have them:** they're how Candy talks about what the host (Python) provides, in Candy, with types the checker can use. Each target ships its own declaration modules with its own runtime behind them. Importing one works like any import: `(import translator (fresh-name))`, or `translator.fresh-name` when qualified.

`system.cdy` has always been one in effect (every built-in such as `len` or `map` is declared there), but it was read specially rather than as a module. Step 2 gives the idea a name and a second instance (`translator`). Step 3 then makes `system` an actual module of this kind.

## Owner

> gawc

## Claude Code

*ran: `git status --short && git diff --stat | tail -1`*

Same files as before; no edits of yours among them. Committing.

*ran: `S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

*ran: `H=$(git rev-parse HEAD) && python3 - "$H" <<'EOF'`*

Step 2a is committed as `7dc8c6f` and tagged `boot/78`.

- `bootstrap.py --tag` checked the step with `old-library` staging and passed ("ok 78 7dc8c6f").
- `boot/78` is an annotated tag (`git cat-file -t` gives `tag`), and its message records `staging: old-library`.

One change is left uncommitted on purpose: 2a's hash in `STAGING` in `script/bootstrap.py`. `--tag` needed it to check the step, and the tag now records the staging. It will go in with 2b, like the earlier `old-library` entries.

Not pushed yet: master `93c4b5e`, branch `library-layers` (`40e7172`, `7dc8c6f`), and the tags `boot/77` and `boot/78`.

Next is 2b, where only modules that import `translator` see the five:
- The translator's modules that call them get `(import translator)`: `cdyc`, `include` and `expand`, plus `form` for `fresh-name`.
- Macro programs get the five implicitly.
- `form.cdy`'s import must not break where macro programs include `form.cdy`'s text instead of importing it.

Shall I go ahead with 2b?

## Owner

> Go

## Claude Code

*ran: `grep -n "(Typed\|Typed " src/cdy/*.cdy | grep -v "^src/cdy/core.cdy:10[0-9][0-9]`*

Giving `Typed` the module that declares it, so `resolve`'s fallback can skip `translator`'s. First, every place that asks "is this a built-in":

*ran: `grep -n "map-has builtins\|map-has (get scope builtins)\|map-has (get [a-z]* bui`*

*ran: `sed -n 370,395p src/cdy/core.cdy && sed -n 244,262p src/cdy/expand.cdy && grep -`*

*ran: `grep -rn "analyse-program\|translate-expanded" src tst | grep -v "^src/cdy/core.`*

*ran: `grep -n '"import"\|import-macros' src/cdy/core.cdy | head && grep -rn "gensym" s`*

*ran: `sed -n 415,430p src/cdy/core.cdy && grep -n "defn analyse-tops" -A30 src/cdy/cor`*

*ran: `grep -n "defn analyse-tops" -A40 src/cdy/core.cdy | head -45`*

*ran: `python3 - <<'EOF'`*

*ran: `python3 - <<'EOF'`*

Fixpoint reached with 2b. Adding the B50 tests and a spec row:

*ran: `python3 - <<'EOF'`*

*ran: `sed -n 40,58p spec/50-macros.md`*

*ran: `python3 - <<'EOF'`*

*ran: `pytest -q tst/py_cdy/test_self_host.py::test_quoting_in_macro_code 2>&1 | grep -`*

*ran: `python3 - <<'EOF'`*

All 704 pass. Now the docs for 2b, B50 and B200:

*ran: `cat backlog/B50-translator-builtins-shared.md && pytest -q tst/py_cdy/test_boots`*

*ran: `python3 - <<'EOF'`*

I removed a sentence from 2a's committed Done note ("2b needs none…"), which turned out to be wrong. Putting it back, since the 2b note already corrects it:

*ran: `python3 - <<'EOF'`*

Now the full checks and the comparison against `boot/78`.

*ran: `ruff check src tst script && ruff format --check src tst script && mypy src/py_c`*

*ran: `ruff format tst/py_cdy/test_self_host.py && ruff format --check src tst script &`*

*ran: `git status --short && git diff --name-only | xargs grep -lE "github_pat_|ghp_" &`*

Step 2b is built and every check passes; nothing is committed yet. With it, B50 (the translator's five host built-ins are every program's) is fixed, and B50 and B200 (library-layers step 2: declaration modules, and `translator.cdy`) are both set to `review`.

**One deviation:** 2b needs `old-library` staging, like 2a, so the reason for splitting the step only half held. `boot/78` reads the `form.cdy` it uses for macro programs straight from the library, and 2b's `form.cdy` now has an `import`, which 78 rejects inside macro code. It's the existing kind, so there's no new bootstrap code. The split was still needed: in one commit, 77 couldn't have found `translator.cdy` at all.

**What changed:**
- **`core.cdy`:**
  - `Typed` now records which declaration module declares the built-in.
  - `resolve` uses a declared built-in without an import only if `system` declares it (`is-everyones`).
  - Using one of `translator`'s without importing it fails with "fresh-name is declared by translator, which this file doesn't import: (import translator)" (`declaring-module`).
  - `analyse-program` now takes the imports macro code gets.
- **The translator's own modules:** `cdyc.cdy`, `include.cdy` and `expand.cdy` have `(import translator)`; `form.cdy` has `(import translator (fresh-name))` for `gensym`.
- **Macro code:**
  - It imports `translator` implicitly, through `macro-imports` (`cdyc.cdy`).
  - `form-defs` (`expand.cdy`) drops `form.cdy`'s import before using its text.
  - In a macro file, an import of a declaration module adds nothing (`include-forms`, `include.cdy`). Without this, the quoting test failed, because it includes `form.cdy` as text.
- **Tests:** a new `test_module_errors` case: `a.cdy` imports `translator` and uses `fresh-name`, while `main.cdy` doesn't import it and gets the error.
- **Spec:**
  - `programs.import` gets the rule and an error row.
  - `programs.shadowing` says the five are only for files that import `translator`.
  - `macros.macro-code` says macro code gets the translator's built-ins.
  - `library` says they're declared in `translator.cdy` and seen only by importers.
- **Docs:**
  - `CLAUDE.md` is updated to match.
  - The HLD has a "2b done" note. 2a's committed note, which said 2b needs no staging, stays as written; the 2b note corrects it.
- **Bootstrap:** `script/bootstrap.py` carries 2a's `STAGING` entry. On commit I'll add 2b's hash the same way and tag `boot/79`.

**Checks:**
- pytest: 704 passed, 4 xfailed.
- ruff, mypy, pyright and pylint are clean.
- `cmp3` against `boot/78`: all 99 programs give the same Python, the translator included.
- No tokens in the changed files.

All changes in `git status` are mine; there are no owner edits. Ready for "gawc".

## Owner

> Gawc

## Claude Code

*ran: `git status --short | wc -l && S=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b`*

Step 2b is committed as `f957aa8` and tagged `boot/79`. `bootstrap.py --tag` checked the step with `old-library` staging and passed. `boot/79` is an annotated tag that records `staging: old-library`.

2b's hash in `STAGING` (`script/bootstrap.py`) is left uncommitted, as 2a's was. It will go in with step 3.

Not pushed yet:
- master: `93c4b5e`
- branch `library-layers`: `40e7172`, `7dc8c6f`, `f957aa8`
- tags: `boot/77`, `boot/78`, `boot/79`

Waiting for your review: B200 (library-layers step 2: declaration modules, and `translator.cdy`) and B50 (the translator's five host built-ins are every program's), both now in `review`.

Next is step 3, B201: `system` becomes an implicitly imported module, so `system.name` works, and a built-in type's module becomes `"system"`.

## Owner

> Tick, go

## Claude Code

*ran: `for f in backlog/B200-library-layers-step-2.md backlog/B50-translator-builtins-s`*

*ran: `cat backlog/B196*.md backlog/B197*.md | head -60 && grep -n 'id="programs.sees"'`*

Ticked: B200 and B50 are `done`. Starting step 3, B201 (library-layers step 3: the system, a module). First, a survey of where built-in types carry module `""`:

*ran: `grep -n 'TCon ""\|(TCon m\|TCon module\|"" "' src/cdy/*.cdy | head -60`*

*ran: `sed -n 55,72p src/cdy/check.cdy && sed -n 118,125p src/cdy/check.cdy && sed -n 1`*

*ran: `grep -n "defn spelled" -A12 src/cdy/emit.cdy && sed -n 470,500p src/cdy/emit.cdy`*

*ran: `sed -n 100,215p src/cdy_rt/primitives.py`*

*ran: `grep -n "is-rest\|rest-item\|MAIN_TYPE\|(tcon \|key-tcon\|is-builtin-type\|globa`*

*ran: `sed -n 1570,1625p src/cdy/core.cdy && sed -n 925,952p src/cdy/core.cdy`*

The plan holds. Reading the checker's spots that turn a type into a key or compare names:

*ran: `sed -n 608,650p src/cdy/check.cdy && sed -n 776,786p src/cdy/check.cdy && sed -n`*

*ran: `grep -n '(= m "")\|(= module "")\|(= bm "")\|"" name\|(!= m "")' src/cdy/*.cdy`*

Applying the step 3 edits across `core`, `check`, `lower`, `emit` and `include`:

*ran: `sed -n 38,46p src/cdy/core.cdy && sed -n 336,343p src/cdy/core.cdy && sed -n 135`*

*ran: `python3 - <<'EOF'`*

*ran: `sed -i 's/(Res (TCon "" "Tup" ts) st1)))/(Res (TCon SYSTEM "Tup" ts) st1)))/ && `*

*ran: `python3 - <<'EOF'`*

Now `(import system)` as an error in `include.cdy`:

*ran: `python3 - <<'EOF'`*

*ran: `grep -n '"Tup"\|"List"\|"Unit"\|"Any"\|"Bool"\|"String"' src/cdy/check.cdy src/c`*

`tcon-name` gives a type's key, which is now `system.Tup`. Checking its users:

*ran: `grep -n "tcon-name\|global-key" src/cdy/check.cdy src/cdy/emit.cdy src/cdy/lower`*

*ran: `sed -n 575,585p src/cdy/check.cdy && sed -n 318,330p src/cdy/check.cdy && grep -`*

*ran: `python3 - <<'EOF'`*

Fixpoint reached. Trying the new behaviour by hand:

*ran: `rm -f *.cdy && cat > s1.cdy <<'EOF'`*

*ran: `python3 - <<'EOF'`*

B196 (a type with the same name as a built-in type can't be shown) is fixed: `s6` prints `(Map 1)`. Full suite:

*ran: `pytest -q 2>&1 | tail -8`*

All pass, but there are still 4 xfails, and B196's repro should be passing now. Checking which ones they are:

*ran: `pytest -q tst/py_cdy/test_spec.py -rx 2>&1 | grep -i xfail | head && pytest -q t`*

In the spec, programs are translated from text, and their top module's stem is `""`, so `global-key` gives just `Map` again. `show-name` should always add the `.`:

*ran: `python3 - <<'EOF'`*

B196's repro now passes, which fails the strict xfail. Moving B196 to `review`:

*ran: `python3 - <<'EOF'`*

*ran: `pytest -q tst/py_cdy/test_spec.py -k B196 2>&1 | grep -E "^E|XPASS|strict" | hea`*

*ran: `grep -n "def item_files" -A15 tst/py_cdy/test_spec.py && grep -rn "## Repro" bac`*

*ran: `sed -n 25,50p backlog/B119-variant-as-type-message.md && grep -n "item_files" -A`*

The process for a fixed defect: the item's `## Repro` moves verbatim into a note, and its example goes into the spec. Doing that for B196, with the example under `library.show`:

*ran: `cat backlog/B196-type-shadowing-builtin-show.md | sed -n 20,60p && grep -n 'id="`*

*ran: `sed -n 318,335p spec/60-library.md`*

*ran: `python3 - <<'EOF'`*

*ran: `sed -i 's/^## Notes\n- 2026-11-16, Claude: fixed by/X/' backlog/B196-type-shadow`*

*ran: `sed -n '/id="programs.qualified"/,/^<a id/p' spec/10-programs.md | sed -n '/'''c`*

*ran: `python3 - <<'EOF'`*

Spec done for `system.name`. Now the docs that still say a built-in type's module is `""`:

*ran: `grep -rn ''""' for a built-in\|built-in type.s module\|"" for a built-in\|B197' `*

*ran: `sed -n 8,30p src/cdy/core.cdy`*

*ran: `python3 - <<'EOF'`*

*ran: `cat >> backlog/B197-builtins-module.md <<'EOF'`*

*ran: `python3 - <<'EOF'`*

Everything passes. Comparing against `boot/79`; programs that `show` a record should differ (B196's fix):

*ran: `rm -rf tmp/c7/sp3/* tmp/c7/b72/bin && git archive refs/tags/boot/79 bin | tar -x`*

*ran: `python tmp/c7/cmp3.py 2>&1 | cut -c1-80 && for p in tst/cdy/sums.cdy tst/cdy/cdy`*

As expected: show names change from `'Tree'` to `'sums.Tree'`. Checking that every difference is of that kind, and what `e15` is (it failed before):

*ran: `cat tmp/c7/sp3/e15.cdy && for p in tst/cdy/sums.cdy tst/cdy/cdyc/library_module.`*

*ran: `git status --short && git diff --name-only | xargs grep -lE "github_pat_|ghp_" &`*

Step 3 is built and every check passes; nothing is committed yet. B201 (library-layers step 3: the system, a module) and B196 (a type with the same name as a built-in type can't be shown) are in `review`. The ticks on B200 and B50 are in this change too.

**How it differs from the HLD:** `system` isn't literally imported as a module. If it were, an imported module that defines its own `len` would clash with `system`'s, which breaks the shadowing rule. Instead, every file's table gets each built-in function, value and type as `system.name` only (`with-system`, `core.cdy`). Unqualified built-ins keep their place as the last thing a name can mean, so shadowing is unchanged.

**What's in it:**
- **Qualified built-ins:** `system.len` and `system.+` are the built-ins even where the file defines its own `len`. `system.Int` works as a type.
  - `(put system.Int)` gives "is a type, not a value"; `(sig x system.len)` gives "is a value, not a type".
  - `system.if` and `system.fresh-name` aren't defined: special forms and `translator`'s built-ins aren't `system`'s.
- **`(import system)`** is an error, "import: every file imports system, implicitly" (`include.cdy`).
- **B197 (the built-ins' module, and macro code's), first half:**
  - In Core, a built-in type's module is now `SYSTEM` instead of `""` (`core.cdy:43`).
  - `analyse-type` writes it, and `global-ref` keeps it for any name no usable entry has.
  - `is-any`, `is-rest`, `returns-unit`, the constraints, `tcon` and `emit` all read it.
  - Macro code keeps `""`, which is B197's second half.
- **B196 fixed:** `show-name` (`emit.cdy`) writes a program's type with its module (`'main.Map'`, or `'.Map'` for a program read from text), so `show` no longer mistakes it for the built-in. As the process asks, the item's repro moved verbatim into a note, and its example is now in `library.show`.
- **Spec:**
  - `programs.sees` and `programs.qualified` cover `system.name`, with an example and error rows.
  - `programs.import` gets the `(import system)` row.
- **Docs:** `CLAUDE.md` and two `core.cdy` comments are updated; B197 has a note; the HLD has step 3's Done note.

**Bugs found while testing:**
- The prelude's `Map` resolved to the program's own `Map`, because an `Elsewhere` entry fell back to `""`. Fixed in `global-ref`.
- `(Tup …)` patterns broke, because a type's key is now `system.Tup`. Fixed in `check.cdy`.

**Checks:**
- pytest: 709 passed, 3 xfailed (B196's xfail is gone).
- ruff, mypy, pyright and pylint are clean.
- `cmp3` against `boot/79`: 15 programs differ, all only in `register_type`/`show` type names. One is the new `system.name` example, which `boot/79` can't translate.
- No staging: `boot/79` builds this step next to today's library.
- No tokens in the changed files.

All changes are mine, plus 2b's `STAGING` entry from before. On "gawc" I'll commit and tag `boot/80`.

*(The context was summarised here; the turns before it are above.)*

## Owner

> Gawc

## Claude Code

*ran: Check status and scan diff for tokens*

Same files as before, no owner edits, no tokens.

*ran: Commit step 3 and tag boot/80*

I committed step 3 as `9b2dabd` (library-layers step 3: the system, a module) and tagged it `boot/80`. The tag is annotated and needs no staging. The working tree is clean.

- **What went in:** the step itself, the ticks on B200 and B50, and step 2b's `STAGING` entry in `script/bootstrap.py`.
- **Before committing:** I checked that none of the changes were yours and that the diff has no tokens.
- **Not pushed:** master `93c4b5e`, `library-layers` (four commits, `40e7172` to `9b2dabd`) and tags `boot/77` to `boot/80` are still only local.

Next is step 4: B202 (library-layers step 4: the 11 built-ins dropped). It will need `old-library` staging. Say "go" to start.

## Owner

> Go

## Claude Code

*ran: Read B202 and HLD outline*

*ran: Read HLD step 4 and related items*

*ran: Find uses of the 11 built-ins*

*ran: Read the primitives to drop*

*ran: Find re import and other references*

I'm dropping the 11 built-ins from `system.cdy`, `spelling.py` and `primitives.py`, then the spec rows and tests. One thing to check first: how generated code imports `re`.

*ran: Read spelling table and imports*

*ran: Read system.cdy and SPELLINGS*

Now the edits: `system.cdy`, `spelling.py`, `primitives.py`, its tests.

*ran: Drop the 11 from system, spelling, primitives*

Python wasn't on the path; rerunning in the conda environment.

*ran: Apply the drops in the conda environment*

Next: `import re` in generated code (`PY_IMPORTS`, `emit.cdy:52`) existed only for the regexes, so it goes too. Then the spec rows.

*ran: Find re import and spec references*

*ran: Check remaining Any-typed built-ins*

*ran: Read system.cdy and translator.cdy headers*

*ran: Update comments, spec, PY_IMPORTS*

*ran: Check module-dir's Any argument*

*ran: Refine Any wording*

The spec, comments and `PY_IMPORTS` are updated. Next I'm rebuilding `bin`, where the staging should show up.

*ran: Rebuild bin*

*ran: Read staging logic and self_host options*

*ran: Read run_step and build functions*

*ran: Copy library into bin and rebuild*

Rebuilt. Running all the checks now; `test_newest_step_reads_the_library` shows whether staging is needed.

*ran: Run tests and all linters*

All checks pass, and no staging warning appeared, with warnings treated as errors. So `boot/80` builds this step next to today's library. Now `cmp3` against `boot/80`:

*ran: Compare outputs with boot/80*

As expected, the old `bin` with its own old library fails against the new runtime. To compare, I'll give it today's library, as the chain does.

*ran: Compare with boot/80 using today's library*

*ran: Show the comparison summary*

96 programs differ. I'm checking whether `import re` is the only difference.

*ran: Compare ignoring the import re line*

*ran: Read HLD steps and note formats*

*ran: HLD Done note, B202 and B32 notes*

*used ToolSearch*

*used TaskStop*

*ran: Check edits landed and read B49*

Those edits landed; a stray `cat` had held the shell open. Now B49, and an over-long line in the HLD note.

*ran: Narrow B49, regenerate index, check links*

The long lines are all older ones; mine are within 90. Last, I'm checking the HLD's count ("83 built-ins in `system`") and the token grep.

*ran: Count built-ins, scan tokens, status*

*ran: Apply B49 and HLD edits, recheck*

Step 4 is built and every check passes; nothing is committed yet. B202 (library-layers step 4: the system, revisited) is in `review`.

**Staging:** the HLD expected this step to be staged, but it doesn't need it.
- The bootstrap chain runs the previous translator with the new step's own library. The new `system.cdy` and the new runtime agree, so `boot/80` can build the step.
- `test_newest_step_reads_the_library` passes with warnings treated as errors, which confirms it.
- Only the local rebuild needed a manual step: `bin/py`'s old library copies had to be replaced first.
- The HLD's Done note records this, and I left the Bootstrap section's text as it was.

**What's in it:**
- **The 11 are gone** from `src/cdy/system.cdy` and `src/cdy_rt/spelling.py`. Their seven Python `def`s and their tests are gone from `primitives.py` and `tst/cdy_rt/test_primitives.py`. `get_args` stays, because `run_main` uses it.
- **No more `import re`:** generated code no longer imports it (`PY_IMPORTS` and `PY_RESERVED`, `src/cdy/emit.cdy:52` and `:94`). That means a program may now use `re` as a name.
- **No `system` built-in is typed `Any` any more.** Only three of `translator`'s are (`load-macros`, `call-macro`, `module-dir`). The texts that said otherwise are updated: `spec/25-checking.md:436`, `spec/60-library.md:20`, and the header comment in `system.cdy`.
- **Spec:** `library.builtins`'s table no longer lists the 11 or the "regular expressions" row.
- **Backlog:**
  - B32 (Regexes are Python's) is `done`.
  - B49 (Host objects have no Candy type) is narrowed to the macros; the old text is kept verbatim in a note.
  - B202 is in `review`.
- **HLD count:** `system` has 78 built-ins left, not the HLD's 83. That figure was counted while `translator`'s five were still in `system`; the Done note says so.

**Checks:**
- pytest: 709 passed, 3 xfailed.
- ruff, mypy, pyright and pylint are clean.
- `cmp3` against `boot/80`, given today's library: once `import re` is ignored, all 100 programs produce the same output.
- No tokens in the diff.

All the changes are mine. On "gawc" I'll commit and tag `boot/81`, with no staging, and run `bootstrap.py --step` on the new commit to confirm it needs none.

## Owner

> gawc

## Claude Code

*ran: Check status and commit step 4*

Committed. Now I'm checking the new step in the chain before tagging.

*ran: Show bootstrap options*

*ran: Check the step in the chain, then tag boot/81*

I committed step 4 as `81e7022` (library-layers step 4: the system, revisited) and tagged it `boot/81`. The tag is annotated and has no staging.

Before tagging, I ran `bootstrap.py --step` on the new commit and it passed (`ok 81`). So `boot/80` builds this step with no staging, as I'd found locally. The working tree is clean.

Still not pushed: master `93c4b5e`, `library-layers` (five commits, up to `81e7022`), and tags `boot/77` to `boot/81`.

Next is step 5, B203 (library-layers step 5: `slurp` without a search). It fixes B54. Say "go" to start.

## Owner

> go

## Claude Code

*ran: Read B203, B54, HLD and slurp*

*ran: Read get_path and slurp uses*

*ran: Read library.errors spec and error handling*

*ran: Read panic hook and file-missing tests*

*ran: Read missing-file tests and read_sexpr*

*ran: Read main.py error handling*

*ran: Rewrite slurp without the search*

Now a runtime test, and the spec rule with its example:

*ran: Read test_files*

*ran: Add slurp test and spec text*

*edited: `spec/60-library.md`*

The translator's source hasn't changed, so `bin` won't change and this step gets no `boot` tag. Running the tests:

*ran: Rebuild bin and run tests*

As expected, the driver now says "slurp: can't read missing.cdy". I'm making that test exact.

*ran: Fix test, rerun tests and linters*

All pass. Now the HLD's Done note, B203 (library-layers step 5: `slurp` without a search) and B54 (`slurp` searches `src/`, `tst/` and `lib/` when a path is missing):

*ran: HLD note, B203 and B54, checks*

Step 5 is built and every check passes; nothing is committed yet. B203 (library-layers step 5: `slurp` without a search) and B54 (`slurp` searches `src/`, `tst/` and `lib/` when a path is missing) are in `review`.

**What changed:**
- **`slurp`** (`src/cdy_rt/primitives.py`, near the "files" section) reads the path it is given and nothing else. If it can't read the file, the program panics with "slurp: can't read path". `SEARCH_PATH`, `find_path` and `get_path` are gone.
- **The translator's driver:** for a missing file it now says `candy: slurp: can't read missing.cdy` instead of "can't find …". `test_bin_driver` (`tst/py_cdy/test_self_host.py:440`) now checks that exact text.
- **The one user of the search:** `tst/cdy/read_sexpr.cdy:84` read itself as `"read_sexpr"`. It now gives its path, `tst/cdy/read_sexpr.cdy`. That path is relative to the repository root, which is where the tests run programs.
- **Spec:** `library.errors` lists a file `slurp` can't read as a panic, with a `candy panic` example.
- **Tests:** `test_files` (`tst/cdy_rt/test_primitives.py`) checks that `slurp` reads a file, and that a bare name is not searched for.

**No `boot` tag:** the translator's source didn't change, so the rebuilt `bin` is the same and this commit gets no tag.

**Checks:**
- pytest: 710 passed, 3 xfailed, with no staging warning.
- ruff, mypy, pyright and pylint are clean.
- No tokens in the diff.

All the changes are mine. On "gawc" I'll commit it.

## Owner

> gawc

## Claude Code

*ran: Commit step 5*

I committed step 5 as `fdbe6b9` (library-layers step 5: slurp without a search). The working tree is clean. It doesn't change `bin`, so the bootstrap chain has no new step and there's no tag.

Still not pushed: master `93c4b5e`, `library-layers` (six commits, up to `fdbe6b9`), and tags `boot/77` to `boot/81`.

Next is step 6, B204 (library-layers step 6: each built-in specified): a rule for each group of built-ins in `spec/60-library.md`, the index, and the test. Say "go" to start.

## Owner

> go

## Claude Code

*ran: Read B204, HLD step 6, library spec outline*

*read: `spec/60-library.md`*

*ran: List system.cdy sigs*

I'm working out which built-ins no `candy run` example names yet, using the fence reader the doc test uses.

*ran: List doc_links helpers and tests*

*ran: Read test_doc_links setup*

*ran: Find built-ins named in no run example*

Those 21 are named in no `candy run` example yet. Before writing file examples, I'm checking where spec examples run (their working directory).

*ran: How spec examples run; operator rules*

*ran: Read edge-case behaviour of primitives*

*ran: Prelude sigs, expr.unit, isspace-at uses*

Now the runtime fix, then the spec rewrite, section by section.

*ran: Bounds-check isspace_at*

*ran: Test isspace_at bounds*

Now the Built-ins section becomes the index:

*edited: `spec/60-library.md`*

Now the lists rule's table:

*edited: `spec/60-library.md`*

*edited: `spec/60-library.md`*

*edited: `spec/60-library.md`*

Now maps:

*edited: `spec/60-library.md`*

*edited: `spec/60-library.md`*

Now output (`library.put`):

*edited: `spec/60-library.md`*

Now the two new rules, files and math, after maps:

*edited: `spec/60-library.md`*

*edited: `spec/60-library.md`*

Now `<=` in the comparisons example. I'm also checking whether the operators' rules give their types:

*ran: Read the operators' rules*

I'll add one table of the operators' types to `expr.arithmetic`, and `<=` to the comparisons example:

*ran: Operator types table and <= example*

Now the test that keeps it so, in `tst/py_cdy/test_doc_links.py`:

*ran: Read rest of test_doc_links*

*edited: `tst/py_cdy/test_doc_links.py`*

*ran: Wire up the test and run spec tests*

*ran: Rebuild bin, full tests and linters*

The grep reported 0, probably because `-q` and `-v` together give no PASSED lines. I'm confirming the new tests ran:

*ran: Confirm the new tests ran*

Both pass. Now the HLD note and B204 (library-layers step 6: each built-in specified). First, checking that B160 is the item for "Python's other errors aren't panics":

*ran: Check B160 and new long lines*

The long lines are older ones; none of mine. Now the HLD note and B204:

*ran: HLD Done note, B204, checks*

Step 6 is built and every check passes; nothing is committed yet. B204 (library-layers step 6: each built-in specified) is in `review`.

**The index:** `library.builtins`' table (`spec/60-library.md:23`) now has one row per group, with columns for the group, its rules and its built-ins.
- Every built-in in `system` is listed, the operators too. `show`, `find-index` and `elem-index` were missing from the old table.
- The prelude's own functions (`rest`, `find`, `index-of`, `with-default`, `map-update`, `put`) are marked "the prelude's".

**The rules:**
- Each group's rule has a table of its calls, with each call's type and what it gives at the edges: lists, maps, strings, output (`library.put`), and the program (`library.errors`).
- Two new rules: `library.files` and `library.math`.
- `expr.arithmetic` (`spec/40-expressions.md`) gets a table of the operators' types.
- New examples cover the 21 built-ins no example used before. The files example writes under `output/spec/`, which git ignores.
- Where a built-in still stops with Python's error rather than a panic, the rule says so and links B160 (Python's own errors aren't panics: its traceback, and its words). That is `map-get` of a missing key, `to-int` of text that isn't a number, `char-code` of a string that isn't one character, `split` on `""`, and a `spit` that can't write.

**A fix I made while specifying:** `isspace-at` wasn't bounds-checked, so a negative index counted from the end, as in Python. It now panics like `char-at` does (`src/cdy_rt/primitives.py`, `isspace_at`). Both the runtime tests and the spec have a case for it.

**The test:** `test_every_builtin_is_specified` (`tst/py_cdy/test_doc_links.py`) checks that each `system.cdy` built-in is in the index and in an example that runs. It has a small self-test too. It differs from the HLD in two ways, both recorded in the HLD's Done note and B204:
- It checks only `system.cdy`. The HLD says "every `sig` in a declaration module", but the same section says `translator`'s five are specified in `translator.cdy`'s comments, not in the spec.
- It counts a `candy panic` example as well as `candy run`, because `fail` can only be shown by a panic.

**No `boot` tag:** the translator didn't change, so `bin` didn't either.

**Checks:**
- pytest: 716 passed, 3 xfailed.
- ruff, mypy, pyright and pylint are clean.
- No tokens in the diff.

All the changes are mine. On "gawc" I'll commit it.

## Owner

> Where is `isspace-at` being used?

## Claude Code

*ran: Find all uses of isspace-at*

Only the translator's reader and the old test reader call it, and every call already checks the index first, so the new bounds check never fires there:

- **`src/cdy/read.cdy`**, the translator's reader, has four calls. Each one is behind a check that the position is inside the text:
  - `:71`, in `skip`: an earlier `cond` clause, `(>= pos (str-len text))`, returns first.
  - `:82` and `:148`: an `or` that tests `(>= pos (str-len text))` before it calls `isspace-at`.
  - `:118`: an `and` that tests `(< (+ pos 1) (str-len text))` before it calls `isspace-at`.
- **`tst/cdy/read_sexpr.cdy:15`**, the old untyped reader test program, uses it in `skip-space`, in the same shape as `skip`.

Apart from those, it appears only where it's declared and spelled (`src/cdy/system.cdy:133`, `src/cdy_rt/spelling.py:197`) and in the tests and spec examples I added.

The full test run passed with the check in place, which bears this out. Mostly, the change just puts `isspace-at` under the same `library.bounds` rule as `char-at`.

## Owner

> Did any files just change?   Trying acode again and it was asking me about file edits

## Claude Code

*ran: Check working tree and recently changed files*

No, nothing has changed since my last report. Nothing has been written since the backlog index was regenerated at the end of step 6, apart from pytest's cache (`.pytest_cache/`, which git doesn't track). Answering your `isspace-at` question only read files.

The tree does have eight modified files, but they are step 6's uncommitted edits, the ones I reported:
- `backlog/B204-library-layers-step-6.md` and `backlog/README.md`
- `doc/hl_rqmt/library_layers.md`
- `spec/40-expressions.md` and `spec/60-library.md`
- `src/cdy_rt/primitives.py`
- `tst/cdy_rt/test_primitives.py` and `tst/py_cdy/test_doc_links.py`

If "acode" is an editor with one of those files open, it was probably asking whether to reload the version I changed on disk, or keep its own copy. Reloading is safe. If you've typed edits in it that you want to keep, save them and tell me, and I'll name them before the commit, as usual.

## Owner

> Does isspace-at still need to be aprim?

## Claude Code

*ran: Look for a char-to-string helper*

*ran: Find char-text's definition*

No, it doesn't need to be a built-in. It's `isspace` applied to one character, and Candy can already say that. `read.cdy` has the pieces:

```
(sig char-text (Fn (String Int) String))
(defn char-text (s i) (text (char-at s i)))     ; read.cdy:89
```

So `(isspace-at s i)` is `(isspace (char-text s i))`. It gets the bounds check from `char-at`, so the panic just says `char-at: index out of range` instead. `tst/cdy/read_sexpr.cdy:8` has the same helper, called `ch`.

It also fits step 4's rule. The only callers are the translator's reader and that old test reader; no program needs it. It's still in `system` only because it was a Python helper the reader used from the start.

**Options:**
1. **Drop it from `system`** *(recommended)*, along with its spelling, its primitive and my bounds-check fix. The five calls in `read.cdy` and `read_sexpr.cdy` would use `isspace` with `char-text` or `ch` instead.
   - The translator changes, so this means a rebuild and `boot/82`.
   - The step 4 pattern should hold, so it needs no staging: the chain reads the step's own library.
   - The reader does a little more work (two calls instead of one per character). The translator's test run would show whether that matters.
   - It would go into step 6, or step 4's follow-up, with notes.
2. **Keep it**, bounds-checked as it now is. It's portable and harmless, just one built-in more than a program needs.

If you pick option 1, should it go in this step's commit or a separate one? I'd put it in this one: the step already touches `isspace-at`, and the spec tables would just lose a row.

## Owner

> My vote is drop it... And if possible try and check what else we can ditch

## Claude Code

I'll drop `isspace-at`. To find anything else that could go, I'm counting where each `system` built-in is used outside its declaration.

*ran: Count uses of each built-in*

The counts show few clear cases. I'll drop `isspace-at` now and put the rest to you as options. First the drop: the reader's five calls become `isspace` over one character.

*ran: Drop isspace-at everywhere*

The working tree no longer mentions `isspace-at`. Rebuilding `bin`, timed to see what the reader's extra call costs:

*ran: Time old vs new translator, rebuild bin*

*ran: Restore isspace-at for the first commit*

*ran: Check spec region formatting*

*ran: Fix blank line, rebuild bin, time old vs new*

The rebuilt `bin` no longer calls `isspace_at`. Translating the translator takes about 1.00s against 0.98s before, so the extra call costs about 2%. Running the checks for commit 1:

*ran: Full checks and cmp3 against boot/81*

Everything passes, and `cmp3` against `boot/81` finds no difference across 102 programs. Updating the notes, since this commit now changes `bin`:

*ran: Update HLD and B204 notes*

*ran: Check which candidates bin calls*

Commit 1 is ready: step 6, plus the reader moved off `isspace-at`. `isspace-at` itself is dropped in commit 2. Here is what else could go there.

I counted each `system` built-in's uses in the translator, the prelude and `tst/cdy`. The counts are from a script I ran just now; they're not saved anywhere.

**1. Clear cases** *(recommended: drop both)*
- **`elem-index`**: only the prelude's `index-of` uses it. That can be written as `(find-index (fn (y) (= x y)) xs)`.
  - `bin` calls it, through the prelude's `index-of`. So the prelude's rewrite would have to go into commit 1, as the reader's did, with the drop in commit 2.
- **`is-digit`**: a near-twin of `is-decimal`, and a small leak, since Python's `isdigit` counts `²` as a digit. Only `tst/cdy/read_sexpr.cdy` uses it, and `is-decimal` works there. `bin` doesn't call it.

**2. Unused, but basic** *(recommended: keep for now)*
- These are `reverse`, `map-size`, `ends-with` and `repeat`. Nothing uses them, but they're portable, ordinary operations a program expects.
- Unlike step 4's drops, they aren't Python's and aren't oddities, and the next branch, `stdlib`, designs the `list`, `string` and `map` modules. Dropping them now would probably mean adding them back there.
- `sin`, `cos` and `tan` stay, as already decided (HLD Question 2).

**3. Writable in Candy over other built-ins** *(recommended: not now)*
- `all` (from `any`), `contains` (from `any`), `take` and `drop` (from `slice`), `starts-with` and `ends-with` (from `substring`), `map-size` (from `map-keys`), `tan` (from `sin` and `cos`).
- Moving them into the prelude has costs:
  - each call runs Candy code instead of one host call, and the translator uses `contains` 37 times and `drop` 11;
  - macro code doesn't get the prelude;
  - every file pays for the prelude.
- These are the "prelude's costs" HLD Question 1 gave to `stdlib`, so they belong there.

So commit 2 would drop `isspace-at`, and also `elem-index` and `is-digit` if you agree. That brings `system` from 78 built-ins to 75.

Which do you want? On your answer, I'd add the prelude's `index-of` rewrite to commit 1 if needed, then commit on "gawc" as `boot/82`, and build commit 2.

## Owner

> Your recommended for all... gawc

## Claude Code

You agreed to all the recommendations, so commit 2 drops `isspace-at`, `elem-index` and `is-digit`. First, the prelude's `index-of` moves onto `find-index`, so commit 1's `bin` no longer calls `elem-index`.

*ran: Read prelude index-of*

*ran: Rewrite index-of, rebuild, test, compare*

98 programs differ because every program's output includes the prelude. Checking that `index-of`'s body is the only difference:

*ran: Inspect differences*

The sample diffs show only that one line. Confirming across all 102 programs, with that line ignored:

*ran: Compare ignoring the index-of line*

*ran: Look at a remaining difference*

*ran: Normalise fresh-name numbering in diff*

The other differences are only renumbered fresh names. Adding the prelude change to the notes, then committing:

*ran: Update notes and check status*

*ran: Commit step 6, check step, tag boot/82*

I committed step 6 as `47bb613` and tagged it `boot/82`. The tag is annotated and has no staging, and `bootstrap.py --step` passes.

Now commit 2: dropping `isspace-at`, `elem-index` and `is-digit`.

*ran: Find every mention of the three*

*ran: Read the surrounding text of each mention*

*ran: Drop the three, rebuild bin*

`bin`'s translator is unchanged, as expected, but `bin/py/system.cdy` changes, so this commit is a boot step too. Running the checks:

*ran: Full checks for commit 2*

All checks pass, and `system` is down to 75 built-ins. Now the notes, in the HLD and on B202 (library-layers step 4: the system, revisited), since this continues that step's drops:

*ran: HLD and B202 notes for commit 2*

I committed step 6 as `47bb613` (library-layers step 6: each built-in specified) and tagged it `boot/82`. The tag is annotated and has no staging, and `bootstrap.py --step` passed. That commit also moved the reader off `isspace-at`, and the prelude's `index-of` off `elem-index`. `cmp3` against `boot/81` found only that changed line and renumbered fresh names.

Commit 2, the drops, is built and every check passes; it isn't committed yet.
- **Dropped:** `isspace-at`, `elem-index` and `is-digit`, with their declarations (`src/cdy/system.cdy`), spellings (`src/cdy_rt/spelling.py`) and runtime functions (`src/cdy_rt/primitives.py`), and the test for `isspace-at`. `system` now has 75 built-ins.
- **Replacements:**
  - `tst/cdy/read_sexpr.cdy:46` uses `is-decimal`.
  - The `library.maybe` example uses `find-index` with `=` instead of `elem-index`.
- **Spec:** the index row, table rows and examples for the three are gone (`spec/60-library.md`), and `checking.constraints` no longer lists `elem-index` (`spec/25-checking.md:154`).
- **Notes:**
  - The HLD's step 6 note has a "Then" paragraph. It names the three dropped and what you chose to keep for `stdlib`: the unused basics, and the ones Candy could write over other built-ins.
  - B202 (library-layers step 4: the system, revisited) has a note too.
- **`bin`:** its translator is unchanged, since it no longer called any of the three, but its copy of `system.cdy` changes. So the commit is a boot step and gets `boot/83`. No staging should be needed: commit 1's `bin` reads this library.

**Checks:**
- pytest: 714 passed, 3 xfailed, with no staging warning.
- ruff, mypy, pyright and pylint are clean.
- No tokens in the diff.

All the changes are mine. On "gawc" I'll commit it, run `bootstrap.py --step` and tag `boot/83`.

## Owner

> Gawc

## Claude Code

*ran: Commit the drops, check step, tag boot/83*

I committed the drops as `db3c05a` (library-layers: isspace-at, elem-index and is-digit dropped) and tagged it `boot/83`. The tag is annotated and has no staging, and `bootstrap.py --step` passed (`ok 83`). The working tree is clean.

Still not pushed: master `93c4b5e`, `library-layers` (eight commits, up to `db3c05a`), and tags `boot/77` to `boot/83`.

Next is the last step, B205 (library-layers step 7: docs). It covers `CLAUDE.md`, marking the epic's fifth branch *done in part*, `library.md`'s "What a program sees", `multi_target.md`, and "Looking back". Say "go" to start.

## Owner

> Go

## Claude Code

*ran: Read B205 and doc outlines*

*ran: Find Looking back precedents and epic status*

*ran: Read epic entry and namespaces' Looking back*

*ran: Read library.md section and multi_target mentions*

*ran: Read multi_target's system section*

I've read the precedents and the target docs. Now I'm checking `CLAUDE.md` for anything stale after this branch, before writing.

*ran: Find stale spots in CLAUDE.md and the epic triage*

*ran: Read Modules bullet, triage rows, B108*

*ran: Namespaces status line, triage rows, history*

I have what I need. Writing the docs now, starting with `CLAUDE.md`:

*ran: Update CLAUDE.md*

Checking that `import`'s lookup order is as I described:

*ran: Read import-path*

That's correct. Now the epic's fifth branch and its triage rows (`python_complete.md`):

*ran: Check triage items' states*

*ran: Update python_complete, library.md, multi_target.md*

*ran: Refine multi_target note*

Now the HLD: its status, step 7's Done note and "Looking back".

*ran: HLD status, step 7 note, Looking back, B205*

The HLD now says "Steps 2a and 2b … did need `old-library`", and I'm checking that against step 2's Done note:

*ran: Find 2a's staging note*

*ran: Read 2a's staging reason and my paragraph*

That sentence oversimplifies 2a: it needed `old-library` for a different reason than 2b. The bullet's headline doesn't fit both cases either. Rewriting it:

*ran: Rewrite the bootstrap lesson*

Docs only, but I'm running the full test suite to be safe:

*ran: Full test run*

Step 7 is done and every check passes; nothing is committed yet. B205 (library-layers step 7: docs) is in `review`, and the HLD is marked *done*. This step changes docs only, so `bin` is unchanged and there's no `boot` tag.

**What changed:**
- **`CLAUDE.md`:**
  - the history gets a sentence for `library-layers`;
  - "Modules" says `import` falls back to the library, and that `(import system)` is an error;
  - "The library" covers `slurp` reading only the path it's given, and each built-in being specified;
  - the spec bullet mentions the new built-in check.
- **`doc/hl_rqmt/python_complete.md`:** the fifth branch is *done in part*, with the second half named as `stdlib`'s. The triage rows for B50, B32 and B54 say done. B49 is narrowed, and B108 is split across `library-layers` and `stdlib`.
- **`doc/hl_rqmt/library.md`:** "What a program sees" has a *done in part* note. B, a prelude that re-exports `system`, still waits on re-export, B198.
- **`doc/hl_rqmt/multi_target.md`:** a "Taken further on `library-layers`" paragraph. Declaration modules give a mechanism for a target's own built-ins, not yet a layout.
- **The HLD** (`doc/hl_rqmt/library_layers.md`): its status is *done*, step 7 has its Done note, and there is a new "Looking back" section with five lessons. The main ones:
  - The Bootstrap section's predictions were wrong three times. Running the chain found each case before tagging.
  - Importing `system` as a real module would have broken shadowing; qualified-only entries didn't.
  - Writing each built-in's spec was a review in itself: it led to three more drops.

**Checks:**
- pytest: 714 passed, 3 xfailed.
- No tokens in the diff.

All the changes are mine. On "gawc" I'll commit it.

Still to do after that:
- **Reviews** waiting for your tick: B196, B201, B202, B203, B204 and B205, plus B54.
- **Before the merge:** `pytest -m bootstrap`. The merge into master needs its own "gawc".
- **The tag:** the merge gets an annotated `library-layers` tag.

## Owner

> When's B198 slated ?

## Claude Code

*ran: Read B198 and where it is referenced*

B198 (Re-export, so a program can see only the prelude) isn't scheduled for any branch. It's an `idea` with `low` priority, and it isn't in `python_complete.md`'s triage table.

Your answer to the HLD's Question 6 (`doc/hl_rqmt/library_layers.md:401`, 2026-11-15) is what left it open: both the system and the prelude are imported implicitly *for now*, and re-export comes "when the standard library shows it is needed". The item's note (`backlog/B198-*.md`) and `library.md:147` repeat that condition.

The natural place for it is `stdlib`, the second half of the epic's `library` branch. That branch splits the built-ins into modules (`list`, `string`, `map`, `io`) and trims the prelude. That's where the question becomes real: does a program see `system` directly, or only a prelude that re-exports what programs need? The target extensions point the same way. If each target's `system` differs underneath, as B97 (a library per target) expects, one shared prelude interface starts to pay.

So when `stdlib`'s HLD is written, it should answer it either way: take B198 in, or say why not yet. I can add it to the epic's triage table with that target in this step's commit, if you like:

`| [[B198]] re-export | L | stdlib (decide) |`

## Owner

> What to you think.... Maybe it's not needed at all... And it would just be more confusing at this point... Initially I thought it would make things clearer

## Claude Code

I think you're right: drop it. Here is my reasoning.

**What B198 was for.** The idea was to give every target one fixed interface, the prelude, while each target's `system` could differ underneath. This branch solved that problem another way:
- `system.cdy` is already target-neutral. It holds only Candy types; what's per target is the spellings (`spelling.py`) and the runtime.
- What really differs by target doesn't belong in `system` at all. It goes in a target extension such as `py`, a declaration module a program imports by name (the `multi_target.md` note I just wrote).

So `system` *is* the portable interface. A prelude re-exporting it would put a second name on the same thing.

**What it would cost.**
- Where a name comes from would become indirect. Is `len` the prelude's, or `system`'s seen through the prelude?
- It would add a layer to the shadowing rules, and to qualified names: is it `prelude.len`, `system.len`, or both?
- Error messages would have to say which one they mean.

That's the confusion you're sensing, and Candy pays it on every name for a benefit it already has.

**The precedent was overstated.** B198 cites "OCaml's `Stdlib` and Elm's core". OCaml fits, since `Stdlib` really is a module that re-exports. But as far as I recall, Elm has no re-export at all: it imports a fixed default list of modules implicitly, which is what Candy does now with `system` and the prelude. That case is evidence *for* today's design.

**What it would still give.** Two smaller things, neither of which needs B198:
- A wrapped built-in, such as an `at` that returns a `Maybe`, is just an ordinary prelude or `stdlib` function under its own name.
- Re-export in general, so a user's module could pass on another module's names, could matter some day. That would be a feature request of its own, if a real program ever needs it, not the reason for this item.

**What I'd do,** in this step's commit, with your say-so:
- Set B198 to `dropped`, with a note giving the reasons above in your words and mine.
- Update `library.md`'s "What a program sees", keeping the old text verbatim in the note. It has to say that B is dropped and that `system` is the interface, rather than "B still needs re-export".
- Update the HLD's Question 6 answer, which links B198 as *for now*, the same way.

Shall I go ahead?

## Owner

> Should we combine them?

## Claude Code

If you mean combining `system` and the prelude into one module, I wouldn't. To a program they already act as one: both are imported implicitly, and nobody writes an import for either. The split exists for the translator and for other targets, and it does real work there.

**`system` is declarations only.** It's a declaration module: every form is a bodiless `sig` or `deft` that the host provides, checked against each target's spellings. That rule is what lets a second target replace `spelling.py` and the runtime, and nothing else.

**The prelude is ordinary Candy:** `rest`, `find`, `Maybe`, `Result` and the rest. It's the same on every target, because it's built on `system`.

Merging them would break one of these two things:
- Candy definitions in `system` would end the "declarations only" rule, so a target would have to tell what to provide from what to compile.
- Declarations in the prelude would make it a declaration module, so it could no longer hold code.

The only place a program can see the split is in qualified names: `system.len`, but `prelude.find`. That's minor and honest about where each name comes from. Hiding it would need re-export, which is what we're dropping.

The real tidying belongs in `stdlib`. That's where the prelude gets trimmed, with much of it moving into `list`, `string` and `map` modules. The prelude may shrink to little more than `Maybe` and `Result`. Whether it should exist at all is a fair question for that HLD.

If you meant combining the B198 drop with step 7's docs into one commit: yes. That's what I'd proposed, since both only change docs and the backlog.

Shall I make the B198 changes in step 7's commit, and add "should the prelude exist?" to `doc/brainstorm.md` for `stdlib`?

## Owner

> B198 drop with step 7's docs into one commit: yes... Agree, what's left? For 205

## Claude Code

Doing the B198 drop now. First, how an earlier dropped item records it:

*ran: See a dropped item, brainstorm tail, Q6*

*ran: Drop B198, revise docs, add brainstorm entry*

*ran: Check Not goals line and spec mentions*

*ran: Check remaining re-export mentions*

Adding a line to B205's note so it records the drop:

*ran: Note B198's drop on B205*

I've dropped B198 (Re-export, so a program can see only the prelude), and those edits are now part of step 7's uncommitted changes:
- **`backlog/B198-reexport.md`:** `state: dropped`, with a dated note. The note gives your reason (it would make things more confusing) and mine: `system` is already the one interface, and what differs by target goes to an extension. It also says Elm has no re-export, as far as I recall.
- **`doc/hl_rqmt/library.md`:** the "What a program sees" note now says B is dropped.
- **The HLD's Question 6** (`doc/hl_rqmt/library_layers.md:402`): a *Revised* line says both modules are implicit, *lasting*, and re-export is dropped. The original answer stays above it.
- **`doc/brainstorm.md`:** a new entry, "does the prelude need to exist?", for `stdlib`'s HLD. It also records why `system` and the prelude stay apart.
- **B205:** a note that B198 went in this commit.

**What's left for B205:** nothing more to build. The doc and backlog tests pass, and no tokens are in the diff. It just needs your review, then "gawc" to commit. The commit is docs only, so there's no `boot` tag.

**Then, to finish the branch:**
1. **Reviews** waiting for your tick:
   - B196 (a type with the same name as a built-in type can't be shown) and B54 (`slurp` searches `src/`, `tst/` and `lib/` when a path is missing);
   - B201 to B205, the step tasks for steps 3 to 7.
2. **`pytest -m bootstrap`**: the full chain, run before merging.
3. **The merge into master**, which needs its own "gawc", then the annotated `library-layers` tag.
4. **Pushing**, only when you ask.

## Owner

> Tick, gawc

## Claude Code

*ran: List items in review*

*ran: Tick the review items*

All seven are ticked. Committing step 7:

*ran: Commit step 7*

*ran: Run the full bootstrap chain*

The bootstrap chain is running. Meanwhile, I'm drafting the merge message, following the format of earlier merge commits:

*ran: Read namespaces merge message and tag*

*ran: Draft the merge message*

I've committed step 7 as `1b1aa47` (library-layers step 7: docs), with B198 dropped and your ticks on B54, B196 and B201 to B205. The working tree is clean. The commit changes only docs and the backlog, so it has no `boot` tag.

`pytest -m bootstrap`, the full chain from `self-host-py` to today's `bin`, is still running in the background. I'll report its result when it finishes.

The merge message is drafted in `/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/scratchpad/merge.txt`. It follows the `namespaces` merge's format and lists:
- each step with its backlog items, and the 14 built-ins dropped (75 left);
- B198 dropped;
- boot steps `boot/77` to `boot/83`, and that `pytest -m bootstrap` passes. That last line is only true once the run passes.

If the chain passes, "gawc" will:
1. check `git status` for any edits of yours;
2. switch to master and run `git merge --no-ff refs/heads/library-layers -F merge.txt`;
3. add the annotated tag `library-layers` on the merge.

Nothing gets pushed until you ask.

## Claude Code

*ran: Read bootstrap result*

`pytest -m bootstrap` passed (1 passed, in 4 min 22 s). That means every step from `self-host-py` to today's `bin` rebuilds, `boot/77` to `boot/83` included. The merge message's line saying so is now accurate.

The branch is ready to merge into master. On "gawc" I'll:
1. check `git status` for any edits of yours;
2. switch to master and run `git merge --no-ff refs/heads/library-layers` with the drafted message (`/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb82/scratchpad/merge.txt`);
3. add the annotated tag `library-layers` on the merge.

Nothing gets pushed until you ask.

## Owner

> Gawc, push
