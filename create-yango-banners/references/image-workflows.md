# Image workflows

## Source generation

Before a new source generation, read [service input ownership](service-inputs.md) and the live `source_input_contract` from `get_banner_capabilities`. Choose the service/style, then fill its actual Hero, Situation or Drive Wish fields. The generator writes the production prompt from those inputs and its guides. `brief` is an optional compatibility fallback, not a required universal prompt.

For Ride-hailing photography, Rides for Business, Drive, Motors and Garage, `location_mode` selects `city` or `countryside`. Supply `location_description` for terrain and atmosphere. Drive/Garage countryside generation does not require a city; keep the target country. `car_logo=false` suppresses automotive branding for the services that support it. Garage identity and color stay tied to its curated sheet.

Garage currently lists Peru/Lima (red Kia Soluto, grey DFSK Glory 560) and Azerbaijan/Baku (white BYD Destroyer, white Toyota Corolla). These examples are not a replacement for fetching the live catalogue. For `regenerate_source_image` with Garage, retain `country` and `vehicle_model`; the advanced regeneration tool also accepts `sourceImageUrl` to recover library identity.

Ride-hailing UAE presets distinguish cities, including Abu Dhabi reference vehicles. Read `get_source_catalog(catalog="vehicles")` before choosing tariff or vehicle values.

For web/MCP comparison, match the selected service, style, country/tariff, composition and both text fields. `inside the car` and `getting into the car` are different presets. Use exact catalogue values, such as `UAE — Abu Dhabi`. New generation uses `generate_source_image`; `regenerate_source_image` requires an already finalized prompt.

## Different creatives and composition selection

Choose scene composition independently from the banner layout (Photo/Frame/etc.) and preserve the brief's fixed conditions. The MCP capability response lists presets by service, style and vehicle. For passenger car photography these are `inside the car`, `near the car`, `getting into the car`, `getting out the car`, `passenger with driver`, `window`, and `free composition`. Moto and tuk-tuk have their own presets; driver and business photography use separate lists. Pass the exact supported label as `composition` and short descriptions in the Hero/Situation fields appropriate to the selected mode. The generator expands these inputs into its production prompt. `preferred_angles` is for automotive services, not passenger scene briefs.

Example for three Yango Abu Dhabi creatives about the first three rides, if the brief leaves scenes open:

Example execution announcement (adapt to the actual audience and supported layouts):

«Покажу сразу три превью:
1. На утренник ребёнка — мама с букетом, композиция у окна такси, фото на весь баннер.
2. После покупок — две подруги с пакетами, композиция рядом с такси, красная рамка.
3. На деловую встречу — мужчина с дорожной сумкой, композиция посадки, белый лейаут.

Для всех: заголовок “Your first 3 rides”, бейдж “30% OFF”, без дополнительного выделения слов. При желании оформление можно заменить на чёрный лейаут, серую или чёрную рамку. Какой дисклеймер добавить — или делаем без него?»

Render these as previews with `create_zip=false`; export selected versions only after a download request. This announces planned generation; it does not claim the images already exist or ask for concept approval. For an open new banner request, generate three sources by default and render each in its assigned layout. Use any explicitly requested count instead; a precise single execution/revision or ideas-only request does not expand to three. Preserve audience constraints and develop relevant contexts instead of repeating this example. The missing-disclaimer question does not block independent source generation; final text-bearing rendering waits for the answer.

| Direction | Composition | Hero | Situation |
| --- | --- | --- | --- |
| Family occasion | `window` | Мама с букетом цветов. | Едет на утренник ребёнка. |
| After shopping | `near the car` | Две подруги с пакетами покупок. | Возвращаются из магазина. |
| Business meeting | `getting into the car` | Мужчина с небольшой дорожной сумкой. | Опаздывает на совещание. |

These are complete description fields, not a fixed carousel or a starting point for a longer photography prompt. Situation gives the life context; the selected composition supplies physical staging such as boarding or sitting inside. Choose contexts suited to the request and earlier visible outputs; leave Situation empty when no context is needed. Pass country, vehicle/tariff, style and composition through their dedicated fields. A time of day (day, evening, night) can be part of the context. Let the generator determine lighting, framing, camera and photographic treatment unless the user explicitly specifies them. Offer, logo and space for copy belong to banner rendering.

For separate scenes, call `generate_source_image` once per direction with `count=1`, `composition` equal to the chosen label, and `compositions` omitted or containing that same label. For one compatible shared brief, send the selected `compositions`, set `composition` to the first item, and use `count` as the TOTAL number of sources. Photo/Drivers composition planning currently caps a call at four images and distributes that count across presets; it is not count-per-preset. Split larger requested sets into bounded calls with distinct plans. Never use a shared brief that specifies “full taxi and person outside on the waterfront” for an interior or boarding preset.

Render each returned source as its own creative. Reuse it for its sizes, selected layouts and CRM text/clean variants. A change of crop or headline alone does not count as another visual concept when different scenes were requested.

## CIS Scooters

Active UI styles are `scooter-3d-2`, `scooter-cinematic-3d` and `scooter-photo`. Cinematic offer generation uses `scooter-cinematic-3d-offer` and requires the exact offer. Older `scooter-3d` and `scooter-3d-offer` routes remain available for compatibility.

`scooter_options` supports `offer`, `concept_count`, `creative_mode` (`minimalism` or `environment`), `photo_compositions`, and composition/location/phone-screen reference URLs. Photo compositions: `beside`, `riding`, `two-riders`, `event`, `phone`, `closeup`, `parking`. Photo mode requires a supported country: Uzbekistan, Kazakhstan, Kyrgyzstan, Georgia, Serbia or Armenia. Other scooter styles can omit country. Use `face_reference_image_url` for the hero when requested.

## Editing and glitch repair

Use `edit_source_image` for an ordinary image edit with an optional second reference and aspect ratio. `regenerate_source_image` reruns an already finalized prompt; it does not turn a new brief into a production prompt.

For selected glitch categories or expanded image repair:

1. Fetch `get_source_catalog(catalog="glitch-repairs")` for actual recipe IDs. An audit through `check_image_glitches` is useful when diagnosis is requested or the defects are unclear; it is not mandatory before an explicitly requested known-category repair.
2. Call `edit_image_advanced` with `imageUrl` and `glitchRepairIds`, plus `repairContext` if needed. Selected category repair can omit `editPrompt`.
3. Keep the original intended source in `originalImageUrl` when available. For full expanded-canvas repair, set `editMode="expanded-full-frame"` and provide both the expanded target and original source. The target is the color/light reference; the original supplies intended identity and geometry.
4. `imageSize` can request `2K` or `4K`. `editMode="expanded-region"` uses an `editRegion` object for a local expanded-area edit. The region uses normalized `x`, `y`, `width`, `height` in 0–1 image coordinates; width/height must be at least 0.005 and the rectangle must fit within the canvas.
5. Inspect the returned image, `glitch_repair`, `expanded_edit` and warnings. Keep the complete corrected canvas as the new source. Backend repair diagnoses selected regions, composites corrections and verifies the result; it does not justify claiming the image is flawless without inspection.

## Banner experiments

`analyze_banner_experiment` takes `imageUrl`, optional brand/country/service, and count (1–6). It returns diagnosis, extracted copy, text sets, hypotheses and image-edit prompts. Review those against the user's intended test.

To generate from that analysis, call `generate_banner_experiment_images` with the source/context and the returned fields at the payload root: `text_sets`, `hypotheses`, `image_edit_prompts`, `extracted`, `diagnosis`, `renderer_constraints_used`, `visual_summary`. Do not wrap them in an invented `analysis` object. `remix_banner_experiment` combines analysis and image generation when the complete experiment is requested. Render the returned editable copy/source variants through the appropriate banner workflow.

## New service modes and Icons

Use [service inputs](service-inputs.md#additional-service-modes) and live capability
schemas for Business 3D, Flare/Playful icons, Beri Zaryad, Power, Yango Scooters and
City to City. The separate Icons web workspace still routes through `ride-hailing`
with `3d-icon`/`3d-icon-playful`; it is not a passenger Photo style. Upload requested
PNG content references first and pass their actual generator URLs. Keep internal
style references under generator control.

Choose the placement before generation. If the request does not identify it, ask
whether the user needs a map object or a promo plaque; do not generate both views
as a default. A promo plaque here is an Icons asset, separate from a CRM Promo card.

| Placement | Typed `icon_placement` | Required native angle | Base canvas |
| --- | --- | --- | --- |
| Object on the map | `map` | `isometric`: three-quarter view from slightly above | 80×80 px |
| Promo plaque | `promo` | `near-side`: straight level elevation, orthographic camera, no downward pitch | 40×40 px |

Call `generate_source_image` with `service="ride-hailing"`, the requested
`style="3d-icon"` (Flare) or `"3d-icon-playful"`, `icon_placement`, and the object
in `situation_description`. Leave `icon_angles` unset; it is only a compatibility
field and must match the placement's single angle if provided. One image is
generated per placement per call. If both carriers are explicitly requested, use
two calls. Advanced `generate_image_advanced` uses the MCP field `iconPlacement`;
MCP translates it into native `iconAngles` and `count=1`. Conflicts fail before any
paid submission. Preserve the returned style, placement and angle metadata.

For an edit, use `edit_source_image(source_image_url=ACTUAL_PNG_URL,
edit_prompt=FULL_ENGLISH_EDIT_PROMPT, style=ORIGINAL_STYLE,
icon_placement=ORIGINAL_PLACEMENT)`. Keep the original style and placement from
metadata through every subsequent edit. The MCP passes `styleId` to native
`/api/edit-image`, which selects the same `gpt-image-2.5-flare` model as generation,
with `background="transparent"`, PNG output and the original RGBA source. Camera,
style, silhouette transparency and subtle contact shadow must survive. Advanced
`edit_image_advanced` requires original `styleId` and MCP `iconPlacement`. Do not use
expanded modes, glitch repair, layer editing or generic regeneration for Icons;
those routes do not guarantee the same model and alpha workflow. Provide the full
English prompt whenever revising it, including the placement requirements.

Export selected finished originals **or edited PNGs** only when download/export
is requested. Use `export_3d_icons` with exactly one `imageUrls` entry containing
the actual `url` and its original `angle`, the same `placement`, and explicit
matching `styleId`. Map rejects near-side; promo rejects isometric. To export
both placements, call separately. No extra generation or local image conversion.
Absolute result URLs from this generator are normalized to local PNG paths.

The native ZIP must contain exactly eight square RGBA PNGs per selected icon:

| Suffix | Density | Map canvas | Promo canvas |
| --- | --- | --- | --- |
| `-mdpi` | 1× | 80×80 | 40×40 |
| `-hdpi` | 1.5× | 120×120 | 60×60 |
| `-xdpi` | 2× | 160×160 | 80×80 |
| `-xxdpi` | 3× | 240×240 | 120×120 |
| `-xxxdpi` | 4× | 320×320 | 160×160 |
| `@1x` | 1× | 80×80 | 40×40 |
| `@2x` | 2× | 160×160 | 80×80 |
| `@3x` | 3× | 240×240 | 120×120 |

The generator fits proportionally and centers the object and shadow on transparent
padding. Preserve native filenames `{placement}-{styleId}-{angle}{suffix}.png`,
including `-xdpi` exactly as the product names it. Do not use banner export or
invent different density names. Keep the returned ZIP and task IDs, poll queued
operations to completion, and verify archive names, all eight canvas sizes and
real alpha before claiming compliance. Opaque or fully transparent assets must
fail rather than be delivered as successful Icons exports.

For requested layer editing, discover `separate_seedream_layers`,
`edit_seedream_layer`, `compose_seedream_layers` with `get_operation_contract`.
Separate using the actual `imageUrl`; retain returned layer URLs and geometry.
Edit the selected saved `layerImageUrl` with the complete requested `prompt`, then
compose `baseImageUrl` plus the native `layers` and optional `crop`. Separation and
layer editing may incur charges; inspect/poll the existing operation before retrying.
Do not substitute local composition or regenerate all layers to change one object.
