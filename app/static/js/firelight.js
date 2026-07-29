// F44: the ☼ button in the nav — turns the firelight wash off and on and
// remembers the choice. The wash itself is pure CSS (main.css, `.firelight`);
// all this does is set `data-firelight="off"` on the root element, which
// theme-boot.js re-applies before first paint on the next page.
(function () {
  var STORAGE_KEY = "storybook-firelight";
  var root = document.documentElement;
  var toggle = document.getElementById("firelight-toggle");
  if (!toggle) return;

  function isOn() {
    return root.getAttribute("data-firelight") !== "off";
  }

  function render() {
    toggle.setAttribute("aria-pressed", isOn() ? "true" : "false");
  }

  // The button ships without aria-pressed: the page is cached and the choice
  // isn't, so only the DOM knows the real state once theme-boot has run.
  render();

  toggle.addEventListener("click", function () {
    if (isOn()) {
      root.setAttribute("data-firelight", "off");
    } else {
      root.removeAttribute("data-firelight");
    }
    if (window.SafeStorage) {
      window.SafeStorage.setString(STORAGE_KEY, isOn() ? "on" : "off");
    }
    render();
  });
})();
