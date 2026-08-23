// Pure, DOM-free rules behind the editor's crash recovery (FEATURES.md
// F31): whether a draft left in localStorage is worth offering back, and
// whether what came out of storage is a draft at all.
//
// Split out of editor.js because the decision was wrong and nothing could
// see it. `applyDraft` restores fourteen fields — date, unlock, draft and
// archived flags, people, tags, sources, audience, the family pickers, the
// sepia dial — while the question "is there anything to restore?" compared
// two: the title and the markdown. A parent who set the date, chose who
// the story was for, tagged it, and then lost the tab got no banner and no
// draft. The autosave had run; the recovery threw it away.
//
// So the comparison is over the whole payload now, and it is here where it
// can be tested (tests/js/draft_logic_test.mjs) rather than three hundred
// lines into a file that needs a browser.
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.DraftLogic = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // Bookkeeping the editor adds on the way out, and which says nothing
  // about whether the writing changed.
  var IGNORED = ["savedAt"];

  // A stable string for one payload value. Arrays keep their order (the
  // order of `people` and `sources` is meaningful and editable), objects
  // are compared key-by-key in sorted order so that two payloads built the
  // same way from the same page never differ on key order alone.
  function canonical(value) {
    if (value === null || value === undefined) return "";
    if (Array.isArray(value)) {
      return "[" + value.map(canonical).join(",") + "]";
    }
    if (typeof value === "object") {
      return "{" + Object.keys(value).sort().map(function (key) {
        return key + ":" + canonical(value[key]);
      }).join(",") + "}";
    }
    // false, 0 and "" all have to survive as themselves: a draft toggled
    // off is a change from a draft toggled on.
    return typeof value + ":" + String(value);
  }

  // Whether the thing read back out of localStorage looks like a payload
  // this editor wrote. Storage is shared per-origin and survives app
  // updates, so it can hold anything — an older shape, a half-written
  // string, something else entirely.
  function isRestorable(stored) {
    return !!stored
      && typeof stored === "object"
      && !Array.isArray(stored)
      && typeof stored.title === "string"
      && typeof stored.markdown === "string";
  }

  // Every field either side mentions, minus the bookkeeping. Taken from
  // both so that a field present in the stored draft but absent from the
  // page — an older autosave, or a picker that isn't on this editor — is
  // still noticed rather than silently matching.
  function comparedKeys(stored, baseline) {
    var keys = {};
    [stored, baseline].forEach(function (side) {
      Object.keys(side || {}).forEach(function (key) {
        if (IGNORED.indexOf(key) === -1) keys[key] = true;
      });
    });
    return Object.keys(keys).sort();
  }

  // The question the recovery banner asks. `baseline` is the payload the
  // page would submit right now, untouched — so this is "did the writing
  // get further than what is already on screen?"
  function hasRecoverableChanges(stored, baseline) {
    if (!isRestorable(stored)) return false;
    var keys = comparedKeys(stored, baseline);
    for (var i = 0; i < keys.length; i++) {
      var key = keys[i];
      if (canonical(stored[key]) !== canonical((baseline || {})[key])) return true;
    }
    return false;
  }

  // What the banner says it is offering. Never throws on a savedAt that is
  // missing or nonsense — a draft with an unreadable timestamp is still a
  // draft worth offering, it just cannot say when.
  function savedAtLabel(stored, formatter) {
    var stamp = stored && stored.savedAt;
    if (typeof stamp !== "number" || !isFinite(stamp)) return "";
    var when = new Date(stamp);
    if (isNaN(when.getTime())) return "";
    return formatter ? formatter(when) : when.toISOString();
  }

  return {
    canonical: canonical,
    isRestorable: isRestorable,
    comparedKeys: comparedKeys,
    hasRecoverableChanges: hasRecoverableChanges,
    savedAtLabel: savedAtLabel,
  };
});
