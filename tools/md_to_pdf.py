#!/usr/bin/env python3
"""Render an XAMS SOP markdown file to PDF in the canonical house style.

    md_to_pdf.py input.md [-o output.pdf]
    md_to_pdf.py input.md --outdir ../XAMS_Operations_Manual_2026-08-07
"""

import argparse
import io
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image,
                                KeepTogether, PageBreak, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

import sop_style as st
from sop_doc import inline, load
from sop_symbols import WarningTriangle

# Administrative fields, shown in the Document control block on the back page.
# Preparation, review and approval are three separate roles and are recorded
# separately; a document with no approver is a draft and its status says so.
CONTROL_LAYOUT = [
    ("Document", "doc_id"),
    ("Revision", "revision"),
    ("Issued", "issue_date"),
    ("Supersedes", "supersedes"),
    ("Prepared by", "prepared_by"),
    ("Reviewed by", "reviewed_by"),
    ("Approved by", "approved_by"),
    ("Status", "status"),
]
CONTROL_SECTION = "Document control"


def _footer_painter(footer_text, total):
    """`onPage` handler drawing the running footer.

    `total` is None on the counting pass, when the page count is not yet known.
    """

    def paint(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", st.FOOTER_SIZE)
        canvas.setFillColor(st.GREEN)
        canvas.drawString(st.MARGIN_X, st.FOOTER_Y, footer_text)
        canvas.setFont("Helvetica", st.FOOTER_SIZE)
        page = f"Page {doc.page}" if total is None else f"Page {doc.page} of {total}"
        canvas.drawRightString(st.PAGESIZE[0] - st.MARGIN_X, st.FOOTER_Y, page)
        canvas.restoreState()

    return paint


class SopDocTemplate(BaseDocTemplate):
    """Adds the PDF outline, so the bookmark pane mirrors the procedure.

    Flowables that belong in the outline are tagged with `_outline` by
    `_flowables`; a section bar is a Table and a step is a Paragraph, so a tag is
    more reliable than inspecting the flowable itself.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._outline_seq = 0
        self._seen_section = False

    def afterFlowable(self, flowable):
        entry = getattr(flowable, "_outline", None)
        if not entry:
            return
        text, level = entry
        if level == 0:
            self._seen_section = True
        elif not self._seen_section:
            level = 0          # a step before any section, rather than a gap
        key = f"sop-outline-{self._outline_seq}"
        self._outline_seq += 1
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level=level, closed=False)


SOP_ID_RE = re.compile(r"^SOP-\d+$", re.I)


def _eyebrow(doc):
    """The SOP number over the title, letterspaced so it reads as a label."""
    sop = doc.meta.get("sop", "").strip()
    # only a real SOP number earns the eyebrow; the index keeps its identifier
    # in the line below the title
    if not SOP_ID_RE.match(sop):
        return None
    return Paragraph(inline("\u2009".join(sop.upper())), st.S_EYEBROW)


def _ident_line(doc, skip_doc_id=False):
    """The one line of identification the operator needs on page 1."""
    meta = doc.meta
    parts = [] if skip_doc_id else [doc.doc_id]
    parts.append(meta.get("revision", ""))
    issued = meta.get("issue_date", "")
    if issued:
        parts.append(f"Issued {issued}")
    parts += [meta.get("location", ""), meta.get("audience", "")]
    return Paragraph(inline("  ·  ".join(p for p in parts if p)), st.S_IDENT)


def _control_grid(doc):
    """Administrative fields as a label/value grid for the back page."""
    rows = []
    for i in range(0, len(CONTROL_LAYOUT), 2):
        row = []
        for label, key in CONTROL_LAYOUT[i:i + 2]:
            value = doc.doc_id if key == "doc_id" else doc.meta.get(key, "")
            row.append(Paragraph(label, st.S_META_LABEL))
            row.append(Paragraph(inline(value or "-"), st.S_META_VALUE))
        rows.append(row)
    tbl = Table(rows, colWidths=st.CONTROL_COLS)
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, st.GRID),
        ("BACKGROUND", (0, 0), (0, -1), st.BG_META_LABEL),
        ("BACKGROUND", (2, 0), (2, -1), st.BG_META_LABEL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def _banner(block):
    spec = st.BANNER_KINDS[block["kind"]]
    para_style = ParagraphStyle(
        f"banner_{block['kind']}", fontName="Helvetica-Bold" if spec["bold"] else "Helvetica",
        fontSize=spec["size"], leading=spec["size"] + 2.6, textColor=spec["color"],
    )
    tbl = Table([[Paragraph(inline(block["text"]), para_style)]],
                colWidths=[st.CONTENT_WIDTH])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, -1), spec["bg"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]
    if spec["border"]:
        style_cmds.append(("BOX", (0, 0), (-1, -1), 1.2, spec["border"]))
    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def _section(block):
    tbl = Table([[Paragraph(inline(block["text"]), st.S_SECTION)]],
                colWidths=[st.CONTENT_WIDTH], rowHeights=[st.SECTION_BAR_H])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), st.GREEN),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14.2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ]))
    return tbl


def _row(block):
    kind = block["kind"]
    spec = st.row_style(kind)
    body_style = st.body_style(kind)
    paras = [p for p in block["text"].split("\n\n") if p.strip()]
    body = []
    for n, text in enumerate(paras):
        if n:
            body.append(Spacer(1, 6))
        body.append(Paragraph(inline(text), body_style))
    tbl = Table(
        [[Paragraph(kind, st.label_style(kind)), body]],
        colWidths=st.ROW_COLS,
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), spec["bg"]),
        ("BOX", (0, 0), (-1, -1), 0.6, st.GRID),
        ("LINEAFTER", (0, 0), (0, 0), 0.4, st.GRID),
        ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
        ("VALIGN", (1, 0), (1, 0), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), st.ROW_PAD),
        ("RIGHTPADDING", (0, 0), (-1, -1), st.ROW_PAD),
        ("TOPPADDING", (0, 0), (-1, -1), st.ROW_PAD),
        ("BOTTOMPADDING", (0, 0), (-1, -1), st.ROW_PAD),
    ]))
    return tbl


BIND_MAX_HEIGHT = 230.0     # a section bar is only bound to a shorter neighbour


def _height(flowables):
    total = 0.0
    for flowable in flowables:
        # KeepTogether cannot be measured itself; measure what it holds
        if isinstance(flowable, KeepTogether):
            total += _height(flowable._content)
            continue
        try:
            total += flowable.wrap(st.CONTENT_WIDTH, 10_000)[1]
        except Exception:                       # noqa: BLE001 - unmeasurable, assume large
            return float("inf")
    return total


def _signal_band(kind, spec, width):
    """Header band of a safety callout: safety-alert triangle, then the word."""
    label = Paragraph(spec["signal"], st.signal_style(kind))
    if spec["triangle"]:
        gap = 7.0
        cells = [[WarningTriangle(st.SIGNAL_SIZE), label]]
        widths = [st.SIGNAL_SIZE + gap, width - st.SIGNAL_SIZE - gap]
    else:
        cells = [[label]]
        widths = [width]
    tbl = Table(cells, colWidths=widths, rowHeights=[st.SIGNAL_BAND_H])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), spec["band"]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return tbl


def _box(block, base_dir, width):
    spec = st.box_style(block["kind"])
    inner_width = width - 2 * st.BOX_PAD
    inner = []
    if spec["signal"]:
        inner.extend([_signal_band(block["kind"], spec, inner_width), Spacer(1, 6)])
    for child in block["blocks"]:
        inner.extend(_flowables(child, base_dir, inner_width, nested=True))
    tbl = Table([[inner]], colWidths=[width])
    cmds = [
        ("BACKGROUND", (0, 0), (-1, -1), spec["bg"]),
        ("LEFTPADDING", (0, 0), (-1, -1), st.BOX_PAD),
        ("RIGHTPADDING", (0, 0), (-1, -1), st.BOX_PAD),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]
    if spec["border"]:
        cmds.append(("BOX", (0, 0), (-1, -1), 1.2, spec["border"]))
    tbl.setStyle(TableStyle(cmds))
    return tbl


def _plain_table(block, width):
    """Two-column label/value grid as used inside callout boxes."""
    label_w = min(140.0, width * 0.32)
    data = [[Paragraph(inline(row[0]), st.S_DEFTERM),
             Paragraph(inline(row[1] if len(row) > 1 else ""), st.S_BODY)]
            for row in block["rows"]]
    tbl = Table(data, colWidths=[label_w, width - label_w])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return tbl


def _column_widths(block, ncols, total=None):
    """Share the width out by measured text, never splitting a word.

    Character counts are a poor proxy: a column of short codes like "SOP-006"
    was coming out narrower than the code itself and wrapping onto two lines.
    """
    total = total or st.CONTENT_WIDTH
    padding = 16.0                      # left + right cell padding
    header = block.get("header") or []
    rows = block["rows"]

    def measure(text, bold):
        plain = re.sub(r"[*`~^]", "", text)
        font = "Helvetica-Bold" if bold else "Helvetica"
        return stringWidth(plain, font, st.S_TABLE_CELL.fontSize)

    minimum, wanted = [], []
    for i in range(ncols):
        cells = [(header[i], True)] if i < len(header) else []
        cells += [(r[i], False) for r in rows if i < len(r)]
        # a column must fit its widest single word, or the text breaks mid-word
        widest_word = max((measure(word, bold)
                           for text, bold in cells for word in text.split() or [""]),
                          default=0)
        minimum.append(min(widest_word + padding, total * 0.6))
        wanted.append(min(max((measure(t, b) for t, b in cells), default=0) + padding,
                          total * 0.6))

    if sum(wanted) <= total:                    # everything fits on one line
        slack = total - sum(wanted)
        share = sum(wanted) or 1
        return [w + slack * w / share for w in wanted]

    slack = total - sum(minimum)
    if slack <= 0:                              # nothing fits; fall back to equal
        return [total / ncols] * ncols
    extra = [max(w - m, 0) for w, m in zip(wanted, minimum)]
    share = sum(extra) or 1
    return [m + slack * e / share for m, e in zip(minimum, extra)]


def _table(block, base_dir):
    head = [Paragraph(inline(c), st.S_TABLE_HEAD) for c in block["header"]]
    body = [[Paragraph(inline(c), st.S_TABLE_CELL) for c in r] for r in block["rows"]]
    ncols = max(len(block["header"]), 1)
    tbl = Table([head] + body, colWidths=_column_widths(block, ncols), repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), st.GREEN),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, st.BG_TABLE_ZEBRA]),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, st.GRID),
        ("BOX", (0, 0), (-1, -1), 0.6, st.GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
    ]))
    return tbl


def _image(block, base_dir):
    path = (base_dir / block["path"]).resolve()
    if not path.exists():
        return Paragraph(inline(f"[missing image: {block['path']}]"), st.S_CAPTION)
    iw, ih = ImageReader(str(path)).getSize()
    width_spec = block.get("width")
    if width_spec and width_spec.endswith("%"):
        target = st.CONTENT_WIDTH * float(width_spec[:-1]) / 100.0
    elif width_spec:
        target = float(width_spec.rstrip("pt"))
    else:
        target = min(st.CONTENT_WIDTH, iw)
    target = min(target, st.CONTENT_WIDTH)
    img = Image(str(path), width=target, height=target * ih / iw)
    img.hAlign = "CENTER"
    if block["caption"]:
        return KeepTogether([img, Paragraph(inline(block["caption"]), st.S_CAPTION)])
    return img


def _plain(text):
    """Markdown text as it should read in an outline or contents entry."""
    return re.sub(r"[*`~^]", "", text).strip()


def _flowables(block, base_dir, width=st.CONTENT_WIDTH, nested=False):
    kind = block["type"]
    if kind == "banner":
        return [_banner(block), Spacer(1, 11.4)]
    if kind == "box":
        return [Spacer(1, 7), _box(block, base_dir, width), Spacer(1, 7)]
    if kind == "section":
        # a bar with nothing under it looks broken: demand some room first
        bar = _section(block)
        bar._outline = (_plain(block["text"]), 0)
        return [CondPageBreak(150), bar, Spacer(1, 8.5)]
    if kind == "step":
        step = Paragraph(inline(block["text"]), st.S_STEP)
        step._outline = (_plain(block["text"]), 1)
        return [step]
    if kind == "row":
        return [_row(block)]
    if kind == "para":
        return [Spacer(1, 6), Paragraph(inline(block["text"]), st.S_BODY), Spacer(1, 6)]
    if kind == "bullets":
        return [Spacer(1, 6)] + [Paragraph(inline(i), st.S_BULLET, bulletText="\u2022")
                                 for i in block["items"]]
    if kind == "table":
        table = _plain_table(block, width) if block.get("style") == "plain" \
            else _table(block, base_dir)
        # a very short table should not be split; longer ones may flow onto the
        # next page, where repeatRows redraws the header
        if not nested and len(block["rows"]) <= 4:
            table = KeepTogether(table)
        return [Spacer(1, 8), table, Spacer(1, 8)]
    if kind == "image":
        return [Spacer(1, 8), _image(block, base_dir), Spacer(1, 8)]
    if kind == "pagebreak":
        return [PageBreak()]
    return []


def build_story(doc, base_dir, blank_page=False):
    story = []
    eyebrow = _eyebrow(doc)
    if eyebrow:
        story.append(eyebrow)
    story.append(Paragraph(inline(doc.meta.get("title", "")).upper(), st.S_TITLE))
    subtitle = doc.meta.get("subtitle")
    if subtitle:
        story.append(Paragraph(inline(subtitle), st.S_SUBTITLE))
    # with the number set over the title the identifier need not repeat below it
    story.append(_ident_line(doc, skip_doc_id=eyebrow is not None))

    seen_control = False
    for block in doc.blocks:
        story.extend(_flowables(block, base_dir))
        # the administrative grid comes straight from the frontmatter, so it is
        # generated rather than written out again in every source
        if block["type"] == "section" and _plain(block["text"]) == CONTROL_SECTION:
            story.extend([_control_grid(doc), Spacer(1, 10)])
            seen_control = True
    if not seen_control:
        story.extend(_flowables({"type": "section", "text": CONTROL_SECTION}, base_dir))
        story.append(_control_grid(doc))
    if blank_page:
        story.extend([PageBreak(),
                      Paragraph("This page is intentionally blank.", st.S_BLANK)])
    return story


def _render_once(doc, base_dir, target, total, blank_page=False):
    """Lay the document out into `target`, returning the page count."""
    keywords = ", ".join(p for p in (doc.doc_id, "XAMS", "Nikhef",
                                     doc.meta.get("revision", ""), "SOP") if p)
    pdf = SopDocTemplate(
        target, pagesize=st.PAGESIZE,
        leftMargin=st.MARGIN_X, rightMargin=st.MARGIN_X,
        topMargin=st.MARGIN_TOP, bottomMargin=st.MARGIN_BOTTOM,
        title=f"{doc.doc_id} {doc.meta.get('title', '')}".strip(),
        author=doc.meta.get("author", ""),
        subject=doc.meta.get("subtitle", ""),
        creator="XAMS SOP toolchain (tools/build.py)",
        keywords=keywords,
    )
    frame = Frame(st.MARGIN_X, st.MARGIN_BOTTOM, st.CONTENT_WIDTH,
                  st.PAGESIZE[1] - st.MARGIN_TOP - st.MARGIN_BOTTOM, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    pdf.addPageTemplates([PageTemplate(id="sop", frames=[frame],
                                       onPage=_footer_painter(doc.footer, total))])
    pdf.build(build_story(doc, base_dir, blank_page=blank_page))
    return pdf.page


def render(md_path, out_path=None, outdir=None):
    doc = load(md_path)
    base_dir = Path(md_path).parent
    if out_path is None:
        out_path = Path(outdir or base_dir) / doc.output_name
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # `Page x of y` needs a total that only exists once the document has been
    # laid out, so it is rendered twice: once into a throwaway buffer to count
    # the pages, then for real. The footer is painted on the canvas outside the
    # text frame, so adding it cannot change the pagination between the two.
    #
    # The obvious alternative - a canvas that buffers pages and stamps the
    # footer at save time - breaks every bookmark and internal link, because
    # the destinations are bound while the pages are being buffered.
    #
    # The manual is printed double-sided, so the count is rounded up to an even
    # number and the padding page is added on the second pass. It sits after a
    # PageBreak with a single line on it, so it adds exactly one page and cannot
    # disturb the pagination the first pass measured.
    laid_out = _render_once(doc, base_dir, io.BytesIO(), None)
    total = laid_out + laid_out % 2
    _render_once(doc, base_dir, str(out_path), total, blank_page=total != laid_out)
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="markdown source")
    ap.add_argument("-o", "--output", help="explicit output PDF path")
    ap.add_argument("--outdir", help="directory for the PDF (name taken from frontmatter)")
    args = ap.parse_args()
    out = render(args.input, args.output, args.outdir)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
