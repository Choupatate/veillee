"""Tests for FEATURES.md F35: images previewing correctly inside the editor.

Story markdown stores bare filenames ("photo-001.jpg") so the folder stays
readable without the app; rendering.py resolves them at render time. The
browser editor has no such step, so media-links.js converts to a resolvable
URL on the way in and back to a bare filename on the way out. That
conversion is unit-tested under Node (tests/js/media_links_test.mjs); what
is testable here is the contract it depends on — the editor pages ship the
script and the media-URL template it needs — plus the server-side invariant
it exists to protect: what lands in index.md is still a bare filename, and
the reader's HTML still resolves it.
"""

from datetime import date

from app import people, storage
from app.rendering import render_markdown


# --- what the editor pages must hand the script ------------------------------


def test_story_editor_ships_media_links_and_its_url_template(auth_client):
    html = auth_client.get("/new").data.decode()
    assert "js/media-links.js" in html
    assert 'data-media-url-template="/story/__ID__/media/__FILENAME__"' in html


def test_person_editor_ships_media_links_and_its_url_template(auth_client):
    html = auth_client.get("/new-person").data.decode()
    assert "js/media-links.js" in html
    assert 'data-media-url-template="/people/__ID__/media/__FILENAME__"' in html


def test_media_links_loads_before_the_editor_that_uses_it(auth_client):
    """editor.js reads window.MediaLinks at call time, but ordering the
    tags correctly is free insurance and keeps the no-build-step rule
    (no module loader to resolve this for us)."""
    html = auth_client.get("/new").data.decode()
    assert html.index("js/media-links.js") < html.index("js/editor.js")


def test_media_url_template_matches_the_route_that_serves_media(auth_client, stories_dir, jpeg_bytes):
    """The template the editor fills in must be the URL that actually
    serves the file, or the preview is broken in a new way."""
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "body")
    resp = auth_client.post(
        f"/api/stories/{story_id}/images",
        data={"file": (jpeg_bytes(color="blue"), "photo.jpg")},
        content_type="multipart/form-data",
    )
    filename = resp.get_json()["filename"]
    html = auth_client.get(f"/edit/{story_id}").data.decode()
    template = html.split('data-media-url-template="')[1].split('"')[0]
    url = template.replace("__ID__", story_id).replace("__FILENAME__", filename)
    assert auth_client.get(url).status_code == 200


# --- the invariant the conversion protects -----------------------------------


def test_saved_story_body_keeps_bare_filenames(auth_client, stories_dir):
    """Whatever the editor shows itself, index.md must stay portable."""
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "")
    auth_client.put(
        f"/api/stories/{story_id}",
        json={
            "title": "A day out",
            "date": "2026-03-01",
            "markdown": "![Her first snow](photo-001.jpg)",
        },
    )
    raw = (stories_dir / story_id / "index.md").read_text()
    assert "![Her first snow](photo-001.jpg)" in raw
    assert f"/story/{story_id}/media" not in raw


def test_a_full_media_url_in_the_body_still_renders(auth_client, stories_dir):
    """Belt and braces: if an absolute media URL ever does reach index.md
    (hand-edited, an older draft), the reader's page must still show the
    photo rather than a broken image."""
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "")
    body = f"![](/story/{story_id}/media/photo-001.jpg)"
    html = render_markdown(body, f"/story/{story_id}/media")
    assert f'src="/story/{story_id}/media/photo-001.jpg"' in html
    assert "/media//story/" not in html


def test_person_body_images_resolve_against_the_person_media_route(people_dir):
    slug = people.create_person(people_dir, "Mamie Rose", body="![](photo-001.jpg)")
    p = people.get_person(people_dir, slug)
    html = render_markdown(p.body, f"/people/{slug}/media")
    assert f'src="/people/{slug}/media/photo-001.jpg"' in html
