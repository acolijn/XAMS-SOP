#!/usr/bin/env python3
"""Rebuild the manual: render every markdown source to PDF.

    build.py                       # md/ -> XAMS_Operations_Manual_<today>/
    build.py --srcdir md --outdir dist
    build.py --check               # also compare text against the previous PDF

Files listed in md/.passthrough are copied instead of rendered (e.g. the P&ID).
"""

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

from check_md import check_collection, check_file
from md_to_pdf import render

ROOT = Path(__file__).resolve().parent.parent


def _words(pdf_path):
    import pymupdf
    text = " ".join(page.get_text() for page in pymupdf.open(pdf_path))
    text = re.sub(r"Page \d+", " ", text)
    return re.findall(r"[^\s]+", text)


def check(old_pdf, new_pdf):
    """Report words present in one PDF but not the other."""
    from collections import Counter
    old, new = Counter(_words(old_pdf)), Counter(_words(new_pdf))
    lost = sorted((old - new).elements())
    gained = sorted((new - old).elements())
    return lost, gained


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--srcdir", default=str(ROOT / "md"))
    ap.add_argument("--outdir", default=None,
                    help="default: XAMS_Operations_Manual_<today>/")
    ap.add_argument("--check", action="store_true",
                    help="compare rendered text with the same-named PDF in --refdir")
    ap.add_argument("--refdir", default=None, help="PDFs to compare against")
    ap.add_argument("--force", action="store_true",
                    help="render even if check_md reports errors")
    ap.add_argument("--clean", action=argparse.BooleanOptionalAction, default=True,
                    help="delete the PDFs already in --outdir first (default: on); "
                         "--no-clean keeps them and overwrites in place")
    args = ap.parse_args()

    srcdir = Path(args.srcdir)
    outdir = Path(args.outdir) if args.outdir else \
        ROOT / f"XAMS_Operations_Manual_{date.today().isoformat()}"
    outdir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        # only ever *.pdf, never recursive: the output directory is disposable,
        # but it is not this script's business to remove anything else
        stale = sorted(outdir.glob("*.pdf"))
        for pdf in stale:
            pdf.unlink()
        if stale:
            print(f"cleaned {len(stale)} PDF(s) from {outdir}")

    passthrough = srcdir / ".passthrough"
    if passthrough.exists():
        for line in passthrough.read_text().splitlines():
            entry = line.strip()
            if not entry or entry.startswith("#"):
                continue
            src = srcdir / entry
            if not src.is_file():
                # fall back to a project-wide search, never picking up a copy
                # this build (or an earlier one) already made
                src = next((p for p in sorted(ROOT.rglob(Path(entry).name))
                            if p.is_file()
                            and outdir.resolve() not in p.resolve().parents), None)
            if src is None:
                print(f"MISSING passthrough file: {entry}", file=sys.stderr)
                continue
            target = outdir / Path(entry).name
            if src.resolve() == target.resolve():
                print(f"kept    {target.name}")
            else:
                shutil.copy2(src, target)
                print(f"copied  {target.name}")

    sources = sorted(srcdir.glob("*.md"))

    broken = []
    for md in sources:
        errors, _ = check_file(md)
        for line_no, message in errors:
            print(f"ERROR   {md.name} line {line_no}: {message}", file=sys.stderr)
        if errors:
            broken.append(md)

    across, _ = check_collection(sources)
    for message in across:
        print(f"ERROR   {message}", file=sys.stderr)

    if (broken or across) and not args.force:
        print(f"\n{len(broken) + len(across)} problem(s) found; "
              f"fix them, or pass --force to build anyway.", file=sys.stderr)
        return 1

    failures = 0
    for md in sources:
        try:
            out = render(md, outdir=outdir)
        except Exception as exc:                       # noqa: BLE001 - report and continue
            print(f"FAILED  {md.name}: {exc}", file=sys.stderr)
            failures += 1
            continue
        print(f"wrote   {out}")
        if args.check and args.refdir:
            ref = Path(args.refdir) / out.name
            if ref.exists():
                lost, gained = check(ref, out)
                if lost:
                    print(f"        lost {len(lost)} words: {' '.join(lost[:12])}")
                if gained:
                    print(f"        new  {len(gained)} words: {' '.join(gained[:12])}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
