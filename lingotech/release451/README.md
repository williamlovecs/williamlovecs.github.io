# LingoTech v4.5.1

Small reliability patch. Existing photo assets and QR payloads are preserved exactly. Canonical URL is unchanged; the legacy URL still redirects to it.

- Exactly one canonical tag; brand-only Open Graph preview and metadata.
- Live camera video uses object-fit:contain so the full preview matches full-frame capture. Decorative camera overlay is removed to avoid suggesting it is baked into the photo.
- Feishu signup form labels say event signup, not automatic community membership.
- Existing regression suites rerun for Chromium/WebKit. Supplemental checks cover denied/late camera permission, invalid files, intentional scene-detail visibility and visitor-free exported HTML. A Chromium fake camera exercises actual video-to-canvas code; it is not a physical iPhone or WeChat validation.
- No forms are submitted. No analytics collector is added. No new participant images are published.
- Feishu Casebook editing and photo-publication permission review are separate. The printed Casebook QR target is not changed by this release.
