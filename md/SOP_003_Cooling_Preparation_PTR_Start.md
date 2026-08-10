---
sop: SOP-003
title: Cooling Preparation And Ptr Start
subtitle: STANDARD OPERATING PROCEDURE - prepare cooling after GXe purification
revision: Rev. D
author: Auke-Pieter Colijn
date: 7 August 2026
location: Nikhef - XAMS
status: Updated release
---

> [!NOTE]
> **Prerequisite:** SOP-002 must be complete: at least seven effective days of GXe
> circulation through the hot getter must be documented in LogIt. Detector pressure must
> be stable and the final valve state recorded.

## A. Prepare emergency cooling

### 1. Check emergency cooling readiness

> **ACTION** — **Ensure N2 gas is present in the emergency-cooling pipe and close the
> solenoid** **valve. Confirm sufficient liquid nitrogen is available.**

> **VERIFY** — Emergency cooling consumes approximately 5-7 kg/hour. Record the
> available amount in LogIt.

## B. Pump the insulation vacuum

### 2. Start roughing and turbopump

> **ACTION** — **Connect the roughing pump to V16. Open V15, then V16. Start the
> roughing pump** **and wait until insulation vacuum is below 9 x 10^-2^ mbar. Then
> start the turbopump.**

> **VERIFY** — The turbopump should spin up and reduce to about 7 W once conditions are
> suitable.

> **STOP** — **If the turbopump does not reduce its power, pressure may still be too
> high or there** **may be a leak. Continue roughing or investigate.**

> **VERIFY** — Continue pumping until the insulation vacuum is in the 10^-6^ mbar
> regime. Record the achieved value in LogIt.

## C. Start the PTR

### 3. Check compressor readiness

> **ACTION** — **Check whether compressor helium requires a refill. Switch ON the
> compressor and** **verify supply pressure is within the approved operating range.**

> **VERIFY** — Point compressor heat exhaust away from the emergency LN2 dewar.

> **STOP** — **If compressor pressure or operation is abnormal, switch it OFF and
> contact an** **experienced operator.**

### 4. Set the LakeShore controller

> **ACTION** — **Set temperature setpoint to -90.00 °C. Set Heater Range to HIGH.**

> **VERIFY** — Displayed setpoint is -90.00 °C and Heater Range is HIGH.

## FINAL SAFE-STATE CHECK

> [!TIP]
> - SOP-002 purification completed and documented
> - Emergency cooling readiness confirmed
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
