# Current CRM controls

Read `get_banner_capabilities` before use. Convenience tools use snake_case;
`render_crm_matrix` and builder settings use the native fields below.

## Brand and marks

CRM brands are `yango`, `yandex-go`, `rides-for-business`. Business is a brand, not
an ordinary service icon. New Business packs use `brand="rides-for-business"`;
legacy Go + Business service links remain supported. Business pill languages:
`en`, `ru`, `am`, `kz`, `kg`, `uz`, `sr`. Set `business_pill_language` explicitly;
`auto` is legacy country resolution and needs an approved `business_country` or
source-country metadata. Copy language does not choose the pill language.

`badge_mode`: badge, icon, logo, none. Left/Center/Right `badge_side` moves the
complete mark group without reversing its contents. Yango Fullscreen can use
`fullscreen_badge_side`; Go and Business share `badge_side`. Main S has no mark.
The renderer owns current brand geometry, lettering and disclaimer placement.

For Go Taxi, Intercity, Scooters and Charger use `go_offer` (`goOffer` natively):

- `mode`: legacy, badge (custom text), icon, offer (Icon + offer), none.
- `type`: number (no sign), percent, currency.
- `value`: no-sign allows 1–160 printable characters, including text. Percent and
  currency allow up to nine integer digits and two decimals; percent may exceed 100.
- `currency`: ₸, soʻm, с̲, ֏, ₾, din., lei. An explicit currency needs no country.
  Legacy country-derived currency remains supported.
- `text`: custom badge wording; `color`: auto, yellow, black, white, green, red,
  lavender, blue, pink. Intercity is always purple. Charger Auto uses blue in
  Kazakhstan/Kyrgyzstan and yellow elsewhere; Taxi/Scooters default yellow.

Use an optional `country` for market-dependent automatic treatment. Do not invent
one for explicit currency offers. Example `go_offer` value:

```json
{"mode":"offer","type":"currency","currency":"₸","value":"1500","color":"yellow"}
```

Do not split a Go offer into the separate legacy `price_badge_*` controls or
replace it with the service name. Revisions merge only supplied `go_offer` fields
with the existing configuration. `badge_mode="logo"` uses `badge_logo_url`.
Text color supports auto/black/white/yellow. Go Yellow is `#FFEA00`, Business
Yellow `#FFFD72`; Go legal copy stays white with Yellow and is fully opaque.

## Carriers and position

Additional placements: `go-stories` 1080×1920 (Go eligible services only),
`ticket-tall` 981×600 (Yango/Go, all services), `drivers-bottom-sheet` 360×210.
Keep driver communication within `drivers-*` placements. Existing Fullscreen,
Promo card and Ticket are 1440×2560, 1551×950 and 981×450 respectively.

Promo card supports `promo_badge_position` top/bottom independently of horizontal
alignment. Saved key: `promoBadgePosition`; native placement key: `badgePosition`.
Omission keeps the native default (Go/Business top, Yango bottom); revisions
preserve a saved position. This moves the whole badge/icon/offer/Business pill.

Tall ticket automatically removes the original source background through a cached
Clipdrop mask. The 981×450 photo card starts at y=150 on a 981×600 transparent
canvas; original photo and cutout share Scale/X/Y. Keep the original source and
reuse it across clean/text variants and position changes. No manual foreground
upload is needed. Other formats may still use expanded sources in a mixed pack.
An ambiguous extraction failure is not permission to repeat a paid submission.

## Shared legal copy and saved state

Use the exact supplied disclaimer, explicitly enabled, or explicit omission.
`disclaimer_enabled=false` keeps stored legal copy disabled during revisions.
An enabled but mixed shared field resolves to empty; hidden legacy per-carrier
values must not reappear on export. Fill the shared value consistently before
rendering; never insert default/test legal text. Native placement objects carry
only the resolved enabled disclaimer. Clean outputs hide all overlay legal copy.

Preserve `goOffer`, `businessCountry`, `businessPillLanguage`, `fullscreenBadgeSide`,
`promoBadgePosition`, `disclaimerEnabled`, text options and crop overrides in saved
settings and render requests. For unsupported convenience changes read/save the
complete state through the native matrix workflow. Do not discard unfamiliar fields.

Each output may include `preview_layout` version 1 and its exact `source_image_url`.
The web editor uses these bounds for local schematic positioning. MCP keeps the
backend as final renderer: inspect the actual rendered file for copy/brand checks.
Old results without geometry need a render before live positioning is available.
