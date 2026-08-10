# XAMS Operations Manual

Standard Operating Procedures for the XAMS xenon TPC at Nikhef.

The markdown files in [`md/`](md) are the source of truth. The PDFs are
generated from them and are never edited by hand: edit the markdown, rebuild,
and every document keeps the same house style.

    md/*.md  ->  tools/build.py  ->  XAMS_Operations_Manual_<date>/*.pdf

## Layout

| Path | Contents |
| --- | --- |
| `md/` | one markdown file per SOP, plus the hand-written index and `figs/` |
| `tools/` | the renderer, validator and build script |
| `XAMS_Operations_Manual_<date>/` | generated output, not tracked in git |
| `old/` | superseded PDFs, kept for reference only |

## Installation

Requires Python 3.9 or newer. From the repository root:

    python3 -m venv tools/.venv
    tools/.venv/bin/pip install reportlab pymupdf

That is the whole setup - `tools/.venv/` is git-ignored, so each machine
creates its own. `reportlab` renders the PDFs; `pymupdf` is used by the
validator and by the one-shot PDF importer.

Check it works:

    tools/.venv/bin/python tools/check_md.py md
    tools/.venv/bin/python tools/build.py

The second command writes `XAMS_Operations_Manual_<today>/`.

## Everyday use

    tools/.venv/bin/python tools/check_md.py md    # validate sources
    tools/.venv/bin/python tools/build.py          # render all PDFs

`build.py` writes to `XAMS_Operations_Manual_<today>/` by default and refuses to
run if `check_md.py` reports an error. Useful flags:

    build.py --outdir dist                      # somewhere else
    build.py --clean                            # drop the PDFs already in outdir first
    build.py --srcdir md --check --refdir OLD   # diff text against older PDFs
    build.py --force                            # render despite validation errors

Rebuilding into an existing directory is safe: files are overwritten in place.
Use `--clean` when a document was renamed or deleted and you want its stale PDF
gone. `--clean` removes only `*.pdf` from the output directory, nothing else.

Render a single document while editing:

    tools/.venv/bin/python tools/md_to_pdf.py md/LXe_Filling_Procedure_SOP_004_Rev_E_9A.md -o /tmp/preview.pdf

## Writing a new SOP

Copy [`tools/TEMPLATE.md`](tools/TEMPLATE.md) into `md/`, or paste
[`tools/PROMPT.md`](tools/PROMPT.md) into ChatGPT along with a description of the
procedure and save the reply as `md/<Name>_SOP_<nnn>_Rev_<X>.md`. Ask a model for
markdown, never for a PDF - layout comes from the renderer, so the document
cannot drift out of house style.

Then validate, build, and read the PDF.

## Syntax

Standard GitHub-flavored markdown, so the sources preview correctly in VS Code.

| Construct | Meaning |
| --- | --- |
| frontmatter keys | title block and footer of the document |
| `## A. Name` | section, drawn as a green bar |
| `### 1. Name` | numbered step |
| `> **ACTION** — text` | procedure row; also `VERIFY`, `STOP`, `NOTE` |
| `> [!WARNING]` etc. | callout box; `NOTE` `TIP` `IMPORTANT` `CAUTION` `WARNING` |
| pipe table | reference table; empty header cells give a plain label/value grid |
| `![cap](figs/x.png){width=70%}` | figure |
| `**bold**`, `*italic*`, `^sup^`, `~sub~` | inline formatting |

Not supported: links, code fences, raw HTML, headings beyond `###`.
`check_md.py` flags all of these.

`md/.passthrough` lists files copied into the build unchanged - currently the
P&ID drawing, which has no markdown source.

`XAMS_Operations_Manual_Index_Rev_D.md` is written by hand rather than imported:
the index is a summary document, not a procedure, so it uses tables and bullets
instead of ACTION/VERIFY rows. Update it whenever an SOP is added or its
revision changes.

## Tools

| File | Role |
| --- | --- |
| `tools/sop_doc.py` | parses the markdown dialect into blocks |
| `tools/sop_style.py` | the house style: colours, fonts, geometry, all in one place |
| `tools/md_to_pdf.py` | renders one markdown file to PDF |
| `tools/build.py` | validates and renders everything |
| `tools/check_md.py` | reports anything the renderer would drop |
| `tools/pdf_to_md.py` | **one-shot migration tool** used to import the original PDFs |

`pdf_to_md.py` has done its job and is kept only for reference. A new procedure
should be written as markdown, not produced as a PDF and imported.

## Changing the look

Every colour, font size and measurement lives in `tools/sop_style.py`. Change it
there and rebuild; all documents follow. Do not put styling in the markdown.
