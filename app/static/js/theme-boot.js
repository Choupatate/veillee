// Runs synchronously in <head>, before first paint: applies the stored
// theme so the page never flashes the wrong colors, and marks the root as
// JS-capable for CSS that opts in. Lived inline in base.html until F36's
// Content-Security-Policy (script-src 'self', no inline scripts) — this
// file must stay a plain blocking <script> in <head> to keep doing its job.
document.documentElement.classList.add("js");
(function () {
  var stored = window.SafeStorage.getString("storybook-theme");
  if (stored === "light" || stored === "dark" || stored === "manuscript") {
    document.documentElement.setAttribute("data-theme", stored);
  }
  // F44: firelight is on unless it was turned off, so only "off" is ever
  // stored — an empty slot has to mean "on" for a first visit. Applied here
  // rather than in firelight.js so the wash never fades in after paint.
  if (window.SafeStorage.getString("storybook-firelight") === "off") {
    document.documentElement.setAttribute("data-firelight", "off");
  }
})();
