#!/usr/bin/env python3
"""Static replacement for outsane.php.

Scans <trip_dir>/<Folder>/*.jpg|jpeg|png, makes thumbnails with macOS sips,
and writes into <trip_dir>:
  thumbs/<Folder>/<file>   thumbnails (longest side THUMB_PX)
  manifest.js              window.TRIPS = {folder: [[file, w, h], ...]}
  index.html               the gallery page (copied from this directory)
Originals are never modified.

Usage: python3 build.py [trip_dir]   (default: this script's directory)
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

THUMB_PX = 480
THUMB_QUALITY = 75
IMAGE_RE = re.compile(r"\.(jpe?g|png)$", re.IGNORECASE)
HERE = Path(__file__).resolve().parent


def image_size(path):
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    w = int(re.search(r"pixelWidth: (\d+)", out).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", out).group(1))
    return w, h


def make_thumb(src, dst):
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["sips", "-Z", str(THUMB_PX), "-s", "format", "jpeg",
         "-s", "formatOptions", str(THUMB_QUALITY), str(src), "--out", str(dst)],
        check=True, capture_output=True,
    )
    return True


def main(trip_dir):
    trip = Path(trip_dir).resolve()
    trips = {}
    made = 0
    for folder in sorted(p for p in trip.iterdir()
                         if p.is_dir() and p.name != "thumbs" and not p.name.startswith(".")):
        files = sorted(f for f in folder.iterdir() if f.is_file() and IMAGE_RE.search(f.name))
        if not files:
            continue
        entries = []
        for f in files:
            w, h = image_size(f)
            # Thumbnails are always JPEG; keep the original name for jpgs.
            thumb = trip / "thumbs" / folder.name / (f.stem + ".jpg")
            made += make_thumb(f, thumb)
            entries.append([f.name, w, h])
        trips[folder.name] = entries

    (trip / "manifest.js").write_text(
        "window.TRIPS = " + json.dumps(trips, separators=(",", ":"), ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    if trip != HERE:
        shutil.copyfile(HERE / "index.html", trip / "index.html")
    n = sum(len(v) for v in trips.values())
    print(f"{len(trips)} folders, {n} images, {made} thumbnails (re)made -> {trip}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit(__doc__)
    main(sys.argv[1] if len(sys.argv) == 2 else HERE)
