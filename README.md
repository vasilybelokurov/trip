# Trip

Vasily Belokurov's trip photo gallery.

**Live site:** https://vasilybelokurov.github.io/trip/

A static replacement for the old `outsane.php` gallery that used to run at
`people.ast.cam.ac.uk/~vasily/trip/`. It keeps the old look and links (grey page,
shuffled wall of every photo, `?goto=` URLs, "oil, canvas, circa …" captions), but
needs no PHP and no server: GitHub builds it and serves it as plain files.

Nothing has to run on your own computer. Photos are added through the github.com
web interface, and GitHub Actions rebuilds and republishes the site on every commit.

---

## Managing photos (all on github.com)

Open https://github.com/vasilybelokurov/trip.

| Task | How |
|---|---|
| Add photos to an existing trip | Click the trip folder → **Add file → Upload files** → drop photos → **Commit changes** |
| Create a new trip | On the repo front page: **Add file → Upload files** → drag a whole folder (e.g. `Rome/`) from Finder → **Commit changes**. The folder name is the trip name shown in the menu. |
| Delete a photo | Open the photo → **⋯** menu (top right) → **Delete file** → **Commit changes** |
| Rename a photo or move it to another trip | Open the photo → pencil icon → edit the path at the top (e.g. `Rome/old.jpg` → `Venice/new.jpg`) → **Commit changes** |
| Delete a whole trip | Delete all its photos; an empty folder disappears from the repo and from the menu |

After each commit the site updates in one to two minutes. Progress is under the
**Actions** tab: a green tick means published, a red cross means the build failed
(click it to see the log).

Rules for photos:

- Formats: `.jpg`, `.jpeg`, `.png` (any letter case). Other files in a trip folder are ignored.
- One level of folders only: `Trip/photo.jpg`. Photos in the repo root or in sub-sub-folders are ignored.
- Folders whose name starts with `.` or `_`, and folders named `thumbs` or `_site`, are ignored.
- Size: originals are shown as they are, so keep them web-sized (the current photos are about
  1000 px wide, 0.3–1.4 MB). The browser upload accepts up to 25 MB per file and 100 files per commit.
- Trips are listed alphabetically; photos inside a trip are sorted by file name.
- The file name is shown in the single-photo caption (`Japan/japan_fire_extinguisher.jpg, oil, canvas, circa 1873`),
  so name files with that in mind.

---

## Using the gallery

| URL | Shows |
|---|---|
| `…/trip/` | Every photo from every trip, shuffled on each load, 7 per row |
| `…/trip/?goto=Japan` | One trip, 3 per row, with its name as a heading |
| `…/trip/?goto=Japan/japan_fire_extinguisher.jpg` | One photo (about 900 px wide; portrait and square ones smaller) with the "oil, canvas, circa <random year 1700–2050>" caption and ← trip → links |

On a single photo: **←**/**→** go to the previous/next photo of the trip (wrapping round),
**Esc** goes back to the trip.

Optional URL parameters carried over from `outsane.php` (combine with `&`):

| Parameter | Effect | Default |
|---|---|---|
| `nx=<1–20>` | Photos per row in a grid | 7 (all), 3 (one trip) |
| `shuffle=0` | Don't shuffle the all-trips page | shuffled |
| `bgcolor=<hex>` | Page background, e.g. `bgcolor=333333` | `aaaaaa` |
| `space=<0–100>` | Gap between photos in px | 8 |
| `width=<200–4000>` | Maximum grid width in px | 1100 |
| `title=<text>` | Browser tab title | `Trip` |

Example: `https://vasilybelokurov.github.io/trip/?nx=5&bgcolor=222222&shuffle=0`

Unknown or malformed `goto` values fall back safely: an unknown trip shows all trips,
an unknown photo in a known trip shows that trip.

---

## How it works

```
 you upload photos on github.com
            │  (a commit to main)
            ▼
 GitHub Actions: .github/workflows/pages.yml
   1. copy the repo (minus .git, .github) into _site/
   2. python build.py _site
        ├─ thumbs/<Trip>/<name>.jpg   480 px thumbnails
        └─ manifest.js                list of trips and photo sizes
   3. upload _site/ and deploy it to GitHub Pages
            │
            ▼
 visitor opens https://vasilybelokurov.github.io/trip/
   index.html loads manifest.js, reads ?goto=, and builds the page in the browser
```

There is no server-side code. GitHub Pages only serves files; all gallery logic
runs in the visitor's browser.

### Files in this repo

| Path | What it is |
|---|---|
| `<Trip>/` (25 folders) | The original photos. These are the only things you normally change. |
| `index.html` | The whole website: HTML, CSS and about 150 lines of plain JavaScript, no libraries. Edit this to change the look or behaviour. |
| `build.py` | Makes the thumbnails and `manifest.js`. Run by GitHub Actions, not by you. |
| `.github/workflows/pages.yml` | The GitHub Actions workflow that runs `build.py` and publishes the site. |
| `.gitignore` | Keeps generated files (`thumbs/`, `manifest.js`, `_site/`) and junk out of the repo. |
| `.nojekyll` | Tells GitHub Pages not to run Jekyll. Not needed with the Actions deploy, kept so the folder also works if published as plain files. |
| `README.md` | This file. |

`thumbs/` and `manifest.js` are **not** in the repo; they are generated on every build
and exist only in the published site.

### `build.py`

- Python 3 with [Pillow](https://pillow.readthedocs.io/).
- Scans `<site dir>/<Trip>/*.{jpg,jpeg,png}`.
- For each photo: applies the camera's EXIF orientation (so phone photos are upright),
  records the displayed width and height, and writes a JPEG thumbnail with longest side
  480 px, quality 75, optimised and progressive. Thumbnails are 10–58 KB (median 35 KB, 9 MB for all 261).
- Writes `manifest.js` as `window.TRIPS = {"Trip": [["file.jpg", width, height], …], …};`
  (a script rather than JSON, so the page also works opened straight from disk).
- Never modifies the original photos.
- Settings at the top of the file: `THUMB_PX`, `THUMB_QUALITY`, `IMAGE_RE`, `SKIP_DIRS`.

### `index.html`

- Reads `window.TRIPS` from `manifest.js` and `?goto=` from the URL.
- `goto` is only ever looked up in the manifest and text is inserted with `textContent`,
  so a crafted URL cannot inject HTML or reach other files.
- Grids use CSS grid with lazy-loaded thumbnails and known image sizes (no layout jumps);
  on screens narrower than 700 px at most 3 per row.
- Single photos use the original file.

### The workflow

`.github/workflows/pages.yml` runs on every push to `main` and can be started by hand
(**Actions → Build and publish gallery → Run workflow**). A build takes about 30 seconds.
If two commits arrive close together, the older build is cancelled and only the newest
is published.

Repository settings this relies on (already set):
**Settings → Pages → Build and deployment → Source: GitHub Actions**.

---

## Changing things

- **Look and layout:** edit `index.html` on github.com (pencil icon) and commit; the site
  updates after the build. Colours and spacing are CSS variables at the top (`--bg`,
  `--space`, `--width`); per-view defaults (7 and 3 per row, 900 px single photo) are in the script.
- **Thumbnail size or quality:** change `THUMB_PX` / `THUMB_QUALITY` in `build.py`.
- **Custom domain:** Settings → Pages → Custom domain.

### Building locally (optional)

Not needed, but useful for previewing a change to `index.html` before committing:

```bash
git clone https://github.com/vasilybelokurov/trip.git && cd trip
python3 -m pip install pillow
python3 build.py                     # writes thumbs/ and manifest.js in place (git-ignored)
python3 -m http.server 8000          # then open http://127.0.0.1:8000/
```

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| New photos don't appear | Wait two minutes and reload (browser cache: Shift-reload). Check the Actions tab for a red cross. Check the extension is `.jpg/.jpeg/.png` and the photo is directly inside a trip folder. |
| Red cross in Actions, "cannot identify image file" | A file named `.jpg` that isn't a real image (or is corrupt). Delete or replace it. |
| Photo appears rotated | Re-export it; the build already applies EXIF orientation, so the pixel data itself is rotated. |
| Site shows the old version | Pages may take a minute after the green tick; then Shift-reload. |
| Warning "Node.js 20 is deprecated" in the log | Harmless notice from GitHub's own Pages actions; bump the action versions in `pages.yml` when newer ones are released. |

Limits of GitHub Pages: published site up to 1 GB, soft bandwidth limit 100 GB/month.
The published gallery is about 145 MB (136 MB of photos plus 9 MB of thumbnails).
Repo limits: 100 MB per file; keep the repo well under 1 GB.

---

## History

- Until 2026 the gallery was `outsane.php` in `~/public_html/trip/` on muon7
  (`people.ast.cam.ac.uk/~vasily/trip/`, a symlink to `/data/vasily/trip/`).
  The department then blocked PHP, so the page returned 403.
- 2026-10-25: rewritten as this static site and moved to GitHub. Compared with the PHP:
  thumbnails instead of full-size images in the grids (the old all-trips page downloaded
  every photo, about 137 MB); `goto` validated (the PHP echoed it unescaped and passed it
  to `opendir`); sorted trips and photos; `.JPG`/`.jpeg`/`.png` handled; landscape single
  photos shown at the intended 900 px (a `$hei = $wid` bug always shrank them to 675 px);
  previous/next navigation; works on phones.
- The photos and the old `outsane.php` are still on muon7 in `/data/vasily/trip/`.
