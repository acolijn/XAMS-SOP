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

import sop_style as st
from sop_doc import ALERT_RE, ALERT_TO_KIND, DEPRECATED_ALERTS, QUOTE_ROW_RE, load

REQUIRED_META = ("sop", "doc_id", "title", "revision", "issue_date", "author",
                 "prepared_by", "audience", "location", "status")

# Fields a released document should carry but a draft legitimately may not:
# a procedure with no approver is a draft, and saying so is the point.
RECOMMENDED_META = ("supersedes", "reviewed_by", "approved_by")

# Sections every procedure carries. The index and the general hazard sheet are
# not procedures and are exempt.
REQUIRED_SECTIONS = ("Scope and competence", "Document control")
EXEMPT_STEMS = ("XAMS_Operations_Manual_Index", "SOP_000_General_Hazards")
SOP_RE = re.compile(r"SOP[-_ ]?(\d+)", re.I)

# Register columns that merely restate an SOP's frontmatter. They are checked
# and can be rewritten by --fix, so the register cannot drift from the sources.
# header name -> (frontmatter key, mismatch is an error)
DERIVED_COLUMNS = {"rev": ("revision", True),
                   "procedure": ("title", False),
                   "purpose": ("subtitle", False),
                   "status": ("status", False)}

# `status:` in the frontmatter is a change note ("Updated release", "Layout
# update"), printed on the cover. The index needs the operational question
# instead: is this approved for use, or still a placeholder?
DRAFT_WORDS = ("draft", "placeholder")
INDEX_STEM = "XAMS_Operations_Manual_Index"
ROW_LABELS = ("ACTION", "VERIFY", "STOP", "NOTE")

# The vocabulary is owned by sop_doc, so the parser and the checker cannot drift.
ALERT_TYPES = tuple(a.upper() for a in ALERT_TO_KIND)
SIGNAL_ALERTS = tuple(a.upper() for a, kind in ALERT_TO_KIND.items()
                      if kind in st.SIGNAL_KINDS)

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
    for key in RECOMMENDED_META:
        if not doc.meta.get(key, "").strip():
            warn(1, f"frontmatter has no '{key}:'")
    if path.stem not in EXEMPT_STEMS:
        headings = {block["text"].strip() for block in doc.blocks
                    if block["type"] == "section"}
        for wanted in REQUIRED_SECTIONS:
            if wanted not in headings:
                warn(1, f"no '## {wanted}' section")
        # if not any(h.startswith("Troubleshooting") for h in headings):
        #     warn(1, "no '## Troubleshooting' section; there is no manufacturer to "
        #             "call, so fault -> cause -> remedy has to be written down here")
    if doc.meta.get("output"):
        warn(1, "frontmatter 'output:' overrides the derived PDF name; "
                "remove it unless the override is deliberate")
    if re.search(r"_Rev[_ ]", path.stem, re.I):
        warn(1, "the source filename should not carry a revision - "
                "the revision lives in the frontmatter and only the PDF is stamped")

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
            elif alert and alert.group(1).upper() in DEPRECATED_ALERTS:
                warn(n, f"'[!{alert.group(1).upper()}]' carries no severity; use a "
                        f"signal word ({', '.join(SIGNAL_ALERTS)}) for anything "
                        f"safety-relevant, or [!NOTE] for background")
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

    def check_hazards(blocks):
        """A safety message states the hazard, its consequence, and how to avoid it.

        Only the injury classes are checked. NOTICE covers property damage and
        needs no consequence-for-people wording.
        """
        for block in blocks:
            if block["type"] != "box":
                continue
            check_hazards(block["blocks"])
            if block["kind"] not in st.INJURY_KINDS:
                continue
            signal = st.BOX_KINDS[block["kind"]]["signal"]
            text = _box_text(block)
            excerpt = text[:48]
            lead = next((b for b in block["blocks"] if b["type"] == "para"), None)
            if lead is None or not lead["text"].lstrip().startswith("**"):
                warn(1, f"{signal} box ({excerpt!r}) does not open with a bold "
                        f"hazard statement; write hazard and source, then the "
                        f"consequence, then how to avoid it")
            if len(re.findall(r"[.!?](?:\s|$)", text)) < 2:
                warn(1, f"{signal} box ({excerpt!r}) is a single sentence; give the "
                        f"consequence and the way to avoid the hazard as well")

    check_tables(doc.blocks)
    check_hazards(doc.blocks)
    return errors, warnings


def _box_text(block):
    """All plain text inside a callout, for structural checks."""
    parts = []
    for child in block.get("blocks", []):
        kind = child["type"]
        if kind in ("para", "step", "section", "row", "banner"):
            parts.append(child.get("text", ""))
        elif kind == "bullets":
            parts.extend(child["items"])
        elif kind == "table":
            parts.extend(cell for row in child["rows"] for cell in row)
        elif kind == "box":
            parts.append(_box_text(child))
    return " ".join(p for p in parts if p)


def _derived_value(doc, key):
    """The frontmatter value as an index table should show it."""
    value = doc.meta.get(key, "").strip()
    if key == "revision":
        return value.replace("Rev.", "").strip()
    if key == "status":
        return "DRAFT" if any(w in value.lower() for w in DRAFT_WORDS) else "Released"
    return value


def _sop_number(text):
    """'SOP-004', 'SOP_004_LXe_...' and a bare '004' all mean SOP-004."""
    text = (text or "").strip()
    match = SOP_RE.search(text) or re.fullmatch(r"(\d{1,3})", text)
    return match.group(1).lstrip("0").zfill(3) if match else None


def _sop_tables(doc):
    """Every table in the index keyed by SOP number, with its column map.

    Sections 1-3 group the procedures editorially and the register lists them
    all; each may restate frontmatter in a column, and all of them are kept in
    step with the sources.
    """
    for block in doc.blocks:
        if block["type"] != "table":
            continue
        header = [h.lower().strip().rstrip(".") for h in (block.get("header") or [])]
        if header[:1] == ["sop"]:
            yield block, {name: i for i, name in enumerate(header)}


def _register_rows(doc):
    """The full register: the SOP table carrying a revision column."""
    for block, columns in _sop_tables(doc):
        if "rev" in columns:
            yield block, columns
            return


def check_collection(paths):
    """Checks that only make sense across the whole manual."""
    errors, warnings = [], []
    docs = {path: load(path) for path in paths}

    by_number = {}
    for path, doc in docs.items():
        if path.stem == INDEX_STEM:
            continue
        number = _sop_number(doc.meta.get("sop", "")) or _sop_number(path.stem)
        if number:
            by_number.setdefault(number, []).append((path, doc))

    current = {}
    for number, entries in sorted(by_number.items()):
        if len(entries) == 1:
            current[number] = entries[0]
            continue
        revisions = {path: doc.meta.get("revision", "").strip() for path, doc in entries}
        names = ", ".join(p.name for p in revisions)
        if len({r.upper() for r in revisions.values()}) == 1:
            errors.append(f"SOP-{number}: {len(entries)} files with the same revision "
                          f"({names}) - only one can be current")
            current[number] = entries[0]
        else:
            newest = max(entries, key=lambda e: e[1].meta.get("revision", "").upper())
            warnings.append(f"SOP-{number}: several revisions present ({names}); "
                            f"treating {newest[0].name} as current - "
                            f"move superseded revisions to old/")
            current[number] = newest

    index_path = next((p for p in docs if p.stem == INDEX_STEM), None)
    if index_path is None:
        warnings.append(f"no {INDEX_STEM}.md found; the register was not checked")
        return errors, warnings

    register = next(_register_rows(docs[index_path]), None)
    if register is None:
        warnings.append(f"{index_path.name}: no SOP register table with a 'Rev.' column")
        return errors, warnings

    block, columns = register
    listed = {_sop_number(row[0]) for row in block["rows"] if _sop_number(row[0])}
    for number, (path, _) in sorted(current.items()):
        if number not in listed:
            errors.append(f"SOP-{number} ({path.name}) is missing from the register "
                          f"in {index_path.name}")

    for table, columns in _sop_tables(docs[index_path]):
        for row in table["rows"]:
            number = _sop_number(row[0])
            entry = current.get(number)
            if entry is None:
                continue
            doc = entry[1]
            for name, (key, fatal) in DERIVED_COLUMNS.items():
                column = columns.get(name)
                if column is None or column >= len(row):
                    continue
                want = _derived_value(doc, key)
                got = row[column].strip()
                if not want or not got or want.lower() == got.lower():
                    continue
                message = (f"SOP-{number}: index {name} is {got!r}, the SOP says "
                           f"{want!r} - run check_md.py md --fix")
                (errors if fatal else warnings).append(message)
    for number in sorted(set(listed) - set(current)):
        warnings.append(f"the register lists SOP-{number}, but no such file is in md/")
    return errors, warnings


def fix_register(paths):
    """Rewrite the register's derived columns from each SOP's frontmatter.

    Only columns listed in DERIVED_COLUMNS are touched - they restate the
    frontmatter and carry no editorial content. Any other column is left alone.
    """
    docs = {path: load(path) for path in paths}
    index_path = next((p for p in docs if p.stem == INDEX_STEM), None)
    if index_path is None:
        return []

    wanted = {}
    for path, doc in docs.items():
        if path.stem == INDEX_STEM:
            continue
        number = _sop_number(doc.meta.get("sop", "")) or _sop_number(path.stem)
        revision = _derived_value(doc, "revision")
        if not number or not revision:
            continue
        # with several revisions present, the register should follow the newest
        if number not in wanted or revision.upper() > wanted[number][0].upper():
            wanted[number] = (revision, doc)

    lines = index_path.read_text(encoding="utf-8").split("\n")
    changes, columns, in_register = [], None, False
    for n, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            in_register, columns = False, None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        lowered = [c.lower().rstrip(".") for c in cells]
        if lowered[:1] == ["sop"]:
            columns = {name: i for i, name in enumerate(lowered)}
            in_register = True
            continue
        if not in_register or not columns:
            continue
        number = _sop_number(cells[0])
        if number is None or number not in wanted:
            continue
        revision, doc = wanted[number]
        for name, (key, _) in DERIVED_COLUMNS.items():
            column = columns.get(name)
            if column is None or column >= len(cells):
                continue
            want = revision if key == "revision" else _derived_value(doc, key)
            if not want or cells[column].lower() == want.lower():
                continue
            changes.append(f"SOP-{number} {name}: {cells[column]!r} -> {want!r}")
            cells[column] = want
        lines[n] = "| " + " | ".join(cells) + " |"

    if changes:
        index_path.write_text("\n".join(lines), encoding="utf-8")
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help=".md files or a directory")
    ap.add_argument("--fix", action="store_true",
                    help="update the index register's revision column from the "
                         "SOP frontmatter, then re-check")
    args = ap.parse_args()

    targets = []
    for item in args.inputs:
        item = Path(item)
        targets.extend(sorted(item.glob("*.md")) if item.is_dir() else [item])

    if args.fix and len(targets) > 1:
        for change in fix_register(targets) or ["register already matches the sources"]:
            print(f"fixed   {change}")

    failed = False
    if len(targets) > 1:
        errors, warnings = check_collection(targets)
        for message in errors:
            print(f"ERROR   {message}")
        for message in warnings:
            print(f"warn    {message}")
        failed = failed or bool(errors)

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
