---
name: create-yango-banners
description: Generate, edit, revise, render, and share finished Yango-family creative assets through Yango Creative Machine. Use for Ride-hailing, Rides for Business, Yango Drive, Yango Motors, or RIDA source images; Photo, Drivers, Yandex Pro or YANGO PRO illustrations, 3D, Lucky, Reference Scene, or Edit workflows; rebuilding flattened banners; revising existing builder links field-by-field; performance and in-app/CRM banner packs; ZIP archives; editable builder links; and publishing finished packs to Yandex Disk.
---

# Create Yango Creatives

Choose the exact image-generation or edit mode, preserve editable states, verify the source, render the requested matrix, and return real asset and editor links.

## Route existing banner revisions first

1. Check whether the user supplied an `edit_url` before treating a banner as an image.
2. When an `edit_url` exists, call `revise_banner_from_edit_link`. Patch only the requested text, brand, layout, badge, source, placement, or positioning fields. Keep omitted fields unchanged, render the saved `perf` or `crm` section, and return the newly created `edit_url`. Do not upload a screenshot, run OCR, or use image Edit merely to change editable fields.
3. When no `edit_url` exists and the supplied PNG/JPEG/WebP is a flattened banner with image, text, logo, or disclaimer baked into one raster, route it through `edit_source_image` (Creative Machine Edit mode).
4. For a flattened banner whose copy or logo must become editable, first use `edit_source_image` to remove the baked text/logo/disclaimer and reconstruct the background. Then pass the cleaned source to `render_banner_pack` or `render_in_app_pack` with the new fields. Do not place fresh editable copy on top of old baked copy.
5. For a purely visual pixel change to a flattened banner, return the Edit result directly unless the user also requests a reusable editable pack.

## Route the source workflow

1. Use an existing public/Yango-hosted source-image URL unchanged when the user supplies one. Apply the existing-banner rules above when the URL points to a finished banner.
2. For an attached/local JPEG, PNG, or WebP up to 20 MB, encode it as a Base64 data URL and call `upload_source_image`. Never pass a local path as a remote source URL.
3. Call `generate_source_image` for generation, using this routing:
   - `photo`: Require country, vehicle model, and tariff/transport label. Use for ordinary Ride-hailing or Rides for Business photography.
   - `drivers`: Require country, vehicle model, tariff, and a driver-focused brief. Use only with Ride-hailing.
   - `yandex-pro`: Require a scene brief and at least one Yandex Pro scene ingredient. Use an approved background color.
   - `yango-pro-illustrations`: Require a scene brief and exactly one scene focus. Optionally select its exact reference and skin-tone palette.
   - `3d`: Require only the object or scene brief.
   - `lucky`: Require country, vehicle model, tariff, and the campaign idea. Default to four variants and one or more Lucky styles; use split and feedback only when requested or iterating.
   - `reference-scene`: Upload references first, preserve their returned order, and describe them as Image 1, Image 2, and so on in the scenario.
4. Use service-specific Photo generation for:
   - `rides-for-business`: country, business vehicle/tariff, and B2B brief.
   - `yango-drive`: country, city, vehicle model, optional color, angles, and variant count.
   - `yango-motors`: vehicle model, optional angle, weather, and location wish.
   - `rida`: one or more RIDA items, each containing a brief, role (`user`, `driver`, or `none`), and transport (`car`, `moto`, or `none`).
5. Call `edit_source_image` for Edit mode. Supply the source URL, precise edit instruction, optional reference URL, and desired ratio. Reuse the returned URL for further edits or rendering. Never use this tool for field-only changes when an `edit_url` exists.
6. Call `regenerate_source_image` only when rerunning an already finalized prompt. Do not use it to translate a new campaign brief.
7. Call `get_banner_capabilities` when a requested service, style, brand, size, placement, or option may be unsupported. Treat it as authoritative.

## Verify and render

1. Inspect every generated or edited source when image inspection is available. Check the requested people, identity, vehicle, setting, action, safety details, references, and usable text space.
2. Choose the renderer:
   - Use `render_banner_pack` for paid-social/performance formats.
   - Use `render_in_app_pack` for CRM, showcase, fullscreen, feed, promo, ticket, or WhatsApp placements.
3. Convert each performance copy variation into a separate text set. Default to all four performance sizes when none are specified.
4. For in-app work, pass requested placements; default to the six main consumer placements. Use a left-side icon when badge text is empty and a badge only when it contains text.
5. Keep positioning at 100% and zero shift unless inspection shows a problem. Use one global adjustment only when it works for the entire pack; otherwise use per-output overrides. Positive X moves right, positive Y moves down, and shifts use 50-pixel increments.
6. Re-render with the same source after crop changes. Do not generate another paid source merely to fix positioning.
7. Verify `status: ready`, asset count, representative square and vertical outputs, and ZIP contents when practical.
8. Return every asset grouped by variant and size/placement, the ZIP URL, the `edit_url`, and all warnings.

## Share to Yandex Disk

1. Call `share_banner_pack_to_yandex_disk` only when the user explicitly asks to share, publish, or upload the finished pack to Yandex Disk. Never publish automatically after rendering.
2. Pass the real asset URLs returned by the render or revision tool. For performance assets, group each variant under `set_N`; for CRM assets, group each source under `image_N`. Use descriptive file names based on size or placement when available.
3. Set `category` to `perf` for performance banners and `crm` for in-app assets. The generator creates and uploads the ZIP automatically; do not upload the render tool's ZIP as another asset.
4. Return `public_url` as the primary share link and also report `folder_name`, `disk_path`, and `uploaded_files` when present.
5. Keep `YANDEX_DISK_OAUTH_TOKEN` in the generator service only. Do not request, copy, or expose it through MCP or the skill.

## Reliability and safety

- Treat generation and editing as potentially paid operations. Do not retry them after an ambiguous timeout without explicit approval.
- Treat upload as state-changing: upload only user-supplied or explicitly approved media.
- Treat Yandex Disk sharing as an external write: call it only after an explicit share/publish/upload request.
- Retry a transient render or ZIP failure at most once because it reuses the source.
- Never fabricate, normalize, or reconstruct source, asset, ZIP, or editor URLs.
- Do not expose credentials, authorization headers, internal traces, or local configuration.
- If authentication fails, distinguish MCP access from upstream Yango access without revealing secrets.
