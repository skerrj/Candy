"""A Claude Code session's chat, as Markdown, for ``doc/archive/chat_<topic>.md``.

A session's transcript (``~/.claude/projects/<project>/<session>.jsonl``) has one JSON entry
per event: the owner's messages, Claude's text, its thinking, its tool calls and their
results, and the system's attachments. Each entry records the git branch it was on, so one
branch's chat is the entries on it (``--branch``), optionally between two times (``--since``,
``--until``, ISO timestamps, as the transcript's are).

The archive keeps the owner's messages and Claude's text verbatim (``doc/process.md``,
"Where notes go"), the owner's as quotes; a tool call becomes a one-line marker
(``*ran: Run the full test suite*``), and where the context was summarised, a marker says so.
Thinking, tool results, attachments and the system's reminders are left out. ``--note`` is a
file whose text goes first: when, where and what came of it::

    python script/chat_archive.py SESSION.jsonl --branch typed-core --title "typed-core" \\
        --note NOTE.md -o doc/archive/chat_typed-core.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL)
HOME = str(Path.home())
# A command's set-up steps, left out of its marker: changing directory, the environment.
SETUP = ("cd ", "source ", "conda activate")
SETUP_SPLIT = re.compile(r"\s*(?:&&|;)\s*")


class Turn(NamedTuple):
    """One turn: who spoke ("owner", "claude" or "summary") and the text."""

    who: str
    text: str


def wanted(entry: dict[str, object], branch: str, since: str, until: str) -> bool:
    """Whether ``entry`` is on ``branch``, between ``since`` and ``until`` (empty: no bound)."""
    stamp = str(entry.get("timestamp", ""))
    return (
        entry.get("gitBranch") == branch
        and not entry.get("isSidechain")
        and (since == "" or stamp >= since)
        and (until == "" or stamp < until)
    )


def short_path(path: str, root: str) -> str:
    """``path`` relative to the repo ``root``, or with ``~`` for the home directory."""
    if path.startswith(root + "/"):
        return path[len(root) + 1 :]
    return path.replace(HOME, "~", 1) if path.startswith(HOME) else path


def tool_marker(block: dict[str, object], root: str) -> str:
    """A one-line marker for a tool call."""
    name = str(block.get("name", "a tool"))
    raw = block.get("input")
    args: dict[str, object] = raw if isinstance(raw, dict) else {}
    path = short_path(str(args.get("file_path", "")), root)
    if name == "Bash":
        if args.get("description"):
            return f"*ran: {args['description']}*"
        line = str(args.get("command", "")).strip().split("\n", maxsplit=1)[0]
        steps = [s.strip() for s in SETUP_SPLIT.split(line)]
        command = " && ".join(s for s in steps if s and not s.startswith(SETUP)) or line
        command = command.replace(root + "/", "").replace(root, ".").replace(HOME, "~")
        return f"*ran: `{command[:80].replace('`', chr(39))}`*"
    if name == "Read":
        return f"*read: `{path}`*"
    if name in ("Edit", "Write"):
        return f"*{'edited' if name == 'Edit' else 'wrote'}: `{path}`*"
    return f"*used {name}*"


def entry_parts(entry: dict[str, object], root: str) -> list[Turn]:
    """The turns in one entry: the owner's text, Claude's text and tool markers, or none."""
    message = entry.get("message")
    if not isinstance(message, dict) or entry.get("isMeta"):
        return []
    content = message.get("content")
    kind = entry.get("type")
    if kind == "user" and entry.get("isCompactSummary"):
        return [Turn("summary", "")]
    if kind == "user" and isinstance(content, str):
        text = REMINDER.sub("", content).strip()
        return [Turn("owner", text)] if text else []
    if kind != "assistant" or not isinstance(content, list):
        return []
    parts: list[Turn] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "text" and str(block.get("text", "")).strip():
            parts.append(Turn("claude", str(block["text"]).strip()))
        elif block.get("type") == "tool_use":
            parts.append(Turn("claude", tool_marker(block, root)))
    return parts


def turns(path: Path, branch: str, since: str, until: str, root: str) -> list[Turn]:
    """The session's turns on ``branch``, consecutive parts by one speaker joined."""
    out: list[Turn] = []
    with path.open(encoding="utf-8") as lines:
        for line in lines:
            entry = json.loads(line)
            if not isinstance(entry, dict) or not wanted(entry, branch, since, until):
                continue
            for part in entry_parts(entry, root):
                if out and out[-1].who == part.who == "claude":
                    out[-1] = Turn("claude", out[-1].text + "\n\n" + part.text)
                else:
                    out.append(part)
    return out


def quoted(text: str) -> str:
    """``text`` as a Markdown block quote."""
    return "\n".join(("> " + line) if line else ">" for line in text.split("\n"))


def markdown(title: str, note: str, chat: list[Turn]) -> str:
    """The archive: the note, the title, and each turn under its speaker."""
    out = [note.strip(), "", f"# {title}", ""]
    for turn in chat:
        if turn.who == "summary":
            out += ["*(The context was summarised here; the turns before it are above.)*", ""]
        elif turn.who == "owner":
            out += ["## Owner", "", quoted(turn.text), ""]
        else:
            out += ["## Claude Code", "", turn.text, ""]
    return "\n".join(out).rstrip("\n") + "\n"


def main(argv: list[str]) -> int:
    """Write the archive; 1 if the branch has no turns in the range."""
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", maxsplit=1)[0])
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--since", default="")
    parser.add_argument("--until", default="")
    parser.add_argument("--title", required=True)
    parser.add_argument("--note", type=Path, required=True)
    parser.add_argument("-o", "--out", type=Path, required=True)
    args = parser.parse_args(argv)
    root = str(Path(__file__).resolve().parent.parent)
    chat = turns(args.transcript, args.branch, args.since, args.until, root)
    if not chat:
        print(f"no turns on {args.branch} in that range", file=sys.stderr)
        return 1
    note = args.note.read_text(encoding="utf-8")
    args.out.write_text(markdown(args.title, note, chat), encoding="utf-8")
    owners = sum(1 for t in chat if t.who == "owner")
    print(f"wrote {args.out}: {owners} owner turns, {len(chat)} in all")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
