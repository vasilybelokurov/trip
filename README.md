# Trip

Photo gallery, served by GitHub Pages at https://vasilybelokurov.github.io/trip/.
Static replacement for the old `outsane.php` gallery.

- One folder per trip, holding `.jpg`/`.jpeg`/`.png` photos.
- `index.html` is the whole site; it reads `manifest.js` and routes on `?goto=<Folder>` or `?goto=<Folder>/<file>`.
- Options from the old script still work: `nx`, `space`, `width`, `shuffle=0`, `title`, `bgcolor`.
- Thumbnails (`thumbs/`) and `manifest.js` are not in the repo: GitHub Actions
  (`.github/workflows/pages.yml`) runs `build.py` on every push and publishes the result.

## Adding photos (all on github.com)

- Existing trip: open the trip folder, then **Add file → Upload files**, drop the photos, **Commit changes**.
- New trip: on the repo front page, **Add file → Upload files**, and drag a whole folder (e.g. `Rome/`) from Finder;
  the folder name becomes the trip name.
- Delete or rename: open the photo, use the **⋯** menu (delete) or the pencil (rename the path).

The site updates one to two minutes later; progress is under the **Actions** tab.
