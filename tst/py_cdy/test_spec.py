"""The executable spec: the examples in ``spec/*.md`` (``doc/hl_rqmt/executable_spec.md``).

A spec file's fenced blocks are its examples:

- ``candy run``, then ``expect``: the program's output must be the ``expect`` block;
- ``candy error``, then ``expect-error``: translating it must fail, with a message that
  contains the ``expect-error`` text;
- ``candy errors``: one error example per line, ``source => message``, after any setup
  lines ended by a ``---`` line (one per table), which go before each row's source and
  must translate on their own;
- any other fence (``candy`` alone, ``markdown``): an illustration, not run.

The fences are read by ``script/doc_links.py`` (three or more backticks, closed by as many
or more, so a block of four can show blocks without running them; indented ones lose their
indent), which also reads the spec's ids (``tst/py_cdy/test_doc_links.py``). Each example
is translated by T1 and run, one test each, named ``file:line``. Each file's ``run``
examples also pass ``mypy --strict`` together, in one mypy run, and T2 translates them as
T1 does. A file whose status line says
``status: draft`` has its examples marked as expected failures (a passing one is reported).

A backlog item's ``candy run`` and ``candy error`` blocks (``backlog/``, ``script/backlog.py``)
are its repro: what *should* happen, run the same way as a strict expected failure, so the
test fails once the defect is fixed, until the example moves into its spec file.
"""

import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Literal, NamedTuple

import pytest
from mypy import api as mypy_api

from backlog import item_files
from cdy_rt.primitives import CandyFail
from doc_links import Block, blocks, status
from self_host import load, translate_with

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "spec"
# The index, which needs no status line (its examples show the block kinds).
INDEX = "README.md"


class SpecError(Exception):
    """A spec file whose blocks don't pair up."""


class Example(NamedTuple):
    """An example: a program, and its output (``run``) or part of its message (``error``);
    a ``setup`` (an error table's) has no expected text, and must translate."""

    kind: Literal["run", "error", "setup"]
    source: str
    expected: str
    line: int


def examples(text: str, name: str) -> tuple[Example, ...]:
    """The examples of the spec file ``name``, whose text is ``text``."""
    found: tuple[Example, ...] = ()
    pending: Block | None = None
    for block in blocks(text):
        if pending is not None:
            want = "expect" if pending.info == "candy run" else "expect-error"
            if block.info != want:
                raise SpecError(f"{name}:{pending.line}: {pending.info} needs {want} after it")
            if want == "expect":
                found = (*found, Example("run", pending.text, block.text, pending.line))
            else:
                found = (*found, Example("error", pending.text, block.text.strip(), pending.line))
            pending = None
        elif block.info in ("candy run", "candy error"):
            pending = block
        elif block.info in ("expect", "expect-error"):
            raise SpecError(f"{name}:{block.line}: {block.info} with no example before it")
        elif block.info == "candy errors":
            found = (*found, *error_table(block, name))
    if pending is not None:
        raise SpecError(f"{name}:{pending.line}: {pending.info} at the end, with no expect")
    return found


def error_table(block: Block, name: str) -> tuple[Example, ...]:
    """The examples of a ``candy errors`` block, one per line that isn't blank, each after
    the block's setup (the lines before a ``---`` line, if it has one). The setup is an
    example of its own too, which must translate."""
    rows = block.text.splitlines()
    separators = [i for i, row in enumerate(rows) if row.strip() == "---"]
    if len(separators) > 1:
        line = block.line + separators[1] + 1
        raise SpecError(f"{name}:{line}: a second --- (a table has one setup)")
    first = separators[0] + 1 if separators else 0
    setup = "".join(f"{line}\n" for line in rows[: first - 1]) if separators else ""
    found: tuple[Example, ...] = (Example("setup", setup, "", block.line + 1),) if setup else ()
    for offset, row in enumerate(rows[first:], start=first + 1):
        if row.strip() == "":
            continue
        if " => " not in row:
            raise SpecError(f"{name}:{block.line + offset}: expected source => message")
        source, message = row.split(" => ", 1)
        example = Example("error", setup + source.strip(), message.strip(), block.line + offset)
        found = (*found, example)
    return found


FILES = sorted(SPEC_DIR.glob("*.md"))
ITEMS = list(item_files(ROOT))
TEXTS = {path: path.read_text(encoding="utf-8") for path in (*FILES, *ITEMS)}


def marks(path: Path) -> tuple[pytest.MarkDecorator, ...]:
    """A draft file's examples may fail; a backlog item's repro must."""
    if path in ITEMS:
        return (pytest.mark.xfail(reason=f"{path.name}: not fixed yet", strict=True),)
    return (pytest.mark.xfail(reason="draft"),) if status(TEXTS[path]) == "draft" else ()


def cases(kind: str) -> list[object]:
    """Each example of ``kind`` in the spec, as a test case named ``file:line``."""
    return [
        pytest.param(example, id=f"{path.name}:{example.line}", marks=marks(path))
        for path in (*FILES, *ITEMS)
        for example in examples(TEXTS[path], path.name)
        if example.kind == kind
    ]


def runs(path: Path) -> tuple[Example, ...]:
    """The ``run`` examples of the spec file at ``path``."""
    return tuple(e for e in examples(TEXTS[path], path.name) if e.kind == "run")


RUN_FILES = [pytest.param(p, id=p.name, marks=marks(p)) for p in FILES if runs(p)]


def run(source: str, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Write ``source`` to a file in ``tmp_path`` and run it from the repository root."""
    path = tmp_path / "example.py"
    path.write_text(source, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(path)], capture_output=True, text=True, check=False, cwd=ROOT
    )


@pytest.mark.parametrize("example", cases("run"))
def test_run(example: Example, t1: ModuleType, tmp_path: Path) -> None:
    done = run(translate_with(t1, example.source), tmp_path)
    assert done.returncode == 0, done.stderr
    assert done.stdout == example.expected


@pytest.mark.parametrize("example", cases("error"))
def test_error(example: Example, t1: ModuleType) -> None:
    with pytest.raises(CandyFail, match=re.escape(example.expected)):
        translate_with(t1, example.source)


@pytest.mark.parametrize("example", cases("setup"))
def test_setup(example: Example, t1: ModuleType) -> None:
    translate_with(t1, example.source)


@pytest.mark.parametrize("path", RUN_FILES)
def test_mypy_strict(path: Path, t1: ModuleType, tmp_path: Path) -> None:
    outs = [tmp_path / f"example_{example.line}.py" for example in runs(path)]
    for out, example in zip(outs, runs(path), strict=True):
        out.write_text(translate_with(t1, example.source), encoding="utf-8")
    stdout, _, code = mypy_api.run(["--strict", "--no-incremental", *map(str, outs)])
    assert code == 0, stdout


@pytest.mark.parametrize("path", RUN_FILES)
def test_t1_and_t2_agree(path: Path, t1: ModuleType, t2: tuple[Path, str]) -> None:
    t2_module = load(t2[0])
    for example in runs(path):
        assert translate_with(t2_module, example.source) == translate_with(t1, example.source)


def test_spec_files_have_a_status() -> None:
    missing = [p.name for p in FILES if p.name != INDEX and status(TEXTS[p]) == ""]
    assert not missing, f"no status: draft|stable|deprecated line in {missing}"


# --- the runner itself ---


def test_blocks_and_nested_fences() -> None:
    text = "a\n```candy run\n(put 1)\n```\n````markdown\n```expect\n1\n```\n````\n"
    assert blocks(text) == (
        Block("candy run", "(put 1)\n", 2),
        Block("markdown", "```expect\n1\n```\n", 5),
    )


def test_indented_fences() -> None:
    text = "- a rule:\n\n  ```candy run\n  (put 1)\n    (put 2)\n  ```\n"
    assert blocks(text) == (Block("candy run", "(put 1)\n  (put 2)\n", 3),)


def test_examples_pair_up() -> None:
    text = (
        "```candy run\n(put 1)\n```\n```expect\n1\n```\n"
        "```candy error\n(put x)\n```\n```expect-error\nunknown name x\n```\n"
        "```candy errors\n(put y) => unknown name y\n\n(put ()) => empty form\n```\n"
    )
    assert examples(text, "t.md") == (
        Example("run", "(put 1)\n", "1\n", 1),
        Example("error", "(put x)\n", "unknown name x", 7),
        Example("error", "(put y)", "unknown name y", 14),
        Example("error", "(put ())", "empty form", 16),
    )


def test_error_table_setup() -> None:
    text = "```candy errors\n(sig s Int)\n(def s 1)\n --- \n(put t) => unknown name t\n```\n"
    assert examples(text, "t.md") == (
        Example("setup", "(sig s Int)\n(def s 1)\n", "", 2),
        Example("error", "(sig s Int)\n(def s 1)\n(put t)", "unknown name t", 5),
    )


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("```candy run\n(put 1)\n```\n```candy\nx\n```\n", "t.md:1: candy run needs expect"),
        ("```expect\n1\n```\n", "t.md:1: expect with no example before it"),
        ("```candy error\n(put x)\n```\n", "t.md:1: candy error at the end"),
        ("```candy errors\n(put x)\n```\n", "t.md:2: expected source => message"),
        ("```candy errors\n(def a 1)\n---\n---\n```\n", "t.md:4: a second ---"),
    ],
    ids=["no-expect", "orphan-expect", "unclosed-pair", "bad-row", "second-separator"],
)
def test_examples_that_dont_pair_up(text: str, message: str) -> None:
    with pytest.raises(SpecError, match=re.escape(message)):
        examples(text, "t.md")


def test_status() -> None:
    assert status("# Match\n\nstatus: draft, since: sum-types\n") == "draft"
    assert status("# Match\n\nstatus: stable\n") == "stable"
    assert status("# Match\n\nStatus is stable.\n") == ""
