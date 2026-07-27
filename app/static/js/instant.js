(function () {
  var form = document.getElementById("instant-form");
  var photoInput = document.getElementById("instant-photo");
  var photoPicker = document.getElementById("instant-photo-picker");
  var photoPreview = document.getElementById("instant-photo-preview");
  var cameraButton = document.getElementById("instant-camera");
  var lineInput = document.getElementById("instant-line");
  var dateInput = document.getElementById("instant-date");
  var saveButton = document.getElementById("instant-save");
  var spinner = document.getElementById("instant-spinner");

  var authorsRoot = document.getElementById("editor-authors");
  var authorChipsController = window.StorybookAuthorChips.init(authorsRoot);
  // Who this instant is kept to (F40) — absent when no groups exist.
  var audiencePicker = window.createAudiencePicker
    ? window.createAudiencePicker(document.getElementById("editor-audience"))
    : null;

  var previewUrl = null;
  // A photo taken with the in-app camera (F34). The two sources are
  // exclusive: picking a file clears the capture and vice versa, so the
  // preview and the save always agree on which photo is "the" photo.
  var capturedFile = null;

  function showPhoto(file) {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      previewUrl = null;
    }
    if (file) {
      previewUrl = URL.createObjectURL(file);
      photoPreview.src = previewUrl;
      photoPreview.hidden = false;
      photoPicker.classList.add("has-photo");
    } else {
      photoPreview.hidden = true;
      photoPreview.removeAttribute("src");
      photoPicker.classList.remove("has-photo");
    }
  }

  photoInput.addEventListener("change", function () {
    capturedFile = null;
    showPhoto(photoInput.files[0]);
  });

  if (cameraButton && window.StorybookCamera && window.StorybookCamera.isSupported()) {
    cameraButton.hidden = false;
    cameraButton.addEventListener("click", function () {
      window.StorybookCamera.open().then(function (file) {
        if (!file) return;
        capturedFile = file;
        photoInput.value = "";
        showPhoto(file);
      });
    });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var file = capturedFile || photoInput.files[0];
    if (!file) {
      window.alert("Please choose a photo.");
      return;
    }

    var line = lineInput.value.trim();
    var storyDate = dateInput.value;
    var author = authorChipsController.getSelected() || "";
    // Only sent on the create below; the follow-up PUT that attaches the
    // cover omits it, and an absent `audience` means "leave unchanged".
    var audience = audiencePicker ? audiencePicker.getSelected() : [];

    saveButton.disabled = true;
    if (spinner) spinner.hidden = false;

    fetch("/api/stories", window.CsrfFetch.withToken({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: line,
        date: storyDate,
        markdown: line,
        kind: "instant",
        author: author,
        audience: audience,
      }),
    }))
      .then(window.FetchJson.parse)
      .then(function (created) {
        var formData = new FormData();
        formData.append("file", file, file.name || "camera.jpg");
        return fetch("/api/stories/" + created.id + "/images", window.CsrfFetch.withToken({
          method: "POST",
          body: formData,
        }))
          .then(window.FetchJson.parse)
          .then(function (uploaded) {
            return fetch("/api/stories/" + created.id, window.CsrfFetch.withToken({
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                title: created.title,
                date: storyDate,
                markdown: line,
                cover: uploaded.filename,
                author: author,
              }),
            })).then(window.FetchJson.parse);
          });
      })
      .then(function () {
        window.location.href = "/";
      })
      .catch(function (error) {
        saveButton.disabled = false;
        if (spinner) spinner.hidden = true;
        window.alert(
          (error && error.message) ||
            "Could not save your instant. Please check your connection and try again."
        );
      });
  });
})();
