"""FEATURES.md F57: photos arriving from the phone's share sheet.

The interesting tests here are the negative ones. `/share` is the only
route in the app exempted from `CSRFProtect` — the share sheet builds the
request and cannot be handed a token — so the things worth pinning are the
guards that stand in its place: the `Sec-Fetch-Site` check, the login
requirement, and the fact that what a share creates is a *draft* and not a
page of the book.
"""

import io

import pytest
from PIL import Image

from app import storage
from app.routes_pages import SHARE_FILES_FIELD
from app.timeline import readable_stories


def _photo(name="IMG_2024.jpg", colour=(200, 120, 60)):
    buf = io.BytesIO()
    Image.new("RGB", (1200, 900), colour).save(buf, format="JPEG")
    buf.seek(0)
    return (buf, name)


def _share(client, headers=None, **fields):
    """A POST shaped exactly like the one Android sends: multipart, no CSRF
    token, arriving as a browser-initiated navigation."""
    sent = {"Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate"}
    sent.update(headers or {})
    return client.post("/share", data=fields,
                       content_type="multipart/form-data", headers=sent)


# --- the manifest side -------------------------------------------------------


def test_the_manifest_advertises_the_share_target(auth_client):
    target = auth_client.get("/manifest.webmanifest").get_json()["share_target"]
    assert target["method"] == "POST"
    assert target["enctype"] == "multipart/form-data"
    assert target["action"] == "/share"


def test_the_manifest_names_the_field_the_route_actually_reads(auth_client):
    """A mismatch here loses every shared photo silently: Android posts
    under the manifest's name and the route reads a different one."""
    target = auth_client.get("/manifest.webmanifest").get_json()["share_target"]
    assert target["params"]["files"][0]["name"] == SHARE_FILES_FIELD


# --- the happy path ----------------------------------------------------------


def test_a_shared_photo_lands_in_the_editor(auth_client, stories_dir):
    resp = _share(auth_client, text="At the lake", **{SHARE_FILES_FIELD: _photo()})
    assert resp.status_code == 302
    assert resp.headers["Location"].startswith("/edit/")

    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    story = storage.get_story(stories_dir, story_id)
    assert story.title == "At the lake"


def test_the_photo_is_saved_and_referenced_by_bare_filename(auth_client, stories_dir):
    resp = _share(auth_client, **{SHARE_FILES_FIELD: _photo()})
    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    story = storage.get_story(stories_dir, story_id)

    assert "![](photo-001.jpg)" in story.body
    assert (stories_dir / story_id / "photo-001.jpg").is_file()
    # Bare, never a URL — the folder has to stay portable without the app.
    assert "/story/" not in story.body


def test_several_photos_all_arrive_in_order(auth_client, stories_dir):
    resp = _share(auth_client, **{SHARE_FILES_FIELD: [
        _photo("a.jpg"), _photo("b.jpg"), _photo("c.jpg")]})
    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    body = storage.get_story(stories_dir, story_id).body
    assert body.index("photo-001") < body.index("photo-002") < body.index("photo-003")


def test_the_shared_photo_is_re_encoded_like_every_other_upload(auth_client, stories_dir):
    """Same guarantee as the editor's upload path: Pillow rewrites it, so a
    thumbnail exists and no original bytes are kept verbatim."""
    resp = _share(auth_client, **{SHARE_FILES_FIELD: _photo()})
    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    assert (stories_dir / story_id / "photo-001.thumb.jpg").is_file()


# --- what a share is, and is not ---------------------------------------------


def test_a_share_creates_a_draft_not_a_page_of_the_book(auth_client, stories_dir):
    """The load-bearing one. A picture flicked at the app from another
    screen is not a memory yet, and this is also what keeps the CSRF
    exemption proportionate."""
    _share(auth_client, **{SHARE_FILES_FIELD: _photo()})
    stories = storage.list_stories(stories_dir)
    assert len(stories) == 1
    assert stories[0].draft is True
    assert readable_stories(stories) == []


# --- titles ------------------------------------------------------------------


def test_an_explicit_shared_title_wins(auth_client, stories_dir):
    resp = _share(auth_client, title="Milo's first steps", text="some caption")
    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    story = storage.get_story(stories_dir, story_id)
    assert story.title == "Milo's first steps"
    assert "some caption" in story.body


def test_a_short_caption_becomes_the_title(auth_client, stories_dir):
    resp = _share(auth_client, text="At the lake")
    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    assert storage.get_story(stories_dir, story_id).title == "At the lake"


def test_a_shared_paragraph_is_a_body_not_a_name(auth_client, stories_dir):
    """A folder name is built from the title, so a pasted paragraph must
    not become one."""
    paragraph = "x" * 200
    resp = _share(auth_client, text=paragraph)
    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    story = storage.get_story(stories_dir, story_id)
    assert story.title == "Untitled"
    assert paragraph in story.body


def test_a_bare_photo_with_no_words_at_all(auth_client, stories_dir):
    """The common case: Android shares a picture and nothing else."""
    resp = _share(auth_client, **{SHARE_FILES_FIELD: _photo()})
    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    assert storage.get_story(stories_dir, story_id).title == "Untitled"


# --- the guards standing in for CSRF -----------------------------------------


def test_it_accepts_a_post_with_no_csrf_token(auth_client, stories_dir):
    """The exemption itself. Android builds this request; there is nowhere
    to put a token. If this starts failing, every share is silently lost."""
    resp = _share(auth_client, **{SHARE_FILES_FIELD: _photo()})
    assert resp.status_code == 302
    assert len(storage.list_stories(stories_dir)) == 1


@pytest.mark.parametrize("site", ["cross-site", "same-site"])
def test_a_forged_post_from_another_site_is_refused(auth_client, stories_dir, site):
    resp = _share(auth_client, headers={"Sec-Fetch-Site": site},
                  **{SHARE_FILES_FIELD: _photo()})
    assert resp.status_code == 403
    assert storage.list_stories(stories_dir) == []


@pytest.mark.parametrize("site", ["none", "same-origin"])
def test_the_browsers_own_navigation_is_allowed(auth_client, site):
    resp = _share(auth_client, headers={"Sec-Fetch-Site": site}, text="hello")
    assert resp.status_code == 302


def test_a_browser_too_old_to_send_fetch_metadata_still_works(auth_client):
    """Absence is allowed deliberately: a browser that sends no Fetch
    Metadata is one with no Web Share Target either, and the header is set
    by the browser, so a page cannot suppress it to get through."""
    resp = auth_client.post("/share", data={"text": "hello"},
                            content_type="multipart/form-data")
    assert resp.status_code == 302


def test_sharing_while_logged_out_goes_to_the_login_page(client, stories_dir):
    resp = _share(client, text="hello")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]
    assert storage.list_stories(stories_dir) == []


# --- things that are not photographs -----------------------------------------


def test_a_file_pillow_cannot_read_does_not_lose_the_whole_share(auth_client, stories_dir):
    """Better to keep the story and drop one attachment than to 500 on the
    person and lose everything they shared."""
    junk = (io.BytesIO(b"this is not an image"), "notes.txt")
    resp = _share(auth_client, text="At the lake",
                  **{SHARE_FILES_FIELD: [_photo(), junk]})
    assert resp.status_code == 302
    story_id = resp.headers["Location"].rsplit("/", 1)[1]
    story = storage.get_story(stories_dir, story_id)
    assert story.title == "At the lake"
    assert "![](photo-001.jpg)" in story.body
    assert "notes.txt" not in story.body
