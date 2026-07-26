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
})();
