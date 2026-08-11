---
sop: SOP-005
doc_id: XAMS-SOP-005
title: Normal LXe Operation
subtitle: Normal operation after LXe filling
revision: Rev. A
issue_date: 2026-08-07
supersedes: N/A
author: Auke-Pieter Colijn
prepared_by: Auke-Pieter Colijn
reviewed_by: Bart Sarlemijn
approved_by: Auke-PIeter Colijn
audience: Trained XAMS operator
location: Nikhef - XAMS
status: Initial release
---

> [!NOTE]
> **Prerequisite:** SOP-004 must be complete. The detector must be filled with LXe,
> detector pressure and temperature must be stable, and the approved measurement plan
> must be available.

## Scope and competence

|  |  |
| --- | --- |
| **Purpose** | Keep the detector in steady liquid operation: temperature control, circulation and monitoring. |
| **Not for** | Filling, recovery, or any change of detector configuration. |
| **Competence** | Trained XAMS operator, briefed on cryogenics and oxygen-deficiency hazards. |
| **Before you start** | SOP-004 complete; pressure and temperature stable; an approved measurement plan available. |

> [!NOTE]
> **General hazards apply:** asphyxiation (xenon and nitrogen), cryogenic burn.
> Read SOP-000 before starting.

## Hazards specific to this procedure

> [!WARNING]
> **Loss of cooling during unattended operation boils the liquid xenon inventory
> into the laboratory.**
> A cooling failure can release the whole inventory over hours while nobody is
> present, producing an oxygen-deficient room that gives no warning to the next
> person through the door.
> Keep the alarm chain and the remote connection active whenever the detector is
> left running, and confirm shifter coverage before leaving.

> [!NOTICE]
> Losing the water chiller or the pump-head cooling while the recirculation pump
> runs destroys the pump.
> Confirm the chiller is running whenever the pump is on, and stop the pump first if
> cooling is lost.

## A. Establish normal LXe operation

### 1. Set temperature control

> **ACTION** — **Set the LakeShore setpoint to -90 °C and ensure the heater is ON.**

> **VERIFY** — LakeShore displays -90 °C and heater control is active.

### 2. Configure the normal circulation valve state

> **ACTION** — **Close all gas-system valves first. Then establish the normal
> circulation path in this** **order: open V9, V12, V11, V26, V10, V8, and finally V7.
> All other valves remain** **CLOSED.**

> **VERIFY** — Open valves: V9, V12, V11, V26, V10, V8, V7. All other valves are CLOSED.

> **STOP** — **Do not start the pump if the valve state is uncertain. Reconstruct and
> record the** **complete configuration in LogIt.**

| Valve state | Required state |
| --- | --- |
| V9 | OPEN |
| V12 | OPEN |
| V11 | OPEN |
| V26 | OPEN |
| V10 | OPEN |
| V8 | OPEN |
| V7 | OPEN |
| All other valves | CLOSED |

### 3. Start pump-head cooling

> **ACTION** — **Switch ON the water chiller for the recirculation-pump head.**

> **VERIFY** — Water chiller is running and pump-head cooling is active.

> **STOP** — **Do not start the recirculation pump without pump-head cooling.**

### 4. Start the recirculation pump

> **ACTION** — **Start the recirculation pump.**

> **VERIFY** — Pump runs smoothly and detector pressure remains stable.

> **STOP** — **Stop the pump if cooling fails or detector pressure changes
> unexpectedly.**

### 5. Set normal circulation flow

> **ACTION** — **Regulate the circulation flow by gradually throttling bypass valve V8
> until the flow** **is approximately 15 g/min.**

> **VERIFY** — Flow is stable near 15 g/min; detector pressure and temperatures remain
> stable.

> **STOP** — **Do not force V8 or make large rapid adjustments. If pressure or flow
> becomes** **unstable, reopen V8 and reduce the restriction.**

## NORMAL OPERATING STATE

> [!CHECKLIST]
> - LakeShore setpoint -90 °C
> - Heater ON
> - Normal circulation valve configuration recorded
> - Water chiller ON
> - Recirculation pump ON
> - Flow stable near 15 g/min
> - Slow Control and alarms active
> - Approved measurement plan available
> - Any deviations documented in LogIt

## Document control

| Revision | Issued | Change |
| --- | --- | --- |
| Rev. A | 2026-08-07 | First issue. |
