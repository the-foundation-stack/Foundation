# The Foundation : Brand Kit, Install and Usage

Everything you need to put the brand live. Read top to bottom the first time. Each terminal block is meant to be run one block at a time; after each one, glance at the output before moving on.

If you only do two things, do these: upload `avatar/avatar-512.png` as the org avatar, and upload `social/social-preview.png` under repository Settings, Social preview. Everything else is polish.

---

## A. What is in this kit

```
brand/
  README.md                  The brand spec (colour tokens, fonts, voice). Lives in the repo.
  INSTALL.md                 This file.
  brand-guidelines.html      Open in a browser for the full visual reference.
  logo/
    the-foundation-logo.svg            Horizontal lockup, light backgrounds
    the-foundation-logo-reversed.svg   Horizontal lockup, dark backgrounds
    the-foundation-mark.svg            Mark only, light backgrounds
    the-foundation-mark-reversed.svg   Mark only, dark backgrounds
  avatar/
    avatar-512.png             Upload this as the GitHub org or repo avatar
    mark-512-transparent.png   Mark only, transparent, for slides or docs
  favicon/
    favicon.ico                16, 32, 48 in one file
    favicon.svg                Scalable source
    favicon-16/32/48.png       Individual sizes
    apple-touch-icon.png       180 x 180
  social/
    social-preview.png         1280 x 640, GitHub social preview and Open Graph
    social-preview.svg         Editable source
```

The wordmark in every logo and social file is converted to vector outlines, so the files look identical on any machine with no font installed.

---

## B. Preview the guidelines (30 seconds, no terminal)

1. Double-click `the-foundation-brand.zip` to unzip it. You get a folder called `brand`.
2. Open the `brand` folder and double-click `brand-guidelines.html`.
3. It opens in your browser. You will see the logo, colour palette, fonts, icon set, and tone of voice. You need an internet connection the first time so the fonts can load.

---

## C. Add the brand folder to the repo (terminal)

Your repo is the monorepo that already contains `open-charity-api`. From your earlier work that is:

```
/Users/mohamedhhussain/Projects/The-Foundation/Foundation/Foundation
```

### Block 1 : confirm you are in the right place

```bash
cd /Users/mohamedhhussain/Projects/The-Foundation/Foundation/Foundation
ls
```

You should see `open-charity-api` in the list (along with README.md, LICENSE, and so on). If you do, you are in the repo root. If you do not see `open-charity-api`, stop and tell me what `ls` shows, because the path has moved.

### Block 2 : pull the latest, then copy the brand folder in

```bash
# make sure local is in sync with GitHub first
git pull

# copy the unzipped brand folder from Downloads into the repo root
cp -R ~/Downloads/brand .

# check it landed
ls brand
```

`ls brand` should show `README.md`, `brand-guidelines.html`, `logo`, `avatar`, `favicon`, `social`, and this `INSTALL.md`.

If `cp` reports that `~/Downloads/brand` does not exist, it means the zip unzipped somewhere else. Run `ls ~/Downloads | grep -i brand` to find it, then adjust the path in the `cp` command.

### Block 3 : commit and push

```bash
git add brand
git commit -m "Add brand kit: logo, favicon, social preview, guidelines"
git push
```

That is the brand folder live in the repo. Confirm by visiting:
`https://github.com/the-foundation-stack/Foundation/tree/main/brand`

---

## D. Set the GitHub avatar (browser, cannot be done from git)

GitHub avatars must be a PNG or JPG, which is why `avatar-512.png` exists.

For the organisation avatar:
1. Go to `https://github.com/organizations/the-foundation-stack/settings/profile`
2. Under **Profile picture**, click **Upload a photo**
3. Choose `brand/avatar/avatar-512.png`
4. GitHub will let you crop. Leave it centred, then save.

(If you would rather set it on the repo itself rather than the org, GitHub does not support per-repo avatars; the org avatar is what shows.)

---

## E. Set the social preview (browser)

This is the image people see when the repo is shared on Slack, X, LinkedIn, and so on.

1. Go to `https://github.com/the-foundation-stack/Foundation/settings`
2. Scroll to **Social preview**
3. Click **Edit**, then **Upload an image**
4. Choose `brand/social/social-preview.png`

Done. Share the repo link anywhere to see it.

---

## F. Wire the favicon and preview into the docs site (optional)

This applies to the published docs landing page (the `docs-site/index.html` that deploys to `the-foundation-stack.github.io/Foundation/`). It makes the browser tab show the keystone icon and makes link previews use the social card.

Open `docs-site/index.html` and paste these lines inside the `<head>` section:

```html
<link rel="icon" href="/Foundation/brand/favicon/favicon.ico" sizes="any">
<link rel="icon" href="/Foundation/brand/favicon/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/Foundation/brand/favicon/apple-touch-icon.png">
<meta property="og:title" content="The Foundation">
<meta property="og:description" content="Open standards for charitable giving.">
<meta property="og:image" content="https://the-foundation-stack.github.io/Foundation/brand/social/social-preview.png">
```

Note the `/Foundation/` prefix in the paths. GitHub Pages for a project repo serves the site under that subpath, so the leading `/Foundation/` is needed. If you ever move to a custom domain at the root, drop the `/Foundation` prefix.

Commit and push the same way as Block 3, wait two or three minutes for the deploy, then hard-refresh the page (Cmd + Shift + R) to see the new tab icon.

---

## G. Where each file goes, at a glance

| File | Goes where |
|------|------------|
| `avatar/avatar-512.png` | Org settings, Profile picture |
| `social/social-preview.png` | Repo Settings, Social preview |
| `favicon/*` | Referenced from `docs-site/index.html` head |
| `logo/*.svg` | README badges, slides, the docs site header |
| `brand-guidelines.html` and `README.md` | Stay in the repo `brand` folder as the reference |

---

## Need a raster version of the lockup?

The lockups are SVG. If a tool needs a PNG (for example a slide deck), open the SVG in any browser, or tell me the size you need and I will export it.

If you want the colour palette changed, or the wordmark set in a different display face, say so and I will regenerate the entire kit in one pass so everything stays consistent.
