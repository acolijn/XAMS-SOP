---
sop: SOP-002
title: Gxe Circulation Through Hot Getter
subtitle: STANDARD OPERATING PROCEDURE - purify xenon before cooling
revision: Rev. C
author: Auke-Pieter Colijn
date: 7 August 2026
location: Nikhef - XAMS
status: Updated release
---

> [!NOTE]
> **Prerequisite:** SOP-001 must be complete. The detector must contain GXe, the pump
> buffer volume must be at 1.0 bar, and the final valve state must be recorded in LogIt.

## A. Prepare the purification loop

### 1. Confirm system readiness

> **ACTION** — **Confirm Slow Control and alarms are running. Confirm detector pressure
> is stable** **and the recirculation-pump buffer volume is at 1.0 bar.**

> **VERIFY** — Detector pressure, buffer pressure, temperatures and flow channels are
> visible and stable.

> **STOP** — **Do not start circulation if pressures, alarms or monitoring are
> unavailable.**

### 2. Start pump-head cooling

> **ACTION** — **Switch ON the water chiller that cools the recirculation-pump head.
> Allow cooling to** **establish normal operation.**

> **VERIFY** — Water chiller is running and pump-head cooling is active.

> **STOP** — **Do not start the recirculation pump unless pump-head cooling is
> running.**

## B. Establish GXe circulation through the hot getter

### 3. Configure the circulation loop

> **ACTION** — **Set V8 fully OPEN and keep V7 fully CLOSED before pump start. Configure
> the** **approved detector-to-pump-to-getter-to-detector circulation path, including
> the** **pump buffer volume. Keep filling and recovery paths isolated.**

> **VERIFY** — The complete circulation loop is configured and storage bottles remain
> isolated.

> **STOP** — **Use the approved current valve map at the gas board. Do not infer the
> route from** **obsolete pump procedures.**

### 4. Start the recirculation pump

> **ACTION** — **With pump-head cooling active, start the recirculation pump.**

> **VERIFY** — Pump runs smoothly, chiller remains operational, and detector/buffer
> pressures remain stable.

> **STOP** — **Stop the pump immediately if pump-head cooling stops or pump**
> **behaviour/pressure becomes abnormal.**

### 5. Start the getter and establish flow

> **ACTION** — **Switch ON the getter and allow it to reach normal hot operating status.
> Then slowly** **open V7; V7 may be opened fully if stable. Regulate the circulation
> flow by** **gradually closing bypass valve V8 until approximately 17 g/min is
> reached.**

> **VERIFY** — Getter indicates normal hot operating status. Flow is stable near 17
> g/min and detector pressure/temperatures remain stable.

> **STOP** — **If the getter alarms, flow becomes unstable, or detector pressure
> changes** **unexpectedly, reduce flow and stop the pump if necessary.**

## C. Purify for at least one week

### 6. Maintain continuous hot-getter purification

> **ACTION** — **Circulate GXe continuously through the hot getter for a minimum of 7
> effective** **days. Keep alarms and remote monitoring active.**

> **VERIFY** — Daily, confirm flow, detector pressure, buffer pressure, getter status,
> water-chiller status, pump status and relevant temperatures. Record checks and
> interventions in LogIt.

> **STOP** — **Calendar time alone is not sufficient if circulation is interrupted
> significantly.** **Extend purification to achieve at least seven effective days.**

### 7. Complete purification and hand over

> **ACTION** — **Record purification start/end times, interruptions, typical flow and
> final system** **state.**

> **VERIFY** — LogIt demonstrates at least seven effective days of GXe circulation
> through the hot getter.

> **STOP** — **Do not proceed to SOP-003 until the purification requirement is complete
> and** **documented.**

## FINAL SAFE-STATE CHECK

> [!TIP]
> - SOP-001 completed
> - Pump buffer volume at 1.0 bar
> - Water chiller operating and pump-head cooling active
> - Getter hot and without alarms
> - At least seven effective days of GXe circulation completed
> - Flow, pressure, temperatures and interruptions recorded in LogIt

> [!TIP]
> - System released for SOP-003: Cooling Preparation and PTR Start

> [!NOTE]
> **NEXT PROCEDURE:** Continue with SOP-003 - Cooling Preparation and PTR Start.
