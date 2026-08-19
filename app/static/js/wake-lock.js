// The screen wake lock behind voice recording (FEATURES.md F47).
//
// A phone left alone dims and locks its screen after twenty or thirty
// seconds, and on Android that takes the microphone with it: the page is
// backgrounded and the recording ends. Someone talking to their child's
// future self is exactly the person who is not tapping the screen every
// half minute, so while a recording runs the app asks the browser to keep
// the screen awake.
//
// Deliberately small and best-effort. The Screen Wake Lock API needs a
// secure context — the same condition getUserMedia already imposes, so
// wherever recording works at all this can be asked for — and it may still
// be refused (battery saver, no support). Nothing here is load-bearing:
// a refusal only means the screen behaves as it always did, which is what
// the recorder's interruption handling is there for.
(function (root) {
  "use strict";

  var sentinel = null;
  // Whether the *app* still wants the screen awake. The browser drops the
  // lock whenever the page is hidden and never gives it back on its own,
  // so this is what tells us to ask again on the way back.
  var wanted = false;

  function isSupported() {
    return !!(root.navigator && root.navigator.wakeLock && root.navigator.wakeLock.request);
  }

  function acquire() {
    if (!isSupported() || sentinel) return Promise.resolve(false);
    if (root.document && root.document.visibilityState !== "visible") {
      return Promise.resolve(false);
    }
    return root.navigator.wakeLock
      .request("screen")
      .then(function (lock) {
        sentinel = lock;
        lock.addEventListener("release", function () {
          if (sentinel === lock) sentinel = null;
        });
        return true;
      })
      .catch(function () {
        return false;
      });
  }

  function request() {
    wanted = true;
    return acquire();
  }

  function release() {
    wanted = false;
    var lock = sentinel;
    sentinel = null;
    if (!lock) return Promise.resolve();
    return Promise.resolve(lock.release()).catch(function () {});
  }

  if (root.document && root.document.addEventListener) {
    root.document.addEventListener("visibilitychange", function () {
      if (wanted && root.document.visibilityState === "visible") acquire();
    });
  }

  root.StorybookWakeLock = {
    isSupported: isSupported,
    isHeld: function () {
      return !!sentinel;
    },
    request: request,
    release: release,
  };
})(typeof window !== "undefined" ? window : this);
