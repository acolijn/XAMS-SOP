# Documentation standard for the XAMS operations manual

**Document owner:** A.P. Colijn (a.p.colijn@nikhef.nl)
**Applies to:** all Standard Operating Procedures of the XAMS xenon TPC, Nikhef
**Issue:** Rev. A, 11 August 2026

## 1. What this manual is

The XAMS operations manual is the set of Standard Operating Procedures for
operating the XAMS xenon time projection chamber at Nikhef. It covers gas and
liquid xenon handling, cooling, recovery, emergency recuperation, cryogen supply
and detector operations.

XAMS is a one-off research instrument. It was built in-house, it is not placed on
the market, and it stays in this laboratory. It therefore has no vendor manual, no
support line and no second unit to compare against: these SOPs are the only
written copy of how the apparatus is operated safely.

The manual is written for **trained XAMS operators** - people who have been
briefed on cryogenics and oxygen-deficiency hazards and who are authorised for the
specific activity. It is not written for visitors, and it is not a training course.
Each SOP states its own required competence.

## 2. What governs the manual

The obligations that actually apply to a fixed, non-marketed laboratory
installation are:

- **Arbowet / Arbobesluit** - the employer's duty to instruct workers in the
  hazards of their work and in the measures that control them.
- **Nikhef's internal safety regime** - the risk inventory and evaluation (RI&E)
  for the XAMS setup, and the oxygen-deficiency (ODH) assessment for the xenon and
  liquid-nitrogen inventory.
- **Pressure-equipment rules** (Warenwetbesluit drukapparatuur) for the gas system
  and storage bottles, together with their inspection regime.

None of these prescribe a documentation format. This standard supplies one.

## 3. The documentation standard applied

The manual is **structured in accordance with the principles of
NEN-EN-IEC/IEEE 82079-1:2020**, *Preparation of information for use (instructions
for use) of products*.

This is a deliberate, voluntary choice, and it is a partial one. 82079-1 is a
product-information standard: it assumes a product placed on a market, unknown
users, a manufacturer-customer relationship and translation obligations. Much of
it does not describe our situation. Rather than claim a conformance we cannot
evidence, we state plainly which clauses were adopted and which were set aside,
and why.

> The manual does **not** claim conformity with IEC/IEEE 82079-1:2020. Conformity
> would require the Clause 5 process evidence - in particular validation by
> someone other than the author, and a formally documented review workflow - which
> is not maintained for this manual.

### 3.1 Adopted

| Clause | What we adopted | Where it lives |
| --- | --- | --- |
| 6.4 safety messages | The DANGER / WARNING / CAUTION / NOTICE signal-word hierarchy of ISO 3864-2 / ANSI Z535.6, with the safety-alert triangle on the three injury classes and no triangle on NOTICE. Each message states hazard and source, consequence, and how to avoid it, and is placed before the step it guards. | callout boxes in every SOP; vocabulary enforced by `tools/check_md.py` |
| 6.4 grouped safety information | The hazards common to the whole installation - oxygen deficiency from xenon and nitrogen, cryogenic burn, stored energy in the gas system, detector high voltage - are stated once on a general hazard sheet, together with PPE, the ODH alarm response and the emergency contacts. Each procedure names those hazards in a one-line pointer and adds only the hazards specific to itself. 82079-1 permits information supplied once for a set of documents where it is referenced and available. | `SOP-000 General Hazards`; `## Hazards specific to this procedure` in each SOP |
| 5.3 target audience and competence | Each SOP states who may run it and what competence is required. PPE is not repeated per procedure: the general hazard sheet states it per activity. | `## Scope and competence`; `audience:` in the frontmatter |
| 6.3 intended use and limits | Each SOP states what it is for and, explicitly, what it is not for. | `## Scope and competence` |
| 6.2 identification | Document identifier, revision, issue date, superseded revision, and the three separate roles of preparer, reviewer and approver. One identification line on page 1; the administrative fields on the back page, generated from the frontmatter so they cannot drift. | frontmatter; `## Document control` |
| 7.2 findability and legibility | Running footer carrying document identifier, revision and `Page x of y`; PDF metadata; a PDF outline mirroring the sections and steps. | `tools/md_to_pdf.py` |
| 6.7 fault clearance | A fault - likely cause - remedy table in each SOP. There is no manufacturer to call. | `## Troubleshooting` |
| 4 verifiability | Setpoints are given as numbers with tolerances, not as approximations, so that a criterion can be checked rather than judged. | throughout |
| 5.6 revision control | A revision history in each document; superseded PDFs retained in `old/`; full change history in git. | `## Document control` |

### 3.2 Deliberately not adopted

| Clause | Not applied, because |
| --- | --- |
| translation and language management | The manual has a single working language, English, and a small fixed group of known users. No translated version exists or is planned. |
| tagged PDF and accessibility conformance | The manual is not distributed outside the group; accessibility needs are handled directly with the individuals concerned. |
| publisher details, customer contact, formal feedback channel | Replaced by a single line: report an error to the document owner, or raise it in the repository. See section 5. |
| separate audience-analysis and task-analysis deliverables | The audience is a handful of known people and is already captured by the per-SOP competence statement; a separate analysis document would add no information. |
| disposal, spare parts, technical data sheets | Not instruction-for-use concerns for a fixed installation that is maintained in-house. |
| per-document Annex A conformity checklists | Replaced by this single project-level statement. |

## 4. How a procedure is issued

The markdown sources in `md/` are the source of truth. PDFs are generated and are
never edited by hand.

1. **Prepare.** Edit or create `md/SOP_<nnn>_<Short_Name>.md`. The filename carries
   no revision; the revision lives in the frontmatter.
2. **Review.** A second person, not the preparer, reads the procedure against the
   apparatus. Record them in `reviewed_by:` with the date.
3. **Approve.** The responsible person releases the revision. Record them in
   `approved_by:` with the date. A procedure without an approver is a draft and
   must say so in `status:`.
4. **Bump.** Raise `revision:`, set `issue_date:`, and record the previous revision
   in `supersedes:`. Add a line to the revision-history table in `## Document control`.
5. **Validate and build.**

       tools/.venv/bin/python tools/check_md.py md --fix
       tools/.venv/bin/python tools/build.py

   `check_md.py --fix` brings the register in the master index back in step with
   the sources. `build.py` refuses to run if validation reports an error.
6. **Retain.** Move the superseded PDF to `old/`. The markdown history is in git.

Printed copies are uncontrolled. The footer on every page carries the document
identifier, the revision and `Page x of y` so that a printout can be checked
against the current revision and against itself.

### 4.1 Printed and laminated copies

The manual is printed double-sided and laminated for use at the apparatus. Every
document is rendered to an even page count for that reason; where the content ends
on an odd page the last page carries the line *"This page is intentionally
blank"*, so a blank back is not mistaken for a printing fault.

The build also writes `XAMS_Operations_Manual_Complete.pdf`, the whole manual in
one file in reading order - index, general hazards, SOP-001 to SOP-008, the
detector procedures, then the P&ID. Because every document is even, each one still
begins on a right-hand page in the combined file. Print from that file; printing
the individual PDFs one job at a time is what puts a procedure out of order.

A laminated copy outlives the revision it was made from, and it looks
authoritative long after it has been superseded. Therefore:

- Keep a note of who holds laminated sets and where they are kept.
- When a revision is issued, **physically destroy** the superseded laminated
  copies. Replacing them "when convenient" is how a superseded procedure stays in
  service.
- Check the revision in the footer before working from any laminated copy.
- SOP-000 is printed single-sided, because it is posted in the laboratory and both
  sides would not be visible.

## 5. Reporting an error in a procedure

If a procedure is wrong, unclear, or no longer matches the apparatus, tell the
document owner directly, or open an issue in the repository. Do not annotate a
printout and leave it: the correction has to reach the source.

If the discrepancy is safety-relevant, stop the activity first and contact an
experienced operator before continuing.

## 6. Open points

The following are placeholders in the current issue and need to be filled in
locally:

- Named reviewer and approver roles for the SOP set.
- Reference numbers of the XAMS RI&E and of the ODH assessment.
- Confirmation of which parts of the gas system fall under the pressure-equipment
  inspection regime.
