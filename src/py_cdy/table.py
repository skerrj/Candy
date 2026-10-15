"""The initial Candy symbol table: what each built-in Candy symbol translates to in Python.

Modelled on schmuz's ``src/py_smz/table.py`` (``OP_TABLE``). Differences from schmuz:

- Entries are typed ``TableEntry`` records instead of dicts, and ``kind`` says how the
  translator renders the symbol (operator, call, value, special form).
- The table is immutable. ``add_fun`` returns a new table instead of changing a global, so
  the translator (and later the self-hosted compiler) passes the table along.
- ``arity`` is ``None`` when a function takes any number of arguments. Calls render every
  argument (schmuz rendered only ``arity`` of them, defaulting to 1).
- Generated code refers to helpers through ``RUNTIME_MODULE`` and ``TABLE_MODULE``, so
  changing where they live is a one-line change here.
- Candy literals (``true``/``false``, chars, string escapes) replace schmuz's ``true``,
  ``false``, ``LF``, ``DQ``, ``BS``, ``ES``, ... symbols.
"""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Literal, NamedTuple

# Modules the generated code imports, by name. ``RUNTIME_MODULE`` holds the helper functions
# (``table_defs.py``); ``TABLE_MODULE`` is this module, which the self-hosted compiler needs
# for the ``table-*`` functions.
RUNTIME_MODULE = "table_defs"
TABLE_MODULE = "table"
IMPORTS: tuple[str, ...] = ("math", "re", TABLE_MODULE, RUNTIME_MODULE)

# Where ``slurp`` looks for a Candy file that isn't found at the given path.
SEARCH_PATH: tuple[str, ...] = ("src", "tst", "lib")

# How the translator renders a symbol:
#   special  - a special form, translated by its own rule (``py`` is unused)
#   binop    - arithmetic, ``a + b``; folds left with more than two arguments
#   compare  - comparison, ``a < b``; chains with more than two arguments
#   boolop   - ``and`` / ``or``; short-circuits
#   unary    - prefix operator, ``not a``
#   call     - a function call, ``py(args...)``
#   value    - a Python expression, used as is (``math.pi``, ``None``)
Kind = Literal["special", "binop", "compare", "boolop", "unary", "call", "value"]


class TableEntry(NamedTuple):
    """What one Candy symbol translates to."""

    py: str
    kind: Kind
    arity: int | None = None


Table = Mapping[str, TableEntry]


def special() -> TableEntry:
    """An entry for a special form."""
    return TableEntry("", "special")


def call(py: str, arity: int | None = None) -> TableEntry:
    """An entry for a function call to the Python name ``py``."""
    return TableEntry(py, "call", arity)


def runtime(name: str, arity: int | None = None) -> TableEntry:
    """An entry for a call to a helper in ``table_defs.py``."""
    return call(f"{RUNTIME_MODULE}.{name}", arity)


def table_fn(name: str, arity: int | None = None) -> TableEntry:
    """An entry for a call to a function in this module."""
    return call(f"{TABLE_MODULE}.{name}", arity)


def value(py: str) -> TableEntry:
    """An entry for a Python expression used as a value."""
    return TableEntry(py, "value")


SPECIAL_FORMS: Table = {
    "import": special(),
    "def": special(),
    "defn": special(),
    "do": special(),
    "if": special(),
    "cond": special(),
    "let": special(),
    "fn": special(),
    "quote": special(),
    "format": special(),
    "tup": special(),
}

MATH: Table = {
    "PI": value("math.pi"),
    "sin": call("math.sin", 1),
    "cos": call("math.cos", 1),
    "tan": call("math.tan", 1),
    "+": TableEntry("+", "binop"),
    "-": TableEntry("-", "binop"),
    "*": TableEntry("*", "binop"),
    "/": TableEntry("/", "binop"),
}

BOOL: Table = {
    "=": TableEntry("==", "compare"),
    "!=": TableEntry("!=", "compare"),
    "<": TableEntry("<", "compare"),
    ">": TableEntry(">", "compare"),
    "<=": TableEntry("<=", "compare"),
    ">=": TableEntry(">=", "compare"),
    "and": TableEntry("and", "boolop"),
    "or": TableEntry("or", "boolop"),
    "not": TableEntry("not", "unary", 1),
    "nil": value("None"),
}

IO: Table = {
    "print": call("print"),
    "display": call("print"),
    "put": call("print"),
    "file-put-lines": runtime("file_put_lines", 2),
    "slurp": runtime("slurp", 1),
    "spit": runtime("spit", 2),
}

RE: Table = {
    "re-search": call("re.search", 2),
    "re-findall": call("re.findall", 2),
    "re-compile": call("re.compile", 1),
}

COLLECTION: Table = {
    "len": call("len", 1),
    "empty-list": value("[]"),
    "at": runtime("at", 2),
    "slice": runtime("slice_", 3),
    "join": runtime("join", 2),
    "is-coll": runtime("is_coll", 1),
    "to-list": runtime("to_list", 1),
}

STRING: Table = {
    "is-empty-str": runtime("is_empty_str", 1),
    "to-int": runtime("to_int", 1),
    "is-str": runtime("is_str", 1),
    "is-digit": runtime("is_digit", 1),
    "is-alpha": runtime("is_alpha", 1),
    "is-neg-int": runtime("is_neg_int", 2),
    "strip": runtime("strip", 2),
    "replace": runtime("replace", 3),
    "isspace-at": runtime("isspace_at", 2),
    "isspace": runtime("isspace", 1),
    "in": runtime("in_", 2),
}

# For the self-hosted compiler: read and extend a symbol table. schmuz called these
# ``op-tab-*`` and changed a global table; here they take the table and ``table-add-fun``
# returns a new one.
META_TABLE: Table = {
    "initial-table": value(f"{TABLE_MODULE}.INITIAL_TABLE"),
    "table-add-fun": table_fn("add_fun", 4),
    "table-is-special": table_fn("is_special", 2),
    "table-is-op": table_fn("is_op", 2),
    "table-is-bin-op": table_fn("is_bin_op", 2),
    "table-get-arity": table_fn("get_arity", 2),
    "table-get-py": table_fn("get_py", 2),
    "is-lit": runtime("is_lit", 1),
}

PY_RENDER: Table = {
    "get-indent": runtime("get_indent", 1),
}

INFRA: Table = {
    "PY_IMPORTS": value(f"{TABLE_MODULE}.IMPORTS"),
    "SYS_ARGS": value(f"{RUNTIME_MODULE}.get_args()"),
}

INITIAL_TABLE: Table = MappingProxyType(
    {
        **SPECIAL_FORMS,
        **MATH,
        **BOOL,
        **IO,
        **RE,
        **COLLECTION,
        **STRING,
        **META_TABLE,
        **PY_RENDER,
        **INFRA,
    }
)


def add_fun(table: Table, name: str, py: str, arity: int | None) -> Table:
    """``table`` plus a user function ``name``, called in Python as ``py``."""
    return MappingProxyType({**table, name: call(py, arity)})


def is_op(table: Table, name: str) -> bool:
    """Whether ``name`` is in the table at all."""
    return name in table


def is_special(table: Table, name: str) -> bool:
    """Whether ``name`` is a special form."""
    return name in table and table[name].kind == "special"


def is_bin_op(table: Table, name: str) -> bool:
    """Whether ``name`` renders as an infix operator (arithmetic, comparison, and/or)."""
    return name in table and table[name].kind in ("binop", "compare", "boolop")


def get_arity(table: Table, name: str) -> int | None:
    """The number of arguments ``name`` takes, or ``None`` for any number."""
    return table[name].arity


def get_py(table: Table, name: str) -> str:
    """The Python name or expression for ``name``; ``name`` itself if it isn't in the table."""
    return table[name].py if name in table else name
