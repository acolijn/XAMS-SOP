# XAMS SOP toolchain

The markdown files in [`md/`](../md) are the source of truth for the operations
manual. PDFs are generated from them and are never edited by hand.

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

Copy [`TEMPLATE.md`](TEMPLATE.md) into `md/`, or paste [`PROMPT.md`](PROMPT.md)
into ChatGPT along with a description of the procedure and save the reply as
`md/<Name>_SOP_<nnn>_Rev_<X>.md`. Ask a model for markdown, never for a PDF -
layout comes from the renderer, so the document cannot drift out of house style.

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

## Files

| File | Role |
| --- | --- |
| `sop_doc.py` | parses the markdown dialect into blocks |
| `sop_style.py` | the house style: colours, fonts, geometry, all in one place |
| `md_to_pdf.py` | renders one markdown file to PDF |
| `build.py` | validates and renders everything |
| `check_md.py` | reports anything the renderer would drop |
| `pdf_to_md.py` | **one-shot migration tool** used to import the original PDFs |

`pdf_to_md.py` has done its job and is kept only for reference. A new procedure
should be written as markdown, not produced as a PDF and imported.

## Changing the look

Every colour, font size and measurement lives in `sop_style.py`. Change it there
and rebuild; all documents follow. Do not put styling in the markdown.

## Setup on another machine

    python3 -m venv tools/.venv
    tools/.venv/bin/pip install reportlab pymupdf
