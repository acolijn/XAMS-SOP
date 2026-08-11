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
    subtitle: One line saying what the procedure is for
    revision: Rev. A
    author: Auke-Pieter Colijn
    date: 7 August 2026
    location: Nikhef - XAMS
    status: Initial release
    ---

The `subtitle:` is one short sentence saying what the procedure is for. Do not
prefix it with "STANDARD OPERATING PROCEDURE" - that is obvious from the
document. It is printed under the title and reused as the Purpose column of the
manual index, so write it as a standalone phrase starting with a capital.

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

**Safety messages** - the four signal words of ISO 3864-2 / ANSI Z535.6, chosen by
the *severity of the consequence*, not by how alarming the wording sounds:

| Alert | Use when the hazard, if not avoided | Triangle |
| --- | --- | --- |
| `[!DANGER]` | is imminent and causes death or serious injury | yes |
| `[!WARNING]` | could cause death or serious injury | yes |
| `[!CAUTION]` | could cause minor or moderate injury | yes |
| `[!NOTICE]` | damages equipment only, nobody is hurt | no |

Every safety message has three parts, in this order: the **hazard and its source**
in bold on the first line, then the **consequence**, then **how to avoid it**.
Place it *before* the step it guards, never after.

    > [!DANGER]
    > **Asphyxiation - xenon released into the laboratory.**
    > Xenon displaces air at floor level and causes loss of consciousness
    > without any warning sensation.
    > Confirm the ODH monitoring is active before opening any bottle valve.

Each SOP also opens with a `## Hazards` section grouping the hazards that apply to
the whole procedure.

**Other callouts** - these carry no severity and must never be used for safety
information:

    > [!NOTE]
    > Neutral background information, or the reason behind a step.

    > [!CUE]
    > **OPERATOR CUE**
    >
    > | | |
    > | --- | --- |
    > | **Indication** | what the operator sees |
    > | **Immediate response** | what to do at once |

    > [!CHECKLIST]
    > - what must be true, or recorded, before the procedure is closed

`[!TIP]` and `[!IMPORTANT]` are deprecated: they still render, but they say
nothing about severity. Use a signal word, `[!NOTE]`, `[!CUE]` or `[!CHECKLIST]`
instead.

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
    subtitle: Regenerate the cold trap after a recovery
    revision: Rev. A
    author: Auke-Pieter Colijn
    date: 7 August 2026
    location: Nikhef - XAMS
    status: Initial release
    ---

    > [!NOTE]
    > **Work discipline:** Record every valve operation, pressure and temperature
    > in the electronic LogIt logbook.

    ## Hazards

    > [!WARNING]
    > **Burn hazard - the cold trap and its heater during regeneration.**
    > Contact with the trap body causes immediate burns.
    > Allow the trap to return to ambient temperature before touching it.

    > [!NOTICE]
    > Heating an isolated trap too quickly overpressurises it.
    > Raise the setpoint at no more than the stated rate and watch PT201.

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

    > [!CUE]
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

    > [!CHECKLIST]
    > - Trap heater OFF
    > - V7, V8 and V12 closed
    > - Final pressure and valve state recorded in LogIt
