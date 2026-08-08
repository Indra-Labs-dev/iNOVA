# Vendored dependency: three.js

**Gate 6 spike only** — not part of the shipped application. See
`docs/16-roadmap/gate-6-3d-spike-report.md` for context.

- **Source**: `https://registry.npmjs.org/three/-/three-0.180.0.tgz` (official npm registry
  publish of the `three` package, maintained by the three.js/mrdoob organization).
- **Version**: `0.180.0`, fetched via `npm pack three@0.180.0` on 2026-08-08.
- **Files**: `build/three.module.min.js` **and** `build/three.core.min.js` from that
  package, both copied verbatim — not modified, not re-minified, not re-bundled.
  `three.module.min.js` has an internal ES module import of `./three.core.min.js`
  (three.js's 0.180.0 build splits core math/object code into a separate chunk);
  both files are required together, discovered by a real 404 during dev-mode
  testing (Flutter's dev server serves a 200/text SPA fallback for unknown paths
  instead of a 404, which made the missing file harder to spot than a normal
  404 would have been — see the Gate 6 report for the full finding).
- **License**: MIT (`LICENSE` in this directory, copied verbatim from the same package).
- **Why vendored, not CDN**: the Gate 6 GO instructions require the spike to run
  without any external CDN/script/third-party service, and to work offline once
  installed. This file is served as a static asset from `frontend/web/spike3d/`,
  which Flutter's web build copies into `build/web/` as-is — no network fetch of
  this file happens at runtime beyond the same-origin request the browser makes
  for it as an ordinary static asset.
- **Not added as a pub package**: `three` is a JavaScript library, not a Dart/Flutter
  package — there is no `pub.dev` equivalent to add to `pubspec.yaml`. Vendoring the
  built JS file directly is the standard way to use a JS library from Flutter web.
