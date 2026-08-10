# Prompt for drafting a new XAMS SOP

Paste everything below the line into ChatGPT (or Claude) together with your
description of the procedure. The model writes only content; all layout,
colours, fonts, page breaks and footers come from the renderer, so never ask
for a PDF, a Word file, or any styling.

Save the reply as `md/SOP_<nnn>_<Short_Name>.md` - number first, and **no
revision in the filename** - then run:

    tools/.venv/bin/python tools/check_md.py md
    tools/.venv/bin/python tools/build.py

---

You are writing a Standard Operating Procedure for the XAMS xenon TPC at
Nikhef. Reply with **one markdown file and nothing else** - no commentary, no
code fence around the whole file.

Use exactly this syntax. Anything outside it is dropped when the document is
rendered.

**Frontmatter** - first block of the file, between `---` lines, all keys
required. Do not add an `output:` key: the PDF name is derived from the source
filename plus the revision.

    ---
    sop: SOP-009
    title: Short Procedure Name
    subtitle: STANDARD OPERATING PROCEDURE - one line saying what it does
    revision: Rev. A
    author: Auke-Pieter Colijn
    date: 7 August 2026
    location: Nikhef - XAMS
    status: Initial release
    ---

**Structure**

- `## A. Section name` - a major phase of the procedure, lettered A, B, C, ...
- `### 1. Step name` - a numbered step, numbered continuously across the whole
  document (do not restart at each section).

**Procedure rows** - a blockquote per row, in this order within a step:

    > **ACTION** — what the operator does, imperative mood.

    > **VERIFY** — the observable state proving the action succeeded.

    > **STOP** — the condition under which the operator must not continue.

    > **NOTE** — background information; not itself an instruction.

Rules: every step has at least an ACTION. Use STOP only for genuine
stop conditions. Separate rows with a blank line. Wrap text at roughly 88
characters; the renderer re-flows it.

**Callouts** - GitHub alert blockquotes:

    > [!NOTE]
    > Neutral background information.

    > [!WARNING]
    > A prominent safety warning, e.g. DRAFT - NOT FOR OPERATION.

    > [!TIP]
    > **OPERATOR CUE**
    >
    > | | |
    > | --- | --- |
    > | **Indication** | what the operator sees |
    > | **Immediate response** | what to do at once |

`[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!CAUTION]` and `[!WARNING]` are the only
alert types.

**Tables** - standard markdown, header row and `| --- |` separator required.
Leave the header cells empty for a plain label/value grid.

**Figures** - `![caption](figs/name.png){width=70%}`. Only reference figures
that already exist; do not invent filenames.

**Text formatting** - `**bold**` and `*italic*` only. Superscript is `^-6^` and
subscript is `~ADC~`, so 1 x 10^-6^ mbar renders correctly. Links, code fences,
raw HTML, and headings other than `##` and `###` are not supported.

**Style** - British spelling, imperative mood, no first person. Name valves and
instruments exactly as the site does (V1-V14, PT101, TT203, E030-1). Write
`TBD - ...` wherever a value must be supplied by a detector expert rather than
inventing numbers, and set `status: Draft placeholder` for such documents.

---

## Worked example

A complete, valid document. Follow this shape.

    ---
    sop: SOP-009
    title: Cold Trap Regeneration
    subtitle: STANDARD OPERATING PROCEDURE - regenerate the cold trap after recovery
    revision: Rev. A
    author: Auke-Pieter Colijn
    date: 7 August 2026
    location: Nikhef - XAMS
    status: Initial release
    ---

    > [!NOTE]
    > **Work discipline:** Record every valve operation, pressure and temperature
    > in the electronic LogIt logbook.

    ## A. Preconditions

    ### 1. Confirm the system is isolated

    > **ACTION** — Confirm SOP-006 has completed and the storage bottle is
    > isolated. Close V12 and confirm V7 and V8 are closed.

    > **VERIFY** — PT201 is stable and no active transfer is in progress.

    > **STOP** — Do not start regeneration while xenon is being transferred.

    ### 2. Set the valve configuration

    > **ACTION** — Set the valves as listed below.

    | Valve / item | Required state |
    | --- | --- |
    | V7, V8 | CLOSED |
    | V12 | CLOSED |
    | Trap heater | OFF |

    ## B. Regeneration

    ### 3. Warm the trap

    > **ACTION** — Switch the trap heater ON and raise the setpoint to TBD °C at
    > no more than TBD °C/min.

    > **VERIFY** — TT301 rises smoothly and pressure stays below TBD bar.

    > [!TIP]
    > **OPERATOR CUE**
    >
    > | | |
    > | --- | --- |
    > | **Indication** | Rapid PT201 rise |
    > | **Immediate response** | Switch the heater OFF and wait |

    > **STOP** — If pressure exceeds TBD bar, stop heating and close V12.

    ## C. Completion

    > **ACTION** — Switch the heater OFF and allow the trap to return to ambient
    > temperature.

    > **NOTE** — Record final pressure, final valve state and total heating time
    > in LogIt.

    ## FINAL SAFE-STATE CHECK

    > [!TIP]
    > - Trap heater OFF
    > - V7, V8 and V12 closed
    > - Final pressure and valve state recorded in LogIt
