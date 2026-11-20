"""The docs' ids and links (``doc/hl_rqmt/tracking.md``, step 1; ``script/doc_links.py``).

Every Markdown file git tracks is read. An id (``<a id="match.exhaustive"></a>``) is
defined once, and dotted and lowercase; every link (``[[match.exhaustive]]``) is to an id
that exists, and a live doc (not in ``doc/archive/``) links to an id, not to one of its
aliases. A backlog item's id is its number, from its file's name (``backlog/B2-...md``,
``script/backlog.py``). In ``spec/``, every rule has an id: each example belongs to the
rule whose anchor is above it, and a stable rule has an example, or says where it is
*Tested in*. An id that was on ``master`` (at this branch's merge base) and is gone, with
no alias left, is a warning: a rename keeps the old id as an alias.
"""

import re
import subprocess
import warnings
from pathlib import Path

import pytest

from backlog import NAME
from cdy_rt.spelling import SPELLINGS
from doc_links import (
    ID,
    Anchor,
    Link,
    anchors,
    blocks,
    git,
    links,
    prose,
    status,
    tracked_docs,
)

ROOT = Path(__file__).resolve().parents[2]
DOCS = tracked_docs(ROOT)
ANCHORS = tuple(a for path, text in DOCS.items() for a in anchors(path, text))
LINKS = tuple(link for path, text in DOCS.items() for link in links(path, text))
# Each item's id, as an anchor on its title line.
ITEMS = tuple(
    Anchor(name.group(1), path, 1, "")
    for path in DOCS
    if path.startswith("backlog/") and (name := NAME.fullmatch(Path(path).name))
)
DEFINED = {a.id: a for a in (*ANCHORS, *ITEMS)}
# The spec's feature files (the index, spec/README.md, has examples of the blocks, no rules).
SPEC = {p: t for p, t in DOCS.items() if p.startswith("spec/") and p != "spec/README.md"}
EXAMPLES = ("candy run", "candy error", "candy errors")
ARCHIVE = "doc/archive/"
# The rule whose table indexes the built-ins.
INDEX = "library.builtins"


def where(item: Anchor | Link) -> str:
    """``path:line`` of an anchor or a link."""
    return f"{item.path}:{item.line}"


def test_ids_are_dotted_and_lowercase() -> None:
    bad = [f"{where(a)}: {a.id}" for a in ANCHORS if not ID.fullmatch(a.id)]
    assert not bad, bad


def test_ids_are_defined_once() -> None:
    seen: dict[str, Anchor] = {}
    twice = []
    for a in ANCHORS:
        if a.id in seen:
            twice.append(f"{a.id}: {where(seen[a.id])} and {where(a)}")
        seen[a.id] = a
    assert not twice, twice


def test_links_are_to_ids() -> None:
    unknown = [f"{where(link)}: [[{link.id}]]" for link in LINKS if link.id not in DEFINED]
    assert not unknown, unknown


def test_live_docs_link_to_ids_not_aliases() -> None:
    old = [
        f"{where(link)}: [[{link.id}]] is now [[{DEFINED[link.id].alias_of}]]"
        for link in LINKS
        if not link.path.startswith(ARCHIVE) and link.id in DEFINED and DEFINED[link.id].alias_of
    ]
    assert not old, old


def rules(text: str) -> tuple[tuple[int, int], ...]:
    """The spec rules in ``text``: each one's anchor line and the line its rule ends before
    (the next anchor, or past the end)."""
    lines = sorted(a.line for a in anchors("", text) if not a.alias_of)
    ends = [*lines[1:], len(text.splitlines()) + 1]
    return tuple(zip(lines, ends, strict=True))


def loose_examples(path: str, text: str) -> list[str]:
    """The examples in the spec file ``text`` above its first rule's anchor."""
    first = min((start for start, _ in rules(text)), default=len(text.splitlines()) + 1)
    return [f"{path}:{b.line}" for b in blocks(text) if b.info in EXAMPLES and b.line < first]


def bare_rules(path: str, text: str) -> list[str]:
    """The rules in the spec file ``text`` with no example, and no *Tested in*."""
    ids = {a.line: a.id for a in anchors(path, text) if not a.alias_of}
    bare = []
    for start, end in rules(text):
        has_example = any(b.info in EXAMPLES and start < b.line < end for b in blocks(text))
        tested = any("*Tested in*" in words for line, words in prose(text) if start < line < end)
        if not has_example and not tested:
            bare.append(f"{path}:{start}: {ids[start]}")
    return bare


@pytest.mark.parametrize("path", sorted(SPEC))
def test_every_spec_example_belongs_to_a_rule(path: str) -> None:
    loose = loose_examples(path, SPEC[path])
    assert not loose, f"examples above the first rule's anchor: {loose}"


@pytest.mark.parametrize("path", sorted(p for p in SPEC if status(SPEC[p]) == "stable"))
def test_every_stable_rule_has_an_example(path: str) -> None:
    bare = bare_rules(path, SPEC[path])
    assert not bare, f"stable rules with no example (or *Tested in*): {bare}"


def builtin_names(text: str) -> tuple[str, ...]:
    """The names a declaration module's bodiless ``sig``s declare."""
    return tuple(re.findall(r"^\(sig (\S+)", text, re.MULTILINE))


def unexampled(names: tuple[str, ...], spec: dict[str, str]) -> list[str]:
    """The ``names`` no example that runs (``candy run``, or ``candy panic`` for what stops
    the program) in ``spec`` uses."""
    used = {
        word
        for text in spec.values()
        for b in blocks(text)
        if b.info in ("candy run", "candy panic")
        for word in re.findall(r'[^\s()"]+', b.text)
    }
    return [name for name in names if name not in used]


def unindexed(names: tuple[str, ...], text: str) -> list[str]:
    """The ``names`` not in the table of the rule ``library.builtins`` in ``text``."""
    start, end = next(
        (s, e) for s, e in rules(text) if f'<a id="{INDEX}"></a>' in text.splitlines()[s - 1]
    )
    rows = [line for line in text.splitlines()[start:end] if line.startswith("|")]
    listed = {span for row in rows for span in re.findall(r"`([^`]+)`", row)}
    return [name for name in names if name not in listed]


def declared_builtins() -> tuple[str, ...]:
    """The built-ins the language's declaration modules declare, as a program names them:
    ``system``'s by their own names, another module's qualified (``string.len``). The
    declaration modules are those the runtime's spellings name (``include.cdy``,
    ``declaration-modules``); ``translator``'s aren't the language's: ``translator.cdy``'s
    comments specify them."""
    modules = sorted({key.split(".")[0] for key in SPELLINGS if "." in key} - {"translator"})
    lib = ROOT / "src/cdy"
    return builtin_names((lib / "system.cdy").read_text(encoding="utf-8")) + tuple(
        f"{m}.{name}"
        for m in modules
        for name in builtin_names((lib / f"{m}.cdy").read_text(encoding="utf-8"))
    )


def test_every_builtin_is_specified() -> None:
    """Every built-in of the language's declaration modules is in ``library.builtins``'
    index and in an example that runs (``doc/hl_rqmt/library_layers.md``, step 6;
    ``doc/hl_rqmt/stdlib.md``, step 1)."""
    names = declared_builtins()
    assert len(names) > 50
    assert not unindexed(names, SPEC["spec/60-library.md"]), "not in library.builtins' table"
    assert not unexampled(names, SPEC), "in no example that runs"


def test_builtin_checks_catch_a_missing_one() -> None:
    text = (
        f'<a id="{INDEX}"></a>\n| lists | `len` |\n'
        '<a id="a.other"></a>\n| x | `at` |\n'
        "```candy run\n(put (len (List 1)))\n```\n"
    )
    assert unindexed(("len", "at"), text) == ["at"]
    assert unexampled(("len", "at"), {"f.md": text}) == ["at"]


def test_renamed_ids_keep_an_alias() -> None:
    try:
        base = git(ROOT, "merge-base", "HEAD", "refs/heads/master").strip()
        before = tracked_docs(ROOT, base)
    except subprocess.CalledProcessError:
        pytest.skip("no master to compare with")
    gone = sorted(
        {a.id for path, text in before.items() for a in anchors(path, text)} - set(DEFINED)
    )
    for ident in gone:
        warnings.warn(f"id {ident} is gone since master, with no alias left", stacklevel=1)


# --- the scanner itself ---


def test_prose_skips_fences_and_code_spans() -> None:
    text = "a [[x.y]]\n```\n[[in.fence]]\n```\nb `[[in.span]]` c\n"
    assert prose(text) == ((1, "a [[x.y]]"), (5, "b  c"))


def test_anchors_and_their_aliases() -> None:
    text = '<a id="new.id"></a><a id="old.id"></a>\n## Heading\n<a id="other.id"></a>\n'
    assert anchors("f.md", text) == (
        Anchor("new.id", "f.md", 1, ""),
        Anchor("old.id", "f.md", 1, "new.id"),
        Anchor("other.id", "f.md", 3, ""),
    )


def test_links_in_prose_only() -> None:
    text = "see [[match.exhaustive]] and `[[not.this]]`\n```\n[[nor.this]]\n```\n"
    assert links("f.md", text) == (Link("match.exhaustive", "f.md", 1),)


def test_rules_span_to_the_next_anchor() -> None:
    text = '<a id="a.one"></a>\nx\n<a id="a.two"></a>\ny\n'
    assert rules(text) == ((1, 3), (3, 5))


def test_checks_catch_loose_examples_and_bare_rules() -> None:
    text = (
        "```candy run\n(put 1)\n```\n"
        '<a id="a.bare"></a>\n## Bare\nno example\n'
        '<a id="a.tested"></a>\n## Tested\n*Tested in* `tst/`\n'
        '<a id="a.ok"></a>\n## Ok\n```candy errors\n(put x) => unknown\n```\n'
    )
    assert loose_examples("f.md", text) == ["f.md:1"]
    assert bare_rules("f.md", text) == ["f.md:4: a.bare"]
