const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

// Loads getMoonSign/getMoonEclipticLongitude/ZODIAC_SIGNS straight out of
// index.html's plain-JS prelude (everything before the first JSX-bearing
// component), so the test exercises the actual shipped code rather than a
// copy that could drift from it.
function loadMoonFunctions() {
  const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
  const scriptMatch = html.match(/<script type="text\/babel"[^>]*>([\s\S]*?)<\/script>/);
  assert.ok(scriptMatch, "could not find the Babel script block in index.html");
  const source = scriptMatch[1];
  const boundary = source.indexOf("function ApiKeyBanner");
  assert.notEqual(boundary, -1, "could not find the plain-JS/JSX boundary in index.html");
  const plainJs = source.slice(0, boundary);
  const factory = new Function(
    "React",
    plainJs + "\nreturn { getMoonSign, getMoonEclipticLongitude, ZODIAC_SIGNS };"
  );
  return factory({}); // stub: this slice only destructures hooks off React, never calls them
}

const { getMoonSign, getMoonEclipticLongitude, ZODIAC_SIGNS } = loadMoonFunctions();

test("known new moon (2000-01-06T18:14Z) lands in Capricorne near 285°", () => {
  const date = new Date("2000-01-06T18:14:00Z");
  const lon = getMoonEclipticLongitude(date);
  assert.ok(lon > 280 && lon < 290, `expected ~285°, got ${lon}`);
  assert.equal(getMoonSign(date), "Capricorne");
});

test("ecliptic longitude is always normalized to [0, 360)", () => {
  for (let i = 0; i < 50; i++) {
    const date = new Date(Date.now() - i * 13 * 86400000);
    const lon = getMoonEclipticLongitude(date);
    assert.ok(lon >= 0 && lon < 360, `longitude ${lon} out of range for ${date.toISOString()}`);
  }
});

test("getMoonSign always returns one of the 12 known zodiac signs", () => {
  for (let i = 0; i < 400; i++) {
    const date = new Date(Date.now() + i * 86400000);
    const sign = getMoonSign(date);
    assert.ok(ZODIAC_SIGNS.includes(sign), `unexpected sign "${sign}" for ${date.toISOString()}`);
  }
});

test("moon sign cycles through close to all 12 signs over one sidereal month (~27.3 days)", () => {
  const seen = new Set();
  const start = new Date("2026-01-01T00:00:00Z");
  for (let i = 0; i < 30; i++) {
    seen.add(getMoonSign(new Date(start.getTime() + i * 86400000)));
  }
  assert.ok(seen.size >= 11, `expected ~12 distinct signs over 30 days, got ${seen.size}: ${[...seen]}`);
});
