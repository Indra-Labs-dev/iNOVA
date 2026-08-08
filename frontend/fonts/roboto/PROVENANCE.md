# Vendored dependency: Roboto

**Gate 7** — fixes the Roboto CDN fetch documented in
`docs/16-roadmap/gate-6-3d-spike-report.md` (finding #4): Flutter's CanvasKit renderer
doesn't bundle any font by default, so it fetched Roboto from `fonts.gstatic.com` at
runtime for every page load until this file was vendored.

- **Source**: `https://raw.githubusercontent.com/google/fonts/main/ofl/roboto/Roboto%5Bwdth,wght%5D.ttf`
  (the official `google/fonts` repository, the canonical distribution source for Google
  Fonts, including Roboto).
- **File**: `Roboto[wdth,wght].ttf` — a single variable font (width + weight axes), fetched
  2026-08-08, 488,584 bytes. One file covers every weight/width the app uses instead of
  vendoring a separate static file per weight.
- **License**: SIL Open Font License 1.1 (`OFL.txt` in this directory, copied verbatim from
  the same repository path).
- **Registered as**: the `Roboto` font family in `pubspec.yaml`'s `flutter: fonts:` section.
  No `ThemeData` change was needed — Flutter's Material 3 default `TextTheme` already
  references the `Roboto` family name; providing a local font under that same name is
  enough for the engine to use it instead of asking CanvasKit to fetch it from Google's CDN.
- **Residual gap, not closed by this file**: CanvasKit's `fontFallbackBaseUrl` (default
  `https://fonts.gstatic.com/s/`) is still used for any glyph outside Roboto's own coverage
  (e.g. CJK, emoji, some symbol ranges). The `→`/`…`/`•` glyphs previously used in the app's
  UI copy were the concrete trigger for this and were replaced with ASCII/`Icon` equivalents
  in the same Gate 7 change — see `docs/PROJECT_STATUS.md` "Known gaps" for the ongoing
  discipline this implies (avoid introducing new non-Latin glyphs in UI text without
  checking their font coverage).
