"""The old name of ``spelling.py``, kept for one bootstrap step: the ``bin`` before
``runtime-names`` imports ``cdy_rt.table`` (``doc/hl_rqmt/runtime_names.md``, "Bootstrap").
Removed in step 2."""

from cdy_rt.spelling import SPELLINGS as INITIAL_TABLE

__all__ = ["INITIAL_TABLE"]
