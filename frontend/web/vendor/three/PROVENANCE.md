# Vendored dependency: three.js

**Gate 7** — this is the permanent copy used by the real `features/world/` screen. It is a
verbatim copy of the same files vendored for the Gate 6 spike
(`frontend/web/spike3d/vendor/three/`); duplicated here (not shared/symlinked) so the spike
directory stays fully isolated and deletable on its own, per the Gate 6 GO instructions,
independent of whether the real 3D World is later expanded or removed.

- **Source**: `https://registry.npmjs.org/three/-/three-0.180.0.tgz` (official npm registry
  publish of the `three` package, maintained by the three.js/mrdoob organization).
- **Version**: `0.180.0`.
- **Files**: `build/three.module.min.js` **and** `build/three.core.min.js` from that package,
  copied verbatim — not modified, not re-minified, not re-bundled. `three.module.min.js` has an
  internal ES module import of `./three.core.min.js`; both files are required together (see the
  Gate 6 spike's `vendor/three/PROVENANCE.md` for how this was discovered).
- **License**: MIT (`LICENSE` in this directory, copied verbatim from the same package).
- **Why vendored, not CDN**: same "no external CDN" requirement that applies to the whole app —
  see the Gate 7 CanvasKit/font fix (`docs/PROJECT_STATUS.md` "Known gaps") for the broader
  context.
- **Not added as a pub package**: `three` is a JavaScript library, not a Dart/Flutter package —
  vendoring the built JS file directly is the standard way to use a JS library from Flutter web.
