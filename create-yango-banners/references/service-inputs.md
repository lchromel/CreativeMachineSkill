# What to send to each generator mode

Use the generator's existing prompt-writing pipeline. The agent supplies the user's content and selects supported controls; the generator supplies its mode's visual language, reference roles and final production prompt. These are different inputs from the finalized `prompt` accepted by regeneration and video submission tools.

## Text fields, not a universal photography prompt

Prefer the explicit web fields in `generate_source_image`:

| MCP field | Web/native field | Purpose |
| --- | --- | --- |
| `hero_description` | Hero / `modelDescription` | Who appears: relevant identity, clothes and accessories. |
| `situation_description` | Situation / `situationDescription` | For passenger/business/scooter Photo: the life context or purpose of the trip. Other modes use this field for their object/idea or service-specific story. |
| `scene_wish` | Drive Wish / `driveWish` | Optional automotive scene wish for Drive, Motors and Garage. |
| `brief` | Compatibility fallback | Used only if explicit fields are omitted; goes to the one field listed below, never both. |

An explicit empty string stays empty. When either Hero or Situation is provided, the unspecified other field stays empty and `brief` is not copied into it. Automotive uses `scene_wish` (or `brief` if omitted) and leaves Hero/Situation empty. Descriptions are optional where the web permits it; do not invent filler text to satisfy a universal required brief.

For photographic trip scenes, Hero describes who the person is; Situation describes why they travel or what is happening in their life: late for a meeting, going to a child’s school performance, returning from shopping. The composition preset supplies boarding, sitting inside, being beside the car and other physical staging. Leave Situation empty if no context is needed; do not fill it by paraphrasing the preset. Preserve an explicitly requested action without inventing extra staging.

Use concise ordinary language. A time of day, weather, place or action can be meaningful content. Photographic light direction, softness, rim light, color temperature, lens, exposure, framing and empty space are already developed by the selected pipeline; add them only for an explicit user request. Keep campaign copy, badges, logos and banner positioning in render fields. Dedicated offer-in-image styles are the exception described below.

Country, tariff, car, color, composition and references have their own controls. Use exact catalogue values; do not replace a preset label or a color name with a paragraph. Descriptions can remain in the user's language: the generator writes its final prompt in English where required.

## Image services

| Service / style | Agent supplies | Generator already supplies | `brief` fallback |
| --- | --- | --- | --- |
| Ride-hailing / `photo` | Exact country/tariff/car, composition; optional Hero and Situation, face reference if requested. Both descriptions may be empty. | Urban Fashion / Documentary guide, casting defaults, local architecture/clothes, composition rules and reference, vehicle/livery reference where available, road geometry and photographic treatment. | Hero only. |
| Ride-hailing / `drivers` | Country/tariff/car, a driver composition, required Situation describing the driver and work context together; the driver preset supplies physical staging. | Driver-only documentary guide, practical clothing defaults, local context, car as supporting context, composition reference and photography. | Situation only. |
| `rides-for-business` / `photo` | Country/tariff/car, business composition, optional Hero and Situation. Put the business task in Situation. | Business editorial guide; Situation is the dominant story. It decides whether a car belongs in an office/lunch/meeting scene rather than forcing a taxi into every scene. | Situation only. |
| `yango-drive` / `photo` | Country/city and car, paint if wanted, supported automotive angle(s), optional scene wish. Countryside uses terrain description instead of a required city. | Vehicle classification/year, local scene selection and references, automotive prompt structure, camera/road logic and lighting. | Drive Wish only; optional. |
| `yango-motors` / `photo` | Car, optional supported angle, `weather`, scene wish and location mode. Default market/city is Cote d'Ivoire / Abidjan. | Model reference and paint from that reference, Abidjan location reference, weather guide, cinematic automotive treatment. | Drive Wish only; optional. |
| `garage` / `photo` | Exact country/city/car from Garage catalogue, supported angle(s), optional scene wish or countryside description. | A deterministic production prompt, exact car and paint from the combined reference sheet, geometry, local setting and lighting. Wishes do not change the reference model/paint. | Drive Wish only; optional. |
| Ride-hailing / `3d` | Required Situation naming an object or small related object set. | Red backdrop, tactile materials, close product composition, studio/rim lighting and style references. | Situation only. |
| Ride-hailing / `yandex-pro` | Required Situation, selected ingredients and supported background color. | Illustration master prompt, selected ingredient references and visual style. | Situation only. |
| Ride-hailing / `yango-pro-illustrations` | Required Situation, exactly one focus, selected scene reference and skin tone. | Mandatory style guide, style anchor, scene/transport construction, anatomy and skin reference card. | Situation only. |
| Ride-hailing / `lucky` | Required message/idea, country/tariff/car, Lucky styles and optional split/feedback. | Creative concept, metaphor, palette, light, composition and full image prompt. Let this service invent the concept instead of prescribing a full photographic scene. | Situation only. |
| Ride-hailing / `reference-scene` | Required new scenario and uploaded references in order; state which reference supplies which requested content when needed. | Image 1 as primary style authority by default, reference analysis and roles, structured final prompt. It preserves the reference medium, rather than defaulting to photography. | Situation only. |
| `rida` / `photo` | One short idea per `rida_items` entry, with independent role (`user`, `driver`, `none`) and transport (`car`, `moto`, `none`). | Selected zebra/vehicle identity, role-specific references, solid RIDA blue `#006BFF`, 3D materials, composition and lighting. | One item's idea; omit when items are supplied. |
| `scooters` / `scooter-photo` | Supported country, photo composition(s), optional Hero and Situation; requested face/location/composition/screen references. | Exact country scooter model, photo guide, reference manifest, casting, helmet/riding rules and composition staging. Both descriptions may be empty. | Hero only. |
| `scooters` / `scooter-3d-2` | Required scene/idea, creative mode and concept count. | Dedicated soft graphic 3D guide, approved yellow scooter and style references, concept development and lighting. | Situation only. |
| `scooters` / cinematic or legacy 3D | Required scene/idea, selected style; exact `scooter_options.offer` for an `*-offer` style. | Approved scooter identity and that style's environment/material/light rules. Offer styles place the exact supplied offer in the image. | Situation only. |

Photo/Drivers/Business compositions are preset labels, not free-text instructions. Read `source_compositions` in capabilities. `free composition` is the passenger Photo option for a custom scene, whose content still belongs in the description. Automotive angles use `preferred_angle`/`preferred_angles`. Scooter Photo uses `scooter_options.photo_compositions`; the same-named passenger presets do not apply.

Face references are used by passenger/business Photo and Scooter Photo. Drivers does not pass a face reference through its current pipeline. General `reference_image_urls` are for Reference Scene; use a mode's dedicated reference control elsewhere rather than assuming every service reads every URL field.

## Complete short description examples

Keep each example as short as shown unless the user supplied more necessary content. Preserve their actual people and life context rather than reusing these examples for every request.

| Mode | Exact description fields |
| --- | --- |
| Passenger Photo | Hero: `Мужчина с небольшой дорожной сумкой.` Situation: `Опаздывает на совещание.` Composition: `getting into the car`. |
| Drivers | Situation: `Водитель около 35 лет начинает рабочую смену.` Composition: `driver inside car`. |
| Business | Hero: `Сотрудница компании с ноутбуком.` Situation: `Едет на встречу с новым клиентом.` Composition: `back-seat work`. |
| Drive / Motors / Garage | Scene wish: `Машина припаркована возле офиса вечером.` Car, city and angle are separate controls. |
| 3D | Situation: `Открытый дорожный чемодан с наушниками внутри.` |
| Yandex Pro illustration | Situation: `Водитель проверяет заказы в телефоне.` Select the corresponding ingredients separately. |
| Yango Pro illustration | Situation: `Водитель помогает пассажиру с сумкой.` Select one matching focus/reference separately. |
| Lucky | Situation: `Экономия на первых поездках даёт больше свободы для планов на день.` Select Lucky styles separately. |
| Reference Scene | Situation: `Герой из Image 2 отдыхает на скамейке в визуальном стиле Image 1.` Upload the two authorized references in that order. |
| RIDA | Item brief: `Пользователь выбирает удобную цену поездки.` Role `user`, transport `car`. |
| Scooter Photo | Hero: `Две подруги.` Situation: `Спешат на встречу с друзьями после учёбы.` Photo composition `two-riders`. |
| Scooter 3D | Situation: `Самокат среди крупных весенних цветов.` Select the 3D style separately. |

## Counts and predefined outputs

Match the requested count to the selected service, rather than assuming every mode expands the same `count` field:

- Photo, Drivers and Business distribute a total of up to four images across compositions. Drive/Garage support one to four variants.
- Motors, object 3D and Reference Scene each produce one source per call. Their backend does not turn `count=3` into three outputs.
- RIDA produces one image per item. Yango Pro Illustration produces one image, Yandex Pro produces two; their counts do not come from the generic `count` argument.
- Lucky uses its requested count (one to six). The web normally requests four.
- Scooter Photo and `scooter-3d-2` use `scooter_options.concept_count`; photo planning may need at least one output per selected composition. Cinematic/legacy 3D modes currently generate one concept. Do not select more compositions than the authorized total.

## Video and existing-image operations

See [video workflows](video-workflows.md) for actual fields and submission. UGC and Story have their own prompt writers: send character/role, action/location, speech and authorized references. The returned final prompt includes scene timing, movement and reference numbering. Preserve that prompt and the same manifest during submission; do not replace it with a new agent-written superprompt.

Automotive video prompt generation needs its source image and car identity. Text-first Story needs `characterDescription`, `location`, `country` and `storyIdea`, without an image from the Image tab. Legacy image-based Story still uses `sourceImageUrl`. These are distinct input paths.

Image Edit takes an existing image plus the specific requested change; it does not use Hero/Situation. Regeneration takes a previously finalized production `prompt`; it does not expand a new short scene description. Banner experiments have their own analysis/concept pipeline. Do not apply the short-description rule to a final prompt returned by one of these generator operations.

## Audit basis

Checked against the generator's `/api/generate-image` handler and its mode-specific services, `app.js` request construction, `call_openai`, `call_driver_openai`, automotive/illustration/scooter/RIDA/Lucky prompt writers and `garage_catalog.garage_prompt`. The runtime capability response's `source_input_contract` is the compact field map. Visual quality remains stochastic; matching input fields proves routing parity, not identical pixels across runs.
