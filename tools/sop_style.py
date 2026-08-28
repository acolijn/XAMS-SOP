"""Canonical visual template for XAMS SOP documents.

All geometry and colour constants were measured from the generated
ReportLab PDFs in XAMS_Operations_Manual_2026-08-07/ so that re-rendered
documents match the existing house style.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm

# --- palette ---------------------------------------------------------------
GREEN = colors.HexColor("#0f5a42")        # titles, section bars, step numbers
GREEN_DARK = colors.HexColor("#0c3f31")   # emphasised body text
RED = colors.HexColor("#8e1f1f")          # STOP label, DANGER band and border
GREY_TEXT = colors.HexColor("#4f4f4f")    # subtitle
GREY_LABEL = colors.HexColor("#555555")   # metadata labels
GRID = colors.HexColor("#b7c2c8")

# signal-word palette (ISO 3864-2 / ANSI Z535.6 colour conventions: DANGER red
# on white, WARNING orange on black, CAUTION yellow on black, NOTICE blue on
# white)
AMBER = colors.HexColor("#c8860d")        # WARNING band
AMBER_LIGHT = colors.HexColor("#f0c96b")  # CAUTION band
AMBER_DARK = colors.HexColor("#9a6a09")   # WARNING / CAUTION border
SLATE = colors.HexColor("#4f6b80")        # NOTICE band and border

BG_ACTION = colors.HexColor("#e8f2ee")
BG_VERIFY = colors.HexColor("#fff3c4")
BG_STOP = colors.HexColor("#f7dddd")
BG_NOTE = colors.HexColor("#e9f0f6")
BG_DANGER = colors.HexColor("#f7dddd")
BG_WARNING = colors.HexColor("#fdf1dc")
BG_CAUTION = colors.HexColor("#fdf8ea")
BG_NOTICE = colors.HexColor("#eef2f6")
BG_META_LABEL = colors.HexColor("#e9f0f6")
BG_TABLE_ZEBRA = colors.HexColor("#f4f9f7")   # alternate rows in reference tables

# --- page geometry ---------------------------------------------------------
PAGESIZE = A4
MARGIN_X = 39.685          # 14 mm
MARGIN_TOP = 39.685        # 14 mm
MARGIN_BOTTOM = 42.0
CONTENT_WIDTH = PAGESIZE[0] - 2 * MARGIN_X      # 515.9 pt
FOOTER_Y = 25.0
FOOTER_SIZE = 8.0

# metadata table: label | value | label | value
META_COLS = [73.7, 192.7, 73.7, 175.8]
META_ROW_H = 27.17

# document-control grid on the back page: label | value | label | value
CONTROL_COLS = [88.0, 170.0, 88.0, CONTENT_WIDTH - 346.0]

# ACTION/VERIFY/STOP/NOTE bands: label | content
ROW_LABEL_W = 76.5
ROW_COLS = [ROW_LABEL_W, CONTENT_WIDTH - ROW_LABEL_W]
ROW_PAD = 8.5
BODY_SIZE = 10.5
BODY_LEADING = 13.0

SECTION_BAR_H = 33.0
STEP_INDENT = 25.8

# --- row kinds -------------------------------------------------------------
# label colour, background, body is bold, body colour
ROW_KINDS = {
    "ACTION": dict(label_color=GREEN_DARK, bg=BG_ACTION, bold=True, color=GREEN_DARK),
    "VERIFY": dict(label_color=GREEN_DARK, bg=BG_VERIFY, bold=False, color=colors.black),
    "STOP":   dict(label_color=RED,        bg=BG_STOP,   bold=True, color=GREEN_DARK),
    "NOTE":   dict(label_color=GREEN_DARK, bg=BG_NOTE,   bold=False, color=colors.black),
}

BANNER_KINDS = {
    "warning": dict(bg=BG_STOP, border=RED, color=RED, bold=True, size=11.0),
    "info":    dict(bg=BG_NOTE, border=None, color=colors.black, bold=False, size=10.6),
}

# --- callout boxes ---------------------------------------------------------
# The first four kinds are the ISO 3864-2 / ANSI Z535.6 signal-word classes and
# render with a signal-word header band. The safety-alert triangle means
# *personal injury*, so NOTICE - property damage only - deliberately has none.
# The remaining kinds are plain callouts: background colour, no band.
SIGNAL_SIZE = 12.5          # triangle edge length in the header band
SIGNAL_BAND_H = 19.0
BOX_PAD = 10.0

BOX_KINDS = {
    "danger":  dict(bg=BG_DANGER,  border=RED,        band=RED,
                    band_text=colors.white, signal="DANGER",  triangle=True),
    "warning": dict(bg=BG_WARNING, border=AMBER_DARK, band=AMBER,
                    band_text=colors.black, signal="WARNING", triangle=True),
    "caution": dict(bg=BG_CAUTION, border=AMBER_DARK, band=AMBER_LIGHT,
                    band_text=colors.black, signal="CAUTION", triangle=True),
    "notice":  dict(bg=BG_NOTICE,  border=SLATE,      band=SLATE,
                    band_text=colors.white, signal="NOTICE",  triangle=False),
    "action":  dict(bg=BG_ACTION, border=None, band=None, band_text=None,
                    signal=None, triangle=False),
    "verify":  dict(bg=BG_VERIFY, border=None, band=None, band_text=None,
                    signal=None, triangle=False),
    "stop":    dict(bg=BG_STOP,   border=None, band=None, band_text=None,
                    signal=None, triangle=False),
    "note":    dict(bg=BG_NOTE,   border=None, band=None, band_text=None,
                    signal=None, triangle=False),
    "info":    dict(bg=BG_NOTE,   border=None, band=None, band_text=None,
                    signal=None, triangle=False),
}

SIGNAL_KINDS = tuple(k for k, v in BOX_KINDS.items() if v["signal"])
INJURY_KINDS = tuple(k for k, v in BOX_KINDS.items() if v["triangle"])

# --- paragraph styles ------------------------------------------------------
# The document identifier as an eyebrow over the title: on a stack of printed
# SOPs the number is what the operator looks for, and the title only confirms it.
S_EYEBROW = ParagraphStyle(
    "eyebrow", fontName="Helvetica-Bold", fontSize=13, leading=16,
    textColor=GREEN, alignment=1, spaceAfter=3,
)
S_TITLE = ParagraphStyle(
    "title", fontName="Helvetica-Bold", fontSize=22, leading=26,
    textColor=GREEN, alignment=1, spaceAfter=11,
)
S_SUBTITLE = ParagraphStyle(
    "subtitle", fontName="Helvetica-Bold", fontSize=11, leading=14,
    textColor=GREY_TEXT, alignment=1, spaceAfter=16,
)
S_META_LABEL = ParagraphStyle(
    "meta_label", fontName="Helvetica-Bold", fontSize=8.2, leading=10,
    textColor=GREY_LABEL,
)
# The cover carries one identification line instead of a metadata grid: every
# page already repeats the identifier and revision in the footer, so page 1
# belongs to the operator, and the administrative fields live on the back page.
S_IDENT = ParagraphStyle(
    "ident", fontName="Helvetica", fontSize=9.5, leading=12.5,
    textColor=GREY_LABEL, alignment=1, spaceBefore=2, spaceAfter=14,
)
S_META_VALUE = ParagraphStyle(
    "meta_value", fontName="Helvetica", fontSize=BODY_SIZE, leading=BODY_LEADING,
)
S_SECTION = ParagraphStyle(
    "section", fontName="Helvetica-Bold", fontSize=14, leading=17,
    textColor=colors.white,
)
S_STEP = ParagraphStyle(
    "step", fontName="Helvetica-Bold", fontSize=12, leading=15,
    textColor=GREEN, leftIndent=STEP_INDENT, spaceBefore=11.3, spaceAfter=8.5,
)
S_BODY = ParagraphStyle(
    "body", fontName="Helvetica", fontSize=BODY_SIZE, leading=BODY_LEADING,
)
S_BULLET = ParagraphStyle(
    "bullet", parent=S_BODY, leftIndent=14, bulletIndent=4, spaceAfter=6,
)
S_CAPTION = ParagraphStyle(
    "caption", fontName="Helvetica-Oblique", fontSize=9, leading=11,
    textColor=GREY_TEXT, alignment=1, spaceBefore=4, spaceAfter=10,
)
S_DEFTERM = ParagraphStyle(
    "defterm", fontName="Helvetica-Bold", fontSize=BODY_SIZE, leading=BODY_LEADING,
    textColor=GREEN_DARK,
)
S_TABLE_HEAD = ParagraphStyle(
    "thead", fontName="Helvetica-Bold", fontSize=10, leading=13,
    textColor=colors.white,
)
S_TABLE_CELL = ParagraphStyle(
    "tcell", fontName="Helvetica", fontSize=10, leading=13,
)
# Documents are printed double-sided, so an odd page count leaves a blank back on
# the last sheet. It is padded to an even count and the filler says so, because a
# silent blank page in a controlled document reads as a printing fault.
S_BLANK = ParagraphStyle(
    "blank", fontName="Helvetica-Oblique", fontSize=9.5, leading=12,
    textColor=GREY_TEXT, alignment=1, spaceBefore=24,
)


def row_style(kind):
    return ROW_KINDS[kind]


def body_style(kind):
    """Paragraph style for the content column of a given row kind."""
    spec = ROW_KINDS[kind]
    return ParagraphStyle(
        f"body_{kind}", parent=S_BODY,
        fontName="Helvetica-Bold" if spec["bold"] else "Helvetica",
        textColor=spec["color"],
    )


def label_style(kind):
    spec = ROW_KINDS[kind]
    return ParagraphStyle(
        f"label_{kind}", fontName="Helvetica-Bold", fontSize=BODY_SIZE,
        leading=BODY_LEADING, textColor=spec["label_color"],
    )


def box_style(kind):
    return BOX_KINDS.get(kind, BOX_KINDS["info"])


def signal_style(kind):
    """Paragraph style for the signal word in a safety callout's header band."""
    spec = BOX_KINDS[kind]
    return ParagraphStyle(
        f"signal_{kind}", fontName="Helvetica-Bold", fontSize=11.5, leading=13.5,
        textColor=spec["band_text"],
    )
