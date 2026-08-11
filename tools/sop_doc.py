"""Parser for the XAMS SOP markdown dialect.

The dialect is GitHub-flavored markdown, so sources preview correctly in an
editor and render to the house PDF style. A document looks like:

    ---
    sop: SOP-101
    title: PMT Power On / Off
    subtitle: Safely power the photomultiplier tube on and off
    revision: Rev. A
    author: Auke-Pieter Colijn
    date: 7 August 2026
    location: Nikhef - XAMS
    status: Draft placeholder
    ---

    > [!WARNING]
    > DRAFT / PLACEHOLDER - NOT FOR OPERATION

    ## A. Purpose and prerequisites

    ### 1. Confirm the approved procedure is available

    > **ACTION** — Do the thing. Long text simply wraps onto
    > further quoted lines.

    > **VERIFY** — The thing happened.

    > **STOP** — Do not do the other thing.

Also supported: bullet lists, pipe tables, `![caption](fig.png){width=60%}`,
plain paragraphs, and `\\newpage`. The `!!!`/`:::` forms are legacy syntax from
the original PDF import and are still accepted.

Source files are named `SOP_<nnn>_<Short_Name>.md` and carry no revision; the
PDF name is derived from the source name plus the revision in the frontmatter.
"""

import html
import re
from pathlib import Path

ROW_RE = re.compile(r"^(ACTION|VERIFY|STOP|NOTE)\s*:\s*(.*)$")
IMG_RE = re.compile(r"^!\[(?P<cap>.*?)\]\((?P<path>[^)]+)\)(?:\{(?P<attrs>[^}]*)\})?\s*$")
BANNER_RE = re.compile(r"^!!!\s*(warning|info)\s*$")          # legacy
BOX_RE = re.compile(r"^:::\s*(action|verify|stop|note|info|warning)\s*$")  # legacy
QUOTE_RE = re.compile(r"^>\s?(.*)$")
QUOTE_ROW_RE = re.compile(r"^\*\*(ACTION|VERIFY|STOP|NOTE)\*\*\s*(?:[-\u2013\u2014:])?\s*(.*)$")
ALERT_RE = re.compile(
    r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION|DANGER|NOTICE|CHECKLIST|CUE)\]\s*$",
    re.I)

# Alert type <-> callout kind. The kind drives the colour and, for the four
# signal-word classes, the header band in the PDF.
#
# DANGER/WARNING/CAUTION/NOTICE are the ISO 3864-2 / ANSI Z535.6 hierarchy and
# are the only forms that should be used for safety information. DANGER and
# NOTICE are not GitHub-native alert types, so an editor preview shows them as a
# plain blockquote; the PDF is the deliverable and `check_md.py` owns the
# vocabulary.
ALERT_TO_KIND = {"danger": "danger", "warning": "warning", "caution": "caution",
                 "notice": "notice", "note": "info",
                 # non-severity callouts: a completion checklist and an
                 # indication/response cue table
                 "checklist": "action", "cue": "verify",
                 # deprecated, accepted so older sources still render
                 "tip": "action", "important": "verify"}
KIND_TO_ALERT = {v: k.upper() for k, v in ALERT_TO_KIND.items()}

# Alerts that carry no severity and must not be used for safety information.
DEPRECATED_ALERTS = ("TIP", "IMPORTANT")


class SopDoc:
    def __init__(self, meta, blocks, source=None):
        self.meta = meta
        self.blocks = blocks
        self.source = source

    @property
    def footer(self):
        if self.meta.get("footer"):
            return self.meta["footer"]
        parts = [self.meta.get("title", ""), self.meta.get("document") or self.meta.get("sop", ""),
                 self.meta.get("revision", "")]
        return " | ".join(p for p in parts if p)

    @property
    def revision_slug(self):
        """'Rev. B' -> 'Rev_B'; empty when the document carries no revision."""
        revision = self.meta.get("revision", "").strip()
        return re.sub(r"[^\w]+", "_", revision).strip("_")

    @property
    def output_name(self):
        """PDF filename: the source name plus the revision from the frontmatter.

        Source files deliberately carry no revision, so a new revision means
        editing one line rather than renaming a file. The PDF does carry it,
        because printed and emailed copies must say which revision they are.
        `output:` in the frontmatter overrides this, but is rarely needed.
        """
        if self.meta.get("output"):
            return self.meta["output"]
        stem = Path(self.source).stem if self.source else "document"
        suffix = f"_{self.revision_slug}" if self.revision_slug else ""
        return f"{stem}{suffix}.pdf"


def parse_frontmatter(lines):
    """Flat `key: value` frontmatter delimited by `---`."""
    meta = {}
    if not lines or lines[0].strip() != "---":
        return meta, 0
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        if line.strip() and ":" in line:
            key, _, value = line.partition(":")
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            meta[key.strip()] = value
        i += 1
    return meta, i + 1


def parse(text, source=None):
    lines = text.replace("\r\n", "\n").split("\n")
    meta, i = parse_frontmatter(lines)
    blocks = []
    para = []

    def flush_para():
        if para:
            blocks.append({"type": "para", "text": " ".join(para).strip()})
            para.clear()

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if not line:
            flush_para()
            i += 1
            continue

        if line.startswith("<!--"):
            i += 1
            continue

        if line.startswith(">"):
            flush_para()
            quoted = []
            # a blank line ends the quote; a bare ">" separates blocks inside it
            while i < len(lines) and lines[i].strip().startswith(">"):
                quoted.append(QUOTE_RE.match(lines[i].strip()).group(1))
                i += 1
            blocks.append(_parse_quote(quoted))
            continue

        m = BOX_RE.match(line)
        if m:
            flush_para()
            kind = m.group(1)
            i += 1
            buf = []
            while i < len(lines) and lines[i].strip() != ":::":
                buf.append(lines[i])
                i += 1
            i += 1
            inner = parse("\n".join(buf))
            blocks.append({"type": "box", "kind": kind, "blocks": inner.blocks})
            continue

        m = BANNER_RE.match(line)
        if m:
            flush_para()
            kind = m.group(1)
            i += 1
            buf = []
            while i < len(lines) and lines[i].strip() != "!!!":
                buf.append(lines[i].strip())
                i += 1
            i += 1
            blocks.append({"type": "banner", "kind": kind, "text": " ".join(b for b in buf if b)})
            continue

        if line in (r"\newpage", "\\pagebreak"):
            flush_para()
            blocks.append({"type": "pagebreak"})
            i += 1
            continue

        if line.startswith("### "):
            flush_para()
            blocks.append({"type": "step", "text": line[4:].strip()})
            i += 1
            continue

        if line.startswith("## "):
            flush_para()
            blocks.append({"type": "section", "text": line[3:].strip()})
            i += 1
            continue

        if line.startswith("# "):
            flush_para()
            blocks.append({"type": "section", "text": line[2:].strip()})
            i += 1
            continue

        m = IMG_RE.match(line)
        if m:
            flush_para()
            attrs = dict(
                kv.split("=", 1) for kv in (m.group("attrs") or "").split() if "=" in kv
            )
            blocks.append({
                "type": "image",
                "path": m.group("path").strip(),
                "caption": m.group("cap").strip(),
                "width": attrs.get("width"),
            })
            i += 1
            continue

        m = ROW_RE.match(line)
        if m:
            flush_para()
            kind, first = m.group(1), m.group(2).strip()
            buf = [first] if first else []
            i += 1
            # continuation: indented lines, or unindented lines that do not start
            # a new construct
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    break
                if ROW_RE.match(nxt.strip()) or nxt.strip().startswith(("#", "!!!", ":::", "|", "- ", "![")):
                    break
                buf.append(nxt.strip())
                i += 1
            blocks.append({"type": "row", "kind": kind, "text": " ".join(buf).strip()})
            continue

        if line.startswith("- ") or line.startswith("* "):
            flush_para()
            items = []
            while i < len(lines) and lines[i].strip():
                current = lines[i]
                if current.strip()[:2] in ("- ", "* "):
                    items.append(current.strip()[2:].strip())
                elif items and current[:1] in (" ", "\t"):
                    items[-1] = f"{items[-1]} {current.strip()}"   # wrapped item
                else:
                    break
                i += 1
            blocks.append({"type": "bullets", "items": items})
            continue

        if line.startswith("|"):
            flush_para()
            rows, header_seen = [], False
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if all(set(c) <= set("-: ") and c for c in cells):
                    header_seen = True   # a `|---|` rule marks the row above as a header
                else:
                    rows.append(cells)
                i += 1
            blank_header = bool(rows) and not any(c.strip() for c in rows[0])
            if blank_header:
                rows = rows[1:]
                header_seen = False
            plain = bool(rows) and all(len(r) == 2 for r in rows) and not header_seen
            if plain:
                blocks.append({"type": "table", "style": "plain",
                               "header": [], "rows": rows})
            else:
                blocks.append({"type": "table", "style": "grid",
                               "header": rows[0] if rows else [], "rows": rows[1:]})
            continue

        para.append(line)
        i += 1

    flush_para()
    return SopDoc(meta, blocks, source=source)


def _parse_quote(quoted):
    """A blockquote is either a procedure row or a callout."""
    first = quoted[0].strip() if quoted else ""

    alert = ALERT_RE.match(first)
    if alert:
        inner = parse("\n".join(quoted[1:]))
        return {"type": "box", "kind": ALERT_TO_KIND[alert.group(1).lower()],
                "blocks": inner.blocks}

    row = QUOTE_ROW_RE.match(first)
    if row:
        text = " ".join([row.group(2)] + [q.strip() for q in quoted[1:]])
        return {"type": "row", "kind": row.group(1), "text": re.sub(r"\s+", " ", text).strip()}

    inner = parse("\n".join(quoted))
    return {"type": "box", "kind": "info", "blocks": inner.blocks}


def load(path):
    path = Path(path)
    return parse(path.read_text(encoding="utf-8"), source=str(path))


def inline(text):
    """Markdown inline formatting -> ReportLab intra-paragraph markup.

    Backslash-escaped markers (`\\*`, `\\^`, ...) are held aside first, so text
    imported from a PDF cannot be re-interpreted as formatting.
    """
    placeholders = {}

    def stash(match):
        token = f"\x00{len(placeholders)}\x00"
        placeholders[token] = match.group(1)
        return token

    out = re.sub(r"\\([*`~^\\])", stash, text)
    out = html.escape(out, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", out)
    out = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', out)
    out = re.sub(r"\^([^\^\s][^\^]*)\^", r"<super>\1</super>", out)
    out = re.sub(r"~([^~\s][^~]*)~", r"<sub>\1</sub>", out)
    for token, literal in placeholders.items():
        out = out.replace(token, html.escape(literal, quote=False))
    return out


def escape_md(text):
    """Inverse of `inline` for literal text recovered from a PDF.

    Only for raw span text: apply it before adding **bold** / ^sup^ / ~sub~
    markup, never after.
    """
    return re.sub(r"([*`~^\\])", r"\\\1", text)
