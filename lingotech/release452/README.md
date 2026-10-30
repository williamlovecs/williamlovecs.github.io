# v4.5.2 deep audit

Bug-fix release on exact v4.5.1. Public canonical remains https://williamlovecs.github.io/lingotech/ and the legacy path redirects. No trackers, photo uploads, external fonts, new participant photos, or new cute-style templates.

The CI runs focused new probes on the unchanged baseline, records failures as evidence, builds a deterministic patch, then requires patched tests and previous editor/camera/QR regressions to pass. Native sharing and delayed permissions use explicit mocks, except for the existing Chromium synthetic-camera capture test. Real iPhone/WeChat delivery and Feishu submissions are NOT certified by these tests.

Repairs cover blank form URLs, misleading texture controls, repeated form DOM replacement, Unicode/IME input, stalled native-share recovery, export retry, canonical index/query cleanup and dynamic mobile action-bar spacing. Existing image bytes and QR payloads are asserted unchanged.

Run: `python lingotech/release452/test_deep.py --baseline`, `python lingotech/release452/build.py`, then `python lingotech/release452/test_deep.py`. Baseline is informational; patched failures block the candidate asset commit. No automatic promotion to main.
