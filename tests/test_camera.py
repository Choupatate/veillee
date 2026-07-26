"""Tests for FEATURES.md F34: taking a photo in the app.

The capture itself (getUserMedia, the freeze-frame canvas, retake/flip)
lives in camera.js and is exercised by hand in a real browser; its pure
frame math is unit-tested under Node (tests/js/camera_logic_test.mjs).
What is testable here is the server-rendered contract those scripts hang
off: the camera scripts are loaded exactly where a photo can be added,
every "Take a photo" button ships hidden (JS unhides it only where
getUserMedia exists), and a captured JPEG uploads through the same image
endpoint a chosen file does.
"""

from datetime import date
from io import BytesIO

from werkzeug.datastructures import FileStorage

from app import storage

CAMERA_SCRIPTS = ("js/camera-logic.js", "js/camera.js")


# --- the pages that can take a photo -----------------------------------------


def test_instant_page_loads_camera_scripts_and_hidden_button(auth_client):
    html = auth_client.get("/new-instant").data.decode()
    for script in CAMERA_SCRIPTS:
        assert script in html
    assert 'id="instant-camera"' in html
    assert "hidden" in html.split('id="instant-camera"')[1].split(">")[0]


def test_instant_photo_input_is_not_required_so_a_capture_can_stand_alone(auth_client):
    """A camera photo never reaches the file input, so a `required` on it
    would have the browser block a save that does have a photo."""
    html = auth_client.get("/new-instant").data.decode()
    photo_input = html.split('id="instant-photo"')[1].split(">")[0]
    assert "required" not in photo_input


def test_story_editor_loads_camera_scripts_and_hidden_section(auth_client):
    html = auth_client.get("/new").data.decode()
    for script in CAMERA_SCRIPTS:
        assert script in html
    assert 'id="editor-camera"' in html
    assert 'id="camera-btn"' in html
    assert "hidden" in html.split('id="editor-camera"')[1].split(">")[0]


def test_editing_an_existing_story_also_offers_the_camera(auth_client, stories_dir):
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "body")
    html = auth_client.get(f"/edit/{story_id}").data.decode()
    assert 'id="camera-btn"' in html


def test_person_editor_loads_camera_scripts_and_hidden_button(auth_client):
    html = auth_client.get("/new-person").data.decode()
    for script in CAMERA_SCRIPTS:
        assert script in html
    assert 'id="editor-photo-camera"' in html
    assert "hidden" in html.split('id="editor-photo-camera"')[1].split(">")[0]


def test_reading_pages_do_not_load_the_camera(auth_client, stories_dir):
    """Nothing on a reading page can add a photo, so nothing there should
    ask the browser for a camera script."""
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "body")
    for path in ("/", f"/story/{story_id}", "/book"):
        html = auth_client.get(path).data.decode()
        for script in CAMERA_SCRIPTS:
            assert script not in html, path


# --- a captured photo is just an upload --------------------------------------


def test_captured_jpeg_uploads_through_the_image_endpoint(auth_client, stories_dir, jpeg_bytes):
    """camera.js hands callers a File named camera-<timestamp>.jpg; the
    endpoint re-encodes it into the story folder like any other photo."""
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "body")
    resp = auth_client.post(
        f"/api/stories/{story_id}/images",
        data={"file": (jpeg_bytes(color="blue", size=(300, 200)), "camera-20260704-090503.jpg")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    filename = resp.get_json()["filename"]
    assert filename == "photo-001.jpg"
    assert (stories_dir / story_id / filename).exists()


def test_captured_photo_can_become_an_instant_cover(auth_client, stories_dir, jpeg_bytes):
    """The instant save path: create, upload the capture, set it as cover."""
    story_id = storage.create_story(
        stories_dir, "First snow", date(2026, 3, 1), "First snow", kind="instant"
    )
    filename = storage.save_image(
        stories_dir,
        story_id,
        FileStorage(
            stream=BytesIO(jpeg_bytes(color="white", size=(200, 200)).read()),
            filename="camera-20260704-090503.jpg",
        ),
    )
    resp = auth_client.put(
        f"/api/stories/{story_id}",
        json={
            "title": "First snow",
            "date": "2026-03-01",
            "markdown": "First snow",
            "cover": filename,
        },
    )
    assert resp.status_code == 200
    story = storage.get_story(stories_dir, story_id)
    assert story.cover == filename
    assert story.kind == "instant"
