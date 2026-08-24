# Vendored: Toast UI Editor 3.2.2

Upstream: https://github.com/nhn/tui.editor — MIT licensed, Copyright (c) 2020
NHN Cloud Corp. The full licence text is in `LICENSE` next to this file.

- `toastui-editor-all.min.js` — a standalone browser bundle built from the
  official npm package with esbuild, because the upstream `-all` CDN bundle is
  not published on npm. The rebuild command is recorded in the file's own banner
  comment:
  `npm i @toast-ui/editor@3.2.2 esbuild && esbuild entry.js --bundle --minify --format=iife`
  with `entry.js` being
  `import Editor from '@toast-ui/editor'; window.toastui = { Editor }`.
- `toastui-editor.min.css` — the editor's stylesheet, same version (3.2.2).
- `theme/toastui-editor-dark.css` — the official dark theme, same version, used
  by the app's dark and manuscript themes. **A licence banner was added locally
  below its `@charset` line**; upstream ships this one file without one, and the
  MIT licence asks for the notice to travel with the copy. It is the only local
  edit to any file in this folder — re-add it if this file is ever re-vendored.

## Network behaviour

The editor ships an opt-out usage-statistics ping (a request to Google Analytics
on instantiation). The app disables it explicitly by passing
`usageStatistics: false` when constructing the Editor — see
`app/static/js/editor.js`. **Never re-enable it**: "no runtime network
dependencies" is a project rule, not a preference (see `CLAUDE.md`).

## Styling

Toast UI's own class names may be styled in exactly one place,
`app/static/css/editor-theme.css`, which re-dresses the editor in the app's
theme variables (F44). Do not add its selectors anywhere else, and do not edit
the vendored stylesheets to restyle anything — `tests/test_editor_theme.py`
enforces the two rules that keep that sheet working.

## Upgrading

Do not upgrade casually. If an upgrade is ever needed: rebuild with the command
above, re-check that `usageStatistics: false` is still honoured by the new
version, re-run the no-network audit (grep the new bundle for
`fetch`/`XMLHttpRequest`/`sendBeacon` and for hardcoded `https://` URLs),
re-add the dark theme's licence banner, and update the version numbers here and
in each file's banner before replacing anything.
