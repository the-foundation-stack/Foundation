# The Foundation : Brand

Open standards for charitable giving, built once and adopted everywhere. From Gift Aid to Zakat, treated as equals.

This folder is the single source of truth for The Foundation's visual identity. Start with `brand-guidelines.html` (open it in any browser) for the full living reference; everything in it is summarised below for quick use.

## Contents

```
brand/
  brand-guidelines.html          Full interactive guidelines (logo, colour, type, icons, voice)
  logo/
    the-foundation-logo.svg          Horizontal lockup, for light backgrounds
    the-foundation-logo-reversed.svg Horizontal lockup, for dark backgrounds
    the-foundation-mark.svg          Mark only, for light backgrounds
    the-foundation-mark-reversed.svg Mark only, for dark backgrounds
  favicon/
    favicon.ico                  Multi-resolution (16/32/48)
    favicon.svg                  Scalable source
    favicon-16/32/48.png         Individual sizes
    apple-touch-icon.png         180x180
  social/
    social-preview.png           1280x640, GitHub social preview / Open Graph
    social-preview.svg           Editable source
```

Wordmark text in the logo and social files is converted to outlines, so the files render identically anywhere with no font installed.

## The logo

The mark is a foundation in three courses: a broad base, a bearing course, and a clay keystone. Read it as a stable plinth, as a *stack* of standards, or as an upward lift. The keystone always carries the warm accent, the single piece that holds the structure together.

Do:
* Keep the keystone in Clay; set the base courses in Bedrock, or reverse them to Sand on dark surfaces.
* Give the mark clearspace of at least one keystone height on every side.
* Use the mark alone as an avatar, favicon, or social tile.
* Set the wordmark in Fraunces, capitalised as "The Foundation".

Don't:
* Recolour the keystone or apply gradients to the courses.
* Rotate, skew, stretch, or drop-shadow the mark.
* Re-typeset the wordmark in another font or in all-caps.
* Place the mark on a busy photo without a solid containing tile.

## Colour

Earth and stone carry the human work of giving; one deep blue carries the trust of a technical standard. Warmth dominates; the blue and ochre punctuate, they are never the field. A rough balance is Sand 60, Bedrock 22, Clay 10, Lapis 5, Ochre 3.

| Token     | Hex       | Use |
|-----------|-----------|-----|
| Bedrock   | `#1A1A17` | Primary ink, logo, dark surfaces, body text |
| Clay      | `#C75B39` | The keystone. Primary accent, links, highlights |
| Clay Deep | `#A4452A` | Link hover, pressed states, depth |
| Lapis     | `#1F4A57` | Trust accent: code, positive states, charts |
| Ochre     | `#D9A441` | Sparing highlight: generosity, callouts |
| Sand      | `#F4EFE6` | Default background |
| Paper     | `#FBF9F4` | Raised cards and surfaces on Sand |
| Stone     | `#8A8170` | Muted captions, metadata, dividers |

```css
:root{
  --bedrock:#1A1A17; --clay:#C75B39; --clay-deep:#A4452A;
  --lapis:#1F4A57; --ochre:#D9A441;
  --sand:#F4EFE6; --paper:#FBF9F4; --stone:#8A8170;
}
```

## Typography

Three voices, all available on Google Fonts under the SIL Open Font License.

* **Fraunces** : display serif, for headlines and pull-quotes. Weights 600, 700, 900.
* **Hanken Grotesk** : humanist sans, for body copy, labels, and UI. Weights 400 to 700.
* **IBM Plex Mono** : monospace, for the thing we actually make: endpoints, fields, and tokens. Weights 400, 500, 600.

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,900&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

## Iconography

One line system: 24px grid, 1.8px stroke, rounded joins, geometric and quiet. Icons explain, they never decorate. Draw in Bedrock and reserve Clay for the single icon you want noticed. The full set lives in `brand-guidelines.html`.

## Tone of voice

We write the way a good standard reads: plainly, precisely, and without taking a side.

* **Clear before clever.** A volunteer running a one-person charity must understand us as easily as a platform engineer. Short sentences, concrete nouns, every acronym expanded on first use.
* **Even-handed, always.** Gift Aid and Zakat get the same care and the same word count. We never rank traditions, platforms, or causes. Respect is non-negotiable; warmth is welcome.
* **Precise, not rigid.** Specs live or die on precision. We use "must", "should", and "may" in their RFC sense, and we would rather be exact than impressive.
* **Confident, open to being wrong.** A standard is an invitation, not a decree. We state our reasoning, welcome critique, and change our minds in public when the evidence is good.

We say:
* "OCAS describes how a charity exposes donations and tax-relief declarations."
* "Zakat is modelled with all eight Asnaf categories as first-class fields."
* "This is a draft. Tell us where it is wrong."

We don't say:
* "Our revolutionary, best-in-class platform disrupts the giving space."
* "We also support some religious donation types."
* "The specification is final and authoritative."

## Wiring it into the repo

For the org avatar and social preview, in your repository settings:
* Upload `logo/the-foundation-mark.svg` (or a PNG export) as the organisation or repository avatar.
* Under Settings, Social preview, upload `social/social-preview.png`.

For the published docs site, add to the page `<head>`:

```html
<link rel="icon" href="/brand/favicon/favicon.ico" sizes="any">
<link rel="icon" href="/brand/favicon/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/brand/favicon/apple-touch-icon.png">
<meta property="og:image" content="/brand/social/social-preview.png">
```

## Licence

Brand assets in this folder are released under CC BY 4.0. Fraunces, Hanken Grotesk, and IBM Plex Mono are licensed separately under the SIL Open Font License.
