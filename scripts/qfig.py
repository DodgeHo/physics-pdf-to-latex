"""Crop every figure-like region in an exam PDF, one PNG per region, named by page.

Regions = embedded image rects (area > min-area) + merged drawing clusters.
No question assignment (numbering is read from the preview pages instead).

Usage: python qfig.py <pdf> <outdir> [--zoom 3.0] [--min-area 8000]
Writes outdir/pNN_k.png and outdir/_figs.json
"""
import argparse
import json
from pathlib import Path

import pymupdf


def figures(page, min_area):
    rects = []
    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            if r.width * r.height > 3000:
                rects.append(pymupdf.Rect(r))

    drs = [pymupdf.Rect(d["rect"]) for d in page.get_drawings()
           if d["rect"].width > 4 and d["rect"].height > 4]
    # iterative merge of overlapping drawing rects
    merged = []
    for r in drs:
        hit = None
        for i, m in enumerate(merged):
            inter = m & r
            if not inter.is_empty and inter.get_area() > 0.55 * min(m.get_area(), r.get_area()):
                hit = i
                break
        if hit is None:
            merged.append(r)
        else:
            merged[hit] = merged[hit] | r
    changed = True
    while changed:
        changed = False
        for i in range(len(merged)):
            for j in range(i + 1, len(merged)):
                inter = merged[i] & merged[j]
                if not inter.is_empty and inter.get_area() > 0.55 * min(merged[i].get_area(), merged[j].get_area()):
                    merged[i] = merged[i] | merged[j]
                    merged.pop(j)
                    changed = True
                    break
            if changed:
                break

    for m in merged:
        if m.width > 45 and m.height > 22:
            rects.append(m)

    out = []
    for r in rects:
        if r.get_area() < min_area:
            continue
        # skip near-duplicates (same area/position)
        if any(abs(r.x0 - o.x0) < 3 and abs(r.y0 - o.y0) < 3 for o in out):
            continue
        out.append(r)
    return sorted(out, key=lambda r: (round(r.y0), round(r.x0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("outdir")
    ap.add_argument("--zoom", type=float, default=3.0)
    ap.add_argument("--min-area", type=float, default=8000)
    a = ap.parse_args()

    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(a.pdf)
    mat = pymupdf.Matrix(a.zoom, a.zoom)

    records = []
    for pno, page in enumerate(doc, start=1):
        k = 0
        for r in figures(page, a.min_area):
            k += 1
            name = f"p{pno:02d}_{k}"
            clip = pymupdf.Rect(r)
            clip.x0 = max(0, clip.x0 - 6)
            clip.y0 = max(0, clip.y0 - 6)
            clip.x1 = min(page.rect.width, clip.x1 + 6)
            clip.y1 = min(page.rect.height, clip.y1 + 6)
            pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
            pix.save(out / f"{name}.png")
            records.append({"name": name, "page": pno, "rect": [round(v, 1) for v in clip],
                            "w": pix.width, "h": pix.height})

    (out / "_figs.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"figs={len(records)}")
    for r in records:
        print(f"  {r['name']:9s} p{r['page']:<3d} {r['w']}x{r['h']} rect={r['rect']}")


if __name__ == "__main__":
    main()
