"""Tests for FEATURES.md F47: a voice recording surviving a locked screen.

The recording itself is `MediaRecorder` in editor.js and can only be
exercised by hand on a real phone; its two pieces of decidable logic are
unit-tested under Node (tests/js/recorder_logic_test.mjs and
wake_lock_test.mjs). What is checked here is everything a screen lock
would otherwise silently break: that the scripts holding the screen awake
are actually served on the pages that record, that editor.js still asks
for the lock and still treats leaving the page as the end of a recording,
and — the one that would fail quietly in production — that every sentence
the recorder can say about an interruption exists in the translation
tables, in both languages.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from app.i18n import JS_STRINGS
from app.translations_fr import TRANSLATIONS_FR

REPO_ROOT = Path(__file__).resolve().parent.parent
EDITOR_JS = (REPO_ROOT / "app" / "static" / "js" / "editor.js").read_text()
NODE = shutil.which("node")

RECORDING_SCRIPTS = ("js/recorder-logic.js", "js/wake-lock.js")


# --- the pages that can record ------------------------------------------------


def test_story_editor_loads_the_recording_scripts(auth_client):
    html = auth_client.get("/new").data.decode()
    for script in RECORDING_SCRIPTS:
        assert script in html


def test_the_scripts_load_before_the_editor_that_uses_them(auth_client):
    """No bundler and no module loader: order in the page is the whole
    dependency mechanism, and editor.js calls RecorderLogic on the way in."""
    html = auth_client.get("/new").data.decode()
    editor_at = html.index("js/editor.js")
    for script in RECORDING_SCRIPTS:
        assert html.index(script) < editor_at


def test_an_existing_story_can_record_too(auth_client, stories_dir):
    from datetime import date

    from app import storage

    story_id = storage.create_story(stories_dir, "A story", date(2026, 1, 1), "Body")
    html = auth_client.get(f"/edit/{story_id}").data.decode()
    for script in RECORDING_SCRIPTS:
        assert script in html


# --- what editor.js does with them --------------------------------------------


def test_starting_a_recording_asks_for_the_wake_lock():
    assert "StorybookWakeLock.request()" in EDITOR_JS


def test_the_wake_lock_is_let_go_with_the_microphone():
    """Released where the stream is, so no path can stop recording and
    leave a phone burning its battery with the screen on."""
    release_block = EDITOR_JS.split("function releaseStream()")[1].split("\n    }")[0]
    assert "StorybookWakeLock.release()" in release_block


def test_a_backgrounded_page_ends_the_recording_instead_of_losing_it():
    assert 'document.visibilityState === "hidden"' in EDITOR_JS
    assert 'interrupt("hidden")' in EDITOR_JS


def test_every_interruption_the_browser_reports_is_handled():
    for reason in ("hidden", "ended", "muted", "error"):
        assert f'interrupt("{reason}")' in EDITOR_JS


def test_coming_back_to_the_page_retries_an_upload_the_freeze_cut_off():
    visible_branch = EDITOR_JS.split('document.visibilityState === "hidden"')[1]
    assert "drainUploads()" in visible_branch.split("});")[0]


def test_closing_the_page_over_an_unsaved_recording_is_warned_about():
    """The browser's own warning is the last line between a recording that
    only exists in the tab and a tab that is about to stop existing."""
    guard = EDITOR_JS.split('addEventListener("beforeunload"')[1]
    assert "audioAtRisk" in guard.split("});")[0]


def test_a_failed_upload_stays_queued_rather_than_being_dropped():
    """The queue is what makes a retry possible at all; a single slot would
    lose the interrupted recording as soon as the next one started."""
    failure = EDITOR_JS.split("function drainUploads()")[1]
    # The head of the queue is shifted off on success only.
    assert failure.index("uploadQueue.shift()") < failure.index(".catch(")


# --- the level meter and the microphone watchdog ------------------------------


def test_the_editor_shows_a_level_while_recording(auth_client):
    """The failure this feature exists for is a microphone that goes dead
    without stopping the recording — invisible on a page that only shows a
    running clock."""
    html = auth_client.get("/new").data.decode()
    assert 'id="voice-meter"' in html
    assert 'id="voice-meter-fill"' in html
    meter = html.split('id="voice-meter"')[1].split(">")[0]
    assert "hidden" in meter
    # Decorative: the bar duplicates nothing a screen reader needs, and the
    # watchdog says the same thing in words when it matters.
    assert "aria-hidden" in meter


def test_the_meter_starts_with_the_recording_and_stops_with_the_stream():
    assert "startMeter(stream)" in EDITOR_JS
    release_block = EDITOR_JS.split("function releaseStream()")[1].split("\n    }")[0]
    assert "stopMeter()" in release_block


def test_silence_long_enough_to_mean_a_dead_microphone_ends_the_recording():
    meter_block = EDITOR_JS.split("function startMeter(")[1].split("function rms(")[0]
    assert "watchSilence" in meter_block
    assert 'interrupt("muted")' in meter_block


def test_a_paused_recording_is_not_mistaken_for_a_dead_microphone():
    """Nothing is being kept while paused, so a silent pause must not be
    read as the microphone having gone."""
    meter_block = EDITOR_JS.split("function startMeter(")[1].split("function rms(")[0]
    guard = meter_block.split('mediaRecorder.state !== "recording"')[1].split("});")[0]
    assert "createSilenceWatch()" in guard


def test_the_watchdog_stands_down_without_float_precision():
    """8-bit time-domain data quantises a quiet room's noise floor to zero,
    which would make the watchdog stop a perfectly good recording."""
    meter_block = EDITOR_JS.split("function startMeter(")[1].split("function rms(")[0]
    assert "getFloatTimeDomainData" in meter_block
    assert "if (!samples) return;" in meter_block


def test_the_meter_is_dressed_by_the_theme_not_by_a_hardcoded_colour():
    css = (REPO_ROOT / "app" / "static" / "css" / "main.css").read_text()
    block = css.split(".editor__voice-meter-fill {")[1].split("}")[0]
    assert "var(--color-accent)" in block


# --- the messages -------------------------------------------------------------


def _interruption_messages():
    """Ask recorder-logic.js itself, so the list can never drift from the
    one the browser will actually show."""
    result = subprocess.run(
        [
            NODE,
            "-e",
            "console.log(JSON.stringify("
            "require('./app/static/js/recorder-logic.js').interruptionMessages()))",
        ],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_the_recorder_can_only_say_things_the_page_knows_how_to_translate():
    messages = _interruption_messages()
    assert len(messages) == 4
    for message in messages:
        assert message in JS_STRINGS


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_the_interruption_messages_are_translated():
    for message in _interruption_messages():
        assert message in TRANSLATIONS_FR
        assert TRANSLATIONS_FR[message] != message


def test_the_offline_message_is_translated():
    """Not one of recorder-logic's own — editor.js says this one when the
    upload never reached the server, which is the likeliest outcome of a
    recording salvaged behind a locked screen."""
    offline = (
        "Could not reach the server. The recording is still here — keep this "
        "page open and it will try again."
    )
    assert offline in EDITOR_JS
    assert offline in JS_STRINGS
    assert offline in TRANSLATIONS_FR


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_every_message_reaches_the_page_in_french(auth_client_factory):
    """The strings are shipped to the browser as a JSON blob, and a message
    absent from it would fall back to English mid-sentence."""
    client = auth_client_factory(DEFAULT_LANGUAGE="fr")
    blob = json.loads(
        client.get("/new").data.decode().split('id="storybook-i18n-data">')[1].split("</script>")[0]
    )
    for message in _interruption_messages():
        assert blob[message] == TRANSLATIONS_FR[message]
