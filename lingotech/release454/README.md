# LingoTech v4.5.4 — Android in-app save fallback

A screenshot showed an outdated Photo Booth export UI with a large signup panel, a futile direct-share retry, and the user's photo far below the fold. The current v4.5.3 already moved the photo above signup and removed the futile retry. This patch addresses the remaining functional gap and recurrence of stale cached pages without redesigning the product.

**Scope**
- When native file sharing is unsupported in an Android/in-app mobile browser, the existing secondary export button becomes **Download JPG file**. The primary action remains **Full-size image · hold to save**.
- Download requests are not falsely described as successful saving to the user's Photos app. If an in-app browser blocks the download, users can use the browser menu to open in a system browser.
- A same-origin, best-effort release.json check shows a small update prompt only when a newer version is detected. It never automatically reloads or destroys the user's current photo. User-triggered reload uses a one-time query parameter and normalizes the visible URL back to the exact clean canonical URL.
- Native-share-capable browsers keep the original action and UX. Desktop download and all scene/frame/QR assets remain unchanged.
- This **does not retroactively update an already-cached v4.5.2 page**: the visitor must refresh or open in a system browser once.

**Safety / regression**
- Immutable baseline: v4.5.3 SHA-256 `aaf0544eb892b1fbf691280062fac9eef017772332dacd9071618cbad5e38554`.
- The generator refuses unexpected source and verifies all embedded image data is byte-identical.
- Browser tests use synthetic local photos and verify the real downloaded JPEG QR target.
- Tests use Chromium/WebKit with mocked native share, not physical iPhone/Android WeChat. No real form submissions, social posting, uploads, trackers or external data collection.
- Historical v4.5.3 test expectation “no native sharing means hide secondary button” is intentionally superseded by the working JPG fallback; no other assertions should be altered.
- Kimi PR #2 QR/ResizeObserver/alt fixes are **not** included. Review that PR separately against the latest `main`.

Canonical: https://williamlovecs.github.io/lingotech/
Legacy redirect remains at https://williamlovecs.github.io/lingotech-photo-booth/
