---
name: create-yango-banners
description: Generate finished, editable Yango or Yandex Go performance and in-app/CRM banner packs from a campaign brief or source image. Use when the user asks to create paid-social banners, app showcases, fullscreen CRM, feed, promo, ticket, or WhatsApp placements; generate a suitable source visual; receive individual assets and a ZIP archive; or get a Yango Creative Machine deep link for later edits.
---

# Create Yango Banners

Turn a brief or source image into a complete banner matrix. Return the rendered assets, ZIP archive, and editable Creative Machine link.

## Workflow

1. Determine whether the user supplied a usable source image URL.
2. If no source image exists, gather only the missing inputs required by the image-generation tool:
   - For a photo, require a brief, country, and vehicle model.
   - For a driver scene, also require the transport label.
   - For Yango Drive, also require the city.
   - For a 3D visual, require only the object or scene brief.
3. Call the capability-discovery tool when the requested brand, layout, style, size, or placement may be unsupported. Treat the returned capabilities as authoritative.
4. Generate a source image only when needed. Use the exact returned image URL; never invent, normalize, or rewrite it.
5. Visually inspect a newly generated source image before rendering when image inspection is available. Verify the requested people, setting, vehicle, pose, safety details, and usable text space. Do not spend a render on a clearly unsuitable source.
6. Select the renderer:
   - Use the performance renderer for paid-social and performance sizes.
   - Use the in-app renderer for CRM, showcase, fullscreen, feed, promo, ticket, and WhatsApp placements.
7. Build the requested matrix:
   - Convert every performance copy variation into a separate text set. When sizes are omitted, request all four supported performance sizes.
   - Pass the requested in-app placements. When placements are omitted, request the six main consumer placements.
8. Position the source image when the default crop does not keep the subject well framed:
   - Use global scale and shifts only when the same adjustment works for the complete pack.
   - Prefer per-output image overrides when different aspect ratios need different crops. Target performance overrides by text-set index and size; target in-app overrides by placement.
   - Use scale percentages and 50-pixel shift increments. Positive X moves the image right; positive Y moves it down.
   - Re-render with the same source image after a positioning adjustment. Do not generate a replacement source merely to fix a crop.
9. Wait for the same render request to finish. Do not start duplicate work merely because adaptive crops or uncrops take longer.
10. Verify that the result reports `status: ready` and contains at least one asset URL. When practical, confirm that the ZIP contains the expected number of files and inspect one square and one vertical result. If a subject is clipped or poorly balanced, adjust only the affected outputs and verify them again.
11. Report the result with:
   - A concise completion summary.
   - Every asset grouped by copy variation and size or placement.
   - The ZIP URL, when returned.
   - The `edit_url`, explicitly labeled as the link for continuing edits.
   - Any renderer warning or omitted format.

## Defaults

- Use brand `yango`, image service `ride-hailing`, style `photo`, and English copy unless the brief says otherwise.
- Use performance layout `photo`.
- For in-app work, use service `taxi`, layout `fade`, automatic text color, and the six default consumer placements.
- Use a left-side icon when badge text is empty. Use a badge only when it contains text.
- Keep image positioning at 100% scale and zero shift unless inspection shows a composition problem. Performance photo layouts support 100–150% scale, frame layouts 100–350%, and in-app placements 50–180%; shifts range from -400 to 400 pixels.
- Use `free composition` when the user gives no composition direction.
- Preserve supplied headline, subtitle, disclaimer, locale, and capitalization verbatim unless the user explicitly requests copywriting or translation.
- Use `**text**` only when the user asks for an accent-color highlight and the renderer documents that syntax.

## Reliability and Safety

- Do not claim success before the selected renderer returns a ready result and real asset URLs.
- Never fabricate or reconstruct asset, archive, source-image, or edit URLs.
- Do not expose credentials, authorization headers, internal errors, or local configuration.
- Do not retry paid image generation after an ambiguous timeout without explicit user approval. The first request may still be running.
- Retry a transient render or ZIP failure at most once because it reuses the existing source image.
- If authentication fails, identify whether access to the MCP service or the upstream Yango service failed without revealing secrets.
- If a source URL is protected or inaccessible, request an accessible URL or use the exact internal path supported by the service; do not guess a replacement.
