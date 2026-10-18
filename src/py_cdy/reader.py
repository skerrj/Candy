"""Read a Candy source file into a string (the first stage of the translator).

For the iMVP the reader just slurps the whole file. ``slurp`` and its path helpers are copied
from ``cdy_rt.table_defs`` for now, so the compiler doesn't depend on the runtime's helpers;
the search path itself still comes from ``cdy_rt.table``.
"""

# The copy from cdy_rt.table_defs is deliberate (see above).
# pylint: disable=duplicate-code

from collections.abc import Sequence
from pathlib import Path

from cdy_rt.table import SEARCH_PATH


def find_path(name: str, search_path: Sequence[str]) -> Path | None:
    """The first ``.cdy`` file under ``search_path`` whose stem matches ``name``.

    Files under a ``tmp`` directory (below the search root) are skipped.
    """
    stem = Path(name).stem
    matches = (
        path
        for root in search_path
        for path in Path(root).rglob("*.cdy")
        if path.stem == stem and "tmp" not in path.relative_to(root).parts
    )
    return next(matches, None)


def get_path(name: str, search_path: Sequence[str]) -> Path:
    """``name`` if it exists, otherwise the matching file under ``search_path``."""
    given = Path(name)
    found = given if given.exists() else find_path(name, search_path)
    if found is None:
        raise FileNotFoundError(f"can't find {name} (searched {', '.join(search_path)})")
    return found


def slurp(name: str, search_path: Sequence[str] = SEARCH_PATH) -> str:
    """The whole text of a Candy file, found as ``get_path`` describes."""
    return get_path(name, search_path).read_text(encoding="utf-8")
