#!/usr/bin/env python3
"""Check SOP markdown sources before rendering.

    check_md.py md/*.md
    check_md.py md            # a directory checks every .md inside it

Reports anything the renderer would silently drop or mis-handle: unknown row
labels, unsupported alert types, ragged tables, missing figures, constructs the
dialect does not implement. Exit status is 1 if any error was found; warnings
alone exit 0.
"""

import argparse
import re
import sys
from pathlib import Path

from sop_doc import ALERT_RE, QUOTE_ROW_RE, load

REQUIRED_META = ("sop", "title", "revision", "author", "date", "location", "status")
ROW_LABELS = ("ACTION", "VERIFY", "STOP", "NOTE")
ALERT_TYPES = ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION")

# markdown the renderer does not implement, and would print literally
UNSUPPORTED = [
    (re.compile(r"(?<!!)\[[^\]]+\]\([^)]+\)"), "links are not rendered; write the target as plain text"),
    (re.compile(r"^```"), "code fences are not supported"),
    (re.compile(r"^\s{0,3}#{4,}\s"), "only '## section' and '### step' headings are supported"),
    (re.compile(r"<[a-zA-Z/][^>]*>"), "raw HTML is not supported"),
]


def check_file(path):
    path = Path(path)
    errors, warnings = [], []

    def error(line_no, message):
        errors.append((line_no, message))

    def warn(line_no, message):
        warnings.append((line_no, message))

    raw = path.read_text(encoding="utf-8").split("\n")
    doc = load(path)

    for key in REQUIRED_META:
        if key not in doc.meta:
            error(1, f"frontmatter is missing '{key}:'")
        elif not doc.meta[key].strip():
            warn(1, f"frontmatter '{key}:' is empty")
    if not doc.meta.get("output", "").endswith(".pdf"):
        warn(1, "frontmatter 'output:' should name the PDF file to write")

    in_frontmatter = raw[0].strip() == "---"
    in_quote = False
    for n, line in enumerate(raw, start=1):
        stripped = line.strip()
        if in_frontmatter:
            if n > 1 and stripped == "---":
                in_frontmatter = False
            continue
        if not stripped.startswith(">"):
            in_quote = False
        elif in_quote:
            pass                      # continuation line, not a label position
        else:
            in_quote = True
            body = stripped[1:].strip()
            label = re.match(r"^\*\*([A-Za-z ]+)\*\*", body)
            alert = re.match(r"^\[!([A-Za-z]+)\]", body)
            if alert and alert.group(1).upper() not in ALERT_TYPES:
                error(n, f"unknown alert type '[!{alert.group(1)}]'; "
                         f"use one of {', '.join(ALERT_TYPES)}")
            elif (label and not QUOTE_ROW_RE.match(body) and not ALERT_RE.match(body)
                    and label.group(1).upper() not in ROW_LABELS):
                error(n, f"unknown row label '{label.group(1)}'; "
                         f"use one of {', '.join(ROW_LABELS)}")
        for pattern, message in UNSUPPORTED:
            if pattern.search(line):
                warn(n, message)

    seen_section = False
    for block in doc.blocks:
        if block["type"] == "section":
            seen_section = True
        elif block["type"] == "step" and not seen_section:
            warn(1, f"step '{block['text'][:40]}' appears before any '## section'")

    def check_tables(blocks):
        for block in blocks:
            if block["type"] == "box":
                check_tables(block["blocks"])
            elif block["type"] == "table":
                widths = {len(r) for r in block["rows"]}
                if len(widths) > 1:
                    error(1, f"table rows have differing column counts {sorted(widths)}")
            elif block["type"] == "image":
                if not (path.parent / block["path"]).exists():
                    error(1, f"figure not found: {block['path']}")

    check_tables(doc.blocks)
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help=".md files or a directory")
    args = ap.parse_args()

    targets = []
    for item in args.inputs:
        item = Path(item)
        targets.extend(sorted(item.glob("*.md")) if item.is_dir() else [item])

    failed = False
    for target in targets:
        errors, warnings = check_file(target)
        if not errors and not warnings:
            print(f"ok      {target}")
            continue
        print(f"{'FAIL' if errors else 'warn'}    {target}")
        for line_no, message in errors:
            print(f"          error line {line_no}: {message}")
        for line_no, message in warnings:
            print(f"          warn  line {line_no}: {message}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
