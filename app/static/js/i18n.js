// Reads the JSON blob base.html embeds (from app/i18n.py's JS_STRINGS,
// translated server-side) and exposes it as a lookup for the handful of
// JS files that render user-facing text at runtime — editor save/voice
// states, the in-app camera, the family tree's view buttons. Falls back
// to the English text itself so a missing/broken tag never breaks a page.
(function () {
  var data = {};
  var node = document.getElementById("storybook-i18n-data");
  if (node) {
    try {
      data = JSON.parse(node.textContent) || {};
    } catch (e) {
      data = {};
    }
  }
  window.storybookT = function (text) {
    return Object.prototype.hasOwnProperty.call(data, text) ? data[text] : text;
  };
})();
