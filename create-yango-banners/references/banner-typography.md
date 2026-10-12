# Banner line breaks and short last lines

Adapted from Jakub Krehel's `better-typography`, sections “Wrap deliberately” and
“Wrapping and punctuation”. The transferable principles are balanced heading
lines (`text-wrap: balance`), avoiding a lone short final word in descriptions
(`text-wrap: pretty`), and keeping compact labels/amounts together (`nowrap`).
These CSS properties are analogies, not MCP parameters: Creative Machine renders
banner files on the backend. This guide is self-contained; another installed
skill is not required at runtime.

## Compose by meaning and visible width

Preserve the approved wording, numbers, offer conditions, emphasis and legal copy.
Use actual newlines between words at phrase boundaries. Judge the rendered line
width in the selected font, not character count. Keep a short headline on one line
when it fits; for multiple lines, aim for a coherent block rather than one full
line followed by a tiny tail. A single short final word is a reason to rebalance,
not a reason to delete a word or invent copy. A deliberate one-word headline or an
explicitly requested break can remain.

Keep a short preposition or conjunction with the phrase that follows it. Keep
numbers with units/currency/percent and qualifiers with the offer they modify.
Keep compact badge copy together when it fits. Avoid discretionary hyphenation
inside words in short advertising headings; prefer a different break between
words. Do not insert HTML entities (`&nbsp;`, `&shy;`), CSS or HTML into MCP copy.
The backend may wrap again if a manually chosen line is too long.

Example: the complete headline “Комфортные поездки по городу” should not be sent as
“Комфортные поездки по” plus the lone word “городу”. A better candidate is:

```text
Комфортные поездки
по городу
```

The complete offer “Скидка 30% на первые 3 поездки” can be tested as:

```text
Скидка 30%
на первые 3 поездки
```

These examples preserve the exact words; the selected font and carrier determine
whether they actually fit. Do not enforce equal lengths if it breaks the meaning.

## Check the rendered carrier

Inspect every requested size/placement at a useful viewing scale, including
square, landscape and vertical outputs. Check for a short last-line tail, stranded
prepositions, split amounts, unintended word breaks, clipping and collisions with
logo, badge or disclaimer. Centered text especially needs optical balance. A
schematic `preview_layout` carries bounds, not readable glyphs; assess wrapping on
the actual banner image.

First move the break to a better phrase boundary, then use size-specific copy
breaks and supported headline sizes if needed. Keep a user-fixed size/line break
unless adjustment is authorized. Performance supports S/M/L/XL; CRM typography is
placement-specific. Use native `bannerTextOverrides` plus saved `textOverrides` for
size-specific performance changes, or separate renders. CRM uses placement text
options. Save the same full multiline values in the editor state.

Re-render through MCP with the same source and `create_zip=false`; retain CRM's
with-text/without-text pair. Do not regenerate imagery for a text-wrap correction.
Never shorten approved offer conditions or change legal wording to make it fit.
If inspection is unavailable, state that visual wrapping is unverified.
