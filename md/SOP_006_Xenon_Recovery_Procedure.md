---
sop: SOP-006
title: Xenon Recovery Procedure
subtitle: STANDARD OPERATING PROCEDURE - transfer xenon from detector to storage bottles
revision: Rev. C
author: Auke-Pieter Colijn
date: 7 August 2026
location: Nikhef - XAMS
status: Updated release
---

> [!NOTE]
> ** Work  discipline: ** Record every valve operation, bottle change, pressure, temperature, flow setting and interruption in the electronic LogIt logbook. 

> **NOTE** — V12 remains OPEN so the getter volume is evacuated during recovery.

## A. Preconditions and preparation

### 1. Confirm safety and resources

> **ACTION** — Open the laboratory door. Confirm ventilation is operating. Prepare two
> nearly full LN2 dewars, a portable LN2 dewar, cryogenic gloves, apron and safety
> goggles.

> **VERIFY** — Emergency cooling remains connected and available throughout recovery.
> Allow approximately 10 hours for preparation and recovery of about 5.2 kg Xe.

> **STOP** — Do not start without two cooled storage bottles, functional emergency
> cooling, ventilation and cryogenic PPE.

### 2. Prepare detector and monitoring

> **ACTION** — Restart Slow Control/monitor VI and confirm logging of PT201,
> TT203-TT205, TT401-TT402 and flow. Switch OFF PMT1, PMT2, anode and cathode voltages.
> Switch OFF the getter heater, but continue circulation through the getter for at least
> 30 minutes to cool it.

> **VERIFY** — PT201 is approximately 2 bar or higher. If necessary, raise the LakeShore
> setpoint to increase detector pressure before recovery.

> **STOP** — Do not change the gas configuration while detector voltages are ON.

### 3. Stop circulation and establish initial valve state

> **ACTION** — Switch OFF the recirculation pump and wait for flow to stop. Record both
> bottle weights and the current valve configuration. Close V11 and V13. Keep V12 OPEN.
> Close V17 counter-clockwise. Close V8, V7 and V10. Keep V9 OPEN. Confirm V3-V6 and
> both bottle valves are CLOSED.

> **VERIFY** — The getter remains connected through V12; xenon between V13 and V9 can
> return through the detector volume.

## B. Cool both storage bottles

### 4. Fill and raise both LN2 dewars

> **ACTION** — Lower both recovery dewars. Put on apron, goggles and cryogenic gloves.
> Protect the recirculation pump with the blue blanket. Fill both dewars no higher than
> 10 cm below the rim. Raise the dewars SLOWLY until the storage cylinders are immersed.

> **VERIFY** — Raise slowly enough to avoid excessive LN2 boil-off that could trigger
> the laboratory oxygen/gas alarm. Wait until vigorous boiling has stopped and both
> bottle bottoms are cold.

> **STOP** — Always cool both bottles. Do not raise the dewars rapidly or allow LN2 to
> reach the top.

### 5. Prevent xenon-ice blockage during recovery

> **ACTION** — During recovery, periodically inspect the storage bottles. If external
> ice accumulation becomes substantial, carefully remove/warm it with the hot-air gun as
> practiced by experienced operators.

> **VERIFY** — Bottle inlet remains able to accept xenon and PT201 does not show the
> rapid rise characteristic of a blockage.

> **STOP** — Do not overheat bottle valves or use excessive force. If flow stops or
> PT201 rises rapidly, close V7 and switch to the second cold bottle.

## C. Start recovery

### 6. Verify the selected bottle is cold and depressurised

> **ACTION** — Briefly open V5 for bottle A or V6 for bottle B to confirm the
> high-pressure side is below 0.9 bar, then close V5/V6 again. If pressure is higher,
> continue cooling.

> **VERIFY** — Selected bottle pressure is below 0.9 bar before opening the recovery
> route.

> **STOP** — Do not start recovery into a bottle that is not sufficiently cold.

### 7. Reset flow integration and open the route

> **ACTION** — Reset integrated flow in the monitor VI. Open the selected storage-bottle
> main valve. Confirm V17 is CLOSED. Open V3 for bottle A or V4 for bottle B. Open V8,
> then V10. V12 remains OPEN; V11 and V13 remain CLOSED. Open V7 gradually.

> **VERIFY** — Flow is visible and stable. Recovery includes the getter, pump-side
> piping and buffer volumes connected through the selected route.

> **STOP** — V7 is the flow-control valve. Open it gradually and never leave active
> recovery unattended.

### 8. Control pressure and temperature

> **ACTION** — Tune V7 to keep PT201 stable between approximately 1.4 and 2.1 bar.
> Monitor TT203-TT205 and TT401-TT402 continuously. Reduce flow if pressure or
> temperature falls rapidly; increase recovery flow if PT201 rises.

> **VERIFY** — Pressure remains stable and detector temperatures do not fall sharply
> from adiabatic expansion.

> **STOP** — If PT201 rises rapidly, suspect an ice blockage. Close V7 and switch to the
> second cold storage bottle.

## D. Refill LN2 or switch bottles

### 9. Refill a recovery dewar

> **ACTION** — Before lowering a dewar, bring PT201 below 2 bar. Close V7, then the
> active V3/V4, V8 and V10. Refill to 10 cm below the rim, raise the dewar slowly and
> wait until boiling subsides. Recheck bottle pressure below 0.9 bar, then reopen V10,
> V8, active V3/V4 and tune V7.

> **NOTE** — The dewar may be topped up while raised if this can be done safely; in that
> case recovery need not be interrupted.

### 10. Switch to the second bottle

> **ACTION** — Bring PT201 to about 1 bar. Close V7, active V3/V4, V8 and V10. Close the
> full bottle valve. If frozen, warm the valve gently with the hot-air gun; do not force
> it. Confirm the second bottle is below 0.9 bar. Open the second bottle valve, then its
> V3/V4 route, V8 and V10. Tune V7.

> **VERIFY** — Closing the active V3/V4 causes flow to fall to zero; opening the new
> route restores flow.

> **STOP** — A bottle change may increase detector pressure by about 0.6 bar. Monitor
> PT201 continuously.

## E. Optional acceleration and emergency response

### 11. Increase evaporation only when required

> **ACTION** — To increase recovery rate, use one or more approved measures: raise the
> LakeShore setpoint, switch OFF the PTR, or increase V7 flow up to about 10 g/min while
> maintaining the pressure limits.

> **STOP** — Breaking the insulation vacuum or using a hot-air gun on the cryostat is an
> exceptional intervention for experienced operators only.

### 12. If pressure becomes too high

> **ACTION** — Increase recovery flow with V7. If needed, restore insulation-vacuum
> pumping or switch immediately to the second cold storage bottle. Do not restart the
> PTR as a routine pressure-control measure during normal recovery.

> **STOP** — If pressure cannot be controlled, transition to SOP-007 - Emergency Xenon
> Recuperation.

## F. Pause or finish recovery

### 13. Pause recovery

> **ACTION** — Return the LakeShore setpoint to -90 °C well before pausing and restore
> insulation-vacuum pumping if it was stopped. Wait until pressure no longer rises when
> recovery valves are closed. Close from detector side to bottle side: V9, V10,
> carefully fully open V17 until the high-pressure section is depressurised, close V17,
> then close V7, V8, V3/V4 and confirm V5/V6 and bottle valves are closed. Record and
> pause integrated flow.

> **VERIFY** — Pressure and temperature are stable, bottle valves are closed and the
> full valve state is recorded.

> **STOP** — Do not leave the system if pressure rises after isolation.

### 14. Finish recovery

> **ACTION** — Wait until detector pressure is sufficiently low. Stop and unplug all
> heaters. Close V9 and V10. Recover buffer-volume gas through the normal flow path,
> then isolate the buffer volumes. Carefully open V17 fully until the high-pressure
> section reaches low pressure, then close V17. Close V7, V8, V26, V3-V6 and both bottle
> valves. Keep V12 open until the getter has been evacuated, then close V12 as the final
> getter-isolation step.

> **VERIFY** — Record integrated flow, final PT201 and final valve state in LogIt.
> Record the final storage-bottle mass the NEXT DAY, after the external ice layer has
> thawed/melted and the weighing is reliable.

> **STOP** — If a frozen bottle valve cannot be closed easily, warm it gently. Never use
> excessive force.

## FINAL SAFE-STATE CHECK

> [!TIP]
> - All detector voltages OFF
> - Both storage-bottle valves closed
> - V3-V11, V13 and V17 closed as applicable
> - Getter evacuated; V12 closed only after getter recovery is complete
> - Buffer volumes recovered and isolated
> - Emergency cooling available until pressure is confirmed safe
> - Integrated flow recorded; bottle mass recorded the next day after external ice has
>   cleared
> - Any interruption, bottle switch or abnormal pressure response documented
