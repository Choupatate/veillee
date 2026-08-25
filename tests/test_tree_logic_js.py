"""Runs the plain-Node unit tests for the /tree view-scope logic
(app/static/js/tree-logic.js), the "Everyone" DAG graph layout
(app/static/js/tree-graph-logic.js), the shared localStorage wrapper
(app/static/js/safe-storage.js), the shared fetch/JSON response
helper (app/static/js/fetch-json.js), the in-app camera's frame math
(app/static/js/camera-logic.js), the photo cropper's pan/zoom geometry
(app/static/js/crop-logic.js), the crash-recovery decision behind its
autosave (app/static/js/draft-logic.js), the editor's image-link conversion
(app/static/js/media-links.js), and the voice recorder's clock and
interruption policy (app/static/js/recorder-logic.js), the screen wake
lock it holds (app/static/js/wake-lock.js), the theme menu's scheme
cycle and press rules (app/static/js/theme-logic.js), and the theme
editor's preview colour maths (app/static/js/palette-logic.js) as part of
the bare `pytest` run.
Skipped, not failed, when node isn't on PATH — the app has no Node
dependency and never should; this just piggybacks on it being present
in CI."""
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
NODE = shutil.which("node")


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_tree_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/tree_logic_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_html_pattern_attributes_compile_in_a_browser():
    """Not pure-function logic like the rest of this file — a guard that
    needs a JS regex engine, because HTML's `pattern` is compiled with the
    `v` flag and Python's `re` cannot tell you what that rejects."""
    result = subprocess.run(
        [NODE, "tests/js/html_patterns_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_share_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/share_link_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_tree_graph_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/tree_graph_logic_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_safe_storage_wrapper():
    result = subprocess.run(
        [NODE, "tests/js/safe_storage_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_fetch_json_wrapper():
    result = subprocess.run(
        [NODE, "tests/js/fetch_json_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_camera_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/camera_logic_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_media_links_conversion():
    result = subprocess.run(
        [NODE, "tests/js/media_links_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_recorder_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/recorder_logic_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_wake_lock():
    result = subprocess.run(
        [NODE, "tests/js/wake_lock_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_theme_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/theme_logic_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_palette_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/palette_logic_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_crop_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/crop_logic_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_draft_logic_pure_functions():
    result = subprocess.run(
        [NODE, "tests/js/draft_logic_test.mjs"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
