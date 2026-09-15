---
sop: SOP-003
doc_id: XAMS-SOP-003
title: Cooling Preparation and PTR Start
subtitle: Prepare cooling after GXe purification
revision: Rev. E
issue_date: 2026-09-15
supersedes: Rev. D
author: Auke-Pieter Colijn
prepared_by: Auke-Pieter Colijn
reviewed_by: Bart Sarlemijn
approved_by: Auke-Pieter Colijn
audience: Trained XAMS operator
location: Nikhef - XAMS
status: Updated release
---

> [!NOTE]
> **Prerequisite:** SOP-002 must be complete: at least seven effective days of GXe
> circulation through the hot getter must be documented in LogIt. Detector pressure must
> be stable and the final valve state recorded.

## Scope and competence

|  |  |
| --- | --- |
| **Purpose** | Bring emergency cooling, insulation vacuum and the pulse-tube refrigerator to the state required before liquid filling. |
| **Not for** | Liquid filling itself, which is SOP-004. |
| **Competence** | Trained XAMS operator, briefed on cryogenics and oxygen-deficiency hazards. |
| **Before you start** | SOP-002 complete and documented; emergency LN2 dewar available; turbopump and compressor serviceable. |

> [!NOTE]
> **General hazards apply:** asphyxiation (xenon and nitrogen), cryogenic burn.
> Read SOP-000 before starting.

## Hazards specific to this procedure

> [!CAUTION]
> **Cold gas jet - the emergency-cooling solenoid valve vents to the roof outlet
> when tested.**
> Cold nitrogen escaping at the valve or at a loose fitting can injure the eyes.
> Confirm the roof exhaust is clear and stand clear of the valve before energising
> it.

> [!NOTICE]
> Starting the pulse-tube refrigerator with a poor insulation vacuum, or exhausting
> compressor heat towards the emergency LN2 dewar, wastes cryogen and can damage the
> cold head.
> Confirm the insulation vacuum and the direction of the heat exhaust before
> starting the compressor.

## A. Pump the insulation vacuum

### 1. Start roughing and turbopump

> **ACTION** — **Connect the roughing pump to V16. Open V15, then V16. Start the
> roughing pump** **and wait until insulation vacuum is below 9 x 10^-2^ mbar. Then
> start the turbopump.**

> **VERIFY** — The turbopump should spin up and reduce to about 7 W once conditions are
> suitable.

> **STOP** — **If the turbopump does not reduce its power, pressure may still be too
> high or there** **may be a leak. Continue roughing or investigate.**

> **VERIFY** — Continue pumping until the insulation vacuum is in the 10^-6^ mbar
> regime. Record the achieved value in LogIt.

## B. Start the PTR

### 2. Check compressor readiness

> **ACTION** — **Check whether helium pressure in compressor is (2.0 +- 0.05)MPa: if too low refill before continuing. Switch ON the
> compressor and verify supply pressure is within the approved operating range.**

> **VERIFY** — Point compressor heat exhaust away from the emergency LN2 dewar.

> **STOP** — **If compressor pressure or operation is abnormal, switch it OFF and
> contact an experienced operator.**

### 3. Set the LakeShore controller

> **ACTION** — **Set temperature setpoint to -90.00 °C. Set Heater Range to HIGH. On the Lakeshore unit click SETPOINT. Then navigate to HIGH with the arrow buttons and click Enter when the appropriate setting is selected **

> **VERIFY** — Displayed setpoint is -90.00 °C and Heater Range is HIGH.

## FINAL SAFE-STATE CHECK

> [!CHECKLIST]
> - SOP-002 purification completed and documented
> - Insulation vacuum in the 10\^-6 mbar regime
> - Turbopump running normally
> - Compressor supply pressure within approved range
> - Heat exhaust directed away from emergency LN2 dewar
> - LakeShore setpoint -90.00 °C
> - Heater Range HIGH
> - All relevant values and deviations recorded in LogIt
> - System ready for SOP-004: LXe Filling Procedure

> [!NOTE]
> **NEXT PROCEDURE:** Continue with SOP-004 - LXe Filling Procedure.

## Document control

| Revision | Issued | Change |
| --- | --- | --- |
| Rev. D | 2026-08-07 | Content updated; see the source history for details. |
| Rev. E | 2026-09-15 | Content updated; no longer check LN2 cooling here + minor changes |

Superseded revisions are retained as PDFs in the old/ directory and in the version history of the markdown source.
