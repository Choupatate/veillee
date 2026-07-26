// Tests for app/static/js/media-links.js — the bare-filename <-> editor-URL
// conversion that lets the editor preview images without changing what gets
// written to disk. Run directly: node tests/js/media_links_test.mjs
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const MediaLinks = require("../../app/static/js/media-links.js");

const BASE = "/story/2026-03-01-a-day-out/media";
const { toEditorMarkdown, toStoredMarkdown, toEditorSrc } = MediaLinks;

// --- expanding for the editor ------------------------------------------------

assert.equal(
  toEditorMarkdown("![](photo-001.jpg)", BASE),
  `![](${BASE}/photo-001.jpg)`,
  "a bare filename becomes a resolvable URL"
);

assert.equal(
  toEditorMarkdown("![Her first snow](photo-002.jpg)", BASE),
  `![Her first snow](${BASE}/photo-002.jpg)`,
  "alt text is untouched"
);

assert.equal(
  toEditorMarkdown('![](photo-003.jpg "In the garden")', BASE),
  `![](${BASE}/photo-003.jpg "In the garden")`,
  "a link title survives the rewrite"
);

assert.equal(
  toEditorMarkdown("Before\n\n![](photo-001.jpg)\n\n![](photo-002.jpg)\n", BASE),
  `Before\n\n![](${BASE}/photo-001.jpg)\n\n![](${BASE}/photo-002.jpg)\n`,
  "every image in the body is rewritten"
);

assert.equal(
  toEditorMarkdown("![](https://example.com/cat.jpg)", BASE),
  "![](https://example.com/cat.jpg)",
  "an absolute URL is somebody else's and is left alone"
);

assert.equal(
  toEditorMarkdown("![](//example.com/cat.jpg)", BASE),
  "![](//example.com/cat.jpg)",
  "protocol-relative URLs are left alone"
);

assert.equal(
  toEditorMarkdown("![](/people/mamie/media/photo-001.jpg)", BASE),
  "![](/people/mamie/media/photo-001.jpg)",
  "a root-relative path is already resolvable and is left alone"
);

assert.equal(
  toEditorMarkdown("A [link](photo-001.jpg) is not an image", BASE),
  "A [link](photo-001.jpg) is not an image",
  "only image syntax is rewritten, never a plain link"
);

assert.equal(
  toEditorMarkdown("![](photo-001.jpg)", ""),
  "![](photo-001.jpg)",
  "with no media base (a story not saved yet) nothing changes"
);

assert.equal(toEditorMarkdown("", BASE), "", "empty markdown stays empty");
assert.equal(toEditorMarkdown(null, BASE), "", "null markdown becomes empty");

// --- collapsing back for storage ---------------------------------------------

assert.equal(
  toStoredMarkdown(`![](${BASE}/photo-001.jpg)`, BASE),
  "![](photo-001.jpg)",
  "the editor URL collapses back to the bare filename"
);

assert.equal(
  toStoredMarkdown(`![Her first snow](${BASE}/photo-002.jpg "In the garden")`, BASE),
  '![Her first snow](photo-002.jpg "In the garden")',
  "alt text and title survive the round trip"
);

assert.equal(
  toStoredMarkdown("![](https://example.com/cat.jpg)", BASE),
  "![](https://example.com/cat.jpg)",
  "an external image is not touched on the way back either"
);

assert.equal(
  toStoredMarkdown("![](/story/some-other-story/media/photo-001.jpg)", BASE),
  "![](/story/some-other-story/media/photo-001.jpg)",
  "another story's media URL is a real cross-link, not ours to collapse"
);

assert.equal(
  toStoredMarkdown(`![](${BASE}/nested/photo-001.jpg)`, BASE),
  `![](${BASE}/nested/photo-001.jpg)`,
  "only a single path segment collapses; a deeper path isn't ours"
);

assert.equal(
  toStoredMarkdown("![](photo-001.jpg)", BASE),
  "![](photo-001.jpg)",
  "an already-bare filename is idempotent"
);

// --- the round trip is what actually protects the saved file -----------------

const body = [
  "# A day out",
  "",
  "![Her first snow](photo-001.jpg)",
  "",
  "Then we walked home.",
  "",
  "![](photo-002.jpg)",
  "![](https://example.com/cat.jpg)",
  "",
].join("\n");

assert.equal(
  toStoredMarkdown(toEditorMarkdown(body, BASE), BASE),
  body,
  "expand -> collapse returns the file byte for byte"
);

// A trailing slash on the base must not produce a doubled one.
assert.equal(
  toEditorMarkdown("![](photo-001.jpg)", BASE + "/"),
  `![](${BASE}/photo-001.jpg)`,
  "a trailing slash in the base is normalized away"
);
assert.equal(
  toStoredMarkdown(`![](${BASE}/photo-001.jpg)`, BASE + "/"),
  "![](photo-001.jpg)",
  "collapsing tolerates a trailing slash too"
);

// --- a single freshly uploaded filename --------------------------------------

assert.equal(toEditorSrc("photo-004.jpg", BASE), `${BASE}/photo-004.jpg`);
assert.equal(
  toEditorSrc("photo-004.jpg", ""),
  "photo-004.jpg",
  "with no base the filename is handed back unchanged"
);
assert.equal(
  toEditorSrc("https://example.com/cat.jpg", BASE),
  "https://example.com/cat.jpg",
  "an absolute src is never prefixed"
);

console.log("media-links.js: all assertions passed");
