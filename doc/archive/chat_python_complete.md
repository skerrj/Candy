*Archived 2026-10-31, from the Claude Code session, on `master` between the merge of
`type-checker` and the start of `typed-core` (2026-10-29 to 2026-10-31), by
`script/chat_archive.py`.* The chat that wrote the epic `doc/hl_rqmt/python_complete.md`
(a complete language on Python, before a second target) and its first branch's HLD,
`doc/hl_rqmt/typed_core.md`: the first cut, the branches' order, Question 4 on the
operators' polymorphism ([[B124]]), the twelve answers ([[B125]]), and `typed_core.md`'s
six. The owner's messages and Claude's replies are verbatim; each tool call is a one-line
marker, and thinking and tool output are left out.

# python_complete: the epic

## Owner

> I was wondering about doing a "towards a python host version complete (I.e. things we need before expanding to a rust target and host" (or something...) epic hld... To figure a way forward... Addressing tup, format, macros, others, maybe parsec lib in candy, etc... a first cut at an interpreter maybe, etc ... Thoughts?

## Claude Code

*ran: Survey the open backlog and existing roadmap notes*

Yes, I think this is the right time for an epic HLD. The backlog has 83 open items with no order beyond priority, and the type checker was the last big thing in the way. Here's how I'd frame it.

**1. Define "complete" as "nothing Candy relies on belongs to Python."** That gives the HLD something to test against and a way to sort the backlog. Every open item goes into one of four groups:
- **Semantics Candy borrows from Python.** These must be fixed before a second target, because Rust would behave differently:
  - printing (B36);
  - `=` (B27), `/` (B23), and `and`/`or` returning an operand (B26);
  - `Maybe` and missing values as `None` (B20, B21);
  - `at` and `slice` (B35);
  - a value used before its `def` (B31, B80).
- **Things a static target can't express.** Rust has no `Any` and needs a concrete type everywhere: B18, B19, B48, B49, and the inferred types kept in Core.
- **The Python backend's own business.** `NamedTuple`s (B29), `match` temporaries (B56) and the like. These are fine as they are, as long as they stay inside `emit`.
- **Later:** performance and convenience.

A possible exit test: the spec runs on two backends with the same output, and no item in the first two groups is open.

**2. Keep "Rust target" and "Rust host" separate.** A target is what the translator writes; a host is where the translator and its macros run. The target has to come first, because a Rust host is the translator compiled to Rust. What ties macros to a host is `load-macros`, which uses Python's `exec`.

**3. That's the strongest argument for an interpreter, and for an early one.** A tree-walking interpreter over Core, written in Candy, would:
- run macros without the host's `eval`, so macros stop depending on Python. That's the hard part of a new host;
- be a second backend straight away, so running the spec through both checks that the semantics are Candy's own, not Python's. It would find the first group's leaks for you;
- give you a REPL nearly for free (it's in `brainstorm.md`'s "dump").

It's a contained project, too: Core is small, maybe 14 node kinds.

**4. `tup` and `format` share one root cause: there are no variadic functions and no list literal** (B48, B99, B29). That's why both are special forms.
- `tup` gets fixed with a list literal and real tuple types (B17).
- `format` could become a macro over string joining plus a `show` per type (B16). That `show` is also the fix for printing (B36), and it needs the types kept in Core.

So "types kept in Core" is an enabler for several items, not one feature among others.

**5. Macros:** B42, B45, B46 and B52, with the interpreter as their foundation.

**6. A parsec library in Candy is a good test of the language, but it isn't on the path.** The hand-written reader works. A parser-combinator library would stress generics, closures and the checker, so I'd list it as a proving-ground option after the type work, not as a prerequisite. B72 only concerns the bootstrap chain.

**A possible order, each phase one or more branches with their own HLDs:**
1. **Candy's own semantics:** sweep the first group, starting with printing and equality.
2. **Types all the way down:**
   - keep the inferred types in Core;
   - get rid of `Any` where possible;
   - add a list literal and variadic built-ins;
   - fix `tup` properly, and make `format` a macro.
3. **The interpreter**, as a second backend and as the macro runner. Then clean up macros.
4. **Multi-target scaffolding:** spellings per target, and the spec run on each backend.
5. **The Rust target, then the Rust host:** each a later epic of its own.

**Process:** `process.md` has no notion of an epic. I'd add it as an HLD whose steps are branches, each with its own HLD, plus a triage table covering every open item. A name like `doc/hl_rqmt/host_independence.md` would work, or `portable_candy.md`.

**Decisions for you:**
- Does the exit test above match what you mean by "complete"?
- Should the interpreter be in this epic, which I'd recommend, or wait until after it?
- Rust target first and the host later, as I'd suggest, or should the epic aim straight at a host?

If you agree with the framing, I'd draft the epic HLD as `proposed`, with the triage of all 83 items. Reading it would be the first place to push back.

## Owner

> Sounds good add system and prelude revisit stuff and std lib stuff and target specific system and lib extensions stuff

## Claude Code

*ran: Read the process doc's lifecycle and HLD rules*

I'll write the epic HLD as a `proposal`, with a triage of every open item. First, the full open list:

*ran: List every open backlog item*

Some items are central to the new parts, target-specific libraries and the interpreter, so I'm reading those in full:

*ran: Read the items about libraries, hosts and the interpreter*

I have what I need. I'm writing the epic HLD as `doc/hl_rqmt/python_complete.md`:

*wrote: `doc/hl_rqmt/python_complete.md`*

Now a check that the triage covers every open item exactly once, and that the links resolve:

*ran: Check the triage covers every open item and the links resolve*

Every open item is covered once: 84 in all (B20's title has an escaped `|`, which tripped my count). I'll fix the "87" in the intro.

*edited: `doc/hl_rqmt/python_complete.md`*

I've drafted the epic HLD as `doc/hl_rqmt/python_complete.md`, with status `proposal`. It's uncommitted on master; the doc-link tests pass with it.

**The library section** adds the parts you asked for. It has five layers, each with a rule for what goes in it and what to revisit:
1. **Special forms:** the language itself. Some are special only because a feature is missing: `tup`, `format` and the operators.
2. **System:** the porting surface, so it should be small and portable.
   - What can be written in Candy moves up (`with-default`, B51).
   - The translator's five host built-ins get a file only the translator imports (B50).
   - What belongs to Python moves into the Python extension: regexes (B32) and `slurp`'s search (B54).
   - Every built-in gets a spec rule.
3. **Prelude:** kept small. Macro code gets it (B52), and a program carries only what it uses (B68, B66, B62).
4. **Standard library:** Candy modules imported by name and qualified, such as `list`, `string`, `map`, `math`, `io` and maybe `parse`. This needs qualified imports (B47) and is how the flat namespace gets split (B108). The I/O refactor (B95) becomes the `io` module's design.
5. **Target extensions:** a target's own built-ins and modules, such as a `py` extension for Python interop and opaque host types (B49), with spec files per target (B97). Importing one is how a program says it isn't portable.

**The rest of the HLD:**
- **The exit test:**
  - the spec runs the same on Python and on an interpreter;
  - nothing in the borrowed-semantics, static-types or macros-on-the-host groups is left open;
  - the porting surface is written down and small;
  - what's specific to one target lives only in its extensions.
- **Seven branches, in order:**
  1. `typed-core`
  2. `interpreter`
  3. `semantics`
  4. `collections`, which covers the list literal, tuple types, variadics, `format` as a macro and less `Any`
  5. `library`
  6. `host-macros`
  7. `porting-surface`
- **A triage table** puts all 84 open items into one of eight groups and gives each the branch where it should close. Defects and the translator's own items go into whichever branch is nearest.
- **Step 1** also adds "epic" to `doc/process.md`, as an HLD whose steps are branches.

**Seven questions,** each with a recommendation:
1. the exit test;
2. the branch order;
3. whether mypy stays: keep it until `semantics`, then decide;
4. overloading and interfaces: special rules for now, and interfaces in an HLD of their own after this epic;
5. target extensions: one module per target rather than reader conditionals;
6. parsec in Candy: yes, as `parse`, if it's cheap in the `library` branch;
7. `Maybe` as a real sum: decide it in the `semantics` HLD, using what the interpreter shows.

One thing to check when you read it: I've marked B67 ("the built-ins' types are read but not used") as probably already fixed by the type checker. It closes in `typed-core` if so.

This is a first cut, so please push back in the triage table first; that's where I made most of the judgment calls. Commit it on "gawc".

## Owner

> Add maybe mention moving or a start at moving testing framework to candy....

## Claude Code

*ran: List the Python test files and their sizes*

*ran: Add testing in Candy to the epic HLD*

*ran: Check the HLD's links*

I've added testing in Candy to the epic HLD, still uncommitted, and its links check passes.

- **"Where things stand"** gets a bullet: pytest runs everything, so a Candy program can't test itself. There's no assertion and no test module, and a second host would have to port the runners.
- **A new goal:** a start at testing in Candy.
- **A new section, "Testing in Candy,"** in two parts:
  1. **A `test` module** in the standard library:
     - `check` is an assertion with a message and a position;
     - `deftest` is a macro that names a test;
     - a runner reports the results and exits non-zero on a failure.

     The test programs' `.out` files stay for tests that are about output.
  2. **The spec's runner in Candy.** It reads a spec file's fences and runs each example, either on the interpreter or by translating it and running the result. It reports by `file:line`, as `test_spec.py` does. It needs three things first:
     - enough Markdown reading to find the fences, which is work for the `string` module;
     - the interpreter;
     - errors as values, not only `fail` (B39), so it can catch an example's expected error.

  pytest stays the driver for the checks that are about Python: mypy on the translation, the bootstrap chain and the fixpoint. It calls the Candy runners for the rest.
- **The branches:** `library` gains the `test` module. A new `test-runner` branch comes before `porting-surface`, making eight branches.
- **Question 8, "how far?":** I recommend the `test` module and the spec's runner, which is the conformance suite a second host needs. Moving the remaining Python tests, such as the backlog and link checks, would wait until a second host needs it. The spec runner could also move earlier, into `interpreter`, since that's its first user.

One possible tightening: the exit test could require that the spec runs through the Candy runner, not through `test_spec.py`. I've left it out for now; it belongs to Question 1.

## Owner

> Nice first cut... Should we consider variadic issues and namespaces?

## Claude Code

Yes, both, and both should be explicit. In the draft they're scattered across items, but each is a design decision that several branches depend on.

**Variadics.** Several things are variadic today, each for its own reason:
- the operators (`+`, `<`, `and`…);
- `tup`, `put` and `format`;
- macros, which are variadic and untyped.

They fall into two kinds:
- **Same type for every argument** (`+`, `<`, `and`, `or`): a typed rest parameter would cover them, something like `(Fn (Int ...) Int)` with the rest arriving as a list. That maps fine to Rust, which would get a slice.
- **Mixed types** (`put`, `format`, `tup`): a rest parameter can't type these. `put` and `format` need a `show` per argument's type, so they're really macros over a typed `show`. `tup`'s type depends on how many arguments it gets, so it stays a special form, or becomes literal syntax. Rust makes the same split: no variadic functions, and `println!` is a macro.

That gives a recommendation: typed rest parameters for the first kind, and macros or special forms for the second.

There are two tensions:
- **Currying (B93):** curried types and partial application need a fixed arity, so they conflict with variadics. The epic should decide which one Candy has, even if neither is built in it.
- **Overloading (Question 4):** `+` over numbers and strings needs special rules or interfaces, whether or not it's variadic.

**Namespaces.** This is the bigger one, and it needs its own branch before `library`, because the standard library and target extensions are built on it. The open questions:
- **Qualified names:** syntax such as `string/split`, Clojure-style. `/` is already the division operator, so the reader has to treat a lone `/` as the operator and `m/name` as a qualified name.
- **Import forms:** `(import m)`, aliases, importing selected names, and what stays unqualified: the prelude, perhaps the operators (B47, B108).
- **Types and values:** one namespace or two (B40). This interacts with constructors, which are values named like types (B119).
- **Macros:** they're global per program now. Should they be qualified and imported like values (B11, B45)?
- **Shadowing:** can a program's own name shadow a prelude or system name? B50 says the program's definition wins now; is that *lasting*?
- **Fields:** `get` finds a field by name and type, as in OCaml. That doesn't change, but it should be stated.
- **Mapping to targets:** each target maps Candy's namespaces to its own, through Python's `stem__name` mangling and Rust's modules. That makes it part of the porting surface (B12, B65).

**What I'd change in the HLD:**
- a **"Variadics"** section in the proposal, with the two-kind split, and a question that also settles variadics versus currying;
- a **"Namespaces"** section, and a **`namespaces` branch** before `library`, taking B47, B108, B40, B11 and part of B50 out of `library`;
- in **Question 4**, the link to overloading, since the two decisions are made together.

That makes nine branches. Should I make these changes?

## Owner

> Yes, and any map, reduce, fold, changes that you found... Forgot where we left this

## Claude Code

I'll find where the map/fold discussion went first.

*ran: Search the docs and backlog for fold, reduce and map notes*

*ran: Find fold and map in system.cdy and docs mentioning them*

*ran: Read the brainstorm and fold mentions in HLDs*

*ran: Search this session's transcript for fold and reduce discussion*

The thread is in the `library` HLD. I'm checking where it was left, and how the translator uses `map` and `fold` today:

*ran: Read the library HLD's list-operation decisions and count uses in the translator*

*ran: Check whether a backlog item tracks the hand-written loops*

*read: `doc/hl_rqmt/python_complete.md`*

*ran: Add B123 for the translator's hand-written list loops*

Now the HLD edits:

*ran: Add variadics, namespaces and list operations to the HLD, update the triage*

*ran: Recheck that the triage covers every open item*

I've added variadics, namespaces and the list operations to the epic HLD. Nothing is committed; the link and backlog tests pass, and the triage covers all 85 open items.

**Where the map/fold question was left.** Question 6 of the `library` HLD decided that the translator's hand-written `acc` loops stay *for now*. Rewriting them as `map` or `fold` calls would turn each `fn` into a nested Python `def` typed `Any` (B19), which costs the fixpoint's `mypy --strict` checking. Many of the loops also carry a counter or a scope along with the list. It said to revisit "when `fn`s get typed annotations", which `typed-core` would provide. No item tracked this; B69 only mentions the quadratic copying. Today the translator calls `map` 10 times, `fold` twice, and `filter` and `find` not at all. So I added:

- **B123** (`tech-debt`, `normal`): the translator writes its list loops by hand. It records `library.md`'s reasoning, the loops that return `(tup acc n)`, and the revisit point.

**New sections in the proposal:**
- **Variadics:**
  - typed rest parameters for operators whose arguments all have one type;
  - macros over a typed `show` for `put` and `format`;
  - `tup` stays a special form;
  - the conflict with currying (B93);
  - why Clojure's several-list `map` isn't worth it: a type can't say the function's arity matches the number of lists, so `zip` is simpler.
- **Namespaces:** what its own HLD settles:
  - qualified names, and `/` as both operator and separator;
  - the import forms, and what stays unqualified;
  - types and values in one namespace or two (B40, B119);
  - macro names (B11), shadowing (B50) and private names;
  - fields stay outside namespaces;
  - each target's name mapping (B65).
- **The list operations:**
  - they stay built-ins, each target implementing them natively (your brainstorm's "optimized target implementations");
  - which to add: `map-acc`, a right fold, `reduce`;
  - the translator moved onto them (B123), which also fixes most of B69;
  - `Collection` types later;
  - the interpreter sharing the same built-ins, so it agrees with Python by design.

**Branches:** there are nine now. `namespaces` goes before `library`, and `collections` also takes the variadics, the list operations' set and B123.

**New questions, with what I propose:**
- **Q9:** rest parameters, with currying dropped as *lasting*, since `fn` covers partial application.
- **Q10:** `namespaces` is a branch of its own, and types and values stay in one namespace, as *lasting*.
- **Q11:** add only `map-acc`. `reduce` needs a list that can't be empty, which Candy can't type, and nothing uses a right fold.
- **Q4** now notes that overloading is decided together with variadics.

**Triage moves:**
- to `namespaces`: B47, B108 (shared with `library`), B40, B11 and B65;
- to `collections`: B93 (decided by Q9), B69 and B123.

## Owner

> Also maybe add where we stand with generics... And for the definition of "complete python host" say, as draft suggestion:  "a solid push off point to rust target and eventually a rust host"....?

## Claude Code

*ran: Translate a generic program to see how generics come out*

*ran: Check whether = and format work on a type variable*

*ran: Check whether = and format work on a type variable*

Both are accepted on a type variable, which matters for Rust: there, `=` on an `a` needs a `PartialEq` bound and showing one needs `Display`. Now the HLD edits:

*ran: Add generics and the draft definition of complete to the HLD*

*edited: `doc/hl_rqmt/python_complete.md`*

I've added both to the epic HLD. It's still uncommitted, and its links check passes.

**The draft definition** now sits at the top: *the Python version is a solid push-off point to a Rust target, and eventually a Rust host.* That means nothing Candy relies on belongs to Python, so the Rust target is a new backend and runtime, not a rework of the language. The Rust host is then the translator built for that target. The four-part exit test is how to tell, and Question 1 now covers both the definition and the test.

**Where generics stand,** a new bullet in "Where things stand." I checked it by translating a few small programs with `bin`.
- **What exists:**
  - generic records and sums, such as `(deft (Box a) ...)` and `(deft (T a) (L ...) (N))`;
  - generic functions from type variables in a `sig`, freshly typed at each use and rigid inside the body;
  - PEP 695 generics in the Python output (`class Box[a]`, `def pick[a]`, `type T[a] = L[a] | N`).
- **What's missing:**
  - let-polymorphism;
  - bounds, so a generic function can't use `+` or `<`;
  - higher kinds and explicit type arguments;
  - variadic types other than `Tup`.
- **A finding that matters for Rust:** `=` and `format` already work on a type variable. `(= x y)` and `"<{x}>"` on an `a` translate and run, because Python can compare and show anything. That's a hidden bound, which Rust would have to make real (`PartialEq`, `Display`).

**A new "Generics" section** in the proposal:
- **The hidden bounds go away in `semantics`.** I propose declaring `=` and `show` for every type, as *lasting*. Every Candy value is plain data, so structural equality and a per-type printer are always possible. A Rust target would derive `PartialEq` and `Debug` on every Candy type.
- **For Rust,** Candy's generics map directly onto Rust's (`struct Box<A>`, `enum T<A>`), so the translator doesn't need to monomorphise. Cloning versus `Rc` is the backend's choice.
- **Left for later:** let-polymorphism, bounds (as interfaces, Question 4) and higher kinds. None of them blocks a Rust target.

**Question 12:** `=` and `show` on a type variable, either declared for every type (proposed) or rejected until interfaces come. The `semantics` branch description now includes it.

That makes 12 questions over nine branches. Your brainstorm's "Generics: not sure where we are at" is answered by that bullet. Shall I remove the brainstorm line when this is committed, or leave the brainstorm to you?

## Owner

> Remove and gawc...

## Claude Code

*ran: Check how HLD drafts landed on master and the tree's state*

HLD proposals have gone straight onto master before (`74cf6fe`, `46a23e3`), so this commit goes there too. I'm removing the brainstorm line and committing:

*ran: Remove the brainstorm's Generics note and commit the epic HLD*

I removed the brainstorm's "Generics" note and committed the epic on master as `2149502`, "python_complete.md (proposal): the epic towards a Python version complete". It isn't pushed.

The commit holds three things:
- the epic HLD, `doc/hl_rqmt/python_complete.md`, with status `proposal`, nine branches and twelve questions;
- **B123**, the translator's hand-written list loops;
- the brainstorm edit.

There were no edits of yours in the tree. The link and backlog tests pass.

Two more brainstorm lines are covered by the HLD, and I've left them alone since you didn't ask:
- "**variadic args, interfaces, and generics**: *break this up*" is split across the Variadics and Generics sections and Question 4.
- "**Map, reduce, fold, etc**: optimized target implementations" is in "The list operations."

Say if you want those removed too.

When you're ready, go through the twelve questions; all of them have a recommendation. Once they're answered, step 1 adds "epic" to `doc/process.md`, and then the first branch, `typed-core`, gets its own HLD.

## Owner

> Remove and push

## Claude Code

*ran: Remove the two brainstorm notes, commit, and push master*

I removed the two brainstorm notes, committed that as `ee5f3b2`, and pushed master (`2b1b8c9..ee5f3b2`). The push also carried the epic HLD commit, `2149502`.

The removed notes were "variadic args, interfaces, and generics: break this up" and "Map, reduce, fold, etc: optimized target implementations".

The HLD's twelve questions are waiting for your answers.

## Owner

> Maybe take on more full pass and focus on/double check branch priorities... If any changes commit and push

## Claude Code

*read: `doc/hl_rqmt/python_complete.md`*

Two things in the order need checking against the code before I change anything: what the interpreter would actually share with the Python target, and whether B67 is already done.

*ran: Check whether the checker uses the built-ins' types*

*ran: Reorder the branches and fix the interpreter's description, Q2, Q3, Q7 and the triage*

The edits applied; the grep found no leftovers. I said the triage is "in branch order", so I'll sort the table to make that true:

*ran: Sort the triage table by branch order*

*ran: Look at the end of the triage table*

B20's escaped `|` threw off the sort, so I'll move that row by hand:

*ran: Move the B20 row, close B67, and check links and the backlog*

*ran: Tidy B67's notes and reread the branch list*

*ran: Commit the HLD pass and B67, then push master*

I made a full pass over the epic HLD and changed the branch order. It's committed as `9727941` and pushed to master.

**The main change: the interpreter moves from second to sixth.** I had overstated what it does.
- **It can't find borrowed semantics on its own.** Its built-ins have to be its own, written over its own value type, and wherever it hands work to Python it inherits Python's meaning, just as the Python target does. What it can check is that the spec says enough to be implemented twice, and that only works once the spec is decided.
- **Second would have meant rewriting it repeatedly.** The list literal, rest parameters, qualified names and maybe `Maybe` as a sum all come later. Placed after the branches that change the language, it's written once.
- **The interpreter section now says what it needs:** its own values, its own built-ins, and a conversion between its values and the translator's `Form`s for running macros. The list-operations section no longer claims the two implementations "agree by sharing" built-ins.

**The new order:**
1. `typed-core`: everything else needs it.
2. `semantics`: moved up, so B36 (printing, the backlog's other `high`) comes right after typed Core, which it depends on.
3. `collections`
4. `namespaces`: independent of 2 and 3, and noted as able to swap with them.
5. `library`
6. `interpreter`
7. `host-macros`
8. `test-runner`
9. `porting-surface`

**Smaller fixes:**
- **mypy:** `typed-core` said it would decide whether mypy stays, while Question 3 said to decide after `semantics`. Now mypy stays through the epic and is decided in `porting-surface`, once there are two implementations.
- **Moved items:**
  - B52 (prelude for macro code) goes to `host-macros`, where the interpreter makes it natural;
  - B38 (operators as values) goes to `collections`, with rest parameters;
  - B13 (the 200-clause `cond`) goes to "any";
  - B75 (mypy one program at a time) goes to "any".
- **Questions 2, 3, 7 and 8** are reworded to match. Q7 (`Maybe`) no longer depends on evidence from the interpreter.
- **The triage table** is sorted in branch order.
- **B67 is closed** (`done`, fixed by `type-checker`): `check.cdy:249` uses every built-in's type from `system.cdy`. That leaves 84 open items, all in the triage.

The trade-off, now listed under "Against": until the sixth branch, only one implementation checks the semantics.

The twelve questions are still open. Question 2 is the one to look at first, since it decides the order above.

## Owner

> Ok, thanks, I'm done for today... Except one minor... Really minor issue...on GitHub, which i'd like to move away from at some point, the links in the hlds back to the spec weren't working last time I checked...

## Claude Code

*ran: Look for earlier notes on how links render on GitHub*

*ran: Read the tracking HLD's decision on link syntax*

They aren't broken: they were never links. The tracking HLD made `[[checking.records]]` a checked reference rather than a Markdown link (`tracking.md`, "Ids and links"). `test_doc_links.py` makes sure every one names an id that exists, but no Markdown renderer turns `[[...]]` into a link, so GitHub shows it as plain text.

The one place with real links is the generated index, `backlog/README.md`. `script/backlog.py` writes its rule links out in full, as `[checking.order](../spec/25-checking.md#checking.order)`. I haven't checked whether GitHub scrolls to the `<a id>` anchors from there; it gives anchor ids a `user-content-` prefix.

There are three ways to fix it:
1. **Generate a rendered copy (my recommendation).** A script would write the docs out with every `[[id]]` turned into a real link, as HTML or Markdown. That's the book idea (B102). It also suits moving off GitHub, because the rendered docs could live anywhere, and the sources keep the short, checked `[[id]]` form.
2. **Write the links out in full in the sources,** as `[checking.order](../../spec/25-checking.md#checking.order)`, with the test checking each one. That works on GitHub today, but the links get long and each one depends on its relative path.
3. **Leave it as it is:** the ids can be searched, and the index links work.

When you're back, I'd add this as a low-priority backlog item, linked to B102, and fold it into the epic's `library` or `porting-surface` docs work, or do it any time. Nothing has changed since the last push. Have a good evening.

## Owner

> "the porting surface": nice!!!

## Claude Code

Thanks! It names something Candy didn't have a name for: the list of what a new target or host has to supply. Once that list is written down and kept small, the Rust epic starts with a clear list of what to build rather than an open question. That's why the HLD makes it part of the exit test.

Nothing is pending. The repo matches what's pushed, and the epic's twelve questions are there for whenever you pick it up again.

## Owner

> is the `+` polymorphism mentioned... still reading...

## Claude Code

*ran: Find where the HLD discusses + and overloading*

Yes, it comes up in four places in `doc/hl_rqmt/python_complete.md`, and Question 4 is where it's decided:

- **:47, "Where things stand" → Generics, bounds:** a type variable can't say "a type that has `+`", so `(+ x 1)` on an `a` is an error. That's the job of interfaces (B34).
- **:225, "`tup` and `format`":** whether `+` and the comparisons stay special rules, become overloaded, or wait for interfaces. This defers to Question 4.
- **:250–254, "Variadics":** a typed rest parameter could make `+` an ordinary built-in in `system.cdy`, except that `+` works on several types, which is overloading.
- **:397, Question 4, "Overloading":** `+` on numbers and strings, `=` on everything, and `Collection`. The options are special rules per operator (as now), interfaces (traits or type classes, which map well to Rust but are a big feature), or one function per type (`str-concat`). It notes that this has to be decided together with variadics (Question 9). The proposal is to keep special rules for now and give interfaces their own HLD after this epic.

For context while you read, here's how `+` works today. The checker has a fixed rule for it (`[[checking.operators]]`): all of a call's arguments have one type, and that type is a number type, `String` or a list. So `+` is polymorphic in the built-in sense, but only through the rule hard-coded into the checker. A program can't write its own function like that, and a generic function can't use `+` on a type variable.

## Owner

> so, having a polymorphic operator... but not allowing candy to define them... ???

## Claude Code

Right, that's an asymmetry. Today the built-ins get something a program can't have. `+` works on `Int`, `Double`, `String` and lists, but nobody can write a `sum` that works on both `Int`s and `Double`s, or make their own type work with `+`. Go was like this before it had generics: `len`, `append` and `map` were polymorphic, and nothing a user wrote could be. Python hides the problem, because `__add__` makes anything addable. A Rust target would expose it.

No backlog item says this outright; B34 (no `Collection`) and B48 (operators have no Candy type) each cover part of it. Under the project's own rule, it's a *for now* that should be a `leak`.

**There are four ways out:**
1. **Remove the polymorphism, OCaml-style.** OCaml uses `+` for ints, `+.` for floats and `^` for strings, so no operator is special. It's the simplest and most honest option. It costs churn: `+` on strings and lists would become `concat`, all through the translator.
2. **Built-in constraint variables, Elm-style.** This is the middle ground. Elm has `number`, `comparable` and `appendable` as special type variables that users *can* write in their own signatures: `(sig sum (Fn ((List number)) number))` works on `Int`s and `Double`s. It's a small feature: a few extra rules in the checker for which types each variable stands for, and no new syntax. Rust maps it directly to trait bounds (`Add`, `Ord`). It also fits Question 12: `=` and `show` would be one more such variable, or simply true of every type. The limit is Elm's well-known complaint: a user's own type can't join `number`.
3. **Interfaces (traits or type classes).** This is the full answer: user types can implement `+`, and `Collection` falls out of it (B34). It's a big feature, already planned as its own HLD after the epic.
4. **Keep the asymmetry for now,** and record it as a leak. That's what the HLD's Question 4 currently proposes, without saying it this plainly.

**I'd recommend option 2 inside the epic, in `collections`, with option 3 after it.** That makes `+` honest: its type becomes something like `(Fn (number ...) number)`, which a program can also write. Generic code works for the cases people actually need. Interfaces would later extend the same idea to user types, so the built-in variables stay valid rather than being thrown away.

When you're done reading, I can add the leak item and rewrite Question 4 around these four options. I won't edit anything while you're still reading.

## Owner

> leaning towards your recommendations: option 2 inside the epic, in collections, with option 3 after it...still reading

## Claude Code

Noted: you're leaning towards option 2 in `collections`, with interfaces after the epic. I'll leave the HLD alone while you read.

When you're ready, the change would be:
- a `leak` item saying that `+` and the comparisons are polymorphic only through rules built into the checker;
- Question 4 rewritten around the four options, with option 2 proposed;
- `collections`' branch description adding the constraint variables (`number`, `comparable`, `appendable`);
- a note under Question 12 that `=` and `show` could be one more such variable, or simply true of every type.

*(The context was summarised here; the turns before it are above.)*

## Owner

> For polymorph ways out option 1...  How much "churn"? I don't see it much more than remaining... Or "typed" renames ... Anyways can we do a quick survey to expand pros/cons of option 1?

## Claude Code

*ran: `grep -n "op \|^(sig [-+*/<>=]" src/cdy/special.cdy src/cdy/system.cdy | head -40`*

*ran: `for op in '+' '-' '\*' '/' '<' '>' '<=' '>=' '=' '!=' && do n=$(grep -ohE "\($op`*

*ran: `echo "(+ in src/cdy: $(grep -oF '(+ ' src/cdy/*.cdy | wc -l)" && echo "(* : $(gr`*

*ran: `grep -hF '(+ ' src/cdy/*.cdy > /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b4`*

Churn first. These are rough counts, from grepping `src/cdy/` (the checker could give exact ones):

| `+` on | sites in the translator |
|---|---|
| lists (`(+ acc (to-list …))` and the like) | about 140 |
| numbers (mostly `(+ i 1)`) | about 80 |
| strings | about 80 |
| **total** | **about 300**, plus about 76 in `spec/` and `tst/cdy/` |

You're right that this is a rename, not a redesign. It can also be done mechanically: the checker already knows each `+`'s type, so a throwaway trace in `infer-op` could list every site with its type, and a script could rewrite them. The only ordering constraint is the bootstrap: first a step that adds the new operators to `bin`, then a step that renames the translator's own uses. So it's two boot steps, not a project.

**What other languages do:**
- **Gleam** goes furthest with option 1: `+` for `Int`, `+.` for `Float`, `<>` for strings, `list.append` for lists, and even `<` against `<.` for comparisons. `==` stays structural and works on every type. It gets away with this because it has only two number types.
- **OCaml:** `+` against `+.`, `^` for strings, `@` for lists, and `Int64.add` and friends in modules. `=`, `<` and `compare` stay polymorphic, built in, and fail at run time on functions. So OCaml keeps the same asymmetry for comparisons.
- **Standard ML:** `^` and `@` are separate, but `+` is overloaded with a default to `int`, which is a special rule (option 4). Equality uses equality type variables (`''a`), which is option 2 for `=`.
- **Elm (option 2)** already splits append from arithmetic: `++` is `appendable` (strings and lists) and `+` is `number`. Option 2 done Elm's way includes most of option 1's churn, the roughly 220 list and string sites.
- **Haskell:** `++` for lists and strings, and type classes for numbers. That's option 1 for append and option 3 for arithmetic.
- **Go before 1.18** had exactly Candy's leak: built-ins were polymorphic and users couldn't write polymorphic functions. Its generics then added constraints (`Ordered`).
- **Rust, Roc, Haskell (option 3):** `Add`, abilities, `Num`. In Rust, `Vec` has no `+` at all.

**Option 1's pros:**
- **No special rules.** Each operator gets an ordinary `sig` in `system.cdy`. `infer-op`'s `+` branch and `needs-kind` go, and a user's function can do whatever a built-in does.
- **Better inference.** `(fn (a b) (+ a b))` is `Int`, where today the type stays a flexible variable.
- **The porting surface.** I hadn't weighed this before, and it may be the biggest point. Python's `+` works on all three kinds of value, so `emit` doesn't need types. Rust's doesn't: a polymorphic `+` would make the checker's types an input to the backend (type-directed lowering), for every target. With separate operators, each one has a single fixed spelling per target.
- **Cost shows in the code.** `++` on a tuple is O(n), and the translator's `(+ acc (to-list x))` loops are O(n²). A separate operator makes that easier to see (it ties in with B123).

**Option 1's cons:**
- **Candy has five number types** (`Int`, `Long`, `Byte`, `Float`, `Double`), which OCaml and Gleam avoid by having two. A full option 1 needs five sets of operators, or names qualified by namespace (`Long.+`), which `namespaces` provides only after `collections`. The other way out is to cut down to `Int` and `Double` plus conversions, which is a bigger change to the language.
- **It doesn't cover `=` and the comparisons.** Even Gleam and OCaml keep a polymorphic `==` that's built in. So option 1 alone leaves Question 12 open, and `=` has 419 uses that nobody would rename. Option 2 covers `=` and `<` with `comparable` (or equality for every type).
- **It may be partly undone later.** If interfaces (option 3) come after the epic, overloaded arithmetic usually comes back with them, as Rust's `Add` and Haskell's `Num` show. A separate `++` for append tends to survive that, though: Haskell and Elm both keep it.
- **Churn in the spec:** `spec/`'s operator rules and their examples, and the error tables.

**Where this leaves me:** the options aren't exclusive, and the survey points to a split:
- **Option 1 for append:** `++` for strings and lists. This is most of the churn, it fixes the porting-surface problem for the case Rust lacks, and it lasts in every language that has it.
- **Option 2 for numbers and comparisons:** `number` across the five number types, and `comparable` (with equality for every type, from Question 12). That avoids five sets of arithmetic operators.
- **Interfaces later**, without undoing either.

That's Elm's design, and it stays in `collections`. If it reads right to you, I'll write Question 4 that way, with this survey as the pros and cons, when you say go.

## Owner

> Go

## Claude Code

*ran: `grep -n "^#\|Question 4\|Question 12\|Overload\|collections\'" doc/hl_rqmt/pytho`*

*ran: `sed -n 40,55p doc/hl_rqmt/python_complete.md && echo .... && sed -n 218,260p doc`*

*ran: `cat backlog/B121*.md && grep -rn 'a id="[a-z.-]*op[a-z.-]*"\|a id="checking.op' `*

Now B124, then the HLD edits.

*wrote: `backlog/B124-polymorphic-operators.md`*

*ran: `grep -h "^found:" backlog/B*.md | sed 's/,.*//' | sort | uniq -c`*

*ran: `grep -n "found" doc/hl_rqmt/tracking.md | head -5`*

*ran: `sed -i 's/^found: python-complete, 2026-10-30/found: master, 2026-10-30/' backlo`*

Now the HLD: Question 4, the `tup`/`format` pointer, Generics, Variadics, `collections`, Question 12 and the triage.

*edited: `doc/hl_rqmt/python_complete.md`*

*edited: `doc/hl_rqmt/python_complete.md`*

*edited: `doc/hl_rqmt/python_complete.md`*

*edited: `doc/hl_rqmt/python_complete.md`*

*edited: `doc/hl_rqmt/python_complete.md`*

*edited: `doc/hl_rqmt/python_complete.md`*

*edited: `doc/hl_rqmt/python_complete.md`*

*ran: `python - <<'EOF'`*

*edited: `doc/hl_rqmt/python_complete.md`*

*ran: `grep -n -A5 "^12\. " doc/hl_rqmt/python_complete.md`*

*edited: `doc/hl_rqmt/python_complete.md`*

*ran: `grep -n "Every open item\|B34\]\] no .Collection\|items\b.*84\|84" doc/hl_rqmt/p`*

*ran: `sed -n 5,10p doc/hl_rqmt/python_complete.md && sed -n 113,128p doc/hl_rqmt/pytho`*

*ran: `sed -i 's/^| \[\[B34\]\] no 'Collection' | T | 'collections' (Question 4) |$/&\n`*

*ran: `git status --short && git diff --stat`*

I've added B124 and rewritten Question 4 in `doc/hl_rqmt/python_complete.md` around the four options, with the survey of option 1 as its pros and cons. The doc-link and backlog tests pass. Nothing is committed, and there are no edits of yours in the tree.

- **B124** (`backlog/B124-polymorphic-operators.md`, a `leak`, priority `normal`, found on `master`): built-in operators are polymorphic through rules in the checker, but a program can't write a polymorphic function. It also records the Python leak behind that: `emit` doesn't need types for `+` because Python's `+` works on numbers, strings and lists, which Rust's doesn't.
- **Question 4's proposal is Elm's design, in `collections`:**
  - `++` appends strings and lists (`appendable`), which is most of the churn;
  - `number` covers `+`, `-`, `*` and `quot` across the five number types;
  - `comparable` covers ordering;
  - all three can be used in a program's own `sig`s;
  - `=` is defined for every type (Question 12);
  - interfaces get their own HLD after the epic.
- **Other sections that point to it:**
  - "Where things stand" (the bounds bullet);
  - the `tup`/`format` pointer;
  - Generics: a new bullet saying the first bounds come in `collections`, spelled in Rust as `Add` and `PartialOrd`;
  - Variadics: `+` would be typed `(Fn (number ...) number)` and `++` `(Fn (appendable ...) appendable)`;
  - the `collections` branch description;
  - Question 12: ordering goes to `comparable`.
- **Triage:** a B124 row under `collections`, and a note that it was added on 2026-10-30. `backlog/README.md` is regenerated.

Say gawc to commit.

## Owner

> Gawc, then let's run thru the questions

## Claude Code

*ran: `git status --short && f=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c87`*

Committed as `b0876d2` on master. There were no edits of yours to include, and it isn't pushed.

Now the questions, one at a time. Answer each with "agree", a different answer, or "skip".

**Question 1: what "complete" means, and how to test it.**

The draft definition: the Python version is complete when it's "a solid push-off point to a Rust target, and eventually a Rust host". It's tested by the four conditions in "Goals":
1. **Every open item is placed.** Each one is either closed, or decided as *lasting* with a reason, or explicitly deferred (P, I, and the rest of L).
2. **The semantics are Candy's own.** No S item is left open: the spec says what each construct means, without "as Python does".
3. **Two implementations agree.** The Python target and the interpreter both run the whole spec.
4. **The porting surface is written down.** It lists what a new target or host must supply.

The alternatives:
- **Less:** no interpreter. The second implementation would be the Rust target itself, so condition 3 waits for Rust. That's a shorter epic, but Rust would be the first test of the spec.
- **More:** the standard library's modules written, not just designed. That's a longer epic, and Rust would get a library to port.

**Proposed: the draft and the four conditions.** The interpreter is the cheapest way to show the spec doesn't depend on Python. And the library's modules can grow on both hosts once the layering is fixed.

## Owner

> Agree

## Claude Code

Agreed. I'll record each answer in the HLD as we go, as `**Answered 2026-10-30:**`. I'll make the edits at the end, unless you'd rather have them one by one.

**Question 2: the order of the branches.**

The proposed order:
1. **`typed-core`:** typed Core, the checker's MVP leftovers, nested `fn`s typed.
2. **`semantics`:** the borrowed semantics, decided in the spec one by one, including `show` and printing (B36, `high`).
3. **`collections`:** the list literal, tuple types, variadics, `++` and the constraint variables, `Any` cut down, the list operations.
4. **`namespaces`:** qualified names and the import forms.
5. **`library`:** the system revisited, the prelude trimmed, the std lib's layering, target extensions, the `test` module.
6. **`interpreter`:** a second implementation over typed Core.
7. **`host-macros`:** macros that don't need Python to run.
8. **`test-runner`:** the spec's runner in Candy.
9. **`porting-surface`:** writing down what a new target or host must supply.

The alternatives:
- **The interpreter second, as a probe:** it can't find a borrowed semantic by itself, since it would give the host the same meaning, and it would be rewritten after every language change that follows it.
- **`namespaces` first or second:** it's independent of `semantics` and `collections`. Moving it up is worth it only if you want qualified names soon. `collections` would also get `Long.+`-style names, though Question 4's proposal no longer needs them.

**Proposed: as listed.** `typed-core` goes first because the rest need it, then `semantics`, because it holds the only other `high` item. The interpreter is written once, against the settled spec.

## Owner

> Agree

## Claude Code

**Question 3: keep mypy?**

Today mypy checks the generated Python as a second check, after Candy's own checker. The choices are:
- **Keep it through the epic, and decide in `porting-surface`.** It catches the Python backend's mistakes: a wrong annotation, a bad spelling, or `emit` producing ill-typed Python from well-typed Core. Neither the checker nor the interpreter can see those. Its costs are time (every spec file and test program gets a `mypy --strict` run) and the workarounds it forces, such as the typed temporary in `match` and the generic-sum exception.
- **Drop it once Core is typed (after `typed-core`).** Tests get faster and the mypy workarounds go. But a backend bug would then show up only as a wrong run, if a test happens to hit it.

**Proposed: keep it through the epic.** Drop it, or keep it only for `bin` and the self-host check, once two implementations check the semantics.

## Owner

> Agree... I'd also like to, at some point, figure a way to make it an option to run any targets static type checker....

## Claude Code

Agreed, with your addition. I'll record it like this:
- **In the answer:** "a target may name a checker for its output, which the driver runs on request (`--check`): mypy for Python. For Rust, `rustc` checks anyway, so the option is a no-op there."
- **In the porting surface:** among what a target supplies, its output checker, as an optional item.
- **As a backlog `idea`, B125, placed in `porting-surface`:** "run the target's own static checker as an option".

That way mypy stops being a test-suite special case and becomes the Python target's entry. Say if you'd rather not have the item.

**Question 4: overloading.** We just settled this one: Elm's design in `collections` (`++` with `appendable`, `number`, `comparable`, `=` for every type), and interfaces after the epic. Shall I record it as agreed?

## Owner

> Agree

## Claude Code

**Question 5: target extensions.**

These are the operations only one target has, such as Python's `module-dir` and `load-macros`, or a Rust-only API later. The choices are:
- **A module per target:** `py.cdy`, found in the target's library directory. A program says it isn't portable by importing it, and a target that lacks the module gives an import error that names it. It's simple, it fits `namespaces` (`py.module-dir`), and it's how Gleam's `@external` modules and Rust's `std::os::unix` work.
- **Reader conditionals in one file:** Clojure's `#?(:clj … :cljs …)`. One file can serve several targets, but every reader and tool must know the targets, and code that isn't portable is harder to spot.

**Proposed: a module per target.** Each target's `system.cdy` part declares its own built-ins. The porting surface lists the module as optional for each target.

## Owner

> Agree

## Claude Code

**Question 6: parsec in Candy.**

The idea is a parser-combinator module in the standard library, `parse`. The reader stays hand-written, since it's on the bootstrap path and is fast enough. The module would be a proving ground for generics, closures, sum types and the constraint variables: parsec.py v4's design notes already set the style. The options:
- **Yes, as `parse`, in `library`'s second half,** if it's cheap there. It tests the language on real generic code before Rust arrives.
- **Later, after the epic:** nothing needs it, and the epic is long.
- **Required:** part of the exit test, as a library a Rust host would port.

**Proposed: yes, in `library`'s second half, if it's cheap there.** It isn't part of the exit test, so if it isn't cheap it moves after the epic, with an `idea` item.

## Owner

> Agree

## Claude Code

**Question 7: `Maybe`.**

Today `(Maybe t)` is Python's `t | None`:
- a `t` is accepted as a `(Maybe t)`;
- `nil` is any `Maybe`;
- there's no narrowing after `(= m nil)` (B20);
- missing values come out as `None` in several places: an `if` with no else, a `cond` with no match, the value of `def` (B21).

This is the biggest S item, and the one that changes the most programs. The choices are:
- **A real sum:** `(deft (Maybe a) (Some ((v a))) (None))`, taken apart with `match`. It's what ML, Elm, Gleam and Rust do (`Option`), and it maps to Rust directly. Every `Maybe` in the translator would change (`map-get`-style lookups, `find`, optional fields), and so would the "`t` is a `Maybe t`" rule. That's a lot of churn, but mechanical, like `+`.
- **`t | None`, kept *lasting*, with narrowing:** less churn, and it reads like Kotlin's or TypeScript's nullable types. Rust would spell it `Option` anyway. The cost: `(Maybe (Maybe t))` collapses, so a lookup in a map of `Maybe`s can't tell "missing" from "present and `nil`". And narrowing is a checker feature to build (shared with B121).
- **Defer:** keep it as it is past the epic, marked as a leak.

**Proposed: decide it in the `semantics` HLD,** with both options costed there (the translator's uses counted, as for `+`). My leaning is the real sum: the collapse is a semantic hole Rust doesn't have, and the churn is a one-off. But it deserves its own survey.

## Owner

> So for the real sum option...`Maybe`  is a macro?

## Claude Code

No macro is needed. `Maybe` would be an ordinary generic sum, declared in the prelude like any user type:

```
(deft (Maybe a) (Some ((v a))) (None))
```

`Some` and `None` are then plain variant constructors, and `match` takes them apart, exhaustively:

```
(match (map-get-maybe m k)
  ((Some v) (use v))
  ((None) default))
```

**What changes in the checker:** the special rules go. "A `t` is a `(Maybe t)`" and "`nil` is any `Maybe`" both disappear, and `nil` is only `Unit`. Narrowing isn't needed at all, because `match` is the narrowing.

**Where macros or functions could help, as sugar:**
- Functions in the prelude, written in Candy: `with-default`, `maybe-map` and similar, like Elm's `Maybe.withDefault` and `Maybe.map`.
- Possibly a macro later for a shortcut like Rust's `?` or `if let`, such as `(when-some (v e) body)`. That would be convenience, not the definition.

**What it costs on Python:** each `Some` is a `NamedTuple` allocation, and `match` is an `isinstance` chain. Generic sums already skip the typed temporary because of mypy's speed problem with them. The backend could later represent `Some` more cheaply. It couldn't simply drop the wrapper, though, since that brings back the collapse.

**What it does to the translator's own code:** every lookup that may miss changes from `(if (= x nil) …)` to a `match`. Counting those uses is part of the `semantics` HLD's survey.

So the real-sum option is "a prelude `deft` and fewer checker rules". Is the proposal for Question 7, deciding it in the `semantics` HLD with both options costed, agreed?

## Owner

> Sorry, ya a type, tracking now .. agree

## Claude Code

Agreed. I'll record the leaning towards the real sum as part of the answer.

**Question 8: how far testing in Candy goes.**

The choices are:
1. **The `test` module only:** assertions and a runner a Candy program can use (`(test "name" (expect-equal …))`). pytest still runs the spec and the test programs.
2. **That and the spec's runner:** the conformance suite in Candy, which reads `spec/*.md`, runs the `candy run` and `candy error` blocks, and checks their output. That's what a second host needs, since it can't use pytest. The runner needs:
   - the interpreter (or a target) to run the examples;
   - `library`'s `string` module, to read markdown;
   - `semantics`' errors as values, to check `candy error` blocks without crashing.

   So it comes after all three: that's the `test-runner` branch, eighth.
3. **Everything in Candy:** pytest only for the Python-only checks (mypy, self-host, bootstrap). That's the most work, and much of it is Python-specific anyway.

**Proposed: the second.** The rest moves to Candy when a second host needs it.

## Owner

> Agree

## Claude Code

**Question 9: variadics or currying?**

They don't mix: currying needs every function to have a fixed arity, and rest parameters break that. The choices are:
- **Typed rest parameters:** `(Fn (Int ...) Int)` in a `sig`, and `(defn sum (& xs) …)` with the rest arriving as a list. That covers `+`, `-`, the comparisons, `and` and `or` as ordinary built-ins, with Question 4's `number` making `+` `(Fn (number ...) number)`. It maps to Rust as a slice (`&[T]`), or the target expands a call into pairs. Partial application is just a `fn`: `(fn (x) (+ x 1))`.
- **Curried types and partial application (B93):** `(Fn (Int Int) Int)` means `Int -> Int -> Int`, so `(+ 1)` is a function. That's elegant in ML and Haskell, but Lisp syntax already has variadic `+`. Rust has no currying, so it would lower to closures. And an under-applied call stops being an arity error.

`put`, `format` and `tup` aren't rest parameters either way. They take mixed types, so `put` and `format` become macros over `show`, and `tup` stays special (or becomes syntax).

**Proposed: rest parameters, of one type, in `collections`.** Currying is dropped (*lasting*), with `fn` (or a later `partial` macro) covering partial application. B93 would close as `dropped`.

## Owner

> Agree... Still not a fan of the `&`... But I'll get over it

## Claude Code

Agreed. I'll record the spelling as open for the `collections` HLD, with no `&` in the answer. Some alternatives to weigh there:
- **`...` after the name, mirroring the `sig`:** `(sig sum (Fn (Int ...) Int))` with `(defn sum (xs ...) …)`. The type and the parameter read the same way, which is my pick.
- **A keyword, as Common Lisp does:** `(defn sum (&rest xs) …)` (`&rest`) or `(defn sum (:rest xs) …)`. It's explicit, but just as noisy as `&`.
- **Scheme's dotted tail:** `(defn sum (a . rest) …)`. It needs a `.` in the reader, and reads poorly.

**Question 10: namespaces' scope.**

Two parts:
- **Where:** a branch of its own, before `library` (proposed), so `library`'s modules are designed with qualified names (`string.split`, `py.module-dir`). Or the first half of `library`, which makes one long branch.
- **Types and values: one namespace or two?** Candy has one today, so `A` names one thing, a type, a variant or a value. Two (Haskell-style), where a type `A` and a constructor `A` can coexist, would make B40 and B119's "is a variant, not a type" a matter of context. The translator and the tests rely on one. Rust has two, but a target can mangle around that.

**Proposed: its own branch; one namespace, *lasting*.** B40 (a variant named like a type) and B119 (the misleading message) become a spec rule and an error message.

## Owner

> Keep it as an option .. agree  "its own branch; one namespace"

## Claude Code

Recorded as: **its own branch, and one namespace *for now*,** with two namespaces kept as an option rather than ruled out. So B40 and B119 get a rule and a message under one namespace, which the `namespaces` HLD can revisit. If by "keep it as an option" you meant the `...` spelling from Question 9, say so and I'll put *lasting* back.

**Question 11: the list operations.**

`system.cdy` already has `map`, `filter`, `fold` (a left fold), `any`, `all`, `find`, `take`, `drop`, `zip` and others. The question is what to add:
- **`map-acc`:** a `map` that threads a state, `(Fn ((Fn (s a) (Tup s b)) s (List a)) (Tup s (List b)))`, as in OCaml's `fold_left_map` and Haskell's `mapAccumL`. The translator's hand-written loops (B123) mostly build a list while carrying something, so this is what moves them onto library operations.
- **`reduce`** (a fold with no start value): it needs a non-empty list, which Candy can't express in a type. On an empty list it's either a run-time failure or a `Maybe` result, which is better after Question 7.
- **A right fold:** nothing uses one, and on tuples it's no cheaper than reversing.

**Proposed: `map-acc` only,** in `collections`. `reduce` waits for Question 7's `Maybe` (as `(Fn (…) (Maybe a))`), and the right fold waits for a use.

## Owner

> Keep it as an option was for the & rest stuff

## Claude Code

Got it. I'll fix both answers:
- **Question 9:** the rest parameter's spelling is open for the `collections` HLD, with `&` kept as an option alongside `...`, `&rest` and the dotted tail.
- **Question 10:** its own branch, and one namespace, *lasting*, as proposed. Two namespaces are no longer recorded as an option.

That leaves Question 11, above: `map-acc` only, `reduce` once `Maybe` is settled, and no right fold?

## Owner

> Agree

## Claude Code

**Question 12: `=` and `show` on a type variable.**

Today `(= x y)` and `"{x}"` on an `a` pass, because Python can compare and print anything. That's a bound nobody wrote down. The choices are:
- **Declared for every type, *lasting*:** every Candy type has structural equality and a `show`. Each target supplies them for all its types: Rust derives `PartialEq` and `Debug` (or a Candy `Show`) on every type it generates. That's possible because every Candy value is data: no functions compared (`=` on `Fn` types becomes a checker error), and no host objects shown (B49). It's Gleam's `==` and Elm's `==` and `Debug.toString`.
- **Rejected until interfaces come:** `=` on an `a` would become an error, like `+` on an `a` today. That's purer, but generic code such as `contains`, `find` with an equal value, or a map's keys couldn't be written, and the translator uses those.

Ordering (`<` on an `a`) isn't part of this. It's `comparable`'s job, in `collections` (Question 4).

**Proposed: declared for every type, in `semantics`, with `=` on function types rejected.** That last part is new: it makes the "every value is data" claim true.

## Owner

> Agree

## Claude Code

All twelve are answered. Now I'll write the answers in.

*ran: `sed -n 1,6p doc/hl_rqmt/python_complete.md && grep -n "porting surface\|porting-`*

*ran: `sed -n 279,300p doc/hl_rqmt/type_checker.md && sed -n 350,360p doc/hl_rqmt/pytho`*

*ran: `sed -n 384,402p doc/hl_rqmt/python_complete.md && sed -n 438,492p doc/hl_rqmt/py`*

*ran: `cat > /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e`*

*ran: `sed -n 555,575p doc/hl_rqmt/python_complete.md`*

*ran: `sed -n 576,600p doc/hl_rqmt/python_complete.md`*

Answers are in; now adding B125 and its triage row, then running the doc tests.

*ran: `sed -i 's/^| \[\[B97\]\] a library per target | L | 'library', 'porting-surface'`*

*ran: `sed -n '/^## Questions/,/^## The triage/p' doc/hl_rqmt/python_complete.md | grep`*

All twelve answers are recorded in `doc/hl_rqmt/python_complete.md`, as `*Answered:*` lines like `type_checker.md`'s. The doc-link and backlog tests pass. Nothing is committed yet.

- **The status line** now reads "proposal (2026-10-29), questions answered (2026-10-30)", and the heading is "Questions (answered: the proposals, 2026-10-30)".
- **Five answers carry extras from our discussion:**
  - Question 3: a target's own static checker can be run as an option.
  - Question 6: if `parse` isn't cheap in `library`, it moves after the epic as an `idea`.
  - Question 7: the leaning towards the real sum, a prelude `deft` that is Rust's `Option`.
  - Question 9: the rest parameter's spelling is left to the `collections` HLD, with `&` kept as an option alongside `...`, `&rest` and a dotted tail. Question 9's own text no longer says `&`.
  - Question 11: `reduce` can come once `Maybe` is decided, returning a `(Maybe a)`.
- **One addition to Question 12:** `=` on function types becomes an error. That wasn't in the doc's proposal before; I added it when presenting the question, and it's what you agreed to.
- **Question 1's wording:** when I presented it, I paraphrased the exit test's four conditions loosely. The answer refers to the doc's own four conditions in "Goals", which are what count.
- **B125** (`idea`, priority `low`): run the target's own static checker as an option. It's in the `porting-surface` branch description and in the triage.

Two loose ends:
1. **Accepting the HLD.** Answering the questions isn't the same as Steps' step 1, "accept this HLD". That step also adds what an epic is to `doc/process.md`. I can do that as the next commit if you want it, and set the status to `accepted`.
2. **B93 (currying).** Question 9 drops currying for good. I've left B93 open, placed in `collections`, so that branch's HLD closes it. I could mark it `dropped` now instead.

Say gawc to commit the answers.

## Owner

> Gawc

## Claude Code

*ran: `git status --short && f=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c87`*

Committed as `e7f747e`: the twelve answers, plus B125. There were no edits of yours to include. Master is now two commits ahead of origin (`b0876d2` and `e7f747e`), and neither is pushed.

The two loose ends from before are still open:
1. **Accept the HLD:** add what an epic is to `doc/process.md`, and set the status to `accepted`.
2. **B93:** mark it `dropped` now, or leave it for the `collections` HLD to close.

## Owner

> Agree with both ...gawc and push

## Claude Code

*ran: `grep -n "^#" doc/process.md && grep -n -i "status\|proposal\|accepted" doc/proce`*

*ran: `sed -n 99,124p doc/process.md && sed -n 195,260p doc/process.md | tail -15 && gr`*

*ran: `sed -n 196,200p doc/process.md && sed -n 262,270p doc/hl_rqmt/python_complete.md`*

*ran: `sed -n 1,12p backlog/B77*.md && tail -4 backlog/B77*.md && sed -n 1,8p doc/hl_rq`*

Now the edits: process.md (epics), the HLD's status and step 1's Done note, B93 dropped, its triage row.

*ran: `cat > /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e`*

*ran: `f=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e54eb`*

I committed both changes as `47b4577` and pushed master, so origin now has `b0876d2`, `e7f747e` and `47b4577`. There were no edits of yours to include, and no tags were involved.

- **The epic is accepted.** Its status line now reads "accepted (2026-10-30)… `typed-core` first", and step 1 has a *Done* note.
- **`doc/process.md` now says what an epic is**, under "Design docs", "Kinds": an HLD whose steps are branches, titled "(epic HLD)". Each branch's HLD names its epic in its status line ("Epic: `python_complete.md`"), and the epic gets a *Done* note per branch. The process log has a 2026-10-30 entry for this.
- **B93 (currying) is `dropped`, *lasting*,** with a note pointing to Question 9. It's out of the triage, and the variadics section no longer counts it as open.

The next step is the `typed-core` branch, starting with its HLD.

## Owner

> Go

## Claude Code

*ran: `sed -n 7,50p doc/process.md && grep -n "typed-core" doc/hl_rqmt/python_complete.`*

*ran: `sed -n 300,330p doc/hl_rqmt/python_complete.md && for b in 15 19 120 122 59 14 1`*

*ran: `grep -n "^(deft" src/cdy/core.cdy src/cdy/check.cdy src/cdy/lower.cdy | head -40`*

*ran: `sed -n 1,60p src/cdy/core.cdy && sed -n 1,90p src/cdy/check.cdy`*

*ran: `for c in Lit Local Global Prim Call If Do Lambda Tuple Fmt Field Assoc MatchE Te`*

Surveying Core, the checker and `emit` so the `typed-core` HLD can say what "typed Core" costs. A bit more reading, then I'll draft it.

*ran: `grep -n "Any" src/cdy/emit.cdy src/cdy/lower.cdy | head -20 && sed -n 11,40p src`*

*ran: `sed -n 1,40p src/cdy/form.cdy && grep -n "infer\b\|(defn infer " src/cdy/check.c`*

*ran: `sed -n 1,30p doc/hl_rqmt/type_checker.md && grep -n "^## \|^### " doc/hl_rqmt/ty`*

*ran: `grep -n "innermost\|position" spec/25-checking.md | head && grep -rn "Lit (" src`*

*ran: `grep -n 'a id=' spec/25-checking.md && sed -n '/checking.definitions/,/a id="che`*

*ran: `grep -rn "line:col\|innermost" spec/*.md | head`*

Writing the `typed-core` HLD draft now, on master.

*wrote: `doc/hl_rqmt/typed_core.md`*

*ran: `grep -rn 'id="types.exist"' spec/ && grep -n "Txt\|IntLit" src/cdy/expand.cdy sr`*

*ran: `grep -n "(Txt\|(IntLit\|Lit " spec/50-macros.md tst/cdy/cdyc/macro_code/quoting.`*

*ran: `sed -n 35,60p spec/50-macros.md && grep -n 'a id=' spec/50-macros.md`*

*ran: `sed -n 76,90p spec/50-macros.md`*

*ran: `cat > /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e`*

I've drafted the `typed-core` HLD at `doc/hl_rqmt/typed_core.md`, with status `proposal` and the epic named in its status line. The doc-link test passes. Nothing is committed or branched yet.

**What it proposes:**
- **Types in Core:** every `Expr` node gets a type field. The checker *elaborates*: it returns each node rebuilt with its type, then puts the final types into the whole definition. `type-check` returns the typed `tops`.
- **Nested `fn`s typed (B19):** a nested Python `def` gets real annotations instead of `Any`, so mypy checks its body and its callers.
- **Positions on every node:** Core's leaves (B122) and the literal forms (B59), plus the positions B14 lacks (`main`'s type, `format` holes).
- **B119:** a variant or value written as a type says what it is.
- **Steps:**
  1. positions;
  2. types in Core;
  3. nested `fn`s typed;
  4. the messages;
  5. docs.

**Two things the survey found:**
- **The churn:** a `match` on `Expr` names every field, so adding one touches about 185 places that take a node apart, across `core`, `check`, `lower` and `emit`.
- **Literal forms are part of the macro API.** `spec/50-macros.md` builds `(Txt (sym-name s))`, so a position on literals is a small language change for macro writers. Errors in a macro's expansion are already reported at the call.

There are six questions. One at a time:

**Question 1: how Core carries types and positions.**
- **A field on every node:** `pos`, then `t` last, on all fourteen node kinds. Only this option gives "every `Expr` has its type", and a later need (`format`, a Rust backend) doesn't change Core again. It has the most churn, about 185 sites, mostly binding the new field as `_`.
- **A side table:** each local's key mapped to its type. It's the least churn and enough for B19. But it can't give a `format` hole's type, or the types a backend needs.
- **Types only where a backend needs them:** a `Lambda`'s, a hole's. Core would change again with each new need.

**Proposed: a field on every node, *lasting*.**

## Owner

> Agree (w/ proposed)

## Claude Code

**Question 2: a type variable left unsolved after checking.**

Some type variables are never pinned down, for example a `fn` that's never called, or an `empty-list` nothing is added to. The choices are:
- **Keep it as a `TVar` in Core, each backend choosing:** Python writes `Any`. It's honest, and nothing that translates today breaks.
- **Replace it with `Any` in Core:** simpler for backends, but it erases a fact a stricter target might want.
- **Make it an error,** like Rust's "type annotations needed": "can't tell the type of …". That's strictest, but it rejects programs that work today, such as `(put empty-list)` or an unused `fn`.

**Proposed: keep it as a `TVar`, with Python writing `Any`, *for now*.** Whether a target needs it to be an error is the porting surface's to decide.

## Owner

> Agree

## Claude Code

**Question 3: which of the checker's own leaks this branch fixes.**
- **B122 (an error in a leaf is reported at its parent):** it comes for free with the positions.
- **B120 (a `get` before a type is known is an error, not a constraint solved later):** it has never fired on the translator or the tests. The fix is a field constraint on a type variable, solved when the variable is bound.
- **B121 (no narrowing to the variant inside a `match` clause):** it has never mattered either, since a clause's names already read the variant's fields. Variants would need types of their own inside the checker.

**Proposed: B122 only.** B120 and B121 stay open at `low`, for when something needs them, which would most likely be `Maybe` as a real sum in `semantics`.

## Owner

> Agree

## Claude Code

**Question 4: positions on literal forms, and the macro API.**

Macro code builds and takes apart forms, so whatever shape literal forms have, macro writers see it. The choices are:
- **A `pos` field on each literal form, last, as `Sym` and `Lst` already have:** macro code writes `(Txt "x" NOWHERE)`, as it already writes `(Sym "at" NOWHERE)`. One spec rule changes (`macros.macro-code`'s example), along with `expand.cdy` and one test program. Errors in an expansion are still reported at the call.
- **Leave literal forms as they are:** only symbol leaves (`Local`, `Global`, `Prim`) get positions, and an error in a literal stays at its parent. B59 would be kept, *lasting*. That's no macro change, but only half of B122.
- **The field, plus a helper per literal** (`txt`, `int-lit`, … giving `NOWHERE`), so macro code needn't spell positions. That's friendlier, but it's eight helpers for something macros rarely do by hand, since they mostly quote, and `quasi` builds the forms itself.

**Proposed: the field, with no helpers.**

## Owner

> agree

## Claude Code

**Question 5: B15, the checker's MVP item, `high`.**

It has five parts left:
- mypy, which the epic's Question 3 placed in `porting-surface`;
- let-polymorphism;
- field constraints (B120);
- narrowing in a clause (B121);
- one error at a time.

The choices are:
- **Close it with this branch.** The parts without an item get one: let-polymorphism as an `idea`, and one error at a time as a `leak` (`low`). mypy is already the epic's. The backlog's `high` items are then what's really left, which would be B36 alone.
- **Keep it open, as the parent of those parts.** It would stay `high` and `in-progress` through the epic, since let-polymorphism isn't planned.

**Proposed: close it here, with the two new items.**

## Owner

> agree

## Claude Code

**Question 6: steps 1 and 2 together or apart.**

Both add a field to Core's nodes, so the same pattern sites change twice. The choices are:
- **Apart:** positions first, then types. That's two commits you can review separately, each with its own `boot/NN`. The positions step is smaller and needs no rewrite of the checker, so if the checker rewrite (step 2) runs into trouble, the positions are already in.
- **Together:** one pass over about 185 sites. That's less total editing, but one big commit that mixes a mechanical change with the checker's redesign.

**Proposed: apart, positions first.**

## Owner

> agree

## Claude Code

*ran: `cat > /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e`*

*ran: `grep -n -B1 -A1 "Proposed: a field on every node" doc/hl_rqmt/typed_core.md`*

*edited: `doc/hl_rqmt/typed_core.md`*

*ran: `sed -i 's/^1\. \*\*'typed-core':\*\* the checker writes/1. **'typed-core'** ('ty`*

*edited: `doc/hl_rqmt/python_complete.md`*

*ran: `f=doc/hl_rqmt/python_complete.md && grep -n "B120\]\] \'get\|B121\]\] no narrow\`*

*ran: `f=doc/hl_rqmt/python_complete.md`*

*ran: `grep -n "in \'semantics\'). First" doc/hl_rqmt/python_complete.md && sed -n 174,`*

*ran: `sed -n 323,330p doc/hl_rqmt/python_complete.md && sed -n 52,56p doc/hl_rqmt/type`*

*ran: `cat > /tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c874-4444-b20d-8e043e`*

All six answers are recorded in `doc/hl_rqmt/typed_core.md`, and the epic's `typed-core` entry links to the new HLD. The doc-link test passes. Nothing is committed yet.

One correction beyond the answers: B120 and B121 are in group T, and the epic's exit test leaves no T item open. So "stay open" now means "fixed in `semantics`", next to B20 (`Maybe`'s narrowing), which needs the same checker work. I've moved them there in the epic's triage and in its `semantics` branch description. `typed_core.md`'s Question 3 answer and its "Not goals" say so too. Let-polymorphism is still after the epic, since it'll be an `idea` and ideas don't block the exit test.

**Next, per the process:**
1. **Commit both docs on master** (gawc).
2. **"Start branch typed-core":** a branch off master, with a first commit that:
   - marks the HLD `accepted`;
   - adds one `task` item per step, B126–B130.

   I'd then go straight into step 1, the positions.

Say gawc for the docs, and "go" if you want the branch started as well.

## Owner

> gawc and go

## Claude Code

*ran: `git status --short && f=/tmp/claude-1000/-home-skerrj-dev-exp-candy/ba1b46a4-c87`*

*ran: `ls backlog | grep -i "type-checker-step\|checker-step" && cat backlog/B115*.md |`*

*ran: `git show 5a4ff9b --stat | head -20 && grep -n "^[0-9]\. \*\*" doc/hl_rqmt/type_c`*

*ran: `git switch -q -c typed-core refs/heads/master && git branch --show-current`*
