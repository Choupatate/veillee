// Plain-Node tests for app/static/js/recorder-logic.js — no framework, no
// npm dependency, run via `node tests/js/recorder_logic_test.mjs`. Wired
// into the pytest suite by test_tree_logic_js.py, which skips gracefully
// if node isn't on PATH.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const RecorderLogic = require("../../app/static/js/recorder-logic.js");

let passed = 0;

function check(name, fn) {
  fn();
  passed++;
  console.log("ok -", name);
}

// --- the elapsed clock -------------------------------------------------------

check("a fresh clock has run for no time at all", () => {
  const clock = RecorderLogic.createClock();
  assert.equal(RecorderLogic.elapsed(clock, 1000), 0);
});

check("a running clock counts from the instant it started", () => {
  const clock = RecorderLogic.startClock(5000);
  assert.equal(RecorderLogic.elapsed(clock, 5000), 0);
  assert.equal(RecorderLogic.elapsed(clock, 12000), 7000);
});

check("starting again forgets what an earlier recording banked", () => {
  let clock = RecorderLogic.startClock(0);
  clock = RecorderLogic.pauseClock(clock, 9000);
  clock = RecorderLogic.startClock(50000);
  assert.equal(RecorderLogic.elapsed(clock, 50000), 0);
});

check("a paused clock holds still", () => {
  let clock = RecorderLogic.startClock(1000);
  clock = RecorderLogic.pauseClock(clock, 4000);
  assert.equal(RecorderLogic.elapsed(clock, 4000), 3000);
  assert.equal(RecorderLogic.elapsed(clock, 999999), 3000);
});

check("resuming counts on from what was banked, not from zero", () => {
  let clock = RecorderLogic.startClock(1000);
  clock = RecorderLogic.pauseClock(clock, 4000);
  clock = RecorderLogic.resumeClock(clock, 100000);
  assert.equal(RecorderLogic.elapsed(clock, 102000), 5000);
});

check("pause and resume survive several rounds", () => {
  let clock = RecorderLogic.startClock(0);
  for (let i = 0; i < 4; i++) {
    clock = RecorderLogic.pauseClock(clock, i * 10000 + 1000);
    clock = RecorderLogic.resumeClock(clock, (i + 1) * 10000);
  }
  // Four one-second runs banked, plus whatever the last resume has run for.
  assert.equal(RecorderLogic.elapsed(clock, 40500), 4000 + 500);
});

check("a clock the system time jumped backwards under never runs backwards", () => {
  const clock = RecorderLogic.startClock(10000);
  assert.equal(RecorderLogic.elapsed(clock, 2000), 0);
});

check("transitions never mutate the clock they were handed", () => {
  const clock = RecorderLogic.startClock(1000);
  const before = JSON.stringify(clock);
  RecorderLogic.pauseClock(clock, 9000);
  RecorderLogic.resumeClock(clock, 9000);
  assert.equal(JSON.stringify(clock), before);
});

// --- the timer readout -------------------------------------------------------

check("formatElapsed: zero is a padded mm:ss", () => {
  assert.equal(RecorderLogic.formatElapsed(0), "00:00");
});

check("formatElapsed: seconds are floored, not rounded up", () => {
  assert.equal(RecorderLogic.formatElapsed(1999), "00:01");
});

check("formatElapsed: minutes and seconds are both padded", () => {
  assert.equal(RecorderLogic.formatElapsed(9 * 60000 + 5000), "09:05");
  assert.equal(RecorderLogic.formatElapsed(59 * 60000 + 59000), "59:59");
});

check("formatElapsed: an hour grows an hours field instead of counting to 60:00", () => {
  assert.equal(RecorderLogic.formatElapsed(3600000), "1:00:00");
  assert.equal(RecorderLogic.formatElapsed(3600000 + 62000), "1:01:02");
  assert.equal(RecorderLogic.formatElapsed(11 * 3600000), "11:00:00");
});

check("formatElapsed: a negative reading is shown as zero, not as -1:-1", () => {
  assert.equal(RecorderLogic.formatElapsed(-5000), "00:00");
});

// --- interruptions -----------------------------------------------------------

check("every interruption salvages the audio recorded so far", () => {
  for (const reason of ["hidden", "ended", "muted", "error"]) {
    assert.equal(RecorderLogic.interruption(reason).salvage, true, reason);
  }
});

check("an interruption nobody anticipated is still salvaged", () => {
  const policy = RecorderLogic.interruption("something-new");
  assert.equal(policy.salvage, true);
  assert.equal(policy.message, RecorderLogic.interruption("error").message);
});

check("each reason explains itself differently", () => {
  const messages = ["hidden", "ended", "muted"].map(
    (reason) => RecorderLogic.interruption(reason).message
  );
  assert.equal(new Set(messages).size, 3);
});

check("every message says the recording was kept", () => {
  for (const message of RecorderLogic.interruptionMessages()) {
    assert.match(message, /saved\.$/);
  }
});

check("interruptionMessages lists exactly what interruption can return", () => {
  const listed = new Set(RecorderLogic.interruptionMessages());
  assert.equal(listed.size, 4);
  for (const reason of ["hidden", "ended", "muted", "error"]) {
    assert.ok(listed.has(RecorderLogic.interruption(reason).message), reason);
  }
});

// --- the microphone watchdog -------------------------------------------------

check("a fresh watch has seen no silence", () => {
  const watch = RecorderLogic.createSilenceWatch();
  assert.equal(watch.since, null);
  assert.equal(watch.dead, false);
});

check("a room's noise floor is not silence", () => {
  // -60 dBFS: a quiet room with a live microphone, orders of magnitude
  // above what a switched-off one reports.
  let watch = RecorderLogic.createSilenceWatch();
  for (let t = 0; t <= 60000; t += 1000) {
    watch = RecorderLogic.watchSilence(watch, 0.001, t);
    assert.equal(watch.dead, false, `at ${t}ms`);
  }
});

check("a dead microphone is called dead only after the full run", () => {
  let watch = RecorderLogic.createSilenceWatch();
  watch = RecorderLogic.watchSilence(watch, 0, 1000);
  assert.equal(watch.since, 1000);
  watch = RecorderLogic.watchSilence(watch, 0, 1000 + RecorderLogic.DEAD_MS - 1);
  assert.equal(watch.dead, false);
  watch = RecorderLogic.watchSilence(watch, 0, 1000 + RecorderLogic.DEAD_MS);
  assert.equal(watch.dead, true);
});

check("a long silence is only worth acting on after several seconds", () => {
  // Someone pausing to find their words must never trip it.
  assert.ok(RecorderLogic.DEAD_MS >= 5000);
});

check("one moment of sound resets the run", () => {
  let watch = RecorderLogic.createSilenceWatch();
  watch = RecorderLogic.watchSilence(watch, 0, 0);
  watch = RecorderLogic.watchSilence(watch, 0, RecorderLogic.DEAD_MS - 1);
  watch = RecorderLogic.watchSilence(watch, 0.05, RecorderLogic.DEAD_MS - 1);
  assert.equal(watch.since, null);
  watch = RecorderLogic.watchSilence(watch, 0, RecorderLogic.DEAD_MS);
  assert.equal(watch.dead, false);
  assert.equal(watch.since, RecorderLogic.DEAD_MS);
});

check("the run is timed from the first silent frame, not the first call", () => {
  let watch = RecorderLogic.createSilenceWatch();
  watch = RecorderLogic.watchSilence(watch, 0.2, 0);
  watch = RecorderLogic.watchSilence(watch, 0, 5000);
  watch = RecorderLogic.watchSilence(watch, 0, 5000 + RecorderLogic.DEAD_MS);
  assert.equal(watch.dead, true);
});

// --- the level meter ---------------------------------------------------------

check("meterWidth: silence fills nothing", () => {
  assert.equal(RecorderLogic.meterWidth(0), 0);
  assert.equal(RecorderLogic.meterWidth(-1), 0);
});

check("meterWidth: everything below the floor reads empty", () => {
  assert.equal(RecorderLogic.meterWidth(0.001 / 1000), 0);
});

check("meterWidth: full scale fills the bar and nothing overflows it", () => {
  assert.equal(RecorderLogic.meterWidth(1), 1);
  assert.equal(RecorderLogic.meterWidth(4), 1);
});

check("meterWidth: speech lands in the middle of the bar, not against an end", () => {
  const speech = RecorderLogic.meterWidth(0.05);
  assert.ok(speech > 0.4 && speech < 0.75, String(speech));
});

check("meterWidth: louder always reads longer", () => {
  let last = -1;
  for (const level of [0.002, 0.01, 0.05, 0.2, 0.6, 1]) {
    const width = RecorderLogic.meterWidth(level);
    assert.ok(width > last, String(level));
    last = width;
  }
});

console.log(`\n${passed} passed`);
