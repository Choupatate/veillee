// The "who can see this" chip row (FEATURES.md F40 Phase 2), shared by the
// story editor and the instant composer. UMD-ish: exposes a factory on
// window rather than owning any page's wiring, so both callers decide when
// to build it and what to do when it changes.
//
// The state line is the reason this is a module rather than three lines
// inline. "No chips lit" means everyone, and a picker where the default is
// invisible is one where somebody eventually writes something private into
// a story the whole family can read. So the current audience is always
// spelled out in words underneath, in every state.
(function () {
  function t(text) {
    return window.storybookT ? window.storybookT(text) : text;
  }

  window.createAudiencePicker = function (root, onChange) {
    if (!root) return null;
    var chips = Array.prototype.slice.call(
      root.querySelectorAll("[data-group-slug]")
    );
    var stateEl = root.querySelector(".editor__audience-state");

    function getSelected() {
      return chips
        .filter(function (chip) {
          return chip.getAttribute("aria-pressed") === "true";
        })
        .map(function (chip) {
          return chip.dataset.groupSlug;
        });
    }

    function selectedNames() {
      return chips
        .filter(function (chip) {
          return chip.getAttribute("aria-pressed") === "true";
        })
        .map(function (chip) {
          return chip.dataset.groupName;
        });
    }

    function renderState() {
      if (!stateEl) return;
      var names = selectedNames();
      if (!names.length) {
        stateEl.textContent = t("Everyone");
        stateEl.classList.remove("editor__audience-state--scoped");
      } else {
        stateEl.textContent = t("Only {names}").replace("{names}", names.join(", "));
        stateEl.classList.add("editor__audience-state--scoped");
      }
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var pressed = chip.getAttribute("aria-pressed") === "true";
        chip.setAttribute("aria-pressed", pressed ? "false" : "true");
        renderState();
        if (onChange) onChange();
      });
    });

    renderState();
    return { getSelected: getSelected };
  };
})();
