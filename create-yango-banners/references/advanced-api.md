# Advanced API and editable matrices

Advanced tools forward native payloads through fixed, named routes. The upstream backend owns validation and layout/generation behavior. `get_operation_contract(tool_name=...)` reports observed fields/defaults, not a complete validation schema; read the mode guidance for relationships between fields. Keep returned warnings and metadata.

## Performance matrices

Use `render_performance_matrix` for multiple sources, selected image/text combinations, per-size text overrides, co-branding or controls outside `render_banner_pack`.

- `imageSets`: up to ten `{imageUrl, bannerSourceUrl}` objects. Preserve a returned expanded `bannerSourceUrl` when reusing a prepared source.
- `textSets`: up to twenty objects with `title`, `subtitle`, `disclaimer`, `language`, `headlineSize`, `textAlign`, `verticalAlign`, `badgeEnabled`, `badgeTopText`, `badgeBottomText`, `badgeSmallTextPosition`, `badgeShiftX`, `badgeShiftY`, `badgeScale` and `accentColor`. Use `imageIndexes` for selected source combinations.
- For new native performance matrices, explicitly send `badgeShiftY: 100` for `verticalAlign: "text-top"` or `0` for `"logo-top"`; native API omissions retain backend defaults, not the browser's new-set defaults. `100` moves upward to the highest allowed position under the copy block. Copy the same values into saved editor state and per-size overrides. The convenience renderer resolves omissions automatically.
- `badgeBottomText` is the LARGE primary offer: use the complete `15% OFF` or localized offer there, with `badgeTopText: ""` unless a small qualifier or split was requested. `badgeSmallTextPosition` changes the small line's position, not the fields' font hierarchy.

- `sizes`: requested performance size keys. Set `renderMode="matrix"`. Queue requests must fit the upstream limit of 100 combinations; split a larger request into batches.
- `brand`, `logoVariant`, `layoutType`, `driveServiceName`, `coBrandLogoUrl` carry branding. Yandex Go B2B uses `brand="yandex-go-b2b"`, frame layout, locales `en/am/kz/uz/uz-ru/kg/sr/ru`, and yellow `#FFFD72`, navy `#081331`, blue `#BFCCFF` or white `#FFFFFF` accents.
- `imageScale` is a multiplier (1.1 for 110%); `imageShiftX/Y` are pixels. `bannerImageOverrides`, `bannerBadgeOverrides` and `bannerTextOverrides` target `textSetIndex` and `size`. Consult the contract for available override fields.

Do not expect raw matrix rendering to create an archive or editable link. After it succeeds, use `create_banners_zip` with the actual `bannerUrls` and `save_builder_settings` with the corresponding full editor state. Preserve original settings when revising a loaded state.

## CRM matrices

Use `render_crm_matrix` for multiple images, multiple copy options per placement, dates/times, price badges, custom fade or hidden overlays.

- `imageSets` holds source and prepared image URLs.
- Each `placements` entry can be a string or an object containing `placement`, `textOptionIndex`, `title`, `subtitle`, `date`, `time`, `disclaimer`. Inline objects are the reliable way to pass multiple options for one placement.
- Per-option price badge fields: `priceBadgeEnabled`, `priceBadgeTopText`, `priceBadgeBottomText`, `priceBadgeSmallTextPosition` (`top`/`bottom`), `priceBadgePositionX/Y` (0–100), `priceBadgeScalePercent` (70–150). These are separate from the global service badge.
- Global fields include `brand`, `service`, `badgeMode`, `badgeSide`, `badgeText`, `badgeLogoUrl`, `fadeColor`, `textColor`, `layoutType`, `feedTextPosition`, `language`, `hideTextAndBadges` and image position.
- `crmImageOverrides` targets `imageIndex`, `placement` and `textOptionIndex`.
- Retain audience routing: driver communication uses only `drivers-*` carriers. The consumer defaults are not a fallback for drivers.

The queue permits at most 30 placement entries per request. Use `category="crm"` for archives or sharing.

## Builder serialization

`get_builder_settings(parameters={"id":"the-s-value"})` returns the saved `settings`. `save_builder_settings(payload={"settings": complete_state})` creates a new short link. Native rendering fields and browser settings are not identical:

| Native render field | Editor state |
| --- | --- |
| `imageSets[].imageUrl` | `imageUrls`, with `sourceImageUrl` for the primary source |
| `layoutType` | `layout` |
| `imageScale` | `imageScalePercent` = multiplier × 100 |
| `imageShiftX`, `imageShiftY` | `imageShiftXStep` = X/50; `imageShiftYStep` = −Y/50 |
| `coBrandLogoUrl` | `coBrandLogo` |
| `textSets[].badgeScale` | `textSets[].badgeScalePercent` = multiplier × 100 |
| `textSets[].accentColor` | Global `accentPreset` and `accentCustomColor`; one palette per editable pack |
| `textSets[].imageIndexes` | `textSets[].excludedImageUrls` for excluded source URLs |
| Performance override arrays | `imageOverrides`, `badgeOverrides`, `textOverrides` maps keyed `textSetIndex:size` |
| CRM inline placement options | `textOptionsByPlacement` plus `activeTextOptionByPlacement` |
| CRM override array | `imageOverrides` map keyed `imageIndex:placement:textOptionIndex` |

Retain `version:1`, `section:"perf"` or `"crm"`, source URLs, selected placements and all unmodified state fields. For B2B use `accentPreset` `b2b-yellow`, `b2b-navy`, `b2b-blue` or `white`; the custom-color field alone does not override a named preset. CRM settings also store brand/service badge, fade/text colors, language (`badgeLanguage`), layout, feed position and `disclaimerEnabled`.

Use convenience render/revision tools when their fields cover the request; they handle serialization automatically. For source-only rendering with hidden overlays, do not claim the returned link restores a hidden-overlay switch unless that state is actually supported by the browser.

## Media library and operational reads

- `list_library_images` / `list_library_videos`: `parameters.limit` defaults to 60. Pass the returned opaque `next_cursor` as `parameters.cursor` to fetch another page.
- `get_banner_stats`: finalization statistics. `get_queue_metrics` and `get_upstream_readiness`: queue/worker health.
- `get_operation_job`: `parameters.id` plus the original `operation_client_id`. `list_operation_jobs` lists that owner's tasks after a disconnected submission.
- `delete_library_image` / `delete_library_video`: explicit requested deletion by `imageUrl` / `videoUrl`. Do not remove records as routine cleanup.
- `upload_image_advanced` supports the native upload metadata/purpose fields; ordinary attachments use the validated `upload_source_image` convenience tool.

Archives accept returned URLs and, where supported, `{url, folder, name}` entries. Pass actual backend paths; never turn a guessed filename into an asset URL. Yandex Disk publishing remains an explicit user-requested operation.
