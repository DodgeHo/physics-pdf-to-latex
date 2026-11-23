"""Crop question figures from the PDF at high resolution, driven by a JSON manifest.

The manifest lists every figure that cannot be transcribed to LaTeX (diagrams,
circuit schematics, field sketches, option panels). Coordinates come from the
bboxes printed by probe_pdf.py, refined against the rendered preview PNGs.

Manifest format:
{
  "pdf": "path/to/exam.pdf",
  "outdir": "images",
  "zoom": 3.0,
  "crops": [
    {"page": 1, "name": "q02_spring", "rect": [54, 344.3, 160.6, 386.3], "margin": 6}
  ]
}

Usage:
    python crop_images.py <manifest.json>
"""
import argparse
import json
from pathlib import Path

import pymupdf


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    src = manifest["pdf"]
    outdir = Path(manifest.get("outdir", "images"))
    zoom = manifest.get("zoom", 3.0)
    margin = manifest.get("margin", 6)

    outdir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(src)
    mat = pymupdf.Matrix(zoom, zoom)

    for crop in manifest["crops"]:
        page = doc[crop["page"] - 1]
        x0, y0, x1, y1 = crop["rect"]
        m = crop.get("margin", margin)
        r = pymupdf.Rect(x0, y0, x1, y1)
        r.x0 = max(0, r.x0 - m)
        r.y0 = max(0, r.y0 - m)
        r.x1 = min(page.rect.width, r.x1 + m)
        r.y1 = min(page.rect.height, r.y1 + m)
        pix = page.get_pixmap(matrix=mat, clip=r, alpha=False)
        pix.save(outdir / f"{crop['name']}.png")
        print(crop["name"], pix.width, pix.height)

    print(f"done -> {outdir}")


if __name__ == "__main__":
    main()
