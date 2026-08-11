# DEVELOPMENT.md - aligning the XAMS manual with IEC/IEEE 82079-1:2020

Implementation plan for restructuring the XAMS operations manual according to the
principles of NEN-EN-IEC/IEEE 82079-1:2020, *Preparation of information for use
(instructions for use) of products*.

## Status

| Phase | Content | State |
| --- | --- | --- |
| 1 | conformity statement | **done** - 11 August 2026 |
| 2 | signal words and safety messages | **done** - 11 August 2026; hazard wording needs operator review |
| 2b | SOP-000 general hazard sheet | **done** - 11 August 2026; same review caveat |
| 3 | document control furniture | not started |
| 4 | frontmatter, template, required sections | not started |
| 5 | content sweep | not started |
| 6 | SOP-103 | not started |
| 7 | reusable starter kit | not started |

## Why, and how far

Nobody requires this. XAMS is a one-off apparatus that is never placed on the
market and never leaves the lab, so 82079-1 - a product-information standard that
assumes unknown users, market placement and liability - does not apply as a legal
obligation. What actually binds is the Arbowet/Arbobesluit duty to instruct
workers, the pressure-equipment rules, and Nikhef's internal RI&E and ODH regime.

The standard is nevertheless the best available checklist, and a one-off
instrument has *no vendor manual, no support line and no second unit to compare
against* - the SOPs are the only copy of the knowledge. So the plan adopts the
clauses that carry real safety value and deliberately scopes out the ones that
only make sense for a marketed product.

**Never write "compliant with IEC/IEEE 82079-1" on a document.** Conformance
requires the Clause 5 process evidence - validation by someone who is not the
author, a documented review workflow - which this plan does not build. Write
*"structured in accordance with the principles of IEC/IEEE 82079-1:2020"*. That
is defensible, and a documented adopted/scoped-out split reads as more competent
than a blanket claim that cannot be evidenced.

### Adopted

| Clause | Adopted as |
| --- | --- |
| 6.4 safety messages | DANGER / WARNING / CAUTION / NOTICE hierarchy, safety-alert triangle, hazard -> consequence -> avoidance wording, placement *before* the guarded step |
| 5.3 target audience | required-competence and PPE statement on page 1 of every SOP |
| 6.2 identification | `doc_id`, revision, issue date, supersedes, prepared/reviewed/approved by |
| 6.2 / 7.2 | running footer `doc_id - Rev - Page x of y`, PDF metadata, PDF outline |
| 6.7 troubleshooting | fault -> cause -> remedy table per SOP |
| 4 verifiability | exact setpoints and tolerances instead of "approximately" |
| 5.6 revision control | revision-history table per document; superseded PDFs kept |

### Scoped out, with reason

| Clause | Not done, because |
| --- | --- |
| translation / language management | single working language (English), fixed known user group |
| tagged PDF, accessibility conformance | no external distribution |
| publisher contact, formal feedback channel | replaced by one line: report errors to the document owner or open a git issue |
| separate audience-analysis and task-analysis deliverables | audience is a handful of known people, already captured by the competence line |
| disposal, spare parts, technical data sheets | not an instruction-for-use concern for a fixed installation |
| per-document Annex A conformity tick sheets | replaced by one project-level statement (Phase 1) |

## Constraints imposed by the existing toolchain

Read these before starting; they shape several design choices.

- `parse_frontmatter` ([tools/sop_doc.py:93](tools/sop_doc.py#L93)) is **flat
  `key: value` only** - no YAML lists or nested maps. Multi-value fields must be
  comma-separated strings, and the revision history must live in a markdown table
  in the body, not in the frontmatter.
- *(resolved in Phase 2)* The alert vocabulary was declared in two places that had
  to stay in step, `ALERT_TO_KIND` in `sop_doc.py` and `ALERT_TYPES` in
  `check_md.py`. `check_md` now derives its list from `sop_doc`; keep it that way.
- *(resolved in Phase 2)* `_box` hardcoded a special case for `warning` and
  `BOX_BG` carried the colours. Both are now driven by `BOX_KINDS` in
  `sop_style.py`, where all styling belongs.
- `build.py --check` strips page numbers with `re.sub(r"Page \d+", ...)`
  ([tools/build.py:27](tools/build.py#L27)). The `of y` suffix added in Phase 3
  breaks that regex - update it in the same commit.
- `tools/pdf_to_md.py` was a one-shot migration tool and is deliberately not
  maintained. Its `ALERT_FOR` map will go stale; leave it, do not extend it.
- Adding keys to `REQUIRED_META` ([tools/check_md.py:20](tools/check_md.py#L20))
  fails all 13 sources at once and `build.py` refuses to run on errors. Every new
  key therefore lands as a **warning** first and is promoted to an error only
  after the sources are migrated.

## Working method

One branch and one commit per phase. After every phase:

    tools/.venv/bin/python tools/check_md.py md
    tools/.venv/bin/python tools/build.py --check --refdir XAMS_Operations_Manual_2026-08-10

The `--check` word diff is the regression net: it should report only the words the
phase was supposed to change. Anything else is a rendering regression.

---

## Phase 1 - the conformity statement (the actual deliverable) - DONE

*Completed 11 August 2026. Delivered as
[docs/DOCUMENTATION_STANDARD.md](docs/DOCUMENTATION_STANDARD.md).*

The safety department will not read SOP-004. They will flip three pages, form a
judgement, and want one thing to file. That thing is a single page.

**Write `docs/DOCUMENTATION_STANDARD.md`** containing:

1. One paragraph: what the manual is, who it is for, what governs it (Arbowet,
   RI&E, ODH assessment, pressure-equipment rules).
2. The statement: *structured in accordance with the principles of IEC/IEEE
   82079-1:2020*, never "compliant with".
3. The **Adopted** table above, with a pointer to where each item lives.
4. The **Scoped out, with reason** table above.
5. How a document is issued: author -> reviewer -> approver, revision bump in
   frontmatter, `check_md.py --fix`, `build.py`, superseded PDFs to `old/`.
6. How to report an error in a procedure.

Deliberately plain markdown, one page. It is not rendered to the house PDF style -
it describes the system, it is not part of the manual.

**Done when:** the page exists, is committed, and can be handed over on its own
without any of the later phases being finished.

### Outcome

The statement describes the manual as it will be *after* Phases 2-5, which is
correct for an issued standard but means the manual does not yet match it. Close
that gap before handing the page to the safety department, or hand it over as
Rev. A with the phases named as planned work.

Section 6 of the statement lists three placeholders that cannot be filled in from
the repository and need local knowledge:

- named reviewer and approver roles for the SOP set;
- reference numbers of the XAMS RI&E and of the ODH assessment;
- which parts of the gas system fall under the pressure-equipment inspection
  regime.

---

## Phase 2 - signal words and safety messages - DONE

*Completed 11 August 2026. See the Outcome section at the end of this phase - the
hazard wording is drafted and needs review by the responsible operator.*

The highest-value phase, both for real safety and for how the manual reads to an
auditor.

### 2.1 Vocabulary

Adopt the ISO 3864-2 / ANSI Z535.6 hierarchy:

| Signal word | Meaning | Triangle |
| --- | --- | --- |
| `DANGER` | imminent hazard; death or serious injury if not avoided | yes |
| `WARNING` | hazard that *could* cause death or serious injury | yes |
| `CAUTION` | minor or moderate injury | yes |
| `NOTICE` | equipment or property damage only, no injury | **no** |

The absent triangle on `NOTICE` is normative, not a style choice - the
safety-alert symbol means *personal injury*.

### 2.2 Markdown syntax

Keep the GitHub alert form and extend the vocabulary:

    > [!DANGER]
    > **Asphyxiation - xenon or nitrogen release in the pit.**
    > Xenon displaces air and causes loss of consciousness without warning.
    > Do not enter the pit while a transfer is running.

Three parts, in order: **hazard and its source** (bold, first line),
**consequence**, **how to avoid**.

Trade-off: `[!DANGER]` and `[!NOTICE]` are not GitHub-native, so GitHub's preview
renders them as a plain blockquote. Accepted - the PDF is the deliverable and
`check_md.py` owns the vocabulary.

### 2.3 Code changes

- `sop_doc.py`: extend `ALERT_RE` and `ALERT_TO_KIND` with `danger` and `notice`
  as their own kinds. Keep `tip`/`important` accepted for now so nothing breaks;
  have `check_md` warn that they are deprecated.
- `sop_style.py`: add a single `BOX_KINDS` table - background, border colour,
  signal word, `triangle: bool`, text colour - replacing `BOX_BG` and the
  hardcoded `warning` branch in `md_to_pdf._box`. New palette entries: an amber
  for `WARNING`/`CAUTION`, a stronger red for `DANGER`, neutral grey-blue for
  `NOTICE`.
- New `tools/sop_symbols.py`: a small ReportLab `Flowable` that draws the ISO 7010
  warning triangle as vector (yellow fill, black border, exclamation mark). No
  image asset, so nothing to lose track of.
- `md_to_pdf._box`: render a signal-word header band inside the box - triangle,
  then the word in bold caps - above the message body.
- `check_md.py`: import the vocabulary from `sop_doc` instead of restating it;
  warn when a `DANGER`/`WARNING`/`CAUTION` box has no bold lead line or is a
  single short sentence (a hazard message missing its consequence or its
  avoidance).

### 2.4 Content pass

Go through all 12 SOPs and reclassify every existing callout:

- Existing `[!WARNING]` / `[!CAUTION]` -> the correct one of the four by
  *consequence severity*, not by how alarming the text sounds.
- `[!TIP]` used for OPERATOR CUE -> keep as a cue box only where nothing safety-
  relevant is being said; otherwise promote to `CAUTION` or `WARNING`.
- `> **STOP**` rows: `STOP` stays a **hold point** (do not proceed until X). Where
  the real content is "you will get hurt", lift it into a `WARNING`/`CAUTION` box
  placed *before* the step. Where it is "you will damage the hardware", `NOTICE`.
- Add a grouped **Hazards** section on page 1 of each SOP covering the ones that
  apply: cryogenic burn, ODH/asphyxiation (Xe and LN2), high voltage, high
  pressure.

**Done when:** every SOP has an explicit hazard section, every callout carries one
of the four signal words, and the word diff shows only intended changes.

### Outcome

Delivered as planned, with two additions that the sources forced.

**Two non-severity callouts were added, not just the four signal words.** All 14
`[!TIP]` uses turned out to be end-of-procedure verification checklists, except two
that were OPERATOR CUE tables - none of them were safety messages. Retyping them
all as `[!NOTE]` would have lost a useful visual distinction, so the vocabulary
gained `[!CHECKLIST]` (renders green, like ACTION) and `[!CUE]` (renders cream,
like VERIFY). `[!TIP]` and `[!IMPORTANT]` still parse but `check_md.py` now warns
that they carry no severity.

**Reclassifications made.** SOP-101's "never apply high voltage" CAUTION became a
WARNING (electric shock can be fatal). SOP-102's light-damage WARNING became a
NOTICE (equipment only) and its wiring CAUTION became a WARNING. SOP-103's
"DRAFT / NOT FOR OPERATION" and the matching note in the index became DANGER. No
existing `STOP` row was converted: on inspection they are all genuine hold points,
which is what `STOP` is for.

**Files changed:** new `tools/sop_symbols.py`; `BOX_KINDS`, the signal palette and
`signal_style` in `sop_style.py`; the alert vocabulary in `sop_doc.py`;
`_signal_band` and a table-driven `_box` in `md_to_pdf.py`; vocabulary import,
deprecation warning and a hazard-structure check in `check_md.py`; the callout
sections of `TEMPLATE.md` and `PROMPT.md`; all 12 SOPs and the index.

`check_md.py md` is clean and `build.py --check` reports only the intended words.

> **The hazard text needs review before issue.** The 30-odd hazard messages were
> drafted from what the procedures themselves describe - ODH from xenon and
> nitrogen, cryogenic burns, stored energy in the bottles, flash evaporation on
> overflow, high voltage, dewar handling. The severities and the avoidance
> measures are plausible but they are not authoritative: they were not taken from
> the XAMS RI&E or the ODH assessment, and nobody who operates the setup has
> checked them. Read every DANGER and WARNING against the real installation before
> this goes anywhere near the safety department.

Deferred to Phase 4: PPE named per hazard belongs in the `## Scope and competence`
section, which does not exist yet. The avoidance lines currently name PPE inline
("wear cryogenic gloves and a face shield"), which is correct but duplicates what
that section will say.

---

## Phase 2b - SOP-000, the general hazard sheet - DONE

*Completed 11 August 2026. Added after Phase 2 showed the front matter growing out
of proportion to the procedures.*

### The problem it solves

Phase 2 put a `## Hazards` section on all 12 SOPs, and the result was twelve
near-verbatim copies of two hazards: asphyxiation from xenon and nitrogen, and
cryogenic burn. On the shorter procedures the hazards filled page 1 and pushed step
1 onto page 2. Duplicated safety text is also how safety text becomes wallpaper
that nobody reads.

82079-1 permits information to be supplied once for a set of documents, provided it
is referenced and available. So the installation-wide hazards move to one sheet and
each SOP keeps only what is specific to it.

### Why SOP-000 and not a separate document type

`md/SOP_000_General_Hazards.md` needs **no tooling change at all**: `_sop_number`
parses `000`, the register check picks it up, `build.py` renders it like any other
document, and it sorts first in `md/` so it leads the built manual. A non-SOP name
such as `XAMS_General_Hazards.md` would have needed a second special case beside
`INDEX_STEM`, for no benefit.

It is not a procedure, so the title and subtitle say so, and the index introduces
it in its own section 0 above the operating sequence rather than inside it.

### What the sheet carries

The four installation-wide hazards in full (asphyxiation, cryogenic burn, stored
energy in the gas system, detector high voltage), PPE by activity, what to do when
an ODH alarm sounds, the emergency contacts, and who may work on XAMS. The contacts
in particular had been reachable only from SOP-007, which was wrong - they are
needed during SOP-004 just as much.

### The pointer line

Each SOP replaces the boilerplate boxes with one `[!NOTE]`:

    > [!NOTE]
    > **General hazards apply:** asphyxiation (xenon and nitrogen), cryogenic burn,
    > stored energy in the gas system. Read SOP-000 before starting.

**Naming the hazards is the point, not the citation.** The one real weakness of
splitting the sheet out is that someone printing SOP-004 alone does not get
SOP-000. Listing the hazards by name in the pointer means that operator still knows
what can kill them, in one line. A bare "see SOP-000" would not.

**Never version-lock the pointer.** Write `SOP-000`, never `SOP-000 Rev. B` -
otherwise every revision of the hazard sheet orphans twelve pointers and
`check_md.py` cannot detect a stale one.

### Which hazards stayed inline

The test applied to each box: *would a competent operator who read SOP-000 last
month still need this warning at this step?*

| SOP | Kept, because it is specific to the procedure |
| --- | --- |
| 002 | hot getter burn - heat, not cryogenic |
| 003 | cold gas jet when the emergency solenoid valve is tested |
| 004 | flash-evaporation overpressure at the overflow transition |
| 005 | loss of cooling during *unattended* running, discovered by the next person through the door |
| 006 | bottle overfilled or warming while isolated |
| 007 | the alarm condition may already have released gas; working alone at night under time pressure |
| 008 | large nitrogen release in a short time with an untrained contractor present; dewar crush and pinch |
| 101 | energising a channel whose interlocks are not satisfied |
| 102 | arcing when a live connector is made or broken |
| 103 | the procedure itself is unapproved |
| 104 | cabling changed on a live calibration setup |

Several were rewritten rather than deleted, to say what is different about *this*
procedure instead of restating the general hazard. SOP-001 kept only its NOTICE.

### Result

`check_md.py md` is clean. SOP-004 went from 6 pages to 5 with step 1 back on
page 1. The review caveat from Phase 2 applies unchanged, and now applies to
SOP-000 most of all: it is the sheet everything else points at.

Two placeholders on SOP-000 need local knowledge: where PPE and personal O~2~
monitors are kept, and whether the ODH re-entry rule as written matches the Nikhef
procedure.

---

## Phase 3 - document control furniture

Small, mechanical, and disproportionately convincing.

- **Footer.** Change `SopDoc.footer` ([tools/sop_doc.py:64](tools/sop_doc.py#L64))
  to `doc_id - revision`. Add `Page x of y` via the standard ReportLab
  `NumberedCanvas` recipe: subclass `canvas.Canvas`, buffer `showPage`, stamp the
  total in `save()`, pass it as `canvasmaker=` to `pdf.build()`. This prevents
  someone working from an incomplete printout at 02:00, which is the actual reason
  the clause exists.
- **Update `build.py:27`** to `re.sub(r"Page \d+ of \d+", ...)` in the same commit.
- **PDF metadata.** `md_to_pdf.render` already sets title/author/subject
  ([tools/md_to_pdf.py:321](tools/md_to_pdf.py#L321)); add `keywords` (SOP number,
  XAMS, revision) and `creator`.
- **PDF outline.** Subclass `BaseDocTemplate` with an `afterFlowable` hook that
  calls `canvas.addOutlineEntry` for every `section` and `step` paragraph, so the
  bookmark pane mirrors the procedure structure.
- **Per-document table of contents** for the long SOPs (004, 006, 007 - all over
  200 source lines). Generated from the `section`/`step` blocks, emitted after the
  metadata table, suppressed for short documents.

**Done when:** every page of every PDF is self-identifying, and the outline pane
shows the full step list.

---

## Phase 4 - frontmatter, template and required sections

### 4.1 Frontmatter

Target set, remembering that the parser is flat:

    doc_id: XAMS-SOP-004
    sop: SOP-004
    title: LXe Filling
    subtitle: Fill the detector with liquid xenon
    revision: Rev. E
    issue_date: 2026-08-10
    supersedes: Rev. D (2026-05-02)
    prepared_by: A.P. Colijn
    reviewed_by: <name>, <date>
    approved_by: <name>, <date>
    audience: Trained XAMS operator; cryogenics and ODH briefed
    ppe: Cryogenic gloves, face shield, personal O2 monitor
    location: Nikhef - XAMS
    status: Updated release

`author` alone is not enough: preparation, review and approval are three roles and
must be separately visible.

Sequence, to keep the build green:

1. Add the new keys to a `RECOMMENDED_META` list in `check_md.py` - warnings only.
2. Migrate all 13 sources.
3. Move the keys into `REQUIRED_META` so they become errors.

### 4.2 Cover block, and where the administrative material goes

The original plan was to keep the six-field grid and add an approval strip under
it. That is the wrong direction: page 1 is the operator's page, and every field
added to it pushes step 1 further away.

**Principle: the front is operational, the back is administrative.** 82079-1 asks
that identification be unambiguous and findable. It never asks for it on page 1,
and after Phase 3 every page already carries `doc_id - Rev - Page x of y` in the
footer.

So:

- Replace the 2x3 `META_LAYOUT` grid
  ([tools/md_to_pdf.py:23](tools/md_to_pdf.py#L23)) with a **single identification
  line** under the subtitle:

      SOP-004 - Rev. E - Issued 10 August 2026 - Trained XAMS operator - Nikhef XAMS

  That is roughly 70 pt recovered, and it repeats nothing the footer does not
  already guarantee on every page.
- Add a `## Document control` block on the **last page**: prepared by, reviewed by,
  approved by, supersedes, status, and the revision history table. This is material
  for whoever audits the document, not for the operator at 02:00.

### 4.3 Required sections

Extend `tools/TEMPLATE.md` and `tools/PROMPT.md`, and have `check_md.py` warn when
an SOP lacks one:

- `## Scope and competence` - what this procedure is for, what it is **not** for,
  the competence required to run it, and any tools or consumables needed before
  starting. **PPE is not repeated here**: SOP-000 carries PPE by activity, so this
  section names only what is unusual for this procedure. Phase 2b already removed
  the general hazards; this removes the second source of duplication.
- The hazard pointer plus `## Hazards specific to this procedure`, as established
  in Phase 2b. A procedure with no specific hazards keeps the pointer and drops the
  section.
- `## Troubleshooting` - a fault -> likely cause -> remedy grid table. There is no
  manufacturer to call; this section is pure bus-factor insurance.
- `## Document control` - the back-page block from 4.2, including the revision
  history.

The avoidance lines written in Phase 2 still name PPE inline ("wear cryogenic
gloves and a face shield"). Leave them: at the point of the hazard that is the
useful place to say it, and SOP-000 is the authority on where the equipment is.

Also add to the template the "why" habit: rationale in `NOTE` boxes. 82079
discourages rationale inside steps, but for a one-off instrument the reasoning
("V13 stays closed on the getter route because ...") is exactly the knowledge that
is otherwise lost.

**Done when:** `check_md.py md` is clean with the new keys required, and every SOP
carries all four sections.

---

## Phase 5 - content sweep

Highest real safety value, near-zero visibility. Do it, but after the phases above.

Per SOP, in numeric order:

1. **Fix the bold mangling.** SOP-004 and others carry import artefacts such as
   `**Confirm the system has been baked ...** **completed.**` - bold runs split at
   the original PDF's line breaks. Add a `check_md.py` warning for adjacent bold
   runs (`\*\*[^*]+\*\*\s+\*\*`) to find them all, then repair by hand.
2. **One step, one action.** SOP-004 step 8 packs a route choice and five valve
   operations into a single numbered step. Split.
3. **Kill the hedging.** Every "approximately", "or lower if", "one day or more"
   becomes a number with a tolerance: `2.0 +/- 0.2 bar`, `>= 24 h`,
   `T(A) = -90 degC`. Nobody can look these up anywhere else, so a vague value is
   a permanently lost value.
4. **Figure numbering and cross-references.** `![caption](fig.png)` currently
   yields a caption only. Add `Figure <step>-<n>` numbering, and reference the
   figure from the step text. While there, rename the stale figure files
   (`Emergency_Xenon_Recuperation_SOP_007_Rev_B_fig1.png` ->
   `SOP_007_fig01.png`) to match the current naming scheme.
5. **Fill the troubleshooting tables** added in Phase 4.

---

## Phase 6 - SOP-103

SOP-103 (TPC Voltages On/Off) is a placeholder carrying a DRAFT warning, listed in
a released manual. A safety officer who finds a draft high-voltage procedure in an
otherwise controlled manual will discount everything in Phases 1-5.

Either finish it with the detector experts, or remove it from `md/` and from the
register in `XAMS_Operations_Manual_Index.md`. Both are acceptable; leaving it is
not.

---

## Phase 7 - make it reusable (optional, high leverage)

Nobody else at Nikhef does this, which is most of the point. The toolchain is
already generic - the only XAMS-specific parts are the content and the green in
`sop_style.py`.

- Move the XAMS palette and the Nikhef/XAMS strings into a small
  `tools/house_style.py` that a different group can swap.
- Ship `tools/TEMPLATE.md`, `tools/PROMPT.md`, `check_md.py`, `build.py` and
  `docs/DOCUMENTATION_STANDARD.md` as a "controlled-SOP starter kit".
- One README section on adopting it for another setup.

"Here is a documented SOP system any group can adopt" is a far larger win than
"my manual is tidy", and costs almost nothing on top of Phases 1-4.

---

## Order and effort

| Phase | Content | Rough effort | Value |
| --- | --- | --- | --- |
| 1 | `docs/DOCUMENTATION_STANDARD.md` | 1 h | the hand-over artefact |
| 2 | signal words, triangle, hazard sections | 1 day | safety + most visible |
| 3 | footer, page x of y, metadata, outline, ToC | half day | cheap credibility |
| 4 | frontmatter, cover, required sections | half day tooling + half day migration | governance |
| 5 | content sweep | 1-2 days | highest real safety value |
| 6 | SOP-103 | depends on the experts | protects everything above |
| 7 | reusable starter kit | half day | reputation multiplier |

Phases 2-4 are mostly tooling, so every document upgrades at once. Phase 5 is the
only one that scales with the number of SOPs.
