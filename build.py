#!/usr/bin/env python3
"""Static replacement for outsane.php.

Scans <trip_dir>/<Folder>/*.jpg|jpeg|png, makes thumbnails with Pillow,
and writes into <trip_dir>:
  thumbs/<Folder>/<stem>.jpg   thumbnails (longest side THUMB_PX)
  manifest.js                  window.TRIPS = {folder: [[file, w, h], ...]}
  index.html                   the gallery page (copied from this directory)
Originals are never modified. Normally run by GitHub Actions on every push
(.github/workflows/pages.yml); locally it needs `pip install pillow`.

Usage: python3 build.py [trip_dir]   (default: this script's directory)
"""
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

THUMB_PX = 480
THUMB_QUALITY = 75
IMAGE_RE = re.compile(r"\.(jpe?g|png)$", re.IGNORECASE)
SKIP_DIRS = {"thumbs", "_site"}
HERE = Path(__file__).resolve().parent


def process(src, dst):
    """Return the displayed (w, h) of src and write its thumbnail to dst."""
    with Image.open(src) as im:
        # Respect the camera's orientation flag, as browsers do.
        im = ImageOps.exif_transpose(im)
        w, h = im.size
        if not (dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime):
            dst.parent.mkdir(parents=True, exist_ok=True)
            im = im.convert("RGB")
            im.thumbnail((THUMB_PX, THUMB_PX), Image.LANCZOS)
            im.save(dst, "JPEG", quality=THUMB_QUALITY, optimize=True, progressive=True)
    return w, h


def main(trip_dir):
    trip = Path(trip_dir).resolve()
    trips = {}
    for folder in sorted(p for p in trip.iterdir()
                         if p.is_dir() and p.name not in SKIP_DIRS
                         and not p.name.startswith((".", "_"))):
        files = sorted(f for f in folder.iterdir() if f.is_file() and IMAGE_RE.search(f.name))
        if not files:
            continue
        entries = []
        for f in files:
            # Thumbnails are always JPEG, named after the original's stem.
            w, h = process(f, trip / "thumbs" / folder.name / (f.stem + ".jpg"))
            entries.append([f.name, w, h])
        trips[folder.name] = entries

    (trip / "manifest.js").write_text(
        "window.TRIPS = " + json.dumps(trips, separators=(",", ":"), ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    if trip != HERE:
        shutil.copyfile(HERE / "index.html", trip / "index.html")
    n = sum(len(v) for v in trips.values())
    print(f"{len(trips)} folders, {n} images -> {trip}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit(__doc__)
    main(sys.argv[1] if len(sys.argv) == 2 else HERE)
