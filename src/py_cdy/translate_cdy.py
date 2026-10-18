"""The whole translator: Candy source text to Python source text.

parse (``parse_cdy``) → ``analyse`` (``core_cdy``) → ``lower`` (``lower_cdy``) →
``emit_py``. See "Layers" in ``doc/hl_rqmt/iMVP_py_translator.md``.
"""

from parsec import parse

from cdy_rt.table import INITIAL_TABLE, Table
from core_cdy import analyse_program
from emit_py import py_source
from lower_cdy import PY_CAPS, lower_program
from parse_cdy import program


def translate(text: str, table: Table = INITIAL_TABLE) -> str:
    """Candy source ``text`` as Python source. Raises ``ParseFailure`` or ``CandyError``."""
    return py_source(
        lower_program(analyse_program(parse(program, text), table), table, PY_CAPS), table
    )
