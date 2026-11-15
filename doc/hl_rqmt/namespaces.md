# Namespaces (HLD)

**Status: accepted (2026-11-12), with the answers to its questions (tasks [[B188]] to
[[B194]]); proposed 2026-11-11, revised 2026-11-12 in review (`import`'s forms, its shape
declared, no alias, one table of names), for branch `namespaces`. Epic: `python_complete.md` (its
fourth branch). After tag `collections-2`.** Qualified names, the import forms, what is
seen everywhere, macros' names, shadowing, private names, and the module kept to the
backend: the epic's "Namespaces" section, whose scope its Question 10 settled (a branch of
its own; types and values one namespace, *lasting*). The MVP this builds on is
`modules.md`; its "After the MVP" is the starting point.

## Where things stand

Counts from today's source (2026-11-11, after tag `collections-2`).

| Item | Today | Seen where |
|---|---|---|
| [[B47]] only `(import m)`, everything unqualified | one import form; two imports that define one name are an error at the import, even if neither is used | `programs.import`; the translator's 24 imports (`cdyc.cdy` 8, `expand.cdy` 5, `emit.cdy` 3, the rest 1 or 2) |
| qualified names | none: `m/x` is an ordinary name (`(def m/x 1)` translates and runs); no program, spec example or test writes one | `read.cdy` reads `u/greet` as one symbol |
| [[B40]] types and values share a namespace | `(deft Box (Box ...))` is "defined more than once"; decided *lasting* (epic, Question 10), not yet a rule | `core.cdy` |
| [[B11]] a variant with the same name as a macro | translates; a later `(M 1)` expands as the macro | its repro |
| [[B50]] the translator's five host built-ins are every program's | `py-spellings`, `load-macros`, `call-macro`, `module-dir`, `fresh-name` in `system.cdy` | `system.cdy` |
| shadowing | a local shadows any outer name, a built-in too (`expr.let`, *lasting*); a program's top-level definition of a built-in's name wins | `core.cdy` |
| private names | none: every top-level name is exported | `modules.md`, Question 1 |
| [[B65]] tests reach internals by Python names | 15 names, 25 uses (`t1.form__Sym`, `t1.read__read_forms`) | `tst/py_cdy/` |
| the names a file sees | seven maps by name, each added for one question: `top`, `variants`, `sums`, `types` and `names` (in `Exports` and `Scope`), `elsewhere` (`Scope`) and `from` (`Seen`); one namespace is a check across them, not their shape | `core.cdy` |
| the module in Core | lost at analysis: a `Global` holds `"util__greet"`, so a backend can't tell `greet` from module `util` | `core.cdy`, `emit.cdy` |
| [[B108]] the built-ins one flat namespace | every file sees every built-in; splitting them into modules is `library`'s | `system.cdy` |
| [[B45]] macro files use inclusion | a macro file's `import` pastes; macros are global to a program | `include.cdy`, `expand.cdy` |

## Goals

- **One table of names:** what a file sees, one map from a name to what it is, so one
  namespace is the table's shape and each rule below is written once.
- **Qualified names:** `m.name` reaches a name module `m` defines, as Clojure's.
- **The import forms:** chosen names, besides `(import m)`, the shape declared in
  `special.cdy`; two imports that define one name are an error only where the name is
  used unqualified.
- **What every file sees, written down:** the special forms, the operators, the
  built-ins and the prelude.
- **The rules that are decided but unwritten:** one namespace ([[B40]]), shadowing,
  a variant with the same name as a macro ([[B11]]).
- **Private names,** so a library module can have helpers.
- **The module kept to the backend:** a `Global` carries its module and its name, each
  target spelling them its own way, and the tests reach Candy names ([[B65]]).

## Not goals

- **The library split into modules** (`math.cos`, [[B108]]): `library`'s, which needs
  this branch's qualified names first.
- **Macro files as modules, macros imported and qualified** ([[B45]]): `host-macros`',
  when macro code runs on the interpreter. Macros stay global to a program, *for now*.
- **One output file per module, separate compilation:** a target's choice once the
  module reaches the backend (`multi_target.md`); Python stays one file.
- **Interfaces** (after the epic).
- **An alias** in `import`, or of any name: [[B187]], `alias`, a special form of its own,
  later.
- **The other special forms' shapes declared:** each keeps its own rule in `core.cdy`
  until a branch touches it (`defmacro`'s parameters fit `host-macros`).

## Proposal

### One table of names

What a file sees is in seven maps today, by name, each added for one question as it came
up: `top` (is it a value, 2026-10-17, T1's first stage), `variants` and `sums` (`match`,
the same day), `names` (the Python name, `modules` step 2), `types` (the number of type
arguments, `name-checks`), and `elsewhere` and `Seen`'s `from` (which module, for two
errors). Each was the least change then; one namespace was decided after them (the
epic's Question 10). A record is in three of them, and nothing keeps them agreeing.

They become one map, from a name as written to an `Entry`, a sum, roughly:

```
(deft Entry
  (Value   ((module String) (global String)))
  (Type    ((module String) (global String) (arity Int) (variants (List String))))
  (Variant ((module String) (global String) (sum String) (fields (List String))))
  (Clash   ((modules (List String)))))
```

A record is one entry, its type and its constructor (the one exception to one
namespace, written once). `Clash` is two imports that define the name, an error where it
is used. `global` is the prefixed string (`util__greet`) until the module in Core
replaces it. The exact kinds are the step's to settle, against how a record and its
constructor are recorded today. Outside the table, as now: locals (`env`), the built-ins
(`builtins`, until `library`), the macros (global, [[B45]]), and the checker's own tables
(`check.cdy`, by global name). A refactor: the Python output stays byte for byte the
same. mypy is slow narrowing a union of `NamedTuple`s, so the step measures the T2 check
and the build; if the sum is slow, `Entry` is one record with a kind field instead.

### Qualified names

A name with a `.` between two parts, `m.name`, is the name `name` that the module imported
as `m` defines, *lasting*. The reader is unchanged (it already reads `m.name` as one
symbol, and a number's `.` stays a number's); analysis splits it. A name may hold no other
`.` (`a.b.c`, `.x` and `x.` are errors), so a program's own name can't hold one either.
`m` is the import's qualifier, the module's file stem (`lib/util` is `util`). A `/` is no
qualifier, but an import's path; a name can't hold one either, reserved, except the
division operator `/` itself. A qualified name works for anything a module defines: a
value, a function, a type (`(sig p shapes.Point)`), a variant (`(shapes.Circle 1.0)`, and in a
pattern).

### The import forms

```
(import m)          ; everything unqualified, and m.name
(import m (a b))    ; a and b unqualified, the rest as m.name
```

- `(import m)` stays as it is, so the translator's 24 imports and every test keep working:
  every name `m` defines, unqualified, and each as `m.name` too.
- `(import m (a b))` makes only those names unqualified; the rest are reached as
  `m.name`. Each must be a name `m` defines ("`m` doesn't define `c`").
- Positional, with no marker words, so nothing is reserved. An alias would be a third
  position, `(import m (a b) u)`, if one is ever wanted there; [[B187]] proposes a form of
  its own instead.

**What's lost without an alias,** *for now* ([[B187]]): two modules with one file stem
(`util`, `lib/util`) still can't both be imported, as today, and a long stem can't be
shortened.

**`import`'s shape, declared.** `special.cdy` names the special forms today, and each
one's shape is a rule in `core.cdy`. `import`'s becomes data:

```
(special import (ModName (Opt (List Name))))
```

The shape's words are syntax categories, capitalised as types are but describing what is
written, not a value's type: `Name` (a symbol), `ModName` (a module path, `lib/util`),
`(List c)`, `(Opt c)` (may be left out, at the end), and later `Rest`, `Expr`, `Form`
as other forms need them. Analysis checks a use against it, and the error is written
from it: `expected (import ModName [(Name*)])`. A form declared with no shape,
`(special if)`, keeps its own rule. `import` is the first, and the only one in this
branch; `import-macros` (one `ModName`) could follow.

**Ambiguous only where used** (`modules.md`, "After the MVP"): two imports that define
one name are an error only where the name is used unqualified ("`greet` is defined by
`a` and `b`: write `a.greet` or `b.greet`"); a file's own definition still wins over
both.

### What every file sees

Unqualified, in every file, *lasting*: the special forms, the operators, the built-ins
(`system.cdy`) and the prelude's names. They have no qualifier (not `system.map`) until
`library` splits the built-ins into modules ([[B108]]), which can give each one; this
branch only writes the rule down.

### One namespace, a rule

Types, values and variants share one namespace per module, *lasting* (the epic's Question
10): a type and a value (or a variant) can't share a name, except a record's own
constructor, which is its type's name. `programs.top-level` says so ([[B40]] kept: a
rule, not a leak). A record's name being both its type and its constructor is the shape
[[B171]] would give `List`.

### Macros' names

*Corrected in step 5 (2026-11-13): a file's macros are its own, not the program's; see
its Done note.* Macros stay global to a program, *for now* until `host-macros` ([[B45]]): a `defmacro`'s
name, and those `import-macros` brings, are seen in every module. A variant, a value or a
type with the same name as a macro is an error at its definition ([[B11]], a defect fixed here), as a
local with one's name already is.

### Shadowing

What a name means, from the innermost: a local; the file's own top-level definition; an
unqualified import; the built-ins and the prelude, *lasting*. So a file's definition of a
built-in's name (`(defn text ...)`) is its own, in that file only, and a local shadows
everything (`expr.let`, as now). A qualified name is never shadowed. The translator's five
host built-ins stay in `system.cdy` ([[B50]], for `library`, which gives a file of
declarations only the translator imports).

### Private names

`(private a b)`, a top-level form, keeps names in their module: they aren't visible
unqualified, and `m.a` is an error ("`a` is private to `m`"). The default stays
everything exported. Question 4 weighs the alternatives: an export list, or a naming rule
(Clojure's `defn-`, Python's leading `_`).

### The module in Core, and the tests

- A `Global` carries its module and its name (`(Global "util" "greet" ...)`), and so do a
  definition and a type's name; analysis resolves each name, qualified or not, to them.
  A module's tops stay grouped, with its imports (`modules.md`, "After the MVP").
- `emit` spells them as now, `util__greet` (and the top module's unprefixed), so the
  Python output doesn't change. Another target spells them its own way
  (`multi_target.md`).
- The tests reach a Candy name, not a Python one ([[B65]]): a helper in `tst/py_cdy/`,
  `candy(t1, "form.Sym")`, reads the spelling from the translator's own mapping, so moving
  a function between modules changes the test's text only where the module's name is.

### The spec

| Rule | File | Step |
|---|---|---|
| `programs.import`: the two forms, ambiguity where used, the error from the shape | `10-programs.md` | 2, 3 |
| `programs.qualified` (new): `m.name`, for values, types, variants, patterns | `10-programs.md` | 2 |
| `programs.top-level`: one namespace; what every file sees; shadowing | `10-programs.md` | 5 |
| `programs.private` (new) | `10-programs.md` | 4 |
| `macros.defmacro`: global, *for now*; a definition with the same name as a macro an error | `50-macros.md` | 5 |
| `syntax.names`: a `.` in a name | `00-syntax.md` | 2 |

## Pros and cons

- **For:** two libraries that define one name can be used together; a reader sees where a
  name comes from; `library` can split the built-ins into modules; the backend knows a
  name's module, which a second target needs.
- **Against:** `(import m)` keeping everything unqualified is the easy path and stays the
  common one, so qualified names may stay rare; no alias until [[B187]]. One table of
  names rewrites every lookup in analysis (about 70 reads of the maps), before anything
  a program sees. The module in Core
  changes every `Global`, a mechanical change through `core`, `check`, `lower` and
  `emit`, each a chance to break a lookup; the fixpoint guards it.

## Bootstrap

Steps that change `src/cdy/` rebuild `bin`, one `boot/NN` each (from `boot/71`). One
table of names changes `core.cdy` only, no syntax, so it is one step.
`import`'s shape in `special.cdy` is a library change the step before can't read (its
`(special name)` takes no shape), so that step is staged (`old-library`, as `collections`
step 2 was), or two boot steps, the reader first. The new import form and `(private
...)` are new syntax: the translator can't use them in the
step that adds them, since the step before can't read them, so its own first uses wait a
step (as `to-list`'s removal waited, `collections_2.md`). Changing `Global` changes no
syntax, so it is one step.

## Steps

1. **One table of names** ([[B40]]'s shape): the seven maps one `Entry` map, `core.cdy`
   only; the output unchanged; mypy and the build measured.
   *Done (2026-11-12). As built:* `Entry` has five kinds: `Value`, `Record` (a type and
   its constructor), `Sum`, `VariantOf` (`Variant` is Core's) and `Elsewhere`; no `Clash`
   yet, which is step 2's. `Scope` keeps one `names` table, and `Exports` is its stem and
   its table (`module-names`, with `add-deft` and `add-entry`); `VInfo`, `Seen`,
   `find-variants`, `add-variants`, `type-arities`, `prefixed` and `blank-scope` are gone.
   `top-names` stays, for `expand.cdy`'s macro names. The lookups are small functions
   (`is-top-value`, `is-sum`, `type-arity`, `variant-sum`, `variant-fields`,
   `sum-variants`, `elsewhere-module`, `global-name`). A module's own names replace an
   import's whole entry, where before each map was merged on its own. One error changed:
   a sum's name used as a value said "S is not defined here; m defines it, but this file
   doesn't import m", even in the file that defines it; it is now "S is a type, not a
   value" (`types.exist`, a new row). Checked against `boot/70`'s `bin`: the same Python
   for the 11 test programs, the translator, and 378 of the spec's and the backlog's 379
   examples (the other is that error). The build 0.88 s to 0.90 s; mypy on the
   translator 1.64 s to 1.62 s.
2. **Qualified names** ([[B47]]): `m.name` for a module `(import m)` imports, for values,
   types and variants (and patterns); the `.` rule in names; ambiguity where used in place
   of the clash at import.
   *Done (2026-11-12). As built:* an import adds each name twice to the table, as `name`
   and as `stem.name`; `Scope` has the file's `qualifiers` (its imports' stems). Two
   imports that define one name make a `Clash` entry (`import-entry`), and `clash-error`
   reports it where it is used unqualified: as a value or a call, a type, or a pattern
   ("x is defined by a and b: write a.x or b.x"); the file's own definition replaces it.
   A name that holds a `.` is never defined (`dot-error`, in
   `add-entry`, `bind-local` and a field), and one that names nothing says why
   (`qualified-error`: not m.name, a module not imported, a name it doesn't define). Two
   places needed more than the table: `analyse-type` read `shapes.Shape` as a type
   variable (it starts lowercase), and `match` compares clauses by their bare names, so
   `(prelude.Some v)` and `(Some w)` are one variant twice; a variant now carries its
   sum's variants (`all`), for exhaustiveness. The rules: `programs.qualified` (new),
   `programs.import` and `programs.prelude` (a clash where used), `syntax.names` (no `.`);
   `tst/cdy/cdyc/qualified.cdy` (new) is the example with two modules, and
   `test_module_errors` has the clash (a value, a type), a module imported only by an
   import, and the prelude's clash where used. Checked against `boot/71`'s `bin`: the
   same Python for the translator and every example but the 12 new ones. The build 0.92 s
   to 0.94 s. In review the owner changed the separator to `.` (Question 3), built as
   above with `.` for `/` (`has-dot`), and `.5` in `syntax.numbers` now a qualified name
   with no module; a `/` in a name stays an error, reserved (the owner), so a definition's
   name is checked by `name-error`, for both.
3. **The name list, and `import`'s shape declared** ([[B47]]): `(import m (a b))`; the
   import's record (`modules.md`'s `Import`, without an alias); `(special import ...)`
   with its shape, the syntax categories `import` needs, the check and its error.
   *Done (2026-11-13). As built:* `special.cdy` declares
   `(special import (ModName (Opt (List Name))))`; `syntax.cdy` (new) reads a shape into
   `Syntax` (`SynName`, `SynModName`, `SynList`, `SynOpt`, the last only last), checks a
   form's arguments against it (`fits-shape`) and writes the error from it (`shape-text`:
   "import: expected (import ModName [(Name*)])"); `read-decls` (`core.cdy`) checks every
   declared shape. `include.cdy` reads import's shape from `special.cdy` once per module
   and checks each import with it (`import-parts`); its `Imp` carries the listed names
   (`only`, a `Maybe`), and a macro file's import (inclusion) can list none. Analysis gets
   an `Import` (`core.cdy`; `modules.md`'s, with `only` for its `Names`): every name goes
   in as m.name, the listed ones (or all) unqualified, and the rest as `Unlisted`, an
   entry whose use says "b: the import of m doesn't list it: write m.b" (`use-error`,
   which was `clash-error`); a listed name `m` doesn't define, or one listed twice, is an
   error at the name. An `Unlisted` name gives way to any other import's. The rule:
   `programs.import`; `tst/cdy/cdyc/import_list.cdy` (new) is the example, and
   `test_module_errors` has the name list's errors. `test_editor_grammar` reads a special
   form declared with a shape. Checked against `boot/72`'s `bin`: the same Python for the
   translator and every example but the new program, which it can't read. The build 1.00 s
   to 1.03 s. `boot/72` can't read the new `special.cdy`, so this step is staged
   `old-library`.
4. **Private names**: `(private ...)`, its errors; the translator's first private names in
   a later step, if any.
   *Done (2026-11-13). As built:* `(special private)`, with a rule of its own (no shape,
   so no staging: `boot/73` reads it). `module-exports` reads a module's `(private ...)`s
   into `Exports`' `privates` (`private-names`): each a name the file defines, listed
   once, not a variant ("private only with its type: (private S)"), a private sum's
   variants private with it. An importer's table has a `Private` entry for each, as
   `name` and as `m.name`; `use-error` says "x is private to m" and "m.x: x is private to
   m", and a name list "import: x is private to m". Like `Unlisted`, a `Private` entry gives
   way to another import's name (`hidden-entry`, which was `unlisted-entry`), and a private
   name is left out of the program's other modules' names (`elsewhere-names`), so one
   that isn't imported is unknown. Analysis skips the form; elsewhere it is "only allowed
   at top level", and expansion leaves it alone. The rule: `programs.private` (new);
   `tst/cdy/cdyc/private.cdy` (new, with `lib/counter.cdy`, an abstract type) is the
   example, and `test_module_errors` has the cross-module errors. The VS Code grammar
   knows `private`. The translator has no private names yet. Checked against `boot/73`'s
   `bin`: the same Python for the translator and every example but the two new ones,
   which it can't read. The build about 1.0 s, as before.
5. **The rules written down** ([[B40]], [[B11]], [[B50]]'s part): one namespace, what
   every file sees, shadowing; a variant or value with the same name as a macro an error.
   *Done (2026-11-13). As built:* three rules under `programs.top-level`, each with an
   example: `programs.namespace` (one namespace, a record's name its type and its
   constructor; [[B40]] kept), `programs.sees` (the built-ins, the prelude, and a file's
   own macros) and `programs.shadowing` (local, own, import, built-in; a qualified name
   never; [[B50]]'s five, *for now*). A `deft`'s type or variant with the same name as a macro is
   "M is a macro, so it can't be defined" (`analyse-top`, `macro-named`; [[B11]] done,
   its repro now `macros.binding`'s rows). Two findings: macros aren't global to a
   program, as "Macros' names" above says: a file's macros are its own `defmacro`s,
   those it loads with `import-macros` and the prelude's, and `import` doesn't pass them
   on (`expand-file`; `macros.import-macros` already said so), so `programs.sees` states
   that. And a file's own `text` changes `put`, whose expansion calls `text` (a note on
   [[B46]], *for now*: the built-ins have no qualifier until `library`). A file may also
   shadow a built-in type's name (`(deft List ...)`), as any built-in's. The naming rules,
   spread over the spec, have an index in `spec/00-syntax.md` ("Naming rules, in one
   place"), its last row pointing to the target's spellings (Python's, *for now*). Checked
   against `boot/74`'s `bin`: the same Python for every program, the translator and
   every example.
6. **The module in Core** ([[B65]]): `Global` with its module and name, definitions too
   (and the table's `global`); `emit`'s spelling unchanged; the tests' `candy` helper.
7. **Docs:** CLAUDE.md, the epic's fourth branch *done*, `modules.md`'s "After the MVP",
   `multi_target.md`'s "Modules and output units"; "Looking back".

## Questions

1. **What `(import m)` makes unqualified:** everything, as now (proposed), so nothing
   that works today breaks; or nothing, as Clojure's `require`, every use `m.name` unless
   its name list names it, which is clearer but rewrites the translator's uses of its own
   modules' names (about 1,030, in its 9 modules). **Proposed: everything, as now,**
   *lasting*. *Answer (2026-11-12, the owner): everything,* *lasting*. Weighed on the
   way: under this, an alias on a module matters only where a file writes `m.name` (a
   clash, the rest of a name list, or two stems alike), so leaving it out costs little;
   a file is one module, and two files with one stem (`util`, `lib/util`) stay an error.
2. **The import forms' spelling:** keywords (`(import m :as u :only (a b))`, as Clojure's
   `require`), marker words (`(import m as u)`), nested forms (`(import (only m a b))`, as
   R7RS), or positional, the shape declared? *Answer (2026-11-12, the owner):
   positional,* `(import m)` and `(import m (a b))`, *as a special form with its shape
   declared* in `special.cdy`; *no alias for now,* and a general `alias` form later
   ([[B187]]). Weighed on the way: `:as` looked like a keyword, which Candy hasn't (a
   value, self-evaluating, in Clojure); an alias third (`(import m (a b) u)`) needed the
   list written to reach it.
3. **The qualifier's separator:** `/` (proposed, as the epic decided, with a lone `/` the
   operator), or `.` (Python's, but `.` is likelier to be wanted for fields), or `::`
   (Rust's)? **Proposed: `/`,** as decided. *Answer (2026-11-12, the owner): `/`.*
   Checked: no name in the translator, the tests or the spec holds a `/` today; only
   `import`'s paths do (`lib/util`), a `ModName` by its declared shape, and a qualifier is
   a stem, so the two never meet (`util/greet`, never `lib/util/greet`). *Changed
   (2026-11-13, the owner, in step 2's review): `.`,* Python's, Java's and OCaml's.
   Question 8 had already found that `.` for modules needn't keep it from fields. Checked:
   no name in the translator, the library, the tests or the spec holds a `.`, and the
   reader keeps a number's (`3.14f`); a word starting with `.` (`.5`), a name until now,
   becomes a qualified name with no module, an error ("a number needs a digit before its
   ." for `.5` and `-.5`, `number-hint`). A `/` in a name stays an error,
   reserved (the owner, 2026-11-13), except the operator `/` itself.
4. **Private names:** a `(private a b)` form (proposed: one place, the default stays
   "everything exported", no rename); an export list (`(export a b)`, everything else
   private: clearer for a library, but every module must list its names); `defn-` and
   `def-` (Clojure's, per definition, but a form per kind); or a leading `_` (Python's
   convention as a rule, but `_` is a field's error in Python, [[B113]], and a parameter
   that is unused). **Proposed: `(private ...)`.** *Answer (2026-11-12, the owner):
   `(private ...)`.*
5. **Shadowing a built-in at top level:** allowed, the file's own definition wins in that
   file (proposed, as today); or an error, so `text` can't mean two things (safer, but
   every new built-in can break a program that defines its name, as `text` broke the
   reader in `collections`). **Proposed: allowed,** *lasting*. The shadowed built-in
   can't be reached in that file *for now*: the built-ins have no qualifier until
   `library` ([[B108]]), and [[B187]]'s `alias` is the other way back. *Answer
   (2026-11-12, the owner): allowed,* *lasting*.
6. **Order:** steps 1 to 6 as above, with the module in Core last (it changes no
   behaviour); or the module in Core first, so qualified names are built on it (cleaner
   code, but a large mechanical step before anything a program sees). **Proposed: the
   module in Core first,** if the survey shows qualified names need it to be resolved
   simply; else last. *To settle at step 1.* *Answer (2026-11-12, the owner): last,*
   settled in review, not at step 1. The survey, done then: steps 2 to 4 work on names
   as written, the maps' keys, and the module in Core changes their values, so it can
   come after them. It found seven maps, not one, so the owner added a step first: one
   table of names (above), in this branch rather than one of its own, since this
   branch's rules (the clash, the module, private names) shape its `Entry`. The module in Core is step 6, `Global` keeping its one string
   until then.
7. **The tasks:** one per step, B188 to B194, as `collections-2` did. **Proposed:
   yes.** *Answer (2026-11-12, the owner): as proposed.*
8. **Must `.` for fields and `.` for modules exclude each other?** (the owner, 2026-11-12,
   from Question 3) No: Python, Java and OCaml use one `.` for both. Candy resolves names
   statically, so `a.b` could be a module's name when `a` is an import's qualifier, and a
   field when `a` is a value (the checker already solves a `get` on a value of unknown
   type, [[checking.records]]). What it would need: a rule for a local with the same name
   as a qualifier (an error, or the local wins); chains read left to right (`m.p.x`, module
   `m`'s `p`, then its field `x`); a reader that splits on `.` but not in numbers
   (`3.14f`); and field syntax, which Candy hasn't (only `(get p x)`). OCaml tells the two
   apart by case (`M.x`, `r.x`). **Proposed: not exclusive, and not decided here:** this
   branch uses `/`, and a `.` for fields, for modules too or not, is the field syntax's
   question, later (a `brainstorm.md` entry, or an idea item). *Answer (2026-11-12, the
   owner): as proposed.* With Question 3 changed to `.` (2026-11-13), field syntax will
   need the rule for a local with the same name as a qualifier ([[B195]]).
