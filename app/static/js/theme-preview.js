// The theme editor's live preview (FEATURES.md F52).
//
// Eighteen hex fields and a description, and until this existed the only
// way to find out what they added up to was to save and go and look. This
// paints a miniature of the book from whatever is in the fields right now.
//
// It computes nothing itself: every colour comes from palette-logic.js,
// which is a port of palette.py held to it by tests/test_palette_preview.py.
// The point of the preview is that it is not an impression of the palette,
// it is the palette — so if you are tempted to approximate something here,
// derive it there instead.
//
// Enhancement only. The element starts `hidden` in the template and is
// shown from here, so a browser with this file blocked sees the form it
// always saw rather than an empty box promising a picture.
(function () {
  "use strict";

  var Palette = window.PaletteLogic;
  var root = document.getElementById("theme-preview");
  if (!Palette || !root) return;

  var pane = document.getElementById("theme-preview-pane");
  var tabs = document.getElementById("theme-preview-tabs");
  var checks = document.getElementById("theme-preview-checks");
  var empty = document.getElementById("theme-preview-empty");
  var warning = document.getElementById("theme-preview-warning");
  if (!pane || !tabs || !checks || !empty || !warning) return;

  // The order main.css declares them in, which is the order the reader's
  // toggle offers them in.
  var SCHEMES = ["dark", "light", "manuscript"];

  var WARNING_TEMPLATE = root.getAttribute("data-warning") || "";
  var EMPTY_TEXT = root.getAttribute("data-empty") || "";
  var NONE_TEXT = root.getAttribute("data-none") || "";

  var active = null;

  function field(scheme, key) {
    return document.getElementById(scheme + "-" + key);
  }

  function seedFor(scheme) {
    var seed = {};
    var missing = false;
    Palette.SEEDS.forEach(function (key) {
      var input = field(scheme, key);
      var value = input ? input.value.trim() : "";
      if (Palette.isHex(value)) seed[key] = value;
      else missing = true;
    });
    return missing ? null : seed;
  }

  function offered() {
    return SCHEMES.filter(function (scheme) {
      var box = document.querySelector(
        'input[name="schemes"][value="' + scheme + '"]');
      return box && box.checked;
    });
  }

  function label(scheme) {
    var box = document.querySelector(
      'input[name="schemes"][value="' + scheme + '"]');
    // The scheme's own translated name is already on the page, in the
    // checkbox's label — no need for a second copy in a JS dictionary.
    var text = box && box.parentNode ? box.parentNode.textContent.trim() : "";
    return text || scheme;
  }

  function renderTabs(list) {
    tabs.textContent = "";
    if (list.length < 2) return;
    list.forEach(function (scheme) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "theme-preview__tab";
      button.textContent = label(scheme);
      button.setAttribute("aria-pressed", scheme === active ? "true" : "false");
      button.addEventListener("click", function () {
        active = scheme;
        render();
      });
      tabs.appendChild(button);
    });
  }

  function paint(seed) {
    var variables = Palette.derive(seed);
    // Custom properties and `color-scheme` alike — setProperty takes both,
    // and the last of them is what makes the browser draw its own furniture
    // (a scrollbar, a focus ring) in the same world as the preview.
    Object.keys(variables).forEach(function (name) {
      pane.style.setProperty(name, variables[name]);
    });
  }

  function renderChecks(seed) {
    var rows = Palette.checks(seed);
    var byKey = {};
    rows.forEach(function (row) { byKey[row.key] = row; });
    checks.querySelectorAll(".theme-preview__check").forEach(function (item) {
      var row = byKey[item.getAttribute("data-check")];
      var value = item.querySelector(".theme-preview__check-value");
      if (!row || !value) return;
      // One decimal, the way the server words its own warning, so the two
      // never appear to disagree over the same palette.
      value.textContent = row.ratio.toFixed(1) + ":1";
      item.classList.toggle("is-low", row.ratio < row.floor);
    });
  }

  function renderWarning(seed) {
    var ratio = Palette.contrast(
      Palette.parseHex(seed.text), Palette.parseHex(seed.bg));
    if (ratio >= Palette.TEXT_FLOOR) {
      warning.hidden = true;
      warning.textContent = "";
      return;
    }
    warning.textContent = WARNING_TEMPLATE.replace("{ratio}", ratio.toFixed(1));
    warning.hidden = false;
  }

  function showNothing(message) {
    pane.hidden = true;
    checks.hidden = true;
    warning.hidden = true;
    empty.textContent = message;
    empty.hidden = false;
  }

  function render() {
    var list = offered();
    if (!list.length) {
      active = null;
      renderTabs(list);
      showNothing(NONE_TEXT);
      return;
    }
    if (list.indexOf(active) === -1) active = list[0];
    renderTabs(list);

    var seed = seedFor(active);
    if (!seed) {
      showNothing(EMPTY_TEXT);
      return;
    }

    empty.hidden = true;
    pane.hidden = false;
    checks.hidden = false;
    paint(seed);
    renderChecks(seed);
    renderWarning(seed);
  }

  // The brand line in the miniature is the theme's own name, so it changes
  // as it is typed. Nothing else in the preview is text the user controls.
  var nameField = document.querySelector('.theme-form input[name="label"]');
  var brand = pane.querySelector(".theme-preview__brand");
  // What the template put there: the book's own title, which is what the
  // nav really shows until this theme has a name. Emptying the field has
  // to go back to it rather than leaving the last thing typed stranded.
  var brandFallback = brand ? brand.textContent.trim() : "";
  function renderName() {
    if (!nameField || !brand) return;
    brand.textContent = nameField.value.trim() || brandFallback;
  }

  // `input` catches typing and the colour picker's drag; `change` catches
  // the checkboxes and a picker that only reports on release. Bound on the
  // form so fields added later would be covered too.
  var form = root.closest ? root.closest(".theme-form") : null;
  (form || document).addEventListener("input", function () {
    render();
    renderName();
  });
  (form || document).addEventListener("change", function () {
    render();
    renderName();
  });

  root.hidden = false;
  renderName();
  render();
})();
