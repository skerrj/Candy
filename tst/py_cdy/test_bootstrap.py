"""Tests for the bootstrap chain (``script/bootstrap.py``, ``doc/hl_rqmt/bootstrap.md``)."""

import subprocess
import sys
import warnings
from pathlib import Path

import pytest

import bootstrap
from self_host import LIBRARY, TRANSLATOR, copy_library


def test_steps_start_at_self_host_py() -> None:
    steps = bootstrap.found_steps()
    assert steps[0].label == bootstrap.FIRST
    assert len(steps) > 1


def test_staging_names_steps() -> None:
    found = {step.commit for step in bootstrap.found_steps()}
    assert set(bootstrap.STAGING) <= found
    for staging in bootstrap.STAGING.values():
        assert staging.split()[0] in ("joined", "old-runtime", "old-library")


def test_tags_cover_the_steps() -> None:
    tagged = bootstrap.tagged_steps()
    if not tagged:
        pytest.skip("no boot/NN tags yet")
    found = bootstrap.found_steps()
    assert [step.label for step in tagged] == [f"boot/{n:02}" for n in range(len(tagged))]
    assert [step.commit for step in tagged] == [step.commit for step in found[: len(tagged)]]
    # Only the newest step may be untagged (it is tagged after it is committed).
    assert len(found) - len(tagged) <= 1
    for step in tagged:
        staging = " ".join(bootstrap.staging_of(step))
        assert staging == bootstrap.STAGING.get(step.commit, "")


def test_newest_step_reads_the_library(tmp_path: Path) -> None:
    """The newest step's translator, next to today's library (``src/cdy``), builds the
    translator, as the next step's check will (``bootstrap.run_step``): a library it can't
    read is found before the commit. If only its own library works, the next step needs
    ``old-library`` staging (a warning); if neither does, it needs two steps."""
    tagged = bootstrap.tagged_steps()
    if not tagged:
        pytest.skip("no boot/NN tags yet")
    newest = tagged[-1].commit
    translator = tmp_path / "cdy_translator.py"
    translator.write_bytes(bootstrap.translator_at(newest))
    copy_library(tmp_path)
    if build(translator, tmp_path).returncode == 0:
        return
    for name in LIBRARY:
        (tmp_path / name).write_text(bootstrap.git("show", f"{newest}:bin/py/{name}"))
    done = build(translator, tmp_path)
    assert done.returncode == 0, (
        f"{tagged[-1].label} reads neither today's library nor its own: two steps are needed\n"
        + done.stderr
    )
    warnings.warn(
        f"{tagged[-1].label} can't read today's library: the next boot step needs staging "
        "old-library (script/bootstrap.py, STAGING)",
        stacklevel=1,
    )


def build(translator: Path, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """``translator`` run on the translator's source, into ``tmp_path``."""
    return subprocess.run(
        (sys.executable, str(translator), str(TRANSLATOR), str(tmp_path / "built.py")),
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.bootstrap
def test_every_step_rebuilds_its_bin() -> None:
    done = subprocess.run(
        (sys.executable, str(bootstrap.ROOT / "script" / "bootstrap.py"), "--check"),
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 0, done.stdout + done.stderr
