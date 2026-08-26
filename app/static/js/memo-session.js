/* Voice memos on the lock screen (FEATURES.md F56).
 *
 * A memo is a child's actual voice, and the way you listen to one is with
 * the phone in your pocket while you do something else. The moment the
 * screen locks, a plain `<audio>` element becomes a nameless thing playing
 * from "Chrome" with no controls you can reach.
 *
 * `navigator.mediaSession` fixes both halves: the metadata gives the lock
 * screen and the notification shade something to say, and the play/pause
 * transport controls start working from the headphones and the lock button.
 *
 * Deliberately no `setActionHandler` calls. Play, pause and stop are wired
 * to the element for free once metadata is set; seek and next/previous
 * would need handlers, and "next" across a story's memos is a playlist,
 * which is a music-player idea and not a book one.
 *
 * The metadata is set on `play` rather than on load, because a story can
 * hold several memos and the session belongs to whichever one is actually
 * sounding.
 */
(function () {
  "use strict";

  if (!("mediaSession" in navigator) || typeof window.MediaMetadata !== "function") return;

  var root = document.querySelector("[data-memo-session]");
  if (!root) return;

  var book = root.getAttribute("data-memo-session-book") || document.title;
  var story = root.getAttribute("data-memo-session-story") || "";
  var artworkSrc = root.getAttribute("data-memo-session-artwork");
  var artwork = artworkSrc
    ? [{ src: artworkSrc, sizes: "512x512", type: "image/png" }]
    : [];

  root.querySelectorAll("audio").forEach(function (audio) {
    audio.addEventListener("play", function () {
      try {
        navigator.mediaSession.metadata = new window.MediaMetadata({
          // The story is the thing you chose to listen to, so it is the
          // track; the book is the collection it belongs to. A memo has no
          // name of its own — it is `memo-003.webm` — so naming it here
          // would mean inventing one.
          title: story,
          artist: book,
          artwork: artwork,
        });
      } catch (error) {
        // Metadata is decoration. A browser that dislikes the artwork URL
        // or the constructor must not take the audio down with it.
      }
    });
  });
})();
