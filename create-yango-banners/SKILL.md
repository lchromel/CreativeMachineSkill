---
name: create-yango-banners
description: Create and revise Yango Creative Machine images, performance and CRM banners, automotive and UGC videos, and creative experiments. Use for Yango-family services including Garage and scooters, image glitch repair, editable builder links, media libraries, archives, and requested Yandex Disk sharing through the Creative Machine MCP.
---

# Create Yango Creatives

Use the Creative Machine MCP for the user's requested image, banner or video workflow. Return actual outputs and preserve editable settings. Reply in the user's language.

## Discover and route

- `get_banner_capabilities` lists image services, styles, brands, placements, sizes and positioning limits.
- `get_source_catalog` reads current `vehicles`, `garage`, or `glitch-repairs` options from the generator. Use the catalogue for exact country/city/car combinations, tariffs and repair IDs.
- `get_operation_contract()` lists advanced tools. Call it with `tool_name` before an unfamiliar operation to see its native request fields and defaults. Advanced tools take a `payload` object with the upstream field names, commonly camelCase; convenience tools take snake_case arguments.
- For source generation, Garage, scooters, countryside scenes, glitch repair or experiments, read [image workflows](references/image-workflows.md).
- For Standard/UGC video, storyboards, reference uploads and branded exports, read [video workflows](references/video-workflows.md).
- For multiple source images, detailed performance/CRM options, native render matrices, library operations or builder state serialization, read [advanced API](references/advanced-api.md).

## Handle queued operations

Convenience image/render tools wait for their results. Advanced generation, editing, rendering, archives and sharing usually return `operation_id`, `operation_client_id` and `status: queued` or `running`.

1. Retain both IDs. Call `wait_for_operation` with them and a timeout up to 60 seconds. Continue checking the same task while it runs; report useful progress during long work.
2. On `succeeded`, use the nested `result` as the operation response. Queued or running is not a finished asset.
3. On `failed` or `interrupted`, inspect `error` and `can_resume`. When `can_resume` is true and continuation is authorized, call `resume_operation` with `payload.operationId` and the original `operation_client_id`. This continues the known video task.
4. After an ambiguous submission timeout, use `list_operation_jobs` with the owner ID reported in the error. After a status timeout, retry only the status read. Never create a new paid generation merely because the connection was lost.
5. Caller-supplied `request_id` requires the original `operation_client_id`; an authorized submission retry must retain both IDs and the exact payload. Do not repurpose the key for changed inputs.
6. Older video/storyboard APIs can return a separate `job_id`; follow it with `get_video_generation_job` or `get_video_storyboard_job` using `parameters.jobId`.

## Keep audience, source style and carrier separate

Choose the intended recipient before rendering. Driver communication includes earnings, fleet and Yango Pro tasks; showing a driver in a passenger advertisement does not make the audience drivers. The `drivers` image style controls photography only.

For CRM, consumer communication uses ordinary placements; driver communication uses `drivers-*`. Map a generic driver request for feed, stories or WhatsApp to `drivers-feed`, `drivers-stories` or `drivers-whatsapp`. Ask about the audience only when it cannot be inferred and the wrong placement family would make the output unusable.

## Revise existing assets

- With an `edit_url`, use `revise_banner_from_edit_link` for requested field changes. Omitted fields stay unchanged and the tool returns a new editable link. Use `performance_text_updates` or `in_app_text_updates` for the saved section.
- Without an editor link, a flattened banner goes through `edit_source_image`. If its copy must become editable, remove baked text/logo/disclaimer and reconstruct the background, then rebuild with a renderer.
- For a purely visual pixel change, return the edited image unless a reusable pack is also requested.
- For unsupported convenience fields, load the full saved state with `get_builder_settings`, preserve untouched fields and follow the native matrix workflow in the advanced reference. Do not silently discard new fields.

## Verify and render

1. Reuse a provided public/Yango source URL unchanged. For local/attached JPEG, PNG or WebP up to 20 MB, call `upload_source_image` with Base64 data; local paths are not remote URLs.
2. Inspect generated/edited sources when image inspection is available: requested subject and vehicle, identity, setting, action, references and usable text space.
3. Use `render_banner_pack` for performance. Each copy variation is a text set; default to the four performance sizes when unspecified.
4. Use `render_in_app_pack` for CRM. Its omitted placements default only to consumers. Driver placements are `drivers-fleet-room-preview`, `drivers-stories-showcase`, `drivers-stories`, `drivers-full-screen`, `drivers-feed`, `drivers-fleet-room-story`, `drivers-whatsapp`, `drivers-tg-chats`, `drivers-tg-post`, `drivers-tg-stories`, and `drivers-mail`.
5. For Yandex Go B2B, use brand `yandex-go-b2b`, layout `frame`, a locale from capabilities, and the desired `text_sets[].accent_color`. One editable pack uses one palette; use separate packs for different colors.
6. Use a left-side icon when CRM badge text is empty; a labeled badge requires text. A CRM price badge is separate from the service badge.
7. Start image positioning at 100% and zero shift. Positive X moves right; positive Y moves down; shifts use 50-pixel increments. Use per-output overrides when one global crop cannot fit the pack.
8. Performance badge shifts are 0–100 in steps of 5; scale is 70–150% in steps of 5. Set defaults on the text set and individual-size values through `badge_overrides`. Revisions use `performance_badge_overrides`. `badge_small_text_position` chooses top/bottom; CRM revisions expose independent `price_badge_*` fields.
9. Re-render the same source after positioning changes; avoid another paid generation solely for crop adjustments.
10. Verify successful status, asset count, representative square/vertical outputs and archive contents when practical. Return all requested asset URLs grouped by variant/size/placement, ZIP, editable link and warnings.

## Deliver and manage media

Publish only when the user asks to share/upload/publish to Yandex Disk. Use `share_banner_pack_to_yandex_disk` for performance/CRM assets or `share_videos_to_yandex_disk` for videos. Pass real rendered URLs; the generator creates the package ZIP. Do not upload a ZIP as another banner. Use category `perf` or `crm`, group performance variants under `set_N` and CRM images under `image_N`, and return `public_url` as the primary share link.

Use paginated library reads to reuse existing assets. Delete library entries only when requested. A download counter update is not an actual media download.

## Reliability

Generation, vision audits, prompt generation and editing may incur provider charges. Do not repeat ambiguous paid operations without authorization. A definite transient render/archive failure may be retried once with the same sources; queued/running tasks must instead be checked by ID.

Upload only user-provided or authorized media. Keep provider credentials and Yandex Disk OAuth in the generator; MCP video submission uses a server-side `YANGO_VIDEO_GENERATION_PASSWORD`. If local credentials are needed, use the user's designated token file first without printing secrets. Distinguish missing MCP access, upstream authentication and video-password configuration failures.

Never fabricate asset links, expose authorization headers/internal traces, or claim a task is complete without its returned output. When rewriting a prompt, provide the complete revised prompt.
