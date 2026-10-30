# LingoTech Photo Booth v4.5

## One public application

`https://williamlovecs.github.io/lingotech/` is canonical. The existing `/lingotech-photo-booth/` URL is retained as a client-side redirect with a noscript meta-refresh and ordinary link fallback. This is not an HTTP 301. Existing printed QR codes remain useful. Known legacy version and UTM parameters are discarded.

## Visitor flow

Create a photo without registering. An optional next-event link appears on the home screen, header, editor and export dialog, using the existing verified event form configuration. The business form is not substituted for event signup. Embedded photo QR content remains the canonical Photo Booth URL, with its original quiet zone and opt-out toggle. Original embedded photo assets are byte-for-byte preserved.

## Shared-device mode

Open organizer settings and enable **公用展台模式 / Shared booth mode** only on the shared booth device. Enabling clears the current visitor's image. The mode is per tab, not site-wide. After 3 minutes without interaction, photo/name/camera/export state is cleared. A 20-second warning allows the current visitor to continue. **完成 / 下一位 / Done / Next visitor** clears immediately. Normal personal-phone sessions are not timed out. Clearing the app cannot delete a previously saved file from the device's Downloads or Photos library; staff must manage those separately.

## Language

Browser language selects Chinese or English automatically. A manual choice is remembered locally, except that a kiosk resets to its automatic language for each visitor. Browser storage denial is handled without blocking photo editing.

## Optional local metrics (not site-wide analytics)

Organizer settings can enable daily anonymous action totals for this browser, export them as JSON or clear them. Off by default; no collector, third-party tracker or upload endpoint. No photo, nickname, filename, device identifier or visitor identifier is stored. Counts describe actions, not unique visitors. Signup clicks do not prove completed registrations. Native-share handoff does not prove successful social posting. A cross-device dashboard needs a separately configured analytics receiver and privacy decision; it is not provided by this local counter.

## Build and verification

Run `python lingotech/release45/build.py`, then `python lingotech/release45/test_release.py`. The candidate workflow checks Chromium and WebKit, layout bounds, all frame/scene/ratio/QR combinations, image exports, QR decoding, share mocks, clearing and language behavior. Existing editor regressions also run with an explicit Chinese locale. Candidate assets are committed only after successful tests. Public verification checks each URL's own expected hash, then browser-navigation arrival at the canonical v4.5 application.

Real iPhone/WeChat photo-library saving, native target availability, WeChat long-press recognition and Feishu guest submission still require real-device checks; automated mocks cannot establish those outcomes.
