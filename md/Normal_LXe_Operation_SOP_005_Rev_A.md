---
sop: SOP-005
title: Normal Lxe Operation
subtitle: STANDARD OPERATING PROCEDURE - normal operation after LXe filling
revision: Rev. A
author: Auke-Pieter Colijn
date: 7 August 2026
location: Nikhef - XAMS
status: Initial release
output: Normal_LXe_Operation_SOP_005_Rev_A.pdf
---

> [!NOTE]
> **Prerequisite:** SOP-004 must be complete. The detector must be filled with LXe,
> detector pressure and temperature must be stable, and the approved measurement plan
> must be available.

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

> [!TIP]
> - LakeShore setpoint -90 °C
> - Heater ON
> - Normal circulation valve configuration recorded
> - Water chiller ON
> - Recirculation pump ON
> - Flow stable near 15 g/min
> - Slow Control and alarms active
> - Approved measurement plan available
> - Any deviations documented in LogIt
