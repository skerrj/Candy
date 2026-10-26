"""Ids and links in the docs (``doc/hl_rqmt/tracking.md``, step 1).

An id is an anchor, ``<a id="match.exhaustive"></a>``, on the line before what it names (a
heading, or a rule's paragraph); more anchors on the same line are aliases of the first, old
ids kept after a rename. A link is ``[[match.exhaustive]]``. Both count only in prose: not
in a fenced block, nor in a code span (```[[id]]``` is an example, not a link).

The fenced blocks are read here too, for the spec's runner (``tst/py_cdy/test_spec.py``): a
fence is three or more backticks, closed by as many or more, so a block of four can show
blocks without running them; it may be indented (in a list item), and its lines lose that
indent.
"""

import re
import subprocess
from pathlib import Path
from typing import NamedTuple

FENCE = re.compile(r"( *)(`{3,})\s*(.*?)\s*")
ANCHOR = re.compile(r'<a id="([^"]*)"></a>')
LINK = re.compile(r"\[\[([^\]]*)\]\]")
CODE_SPAN = re.compile(r"(`+).+?\1")
# A dotted, lowercase id: `match.exhaustive`, `design.sum-types`.
ID = re.compile(r"[a-z][a-z0-9-]*(\.[a-z0-9-]+)+")
STATUS = re.compile(r"^status: (draft|stable|deprecated)(?:, since: (\S+))?\s*$", re.MULTILINE)


class Block(NamedTuple):
    """A fenced block: its info string (``candy run``), its text, and its opening line."""

    info: str
    text: str
    line: int


class Anchor(NamedTuple):
    """An id, where it is defined, and the id it is an alias of (``""`` for none)."""

    id: str
    path: str
    line: int
    alias_of: str


class Link(NamedTuple):
    """A link to an id, and where it is."""

    id: str
    path: str
    line: int


def fences(text: str) -> tuple[tuple[int, int], ...]:
    """The fenced blocks of the Markdown ``text``: the index of each one's opening line and
    of its closing line (the number of lines, if it is never closed)."""
    lines = text.splitlines()
    found: tuple[tuple[int, int], ...] = ()
    i = 0
    while i < len(lines):
        opening = FENCE.fullmatch(lines[i])
        if opening is None:
            i += 1
            continue
        closing = re.compile(f" *`{{{len(opening.group(2))},}}\\s*")
        j = i + 1
        while j < len(lines) and closing.fullmatch(lines[j]) is None:
            j += 1
        found = (*found, (i, j))
        i = j + 1
    return found


def blocks(text: str) -> tuple[Block, ...]:
    """The fenced blocks of the Markdown ``text``, in order."""
    lines = text.splitlines()
    found: tuple[Block, ...] = ()
    for start, end in fences(text):
        opening = FENCE.fullmatch(lines[start])
        assert opening is not None
        indent = len(opening.group(1))
        body = "".join(dedent(line, indent) + "\n" for line in lines[start + 1 : end])
        found = (*found, Block(opening.group(3), body, start + 1))
    return found


def dedent(line: str, indent: int) -> str:
    """``line`` without up to ``indent`` leading spaces (its fence's indent)."""
    return line[min(indent, len(line) - len(line.lstrip(" "))) :]


def prose(text: str) -> tuple[tuple[int, str], ...]:
    """The lines of ``text`` outside its fenced blocks, numbered from 1, with code spans
    blanked out."""
    inside = {i for start, end in fences(text) for i in range(start, end + 1)}
    return tuple(
        (i + 1, CODE_SPAN.sub("", line))
        for i, line in enumerate(text.splitlines())
        if i not in inside
    )


def anchors(path: str, text: str) -> tuple[Anchor, ...]:
    """The ids ``text`` defines; on a line with several, the first is the id and the rest
    are its aliases."""
    found: tuple[Anchor, ...] = ()
    for line, words in prose(text):
        ids = ANCHOR.findall(words)
        if ids:
            first = ids[0]
            found = (*found, Anchor(first, path, line, ""))
            found = (*found, *(Anchor(alias, path, line, first) for alias in ids[1:]))
    return found


def links(path: str, text: str) -> tuple[Link, ...]:
    """The links in ``text``."""
    return tuple(
        Link(target, path, line) for line, words in prose(text) for target in LINK.findall(words)
    )


def status(text: str) -> str:
    """The status of a spec file (``draft``, ``stable`` or ``deprecated``), or ``""``."""
    found = STATUS.search(text)
    return found.group(1) if found is not None else ""


def tracked_docs(root: Path, commit: str = "") -> dict[str, str]:
    """Every Markdown file git tracks under ``root`` (at ``commit``, or in the work tree),
    by path, with its text."""
    if commit:
        names = git(root, "ls-tree", "-r", "--name-only", commit).split()
        return {
            name: git(root, "show", f"{commit}:{name}") for name in names if name.endswith(".md")
        }
    names = git(root, "ls-files", "*.md").split()
    return {name: (root / name).read_text(encoding="utf-8") for name in names}


def git(root: Path, *args: str) -> str:
    """The output of ``git args`` in ``root``."""
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=True
    ).stdout
