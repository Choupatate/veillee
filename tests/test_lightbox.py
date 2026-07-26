"""Tests for FEATURES.md F7: tap-to-zoom lightbox.

The interaction itself (click-to-open, Escape, back-gesture, focus
management) lives entirely in story.js and is exercised manually with a
headless browser; these tests cover the server-rendered contract the script
depends on: cover/figure images are present and story.js is loaded only on
the story page (see also test_reading_order.test_story_js_only_loaded_on_story_page).
"""

from datetime import date

from app import storage


def test_story_page_cover_and_figure_images_present_for_lightbox(auth_client, stories_dir, jpeg_bytes):
    from werkzeug.datastructures import FileStorage

    story_id = storage.create_story(
        stories_dir, "Photo story", date(2026, 1, 1),
        "Some text.\n\n![A caption](photo-001.jpg)",
    )
    buf = jpeg_bytes(color="red", size=(200, 200))
    filename = storage.save_image(stories_dir, story_id, FileStorage(stream=buf, filename="c.jpg"))
    story = storage.get_story(stories_dir, story_id)
    storage.save_story(stories_dir, story_id, story.title, story.date, story.body, cover=filename)

    resp = auth_client.get(f"/story/{story_id}")
    html = resp.data.decode()
    assert 'class="story__cover"' in html
    assert "story__body" in html
    assert "<figure>" in html
    assert "<figcaption>A caption</figcaption>" in html


def test_an_inline_image_is_also_reachable_by_the_lightbox(auth_client, stories_dir):
    """F35 widened the lightbox from figures to every story image; the
    server just has to emit the <img> inside .story__body for story.js to
    find it."""
    story_id = storage.create_story(
        stories_dir, "Inline photo", date(2026, 1, 1),
        "We walked and then ![](photo-001.jpg)she slept.",
    )
    html = auth_client.get(f"/story/{story_id}").data.decode()
    assert "<figure>" not in html
    assert f'src="/story/{story_id}/media/photo-001.jpg"' in html
