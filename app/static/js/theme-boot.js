// Runs synchronously in <head>, before first paint: applies the stored
// theme so the page never flashes the wrong colors, and marks the root as
// JS-capable for CSS that opts in. Lived inline in base.html until F36's
// Content-Security-Policy (script-src 'self', no inline scripts) — this
// file must stay a plain blocking <script> in <head> to keep doing its job.
document.documentElement.classList.add("js");
(function () {
  var root = document.documentElement;

  // F46: which colour schemes exist is the theme pack's decision, rendered
  // onto <html> by base.html. A reader who chose "manuscript" in a ranch
  // book and then opens an orbit one must not be handed a scheme that pack
  // never designed — so an unavailable stored value is simply not applied,
  // and the reader falls back to their system preference.
  var allowed = (root.getAttribute("data-schemes") || "").split(" ");
  window.StorybookSchemes = allowed;

  var stored = window.SafeStorage.getString("storybook-theme");
  if (stored && allowed.indexOf(stored) !== -1) {
    root.setAttribute("data-theme", stored);
  }
  // F44: firelight is on unless it was turned off, so only "off" is ever
  // stored — an empty slot has to mean "on" for a first visit. Applied here
  // rather than in firelight.js so the wash never fades in after paint.
  if (window.SafeStorage.getString("storybook-firelight") === "off") {
    root.setAttribute("data-firelight", "off");
  }
})();
