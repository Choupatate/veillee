/* Handing a link over (FEATURES.md F56).
 *
 * A write link and an invite are both a URL that exists to be given to one
 * specific person — usually a grandparent, usually over WhatsApp, usually
 * from a phone. Until now the page printed the URL and left you to select
 * it with your fingertip, which is the single most annoying gesture a
 * touchscreen has.
 *
 * Three tiers, best first, because this is exactly the kind of button that
 * must never be a dead one:
 *
 *   1. `navigator.share()`  — the OS share sheet. The link goes straight
 *      into a conversation with the person it is for. Phones, and Safari.
 *   2. `navigator.clipboard` — copy, and say so. Desktop browsers.
 *   3. select the text      — not the same as copying it, but it is one
 *      keystroke away rather than a dead button. Same last resort
 *      `theme-form.js` already uses for its copy buttons, and for the same
 *      reason: the Clipboard API needs a secure context, and plenty of
 *      these installs are plain HTTP on a home network.
 *
 * The button ships `hidden` and this file unhides it, so a browser with no
 * JavaScript shows the URL as selectable text and no button that would do
 * nothing — the same bargain the camera button makes in `editor.js`.
 */
(function () {
  "use strict";

  function t(text) {
    return window.storybookT ? window.storybookT(text) : text;
  }

  function flash(button, message) {
    var was = button.textContent;
    button.textContent = message;
    setTimeout(function () {
      button.textContent = was;
    }, 1500);
  }

  function selectFallback(button) {
    var target = document.getElementById(button.getAttribute("data-share-source"));
    if (!target) return;
    var range = document.createRange();
    range.selectNodeContents(target);
    var selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  }

  function copy(button, url) {
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      selectFallback(button);
      return;
    }
    navigator.clipboard.writeText(url).then(
      function () { flash(button, t("Copied")); },
      function () { selectFallback(button); }
    );
  }

  document.querySelectorAll("[data-share-url]").forEach(function (button) {
    var url = button.getAttribute("data-share-url");
    if (!url) return;

    // `navigator.share` exists but throws outside a secure context, and on
    // some desktop browsers it exists and can only share text. Feature-test
    // for the real thing rather than for the property.
    var tier = window.ShareLogic.tier({
      canShare: !!(navigator.share && navigator.canShare
        && navigator.canShare({ url: url })),
      canCopy: !!(navigator.clipboard && navigator.clipboard.writeText),
    });

    button.textContent = tier === "share" ? t("Share") : t("Copy");
    button.hidden = false;

    button.addEventListener("click", function () {
      if (tier !== "share") {
        copy(button, url);
        return;
      }
      navigator.share({
        title: button.getAttribute("data-share-title") || document.title,
        text: button.getAttribute("data-share-text") || "",
        url: url,
      }).catch(function (error) {
        if (window.ShareLogic.afterShareFailure(error) === "copy") copy(button, url);
      });
    });
  });
})();
