"""One-shot per-paper prep: page previews + auto figure crops + labeled contact sheet.

Usage:
  python prep.py <pdf> <卷名> [--root <batroot>] [--out <vol_dir>] [--min-area 3000]
                 [--cols 5] [--maxw 340] [--scan]

Outputs (default layout):
  <root>/tex输出/<卷名>/preview/page_N.png (1.6x) + page_N.txt
  <root>/_tmp/<卷名>/pNN_k.png + _figs.json + _sheet.png
  <out>/images/            (created empty, ready for crops)

--scan  additionally re-renders whole pages at 3.6x into <root>/_tmp/<卷名>/hi/
        for pure-scan PDFs whose text layer is empty (small print unreadable at 1.6x).
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("vol", help="卷名，如 2025湖南")
    ap.add_argument("--root", default=r"D:\Downloads\2024+2025年物理PDF-44",
                    help="批次根目录，默认本批次工作根")
    ap.add_argument("--out", default=None, help="成稿目录，默认 <root>/tex输出/<卷名>")
    ap.add_argument("--min-area", type=float, default=3000)
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--maxw", type=int, default=340)
    ap.add_argument("--scan", action="store_true", help="额外 3.6x 重渲染整页到 _tmp/<卷名>/hi")
    a = ap.parse_args()

    root = Path(a.root)
    vdir = Path(a.out) if a.out else root / "tex输出" / a.vol
    tmp = root / "_tmp" / a.vol
    tmp.mkdir(parents=True, exist_ok=True)
    (vdir / "images").mkdir(parents=True, exist_ok=True)

    subprocess.run([sys.executable, str(HERE / "probe_pdf.py"), str(a.pdf),
                    "--out", str(vdir / "preview")], check=True)
    subprocess.run([sys.executable, str(HERE / "qfig.py"), str(a.pdf), str(tmp),
                    "--min-area", str(a.min_area)], check=True)
    subprocess.run([sys.executable, str(HERE / "sheet.py"), str(tmp),
                    "--cols", str(a.cols), "--maxw", str(a.maxw)], check=True)

    if a.scan:
        import pymupdf
        hi = tmp / "hi"
        hi.mkdir(exist_ok=True)
        mat = pymupdf.Matrix(3.6, 3.6)
        with pymupdf.open(a.pdf) as doc:
            for i, page in enumerate(doc, start=1):
                page.get_pixmap(matrix=mat).save(hi / f"h{i}.png")
        print(f"hi-res pages -> {hi}")


if __name__ == "__main__":
    main()
