# XAMS Operations Manual

Standard Operating Procedures for the XAMS xenon TPC at Nikhef.

The markdown files in [`md/`](md) are the source of truth. The PDFs are
generated from them and are never edited by hand: edit the markdown, rebuild,
and every document keeps the same house style.

    md/SOP_004_LXe_Filling_Procedure.md
      ->  tools/build.py
      ->  XAMS_Operations_Manual_<date>/SOP_004_LXe_Filling_Procedure_Rev_E.pdf

Source files carry **no revision in their name**; the revision lives in the
frontmatter and is stamped onto the PDF automatically. Issuing a new revision is
therefore a one-line edit, not a rename.

## Layout

| Path | Contents |
| --- | --- |
| `md/` | one markdown file per SOP, plus the hand-written index, `figs/` and `assets/` |
| `tools/` | the renderer, validator and build script |
| `XAMS_Operations_Manual_<date>/` | generated output, not tracked in git |

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
run if `check_md.py` reports an error. Besides one PDF per document it writes
`XAMS_Operations_Manual_Complete.pdf` - the whole manual in one file, in reading
order, with a bookmark per document. That is the file to print.

Every document is rendered to an even page count, so in the combined file each
one still begins on a right-hand page when printed double-sided. Where the
content ends on an odd page the last page says so, rather than looking like a
printing fault. Useful flags:

    build.py --no-combined                      # skip the single-file print copy
    build.py --outdir dist                      # somewhere else
    build.py --no-clean                         # keep existing PDFs, overwrite in place
    build.py --srcdir md --check --refdir OLD   # diff text against older PDFs
    build.py --force                            # render despite validation errors

The output directory is cleaned before each build, so a renamed or deleted
document cannot leave a stale PDF behind. Cleaning removes only `*.pdf` from the
top level of that directory and nothing else - the P&ID is copied back in from
`md/assets/` on every build. Pass `--no-clean` to keep what is there.

Render a single document while editing:

    tools/.venv/bin/python tools/md_to_pdf.py md/SOP_004_LXe_Filling_Procedure.md -o /tmp/preview.pdf

## Writing a new SOP

Name the file `SOP_<nnn>_<Short_Name>.md` - number first, so `md/` and the built
manual both sort in procedure order, and no revision in the name.

Copy [`tools/TEMPLATE.md`](tools/TEMPLATE.md) into `md/`, or paste
[`tools/PROMPT.md`](tools/PROMPT.md) into ChatGPT along with a description of the
procedure and save the reply under that name. Ask a model for
markdown, never for a PDF - layout comes from the renderer, so the document
cannot drift out of house style.

Then validate, build, and read the PDF.

## Syntax

Standard GitHub-flavored markdown, so the sources preview correctly in VS Code.

| Construct | Meaning |
| --- | --- |
| frontmatter keys | title block and footer; `title:` and `subtitle:` also fill the index register |
| `## A. Name` | section, drawn as a green bar |
| `### 1. Name` | numbered step |
| `> **ACTION** — text` | procedure row; also `VERIFY`, `STOP`, `NOTE` |
| `> [!WARNING]` etc. | callout box; `NOTE` `TIP` `IMPORTANT` `CAUTION` `WARNING` |
| pipe table | reference table; empty header cells give a plain label/value grid |
| `![cap](figs/x.png){width=70%}` | figure |
| `**bold**`, `*italic*`, `^sup^`, `~sub~` | inline formatting |

Not supported: links, code fences, raw HTML, headings beyond `###`.
`check_md.py` flags all of these.

`md/.passthrough` lists files copied into the build unchanged, one path per line
relative to `md/`. Currently it holds the P&ID drawing, which has no markdown
source; it lives in `md/assets/` so that it is tracked in git rather than only
existing inside a generated manual folder.

`XAMS_Operations_Manual_Index.md` is written by hand rather than imported:
the index is a summary document, not a procedure, so it uses tables and bullets
instead of ACTION/VERIFY rows. Update it whenever an SOP is added or its
revision changes - `check_md.py` compares its register against the frontmatter of
every SOP and reports anything that has drifted.

## Consistency checks

Run over the whole directory, `check_md.py` also checks the manual as a whole:

- two files claiming the same SOP number **and** revision - an error, since only
  one can be current
- several revisions of one SOP - a warning naming the one it treats as current;
  superseded revisions belong in `old/`
- an SOP missing from the index register, or a register entry with no file
- a register revision that disagrees with the file's frontmatter
- a revision left in a source filename, or a stale `output:` override

`build.py` runs all of this first and refuses to render if anything is an error.

When you bump a revision in an SOP, update the register with:

    tools/.venv/bin/python tools/check_md.py md --fix

That rewrites the derived columns of **every** SOP table in the index -
`Rev.` from `revision:`, `Procedure` from `title:`, `Purpose` from `subtitle:`
and `Status` from `status:` - so the index cannot drift from the procedures it
lists. Any other column, such as "Condition to move on", is left alone, and so
is prose outside the tables.

`Status` is the one derived value that is not copied verbatim: a `status:`
containing "draft" or "placeholder" shows as `DRAFT`, anything else as
`Released`. The build
never edits your sources; run `--fix` yourself so the change shows up in a diff.

A revision mismatch is an error and blocks the build; a stale procedure name or
purpose is only a warning.

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
