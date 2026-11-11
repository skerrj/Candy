"""Tests for ``cdy_rt.spelling``: each built-in's Python spelling."""

from cdy_rt.spelling import PRIMITIVES_MODULE, SPELLINGS, Spelling


def test_spellings() -> None:
    assert SPELLINGS["="] == Spelling("==", "compare", f"{PRIMITIVES_MODULE}.eq")
    assert SPELLINGS["slurp"] == Spelling(f"{PRIMITIVES_MODULE}.slurp", "call")
    assert SPELLINGS["empty-list"] == Spelling("()", "value")
    assert "user-fn" not in SPELLINGS


def test_runtime_entries_exist() -> None:
    import importlib  # pylint: disable=import-outside-toplevel

    for entry in SPELLINGS.values():
        if entry.kind == "call" and "." in entry.py:
            module, name = entry.py.rsplit(".", 1)
            assert hasattr(importlib.import_module(module), name), entry.py
        if entry.value:
            module, name = entry.value.rsplit(".", 1)
            assert hasattr(importlib.import_module(module), name), entry.value


def test_every_operator_is_a_value() -> None:
    operators = {"binop", "compare", "boolop", "unary"}
    for name, entry in SPELLINGS.items():
        assert bool(entry.value) == (entry.kind in operators), name
