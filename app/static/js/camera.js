// The in-app camera (FEATURES.md F34): a full-screen overlay that streams
// getUserMedia into a <video>, freezes one frame onto a canvas, and hands
// the caller back a JPEG File — the same shape an <input type="file">
// would give them, so every existing upload path works unchanged.
//
// Shared by the instant page, the story editor and the person editor, so
// the markup is built here rather than copied into three templates.
// Requires a secure context (HTTPS, or localhost in development), exactly
// like the F12 voice recorder: without one `navigator.mediaDevices` is
// undefined, isSupported() is false, and callers keep their camera button
// hidden and their file input as the only way in.
//
//   window.StorybookCamera.isSupported() -> boolean
//   window.StorybookCamera.open()        -> Promise<File|null>
//                                           (null = the user backed out)
(function () {
  "use strict";

  var JPEG_QUALITY = 0.92;

  var active = null;

  function isSupported() {
    return !!(
      window.CameraLogic &&
      navigator.mediaDevices &&
      navigator.mediaDevices.getUserMedia &&
      window.HTMLCanvasElement &&
      HTMLCanvasElement.prototype.toBlob &&
      window.URL &&
      window.URL.createObjectURL
    );
  }

  function element(tag, className) {
    var node = document.createElement(tag);
    node.className = className;
    return node;
  }

  function button(className, label) {
    var node = element("button", className);
    node.type = "button";
    node.textContent = label;
    return node;
  }

  function describeError(error) {
    var name = (error && error.name) || "";
    if (name === "NotAllowedError" || name === "SecurityError") {
      return "Camera access was denied. You can still add a photo from your files.";
    }
    if (name === "NotFoundError" || name === "OverconstrainedError") {
      return "No camera found on this device.";
    }
    if (name === "NotReadableError") {
      return "The camera is busy in another app. Close it and try again.";
    }
    return "Could not start the camera.";
  }

  function toFile(blob, filename) {
    try {
      return new File([blob], filename, { type: "image/jpeg", lastModified: Date.now() });
    } catch (e) {
      // Older Safari has no File constructor; a Blob with a name works
      // everywhere the app uses the result (FormData, createObjectURL).
      blob.name = filename;
      return blob;
    }
  }

  function open(options) {
    if (!isSupported() || active) return Promise.resolve(null);
    var Logic = window.CameraLogic;
    var opts = options || {};

    return new Promise(function (resolve) {
      var facing = opts.facingMode || "environment";
      var stream = null;
      var capturedBlob = null;
      var capturedUrl = null;
      var settled = false;
      var lastFocused = document.activeElement;
      var previousOverflow = document.body.style.overflow;

      var overlay = element("div", "camera");
      overlay.setAttribute("role", "dialog");
      overlay.setAttribute("aria-modal", "true");
      overlay.setAttribute("aria-label", opts.label || "Take a photo");
      overlay.tabIndex = -1;

      var stage = element("div", "camera__stage");
      var video = element("video", "camera__video");
      video.autoplay = true;
      video.muted = true;
      video.playsInline = true;
      video.setAttribute("playsinline", ""); // iOS honours the attribute, not the property
      video.setAttribute("muted", "");
      var still = element("img", "camera__still");
      still.alt = "";
      still.hidden = true;
      stage.appendChild(video);
      stage.appendChild(still);
      overlay.appendChild(stage);

      var message = element("p", "camera__message");
      message.hidden = true;
      overlay.appendChild(message);

      var controls = element("div", "camera__controls");
      var cancelBtn = button("btn camera__btn", "Cancel");
      var flipBtn = button("btn camera__btn", "Flip");
      flipBtn.setAttribute("aria-label", "Switch camera");
      flipBtn.hidden = true;
      var shutterBtn = button("btn btn--primary camera__btn camera__shutter", "Take photo");
      var retakeBtn = button("btn camera__btn", "Retake");
      retakeBtn.hidden = true;
      var useBtn = button("btn btn--primary camera__btn camera__use", "Use photo");
      useBtn.hidden = true;
      controls.appendChild(cancelBtn);
      controls.appendChild(flipBtn);
      controls.appendChild(shutterBtn);
      controls.appendChild(retakeBtn);
      controls.appendChild(useBtn);
      overlay.appendChild(controls);

      function showMessage(text) {
        message.textContent = text || "";
        message.hidden = !text;
      }

      function stopStream() {
        if (stream) {
          stream.getTracks().forEach(function (track) {
            track.stop();
          });
          stream = null;
        }
        video.srcObject = null;
      }

      function maybeShowFlip() {
        if (!navigator.mediaDevices.enumerateDevices) return;
        navigator.mediaDevices
          .enumerateDevices()
          .then(function (devices) {
            var cameras = devices.filter(function (device) {
              return device.kind === "videoinput";
            });
            flipBtn.hidden = cameras.length < 2;
          })
          .catch(function () {});
      }

      function start() {
        showMessage("");
        shutterBtn.disabled = true;
        return navigator.mediaDevices
          .getUserMedia({
            audio: false,
            video: {
              facingMode: { ideal: facing },
              width: { ideal: 1920 },
              height: { ideal: 1920 },
            },
          })
          .then(function (mediaStream) {
            stream = mediaStream;
            video.srcObject = mediaStream;
            video.style.transform = Logic.isMirrored(facing) ? "scaleX(-1)" : "";
            var played = video.play();
            if (played && played.catch) played.catch(function () {});
            shutterBtn.disabled = false;
            maybeShowFlip();
          })
          .catch(function (error) {
            showMessage(describeError(error));
            shutterBtn.hidden = true;
            flipBtn.hidden = true;
          });
      }

      function capture() {
        var size = Logic.captureSize(video.videoWidth, video.videoHeight);
        if (!size) {
          showMessage("The camera isn't ready yet — try again in a moment.");
          return;
        }
        var canvas = document.createElement("canvas");
        canvas.width = size.width;
        canvas.height = size.height;
        // Drawn from the raw frame, so a selfie is saved the way everyone
        // else sees it even though the preview above was mirrored.
        canvas.getContext("2d").drawImage(video, 0, 0, size.width, size.height);
        shutterBtn.disabled = true;
        canvas.toBlob(
          function (blob) {
            shutterBtn.disabled = false;
            if (!blob) {
              showMessage("Could not take that photo. Try again.");
              return;
            }
            showCaptured(blob);
          },
          "image/jpeg",
          JPEG_QUALITY
        );
      }

      function showCaptured(blob) {
        capturedBlob = blob;
        capturedUrl = URL.createObjectURL(blob);
        still.src = capturedUrl;
        still.hidden = false;
        video.hidden = true;
        shutterBtn.hidden = true;
        flipBtn.hidden = true;
        retakeBtn.hidden = false;
        useBtn.hidden = false;
        useBtn.focus();
      }

      function retake() {
        if (capturedUrl) {
          URL.revokeObjectURL(capturedUrl);
          capturedUrl = null;
        }
        capturedBlob = null;
        still.hidden = true;
        still.removeAttribute("src");
        video.hidden = false;
        retakeBtn.hidden = true;
        useBtn.hidden = true;
        shutterBtn.hidden = false;
        shutterBtn.focus();
        maybeShowFlip();
      }

      function flip() {
        facing = Logic.nextFacingMode(facing);
        stopStream();
        start();
      }

      function settle(result, viaPopstate) {
        if (settled) return;
        settled = true;
        stopStream();
        if (capturedUrl) {
          URL.revokeObjectURL(capturedUrl);
          capturedUrl = null;
        }
        document.removeEventListener("keydown", onKeydown, true);
        window.removeEventListener("popstate", onPopstate);
        overlay.remove();
        document.body.style.overflow = previousOverflow;
        active = null;
        if (lastFocused && lastFocused.focus) lastFocused.focus();
        // Mirrors the F7 lightbox: opening pushed a history entry so the
        // phone's back gesture closes the camera instead of the page.
        if (!viaPopstate) history.back();
        resolve(result);
      }

      function onKeydown(event) {
        if (event.key !== "Escape") return;
        event.stopPropagation();
        settle(null, false);
      }

      function onPopstate() {
        settle(null, true);
      }

      cancelBtn.addEventListener("click", function () {
        settle(null, false);
      });
      flipBtn.addEventListener("click", flip);
      shutterBtn.addEventListener("click", capture);
      retakeBtn.addEventListener("click", retake);
      useBtn.addEventListener("click", function () {
        if (!capturedBlob) return;
        settle(toFile(capturedBlob, Logic.captureFilename()), false);
      });

      document.addEventListener("keydown", onKeydown, true);
      window.addEventListener("popstate", onPopstate);

      document.body.appendChild(overlay);
      document.body.style.overflow = "hidden";
      overlay.focus();
      history.pushState({ storybookCamera: true }, "");
      active = overlay;
      start();
    });
  }

  window.StorybookCamera = { isSupported: isSupported, open: open };
})();
