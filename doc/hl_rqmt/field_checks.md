# Field checks (HLD)

**Status: accepted (2026-10-27), with the proposed answers to its questions, on branch
`field-checks`, after tag `name-checks`.**
[[B6]], the backlog's next small `high` defect, with the checks next to it: the names a
`deft` declares (its fields, and its type variables) aren't checked against each other,
or against what Python allows.

## Where things stand

`top-deft` (`src/cdy/core.cdy`) reads a record's or variant's fields (`deft-fields`) and
checks their types (`check-fields`, since `name-checks`), but not their names:

- **The same field twice** (`(deft V ((x Int) (x Int)))`, or in a variant) becomes a
  one-field Python class, silently ([[B6]]). A pattern with a name twice is already an
  error ("names in a pattern must be different").
- **Two fields that are one Python name** (`a-b` and `a_b`; `py-mangle` turns `-` into
  `_`) are the same: one field, silently. `name-checks` made this an error for top-level
  names, and left fields to this branch.
- **A field that starts with `_` or `-`** (`_x`, `-x`) translates, and fails when it
  runs: `NamedTuple` forbids a leading `_`, with Python's `ValueError` ([[B5]]).
- **The same type variable twice** (`(deft (P a a) ((x a)))`) translates, and fails when
  it runs, with Python's `SyntaxError: duplicate type parameter 'a'` (found writing this
  HLD; no item yet).

Variant and type names are already checked: a name defined twice, in one sum or across
`deft`s, is "defined more than once".

## Goals

- A `deft` whose fields, or type variables, repeat a name is an error, with its position.
- Two fields that would be one Python name are an error, as two top-level names are.
- A field Python can't spell is an error at translation, not at run time.
- Each defect's repro passes and moves into the spec (`[[types.records]]`).

**Not goals:** checking a constructor's arguments or the fields `get` names ([[B10]],
[[B30]]); a field named like a tuple method (`count`, `index`), which mypy rejects
("base class "tuple" defined the type as ...") because a record is a `NamedTuple`: a new
`leak`, with [[B29]].

## Proposal

### Repeated names ([[B6]])

In `top-deft`, for a record and for each variant: two fields with one name fail, `deft V:
field names must be different (x)`, at the `deft`'s position. The type variables get the
same check: `deft P: type variables must be different (a)`. Both are Candy's own rules
(*lasting*), so they go in `core.cdy`, where the position is.

### Python names (with [[B5]])

Where `emit.cdy` writes a class's fields, two fields that `py-mangle` makes one name fail,
as `add-globals` does for top-level names: `V: fields a-b and a_b are one name in Python
(a_b)`. A field that starts with `_` or `-` fails there too: `V: a field can't start
with _ in Python (_x)`. Both are the Python target's limits, not Candy's, so they belong
in `emit` (*for now*: no position, [[B14]]); the second is a leak, so [[B5]] closes with a
new `leak` item for it (or Question 1's other answer).

## Pros and cons

- **Pro:** four silent wrong outputs, or run-time failures in Python, become errors at
  translation.
- **Pro:** no generated name changes, so `bin`'s output only gains the checks: one rebuild
  per step that touches `src/cdy/`, no staging.
- **Con:** the `_x` rule is Python's, visible in Candy (a leak, recorded as one).
- **Why now:** [[B6]] is `high`, and the rest are the same few lines next to it.

## Steps

1. **Repeated names:** the field and type-variable checks in `top-deft`; [[B6]]'s repro
   passes and moves into `spec/20-types.md` (`[[types.records]]`), with a variant row and a
   type-variable row; the type-variable defect recorded as an item and closed.

   *Done.* As built:
   - **`core.cdy`:** `deft-fields` fails on a field whose name an earlier one has
     (`has-field`), at that field: `deft: field names must be different (x)`, for a
     record and a variant alike; `top-deft` fails on a repeated type variable
     (`repeated`), at the `deft`: `deft: type variables must be different (a)`. Neither
     names the type (the position does), unlike the HLD's `deft V: ...`.
   - **The spec:** a sentence in `[[types.records]]` (*lasting*) and three error rows; the
     type-variable defect is [[B112]], closed.
   - **Bootstrap:** one rebuild.
2. **Python names:** the clash and leading-`_` checks in `emit.cdy`; [[B5]]'s repro passes
   and moves into the spec; the leak recorded; the tuple-method leak recorded.

   *Done.* As built:
   - **`emit.cdy`:** `check-py-fields`, before a record's or a variant's class is
     written: two fields that `py-mangle` makes one name fail, `V: fields a-b and a_b are
     one name in Python (a_b)` (the first field as written, as `add-globals` does); a field
     whose Python name starts with `_` fails, `V: field -x can't start with _ in Python
     (_x)`. It reads the Python name, so `?x` (`_px`) is caught too. The type is named as
     `candy-name` writes it (`V (from module util)`), since `emit`'s errors have no
     position. Fields of different variants are different classes, so they don't clash.
   - **The spec:** `[[types.records]]` says both, the leading `_` *for now*, with three
     error rows.
   - **Backlog:** [[B5]] is done; the leading-`_` limit is the leak [[B113]], and a field
     named like a tuple method (`count`), which fails mypy, is the leak [[B114]] (both
     `low`, with [[B29]]).
   - **Bootstrap:** one rebuild.
3. **Docs:** CLAUDE.md (the `deft` checks, a History sentence), the iMVP doc's leak list
   if it still names `_x`.

   *Done.* As built: CLAUDE.md (the `deft` checks under "Sum types", the branch in
   "History"); the iMVP doc, whose Python translator rejected a field starting with `_`
   (as `CandyError`), notes that the Candy translator lost the check until now. Its leak
   lists are archived (`doc/archive/`), so they stay as they were. The spec changed with
   steps 1 and 2.

## Questions (answered: the proposals, 2026-10-27)

1. **A leading `_`: reject, or mangle field names so Python accepts them?** Mangling
   (`_x` to `f__x`, say) hides the limit, but changes how every field reads in Python and
   still leaves `count` and `index`. **Proposed: reject, for now** (a leak item).
2. **Where the Python-name checks go:** `emit` (no position, as `name-checks` did) or
   `core` (with a position, but then `core` knows Python's mangling)? **Proposed: `emit`,
   for now** ([[B14]]), as `name-checks` decided.
3. **One branch for both?** Step 2 could be its own later branch, leaving this one to
   [[B6]]. **Proposed: one branch**; both steps are small.
