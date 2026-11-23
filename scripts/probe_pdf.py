"""Probe an exam PDF: page count, per-page text/image/drawing stats, bounding boxes,
and render low-resolution previews + dumped text for manual transcription review.

Usage:
    python probe_pdf.py <pdf_path> [--out <preview_dir>]

Outputs under <preview_dir> (default: ./preview):
    page_<n>.png   1.6x render of each page, used to read formulas/figures correctly
    page_<n>.txt   raw text layer (formula sub/superscripts are often misordered;
                    never trust it blindly -- compare against the rendered PNG)

Prints image xref bboxes and clustered drawing bboxes so figures can be located
for cropping (see crop_images.py).
"""
import argparse
from pathlib import Path

import pymupdf


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", default="preview")
    args = ap.parse_args()

    src = Path(args.pdf)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(src)
    print(f"pages: {doc.page_count}")
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text", sort=True)
        imgs = page.get_images(full=True)
        drawings = page.get_drawings()
        print(
            f"p{i}: text={len(text)} images={len(imgs)} "
            f"drawings={len(drawings)} size={page.rect.width:.0f}x{page.rect.height:.0f}"
        )
        for img in imgs:
            xref = img[0]
            for r in page.get_image_rects(xref):
                print(f"  img xref={xref} bbox={tuple(round(v, 1) for v in r)}")
        dr = [
            d["rect"]
            for d in drawings
            if d["rect"].width > 2 and d["rect"].height > 2
        ]
        for r in dr:
            print(f"  draw bbox={tuple(round(v, 1) for v in r)}")

        (outdir / f"page_{i}.txt").write_text(text, encoding="utf-8")
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), alpha=False)
        pix.save(outdir / f"page_{i}.png")

    print(f"preview -> {outdir}")


if __name__ == "__main__":
    main()
