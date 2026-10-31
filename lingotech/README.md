# LingoTech Photo Booth — current source and debugging entry point

This directory is the **live, public** LingoTech Photo Booth project. It is a small, self-contained GitHub Pages app; do not scaffold a replacement or clone the visual UI.

## Current verified baseline

- Production (clean URL): https://williamlovecs.github.io/lingotech/
- Legacy visitor URL: https://williamlovecs.github.io/lingotech-photo-booth/ — client-side redirect to production (not an HTTP 301).
- Version at handoff: **4.5.3**; immutable baseline Git commit: **fe83a182381235074cf896d93b9fbb3eaff40ec9**.
- Release manifest: lingotech/release.json (SHA-256 of served index.html; version and expected URLs).
- GitHub Pages deployment and public verification for the above commit completed successfully on 2026-10-31 UTC. This proves automation results, **not** physical iPhone/WeChat or Mainland China network usability.
- IMPORTANT: The already existing `main` serves production. Changing it deploys a new public version.

## File map

| Path | Purpose | Safe Kimi treatment |
| --- | --- | --- |
| lingotech/index.html | Actual production HTML, CSS, JS and embedded assets (~1.2 MB) | Read; make minimal, localized bug fixes only on a working branch |
| lingotech/release.json | Version, canonical URL, SHA-256, release contracts | Do not hand-edit during investigation; update only for a fully tested release |
| lingotech/release453/mobile-export.js | Latest intentional mobile save/share behavior | Reference for v4.5.3; do not revert |
| lingotech/release453/test_mobile.py | Current Chromium and WebKit mobile/export regression | Run before and after bug fixes |
| lingotech/release453/build.py | Historical **one-time** exact-hash build from v4.5.2 to v4.5.3 | **Do not run on current main**: intentionally fails if the baseline has changed |
| lingotech/release452/test_deep.py | Prior browser/race/QR matrix regression | Consult and rerun selectively against current behavior; old assertions may require investigation |
| lingotech/release45/test_release.py | Earlier QR and privacy regression | Historical expectations; do not edit assertions merely to force green |
| lingotech/release43/test_release.py | Older original editor regression | Historical reference |
| lingotech/share-debug/index.html | Separate WeChat share compatibility diagnostic page | Do not change or link publicly without request |
| lingotech-photo-booth/index.html | Legacy redirect | Preserve |
| _archive/lingotech-photo-booth/ | Immutable historical releases | Never overwrite |
| .github/workflows/lingotech-v453-mobile.yml | Latest candidate mobile browser CI | Reference when creating targeted tests |
| .github/workflows/lingotech-public-check.yml | Production hash, redirect, export and QR verification | Preserve; future releases must pass |

GitHub Pages and scripts in this repository may also serve **other unrelated projects**. Do not alter repo root, other applications or site routes.

## Approved workflow for Kimi

1. Read **lingotech/AGENTS.md** and **lingotech/KIMI_DEBUG_HANDOFF.md** before modifying anything.
2. Start from the published 4.5.3 main baseline. Work in the separate branch: **debug/lingotech-v453-kimi-fix-only-20261101**.
3. Obtain clean baseline screenshots and use **synthetic** photos. Do not commit user photos, submissions, personal data or tokens.
4. Reproduce each bug, write regression evidence, make the smallest behavior-only change, and rerun tests.
5. Open a PR against main. **No direct pushes or merges to main, no production deployment** without a separate review of test and UI diffs.
6. If no reproducible issue remains, deliver findings without gratuitous source modifications.

## Current testing

From repository root, after installing Python 3 and browser dependencies:

    python -m pip install playwright==1.56.0 pillow==11.3.0 opencv-python-headless==4.12.0.88
    python -m playwright install chromium webkit
    python lingotech/release453/test_mobile.py

For WebKit (PowerShell):

    $env:BROWSER="webkit"
    python lingotech/release453/test_mobile.py

There are also historical tests in release452, release451, release45 and release43. The latest UI semantics take precedence over outdated assertions; identify and document any mismatch rather than weakening coverage.

## Do not confuse outcomes

Browser mocks cannot prove that an iPhone saved to Photos, that WeChat Moments accepted or published an image, that Feishu accepted a guest submission, or that the site is fast/reachable on Mainland networks. Those are separate real-device/guest acceptance steps.
