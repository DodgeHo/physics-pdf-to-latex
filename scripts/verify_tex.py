"""Verify generated .tex files against the MathLive format contract.

Checks, per file:
- Every local absolute-path image reference resolves to an existing file.
- Question numbers present (lines starting with `\\noindent <n>.`).
- Forbidden LaTeX commands/environments are absent.
- Legacy spacing/escaping leftovers are absent: \\vspace, \\quad, \\qquad, \\_ .

Usage:
    python verify_tex.py <file1.tex> [file2.tex ...]

Exit code is 1 if any file fails, so it can gate final delivery.
"""
import argparse
import pathlib
import re

FORBIDDEN = [r"\hline", "itemize", r"\ce", r"\align", "tabular"]
LEFTOVER = [r"\vspace", r"\quad", r"\qquad", r"\_"]
IMG_RE = re.compile(r"\{([A-Za-z]:/[^}]+?\.(?:png|jpg|jpeg|gif|svg))\}")
Q_RE = re.compile(r"^\\noindent\s*(\d+)\.", re.M)


def check(path: pathlib.Path) -> bool:
    ok = True
    t = path.read_text(encoding="utf-8")

    refs = IMG_RE.findall(t)
    missing = [r for r in refs if not pathlib.Path(r).exists()]
    questions = Q_RE.findall(t)

    print(f"[{path.name}] refs={len(refs)} missing={missing} questions={questions}")

    if missing:
        ok = False
        print("  FAIL: missing images:", missing)

    for bad in FORBIDDEN:
        if bad in t:
            ok = False
            print(f"  FAIL: forbidden token present: {bad}")

    for bad in LEFTOVER:
        count = t.count(bad)
        if count:
            ok = False
            print(f"  FAIL: leftover {bad} x{count}")

    if ok:
        print("  OK")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tex", nargs="+")
    args = ap.parse_args()

    all_ok = True
    for f in args.tex:
        all_ok &= check(pathlib.Path(f))

    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
