# LingoTech v4.5.3 — mobile save / share

Scope: only LingoTech export flow. No change to other sites, signup destinations, templates, QR destination or photo storage policy. No image upload, server image storage or analytics collector.

Baseline: main commit `65777d736274af6bea9339839814fd6174d115b0`; index SHA-256 `53fcdcbfd6ca0db54d4c427ca713826c6af7b2e539b1f70472576d480396392f`.

Reproduced on desktop Chromium with mobile viewport / user-agent and explicitly mocked native share: Save automatically downloaded a file outside WeChat; cancelled shares had no image preview; an unsettled share could leave buttons locked without immediate recovery; registration and lengthy fallback instructions preceded the image. These tests are not evidence of physical iOS/WeChat save or send success.

Changes: image preview first on mobile; real full-size IMG viewer; explicit native sharing with precomputed files-only payload; WeChat-labelled entry shows image and album instructions first; visible fallback after cancel, rejection or no callback; registration/diagnostics moved below the photo; JPG available while PNG encodes separately.

Build fails closed if index differs from the audited baseline. Candidate branch is committed only after Chromium and WebKit suites pass. The workflow does not publish main.

Physical acceptance still required: iPhone Safari and iOS/Android WeChat, long-press save, locating image in Photos, sending to a friend, posting to Moments. A browser cannot guarantee an installed share target, saving to Photos, or final delivery. Never claim that the simulated tests passed those device-native operations.
