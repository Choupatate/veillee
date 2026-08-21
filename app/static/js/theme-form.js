// The two small conveniences on the theme-making pages (FEATURES.md F50):
// a colour picker beside each hex field, and a copy button on each prompt.
// Both are enhancements — the hex fields and the textareas are what the
// page actually runs on, and everything here can fail without costing
// anyone a theme.
(function () {
  "use strict";

  // The <input type="color"> carries no name; the text field beside it is
  // what gets submitted, so the form still works with this file absent.
  document.querySelectorAll("[data-syncs]").forEach(function (picker) {
    var field = document.getElementById(picker.getAttribute("data-syncs"));
    if (!field) return;
    picker.addEventListener("input", function () {
      field.value = picker.value;
    });
    field.addEventListener("input", function () {
      if (/^#[0-9a-fA-F]{6}$/.test(field.value.trim())) picker.value = field.value.trim();
    });
  });

  document.querySelectorAll(".asset-sheet__copy").forEach(function (button) {
    button.addEventListener("click", function () {
      var source = document.getElementById(button.getAttribute("data-copies"));
      if (!source) return;
      var done = function () {
        var was = button.textContent;
        button.textContent = button.getAttribute("data-copied") || was;
        setTimeout(function () {
          button.textContent = was;
        }, 1500);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(source.value).then(done, function () {
          source.select();
        });
      } else {
        // Older browsers, and any page not served over HTTPS: selecting the
        // text is not the same as copying it, but it is one keystroke away
        // rather than a dead button.
        source.select();
      }
    });
  });

  document.querySelectorAll("[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!window.confirm(form.getAttribute("data-confirm"))) event.preventDefault();
    });
  });
})();
