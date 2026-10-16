"""Runtime helpers that translated Candy code calls (``table.py`` entries point here).

Started from schmuz's ``src/py_smz/smztils.py``. Differences from schmuz:

- No ``bop_table`` copy or renamed imports: ``SEARCH_PATH`` comes straight from ``table``.
- Names that clash with Python built-ins or keywords get a trailing ``_``: ``slice_``,
  ``in_``. ``join_it`` is now ``join``.
- ``spit`` takes ``(path, text)`` and writes a string, like Clojure's ``spit``.
  ``file_put_lines`` takes ``(path, lines)``. (schmuz had them in opposite orders.)
- ``slurp`` raises ``FileNotFoundError`` instead of calling ``exit()``, and looks for
  ``.cdy`` files.
- ``is_coll`` accepts tuples as well as lists.
- ``is_str`` is a plain type check. schmuz's version tested for a ``"``-quoted token.
- Added ``is_empty_str`` (schmuz's table referred to it, but smztils never defined it).
- Dropped the ``m_table_*`` functions (the self-hosted compiler calls ``table``'s functions
  directly), the ``parse_string_help*`` leftovers (schmuz's own ``parse.scm`` defined the
  one it used) and commented-out experiments.
"""

import sys
from collections.abc import Sequence
from pathlib import Path

from cdy_rt.table import SEARCH_PATH

# --- collections ---


def at[T](coll: Sequence[T], i: int) -> T:
    """The item at index ``i``."""
    return coll[i]


def slice_[T](coll: Sequence[T], i: int, j: int) -> Sequence[T]:
    """Items ``i`` up to (not including) ``j``."""
    return coll[i:j]


def join(coll: Sequence[str], delim: str) -> str:
    """The strings in ``coll`` joined with ``delim``."""
    return delim.join(coll)


def is_coll(expr: object) -> bool:
    """Whether ``expr`` is a list or tuple."""
    return isinstance(expr, (list, tuple))


def is_lit(expr: object) -> bool:
    """Whether ``expr`` is an atom rather than a list or tuple."""
    return not is_coll(expr)


def to_list[T](val: T) -> list[T]:
    """A one-item list holding ``val``."""
    return [val]


def in_(item: object, coll: Sequence[object] | str) -> bool:
    """Whether ``item`` is in ``coll``."""
    return item in coll


# --- strings ---


def is_str(expr: object) -> bool:
    """Whether ``expr`` is a string."""
    return isinstance(expr, str)


def is_empty_str(text: str) -> bool:
    """Whether ``text`` is the empty string."""
    return text == ""


def is_digit(text: str) -> bool:
    """Whether ``text`` is all digits (and not empty)."""
    return text.isdigit()


def is_alpha(text: str) -> bool:
    """Whether ``text`` is all letters (and not empty)."""
    return text.isalpha()


def is_neg_int(text: str, pos: int) -> bool:
    """Whether ``text`` has a ``-`` followed by a digit at ``pos``."""
    return text[pos : pos + 1] == "-" and text[pos + 1 : pos + 2].isdigit()


def isspace(text: str) -> bool:
    """Whether ``text`` is all whitespace (and not empty)."""
    return text.isspace()


def isspace_at(text: str, pos: int) -> bool:
    """Whether the character at ``pos`` is whitespace."""
    return text[pos].isspace()


def to_int(text: str) -> int:
    """``text`` parsed as an integer."""
    return int(text)


def strip(text: str, chars: str) -> str:
    """``text`` without leading or trailing characters from ``chars``."""
    return text.strip(chars)


def replace(text: str, old: str, new: str) -> str:
    """``text`` with the first ``old`` replaced by ``new``."""
    return text.replace(old, new, 1)


# --- files ---


def find_path(name: str, search_path: Sequence[str]) -> Path | None:
    """The first ``.cdy`` file under ``search_path`` whose stem matches ``name``.

    Files under a ``tmp`` directory are skipped.
    """
    stem = Path(name).stem
    matches = (
        path
        for root in search_path
        for path in Path(root).rglob("*.cdy")
        if path.stem == stem and "tmp" not in path.parts
    )
    return next(matches, None)


def get_path(name: str, search_path: Sequence[str]) -> Path:
    """``name`` if it exists, otherwise the matching file under ``search_path``."""
    given = Path(name)
    found = given if given.exists() else find_path(name, search_path)
    if found is None:
        raise FileNotFoundError(f"can't find {name} (searched {', '.join(search_path)})")
    return found


def slurp(name: str) -> str:
    """The whole text of a Candy file, found as ``get_path`` describes."""
    return get_path(name, SEARCH_PATH).read_text()


def spit(path: str, text: str) -> None:
    """Write ``text`` to ``path``, replacing its contents."""
    Path(path).write_text(text)


def file_put_lines(path: str, lines: Sequence[str]) -> None:
    """Write ``lines`` to ``path`` as they are (they carry their own newlines)."""
    Path(path).write_text("".join(lines))


# --- rendering Python source ---


def get_indent(n: int) -> str:
    """Indentation for nesting level ``n`` (four spaces per level)."""
    return " " * 4 * n


# --- infra ---


def get_args() -> list[str]:
    """The command-line arguments, without the program name."""
    return sys.argv[1:]
