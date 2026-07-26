// Story markdown stores image links as bare filenames ("photo-001.jpg"),
// deliberately: the folder has to stay readable and movable without the
// app (see CLAUDE.md), and rendering.py is what turns a bare src into
// "/story/<id>/media/<file>" at render time. A browser editor has no such
// step, so it resolves "photo-001.jpg" against the page URL and shows a
// broken image. These two pure functions convert between the two forms —
// bare on disk, resolvable in the editor — so the editor can preview what
// the reader will see without changing a byte of what's saved.
//
// DOM-free on purpose, so it's unit-tested under plain Node
// (tests/js/media_links_test.mjs).
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.MediaLinks = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // Same test rendering.py's _ABSOLUTE_SRC_RE applies: anything with a
  // scheme, a protocol-relative "//", or a leading "/" is somebody else's
  // URL and is left exactly as written.
  var ABSOLUTE_RE = /^([a-z]+:)?\/\/|^\//i;

  // ![alt](destination "optional title") — destination is everything up to
  // whitespace or the closing paren, which covers every link this editor
  // produces (upload filenames never contain spaces or parens).
  var IMAGE_RE = /(!\[[^\]]*\]\()([^\s)]*)([^)]*\))/g;

  function isAbsolute(src) {
    return ABSOLUTE_RE.test(src);
  }

  function trimBase(base) {
    return (base || "").replace(/\/+$/, "");
  }

  function mapImageSrcs(markdown, fn) {
    if (!markdown) return markdown || "";
    return markdown.replace(IMAGE_RE, function (whole, open, src, rest) {
      var mapped = fn(src);
      return mapped === null ? whole : open + mapped + rest;
    });
  }

  /** Bare filename -> "<base>/<filename>", so the editor can load it. */
  function toEditorMarkdown(markdown, base) {
    var prefix = trimBase(base);
    if (!prefix) return markdown || "";
    return mapImageSrcs(markdown, function (src) {
      if (!src || isAbsolute(src)) return null;
      return prefix + "/" + src;
    });
  }

  /** The inverse, applied before anything is saved or autosaved. */
  function toStoredMarkdown(markdown, base) {
    var prefix = trimBase(base);
    if (!prefix) return markdown || "";
    return mapImageSrcs(markdown, function (src) {
      if (src.indexOf(prefix + "/") !== 0) return null;
      var filename = src.slice(prefix.length + 1);
      // Only ever collapse back to a single path segment; a deeper path
      // isn't something this app wrote, so leave it alone.
      return filename && filename.indexOf("/") === -1 ? filename : null;
    });
  }

  /** The editor-side URL for one freshly uploaded filename. */
  function toEditorSrc(filename, base) {
    var prefix = trimBase(base);
    if (!prefix || !filename || isAbsolute(filename)) return filename;
    return prefix + "/" + filename;
  }

  return {
    toEditorMarkdown: toEditorMarkdown,
    toStoredMarkdown: toStoredMarkdown,
    toEditorSrc: toEditorSrc,
  };
});
