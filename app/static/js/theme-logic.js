// Pure, DOM-free helpers behind the theme menu (FEATURES.md F46, F49):
// which colour scheme a press lands on, and what a press on the toggle
// should do given what the menu is already doing. Kept out of theme.js so
// the two rules that are easy to get subtly wrong — a scheme that came
// from the system rather than a choice, and a tap arriving right after a
// long press opened the menu — can be unit-tested under plain Node
// (tests/js/theme_logic_test.mjs).
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.ThemeLogic = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // The next stop in the pack's own cycle. A `current` the list doesn't
  // contain means the reader has never chosen — the scheme on screen came
  // from their system — and the first press lands on the first stop.
  function nextScheme(schemes, current) {
    var list = (schemes || []).filter(Boolean);
    if (!list.length) return null;
    var index = list.indexOf(current);
    return list[(index + 1) % list.length];
  }

  // What a press on the toggle means. Three inputs, and the order they are
  // tested in is the whole rule:
  //
  //   longPress  the press was held, so it was a request for the menu, and
  //              the click that follows a long press must not also cycle —
  //              a reader who held the button to see their options would
  //              otherwise have their colours changed underneath the menu.
  //   open       the menu is showing, so the toggle is the way out of it.
  //   otherwise  the fast path, and the reason the menu is behind a hold:
  //              one tap still cycles light and dark.
  function pressAction(state) {
    var s = state || {};
    if (s.longPress) return "open";
    if (s.open) return "close";
    return "cycle";
  }

  return { nextScheme: nextScheme, pressAction: pressAction };
});
