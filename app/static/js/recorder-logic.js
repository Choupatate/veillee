// Pure, DOM-free helpers behind the voice recorder (FEATURES.md F12, F47):
// the pause-aware elapsed clock and the policy that decides what to do
// when something interrupts a recording. Kept out of editor.js so it can
// be unit-tested under plain Node (tests/js/recorder_logic_test.mjs)
// without a browser, a microphone, or a phone whose screen can be locked.
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.RecorderLogic = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // --- the elapsed clock ----------------------------------------------------
  //
  // A recording's length is "however long it has been running", which pause
  // and resume interrupt. Held as a plain value (milliseconds already banked
  // plus the instant the current run began) so every transition is a
  // function of the old clock and the current time, not a mutation.

  function createClock() {
    return { startedAt: null, banked: 0 };
  }

  function startClock(now) {
    return { startedAt: now, banked: 0 };
  }

  function pauseClock(clock, now) {
    return { startedAt: null, banked: elapsed(clock, now) };
  }

  function resumeClock(clock, now) {
    return { startedAt: now, banked: clock.banked };
  }

  function elapsed(clock, now) {
    if (!clock) return 0;
    if (clock.startedAt === null) return clock.banked;
    // A clock the system time has jumped backwards under must never run
    // backwards on screen.
    return clock.banked + Math.max(0, now - clock.startedAt);
  }

  // mm:ss, growing an hours field rather than counting to "83:20" — memos
  // have no length cap, so an hour is reachable.
  function formatElapsed(ms) {
    var total = Math.max(0, Math.floor(ms / 1000));
    var seconds = total % 60;
    var minutes = Math.floor(total / 60) % 60;
    var hours = Math.floor(total / 3600);
    var out = pad(minutes) + ":" + pad(seconds);
    return hours ? hours + ":" + out : out;
  }

  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }

  // --- interruptions --------------------------------------------------------
  //
  // A phone whose screen locks mid-recording takes the microphone away, and
  // a MediaRecorder's audio only exists in the page until it is stopped and
  // uploaded — so an interruption that is ignored is minutes of someone's
  // voice thrown away. Every one of them therefore ends the recording *on
  // purpose*, which hands us the audio so far, and says so afterwards.
  //
  // Reasons, all of them observed rather than guessed at:
  //   "hidden"      the page went to the background (screen lock, app switch)
  //   "ended"       the microphone track ended (device gone, taken by an app)
  //   "muted"       the track went silent — recording on would bank silence
  //   "error"       MediaRecorder itself gave up
  var REASONS = {
    hidden: "Recording stopped when the page went to the background. "
      + "Everything recorded up to then has been saved.",
    ended: "Recording stopped when the microphone became unavailable. "
      + "Everything recorded up to then has been saved.",
    muted: "Recording stopped when the microphone went silent. "
      + "Everything recorded up to then has been saved.",
    error: "The recording was interrupted. "
      + "Everything recorded up to then has been saved.",
  };

  // --- is the microphone still alive? --------------------------------------
  //
  // The failure this was written for: a phone locks its screen, the
  // microphone stops delivering sound, and MediaRecorder carries on
  // banking silence. Nothing errors, nothing stops, and the recording
  // looks healthy right up until you play back two minutes of nothing.
  //
  // A live microphone in a silent room is never mathematically silent —
  // room tone, breathing and the preamp's own noise put its level orders
  // of magnitude above this. A microphone the phone has switched off is
  // zero.
  //
  // The run is long on purpose. Some phones gate their noise suppressor
  // all the way to zero between words, so the two mistakes are not equal:
  // ending a good recording early is a rude surprise, while missing a dead
  // microphone only falls through to the interruptions above, which catch
  // the screen-lock case anyway. Twenty unbroken seconds of exact zero,
  // with the level meter visible the whole time, is the price of acting.
  var DEAD_LEVEL = 0.0002;
  var DEAD_MS = 20000;

  function createSilenceWatch() {
    return { since: null, dead: false };
  }

  // `level` is the RMS amplitude of the last analysis frame, 0..1.
  function watchSilence(watch, level, now) {
    if (level > DEAD_LEVEL) return { since: null, dead: false };
    var since = watch && watch.since !== null ? watch.since : now;
    return { since: since, dead: now - since >= DEAD_MS };
  }

  // Where the level meter's bar should reach, 0..1. Linear amplitude spends
  // most of its range on sounds nobody can hear, so this is decibels: the
  // quietest speech worth showing at the bottom, a shout at the top.
  var METER_FLOOR_DB = -60;

  function meterWidth(level) {
    if (!(level > 0)) return 0;
    var db = 20 * Math.log10(level);
    if (db <= METER_FLOOR_DB) return 0;
    return Math.min(1, db / -METER_FLOOR_DB + 1);
  }

  function interruption(reason) {
    return { salvage: true, message: REASONS[reason] || REASONS.error };
  }

  // Every message `interruption` can return, so the translation table can be
  // checked for holes without reaching into the map.
  function interruptionMessages() {
    return Object.keys(REASONS).map(function (key) {
      return REASONS[key];
    });
  }

  return {
    createClock: createClock,
    startClock: startClock,
    pauseClock: pauseClock,
    resumeClock: resumeClock,
    elapsed: elapsed,
    formatElapsed: formatElapsed,
    interruption: interruption,
    createSilenceWatch: createSilenceWatch,
    watchSilence: watchSilence,
    meterWidth: meterWidth,
    DEAD_MS: DEAD_MS,
    interruptionMessages: interruptionMessages,
  };
});
