*Archived 2026-11-21, from the two Claude Code sessions that built branch `stdlib`
(2026-11-18 to 2026-11-21; HLD `doc/hl_rqmt/stdlib.md`, tag `stdlib`), by
`script/chat_archive.py`, before the merge.* The owner's messages and Claude's replies on
the branch, verbatim; each tool call is a one-line marker, and thinking and tool output
are left out. The first part is the end of the earlier session: Claude creating the
branch and drafting the HLD (the owner asked for it on `master`); the second is the
session that answered its questions and built it, which began by repeating the first's
last reply (left out here). A notice of a background job finishing, which the harness
writes as the owner's turn, is left out.
What came of it: the modules `math`, `string`, `map` (its lookup `map.at`, Question 4
revised), `list` and `test`; the declaration modules from the spellings; the prelude's
costs ([[B66]], [[B62]]); a top-level `do` spliced; an unlisted name giving way to a
built-in; [[B214]], [[B215]] and [[B216]] filed; Question 8 tabled (`doc/brainstorm.md`,
"is `system` only the language?"); and "Looking back".

# stdlib

## Claude Code

I created the `stdlib` branch from master. Now I'm reading what the epic says about this half, and the items it was given.

*ran: Read the epic's library section*

*ran: Read rest of epic testing and questions*

*ran: Read the exit test and Q5-Q8*

*ran: Read stdlib-related backlog items*

*ran: Read prelude and cost measurements*

*ran: Survey generic helpers in the translator*

*ran: Find string helper candidates*

*ran: Find string helper candidates*

*ran: Read step 1's cost measurements and goals*

*ran: Read programs.import rule*

*wrote: `doc/hl_rqmt/stdlib.md`*

The draft is written. Running the doc-link checks on it; it's a new file, so it needs `git add -N` first:

*ran: Check links and line lengths*

I created the `stdlib` branch from master and wrote the draft HLD, `doc/hl_rqmt/stdlib.md` (228 lines). It's uncommitted, and its doc-link checks pass.

**What it proposes:**
- **Modules for the groups** (B108, the built-ins are one flat namespace):
  - `string`, `map` and `math` become library modules. Their built-ins lose their prefixes: `str-len` becomes `string.len`, `map-get` becomes `map.get`. Each also gets a little Candy, such as `string.trim` and `map.update`.
  - The list built-ins stay in `system`, since they're everywhere (`len` 263 uses, `at` 296), and a `list` module holds Candy over them (`sort`, `last`, `sum`).
  - The files stay in `system` until `io`.
- **The mechanism first:** a declaration module is found by what it holds, so the `DECLARATION_MODULES` list goes. Built-ins are keyed by module, so `string.len` and `len` can both exist.
- **The prelude trimmed** to `Maybe`, `Result` and `rest`. Its costs get fixed:
  - B66: reading the built-ins is 62% of a translation; they would be read once per translation instead.
  - B62: the prelude's macros would be compiled once per translation, not per module.
  - B68: only the prelude a program uses would go into its Python, if that's cheap.
- **A `test` module:** `deftest`, a `check` macro that reports the failing expression's text and position, and `test.run` for `main`'s exit status. The modules test themselves with it.
- **Not in this branch:** the I/O refactor (B95), the `py` extension, `parse`, and interfaces.
- **Steps (8):** the mechanism, the costs, `test`, `math`, `string`, `map`, `list`, docs. Each module's move takes the translator with it; that's about 425 call sites, changed mechanically.

**The questions** (each with my recommendation):
1. **Scope:** do it all as listed, or split the costs and `test` into branches of their own? *As listed.*
2. **A module with both built-ins and Candy:** one file, or two (the declarations kept apart)? *One file.* Any bodiless `sig` makes it a declaration module.
3. **How a program imports a module:** a plain `(import string)` would make `string.len` shadow the list's `len`. Write `(import string ())` by convention, or add a new rule that an import never shadows a built-in? *The convention, `()`, for now.*
4. **`map`'s name:** `map` (as the type is `Map`) or `dict`? *`map`.*
5. **The Candy parts' contents:** small, as listed, grown as programs need them? *Yes.*
6. **Where the library lives:** stay in `src/cdy/` with the translator's own files, or move to a directory of its own? *Stay, for now.* Moving needs bootstrap staging; I'd file an idea item for it instead.
7. **`test`'s registry:** does a program list its tests for `test.run`, or does `deftest` register them? *Listed.* Candy can't add to a module-level list.

Answer whichever you like, in any order. Once they're settled, the first commit marks the HLD accepted and files a task for each step.

*(The context was summarised here; the turns before it are above.)*

## Owner

> "The list built-ins stay in system, since they're everywhere (len 263 uses, at 296), and a list module holds Candy over them (sort, last, sum)."... can you expand on this... Especially the second part... And also I'm wondering if they belong in `system`... I.e the definition of a "lisp" family language... Just wondering if it's worth a distinction/separation....?

## Claude Code

*ran: Find the list parts of the HLD and system.cdy's declarations*

*ran: Read the HLD's list text and the prelude's definitions*

*ran: Check how core.cdy resolves a qualified name*

On "a `list` module of Candy over them": `system` would keep the list primitives, and a new `list` module would hold only ordinary Candy definitions built on top of them. It would have no bodiless `sig`s and no Python behind it. For example:

```
(defn last (xs) (at xs (- (len xs) 1)))
(defn sum (xs) (fold + 0 xs))
(defn flat-map (f xs) (concat (map f xs)))
(defn partition (keep xs) (Tup (filter keep xs) (filter (fn (x) (not (keep x))) xs)))
;; sort: a merge sort on a comparable, in Candy
```

A program would write `(import list ())` and call `(list.sort xs)`. The rule behind it is the one `system.cdy` already follows: something is a built-in only if it needs the host or the speed (`src/cdy/system.cdy:84`). Everything else is Candy and works the same on every target. The prelude's `find` and `index-of` (`src/cdy/prelude.cdy:22-27`) are already this kind of thing; `list` would just collect more of them in one place.

Other languages split it the same way. Racket has `racket/base` (`map`, `length`, `list-ref`) and `racket/list` (`last`, `partition`, `append-map`), almost the same split as proposed. Haskell has the Prelude and `Data.List`; Clojure has `clojure.core`, with `clojure.string` loaded separately.

**Do the list operations belong in `system`?** I'd separate two questions.

1. **The `List` type: yes, it's part of the language.** The Lisp argument for privileging lists doesn't really apply to Candy. In Lisp, code is made of lists. In Candy, code is `Form`s (`form.cdy`), and `List` is an immutable vector (a Python tuple underneath). But the language still needs `List` for other reasons:
   - rest parameters produce one;
   - `++` appends lists;
   - the built-ins' types use it (`split`, `map-keys`, `join`).

   So the type stays in `system` whatever happens to the operations.
2. **The operations: it's a choice, and there's a cleaner line.** `system` holds three kinds of thing today:
   - **The language:** the types, the operators, `nil`, `fail`, `show` and `text`.
   - **Host primitives:** the lists, the files and the output.
   - **The host's math:** about to move to `math`.

   The cleanest version would be `system` holding only the language, with the list operations in a `list` declaration module that every file imports implicitly, as it does the prelude. Call sites wouldn't change (`len` would still work unqualified), `list.len` would sit beside `string.len`, and one module would hold both the primitives and the Candy extras.

My view is that it's worth writing down, but not doing in this branch:
- **What it costs:**
  - a second implicit declaration import, new machinery next to `with-system`;
  - one more file read per module, which adds to B66 (reading the built-ins is 62% of a translation) and B62 (the prelude's macros compiled per module) at the very moment this branch is trying to fix them;
  - the bootstrap staging for moving about 645 call sites' built-ins.
- **What it buys:** mostly symmetry, since the target still has to provide every one of those primitives either way.
- **When it pays off:** the line between the language and host primitives starts to matter at `io` (B95), when the files leave `system`, or at a second target. At that point `system` would be left with the language plus the lists, and the question decides itself.

So I'd keep the HLD's proposal (list operations in `system`, a Candy-only `list` module) and add **Question 8**: "should `system` be only the language, with the list primitives in an implicitly imported `list`?" I'd propose *not now*, with a brainstorm entry that points at `io`.

Do you want me to add Question 8 and the brainstorm entry to the draft? Or, if you'd rather make the split now, I can rework the proposal around an implicit `list` module.

## Owner

> So, bluf: "candy differs from traditional lisp family like languages do to....."

## Claude Code

Candy differs from traditional Lisps because its code isn't made of its lists. Code is `Form`s (`form.cdy`), and `List` is just an immutable vector, a Python tuple underneath. So the Lisp reason for building lists into the language's core doesn't apply.

What keeps the `List` type in `system` is that the language itself uses it: rest parameters, `++`, and the built-ins' types. Most of the list operations sit in `system` only because the host has to provide them, not because they define the language. Moving them out is a choice of how to organize things, and I'd decide it at `io` (B95, the I/O refactor) or a second target.

## Owner

> Tick your initial recommendations for the stdlib hld... Table our conversation

## Claude Code

*ran: Read the HLD's status and questions, and prior answer format*

*ran: Read brainstorm format and how the last HLD was accepted*

*ran: See the task-item format and the HLD's steps*

*ran: Show the original task item's text*

*ran: Record the answers, table Question 8, file the step tasks, and check*

The answers, Question 8 and the step tasks are in; I'm fixing one line that's too long.

*ran: Show the status lines*

*edited: `doc/hl_rqmt/stdlib.md`*

*ran: Recheck doc links and the backlog, and grep for tokens*

I've recorded your answers and tabled our conversation. The `stdlib` HLD is now accepted, and nothing is committed.

- **The answers:** Questions 1 to 7 each now say "*Answer (2026-11-18, the owner): as proposed.*", and the status line says the HLD is accepted (`doc/hl_rqmt/stdlib.md:3`).
- **Our conversation, tabled:**
  - It's written up as a new Question 8, "Is `system` only the language?" (at the end of `doc/hl_rqmt/stdlib.md`). It opens with the bottom line (Candy's code is `Form`s, not lists, so the Lisp reason for building lists in doesn't hold) and is marked *Tabled (2026-11-18, the owner)*, to decide at `io` (B95, the I/O refactor) or a second target.
  - I also added a matching entry at the end of `doc/brainstorm.md`, so the question is still easy to find after this branch's HLD is done.
- **The step tasks:** I filed one task per step, B206 (stdlib step 1: declaration modules by what they hold, built-ins keyed by module) to B213 (stdlib step 8: docs), as `backlog/B206-stdlib-step-1.md` to `backlog/B213-stdlib-step-8.md`, and rewrote the index. That's more than "tick" asked for, but it's what the last HLD's acceptance commit included; say if you'd rather leave them out.

The doc-link and backlog tests pass (48), no new line is over 90 characters, and the diff has no token shapes. Say "gawc" to commit the acceptance as "stdlib: HLD accepted, B206-B213 its tasks"; after that comes step 1.

## Owner

> Gawc

## Claude Code

*ran: Check the tree for the owner's edits and tokens*

Only my changes are there. Committing:

*ran: Commit the HLD's acceptance*

I committed the HLD's acceptance on `stdlib` as `4dec971` ("stdlib: HLD accepted, B206-B213 its tasks"), and the tree is clean. It holds the accepted HLD, Question 8 tabled, the brainstorm entry and the eight step tasks, B206 to B213.

It doesn't change `bin`, so there's no `boot/NN` tag, and nothing is pushed.

Next is step 1, B206 (stdlib step 1: declaration modules by what they hold, built-ins keyed by module). Say "go" when you want it started.

## Owner

> Go

## Claude Code

*ran: Read step 1's proposal and find the declaration-module code*

*ran: Read the driver and library-builtins*

*ran: Read core.cdy's built-in entries and their reading*

*ran: Read the bootstrap staging mechanism*

*ran: Find where bodiless sigs and declared names are handled*

*ran: Read how names resolve to built-ins and where Prim is used*

Working on step 1. I've read how built-ins are keyed and resolved, and I'm checking where the translator's five built-ins are named directly before changing the keys.

*ran: Find hard-coded uses of the translator's built-in names*

*ran: Read the tests on the library's declarations and the spelling table's end*

*ran: Find the bodiless-sig error and the HLD's mentions*

*ran: Check spelling keys, prim-type, the arity message and the spec's wording*

*ran: Read the spec rule, prim-type, the arity error and old-runtime's build*

Now the edits. First `core.cdy`: built-ins keyed by module.

*ran: Find SYSTEM and global-key in core.cdy*

*ran: Key built-ins by module in core.cdy*

`ends-with` takes the text first; I'll fix that and simplify `declaring-module`.

*ran: Simplify declaring-module*

Next, `include.cdy`: the declaration modules come from the target's spellings instead of a list.

*ran: Derive the declaration modules from the spellings, and key the translator's spellings*

*ran: Read how bootstrap builds an old-runtime bridge*

*ran: Read the rest of the bridge function*

Now the local bridge: the old `bin` with the old runtime translates the new source, then `self_host.py` rebuilds.

*ran: Build the bridge with the old runtime, then rebuild bin*

*ran: Copy the library, build the bridge, then rebuild bin*

`bin` rebuilt. Running the tests:

*ran: Run the test suite*

*ran: Run the test suite*

Three failures, all expected from the change. I'm checking how the bootstrap test handles a staged step:

*ran: Read the newest-step bootstrap test*

The test only knows the `old-library` staging. I'll teach it `old-runtime` too: if the newest step builds with its own runtime, the next step needs `old-runtime`.

*ran: Read the rest of the bootstrap test file*

*ran: Teach the bootstrap test old-runtime, and update the library-error cases*

That edit was mine. Next, the index test over every declaration module, and the spec's wording:

*ran: Extend the index test to every declaration module*

*ran: Format, and read the spec's declaration-module text*

*ran: Update programs.import's declaration-module text*

Those long lines were already there. Now `spelling.py`'s comments:

*ran: Read spelling.py's header*

*ran: Note the keys in spelling.py, then run the linters and checkers*

All five checks pass. Next, comparing the new `bin` with `boot/83`'s:

*ran: Compare the new bin's output with boot/83's*

That's expected: `boot/83` can't read the new runtime, so the comparison needs `boot/83` run with its own. I'm checking how `cmp3` runs it:

*ran: See how cmp3 runs the old translator*

*ran: Read cmp3*

*ran: Let cmp3 run the old bin with the old runtime, and compare*

The outputs are identical on all 102 programs, including the translator itself. Running the full suite in the background while I write the notes:

*ran: Run the full test suite*

*ran: Read the step's HLD text and the last Done-note format*

*ran: Write step 1's Done note and move B206 to review*

The suite is still running; I'll finish once it reports.

*ran: Show the working tree*

*used ReadNotifications*

The suite is still running. I'll report once it's done.

## Claude Code

*ran: Read the test result and grep the diff for tokens*

Step 1, B206 (stdlib step 1: declaration modules by what they hold, built-ins keyed by module), is built, and B206 is in review. All the tests pass (715 passed, 3 xfailed), as do ruff, mypy, pyright and pylint. Nothing is committed.

**One deviation from the HLD:** the translator doesn't find declaration modules by reading each library file. It takes them from the runtime's spelling keys instead (`declaration-modules`, `src/cdy/include.cdy:226`): every `m.name` key in `spelling.py` makes `m` a declaration module.
- **Why:** reading and parsing every library file on each translation would add to B66 (reading the built-ins is 62% of a translation), and Candy has no way to list a directory.
- **Which way to choose:** either keep this, or have me read each library file instead, which would also need a new directory-listing built-in in `translator.cdy`.
- **Mixed files:** a declaration module still holds only bodiless forms. Letting one hold Candy too (your Question 2 answer) comes with step 4, `math`, the first module that needs it.

**What changed:**
- **Keys:** a built-in is now keyed by its module and name (`builtin-key`, `src/cdy/core.cdy:357`), except that `system`'s keep their bare names. In practice only the translator's five change, to `translator.fresh-name` and so on (`src/cdy_rt/spelling.py:202-215`).
- **`core.cdy`:** names now resolve to built-ins by these keys (`declared-name`, `declaring-module`, `read-sigs`), and `DECLARATION_MODULES` is gone.
- **Spec:** `programs.import` now says what the declaration modules are and how their built-ins are keyed (`spec/10-programs.md:247`).
- **Tests:**
  - The built-in index test now covers every declaration module except `translator` (`declared_builtins`, `tst/py_cdy/test_doc_links.py:153`).
  - In `test_library_errors`, a `len` declared in `translator.cdy` is no longer "already declared" (it's `translator.len`); a second `fresh-name` is.
  - `test_newest_step_reads_the_library` now also tries the step's own runtime, and warns when the next step needs `old-runtime` (`tst/py_cdy/test_bootstrap.py:41`).
- **Notes:** the HLD's step 1 has its *Done* note (`doc/hl_rqmt/stdlib.md:186`).

**Checks:**
- **Bootstrap:** `boot/83` can't read the new keys, so this commit needs the `old-runtime` staging. I built `bin` that way locally, then rebuilt it with `self_host.py`.
- **Output compared:** `boot/83`, run with its own runtime, gives the same output as the new `bin` on all 102 programs, the translator included.
- **The one warning:** the test run's only warning is that new one, saying the next step needs `old-runtime`. That's what I expected.

On "gawc" I'll commit, add the commit to `STAGING` as `old-runtime`, run `bootstrap.py --step` and `--tag` (it gets `boot/84`), and check the tag is annotated.

## Owner

> "directory-listing built-in in translator.cdy.".... Is a "search" for cdy files?

## Claude Code

Not a search like the one we took out of `slurp`. That walked a list of directories looking for one file by name. This would list a single directory the translator already knows, the library's (`bin/py/`, `library-dir`), and keep the names ending in `.cdy`. There's no path list and no recursion.

What it would cost is the next part. A file's name doesn't say whether it's a declaration module, so the translator would have to read and parse each listed `.cdy` file on every translation to check for a bodiless `sig`. That's about six files now, and twelve or so once `string`, `map`, `math`, `list` and `test` exist. B66 (reading the built-ins is 62% of a translation) is already that kind of cost.

I'd keep the spellings approach. The runtime has to provide every built-in anyway, so its keys already say which modules are declaration modules; asking the files again would only repeat that. If a library file ever declares a built-in the spellings don't name, it still fails clearly: `read-sigs` says the name has no Python mapping, or analysis gives "sig for x, but no def". Say if you'd rather have the listing, and I'll switch.

## Owner

> So it's looking only for bodyless sigs?

## Claude Code

Under the listing approach, yes. It would read each `.cdy` file in the library and count any file with a bodiless `sig` as a declaration module. (Bodiless `deft`s, the built-in types, are only allowed in `system.cdy`, which is always read anyway.)

Under what's built now, the translator doesn't scan files for anything. It goes the other way:
1. The spelling keys name the modules: `translator.fresh-name` makes `translator` one.
2. `library-builtins` reads only those modules' files, plus `system.cdy`.
3. `read-sigs` then requires every form in them to be a bodiless `sig`, and fails on anything else ("expected (sig name Type)").

So the translator only reads a file it has been told is a declaration module, and checks that it holds nothing but declarations. In step 4 that check loosens: a declaration module may also hold ordinary Candy, and only its bodiless `sig`s become built-ins.

## Owner

> I feel like we've been here before...

## Claude Code

*ran: Search past HLDs for the declaration-module finding discussion*

*ran: Read library-layers' declaration-module definition and step 2's note*

Yes, we have. This is the third time the definition has been written one way and built another:

1. **The `library-layers` HLD** defined a declaration module by what it holds: "a library module whose every top-level form is a bodiless `sig` or `deft`" (`doc/hl_rqmt/library_layers.md:77`).
2. **Its step 2a didn't build that.** It added a list, `DECLARATION_MODULES`, because finding modules by their contents meant reading every library file (`library_layers.md:222`).
3. **The `stdlib` HLD said "found by what it holds" again** (`doc/hl_rqmt/stdlib.md:77`). Your Question 2 answer then changed what "holds" means to "any bodiless `sig`", and this step built neither: it uses the spelling keys.

The cost is the same every time: telling a module by its contents means reading every library file. So the practical answer has always been to name the modules somewhere, first in a list and now in the spelling keys.

I'd settle it by changing the definition rather than the code. A declaration module is a library module the target provides built-ins for; its bodiless `sig`s say each built-in's type. "Bodiless `sig`s only" stays a rule about what such a module may hold (loosened in step 4); it stops being how the translator finds one. I'd update the stdlib HLD's proposal (`stdlib.md:77`), `programs.import`, and step 1's *Done* note to say so, so the docs and the code agree and it doesn't come up a fourth time.

Shall I make that change?

## Owner

> What about system and prelude?

## Claude Code

Neither one is found the way `translator` is, and neither needs to be.

| File | What it is | How the translator finds it | Who sees it |
|---|---|---|---|
| `system.cdy` | a declaration module | by name; its spelling keys are bare (`len`), and a bare key means `system` (`builtin-key`) | every file, implicitly |
| `translator.cdy` | a declaration module | its spelling keys (`translator.fresh-name`) | a file that imports it |
| `prelude.cdy` | an ordinary Candy module, no built-ins | by name (`prelude-module`, `include.cdy:55`) | every file but itself and the declaration modules, implicitly |
| `form.cdy` | an ordinary library module | by name, when a file imports it | a file that imports it |
| `special.cdy`, `prelude_macros.cdy` | not modules (`NOT_MODULES`); the translator reads them itself | by name | — |

- **`system`** fits the new definition: the target provides its built-ins. It's found by name because every file imports it, so there's nothing to discover. Its bare keys could become `system.len` so that every key names its module. I wouldn't do it: it would rename all 75 of its keys, for no change in behaviour.
- **The prelude** isn't a declaration module under either definition. It holds Candy, the same on every target, and the target provides nothing for it. That's the line the brainstorm entry already draws ("does the prelude need to exist?"). It stays as it is: found by name, imported implicitly.

So the names the translator hard-codes are `system`, `prelude`, `special` and `prelude_macros`: the language's fixed points, which a program can neither add to nor replace. Everything else is found by a rule: a declaration module by its spelling keys, any other library module by its file name. After `stdlib`, `string`, `map` and `math` will be declaration modules like `translator`, and `list` and `test` ordinary modules like `form`.

If that sounds right, I'll use this table in the definition change I offered (the stdlib HLD's proposal, `programs.import`, step 1's *Done* note), so the file roles are written down in one place.

## Owner

> Ok, stick with your original deviation... What else is needed?

## Claude Code

*ran: Find the docs that still say "by what it holds"*

I'll make the docs match the deviation. Following the navigation rule, the old wording is kept verbatim in a revision note.

*ran: Reword the HLD's proposal and B206's title, keeping the old text*

*ran: Reword the last mention of finding by contents*

The deviation stays, and the docs now say the same as the code (uncommitted):
- **The HLD's proposal** now says declaration modules are found from the spellings. I added the table of the library's files (what each is, how it's found, who sees it) and a *Revised (2026-11-19)* note. The note keeps the old paragraph verbatim and records that `library-layers` had proposed the same thing and built a list instead (`doc/hl_rqmt/stdlib.md:73`).
- **The step's own wording** now says "from the spellings": the bootstrap line, the spec-changes line and step 1's heading.
- **B206's title** is now "Declaration modules from the spellings, built-ins keyed by module", with the old title kept in a note.

The doc-link and backlog tests pass. Since your last view, only those three docs and the backlog index have changed; the code, `bin` and the tests are as I reported.

Nothing else is needed for step 1. On "gawc":
1. Commit step 1.
2. Add the commit to `STAGING` in `script/bootstrap.py` as `old-runtime`.
3. Run `python script/bootstrap.py --step <hash>`, then `--tag`, which gives `boot/84`.
4. Check that `boot/84` is an annotated tag.

The `STAGING` line has to name the commit's hash, so it can't go into step 1's own commit. Last branch, I believe it went into the next step's commit; say if you'd rather have a small commit of its own.

## Owner

> Gawc

## Claude Code

*ran: See how the last staging line was committed, and check the tree*

That staging line went into the next step's commit (`9b2dabd`), so I'll do the same: the edit stays uncommitted and goes into step 2's commit. Only my changes are in the tree. Committing:

*ran: Commit step 1*

*ran: Add the step to STAGING and check its bootstrap step*

*ran: Tag boot/84, check it's annotated, and rerun the bootstrap tests*

Step 1 is committed as `19736fc` ("stdlib step 1: declaration modules from the spellings, built-ins keyed by module") and tagged `boot/84`.

- **Bootstrap:** `bootstrap.py --step` passes, with the `old-runtime` staging in 6 s. The `boot/84` tag is annotated, and its message records "staging: old-runtime".
- **Tests:** the bootstrap tests pass (4), and the warning about needing `old-runtime` is gone now that `boot/84` is the newest step.
- **Left uncommitted:** the `STAGING` line for `19736fc` (`script/bootstrap.py:66`). It goes into step 2's commit, as last branch's did.
- **Backlog:** B206 (stdlib step 1: declaration modules from the spellings, built-ins keyed by module) is in review.
- **Not pushed.**

Next is step 2, B207 (stdlib step 2: the prelude's costs). It fixes B66 (the built-ins read once per translation) and B62 (the prelude's macros compiled once per translation), with times before and after, plus B68 (only the prelude a program uses goes into its Python) if that's cheap. Say "go" when you want it.

## Owner

> Go

## Claude Code

*ran: Read the three cost items and what the HLDs measured*

*ran: Read the planned fixes, how the costs were measured, and library-builtins' callers*

First the "before" numbers, then the code paths. I'm timing `bin` on three programs and counting the `library-builtins` calls:

*ran: List the test programs*

*ran: Time bin on four programs and profile the built-ins' reads*

Before: `library-builtins` runs 11 times for `modules.cdy` (61% under the profiler), 23 times for the translator. Now the expansion code:

*ran: Read expand.cdy's expansion and macro loading*

*ran: Find every caller of the macro-expansion entry points*

*ran: Thread an Expander through expansion, built once per translation*

Rebuilding `bin` (no runtime change this time, so no bridge):

*ran: Rebuild bin*

*ran: Time and profile the new bin*

*ran: Run the full test suite*

*ran: Read Core's Top and Global shapes*

While the suite runs, sizing B68. `check-order` already follows a definition's references through function bodies, so there may be a walker to reuse:

*ran: Find the definition-order check's reference walker and Core's node kinds*

*ran: Read the uses walker and the Clause/Pattern shapes*

*used ReadNotifications*

Writing the notes while the suite runs:

*ran: Read step 2's HLD lines and task*

*ran: Write step 2's Done note and the backlog notes*

*ran: Read the test result and the long backlog lines*

All 715 tests pass, and the suite now takes 45 s, down from 71. Re-wrapping my two long note lines:

*ran: Wrap the notes, run the checks, and compare with boot/84's output*

*ran: Rerun pylint, show the tree, and grep for tokens*

*ran: Show pylint's message*

*ran: Rename the shadowing variable and recheck*

Step 2, B207 (stdlib step 2: the prelude's costs), is built, and B207 is in review. All 715 tests pass, as do the five checkers, and nothing is committed.

**What changed:**
- **One `Expander` per translation** (`src/cdy/expand.cdy:35`). It's made once in `cdyc.cdy` (`expander`) and carries:
  - the built-ins, which `load-defs` now takes from it;
  - the macro compiler, which `compile-macros` builds once over the built-ins and macro code's imports;
  - the prelude's macros, compiled and loaded once (`new-expander`). Every file's expansion starts from them, replacing `prelude-import`.
- **Effect:**
  - B66 (the built-ins read for every translation) is in review: `library-builtins` now runs once per translation, where it ran 11 times for `modules.cdy` and 23 for the translator.
  - B62 (every module compiles the prelude's macros) is in review.
- **Test:** `translate_macro_code` passes the built-ins and imports to `translate-expanded` (`tst/py_cdy/test_self_host.py:322`).

**Times** (with `bin`, median of 5):

| Program | Before | After |
|---|---|---|
| `modules.cdy` | 0.219 s | 0.119 s |
| `(put 1)` | 0.153 s | 0.114 s |
| `macro_files.cdy` | 0.240 s | 0.134 s |
| the translator | 1.041 s | 0.861 s |

The test suite also dropped from 71 s to 45 s.

**B68 (the whole prelude goes into every program) waits**, as the HLD allows when it's more than a step:
- **What it needs:** a reachability pass over Core, through the functions' bodies, every node's and definition's types (the annotations name them) and each `match` clause's variant. Anything `lower` or `emit` names without a `Global` behind it is also a risk.
- **What it would save:** 49 lines of each program's Python and about 5 ms of its translation.

The design is in its note, and the HLD's step 2 has its *Done* note (`doc/hl_rqmt/stdlib.md:233`).

**Checks:**
- `boot/84`'s `bin` gives the same output on all 102 programs.
- No staging is needed, since the runtime didn't change.

The uncommitted `STAGING` line for step 1 goes into this commit (`script/bootstrap.py:66`).

On "gawc" I'll commit, run `bootstrap.py --step` and `--tag` (it gets `boot/85`), and check the tag is annotated.

## Owner

> Gawc

## Claude Code

*ran: Commit step 2, check its bootstrap step and tag boot/85*

Step 2 is committed as `9d60b73` ("stdlib step 2: the built-ins read once, the prelude's macros compiled once") and tagged `boot/85`.

- **The commit:** it includes step 1's `old-runtime` line in `STAGING`. There were no edits of yours in the tree, and the diff has no token shapes.
- **Bootstrap:** `bootstrap.py --step` passes with no staging, and `boot/85` is an annotated tag. The tree is clean.
- **Backlog:** in review are B207 (stdlib step 2: the prelude's costs), B66 (`special.cdy` and `system.cdy` are read for every translation) and B62 (every module compiles the prelude's macros). B68 (the whole prelude goes into every program) stays open.
- **Not pushed.**

Next is step 3, B208 (stdlib step 3: the `test` module), with `check`, `deftest` and `test.run`, and its own tests. Say "go" when you want it.

## Owner

> Go

## Claude Code

*ran: Read the HLD's test module design*

*ran: Read form.cdy's helpers and the prelude's macros*

*ran: Look for a form printer, and how test programs are run*

*ran: Read how test programs are collected and run, and the LIBRARY list*

*ran: Check how top-level macro expansions are handled*

A macro can't expand to several top-level forms today, so `deftest` couldn't give its test the `sig` every top-level `def` needs. Checking the spec for a top-level `do` and for qualified patterns:

*ran: Search the spec for top-level do and qualified patterns*

Before writing the module, one decision is yours, because it's a language change.

`deftest` needs to define a name, which takes two top-level forms: `(sig splits test.Test)` and `(def splits ...)`, since every top-level `def` needs its `sig`. But a macro expands to one form, and the translator has no way to splice several forms in at top level (`expand-form`, `src/cdy/expand.cdy:293`). Options:

1. **A top-level `do` is its forms, spliced** (recommended). This is Scheme's `begin` rule. `deftest` would expand to `(do (sig splits test.Test) (def splits ...))`, and any macro could define several things.
   - Nothing that works today changes: a top-level `(do (put 1) (put 2))` still runs the same.
   - What changes: a `sig` or `def` inside a top-level `do` becomes legal, while a `do` anywhere else still can't hold one (`spec/10-programs.md:39-44` stay).
   - It's about 10 lines in `expand.cdy`, plus a spec rule with examples.
2. **`deftest` as an expression, not a definition:** `(test.run (List (deftest splits (check ...)) ...))`. There's no language change, but the tests can't be named and reused, and it departs from the HLD's example.
3. **The user writes the `sig`:** `(sig splits test.Test) (deftest splits ...)`. There's no language change either, but it's boilerplate on every test.

Everything else is as the HLD has it:
- `test.cdy` is an ordinary library module with `Check` (`Pass` or `(Fail text pos)`), `Test` and `run`.
- `test_macros.cdy` is a library macro file with `deftest`, and `check`, which writes the expression's text and position.
- The tests are `tst/cdy/stdlib/test_test.cdy`, with `.out` files, which `test_output` checks for exit status 0.
- The spec gets a rule, `library.test`.

Which option do you want?

## Owner

> So deftest is a special form.?

## Claude Code

No. `deftest` stays a macro, in the library macro file `test_macros.cdy`, as `cond` and `put` are in `prelude_macros.cdy`. The translator wouldn't know it exists.

The special form that changes in option 1 is `do`, which already is one. The new rule is that a `do` at top level is its forms, spliced in, so a macro can expand to `(do (sig ...) (def ...))`. Any macro gets that, not just `deftest`: a `defrecord`-style macro could define a type and its helpers the same way.

Making `deftest` a special form would be a fourth option, and I'd advise against it:
- **The translator:** it would have to learn about the `test` module's types (`special.cdy`, `core.cdy`).
- **The test library:** it would become part of the language and of every target, when it's only library code built on macros.

Special forms are for what a macro can't do. Here, the only thing missing is a way for a macro to give more than one top-level form, and the top-level `do` rule adds that once, in the language.

## Owner

> So, is there a way to have  dummy sig and def.... And a second macro that expands them to proper sig and def

## Claude Code

No. A macro call is replaced by exactly one form, and expansion repeats on that form until it isn't a macro call anymore (`expand-form`, `src/cdy/expand.cdy:298`). However the macros are chained, one form at top level ends as one form. Something has to turn one form into two, and only the translator can do that.

There are two places to put it:
1. **A top-level `do` spliced** (my recommendation). The splice happens once, in `expand.cdy`, after expansion. `deftest` expands to `(do (sig ...) (def ...))`, and analysis sees two ordinary top-level forms.
2. **One form that carries both**, such as a `def` with its type inline: `(def splits test.Test (test.Test ...))`. That's a bigger change to the language: a second way to give a type, against the rule that a `sig` is a separate statement, and changes to `core.cdy` and to the spec of `def` and `sig`.

The "dummy" idea comes down to option 1 anyway. The dummy is the `do`, and the "second macro" is the translator's splice, which has to be built in because no macro can produce two forms.

Shall I go ahead with the top-level `do`?

## Owner

> Yes

## Claude Code

Implementing the top-level `do`. First, where the spec's top-level rules are:

*ran: Read the spec's top-level rules*

Writing the splice in `expand-file`. A `defmacro`, `import` or `import-macros` inside the `do` is an error, since those are read before macros expand.

*ran: Splice top-level dos after expansion, with a spec rule*

Now the module itself. First, how spec examples are named when they run, since a failed check's message carries its file's path:

*ran: Check how spec examples are written and translated*

*wrote: `src/cdy/test.cdy`*

*wrote: `src/cdy/test_macros.cdy`*

*ran: Add the files to the library, and try a test program with T1*

It works first time, with T1: the failures are written with their positions, then the count, and the exit status is 1. Now the module's own tests and the spec rule:

*ran: Write the test module's own tests, and run them*

A list can't hold mixed literals. I'll use a tuple, and add the test I left out of `main`:

*ran: Use a tuple of literals, and rerun the tests*

The definition-order check counts a `fn` in a `def` as called, so `literals` has to come before the test that reads it. Reordering:

*ran: Move the literals test before its reader, and rerun*

The framework caught my own mistake: the column I expected is wrong. Computing it:

*ran: Fix the expected column and rerun*

*ran: Use column 39 and rerun*

All 7 checks pass, exit status 0. Next: the expected output, `tst/cdy/stdlib/` in the test programs, and the spec rule.

*ran: Add the stdlib tests to the test programs, and list the library rules*

*ran: Read the library spec's header and its last rule*

*ran: Write the library.test rule and run its example through T1*

*ran: Fix the example's column and run the two spec files*

Both spec files pass (104). Rebuilding `bin`, with the library's two new files copied next to it:

*ran: Copy the library into bin, rebuild it, and mark the new files*

*ran: Run the full test suite*

*ran: Run the checkers and compare with boot/85's output*

Only the three programs that use a top-level `do` differ, and `boot/85` can't splice, so that's expected. pylint's line came out blank; checking it:

*ran: Show pylint's result*

*ran: Check backlog priorities, the newest id, and step 3's HLD line*

*ran: Read the test result*

All 725 tests pass. Filing the two items and linking them from the *for now*s:

*ran: File B214 and B215, write step 3's notes, and recheck*

Step 3, B208 (stdlib step 3: the `test` module), is built, and B208 is in review. All 725 tests pass, as do the five checkers, and nothing is committed.

**The top-level `do` you chose** (`splice-dos`, `src/cdy/expand.cdy`): after expansion, a top-level `(do ...)` is replaced by its forms, so a macro can define several things.
- A `defmacro`, `import` or `import-macros` inside one is an error, since those are read before macros expand.
- The rule is `programs.top-do` (`spec/10-programs.md`), with a `defsquare` macro as its example and the three errors.

**The `test` module:**
- **`src/cdy/test.cdy`**, an ordinary library module, holds:
  - `Check`, which is `Pass` or `(Fail text pos)`;
  - `Test`, a name and a function giving its checks;
  - `run`, which writes each failed check as `{pos}{test}: {text}`, then `tests: N, checks: N, failed: N`, and gives 0 or 1;
  - `failures`.
- **`src/cdy/test_macros.cdy`**, a library macro file, holds:
  - `deftest`, which expands to a top-level `do` of its test's `sig` and `def`;
  - `check`, which records the expression's text and position;
  - `form-text`, which writes a form back as the program wrote it.
- **Library:** both files are added to `LIBRARY` (`src/py_cdy/self_host.py`) and copied into `bin/py/`.

**Its tests:** `tst/cdy/stdlib/test_test.cdy` tests the module with itself: 4 tests, 7 checks, including a failure's text and column, and the text of every kind of literal.
- `test_output` now covers `tst/cdy/stdlib/`. It checks that a program exits with 0 and prints its `.out`.
- A failed check's line includes its file's absolute path, so this program checks its failures as values rather than printing them.

**The spec:** the rule `library.test` (`spec/60-library.md`), with a table, an example where one check fails, and `deftest`'s errors. Spec examples are translated from text, so a failure there reads `line 4, column 42: `, which is stable across checkouts.

**New items:**
- B214 (`check`'s text doesn't write a string's escapes back), tech-debt.
- B215 (`deftest` doesn't register its tests), an idea; that's Question 7's "listed, *for now*".

**Checks:**
- **Output compared:** `boot/85`'s `bin` gives the same output except on the three programs that use a top-level `do`, which it rejects, as expected.
- **No staging needed.**
- **Notes:** the HLD's step 3 has its *Done* note.

On "gawc" I'll commit, run `bootstrap.py --step` and `--tag` (it gets `boot/86`), and check the tag is annotated.

## Owner

> Gawc

## Claude Code

*ran: Commit step 3, check its bootstrap step and tag boot/86*

Step 3 is committed as `dcba931` ("stdlib step 3: the test module, and a top-level do spliced") and tagged `boot/86`.

- **The commit:** only my changes were in the tree, and the diff has no token shapes.
- **Bootstrap:** `bootstrap.py --step` passes with no staging, and `boot/86` is an annotated tag. The tree is clean.
- **Backlog:**
  - B208 (stdlib step 3: the `test` module) is in review.
  - B214 (`check`'s text doesn't write a string's escapes back) and B215 (`deftest` doesn't register its tests) are new and open.
- **Not pushed.**

Next is step 4, B209 (stdlib step 4: the `math` module):
- **What moves:** `PI`, `sin`, `cos` and `tan` leave `system`, and `abs`, `min` and `max` are added in Candy.
- **First of its kind:** it's the first declaration module that also holds ordinary Candy (your Question 2 answer), so the translator has to learn to read one.
- **The translator's own code:** nothing in it uses `math`, so none of its calls change.

Say "go" when you want it.

## Owner

> Go

## Claude Code

Step 4 needs two commits, like `library-layers`' 2a and 2b:
- **Why one won't do:** `boot/86`'s `bin` would find `math` through the new spelling keys, then fail on its Candy definitions ("expected (sig name Type)"). Neither staging covers that, since the old runtime and the old library each fail on their own.
- **4a:** the translator learns to read a declaration module that also holds Candy.
- **4b:** `math` moves, read by 4a's `bin`.

Starting 4a:

*ran: Read read-sigs, module-names and def-names*

*ran: Let a declaration module hold Candy*

There's an extra paren in my `let` binding; fixing it, then updating the test row that no longer errors and adding a test of a mixed module:

*ran: Fix the binding, update the tests, rebuild bin and run them*

The mixed module works. Updating `programs.import` to say a declaration module may hold Candy:

*ran: Note it in programs.import and run the full suite*

*ran: Run the checkers and compare with boot/86's output*

*ran: Format the test file and recheck*

Writing 4a's note in the HLD; B209 goes to `in-progress` until 4b:

*ran: Write 4a's note and move B209 to in-progress*

Step 4 has to be two commits, and the first, 4a, is built and uncommitted. All 726 tests pass, and so do the five checkers.

**Why two:** `boot/86`'s `bin` would find `math` through its new spelling keys, then fail on its Candy definitions ("expected (sig name Type)"). Neither staging helps, since the old runtime and the old library each fail on their own. So 4a teaches the translator to read a declaration module that holds Candy, and 4b moves `math`, read by 4a's `bin`.

**4a, what changed:**
- **Declarations** (`declarations` and `definitions`, `src/cdy/core.cdy`): a declaration module's declarations are each `sig` of a name the file doesn't define, plus each bodiless `deft`. Everything else is ordinary Candy.
- **Reading:** `read-sigs` and `declared-exports` read only the declarations. `system.cdy` stays declarations-only, as before.
- **Expanding:** `expand-modules` (`src/cdy/cdyc.cdy`) expands and analyses a declaration module's Candy like any module's. Its exports include both its definitions and its built-ins (`with-declared`), so its Candy can call its own built-ins unqualified.
- **Spec:** `programs.import` says so.
- **Tests:**
  - `test_a_declaration_module_holds_candy` adds two `defn`s to a copy of `translator.cdy`, one calling a built-in, and checks a program can use them unqualified and qualified.
  - A `test_library_errors` row that had a `def` in `translator.cdy` (no longer an error) now uses a malformed `sig`.
- **Checks:** `boot/86` gives the same output on all 105 programs, and no staging is needed.
- **Notes:**
  - The HLD's step 4 explains the two commits and has 4a's *Done* note.
  - B209 (stdlib step 4: the `math` module) is `in-progress` until 4b.

On "gawc" I'll commit 4a and tag it `boot/87`, then build 4b.

## Owner

> Gawc

## Claude Code

*ran: Commit 4a, check its bootstrap step and tag boot/87*

4a is committed as `ae95d09` and tagged `boot/87`. Now 4b: the `math` spec rule and the four spellings.

*ran: Read the math rule, spellings, and other mentions*

*ran: Find other uses of the four math built-ins*

Only `tst/cdy/t1/basics.cdy` uses one, `PI`. Writing `math.cdy`, moving the four, and checking how `abs` types on a `number`:

*ran: Write math.cdy, move the four out of system, and update basics.cdy*

*ran: Import math in basics.cdy, add math.cdy to the library, and try it*

Everything works. Now the spec rule, the index row, and a comment on `spelling.py`'s `MATH`:

*ran: Rewrite library.math for the module, and run the library spec*

The translator already gives a better error than I expected. I'll specify that one:

*ran: Fix the expected error, rebuild bin, and run the full suite*

*ran: List the failures*

The error's list of files now includes `math.cdy`. Checking its order, and what the index test says:

*ran: Show the two failures' details*

*ran: Count only bodiless sigs as built-ins, and loosen the error tests*

Adding a check that `builtin_names` skips a defined name, then the full suite, the checkers and the comparison:

*ran: Run the full suite, the checkers and the comparison with boot/87*

*ran: Write 4b's note and move B209 to review*

4b is built, and B209 (stdlib step 4: the `math` module) is in review. All 728 tests pass, as do the five checkers, and nothing is committed.

**What changed:**
- **`src/cdy/math.cdy`**, the first declaration module that also holds Candy:
  - it declares `PI`, `sin`, `cos` and `tan`, which leave `system.cdy` (71 built-ins left) and are spelled `math.PI` and so on in `spelling.py`;
  - in Candy it defines `abs` on a `number` (`(- x x)` stands in for zero, since a literal `0` would make it `Int`), and `min` and `max` on a `comparable`;
  - it's added to `LIBRARY` and copied into `bin/py/`.
- **The spec:** `library.math` is rewritten for the module, with a table, examples of all seven, and two errors. Writing `sin` without the import gives "sin is declared by math, which this file doesn't import: (import math)". The index row now lists `math.PI` and the rest.
- **Tests:**
  - The index test counts only bodiless `sig`s as built-ins (`builtin_names`, with a check of its own).
  - The `test_library_errors` messages are matched only up to `system.cdy`, so they don't break each time a declaration module is added.
  - `tst/cdy/t1/basics.cdy` imports `math` for `math.PI`.

**Checks:**
- **Output compared:** `boot/87`'s `bin`, given the new library and runtime, gives the same output on all 105 programs, so 4b needs no staging.
- **`bin`:** the translator's own Python is unchanged, since it uses none of `math`. `bin/` still changes (`system.cdy`, plus the new `math.cdy`), so this commit gets a tag, `boot/88`.

On "gawc" I'll commit 4b, run `--step` and `--tag`, and check the tag is annotated. Next is step 5, `string`, the first step that moves the translator's own calls.

## Owner

> Gawc

## Claude Code

*ran: Commit 4b, check its bootstrap step and tag boot/88*

4b is committed as `b15d1fb` ("stdlib step 4b: the math module") and tagged `boot/88`.

- **Bootstrap:** `bootstrap.py --step` passes with no staging, and `boot/88` is an annotated tag. The tree is clean.
- **Backlog:** B209 (stdlib step 4: the `math` module) is in review.
- **Not pushed.**

Next is step 5, B210 (stdlib step 5: the `string` module):
- **The renames:** the string built-ins move to `string` with their prefixes dropped: `str-len` becomes `string.len`, `char-at` `string.at`, `substring` `string.slice`, `str-contains` `string.contains`, and the rest. Candy's `trim` and `lines` are added.
- **The translator moves too:** its own source calls these about 115 times, and every call changes, mechanically.
- **Bootstrap:** the old `bin`'s own Python still calls the old primitives, so a renamed built-in keeps its Python function. Moving the translator off the old names and dropping them may again need two commits.

I'll check the bootstrap case first, before changing any calls. Say "go" when you want it.

## Owner

> Go

## Claude Code

Step 5. First the names (the HLD's), and how many places use them:

*ran: List the string built-ins and count their uses by area*

*ran: Find the string built-ins named in quotes*

No special cases, only the spellings. Now the Candy written inside the Python tests:

*ran: Find Candy calls of them in the Python tests and the editor grammar*

None in the Python tests or the editor grammar. One more trap: `format` holes put Candy inside strings, so a rewrite that skips strings would miss them. Checking for any:

*ran: Find string built-ins inside format holes*

Ten uses in `format` holes, all calls, so the rewrite will handle holes too. Next, whether the library's macro-code files use any of them, since macro code can't import a module:

*ran: Check which library files use the string built-ins*

*wrote: `tmp/c7/strmove.py`*

*ran: Rename the string built-ins across the translator, tests, spec and backlog*

The script put `test.cdy`'s import under the comment that belongs to `Check`. Fixing that, and checking where it landed in the other files that had no imports:

*ran: Move test.cdy's import, and show where it went elsewhere*

*ran: Move read_sexpr.cdy's import above its first comment, and look at quoting.cdy*

`quoting.cdy` is translated as macro code, which is exactly the case for adding `string` to `macro-imports`. Making that change, and moving `test_macros.cdy` onto `string.join`:

*ran: Read macro-imports*

*ran: Give macro code string's built-ins, qualified, and use string.join in test_macros*

Now `string.cdy` itself, and the built-ins out of `system.cdy` and into `spelling.py`'s `string.` keys:

*ran: Read the spellings and system.cdy around the string built-ins*

*ran: Write string.cdy, move the built-ins, and rebuild bin*

*ran: Read use-error and hidden-entry*

*ran: Read use-error's comment and its callers*

*ran: Let an unlisted or private name give way to a built-in, and rebuild*

*ran: Save step 5's changes as a patch, and check it reverses cleanly*

*ran: Reverse step 5's changes, leaving a clean tree*

*ran: Apply only the gives-way rule, and look at the import-list test program*

To test the rule, I'll give `lib/tags.cdy` (imported with `()`) a `len` of its own, and check that `import_list.cdy` still gets the list's `len` unqualified:

*ran: Read lib/tags.cdy and who imports it*

*ran: Add a len to lib/tags, and check import_list gets the system's*

*ran: Read programs.import's name-list text*

*ran: Note the rule in programs.import, rebuild bin and run the suite*

All 728 pass. The spec sentence names `string`, which doesn't exist until 5b, so I'll word it with `tags` for now:

*ran: Reword the sentence, run the checkers and compare with boot/88*

Only `import_list.cdy` differs, which `boot/88` rejects, as expected. Writing 5a's notes:

*ran: Write 5a's notes and move B210 to in-progress*

Step 5 also needs two commits. The first, 5a, is built and uncommitted, and all 728 tests and the five checkers pass.

**Why two:** with `(import string ())`, an unqualified `len` was an error ("len: the import of string doesn't list it") instead of the list's `len`. So Question 3's convention, import with `()`, didn't actually work yet. The translator's own source depends on the fix, so the `bin` that builds it must already have it.

**5a, what changed:**
- **The rule** (`use-error` and `gives-way`, `src/cdy/core.cdy:160`): a name an import doesn't make unqualified, because it isn't listed or the module keeps it private, now gives way to a built-in of the same name.
- **Spec:** `programs.import` says so.
- **Tests:** `tst/cdy/cdyc/lib/tags.cdy` now defines a `len`. `import_list.cdy`, which imports it with `()`, still gets the list's `len` unqualified and `tags.len` qualified (`2 99`).
- **Checks:** `boot/88` gives the same output on all programs except `import_list.cdy`, which it rejects, as expected. No staging is needed.
- **Notes:** the HLD's step 5 explains the two commits and has 5a's *Done* note. B210 (stdlib step 5: the `string` module) is `in-progress`.

**5b is ready to go back in.** The rest of step 5 is saved as a patch (`tmp/c7/step5.patch`):
- `string.cdy`, with 16 built-ins plus `trim` and `lines` in Candy;
- the renames across 16 files: the translator's 128 calls, the spec, and the test programs;
- `macro-imports` giving macro code `string`, qualified only.

On "gawc" I'll commit 5a and tag it `boot/89`, then reapply 5b on top and finish it.

## Owner

> Gawc

## Claude Code

*ran: Commit 5a, check its bootstrap step and tag boot/89*

5a is committed as `44b9dd1` and tagged `boot/89`. Now reapplying 5b. `core.cdy` and `programs.import` changed in 5a, so I'll apply the patch without those two and rerun the rename on `core.cdy`:

*ran: Reapply 5b without the two files, and redo core.cdy's renames*

Rebuilding with 5a's `bin`:

*ran: Copy the library into bin and rebuild*

*ran: Find the old names the rename missed*

*ran: Handle char literals in the rename script, and rerun it*

Only `read.cdy` had more to rename. Rebuilding:

*ran: Rebuild bin*

*ran: Check core.cdy's imports*

The import check matched the text `(import string ())` in 5a's comment, so `core.cdy` never got the import. Adding it by hand:

*ran: Import string in core.cdy and rebuild*

The translator builds on the `string` module. Running the suite:

*ran: Run the full test suite*

Five failures. Looking at each:

*ran: Show four of the failures' details*

*ran: Show the index failure, README uses, and the index table*

The index and `library.strings`' prose and tables still use the old names, since the script only touched code. Here's the rule:

*ran: Read library.strings and other prose mentions*

*ran: Find every remaining mention of the old names in the spec*

The panic messages still name `substring`, which no longer exists in Candy. Checking how the runtime words them:

*ran: Find the runtime's out-of-range messages*

I'll make them `string.at:` and `string.slice:`, the names a program writes, and fix the rest of the spec at the same time:

*ran: Read the prose to change and the tests on the messages*

*ran: Rewrite library.strings, fix the spec's other mentions and the messages*

*ran: Update read_sexpr's output and rerun the suite*

All 729 pass. Checking the bootstrap warning, the checkers, comments in the translator that still use the old names, and the comparison with `boot/89`:

*ran: Run the bootstrap tests and checkers, and find old names in comments*

Only the Python functions keep the old names, on purpose. Comparing with `boot/89`:

*ran: Compare with boot/89's output, count system's built-ins, and time the translator*

*ran: Write 5b's notes and move B210 to review*

5b is built, and B210 (stdlib step 5: the `string` module) is in review. All 729 tests pass, as do the five checkers, and nothing is committed.

**The `string` module** (`src/cdy/string.cdy`):
- **16 built-ins**, all gone from `system.cdy` (55 left): `len`, `at`, `slice`, `contains`, `starts-with`, `ends-with`, `split`, `join`, `repeat`, `replace`, `to-int`, `to-float`, `is-decimal`, `code` (was `char-code`), `hex-char` and `is-space` (was `isspace`).
- **`trim` and `lines`**, defined in Candy, with their helpers private.
- **In `spelling.py`** they're keyed `string.` and keep their Python functions (`substring`, `isspace`), so the old `bin` still runs.
- **Panic messages** use the new names: "string.slice: index out of range".

**The translator moves onto it:**
- Its modules import `(import string ())`, and 128 calls are renamed, as are the spec's examples and the test programs. The rename script skips strings (except `format` holes), comments and char literals. It had two bugs along the way, both fixed:
  - it misread a char literal like `\"`, so it skipped some of `read.cdy`;
  - it took a comment containing `(import string ())` for the import itself, so `core.cdy` never got one.
- **Macro code** now imports `string` implicitly, qualified only (`macro-imports`, `src/cdy/cdyc.cdy:109`), for `test_macros.cdy`'s `string.join`. It gets only the built-ins, not `trim` or `lines`: macro code gets no Candy from the library, as with B52 (macro code doesn't get the prelude).
- **Cost:** the translator still translates itself in 0.86 s.

**The spec:**
- `library.strings` is rewritten for the module, with every call in a table and a new example of `trim`, `lines`, and `len` next to `string.len`.
- The index row now lists `string.len` and the rest.
- The mentions in `library.bounds`, `00-syntax.md`, `25-checking.md` and `spec/README.md`'s indented example are updated.

**Checks:**
- **Output compared:** `boot/89` gives the same output on every program, the translator included, except the two that use `test_macros`; `boot/89`'s macro code has no `string`.
- **Staging:** none needed, and the bootstrap test gives no warning.
- **Notes:** the HLD's step 5 has 5b's *Done* note.

On "gawc" I'll commit 5b, run `--step` and `--tag` (it gets `boot/90`), and check the tag is annotated.

## Owner

> Gawc

## Claude Code

*ran: Commit 5b, check its bootstrap step and tag boot/90*

5b is committed as `2f03ddc` ("stdlib step 5b: the string module") and tagged `boot/90`.

- **Bootstrap:** `bootstrap.py --step` passes with no staging, and `boot/90` is an annotated tag. The tree is clean.
- **Backlog:** B210 (stdlib step 5: the `string` module) is in review.
- **Not pushed.** Six commits and seven tags (`boot/84` to `boot/90`) are local only, so this might be a good point to push.

Next is step 6, B211 (stdlib step 6: the `map` module):
- **The renames:** the map built-ins move to `map`: `map-get` becomes `map.get`, `map-set` `map.set`, and so on.
- **The prelude's `map-update`** becomes `map.update`. `values` and `get-or` are added in Candy.
- **The translator moves too:** it uses the map built-ins about 310 times, more than the strings.
- **Approach:** the rename script is reusable.
- **Bootstrap:** 5a's "gives way" rule already covers `(import map ())`, so I expect a single commit unless the bootstrap finds something.
- **One name to watch:** the module `map` and the list function `map` would share a name. They don't clash mechanically: `map.get` is one symbol, and the function stays a `system` built-in. I'll check that early.

Say "go" when you want it, or "push" first.

## Owner

> Go

## Claude Code

Step 6. One catch first: the `map` module would declare `get`, which is also a special form (`get` on a record's field). Checking how analysis decides a list's head is a special form, since `map.cdy`'s own Candy sees its names unqualified:

*ran: Read how a special form's head is recognised*

*ran: Read with-own and the qualified-names rule*

The plan for 6a: a module's own names are also in its table as `stem.name`, and its own stem is one of its qualifiers (not for macro code, whose stem is `""`). Here's `programs.qualified`:

*ran: Read the qualified-names rule*

*ran: Let a module write its own names qualified, and try it*

Running the full checks for 6a:

*ran: Rebuild bin, run the suite and checkers, and compare with boot/90*

Only the four programs that import `lib/tags` differ, which `boot/90` rejects, as expected. Checking whether any of the long spec lines are mine:

*ran: Show long lines among the spec lines I added*

None are mine. Writing 6a's notes:

*ran: Write 6a's notes and move B211 to in-progress*

Step 6 also needs two commits. The first, 6a, is built and uncommitted; all 729 tests and the five checkers pass.

**Why:** `map.cdy`'s own Candy (`update`, `get-or`, `values`) needs the module's `get`. But `get` at the head of a form is always the special form that reads a field, and a module had no way to write its own names qualified.

**6a is a small rule I chose, which you can veto:** a module may write its own names qualified, as its importers do. So `map.cdy` writes `map.get`. The alternative was a private alias built-in with another name, which would be a hack.
- **Code:** `with-own` adds a module's own names as `stem.name` too, and `own-qualifier` adds its stem to its qualifiers (`src/cdy/core.cdy:1514`). Macro code is left out, since its stem is `""`.
- **Spec:** `programs.qualified` says so.
- **Test:** `lib/tags.cdy`'s `tag` now returns `tags.label`, which the four programs importing it exercise.
- **Checks:** `boot/90` gives the same output on all programs except those four, which it rejects, as expected. No staging is needed.
- **Notes:** the HLD's step 6 explains the two commits, and B211 (stdlib step 6: the `map` module) is `in-progress`.

On "gawc" I'll commit 6a and tag it `boot/91`, then do 6b: the move, with the rename script adapted to the map names.

## Owner

> Can we walk thru some 6a examples and the alternatives?

## Claude Code

The problem 6a solves, in `map.cdy`:

```
(sig get (Fn ((Map k v) k) v))                      ; the built-in, a bodiless sig
(sig update (Fn ((Map k v) k (Fn (v) v)) (Map k v)))
(defn update (m key f) (set m key (f (get m key)))) ; <- this get is the special form
```

Inside `map.cdy`, `(get m key)` is the record field read, because `get` at a form's head is always the special form. So it fails: `m` isn't a record, and `key` isn't a field name. A program has the same problem with `(import map (get))`: it can list `get`, but can't call it unqualified. Only `map.get` works anywhere.

**A. 6a, a module may qualify its own names** (built, uncommitted):
```
(defn update (m key f) (set m key (f (map.get m key))))
(defn get-or (m key fallback) (if (has m key) (map.get m key) fallback))
```
Any module can now write `tags.label` inside `tags.cdy`. It's general and harmless, but it gives every name a second spelling inside its own module, and it costs an extra commit.

**B. A private alias built-in:**
```
(sig lookup (Fn ((Map k v) k) v))   ; spelling.py: "map.lookup", the same Python as map.get
(private lookup)
(defn update (m key f) (set m key (f (lookup m key))))
```
No rule change, but it's a hack: a second built-in that exists only to dodge a name clash, with its own spelling entry, and the index test would have to skip it.

**C. Name the built-in `at`, not `get`** (not in the HLD):
```
(sig at (Fn ((Map k v) k) v))
(defn update (m key f) (set m key (f (at m key))))
;; a program: (map.at m "a"), as (at xs 0) and (string.at s 0)
```
- **No clash and no rule change:** `get` stays only the field read, so step 6 is a single commit.
- **One verb:** lists, strings and maps would all use `at` to give the item at an index or key. That suits interfaces later (B34), where one `at` would work on each.
- **The cost:** it departs from the HLD's `map.get`, and from Clojure's `get`. For `has` and `set`, nothing clashes (`set` isn't a special form; the record update is `assoc`).

**D. Put `map`'s Candy somewhere else**, such as the prelude or a second module. That goes against your Question 2 answer, one file per module, so I wouldn't.

My recommendation is C. It removes the clash at the source instead of working around it, and it makes the three collections consistent. If you agree, I'll undo 6a (nothing is committed) and do step 6 as one commit, with `map.at`. If you'd rather keep `map.get`, A is the cleanest way to get it.

## Owner

> C sounds good ... Any last thoughts on the switch from the previous 6a idea to c?

## Claude Code

A few, none of them blocking:

1. **Undoing 6a is clean.** Nothing is committed, so I'll restore the six files it touched: `core.cdy`, `programs.qualified`, `lib/tags.cdy`, `bin`, the HLD and B211. Nothing else depends on it.
2. **Self-qualification can come back if it's ever needed.** The only case that needed it was a module's own name colliding with a special form, and C removes that case. I'd add one line to `doc/brainstorm.md` ("a module writing its own names qualified, `m.x` inside `m`: built and dropped in `stdlib` step 6 for `map.at`"), so it isn't reinvented from scratch.
3. **`get-or` would be the odd one out.** With `at`, I'd call it `at-or`: `(map.at-or m k fallback)`. Then `update`, `values` and `at-or` sit next to `at`, `has`, `set`, `keys`, `from`, `size` and `empty`.
4. **Inside `map.cdy`, its own `at` shadows the list's.** That's the same situation as `len` in `string.cdy`: its Candy writes `system.at` if it ever needs the list's. `values` doesn't (`(map (fn (k) (at m k)) (keys m))` uses only the map's `at`).
5. **The HLD changes visibly.** Its names list and Question 4 say `map.get`. I'll revise them with a dated note keeping the old text, as with step 1's revision, recording the reason: `get` is the field read, and `at` is the verb all three collections share.
6. **The `at`s still differ underneath.** `map.at` of a missing key raises Python's `KeyError`, while a list's or string's `at` out of range is a Candy panic. That's B160 (other Python errors aren't panics yet), so I'll note it in the rule rather than fix it here.

Shall I go ahead: undo 6a, then build step 6 as one commit with `map.at` and `at-or`?

## Owner

> I'm lost on 3... Tracking everything else

## Claude Code

Point 3 is only about one Candy helper's name.

The HLD plans three Candy functions in the `map` module, built on its built-ins:
- `update`: change one key's value with a function;
- `values`: all the values;
- `get-or`: a key's value, or a fallback if the key is missing.

```
(map.get-or m "a" 0)    ; m's value for "a", or 0 if there's none
```

That name was chosen when the lookup was going to be `map.get`: "get, or else". With C the lookup is `map.at`, so `get-or` would be the only `get` left in the module, with no `map.get` beside it. I'd rename it to match:

```
(map.at m "a")          ; the value for "a" (a missing key is an error)
(map.at-or m "a" 0)     ; the value for "a", or 0
```

So `at-or` reads as "`at`, or a fallback", the same way `get-or` did for `get`. Nothing else changes.

## Owner

> Thanks tracking, note the "or" stuff and go with c.... map.at

## Claude Code

Undoing 6a first. I'll keep its diff in `tmp/c7/`, in case self-qualification is ever wanted:

*ran: Save 6a's diff and restore the files it changed*

Now the map built-ins and their uses. First, checking none of the new names is a special form:

*ran: List the special forms, the map built-ins, and count their uses*

No new name is a special form. The translator uses these about 320 times. Checking the library's macro-code files, and the prelude, which defines `map-update`:

*ran: Find map built-ins in the library files and the spec's prelude mentions*

Nothing in macro code uses them, so `macro-imports` needs no `map`. I'll adapt the rename script to the map names, and fix its import check to look for an import line, not the text anywhere:

*ran: Make a map version of the rename script and run it*

The rename touched six translator files and two spec files. Next: `map.cdy`, the built-ins out of `system.cdy` and the prelude, the spellings, and `LIBRARY`:

*ran: Read the prelude's map-update and the map spellings*

*ran: Read the prelude's header*

*ran: Write map.cdy, move the built-ins and map-update, and rebuild bin*

The translator builds on `map`, with `boot/90`'s `bin`, in one commit. Running the suite:

*ran: Run the full test suite*

*ran: Show the declaration-module test's failure*

The test's own Candy, written into a copy of `translator.cdy`, still says `map-has`. Moving it to `map.has`, with the import:

*ran: Fix the test's Candy and rerun it, then show the index failure*

Now the spec: the index row, `library.maps`, and `programs.prelude`'s list. The current text:

*ran: Read library.maps and the other old-name mentions*

*ran: Rewrite library.maps and the index row, and rerun the suite*

All 730 pass. Running the checkers and the comparison with `boot/90`, and finding where the HLD says `map.get` and `get-or`:

*ran: Run the checkers, compare with boot/90, and find the HLD's map names*

`boot/90` gives the same output on all 107 programs, and `system` is down to 48 built-ins. Now the HLD's `map.get` and `get-or`, revised with the old text kept:

*ran: Read the HLD lines that name map.get and get-or*

*ran: Revise the HLD's map names, write step 6's notes and the brainstorm entry*

*(The context was summarised here; the turns before it are above.)*

## Claude Code

*ran: Show the HLD's long line*

*ran: Rewrap the HLD line and recheck*

Step 6 is built as a single commit, with `map.at` and `at-or`. B211 (stdlib step 6: the `map` module) is in review; nothing is committed. All 730 tests pass, as do the five checkers.

**Undoing 6a:** its diff is saved at `tmp/c7/step6a-dropped.patch`, and the six files it touched are restored.

**The `map` module** (`src/cdy/map.cdy`):
- **7 built-ins**, gone from `system.cdy` (48 left): `empty`, `at`, `has`, `set`, `keys`, `from` and `size`.
- **In Candy:**
  - `update`, which replaces the prelude's `map-update`, now gone;
  - `values`;
  - `at-or`: `(map.at-or m k fallback)`, the value at `k`, or `fallback` if `k` isn't there.
- **In `spelling.py`** they're keyed `map.`, and keep their Python functions, so `boot/90`'s `bin` still reads the new library.
- **Macro code** doesn't use maps, so it doesn't import `map`.

**The translator moves onto it:**
- Its modules import `(import map ())`, and 312 calls are renamed: `core` 131, `check` 99, `emit` 46, `expand` 15, `include` 13, `cdyc` 8.
- I reused the step-5 rename script. Its import check now looks for a line that starts with the import, so a comment containing the text can't fool it.
- One test, `test_a_declaration_module_holds_candy`, had `map-has` inside a Python string, so I renamed it there by hand.

**The spec:**
- `library.maps` is rewritten for the module, explaining why the lookup is `at` (`get` is the special form). It has a new example of `values` and `at-or`, which also shows the list function `map` still working next to the module.
- The index row is updated, `map-update` is gone from the prelude's list in `programs.prelude`, and `map.cdy` is added to the list of declaration modules.

**Notes:**
- **HLD:** the names list and the `map` section say `at` and `at-or`. Question 4 gets a dated *Revised* note: the module stays `map`, and the lookup is `at`. Step 6 has its *Done* note, which records the alternatives weighed.
- **Brainstorm:** `doc/brainstorm.md` has an entry for the dropped self-qualification idea.
- **Backlog:** B211's notes record your decision.

**Checks:** `boot/90` gives the same output on all 107 programs, the translator included. No staging is needed.

On "gawc" I'll commit step 6, run `--step` and `--tag` (it gets `boot/91`), and check the tag is annotated. Next is step 7, B212 (stdlib step 7: the `list` module).

## Owner

> Gawc

## Claude Code

*ran: Commit step 6, check its bootstrap step and tag boot/91*

Step 6 is committed as `826963c` ("stdlib step 6: the map module") and tagged `boot/91`.

- **Bootstrap:** `bootstrap.py --step` passes with no staging, and `boot/91` is an annotated tag.
- **Tree:** clean, and the diff had no token shapes.
- **Backlog:** B211 (stdlib step 6: the `map` module) is in review.
- **Not pushed.** Seven commits and eight tags (`boot/84` to `boot/91`) are local only.

Next is step 7, B212 (stdlib step 7: the `list` module). The list built-ins stay in `system`. The new `list` module adds Candy built on them: `sort`, `last` and `sum`, per the HLD. The translator doesn't need to move this time, since nothing is renamed. Say "go" when ready.

## Owner

> Go

## Claude Code

*ran: Read the HLD's list plans and B212*

*ran: Read the list module's plan and the library-module test*

*ran: Read math's Candy part, find list-copying items, and Question 5*

*ran: Find the next backlog id, read B69, and the LIBRARY list*

*ran: Write list.cdy and try it with T1*

The one failure is my test's: `(list.sort empty-list)` leaves the item type unsolved, so `show` can't show it. Typing the empty list:

*ran: Rerun the trial, the empty sum, and mypy on the output*

Everything works, and mypy passes on the output. A 300-item sort runs without hitting the recursion limit, so the tail-recursive merge became a loop. Now the spec rule, the new item, and the notes:

*ran: Read the library spec's rules and a recent backlog item's shape*

*ran: Read the zip rule and the math rule's opening*

*ran: Write the rule, B216 and the notes, rebuild bin, and run the suite*

*ran: Run the checkers, compare with boot/91, and check the diff*

The translator itself is unchanged; the only change to `bin` is the new copy of `list.cdy`. I'll rewrap B216's long line; `list.cdy:23` is a code line, which the 90-character rule doesn't cover:

*ran: Rewrap B216 and recheck the backlog and links*

Step 7 is built and uncommitted, and B212 (stdlib step 7: the `list` module) is in review. All 732 tests pass, as do the five checkers.

**The `list` module** (`src/cdy/list.cdy`) is an ordinary library module, all Candy:
- **`last`:** an empty list panics, as `at` out of range does.
- **`sort`:** a stable merge sort on any `comparable` type (numbers, strings). Its tail-recursive merge became a loop, so a 500-item sort works. It is still quadratic, though, since each merge copies its list as it grows (B69, building a list is quadratic).
- **`sum`:** on any `number` type.
- **`flat-map`** and **`partition`**: `partition` returns a tuple of the matching items and the rest.
- The helper `merge` is private.

**Decision for you:** an empty `list.sum` panics with "list.sum: the list is empty", where Python's `sum([])` gives 0.
- **Why:** `sum` can't write a zero of its own number type, since a literal `0` is always an `Int`. So it starts from the first item, and an empty list has none.
- **Tracked:** I filed this as B216 (a number type variable has no zero), a `leak`, linked from the rule. It's the same gap that makes `math.abs` write `(- x x)`.
- **Alternative:** `sum` on `Int` lists only. That would give 0 for an empty list, but other number types would need `fold`. Say if you'd prefer it.

**Spec:** a new rule, `library.list`, with a table of the five calls, an example that runs and a panic example. The `library.builtins` index has a row for the module.

**Checks:**
- **Output compared:** `boot/91`'s `bin` gives the same output on all 108 programs. No staging is needed.
- **`bin`:** the translator is unchanged, but `bin` gets a copy of `list.cdy`, so this commit gets `boot/92`.
- **Notes:** the HLD's step 7 has its *Done* note.

On "gawc" I'll commit, then run `--step` and `--tag` for `boot/92`. Step 8 (docs) comes after that.

## Owner

> What's the sig on list's sum?

## Claude Code

It's:

```
(sig sum (Fn ((List number)) number))
```

`number` is a constraint variable: one type, which must be a number type (`Int`, `Long`, `Byte`, `Float` or `Double`). That type is both the list's items and the result. So `(list.sum (List 1 2 3))` is an `Int`, 6, and `(list.sum (List 1.5 2.0))` is a `Double`, 3.5. A list of strings is a type error.

This is also why the empty list is a problem. Inside `sum`, the body can't write a zero of whichever number type `number` turns out to be, because a literal `0` is always an `Int`. So it starts from the first item instead (`src/cdy/list.cdy:35`).

## Owner

> So, keep the panic and note the zero issue on the number constraint

## Claude Code

*ran: Read the constraint rule and CONSTRAINTS' comment*

*ran: Note the zero on the number constraint and in B216*

The empty-list panic stays, and the zero issue is now noted on the `number` constraint. Nothing is committed yet.

- **The spec:** `checking.constraints` (`spec/25-checking.md`) already said a literal inside a `number` body is an `Int`. It now continues: so the body can't write its zero or one. `math.abs` writes `(- x x)`, and `list.sum` of an empty list panics. It's marked *for now*, linking B216 (a number type variable has no zero).
- **The backlog:** B216 now links that rule, and its notes record your call.
- **Checks:** the doc-link and backlog tests pass. Nothing else changed since the full run.

On "gawc" I'll commit step 7, then run `--step` and `--tag` for `boot/92`.

## Owner

> Gawc

## Claude Code

*ran: Commit step 7, check its bootstrap step and tag boot/92*

Step 7 is committed as `9cff836` ("stdlib step 7: the list module") and tagged `boot/92`.

- **Bootstrap:** `bootstrap.py --step` passes with no staging, and `boot/92` is an annotated tag.
- **Tree:** clean, and the diff had no token shapes. None of your own edits were in the working tree.
- **Backlog:** B212 (stdlib step 7: the `list` module) is in review, and B216 (a number type variable has no zero) is new and open.
- **Not pushed.** Eight commits and nine tags (`boot/84` to `boot/92`) are local only.

The last step is 8, B213 (stdlib step 8: the docs). It brings `CLAUDE.md`, `README.md` and the older HLDs up to date with the modules. Then come the `stdlib` tag and the merge into `master`, after `pytest -m bootstrap`. Say "go" for step 8.

## Owner

> Go

## Claude Code

*ran: Read B213 and the HLD's step 8*

*ran: Find the docs that use the old names and the Looking back sections*

*ran: Read how library-layers did its docs step, and the epic and multi-target mentions*

*ran: Read library-layers' Looking back, the epic's library section, and the HLD's head*

*ran: Read the epic's library section, multi_target's note, and library.md's section*

*ran: Read the HLD's scope answer, its outline, and library.md's section*

*ran: Find library mentions in README and CLAUDE.md*

*ran: Read README's source list and CLAUDE.md's history sentence*

*ran: Read CLAUDE.md's modules, built-ins and library bullets*

*ran: Update CLAUDE.md, README, the epic, multi_target.md and library.md*

Now the HLD's status, step 8's *Done* note, and "Looking back":

*ran: Read the HLD's step 8, its end, and steps 1 and 2*

*ran: Read step 2's Done note for its numbers*

*ran: Write the HLD's status, step 8's note and Looking back; recheck*

Checking whether any of those long lines are mine:

*ran: Show long lines among the added doc lines*

*ran: Read the HLD's status paragraph*

*ran: Rewrap the status line and run the full suite*

Step 8 is built and uncommitted; it changes only docs, and all 732 tests still pass. B213 (stdlib step 8: the docs) is in review.

**What changed:**
- **`CLAUDE.md`:**
  - **History:** `stdlib` as the second half of the epic's `library` branch.
  - **Library files:** the six new modules added to the list.
  - **"Modules":** a declaration module is one named by `spelling.py`'s keys, and an import's unlisted name gives way to a built-in.
  - **"The library":** list built-ins in `system`, the `string`, `map`, `math`, `list` and `test` modules, and macro code's implicit `string`.
- **`README.md`:** the new library files.
- **`python_complete.md`:** the fifth branch marked *done*, except `io`, `py` and `parse`, which Question 1 moved to later branches. Its B108 (one flat namespace) row now says done.
- **`library.md` and `multi_target.md`:** dated *Taken further on branch `stdlib`* notes. Neither old HLD is rewritten.
- **`stdlib.md`:**
  - the status says all 8 steps are built and in review;
  - step 8 has its *Done* note;
  - a new "Looking back" section has six lessons:
    1. a rename meets rules a name was relying on: try another name before adding a rule;
    2. the old `bin` decides how many commits a step is;
    3. a mechanical rename needs a tokenizer, not a regex;
    4. the spellings already say what a target provides;
    5. a constraint variable has no literals (B216, a number type variable has no zero);
    6. a spliced top-level `do` lets a macro write two definitions.

`bin` is unchanged, so this commit gets no `boot/NN`.

**After this commit, to finish the branch:**
1. **Review:** B206 to B213 are all in review, waiting for your "tick". It's one item per step: B206 (step 1, declaration modules from the spellings), B207 (step 2, the prelude's costs), B208 (step 3, `test`), B209 (step 4, `math`), B210 (step 5, `string`), B211 (step 6, `map`), B212 (step 7, `list`), B213 (step 8, the docs).
2. **Chat archive:** archive the branch's chat with `script/chat_archive.py`, scrubbing `github_pat_` and the other token shapes first.
3. **Merge:** run `pytest -m bootstrap`, merge into `master` with `--no-ff`, and add the annotated `stdlib` tag. The merge needs its own "gawc".

On "gawc" I'll commit step 8.

## Owner

> gawc

## Claude Code

*ran: Commit step 8*

Step 8 is committed as `989abfb` ("stdlib step 8: the docs"). It's docs only and `bin` is unchanged, so it gets no `boot/NN` tag. The tree is clean, and the diff had no token shapes.

All eight steps of `stdlib` are now committed, nothing is pushed, and the eight step items, B206 to B213, are in review. To finish the branch:

1. **Review:** say "tick" (all, or name some) and I'll mark the items done.
2. **Chat archive:** I'll write the branch's chat into `doc/archive/` with `script/chat_archive.py`. I'll scrub the token you pasted earlier (`github_pat_`) and any other token shapes first, and tell you what I found.
3. **Merge:** after `pytest -m bootstrap`, a `--no-ff` merge into `master` and an annotated `stdlib` tag, on its own "gawc".

The push is separate: the branch, `boot/84` to `boot/92`, and later `stdlib` go only when you say "push".

## Owner

> Tick all

## Claude Code

*ran: Mark B206 to B213 done with a tick note*

The HLD's status should say the review is done too, as `library.md`'s does:

*ran: Mark the HLD reviewed*

*ran: Rewrap the status line and recheck the links*

All eight are ticked: B206 to B213 are `done`, each with the note "2026-11-21, the owner: ticked in review.". I also changed the HLD's status to say "reviewed (2026-11-21): done", as `library.md`'s does, and regenerated the backlog index. Nothing is committed.

Next is the chat archive, which I'd fold into the same commit as the ticks. I'll write the branch's chat into `doc/archive/` with `script/chat_archive.py`, then scan it for `github_pat_`, `ghp_` and the other token shapes and scrub anything found. I'll tell you what turned up before you commit.

Should I go ahead with the archive?

## Owner

> Go

## Claude Code

*ran: Read the archive script's usage and list past archives*

*ran: Read the last archive's header, the branch's start, and the transcripts*

*ran: Find which transcripts hold the stdlib branch's chat*

Two sessions have turns on `stdlib`: this one, and 66 entries at the end of the long earlier session. Checking what those 66 are, and how the last archive handled a branch split across sessions:

*ran: List the archives and time the old session's stdlib entries*

There's no archive for `namespaces` or `library-layers`, so it isn't done for every branch. Checking what `doc/process.md` says:

*ran: Find the chat-archive rule in the process doc*

*ran: Generate both sessions' stdlib chat and list the old one's turns*
