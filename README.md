# Trip

Photo gallery, served by GitHub Pages at https://vasilybelokurov.github.io/trip/.
Static replacement for the old `outsane.php` gallery.

- One folder per trip, holding `.jpg`/`.jpeg`/`.png` photos.
- `index.html` is the whole site; it reads `manifest.js` and routes on `?goto=<Folder>` or `?goto=<Folder>/<file>`.
- Options from the old script still work: `nx`, `space`, `width`, `shuffle=0`, `title`, `bgcolor`.

## Adding photos

```bash
cp ~/somewhere/*.jpg NewTrip/
python3 build.py          # macOS: uses sips; writes thumbs/ and manifest.js
git add -A && git commit -m "Add NewTrip" && git push
```
