# Image workflows

## Source generation

`generate_source_image` supports the following service/style decisions. Query capabilities and current catalogues for exact options instead of inventing a preset.

| Service / style | Inputs and behavior |
| --- | --- |
| Ride-hailing `photo` | Country, vehicle model and tariff/transport label; visual brief and composition. |
| Ride-hailing `drivers` | Country, vehicle model, tariff and driver-focused brief. Audience and CRM carrier remain independent decisions. |
| `yandex-pro` | Scene brief, one or more `yandex_pro_selections`, approved background color. |
| `yango-pro-illustrations` | Brief, exactly one scene focus, optional exact reference and skin-tone palette. |
| `3d` | Object or scene brief. |
| `lucky` | Country, car, tariff and campaign idea; normally four variants with one or more Lucky styles. Split and feedback are for requested variants or iteration. |
| `reference-scene` | Upload references first; retain URL order and refer to Image 1, Image 2, etc. Queue limit is eight references per request. |
| `rides-for-business` / `photo` | Country, business car/tariff and B2B visual brief. Yandex Go B2B is a render brand, not a new source service. |
| `yango-drive` / `photo` | Country, vehicle model, city in city mode, optional color and camera angles. |
| `yango-motors` / `photo` | Vehicle model, optional angle/weather/location wish. |
| `rida` / `photo` | Independent `rida_items` with brief, role (`user`, `driver`, `none`) and transport (`car`, `moto`, `none`). `improve_rida_brief` can refine one brief. |
| `garage` / `photo` | Fetch the `garage` catalogue. Use its exact country/car and, in city mode, an allowed city. Reference sheets determine model and paint. |
| `scooters` | Select a `scooter-*` style and supply `scooter_options` as needed. |

For Ride-hailing photography, Rides for Business, Drive, Motors and Garage, `location_mode` selects `city` or `countryside`. Supply `location_description` for terrain and atmosphere. Drive/Garage countryside generation does not require a city; keep the target country. `car_logo=false` suppresses automotive branding for the services that support it. Garage identity and color stay tied to its curated sheet.

Garage currently lists Peru/Lima (red Kia Soluto, grey DFSK Glory 560) and Azerbaijan/Baku (white BYD Destroyer, white Toyota Corolla). These examples are not a replacement for fetching the live catalogue. For `regenerate_source_image` with Garage, retain `country` and `vehicle_model`; the advanced regeneration tool also accepts `sourceImageUrl` to recover library identity.

Ride-hailing UAE presets distinguish cities, including Abu Dhabi reference vehicles. Read `get_source_catalog(catalog="vehicles")` before choosing tariff or vehicle values.

## Different creatives and composition selection

Choose scene composition independently from the banner layout (Photo/Frame/etc.) and preserve the brief's fixed conditions. The MCP capability response lists presets by service, style and vehicle. For passenger car photography these are `inside the car`, `near the car`, `getting into the car`, `getting out the car`, `passenger with driver`, `window`, and `free composition`. Moto and tuk-tuk have their own presets; driver and business photography use separate lists. Pass the exact supported label as `composition` and a short hero/action description as `brief`. The generator expands these inputs into its production prompt. `preferred_angles` is for automotive services, not passenger scene briefs.

Example for three Yango Abu Dhabi creatives about the first three rides, if the brief leaves scenes open:

| Direction | Composition | Complete brief |
| --- | --- | --- |
| City journey | `window` | A young woman rides in the rear seat of a taxi, looking at the city through the open window. |
| Meeting friends | `near the car` | Two friends beside a taxi. One shows the other something on her phone; both smile. |
| Start your ride | `getting into the car` | A man with a small travel bag gets into the rear seat of a taxi. |

These are complete short briefs, not a fixed carousel or a starting point for a longer photography prompt. Select scenes suited to the current request and earlier visible outputs. Pass country, vehicle/tariff, style and composition through their dedicated fields. Let the generator determine framing, camera, lighting and photographic treatment unless the user explicitly specifies them. Offer, logo and space for copy belong to banner rendering; do not add empty-area or small-subject instructions to the source brief.

For separate scene briefs, call `generate_source_image` once per direction with `count=1`, `composition` equal to the chosen label, and `compositions` omitted or containing that same label. For one compatible shared brief, send the selected `compositions`, set `composition` to the first item, and use `count` as the TOTAL number of sources. Photo/Drivers composition planning currently caps a call at four images and distributes that count across presets; it is not count-per-preset. Split larger requested sets into bounded calls with distinct plans. Never use a shared brief that specifies “full taxi and person outside on the waterfront” for an interior or boarding preset.

Render each returned source as its own creative. Reuse it for its sizes, selected layouts and CRM text/clean variants. A change of crop or headline alone does not count as another visual concept when different scenes were requested.

## Scooters

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
