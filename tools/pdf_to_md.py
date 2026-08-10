#!/usr/bin/env python3
"""Import an XAMS SOP PDF back into the markdown source dialect.

    pdf_to_md.py SOP.pdf --outdir md/

The PDF is read geometrically - band fills, section bars, the metadata table,
column positions - rather than as flat text, so ACTION/VERIFY/STOP/NOTE rows,
sections, steps, callout boxes and two-column grids come back as structure.
Font sizes and page margins are derived per document, because the generated
PDFs do not all use the same scale. Embedded images are written to a `figs/`
directory next to the markdown.

Rendering the result with md_to_pdf.py reproduces the document in the canonical
house style; it is not a byte-identical round trip.
"""

import argparse
import re
import textwrap
from collections import Counter
from pathlib import Path

import pymupdf

from sop_doc import escape_md

ROW_KINDS = ("ACTION", "VERIFY", "STOP", "NOTE")
FOOTER_MIN_Y = 795.0
LEFT_EDGE = 39.7
RIGHT_EDGE = 555.6
EDGE_TOL = 3.0
LINE_TOL = 3.0          # spans within this vertical distance are one line
COL_GAP = 14.0          # horizontal gap that separates two columns

# background colour -> box kind, matched to the nearest known fill
BOX_BGS = {
    "action": (0xE8, 0xF2, 0xEE),
    "verify": (0xFF, 0xF3, 0xC4),
    "stop": (0xF7, 0xDD, 0xDD),
    "info": (0xE9, 0xF0, 0xF6),
}


def _hex(rgb):
    return "#%02x%02x%02x" % tuple(int(round(c * 255)) for c in rgb)


def _rgb(hex_color):
    return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))


def _box_kind(hex_color):
    target = _rgb(hex_color)
    return min(BOX_BGS, key=lambda k: sum((a - b) ** 2
                                          for a, b in zip(BOX_BGS[k], target)))


def _is_white(hex_color):
    return all(v >= 250 for v in _rgb(hex_color))


def _is_dark(hex_color):
    r, g, b = (v / 255 for v in _rgb(hex_color))
    return 0.299 * r + 0.587 * g + 0.114 * b < 0.5


def _spans(page):
    out = []
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if not span["text"].strip():
                    continue
                out.append({
                    "text": span["text"],
                    "x0": span["bbox"][0], "x1": span["bbox"][2],
                    "y0": span["bbox"][1], "y1": span["bbox"][3],
                    # the enclosing text line, so super/subscripts stay in place
                    "ly": line["bbox"][3],
                    "size": round(span["size"], 2),
                    "bold": span["font"].endswith(("Bold", "bold")),
                    "color": "#%06x" % span["color"],
                })
    out.sort(key=lambda s: (round(s["ly"] / LINE_TOL), s["x0"]))
    return out


def _lines(spans):
    """Group spans into visual lines."""
    lines, current = [], []
    for span in sorted(spans, key=lambda s: (round(s["ly"] / LINE_TOL), s["x0"])):
        if current and abs(span["ly"] - current[-1]["ly"]) > LINE_TOL:
            lines.append(current)
            current = []
        current.append(span)
    if current:
        lines.append(current)
    return lines


def _columns(line):
    """Split one line into columns on wide horizontal gaps."""
    cols, current = [], []
    for span in line:
        if current and span["x0"] - current[-1]["x1"] > COL_GAP:
            cols.append(current)
            current = []
        current.append(span)
    if current:
        cols.append(current)
    return cols


def _text(spans, markup=True):
    """Render a run of spans as markdown, keeping bold and super/subscripts."""
    if not spans:
        return ""
    main = max(s["size"] for s in spans)
    mixed_bold = markup and len({s["bold"] for s in spans}) > 1
    baseline = max((s["y1"] for s in spans if s["size"] >= main - 0.1), default=0)
    parts, prev = [], None
    for span in spans:
        text = escape_md(span["text"])
        stripped = text.strip()
        small = markup and stripped and span["size"] < main - 0.5
        if small:
            # smaller type sitting above or below the baseline of the run
            marker = "^" if span["y1"] < baseline - 0.8 else "~"
            text = text.replace(stripped, f"{marker}{stripped}{marker}", 1)
        elif mixed_bold and span["bold"] and stripped:
            lead = " " if text[:1] == " " else ""
            tail = " " if text[-1:] == " " else ""
            text = f"{lead}**{stripped}**{tail}"
        if prev is not None:
            if abs(span["ly"] - prev["ly"]) > LINE_TOL:
                parts.append(" ")
            elif (not small and span["x0"] - prev["x1"] > 1.0
                  and not parts[-1].endswith(" ") and not text.startswith(" ")):
                parts.append(" ")   # separate runs the PDF spaced out geometrically
        parts.append(text)
        prev = span
    return re.sub(r"[ \t]+", " ", "".join(parts)).strip()


def _structure(spans):
    """Turn a run of spans into paragraph and table blocks.

    Column anchors are the x positions where cells start on more than one line;
    lines that fill several anchors become table rows, the rest paragraphs.
    """
    lines = _lines(spans)
    if not lines:
        return []

    split = [_columns(line) for line in lines]
    anchors = sorted(x for x, n in Counter(
        round(col[0]["x0"] / 4) * 4 for cols in split for col in cols[1:]
    ).items() if n >= 2)

    def cell_index(col):
        x = col[0]["x0"]
        best = min(range(len(anchors)), key=lambda i: abs(anchors[i] - x)) if anchors else None
        if best is None or abs(anchors[best] - x) > 8:
            return None
        return best + 1

    blocks, para, rows, bullets = [], [], [], []

    def flush_bullets():
        if bullets:
            blocks.append({"type": "bullets", "items": list(bullets)})
            bullets.clear()

    def flush_para():
        if para:
            blocks.append({"type": "para", "text": " ".join(para)})
            para.clear()

    def flush_rows():
        if len(rows) >= 2:
            width = max(len(r) for r in rows)
            padded = [r + [""] * (width - len(r)) for r in rows]
            header = padded[0] if width >= 3 else []
            blocks.append({"type": "table",
                           "style": "grid" if header else "plain",
                           "header": header,
                           "rows": padded[1:] if header else padded})
        elif rows:
            para.extend(" ".join(c for c in row if c) for row in rows)
        rows.clear()

    for cols in split:
        indices = [cell_index(col) for col in cols[1:]]
        if len(cols) >= 2 and all(i is not None for i in indices):
            flush_para()
            row = [""] * (max(indices) + 1)
            row[0] = _text(cols[0])
            for col, index in zip(cols[1:], indices):
                row[index] = _text(col)
            rows.append(row)
        elif (rows and len(cols) == 1 and cell_index(cols[0]) is not None):
            index = cell_index(cols[0])
            if index < len(rows[-1]):
                rows[-1][index] = f"{rows[-1][index]} {_text(cols[0])}".strip()
            else:
                rows[-1].append(_text(cols[0]))
        else:
            flush_rows()
            text = _text([s for col in cols for s in col])
            bullet = re.match(r"^[\u2022\u2023\u25cf\u00b7\u2010-]\s*(.*)$", text)
            if bullet:
                flush_para()
                bullets.append(bullet.group(1).strip())
            elif bullets and cols[0][0]["x0"] > lines[0][0]["x0"] + 4:
                bullets[-1] = f"{bullets[-1]} {text}".strip()   # wrapped bullet
            else:
                flush_bullets()
                spans_here = [s for col in cols for s in col]
                if text and all(s["bold"] for s in spans_here) and "**" not in text:
                    text = f"**{text}**"    # a wholly bold line, e.g. a box title
                para.append(text)
    flush_rows()
    flush_bullets()
    flush_para()
    return blocks


def _fills(page):
    out = []
    for drawing in page.get_drawings():
        if drawing["type"] != "f" or not drawing.get("fill"):
            continue
        out.append((drawing["rect"], _hex(drawing["fill"])))
    out.sort(key=lambda f: (f[0].y0, f[0].x0))
    return out


def _page_edges(page):
    """Content margins vary between document generations; measure them."""
    wide = [d["rect"] for d in page.get_drawings() if d["rect"].width > 350]
    if not wide:
        return LEFT_EDGE, RIGHT_EDGE
    left = Counter(round(r.x0, 1) for r in wide).most_common(1)[0][0]
    right = Counter(round(r.x1, 1) for r in wide).most_common(1)[0][0]
    return left, right


def _is_full_width(rect, edges):
    left, right = edges
    return abs(rect.x0 - left) < EDGE_TOL and abs(rect.x1 - right) < EDGE_TOL


def _has_row_label(rect, spans):
    return any(rect.y0 - 1 <= s["y0"] and s["y1"] <= rect.y1 + 1
               and s["text"].strip() in ROW_KINDS for s in spans)


def _merge_bands(bands, spans):
    """Join touching bands of the same colour into one callout.

    A checklist is drawn as one band per item; without this each item would
    become its own box. Bands carrying a row label are never merged.
    """
    merged = []
    for rect, color in bands:
        if merged:
            prev_rect, prev_color = merged[-1]
            if (prev_color == color and abs(prev_rect.y1 - rect.y0) < 0.6
                    and not _has_row_label(prev_rect, spans)
                    and not _has_row_label(rect, spans)):
                merged[-1] = (pymupdf.Rect(prev_rect.x0, prev_rect.y0,
                                           rect.x1, rect.y1), color)
                continue
        merged.append((rect, color))
    return merged


def _meta_region(fills, edges):
    """The metadata table is drawn as two narrow label-column fills."""
    narrow = [r for r, _ in fills
              if abs(r.x0 - edges[0]) < EDGE_TOL and 60 < r.width < 100 and r.height > 30]
    if not narrow:
        return None
    rect = narrow[0]
    second = [r for r, _ in fills
              if r.x0 > 200 and abs(r.y0 - rect.y0) < 2 and 60 < r.width < 100]
    return rect.y0, rect.y1, rect.x1, (second[0].x0 if second else None)


def _extract_images(doc, outdir, stem):
    figs, seen = [], {}
    figdir = outdir / "figs"
    for pno, page in enumerate(doc):
        for info in page.get_image_info(xrefs=True):
            xref = info.get("xref")
            rect = pymupdf.Rect(info["bbox"])
            if not xref or rect.width < 20 or rect.height < 20:
                continue
            if xref not in seen:
                pix = pymupdf.Pixmap(doc, xref)
                if pix.n - pix.alpha >= 4:
                    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                figdir.mkdir(parents=True, exist_ok=True)
                name = f"{stem}_fig{len(seen) + 1}.png"
                pix.save(figdir / name)
                seen[xref] = f"figs/{name}"
            figs.append((pno, rect.y0, seen[xref], rect.width))
    return figs


def _read_meta(spans, region, meta):
    """Read the label/value pairs out of the metadata table."""
    top, bottom, label_x1, second_x0 = region
    label_w = label_x1 - min((s["x0"] for s in spans), default=label_x1 - 70)
    for row in _lines([s for s in spans if top - 2 <= s["y0"] <= bottom + 2]):
        row = sorted(row, key=lambda s: s["x0"])
        cells, current = [], []
        for span in row:
            is_label = span["x0"] < label_x1 or (
                second_x0 is not None and second_x0 <= span["x0"] < second_x0 + label_w)
            if is_label and current:
                cells.append(current)
                current = []
            current.append(span)
        if current:
            cells.append(current)
        for cell in cells:
            key = cell[0]["text"].strip().lower().rstrip(":")
            if key in ("document", "revision", "author", "date", "location", "status"):
                meta[key] = _text(cell[1:], markup=False)


def parse_pdf(pdf_path, outdir):
    pdf_path, outdir = Path(pdf_path), Path(outdir)
    doc = pymupdf.open(pdf_path)
    images = _extract_images(doc, outdir, pdf_path.stem)

    meta, warnings = {}, []
    title = subtitle = ""
    region = None
    items = []

    sizes = Counter()
    for page in doc:
        edges = _page_edges(page)
        bands = [r for r, c in _fills(page)
                 if _is_full_width(r, edges) and r.height >= 8 and not _is_white(c)]
        for span in _spans(page):
            if any(r.y0 - 1 <= span["y0"] and span["y1"] <= r.y1 + 1 for r in bands):
                sizes[span["size"]] += 1
    body_size = sizes.most_common(1)[0][0] if sizes else 10.5

    for pno, page in enumerate(doc):
        all_spans = _spans(page)
        spans = [s for s in all_spans if s["y0"] < FOOTER_MIN_Y]
        fills = _fills(page)
        edges = _page_edges(page)
        bands = _merge_bands([(r, c) for r, c in fills
                              if _is_full_width(r, edges) and r.height >= 8
                              and not _is_white(c)], spans)

        if pno == 0:
            footer = _text([s for s in all_spans
                            if s["y0"] >= FOOTER_MIN_Y and not s["text"].startswith("Page")],
                           markup=False)
            if "|" in footer:
                parts = [p.strip() for p in footer.split("|")]
                for key, value in zip(("footer_title", "footer_doc", "footer_rev"), parts):
                    if value:
                        meta[key] = value
            region = _meta_region(fills, edges)
            if region:
                header = [s for s in spans if s["y1"] <= region[0]]
                if header:
                    top_size = max(s["size"] for s in header)
                    title = _text([s for s in header if s["size"] == top_size], markup=False)
                    subtitle = _text([s for s in header if s["size"] < top_size], markup=False)
                _read_meta(spans, region, meta)
            else:
                warnings.append("metadata table not recognised")
            if region:
                bands = [(r, c) for r, c in bands
                         if r.y1 <= region[0] + 1 or r.y0 >= region[1] - 1]

        used = set()
        for rect, color in bands:
            inside = [s for s in spans
                      if rect.y0 - 1 <= s["y0"] and s["y1"] <= rect.y1 + 1 and id(s) not in used]
            if not inside:
                continue
            for span in inside:
                used.add(id(span))

            if _is_dark(color):
                items.append((pno, rect.y0, {"type": "section", "text": _text(inside)}))
                continue

            kind = next((s["text"].strip() for s in inside
                         if s["text"].strip() in ROW_KINDS), None)
            if kind:
                body = [s for s in inside if s["text"].strip() != kind]
                blocks = _structure(body)
                lead = blocks[0]["text"] if blocks and blocks[0]["type"] == "para" else ""
                items.append((pno, rect.y0, {"type": "row", "kind": kind, "text": lead}))
                rest = blocks[1:] if lead else blocks
                if rest:
                    items.append((pno, rect.y0 + 0.1,
                                  {"type": "box", "kind": kind.lower(), "blocks": rest}))
                continue

            blocks = _structure(inside)
            if len(blocks) == 1 and blocks[0]["type"] == "para":
                items.append((pno, rect.y0,
                              {"type": "banner",
                               "kind": "warning" if _box_kind(color) == "stop" else "info",
                               "text": blocks[0]["text"]}))
            else:
                items.append((pno, rect.y0,
                              {"type": "box", "kind": _box_kind(color), "blocks": blocks}))

        loose = [s for s in spans if id(s) not in used]
        if pno == 0 and region:
            loose = [s for s in loose if s["y0"] > region[1]]
        # step headings first, then everything else as one run so that tables
        # spread over widely spaced rows are still recognised
        rest = []
        for line in _lines(loose):
            head = line[0]
            if (head["bold"] and head["size"] > body_size + 1.0
                    and len(_columns(line)) == 1):
                items.append((pno, head["y0"], {"type": "step", "text": _text(line)}))
            else:
                rest.append(line)
        if rest:
            flat = [span for line in rest for span in line]
            for block in _structure(flat):
                items.append((pno, rest[0][0]["y0"], block))

        for ipno, y, path, width in images:
            if ipno == pno:
                pct = max(10, min(100, round(100 * width / (edges[1] - edges[0]))))
                items.append((pno, y, {"type": "image", "path": path,
                                       "caption": "", "width": f"{pct}%"}))

    items.sort(key=lambda t: (t[0], t[1]))
    blocks = _merge([b for _, _, b in items])
    if not any(b["type"] == "row" for b in blocks):
        warnings.append("no ACTION/VERIFY/STOP/NOTE rows found - check the result by hand")
    return meta, title, subtitle, blocks, warnings


def _merge(blocks):
    """Join consecutive paragraphs and rows continued across a page break."""
    out = []
    for block in blocks:
        prev = out[-1] if out else None
        if block["type"] == "para" and prev and prev["type"] == "para":
            prev["text"] = f"{prev['text']} {block['text']}".strip()
            continue
        if (block["type"] == "banner" and block["text"] and prev
                and prev["type"] == "row" and not block["text"][:1].isupper()):
            prev["text"] = f"{prev['text']} {block['text']}".strip()
            continue
        out.append(block)
    return out


ALERT_FOR = {"action": "TIP", "verify": "IMPORTANT", "stop": "CAUTION",
             "warning": "WARNING", "info": "NOTE", "note": "NOTE"}
WRAP_AT = 88


def _wrap(text, prefix=""):
    """Soft-wrap prose so that edits produce small, readable diffs."""
    if not text:
        return [prefix.rstrip()]
    return textwrap.wrap(text, width=WRAP_AT, initial_indent=prefix,
                         subsequent_indent=prefix, break_long_words=False,
                         break_on_hyphens=False)


def _wrap_item(text, prefix=""):
    """Bullet with a hanging indent."""
    return textwrap.wrap(text, width=WRAP_AT, initial_indent=prefix + "- ",
                         subsequent_indent=prefix + "  ", break_long_words=False,
                         break_on_hyphens=False) or [prefix + "-"]


def _emit_table(block, out, prefix=""):
    header = block.get("header") or []
    width = max([len(header)] + [len(r) for r in block["rows"]], default=2)
    cells = header if any(h.strip() for h in header) else [""] * width
    out.append(prefix + "| " + " | ".join(cells) + " |")
    out.append(prefix + "|" + "|".join([" --- "] * width) + "|")
    for row in block["rows"]:
        padded = row + [""] * (width - len(row))
        out.append(prefix + "| " + " | ".join(padded) + " |")


def _emit_quoted(blocks, out):
    """Body of a callout: everything indented with '> '."""
    for n, child in enumerate(blocks):
        if n:
            out.append(">")
        if child["type"] == "table":
            _emit_table(child, out, "> ")
        elif child["type"] == "bullets":
            for item in child["items"]:
                out.extend(_wrap_item(item, "> "))
        else:
            out.extend(_wrap(child.get("text", ""), "> "))


def _emit(block, out):
    kind = block["type"]
    if kind == "section":
        out += ["", f"## {block['text']}", ""]
    elif kind == "step":
        out += ["", f"### {block['text']}", ""]
    elif kind == "row":
        out.append("")
        out.extend(_wrap(f"**{block['kind']}** \u2014 {block['text']}", "> "))
        out.append("")
    elif kind == "banner":          # legacy single-paragraph callout
        out += ["", f"> [!{ALERT_FOR[block['kind']]}]"]
        out.extend(_wrap(block["text"], "> "))
        out.append("")
    elif kind == "box":
        out += ["", f"> [!{ALERT_FOR.get(block['kind'], 'NOTE')}]"]
        _emit_quoted(block["blocks"], out)
        out.append("")
    elif kind == "para":
        out.append("")
        out.extend(_wrap(block["text"]))
        out.append("")
    elif kind == "table":
        out.append("")
        _emit_table(block, out)
        out.append("")
    elif kind == "bullets":
        out.append("")
        for item in block["items"]:
            out.extend(_wrap_item(item))
        out.append("")
    elif kind == "image":
        out += ["", f"![{block['caption']}]({block['path']})"
                    f"{{width={block['width']}}}", ""]


def to_markdown(meta, title, subtitle, blocks, pdf_name):
    from_name = re.search(r"_Rev_([A-Z])", pdf_name)
    front = {
        "sop": meta.get("document") or meta.get("footer_doc", ""),
        "title": meta.get("footer_title") or title.title(),
        "subtitle": subtitle,
        "revision": (meta.get("revision") or meta.get("footer_rev")
                     or (f"Rev. {from_name.group(1)}" if from_name else "")),
        "author": meta.get("author", ""),
        "date": meta.get("date", ""),
        "location": meta.get("location", ""),
        "status": meta.get("status", ""),
        "output": pdf_name,
    }
    lines = ["---"] + [f"{k}: {v}" for k, v in front.items()] + ["---", ""]
    for block in blocks:
        _emit(block, lines)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).rstrip() + "\n"


def convert(pdf_path, outdir):
    pdf_path, outdir = Path(pdf_path), Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    meta, title, subtitle, blocks, warnings = parse_pdf(pdf_path, outdir)
    md_path = outdir / (pdf_path.stem + ".md")
    md_path.write_text(to_markdown(meta, title, subtitle, blocks, pdf_path.name),
                       encoding="utf-8")
    return md_path, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help="PDF files to import")
    ap.add_argument("--outdir", default="md", help="destination directory for .md files")
    args = ap.parse_args()
    for pdf in args.inputs:
        out, warnings = convert(pdf, args.outdir)
        print(f"{pdf} -> {out}")
        for warning in warnings:
            print(f"  ! {warning}")


if __name__ == "__main__":
    main()
