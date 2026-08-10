---
sop: SOP-001
title: GXe Filling Procedure
subtitle: STANDARD OPERATING PROCEDURE - initial gas fill before purification
revision: Rev. B
author: Auke-Pieter Colijn
date: 5 August 2026
location: Nikhef - XAMS
status: Updated release
output: GXe_Filling_Procedure_SOP_001_Rev_B.pdf
---

> [!NOTE]
> **Work discipline:** Every valve operation, configuration change, pressure, mass and
> flow value must be recorded in the electronic LogIt logbook.

## A. Preconditions and preparation

### 1. Pump out detector and gas lines

> **ACTION** — **Fully pump out the detector volume and all connected pipes, including
> the pipe** **between pressure regulator V17 and high-pressure valves V5/V6.**

> **VERIFY** — Perform an RGA scan before filling. Required pressure: **< 1 x 10**^-6^
> **mbar**. Record the detector pressure and RGA result in LogIt.

> **STOP** — **Do not start filling if the required vacuum or RGA condition is not
> met.**

### 2. Start Slow Control and flow integration

> **ACTION** — **Ensure Slow Control is running. Press Reset Integrated Flow and
> confirm** **integration is active. Start Slow Control monitoring in LogIt using the
> documented** **script.**

> **VERIFY** — The live pressure channels and integrated flow must be visible before
> proceeding.

### 3. Prepare storage bottle and recirculation-pump buffer volume

> **ACTION** — **Record the selected bottle and its initial mass in LogIt using mA = ...
> kg or mB = ...** **kg. Confirm the recirculation pump is OFF. Ensure the
> recirculation-pump buffer** **volume is filled with xenon to 1.0 bar.**

> **VERIFY** — The buffer volume may be filled once and then left isolated at 1.0 bar
> for later use. Confirm all system valves are initially closed. Do not fully tighten
> V8. Remove the V14 knob so it cannot be opened accidentally.

> **STOP** — **V8 is a needle valve and can be damaged by overtightening.**

| Valve state | Required state |
| --- | --- |
| V1-V14 | CLOSED |
| V14 knob | REMOVED |
| V17 regulator | FULLY CLOSED - turn counter-clockwise, towards you |
| V18/V19 bottle valve | CLOSED |
| Recirculation pump | OFF |
| Pump buffer volume | 1.0 bar GXe; isolated |

## B. Pressurise and set the regulator

### 4. Pressurise the initial gas line

> **ACTION** — **Open the selected storage-bottle main valve: V18 for bottle A or V19
> for bottle B.** **Then open V5 for A or V6 for B.**

> **VERIFY** — Monitor P-high (PT101), P-low (PT102), and detector pressure in Slow
> Control. P-high should rise to about **62 bar**. With V17 closed, P-low may reach
> about **1.9 bar**.

> **STOP** — **If pressures behave unexpectedly, close the bottle valve and the selected
> V5/V6** **and investigate.**

### 5. Tune pressure regulator V17

> **ACTION** — **Open V17 slowly in 1/4-turn increments until P-low reaches 2.3 bar.
> Allow the** **pressure to stabilise after each adjustment.**

> **VERIFY** — P-low = 2.3 bar. Keep watching Slow Control continuously.

> **STOP** — **Do not overshoot 2.3 bar. If you do, close V17 by approximately the
> amount of the** **overshoot and allow the regulator to stabilise.**

## C. Open the path and fill the detector

### 6. Open the pipe path up to V7

> **ACTION** — **Open V8, then V13, then V9. Leave V7 closed.**

> **VERIFY** — No detector-pressure change should be visible yet.

> **STOP** — **If detector pressure changes before V7 is opened, stop and verify the
> valve** **configuration.**

| Valve state | Required state |
| --- | --- |
| V8 | OPEN |
| V13 | OPEN |
| V9 | OPEN |
| V7 | CLOSED |

### 7. Start controlled GXe filling

> **ACTION** — **Open V7 very gradually. Adjust for approximately 1-2 slpm,
> corresponding to** **about 5.9-11.7 g/min for xenon.**

> **VERIFY** — Monitor detector pressure continuously. Stop the active fill by closing
> V7 when detector pressure reaches **1.3 bar**.

> **STOP** — **V7 is highly sensitive. Do not leave it unattended. Closing at 1.3 bar is
> intentional:** **gas remaining upstream will later add roughly 1 bar.**

### 8. Empty the high-pressure line into the detector

> **ACTION** — **Close the storage-bottle main valve. Reopen V7 and allow the trapped
> gas to enter** **the detector.**

> **VERIFY** — Wait until P-high matches P-low. The detector pressure should increase by
> about 1 bar.

> **STOP** — **Keep monitoring detector pressure. If it approaches an unsafe value or
> rises** **unexpectedly, close V7 and stop.**

### 9. Equalise remaining pressure

> **ACTION** — **Fully open V17 to release the remaining gas from the regulator section
> into the** **connected system.**

> **VERIFY** — Confirm P-high, P-low, and detector pressure are approximately equal.

> **STOP** — **Do not proceed to closure until the three pressures are consistent.**

### 10. Isolate the system

> **ACTION** — **Close V17. Close V5 if bottle A was used or V6 if bottle B was used.
> Close all** **remaining valves unless SOP-002 explicitly requires another state.**

> **VERIFY** — Record the final valve configuration and the buffer-volume pressure in
> LogIt.

## D. LogIt completion and cross-check

> [!TIP]
> - Bottle ID (A or B) and initial mass
> - Detector pressure after pump-out
> - RGA result and pressure
> - Times and states for every valve operation/configuration change
> - Initial and final bottle mass
> - Integrated flow value - Slow Control does not log this automatically
> - Comparison of GXe mass from bottle weight loss with integrated flow
> - Final pressures and final valve configuration
> - Recirculation-pump buffer volume pressure (target 1.0 bar)
> - Any deviation, unexpected response, or intervention

> **STOP** — **If the bottle-mass loss and integrated flow disagree significantly, do
> not continue** **until the discrepancy has been understood and documented.**

## FINAL SAFE-STATE CHECK

> [!TIP]
> - GXe filling completed and pressure equalised
> - Storage bottle isolated
> - V17 closed
> - Pump buffer volume at 1.0 bar and isolated
> - Final valve state recorded in LogIt
> - Bottle mass and integrated flow cross-checked
> - System ready for SOP-002: GXe circulation through the hot getter
