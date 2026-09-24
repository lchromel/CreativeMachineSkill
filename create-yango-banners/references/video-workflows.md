# Video: Story, UGC, RIDA and Edit

Use this MCP's current `get_video_capabilities` and typed tools. The service writes prompts and runs its configured Seedance integration. An arbitrary prose brief does not replace settings. Do not route modern video through legacy `generate_video`, generic `start_video_generation`, or automotive image-to-video tools.

## Gather a complete setup

Read capabilities and collect the following choices from the request and attachments. Ask one concise grouped question for missing material choices. You may offer 10 seconds and Balanced dynamics when useful. **For every new video request without a stated format, ask the user to choose PERF or SMM before writing a prompt or submitting a video. There is no format default.** Preserve explicit choices. Do not ask again for information already given. Explain optional references and allow an explicit “none”; do not silently discard attached files or assume every image is a portrait.

| Choice | Exact field / values |
| --- | --- |
| Mode | `mode`: `ugc` for a spoken testimonial; `standard-story` for a human narrative; `rida-story` for RIDA zebras |
| Duration | `durationSeconds`: **10, 15, 20, 25, 30**, required in every modern mode |
| Format | Required explicit choice: PERF maps to `outputType="performance"` = square 1:1; SMM maps to `outputType="smm"` = vertical 9:16; native 1080p. Ask when unspecified; do not infer from destination, mode or examples |
| Dynamics | `videoDynamics`: **0 Melodrama, 1 Drama, 2 Balanced, 3 Adventure, 4 Action**; changes writing, pacing and camerawork |
| Human casting | `country`, `role` (`user`/`driver`), `gender` (`women`/`men`, required without a portrait), `age` (integer **18–70**, required without a selected portrait), `portraitImageUrl` if keeping a supplied/chosen identity |
| Vehicle | `transportLabel`: exact class label for the selected country from `get_source_catalog(catalog="vehicles")`; omit for no catalogue vehicle. Country/class selects the real approved livery and moto helmet, not a made-up car reference |
| Merchandise | `merchIds`: explicit list, including `[]` for none. Read `get_source_catalog(catalog="video-references")`; values **mug, tote, phone-case, bucket-hat, cap, sunglasses, neon-sign**. Cap and bucket hat are mutually exclusive |
| Setting | `location` and/or `locationImageUrl`; UGC requires at least one, Story can derive a setting from its idea |
| Voice | UGC `speech` or uploaded `voiceoverReferenceUrl`; Story/RIDA narration fields below |
| Phone screen | UGC `screenReferenceType` + `screenReferenceUrl`; Story `screenImageUrl`; RIDA `ridaInterfaceImageUrl` |

Use `get_source_catalog(catalog="ridehail-branding")` to inspect the service's current approved vehicle references. For custom `brandingImageUrl`, omit `transportLabel`: a selected catalogue class overrides custom branding at the API. Tell the user when their requested custom livery conflicts with that choice. When selecting Oman transport, provide gender even with a portrait: the service uses it to select the correct approved livery. Treat portrait identity as authoritative; do not describe a different age or gender than the selected person.

Illustrative Ghana UGC format mapping: after confirming the live Ghana tariff label is `Moto`, a user-selected PERF format gives `mode="ugc"`, `country="Ghana"`, `transportLabel="Moto"`, `outputType="performance"` (square 1:1). A user-selected SMM format changes only `outputType` to `"smm"` (vertical 9:16). This is a partial setup, not a call: obtain the actual user's age and gender (or selected portrait), setting, speech or uploaded audio, duration, dynamics and explicit merchandise choice before building complete settings.

Before writing, briefly show the selected setup, including merch and each attachment's role. This is a reviewable description, not an extra permission gate when the user has already authorized the work. Ask about actual ambiguity rather than inserting invented defaults for casting, speech or attachment roles.

## Uploads and portrait selection

Images: upload user-provided images through the MCP image upload tools. Use the returned local URL as the relevant portrait/location/screen/branding field. `upload_image_advanced` accepts native `imageData`, `fileName` and `purpose="ugc-portrait"` for portrait uploads.

Audio: `upload_audio(media_base64, file_name, mime_type)` accepts MP3/WAV, **2–15 seconds**, **15 MB**. Preserve the returned `audio_public_url` including its temporary token. It is a speech reference, not an arbitrary background music attachment.

UGC screencast: `upload_video(..., purpose="ugc-reference")`, **2–15 seconds**, MCP maximum **100 MB**; use `video_public_url`. Set `screenReferenceType="video"`. For a screenshot use `"image"`. A local filename, chat attachment handle or video library URL is not a substitute for the returned public reference URL. Upload an expired temporary reference again and rewrite the prompt with the new setup.

For a new identity, use `generate_video_portraits(settings={role,country,age,gender,details,characterDescription,merchIds,avoidPrompts})`; required casting fields are role/user-or-driver, country, age, gender and merchIds. This is a paid image operation returning candidates. Show them and let the user select one; do not silently choose an unrelated face. Save the selected candidate with `save_video_portrait(settings={imageUrl,country,label,prompt,casting})`, retaining the original casting settings. Use its portrait URL in the video setup. A new portrait is optional: text casting and an existing/uploaded portrait are supported.

## Exact mode settings

All modern calls use a **`settings` object**, not `payload`. Unknown fields fail validation. Read the returned JSON schema for the current complete contract.

**UGC** adds `role` (`user` or `driver`), `characterDescription` (optional subject details), `location`, `locationImageUrl`, `speech`, `voiceoverReferenceUrl`, `brandingImageUrl`, `screenReferenceType` and `screenReferenceUrl` to the shared human fields. Speech or audio is required. Spoken text must fit **2.4 words per second**. Screen type and URL must appear together. A portrait is optional; without it, age is required. Put actual spoken words in `speech`, environment in `location`, and wearable choices in `merchIds`, not all together in a generic prompt.

**Story** adds required `storyIdea` and `characterDescription`, plus optional `location`, `locationImageUrl`, `screenImageUrl`, `brandingImageUrl`, `brandingLabel`, `voiceoverLanguage`, `voiceoverWish`, `voiceoverText`, `voiceoverReferenceUrl`. Describe the selected cast and action in characterDescription; keep the narrative in storyIdea. There is no requirement for an Image-tab source image. A selected portrait controls identity. Empty screenImageUrl uses the service's default phone artwork. Voiceover language defaults to English; preserve a requested language explicitly. voiceoverWish directs new copy; voiceoverText retains existing speech; uploaded audio supplies the exact spoken performance.

**RIDA** uses only shared duration/output/dynamics plus `storyIdea`, `ridaRoles` (`["user"]`, `["driver"]`, both, or `[]`), `ridaTransport` (`car`, `moto`, `none`), `ridaLocationMode` (`blue` or `natural`), optional `ridaInterfaceImageUrl` and narration fields `voiceoverLanguage`, `voiceoverWish`, `voiceoverText`, `voiceoverReferenceUrl`. At least one mascot or vehicle is required. Natural location requires `country`, with optional `location` wishes. Blue uses the branded blue set and no country/location fields. RIDA has its own mascot/vehicle assets; do not attach human portraits, merch or human transport classes to this mode.

## Write, review and submit the same setup

1. Call `write_video_prompt(settings=...)`. Preserve its **`settings_digest`** and the complete settings object. It may return a queued operation: poll `wait_for_operation(operation_id, operation_client_id)` until succeeded and take the full `result.prompt` (and `voiceover_text` when present).
2. Show the complete scenario and spoken text, not just the opening line. Preserve the server's reference manifest and numbering. Apply the user's existing authorization; request a choice only when unresolved settings or requested scenario review require it.
3. For Story/RIDA revisions, call `write_video_prompt` with the same settings plus **both** `current_prompt` (full scenario) and `revision_comment`. Use the new complete result. UGC uses a new prompt-writing call with the revised structured setup; it does not support these revision arguments.
4. Call `submit_video(settings=the_same_object, prompt=the_complete_final_prompt, settings_digest=the_returned_digest)`. Do not swap duration, portrait, merch, transport, screen, audio or dynamics between writing and submitting. Changed settings require a new writing call and digest. The digest checks settings continuity; do not compute or invent it yourself.
5. Poll the returned operation; a queued response is not success. Successful results include the stored raw video. The account token owns the generation task/history; it must have Video permission. No separate login/password is needed. In account mode, the outer operation is authoritative even if result metadata includes a legacy job_id; do not poll legacy job endpoints.
6. **After every successful generation, show the actual video and offer Edit.** Example: “Видео готово. Добавить логотип, пэкшот поверх видео или отдельным финалом, текст и субтитры?” Mention options appropriate to the user's brand. If they already requested these edits, proceed with those settings. Otherwise offer them without automatically adding overlays or triggering paid transcription.

The server constructs references in its own fixed order: portrait (if selected), location, approved vehicle and helmet as applicable, phone image, then selected merch in catalogue order. UGC screen video and audio have separate video/audio numbering; Story uses its phone screen/default. RIDA uses user, driver, selected vehicle, optional interface, then audio separately. Keep the generated manifest rather than manually inventing @Image numbers. Source AIGC registration is handled by the service.

For safe retries you may supply `operation_client_id` (32 lowercase hexadecimal characters) and `request_id` together. Retain both and the exact request. Never start another paid task after an ambiguous response. Inspect existing tasks and resume only when `can_resume=true`, preserving the original operation ID and owner ID. Report a failure or unknown provider outcome honestly.

## Edit after generation

Use **`edit_video(settings=...)`** with the successful raw **`videoUrl`**. This reuses the existing video. Gather branding placement, final message and subtitle choice; do not silently render the default Yango logo for another brand.

| Field | Values / behavior |
| --- | --- |
| `videoUrl` | Existing generated or uploaded video library URL |
| `outputType` | Required `performance`: 1920×1080, 1080×1080, 1080×1920; `smm`: 1080×1920 only |
| `watermark` | Required `none`, `yango-logo`, `yango-icon`, `yango-pro-logo`, `yango-pro-icon`, `rides-for-business-logo`, `rida-logo`, `rida-icon` |
| `watermarkLogoVariant` | Rides for Business locale `en`, `pt`, `fr`, `az`, `ru`, `es`, `pe`, `ar`, `ur`, `tr` |
| `watermarkPosition` | `top-left` (default), `top-right`, `bottom-left`, `bottom-right` |
| `packshotMode` | Required `none`, `overlay` (over video), `append-1` (one-second ending), `append` (two-second ending) |
| `packshotLine` | Final message, max 180 characters; specify requested copy, service default “Download the app” |
| `packshotDisclaimer` | Final legal text, max 360 characters |
| `videoDisclaimer` | Full-video legal text, max 360 characters |
| `autoSubtitles` | False by default; true opts into paid automatic transcription |
| `subtitleCues` | Optional manual array `{start,end,text}`, seconds in the original source timeline; up to 200, each >=0.1s, no overlaps, text <=500 chars; alternative to autoSubtitles |
| `keepRanges` | Optional 1–50 `[start,end]` ranges, source seconds in montage order, each >=0.1s, no overlaps |
| `replacement` | Optional existing fragment `{videoUrl,start,in,out}`: insertion time in source and fragment in/out times |

RIDA uses the supplied two-second outro: `append-1` is unavailable with `rida-logo`/`rida-icon`; choose `append`, `overlay` or `none`.

Poll the edit operation and show its successful deliverables. Preserve both the raw original and edited versions. Automatic subtitles may incur transcription cost; editing does not restart Seedance generation.

For a requested pixel/content repair, use `repair_video_fragment(settings={videoUrl,selection:[start,end],prompt,referenceImageUrls})`. This **does** start a paid video operation. Select 0.1–30 seconds from a library source of at least 4 seconds; attach at most 8 previously uploaded images. @Video1 denotes the source, @Image1..N follow that list. The service adds context for short selections and checks returned timing. A failed repair must not be blindly retried. Preview the returned fragment with `preview_video_replacement(video_url,replacement)` before a requested export. `detect_video_scenes(video_url)` finds cuts in existing videos up to 300 seconds without an AI provider call.

Create a ZIP with `create_videos_zip` only when export/download is requested. Share using `share_videos_to_yandex_disk` only when requested. `record_video_download` records an actual finalized download, not generation success. Return the real saved media and sharing URLs.
