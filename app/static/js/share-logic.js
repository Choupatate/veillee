// Pure, DOM-free rules behind the "hand this link over" button
// (FEATURES.md F56): which of the three ways of giving someone a URL a
// given browser can actually do, and what a failed share means. Kept out
// of share-link.js because both rules are the kind that look obvious and
// are wrong in one specific case — a share sheet the user dismissed is not
// a share that failed — and that case is unreachable from a test that
// needs a real share sheet (tests/js/share_link_test.mjs).
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.ShareLogic = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // Best available way to hand over a URL, in descending order of how much
  // work it saves the person doing it:
  //
  //   "share"   the OS share sheet — the link lands in a conversation with
  //             the person it was made for, which is the whole point.
  //   "copy"    the clipboard, and say so. Desktop, mostly.
  //   "select"  select the text and let them press the keys. Not copying,
  //             but one keystroke from it rather than a dead button.
  //
  // `canShare` must come from `navigator.canShare({url})` rather than from
  // `"share" in navigator`: the property exists in places the call throws,
  // and some browsers can share text but not a URL. `canCopy` is false on
  // plain HTTP, which plenty of these installs are.
  function tier(capabilities) {
    var c = capabilities || {};
    if (c.canShare) return "share";
    if (c.canCopy) return "copy";
    return "select";
  }

  // A share sheet that was opened and dismissed rejects with AbortError.
  // That is the person saying "not now", and it is the one rejection that
  // must not be treated as a broken share — quietly copying the link to
  // their clipboard because they closed a dialog puts a private URL
  // somewhere they did not ask for it.
  function isDismissal(error) {
    return !!error && error.name === "AbortError";
  }

  // What to do when navigator.share() rejects: nothing if they dismissed
  // it, otherwise fall down a tier and copy.
  function afterShareFailure(error) {
    return isDismissal(error) ? "none" : "copy";
  }

  return { tier: tier, isDismissal: isDismissal, afterShareFailure: afterShareFailure };
});
