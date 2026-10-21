"""The bootstrap chain: Candy built from the Python translator at ``self-host-py`` up to
today's ``bin``, through the history (``doc/hl_rqmt/bootstrap.md``).

A step is ``self-host-py`` or a later commit that changes ``bin``: any file in a target's
directory, ``bin/<target>/`` (the translator, or a library copy next to it, which the
translator reads as it runs); ``bin/README.md`` alone doesn't count. Each step is run in a
scratch worktree under ``tmp/bootstrap/``: the step's ``bin`` translator is replaced by the
one before it (except at the first step, which uses the Python translator), the step's own
``src/py_cdy/self_host.py`` rebuilds ``bin`` with it, against the step's own runtime, and
the result must equal the step's checked-in ``bin``, byte for byte.

    python script/bootstrap.py --list           the steps, with their feature tags and staging
    python script/bootstrap.py --step C         one step, from its parent step's checked-in bin
    python script/bootstrap.py --check          every step that way (each on its own)
    python script/bootstrap.py --from-scratch   the true chain, each output into the next
    python script/bootstrap.py --tag            tag the steps boot/00, boot/01, ...

The steps are the ``boot/NN`` tags, then the commits after them found with ``git log``
(not tagged yet). A step that needed staging says how in its tag's message, on a line
``staging: KIND ARGS`` (``STAGING`` holds the lines until the tags exist). Each kind builds
a bridge: the translator before translates the step's translator source, and the step's
``self_host.py`` starts from the result.

- ``joined FILE...``: the step's files (``src/cdy/FILE.cdy``) joined into one text,
  without their ``(import ...)`` lines, through ``translate_text``. For the step that added
  ``import`` (and ``translate_file``), which the translator before can't read.
- ``old-runtime``: ``src/cdy/cdyc.cdy`` through ``translate_file``, with the runtime of the
  step's parent commit. For a step that removes a table entry the translator before still
  needs (``cond``, when it became a macro), since a translator reads the live table.
"""

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import NamedTuple, cast

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tmp" / "bootstrap"
FIRST = "self-host-py"
# What "a commit that changes bin" means: any file in a target's directory under bin/.
BIN_FILES = ":(glob)bin/*/**"
TRANSLATOR = Path("bin") / "py" / "cdy_translator.py"
PYTHON = f"python {sys.version_info.major}.{sys.version_info.minor}"
# Deep enough for the translator's recursion (only self tail calls loop).
RECURSION_LIMIT = 20_000

# Staging found by running the chain, by commit, until the boot/NN tags record it.
STAGING = {
    "84bf89a5ef63d5ac4dfe4b7a08438a21e935345e": "joined form read include core lower emit cdyc",
    "a0499db578e82a82e7a929d2cc20c283e6a27875": "old-runtime",
}


class Step(NamedTuple):
    """One step of the chain: its commit and a label (its tag, or a short commit)."""

    commit: str
    label: str


class StepFailed(Exception):
    """A step didn't rebuild its checked-in ``bin``."""


def git(*args: str, cwd: Path = ROOT) -> str:
    """The output of ``git args``, stripped."""
    done = subprocess.run(("git", *args), cwd=cwd, check=True, capture_output=True, text=True)
    return done.stdout.strip()


def found_steps(head: str = "HEAD") -> tuple[Step, ...]:
    """The steps from the history: ``self-host-py``, then each commit after it that changes
    ``bin`` (``BIN_FILES``), oldest first."""
    later = git("rev-list", "--reverse", f"refs/tags/{FIRST}..{head}", "--", BIN_FILES).split()
    first = git("rev-parse", f"refs/tags/{FIRST}^{{commit}}")
    return (Step(first, FIRST), *(Step(commit, commit[:7]) for commit in later))


def tagged_steps() -> tuple[Step, ...]:
    """The steps from the ``boot/NN`` tags, in order (empty before they exist)."""
    names = git("tag", "--list", "boot/*", "--sort=refname").split()
    return tuple(Step(git("rev-parse", f"refs/tags/{name}^{{commit}}"), name) for name in names)


def steps() -> tuple[Step, ...]:
    """The chain: the ``boot/NN`` tags, then the history's steps after them that aren't
    tagged yet (all of them, before there are tags)."""
    tagged = tagged_steps()
    return (*tagged, *found_steps()[len(tagged) :])


def staging_of(step: Step) -> tuple[str, ...]:
    """The step's staging, split into words (empty if it needs none)."""
    if not step.label.startswith("boot/"):
        return tuple(STAGING.get(step.commit, "").split())
    message = git("tag", "--list", "--format=%(contents)", step.label)
    for line in message.splitlines():
        if line.startswith("staging:"):
            words = tuple(line.removeprefix("staging:").split())
            return () if words == ("none",) else words
    return ()


def feature_of(step: Step) -> str:
    """The first feature tag (a branch's merge into ``master``) that holds the step, or
    ``-`` if none does yet."""
    names = git("tag", "--contains", step.commit, "--sort=creatordate").split()
    features = [name for name in names if not name.startswith(("boot/", "archive/"))]
    return features[0] if features else "-"


def translator_at(commit: str) -> bytes:
    """The checked-in translator at ``commit``."""
    done = subprocess.run(
        ("git", "show", f"{commit}:{TRANSLATOR}"), cwd=ROOT, check=True, capture_output=True
    )
    return done.stdout


def run_python(tree: Path, pythonpath: Path, *args: str) -> None:
    """Run ``python args`` in ``tree`` with ``pythonpath`` (whose ``cdy_rt`` is the
    runtime) first on the path; raises ``StepFailed`` if it fails."""
    env = {**os.environ, "PYTHONPATH": str(pythonpath)}
    done = subprocess.run(
        (sys.executable, *args), cwd=tree, env=env, capture_output=True, text=True, check=False
    )
    if done.returncode != 0:
        raise StepFailed(f"{' '.join(args)} failed:\n{done.stderr[-2000:]}")


def stage(step: Step, tree: Path) -> None:
    """Build the step's bridge in ``tree``, if its staging asks for one."""
    staging = staging_of(step)
    if not staging:
        return
    kind = staging[0]
    if kind == "joined":
        run_python(tree, tree / "src", str(Path(__file__)), "--bridge", *staging)
    elif kind == "old-runtime":
        parent = WORK / f"{step.commit[:12]}-parent"
        shutil.rmtree(parent, ignore_errors=True)
        parent.mkdir(parents=True)
        archive = subprocess.run(
            ("git", "archive", f"{step.commit}^", "src/cdy_rt"),
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        subprocess.run(("tar", "-x", "-C", str(parent)), input=archive.stdout, check=True)
        run_python(tree, parent / "src", str(Path(__file__)), "--bridge", *staging)
    else:
        raise StepFailed(f"unknown staging {kind!r}")


def load_translator() -> ModuleType:
    """The translator in the current directory's ``bin``, loaded."""
    spec = importlib.util.spec_from_file_location("before", TRANSLATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bridge(staging: tuple[str, ...]) -> None:
    """Replace the translator in the current directory's ``bin`` by its translation of the
    translator source there, as ``staging`` says (run by ``stage``, in a step's tree)."""
    sys.setrecursionlimit(RECURSION_LIMIT)
    before = load_translator()
    if staging[0] == "joined":
        text = "\n".join(
            re.sub(
                r"^\(import [^)]*\)\s*$",
                "",
                (Path("src/cdy") / f"{name}.cdy").read_text(),
                flags=re.MULTILINE,
            )
            for name in staging[1:]
        )
        built = cast(str, before.translate_text(text))
    else:
        built = cast(str, before.translate_file("src/cdy/cdyc.cdy"))
    TRANSLATOR.write_text(built)


def run_step(step: Step, before: bytes | None) -> bytes:
    """Rebuild ``bin`` at ``step`` from the translator ``before`` (``None``: the step's own
    Python translator). Returns the new translator; raises ``StepFailed`` if it can't, or
    if it differs from the checked-in one."""
    tree = WORK / step.commit[:12]
    if tree.exists():
        git("worktree", "remove", "--force", str(tree))
    git("worktree", "add", "--detach", str(tree), step.commit)
    try:
        if before is not None:
            (tree / TRANSLATOR).write_bytes(before)
            stage(step, tree)
        run_python(tree, tree / "src", "src/py_cdy/self_host.py")
        built = (tree / TRANSLATOR).read_bytes()
        if built != translator_at(step.commit):
            raise StepFailed("bin differs from the checked-in one")
        return built
    finally:
        git("worktree", "remove", "--force", str(tree))


def check_step(chain: tuple[Step, ...], index: int) -> bool:
    """Run step ``index`` from its parent step's checked-in translator, and report."""
    before = None if index == 0 else translator_at(chain[index - 1].commit)
    try:
        run_step(chain[index], before)
    except StepFailed as err:
        print(f"FAIL {index:02} {chain[index].label}: {err}", flush=True)
        return False
    print(f"ok {index:02} {chain[index].label}", flush=True)
    return True


def from_scratch(chain: tuple[Step, ...]) -> bool:
    """The true chain: each step's output is the next step's translator."""
    before: bytes | None = None
    for index, step in enumerate(chain):
        try:
            before = run_step(step, before)
        except StepFailed as err:
            print(f"FAIL {index:02} {step.label}: {err}", flush=True)
            return False
        print(f"ok {index:02} {step.label}", flush=True)
    return True


def step_index(chain: tuple[Step, ...], name: str) -> int:
    """The index of the step that ``name`` (a commit or tag) names."""
    commit = git("rev-parse", f"{name}^{{commit}}")
    for index, step in enumerate(chain):
        if step.commit == commit:
            return index
    raise SystemExit(f"{name} is not a step of the chain")


def tag_steps() -> None:
    """Tag each step found in the history that has no ``boot/NN`` tag yet, numbering on
    from the tags there are."""
    tagged = {step.commit for step in tagged_steps()}
    number = len(tagged)
    for step in found_steps():
        if step.commit in tagged:
            continue
        staging = " ".join(staging_of(step)) or "none"
        name = f"boot/{number:02}"
        git("tag", "-a", name, step.commit, "-m", f"{name}: {PYTHON}\nstaging: {staging}")
        print(f"tagged {name} {step.commit[:7]} (staging: {staging})")
        number += 1


def main() -> None:
    """The command line."""
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", maxsplit=1)[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true")
    mode.add_argument("--step", metavar="COMMIT")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--from-scratch", action="store_true")
    mode.add_argument("--tag", action="store_true")
    mode.add_argument("--bridge", nargs="+", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.bridge:
        bridge(tuple(args.bridge))
        return
    if args.tag:
        tag_steps()
        return
    chain = steps()
    if args.list:
        for index, step in enumerate(chain):
            staging = " ".join(staging_of(step))
            print(f"{index:02} {step.label:12} {step.commit[:7]} {feature_of(step):18} {staging}")
        return
    WORK.mkdir(parents=True, exist_ok=True)
    if args.step:
        passed = check_step(chain, step_index(chain, args.step))
    elif args.check:
        results = tuple(check_step(chain, index) for index in range(len(chain)))  # all of them
        passed = all(results)
    else:
        passed = from_scratch(chain)
    shutil.rmtree(WORK, ignore_errors=True)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
