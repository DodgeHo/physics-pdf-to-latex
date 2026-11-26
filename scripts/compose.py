"""Compose several cropped option images into one labeled panel (2 columns).

Usage: python compose.py <out.png> <A.png> <B.png> [C.png] [D.png]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

LABELS = "ABCDEFGH"


def main():
    out = Path(sys.argv[1])
    inputs = [Path(p) for p in sys.argv[2:]]
    ims = [Image.open(p).convert("RGB") for p in inputs]
    maxw = max(i.width for i in ims)
    pad = 14
    lh = 22
    cols = 2 if len(ims) > 1 else 1
    rows = (len(ims) + cols - 1) // cols
    ch = max(i.height for i in ims) + lh + pad
    cw = maxw + pad
    sheet = Image.new("RGB", (cols * cw, rows * ch), "white")
    dr = ImageDraw.Draw(sheet)
    for idx, im in enumerate(ims):
        r, c = divmod(idx, cols)
        x, y = c * cw + 4, r * ch + 4
        dr.text((x, y), f"{LABELS[idx]}", fill="black")
        sheet.paste(im, (x, y + lh))
        dr.rectangle([x - 1, y + lh - 1, x + im.width, y + lh + im.height], outline="gray")
    sheet.save(out)
    print(f"{out} {sheet.width}x{sheet.height}")


if __name__ == "__main__":
    main()
