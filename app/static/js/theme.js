(function () {
  var STORAGE_KEY = "storybook-theme";
  // F46: the schemes this theme pack offers, in cycle order — theme-boot.js
  // read them off <html> before first paint. A pack whose world has no aged
  // paper in it declares two, and the toggle simply has one fewer stop.
  var THEMES = (window.StorybookSchemes || []).filter(Boolean);
  if (!THEMES.length) THEMES = ["dark", "light", "manuscript"];
  var toggle = document.getElementById("theme-toggle");

  function currentTheme() {
    var attr = document.documentElement.getAttribute("data-theme");
    if (attr) return attr;
    return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  }

  // Loaded on every page before any page-specific script (base.html), so
  // editor.js/tree.js derive their own theme checks from this instead of
  // each re-deriving the data-theme/prefers-color-scheme fallback logic.
  window.StorybookTheme = { current: currentTheme };

  // R4.8: the two theme-color metas key off prefers-color-scheme, so once a
  // theme is actively chosen (rather than left to follow the OS), the
  // address-bar chrome can clash with it. Once a theme is applied, overwrite
  // both metas' content with that theme's own background so whichever one
  // the browser matches shows the same color. With no stored theme neither
  // meta is touched, so the OS-scheme defaults keep applying.
  // Captured before the first sync below overwrites them: going back to
  // "System" has to put the OS-keyed pair back, or the address bar would
  // stay stuck on whichever scheme was last chosen.
  var META_DEFAULTS = [];
  document.querySelectorAll('meta[name="theme-color"]').forEach(function (meta) {
    META_DEFAULTS.push([meta, meta.getAttribute("content")]);
  });

  function restoreThemeColorMeta() {
    META_DEFAULTS.forEach(function (pair) {
      pair[0].setAttribute("content", pair[1]);
    });
  }

  function syncThemeColorMeta() {
    var bg = getComputedStyle(document.documentElement).getPropertyValue("--color-bg").trim();
    if (!bg) return;
    document.querySelectorAll('meta[name="theme-color"]').forEach(function (meta) {
      meta.setAttribute("content", bg);
    });
  }

  if (document.documentElement.hasAttribute("data-theme")) {
    syncThemeColorMeta();
  }

  var menu = document.getElementById("theme-menu");
  if (!toggle) return;

  // --- choosing a scheme ----------------------------------------------------

  function applyScheme(scheme) {
    if (scheme) {
      document.documentElement.setAttribute("data-theme", scheme);
      if (window.SafeStorage) window.SafeStorage.setString(STORAGE_KEY, scheme);
      syncThemeColorMeta();
    } else {
      // "System": forget the choice rather than store a fourth value, so
      // the page follows prefers-color-scheme again the way a first visit
      // does — and theme-boot.js has nothing to re-apply on the next load.
      document.documentElement.removeAttribute("data-theme");
      if (window.SafeStorage) window.SafeStorage.removeString(STORAGE_KEY);
      restoreThemeColorMeta();
    }
    markChips();
    // Anything that can't be expressed as a CSS variable — the Toast UI
    // toolbar's icon sprite (F44) — listens for this rather than polling.
    window.dispatchEvent(
      new CustomEvent("storybook:themechange", { detail: currentTheme() })
    );
  }

  function cycle() {
    applyScheme(window.ThemeLogic.nextScheme(THEMES, storedTheme()));
  }

  // What the reader *chose*, which is not what they are looking at: with no
  // choice stored the cycle starts from the top rather than from whatever
  // their system happens to be showing.
  function storedTheme() {
    return (window.SafeStorage && window.SafeStorage.getString(STORAGE_KEY)) || "";
  }

  function markChips() {
    if (!menu) return;
    var chosen = storedTheme();
    menu.querySelectorAll("[data-scheme]").forEach(function (chip) {
      chip.setAttribute(
        "aria-pressed",
        chip.getAttribute("data-scheme") === chosen ? "true" : "false"
      );
    });
  }

  // --- the menu behind the hold ---------------------------------------------

  var HOLD_MS = 450;
  var holdTimer = null;
  var longPress = false;

  function openMenu() {
    if (!menu || menu.open) return;
    menu.open = true;
    markChips();
  }

  function closeMenu(refocus) {
    if (!menu || !menu.open) return;
    menu.open = false;
    if (refocus) toggle.focus();
  }

  function cancelHold() {
    clearTimeout(holdTimer);
    holdTimer = null;
  }

  if (menu) {
    toggle.addEventListener("pointerdown", function () {
      longPress = false;
      cancelHold();
      holdTimer = setTimeout(function () {
        longPress = true;
        openMenu();
      }, HOLD_MS);
    });
    ["pointerup", "pointercancel", "pointerleave"].forEach(function (name) {
      toggle.addEventListener(name, cancelHold);
    });

    // Press-and-hold with a mouse is a right-click, and on a phone the
    // callout this would otherwise raise lands on top of the menu.
    toggle.addEventListener("contextmenu", function (event) {
      event.preventDefault();
      cancelHold();
      longPress = false;
      openMenu();
    });

    toggle.addEventListener("keydown", function (event) {
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        openMenu();
        var first = menu.querySelector(".theme-menu__chip, .pack-picker__btn");
        if (first) first.focus();
      } else if (event.key === "Escape") {
        closeMenu();
      }
    });

    menu.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        event.stopPropagation();
        closeMenu(true);
      }
    });

    menu.addEventListener("click", function (event) {
      var chip = event.target.closest("[data-scheme]");
      if (!chip) return;
      applyScheme(chip.getAttribute("data-scheme"));
    });

    document.addEventListener("click", function (event) {
      if (menu.open && !menu.contains(event.target)) closeMenu();
    });

    markChips();
  }

  toggle.addEventListener("click", function (event) {
    // The summary never toggles itself: a plain press is the fast path, and
    // the menu is reached by holding instead.
    event.preventDefault();
    var action = window.ThemeLogic.pressAction({
      open: !!(menu && menu.open),
      longPress: longPress,
    });
    longPress = false;
    cancelHold();
    if (action === "cycle") cycle();
    else if (action === "close") closeMenu();
    else openMenu();
  });
})();
