# LingoTech — constrained bug-fixing agent rules

**Scope: BUGFIX ONLY. The production UI/UX is frozen.**

This file is written for Kimi Code or another coding agent. The user wants robustness improvements, **not** a redesign, a rebrand, a new framework, or additional decorative templates.

## Mandatory starting point

- Current production: v4.5.3 at https://williamlovecs.github.io/lingotech/
- Base Git commit: fe83a182381235074cf896d93b9fbb3eaff40ec9
- Read README.md, KIMI_DEBUG_HANDOFF.md, release.json and release453/README.md.
- Work only in debug/lingotech-v453-kimi-fix-only-20261101. Never push to main.
- Start by verifying the checked-out commit and current branch. Stop and rebase/reconcile if the base changes.

## Hard invariants — DO NOT CHANGE

1. Visual design: typography, fonts, sizes, colors, gradients, spacing, layout, breakpoints, component order, buttons, modal styling, background textures, animations, photos, icons and bilingual visual hierarchy. **No UI reconstruction.**
2. Scenes/frames: 3 scenes (AI creation, community/friends, culture/play), 7 current templates, 3 ratios, their exact design appearance, text placement, thumbnail styling, memory strip behavior. The absence of playful texture controls in AI co-creation is **intentional**.
3. Identity/assets: original LingoTech/LingoCorner logo and actual event photos. No AI-redrawn people; no swapping, cropping/replacing stock photos or changing encoded embedded assets.
4. QR/URLs: photo's QR resolves to exactly https://williamlovecs.github.io/lingotech/. Preserve QR quiet zone, readability, opt-out toggle, legacy redirect and clean URL (no UTM/version parameters).
5. Conversion mapping: event signup and B2B partnership destinations are distinct. Do not redirect one to the other; do not invent a new membership promise or alter Feishu settings.
6. Privacy: photos stay on-device; no upload or remote photo processing, no analytics beacons, no external scripts/fonts; local anonymous action counting remains off by default. Shared-booth clears photo/name/camera/export buffers, never leaks previous visitor data.
7. Latest mobile save/share design (v4.5.3): on mobile, saving shows an image preview first, not an automatic browser download; in WeChat show the image and album instructions first, then optional native share. Preserve full-size image viewer and non-destructive share recovery. Do not revert to v4.5.2 logic.
8. No new design directions: don't add Cute/cat/dog sticker packs, scrapbook, playful-pop templates, new UI themes, or any feature not expressly approved.
9. Do not modify other projects, root Pages configuration, or old archives.

## Allowed

- Fix reproduced JavaScript logic errors, race conditions, privacy/stale-data behavior, broken media fallbacks, QR mapping, unexpected file errors, form safety, accessibility bugs.
- Add or improve automated tests, using synthetic inputs and stable screenshots.
- Make an absolutely necessary one-line style adjustment only if a proven rendering bug cannot be fixed otherwise. Capture before/after, describe the exact visible change, and ask for review; otherwise zero visible UI delta.
- Add a concise changelog/PR explanation.

## Process and acceptance

**Never say "tested" without listing the actual engine/device and method.**

1. Inventory source version and constraints, then capture baseline screenshots on current main before edits: 320/375/390/430/768/1024/1440 widths; Chinese and English; home, editor, modal, sharing fallback; 3 ratios and relevant scene options.
2. File a numbered defect report: reproduction steps, expected vs. actual, impact, screenshot/log, priority and whether confirmed or conjectural.
3. For each confirmed bug, write a failing test or reliable reproduction first. Apply **minimum diff**. No broad refactors, dependency upgrades or CSS cleanups.
4. Compare same-engine baseline and fixed screenshots/canvas pixel outputs. Unrelated UI must remain visually the same; account only for dynamic data and rasterization noise. Investigate every unexpected difference.
5. Run v4.5.3 mobile tests in Chromium and WebKit; then compatible prior editor, QR/privacy, full-frame camera, and accessibility regressions. Do not simply remove failing assertions.
6. Stress async transitions: rapid photo replacement, clearing during encode/share, camera denial/late grant, background/foreground, screen rotation, HEIC/EXIF orientation if supported, repeated open/close, 40-grapheme input with Chinese IME/emoji, 720px JPEG QR scanning.
7. No network requests or persistent storage of sensitive photos. No app/QR redirect drift. For real iPhone/Android WeChat, state NOT TESTED until a human tests on physical devices.
8. PR must include changed files, reproducible defects, exact commands + results, screenshots/diff summary, QR checks, privacy checks, known limitations, rollback commit. If it needs even a noticeable UI change, request approval instead of merging.

## Forbidden

- Pushing/merging to main; changing live deployment, paid services, forms or permissions.
- Replacing site with React/Next.js, changing its layout, or rebuilding the photo editor.
- Editing tests to hide failures, introducing fake buttons, hardcoding mock results as real results.
- Uploading real customer/event photos as test fixtures, leaking credentials in commits.
- Claiming simulated native-share API resolves proves a WeChat delivery or successful saved image.

If no reproducible bugs remain, stop and report a clean audit. Do not create change for the sake of activity.
