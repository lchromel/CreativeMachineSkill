# Video workflows

Use Creative Machine's backend video tools. Its current integration uses Seedance 2.5; do not silently replace it with a different provider or an unrelated Seedance 2.0 workflow.

All advanced POST tools take `payload` with native field names. Read `get_operation_contract(tool_name=...)` for the selected tool. Follow outer `operation_id` + `operation_client_id` to completion, then any returned legacy video/storyboard `job_id` using the appropriate GET tool and `parameters.jobId`.

## Standard and automotive

- Automotive: `generate_video_prompt` uses `imageUrl`, `carModel`, optional `colorName` and `basePrompt`.
- Ride-hailing story: `generate_ridehail_video_scenario` uses `imageUrl`, `brief`, `voiceoverText`, `durationSeconds`, `country`, `transport`.
- For a storyboard workflow, `generate_ridehail_storyboards` or `start_ridehail_storyboards` takes `imageUrl` and `story`. Select a returned board, then use `prepare_ridehail_video_storyboard` when that workflow requires a prepared source.
- `generate_ridehail_seedance_prompt` uses `storyIdea`, `sourceImageUrl`, and optional screen, vehicle-branding and voiceover references. Preserve the returned manifest and complete prompt.
- Submit through `start_video_generation` with `imageUrl`, `prompt`, the intended `mode`, `durationSeconds` and `brand`. Use `promptIsFinal=true` for a finalized prompt that should remain unchanged. Story modes include `standard-story`, `ride-hailing-storyboard` and `ride-hailing-storyboard-safe`; retain source/safe-storyboard URLs returned by preparation.

Ordinary Standard generation uses 10 or 15 seconds. The backend additionally permits 20/25/30 seconds for `standard-story` and UGC; match the duration used when writing the prompt. Resolution and model endpoint are configured by the generator, not arbitrary MCP fields.

## UGC

1. Use `generate_ugc_portraits` with role, country, age, gender, details and optional `avoidPrompts`. Inspect candidates and retain the chosen identity. `save_ugc_portrait` saves the selected `imageUrl` with optional label/prompt/country.
2. Upload requested references. `upload_video` accepts raw `media_base64`, `file_name`, `mime_type` and `purpose="ugc-reference"`; use its `video_public_url`. Reference video is limited to 15 seconds. Ordinary library video supports up to 100 MB/600 seconds.
3. `upload_audio` accepts an MP3/WAV voiceover up to 15 MB and 2–15 seconds. Use the returned `audio_public_url`. Temporary public reference URLs must be reused exactly, including tokens.
4. `generate_ugc_video_prompt` takes `portraitImageUrl`, role/country/age/gender, location/speech, `durationSeconds`, `outputType` and optional `locationImageUrl`, `brandingImageUrl`, `screenReferenceType` + `screenReferenceUrl`, `voiceoverReferenceUrl`.
5. Use the same reference set for `start_video_generation`: `mode="ugc"`, chosen portrait as `imageUrl`, returned full `prompt`, and the same duration/output/reference fields. `outputType="smm"` makes 9:16; `performance` makes 1:1. `screenReferenceType` is `image` or `video` and must match its URL.
6. Do not reorder or add reference tokens after prompt generation. The backend validates the manifest, registers the AIGC source where required, generates and stores a raw video.

Video submission requires the MCP server's `YANGO_VIDEO_GENERATION_PASSWORD` to match the generator's configured video password. Do not ask the user to put credentials into `payload`. Report a missing configuration clearly; other tools remain usable.

## Edit and export existing video

Use `remix_video` with an existing `videoUrl`. This is a separate operation from generation and accepts:

| Field | Values / purpose |
| --- | --- |
| `watermark` | `yango-logo`, `yango-icon`, `yango-pro-logo`, `yango-pro-icon`, `rides-for-business-logo` |
| `watermarkLogoVariant` | Locale for the Rides for Business wordmark |
| `watermarkPosition` | `top-left`, `top-right`, `bottom-left`, `bottom-right` |
| `packshotMode` | `append` or `overlay` |
| `packshotLine`, `packshotDisclaimer` | Requested final brand message and legal copy |
| `autoSubtitles` | Boolean; defaults to true |

The exporter produces 1920×1080, 1080×1080 and 1080×1920 deliverables, preserving source audio and applying the requested branding/subtitles. Inspect returned deliverables rather than assuming raw generation includes these overlays.

Use `create_videos_zip` for existing `videoUrls`. Use `share_videos_to_yandex_disk` with `videoUrls` and `packageName` only for a requested publication; return its real public folder link. `record_video_download` records actual download finalization and must not be used merely because generation finished.

## Interrupted tasks

Poll the existing task. Resume only when `can_resume=true` and continuation is authorized, using `resume_operation` with the original owner ID. A failed/interrupted task without a recoverable provider ID does not permit an automatic new paid submission. Preserve task IDs in the user-facing explanation if recovery needs follow-up.
