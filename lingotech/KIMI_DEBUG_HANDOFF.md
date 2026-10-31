# Kimi Code handoff — LingoTech v4.5.3 bug-only audit

**Owner request (Chinese):** 只做 DEBUG，不改变现在的 UI、主题、相框设计、照片、排版或用户流程；不要重构。先确认问题真实存在，再最小修改，自动化测试，提供 PR 供人工审核。不要直接部署。

## Project goal and user experience

This is a lightweight, bilingual (Chinese/English) **on-site photo booth** for the LingoTech × LingoCorner community. Event visitors enter by QR code, take/select their own photo, apply a branded frame, save/share it, and may optionally follow an event signup link. Generated photo includes an optional branded QR so friends can scan and make their own photo. It is *not* a face-generation/AI portrait app.

Core journey: scan or open canonical URL → local photo input/camera → choose 1 of 3 scenes → 7 original templates → ratio (post 1080×1350, story 1080×1920, landscape 1620×1080) → position/fit/rotate/photo/optional text → preview → save or share → optional event entry. Local photos must never be uploaded.

Audience and event workflow: Photo Booth attracts visitors; a separate LingoCorner/Xiaohongshu group and event signup nurture community; the HICOOL Feishu Cases & Partnerships document and another B2B partnership form handle enterprise leads. **Never mix those QR destinations or forms.**

## Current production status — inspect rather than assume

- Repo: https://github.com/williamlovecs/williamlovecs.github.io
- Production: https://williamlovecs.github.io/lingotech/
- Old URL: https://williamlovecs.github.io/lingotech-photo-booth/ (client-side redirect to production).
- Working baseline at this handoff: main fe83a182381235074cf896d93b9fbb3eaff40ec9; released v4.5.3.
- Production SHA-256 in release.json: aaf0544eb892b1fbf691280062fac9eef017772332dacd9071618cbad5e38554.
- Latest GitHub Pages and public check successful (Actions 41162990730 and 41162991123). Historical deep v4.5.2 audit also succeeded. This is not a guarantee that no bugs exist; verify current repo head again before work.
- No independent custom domain or CNAME requested; "clean URL" refers to the unchanged github.io/lingotech/ path with no query or tracking parameters.

## Architecture map

- Main static app: lingotech/index.html, intentionally single-file HTML/CSS/JS plus inline assets.
- Build/release identity: lingotech/release.json.
- Newest mobile export module: lingotech/release453/mobile-export.js and README.md.
- Current mobile regression: lingotech/release453/test_mobile.py; candidate GitHub Action .github/workflows/lingotech-v453-mobile.yml.
- Earlier deep tests: lingotech/release452/test_deep.py; prior version suites release451/test_extra.py, release45/test_release.py, release43/test_release.py. Be mindful of intentional changes between v4.5.2 and v4.5.3.
- CI public verification: .github/workflows/lingotech-public-check.yml.
- Legacy redirect: lingotech-photo-booth/index.html; historical archives at _archive/lingotech-photo-booth/.
- Separate share diagnostic tool: lingotech/share-debug/index.html.
- **DO NOT RUN lingotech/release453/build.py on current main:** that script is a fail-closed one-time patch and expects the exact older v4.5.2 SHA-256. Use it as history/reference only.

## Intentional behavior that is NOT a bug

- AI creation scene stays relatively clean/technical, while community/culture scenes support more paper decorations. Some style selectors are intentionally absent where decoration is fixed.
- Current product is not yet the proposed v4.6 Cute, Scrapbook or Playful Pop; do not add cat/dog stickers, UI variants or decorative assets.
- On mobile, "save" prioritizes a full-screen image preview and manual album save; it does NOT guarantee an automatic system Photos write. WeChat fallback shows the image/instructions before optional native share. Keep this intact.
- Personal phones do not auto-clear; only explicitly enabled, per-tab shared booth mode has 3-min idle clear and 20-s warning. Manual Done/Next Visitor clears relevant photo/name/cache/camera and resets embedded QR toggle.
- Bilingual automatic language with manual override; optional on-device counter is not cross-device analytics. All photos remain local.
- The embedded QR targets only the canonical Photo Booth site, never directly a short-lived Feishu or Xiaohongshu group QR.
- User photography and HTML-generated photo are not an AI modification of person/face. Original event photos are not to be replaced.

## Known UNVERIFIED areas (do NOT classify as passed)

- Actual iOS/Android WeChat long-press image recognition, save to Photos, file download, share to Moments; privacy/permission differences by device and WeChat version.
- Mainland China network latency/availability to GitHub Pages; no independent China-hosted mirror.
- Unauthenticated Feishu guest document access and confirmed signup form submission.
- Publicity consent for identifiable people in event gallery.
- Screenshot and performance behavior on unsupported/outdated embedded browsers.

## Kimi task sequence

**Stage A — read-only inventory and capture.** Check out debug branch. Confirm HEAD, index SHA, release metadata and modified-file list. Capture baseline screenshot evidence and generate synthetic photo fixtures. Do not touch production code until a bug reproduces.

**Stage B — systematic QA.** Cover:
- Mobile upload incl. rotation/EXIF, file rejection, camera permission denied/late, fast re-selection and clearing; camera full-frame composition.
- Existing three scenes, seven frames, three ratios; canvas text safety, QR quiet zone and decoded destination; QR on JPEG/PNG and compressed 720px share image.
- Stable photo/text and caches after switch of scene/ratio, save, share, cancel, error, retry; no stale or wrong-visitor photo.
- Chinese/English copy and IME/emoji (40 visible graphemes); selected texture controls must actually affect the chosen style.
- Mobile preview-before-save and share fallback under Safari/WebKit/WeChat UA; native share files-only handoff, cancelled, rejected, pending, double tap. Never infer actual social delivery from a mocked Promise.
- Local privacy in per-tab kiosk mode, foreground/background, offscreen save bar/modals on 320px and 375px, 390px, 430px, 768px, 1024px and 1440px.
- Verified mapping and external-open behavior of forms; no fake QR when a custom URL has no matching QR.
- Old path redirect + UTM/index cleanup. No extra network uploads or third-party analytics.

**Stage C — fix only what you can prove.** Issue number, before screenshot/log, failing test, minimum source change, after screenshot/log, regression results. If a fix affects UI pixels outside the bug, flag and stop for review.

**Stage D — evidence and PR.** Run Chromium + WebKit current suite at minimum (release453/test_mobile.py). Run independent matrix checks incl. QR decoder and relevant older tests. Record why a legacy assertion does or does not apply to v4.5.3. Supply a concise bug table, exact test commands, visual diff summary, link mapping, consent and real-device caveats, changed-file list, and PR URL. **Do not merge or deploy.**

## Environment bootstrap (from repository root)

    git checkout debug/lingotech-v453-kimi-fix-only-20261101
    python -m pip install playwright==1.56.0 pillow==11.3.0 opencv-python-headless==4.12.0.88
    python -m playwright install chromium webkit
    python lingotech/release453/test_mobile.py

For WebKit in Windows PowerShell:

    $env:BROWSER="webkit"
    python lingotech/release453/test_mobile.py

Always read lingotech/AGENTS.md first. If a feature appears flawed but cannot be reproduced, report it as a hypothesis, not a confirmed bug.

## Expected report

- **Baseline:** current SHA / version / hash and screenshots.
- **Findings:** P0/P1/P2 confirmed vs. unverified, steps, expected/actual, engines/devices.
- **Fixes:** minimal changed files and why.
- **No-UI-change proof:** screenshot diff for home/editor/all frame families and all critical ratios; clear any justified single-line visual bug fix.
- **Regression:** exact pass/fail totals, QR decodes/destinations, privacy/reset checks, native share simulation vs. real devices.
- **Deliverable:** PR against main and optional CI evidence; **do not change main or public deployment**.
