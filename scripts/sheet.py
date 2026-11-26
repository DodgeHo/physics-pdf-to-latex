"""Build a labeled contact sheet from cropped figure PNGs for quick visual review.

Usage: python sheet.py <images_dir> [--out sheet.png] [--cols 4] [--maxw 420]
Each crop is scaled to fit maxw, labeled with its file stem, laid out in a grid.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("indir")
    ap.add_argument("--out", default=None)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--maxw", type=int, default=420)
    ap.add_argument("--label-h", type=int, default=26)
    a = ap.parse_args()

    d = Path(a.indir)
    files = sorted([p for p in d.glob("*.png") if not p.name.startswith("_")])
    if not files:
        print("no crops")
        return

    cells = []
    for p in files:
        im = Image.open(p).convert("RGB")
        if im.width > a.maxw:
            h = int(im.height * a.maxw / im.width)
            im = im.resize((a.maxw, h), Image.LANCZOS)
        cells.append((p.stem, im))

    cols = a.cols
    rows = (len(cells) + cols - 1) // cols
    cw = a.maxw + 12
    ch = max(im.height for _, im in cells) + a.label_h + 12
    sheet = Image.new("RGB", (cols * cw, rows * ch), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(cells):
        r, c = divmod(i, cols)
        x = c * cw + 6
        y = r * ch + 6
        draw.text((x + 2, y + 2), f"{i+1}. {name}", fill="black")
        sheet.paste(im, (x, y + a.label_h))
        draw.rectangle([x - 1, y + a.label_h - 1, x + im.width, y + a.label_h + im.height], outline="gray")

    out = Path(a.out) if a.out else d / "_sheet.png"
    sheet.save(out)
    print(f"{out} ({sheet.width}x{sheet.height}) items={len(cells)}")


if __name__ == "__main__":
    main()
