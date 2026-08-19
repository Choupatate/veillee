// Plain-Node tests for app/static/js/wake-lock.js (FEATURES.md F47).
//
// The module talks to nothing but `navigator.wakeLock` and two properties
// of `document`, so a hand-written fake window is enough to drive it —
// including the case that matters most and that no unit test in a real
// browser can stage on demand: the browser silently dropping the lock when
// the page is hidden, and the page having to ask again on the way back.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const requests = [];
let refuse = false;
let held = null;

function makeSentinel(type) {
  const sentinel = {
    type: type,
    released: 0,
    onrelease: null,
    addEventListener(name, fn) {
      if (name === "release") sentinel.onrelease = fn;
    },
    release() {
      sentinel.released++;
      return Promise.resolve();
    },
  };
  return sentinel;
}

const listeners = {};
const fakeWindow = {
  navigator: {
    wakeLock: {
      request(type) {
        requests.push(type);
        if (refuse) return Promise.reject(new Error("refused"));
        held = makeSentinel(type);
        return Promise.resolve(held);
      },
    },
  },
  document: {
    visibilityState: "visible",
    addEventListener(name, fn) {
      listeners[name] = fn;
    },
  },
};

globalThis.window = fakeWindow;
const require = createRequire(import.meta.url);
require("../../app/static/js/wake-lock.js");
const WakeLock = fakeWindow.StorybookWakeLock;

let passed = 0;

async function check(name, fn) {
  await fn();
  passed++;
  console.log("ok -", name);
}

await check("it installs itself on the window", () => {
  assert.equal(typeof WakeLock.request, "function");
  assert.equal(WakeLock.isSupported(), true);
  assert.equal(WakeLock.isHeld(), false);
});

await check("a request asks for the screen and is held onto", async () => {
  assert.equal(await WakeLock.request(), true);
  assert.deepEqual(requests, ["screen"]);
  assert.equal(WakeLock.isHeld(), true);
});

await check("asking again while holding one does not ask the browser twice", async () => {
  assert.equal(await WakeLock.request(), false);
  assert.deepEqual(requests, ["screen"]);
  assert.equal(WakeLock.isHeld(), true);
});

await check("coming back to a page that already holds one asks for nothing", async () => {
  await listeners.visibilitychange();
  assert.deepEqual(requests, ["screen"]);
});

await check("a lock the browser drops is asked for again on the way back", async () => {
  // What a phone does when its screen locks: the page is hidden and the
  // lock is released underneath us, with nothing asking for it again.
  const dropped = held;
  fakeWindow.document.visibilityState = "hidden";
  dropped.onrelease();
  assert.equal(WakeLock.isHeld(), false);

  // Hidden is the wrong moment to ask — the browser would refuse anyway.
  await listeners.visibilitychange();
  assert.deepEqual(requests, ["screen"]);

  fakeWindow.document.visibilityState = "visible";
  await listeners.visibilitychange();
  assert.deepEqual(requests, ["screen", "screen"]);
  assert.equal(WakeLock.isHeld(), true);
});

await check("releasing releases the browser's lock too", async () => {
  const current = held;
  await WakeLock.release();
  assert.equal(current.released, 1);
  assert.equal(WakeLock.isHeld(), false);
});

await check("once released, returning to the page does not take the screen back", async () => {
  const before = requests.length;
  await listeners.visibilitychange();
  assert.equal(requests.length, before);
});

await check("releasing when nothing is held is harmless", async () => {
  await WakeLock.release();
  assert.equal(WakeLock.isHeld(), false);
});

await check("a request made while the page is hidden asks for nothing", async () => {
  const before = requests.length;
  fakeWindow.document.visibilityState = "hidden";
  assert.equal(await WakeLock.request(), false);
  assert.equal(requests.length, before);
  fakeWindow.document.visibilityState = "visible";
  // ...but it is still wanted, so the way back takes the screen.
  await listeners.visibilitychange();
  assert.equal(requests.length, before + 1);
  await WakeLock.release();
});

await check("a browser that refuses the lock resolves false rather than throwing", async () => {
  refuse = true;
  assert.equal(await WakeLock.request(), false);
  assert.equal(WakeLock.isHeld(), false);
  refuse = false;
  await WakeLock.release();
});

await check("a browser without the API is simply unsupported", async () => {
  const api = fakeWindow.navigator.wakeLock;
  delete fakeWindow.navigator.wakeLock;
  assert.equal(WakeLock.isSupported(), false);
  assert.equal(await WakeLock.request(), false);
  assert.equal(WakeLock.isHeld(), false);
  await WakeLock.release();
  fakeWindow.navigator.wakeLock = api;
});

console.log(`\n${passed} passed`);
