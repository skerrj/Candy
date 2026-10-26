"""The backlog: one file per item in ``backlog/``, and its index (``doc/hl_rqmt/tracking.md``).

An item is ``backlog/B<n>-<slug>.md``: a title line, ``# B<n>: what it is``, then its fields,
one ``name: value`` line each, then its text::

    # B2: `(sig x (List))` crashes the translator

    kind: defect
    state: open
    priority: normal
    found: executable-spec, 2026-10-24
    fixed:
    where: `src/cdy/emit.cdy` (`emit-tcon`)
    refs: [[types.names]]

The fields are all there, in that order; ``fixed`` and ``where`` may be empty, ``refs`` is
links only (``[[id]]``, or empty). A defect's repro is a spec block (``candy run`` or
``candy error``, with its ``expect``) of what *should* happen: the spec runner
(``tst/py_cdy/test_spec.py``) runs it as an expected failure until the fix lands, when it
moves into its spec file. ``python script/backlog.py`` writes the index,
``backlog/README.md``; ``--check`` only says whether it is current.
"""

import re
import sys
from itertools import pairwise
from pathlib import Path
from typing import NamedTuple

from doc_links import LINK, anchors, blocks, links, tracked_docs

KINDS = ("defect", "leak", "tech-debt", "feature", "task", "idea")
STATES = ("open", "in-progress", "review", "done", "dropped", "kept")
# The states of work still to do; the others are closed.
OPEN = ("open", "in-progress", "review")
PRIORITIES = ("high", "normal", "low")
FIELDS = ("kind", "state", "priority", "found", "fixed", "where", "refs")
# The fields that can't be empty.
REQUIRED = ("kind", "state", "priority", "found")
NAME = re.compile(r"(B([1-9][0-9]*))-[a-z0-9]+(-[a-z0-9]+)*\.md")
TITLE = re.compile(r"# (B[1-9][0-9]*): (.+)")
FIELD = re.compile(r"([a-z]+):(?: (.*))?")
REPROS = ("candy run", "candy error")
INDEX = "backlog/README.md"


class BacklogError(Exception):
    """An item file that isn't one."""


class Item(NamedTuple):
    """A backlog item: its id, number and file, its title, and its fields."""

    id: str
    number: int
    path: str
    title: str
    kind: str
    state: str
    priority: str
    found: str
    fixed: str
    where: str
    refs: tuple[str, ...]


def item(path: str, text: str) -> Item:
    """The item in the file ``path`` (``backlog/B2-sig-list-crash.md``), whose text is
    ``text``."""
    name = NAME.fullmatch(Path(path).name)
    if name is None:
        raise BacklogError(f"{path}: an item's file is B<n>-<slug>.md (lowercase)")
    lines = text.splitlines()
    title = TITLE.fullmatch(lines[0]) if lines else None
    if title is None or title.group(1) != name.group(1):
        raise BacklogError(f"{path}:1: the first line is # {name.group(1)}: <title>")
    fields = fields_of(path, lines)
    for field in REQUIRED:
        if not fields[field]:
            raise BacklogError(f"{path}: {field} is empty")
    for field, allowed in (("kind", KINDS), ("state", STATES), ("priority", PRIORITIES)):
        if fields[field] not in allowed:
            raise BacklogError(f"{path}: {field} is {fields[field]}, not one of {allowed}")
    if fields["state"] == "done" and not fields["fixed"]:
        raise BacklogError(f"{path}: a done item says where it was fixed")
    if fields["state"] not in OPEN and any(b.info in REPROS for b in blocks(text)):
        raise BacklogError(f"{path}: a closed item has a repro left (move it to the spec)")
    refs = tuple(link.id for link in links(path, f"{fields['refs']}\n"))
    if LINK.sub("", fields["refs"]).strip(" ,"):
        raise BacklogError(f"{path}: refs are links only, [[id]]")
    return Item(
        name.group(1),
        int(name.group(2)),
        path,
        title.group(2),
        fields["kind"],
        fields["state"],
        fields["priority"],
        fields["found"],
        fields["fixed"],
        fields["where"],
        refs,
    )


def fields_of(path: str, lines: list[str]) -> dict[str, str]:
    """The fields of an item, from the lines after its title (and a blank line)."""
    rows = lines[2 : 2 + len(FIELDS)]
    if len(lines) < 2 or lines[1] != "" or len(rows) < len(FIELDS):
        raise BacklogError(f"{path}: the title, a blank line, then the fields {FIELDS}")
    found: dict[str, str] = {}
    for offset, (row, want) in enumerate(zip(rows, FIELDS, strict=True), start=3):
        field = FIELD.fullmatch(row)
        if field is None or field.group(1) != want:
            raise BacklogError(f"{path}:{offset}: expected {want}: ...")
        found[want] = (field.group(2) or "").strip()
    return found


def items(root: Path) -> tuple[Item, ...]:
    """Every item in ``root``'s backlog, by number; two items with one number are an
    error."""
    found = tuple(
        sorted(
            (item(f"backlog/{p.name}", p.read_text(encoding="utf-8")) for p in item_files(root)),
            key=lambda i: i.number,
        )
    )
    twice = [a.id for a, b in pairwise(found) if a.number == b.number]
    if twice:
        raise BacklogError(f"backlog: two items numbered {', '.join(twice)}")
    return found


def item_files(root: Path) -> tuple[Path, ...]:
    """The files of ``root``'s backlog that are items (all but the index)."""
    return tuple(sorted(p for p in (root / "backlog").glob("*.md") if p.name != "README.md"))


def index(found: tuple[Item, ...], rules: dict[str, str]) -> str:
    """The text of ``backlog/README.md`` for the items ``found``; ``rules`` gives each rule
    id's file, from the repository root, for a link to it."""
    order = {p: n for n, p in enumerate(PRIORITIES)}
    live = sorted(
        (i for i in found if i.state in OPEN), key=lambda i: (order[i.priority], i.number)
    )
    closed = [i for i in found if i.state not in OPEN]
    next_id = max((i.number for i in found), default=0) + 1
    out = [
        "# Backlog",
        "",
        "Generated by `python script/backlog.py` from the items here; don't edit. The format",
        "is in `script/backlog.py`, and why it is so in `doc/hl_rqmt/tracking.md`.",
        "",
        f"The next item is B{next_id}.",
        "",
        "## Open",
        "",
        *table(live),
        "## By rule",
        "",
        "The open items, by the ids in their refs (spec rules, and sections of other docs).",
        "",
    ]
    by_rule: dict[str, list[Item]] = {}
    for i in live:
        for ref in i.refs:
            if ref in rules:
                by_rule.setdefault(ref, []).append(i)
    for rule in sorted(by_rule):
        listed = ", ".join(item_link(i) for i in by_rule[rule])
        out.append(f"- [{rule}](../{rules[rule]}#{rule}): {listed}")
    if by_rule:
        out.append("")
    out += ["## Closed", "", *table(closed)]
    return "\n".join(out).rstrip("\n") + "\n"


def table(found: list[Item]) -> list[str]:
    """A table of ``found``'s items, or a line saying there are none."""
    if not found:
        return ["None.", ""]
    rows = [
        f"| {item_link(i)} | {cell(i.title)} | {i.kind} | {i.state} | {i.priority} |" for i in found
    ]
    return ["| Item | | Kind | State | Priority |", "|---|---|---|---|---|", *rows, ""]


def cell(text: str) -> str:
    """``text`` for a table cell, its ``|`` escaped."""
    return text.replace("|", "\\|")


def item_link(found: Item) -> str:
    """A Markdown link to an item, from the index."""
    return f"[{found.id}]({Path(found.path).name})"


def rule_files(root: Path) -> dict[str, str]:
    """Each id that a tracked doc outside the backlog defines, with the doc's path."""
    return {
        a.id: path
        for path, text in tracked_docs(root).items()
        if not path.startswith("backlog/")
        for a in anchors(path, text)
    }


def main(argv: list[str]) -> int:
    """Write the index (or, with ``--check``, say whether it is current)."""
    root = Path(__file__).resolve().parents[1]
    try:
        text = index(items(root), rule_files(root))
    except BacklogError as error:
        print(error, file=sys.stderr)
        return 1
    path = root / INDEX
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if "--check" in argv:
        if current != text:
            print(f"{INDEX} is out of date: run python script/backlog.py", file=sys.stderr)
            return 1
        return 0
    if current != text:
        path.write_text(text, encoding="utf-8")
        print(f"wrote {INDEX}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
