---
sop: SOP-004
title: LXe Filling
subtitle: Fill the detector with liquid xenon
revision: Rev. E
author: Auke-Pieter Colijn
date: 10 August 2026
location: Nikhef - XAMS
status: Updated release
---

> [!NOTE]
> **Work discipline:** Record every valve operation, configuration change, bottle mass,
> pressure, temperature, and integrated-flow value in the electronic LogIt logbook.

> [!NOTE]
> **General hazards apply:** asphyxiation (xenon and nitrogen), cryogenic burn,
> stored energy in the gas system. Read SOP-000 before starting.

## Hazards specific to this procedure

> [!WARNING]
> **Overpressure - flash evaporation when liquid xenon first contacts warm cryostat
> surfaces.**
> A sudden pressure rise in the detector volume can rupture a fitting or a window
> and injure anyone standing at the cryostat.
> Keep emergency cooling operational, monitor TT203/TT204/TT205 continuously through
> the overflow transition, and do not stand over the cryostat while filling.

> [!NOTICE]
> Mixing the direct and hot-getter filling routes, or filling with detector voltages
> on, damages the getter and the detector electronics.
> Switch off all detector voltages before filling, and record the chosen route in
> LogIt before opening V7.

## A. Preconditions and preparation

### 1. Confirm prerequisites

> **ACTION** — **Confirm the system has been baked and that SOP-001 has been
> completed.** **Confirm SOP-002 has provided at least 7 effective days of GXe
> circulation** **through the hot getter. Confirm SOP-003 cooling preparation has been**
> **completed.**

> **VERIFY** — Detector contains purified xenon gas, cooling systems are ready, and
> required permissions have been obtained.

> **STOP** — **Do not start LXe filling unless the one-week hot-getter purification
> requirement is** **complete and documented in LogIt.**

### 2. Verify alarms, remote access, and computer readiness

> **ACTION** — **Confirm alarm systems and emergency shifter coverage are operational.
> Check** **the Alcatel USB dongle internet connection by loading an internet page.
> Confirm** **the SIM is active. Prevent automatic Windows updates or restarts during**
> **unattended operation.**

> **VERIFY** — Remote connection works, alarms are active, and the Slow Control computer
> will not restart unexpectedly.

> **STOP** — **Do not continue if alarms, remote access, or Slow Control availability
> are** **uncertain.**

### 3. Make emergency cooling operational

> **ACTION** — **Switch on power supply E030-1 for the solenoid valve. Open the liquid
> valve on** **the emergency dewar. Briefly test the solenoid valve and confirm
> nitrogen** **exhaust at the roof outlet. Confirm the emergency-cooling pressure
> switch** **setting.**

> **VERIFY** — A click is heard when power is applied, nitrogen exhaust is observed
> during the brief test, and sufficient LN2 is available.

> **STOP** — **Do not proceed without functional emergency cooling. Minimise LN2 loss
> during** **the test.**

### 4. Pre-cool the TPC with gas

> **ACTION** — **Set LakeShore T(A) to approximately -90 °C, or lower if liquid droplets
> are** **intentionally required. Set Heater Range to HIGH. Run recirculation during
> the** **gas cool-down to maximise heat transfer. Allow approximately one day or
> more.**

> **VERIFY** — Heater Range is HIGH. TPC pressure and temperature are below the intended
> final operating point, providing thermal margin for filling.

> **STOP** — **Do not begin liquid filling until the detector is sufficiently cold and
> stable.**

## B. Optional first data

### 5. Take optional pre-fill data

> **ACTION** — **Optionally take a PMT calibration and gas-phase scintillation
> measurements** **before filling. No electric fields are required for these
> measurements; keep** **detector high voltages off unless a separately approved
> measurement procedure** **explicitly requires them.**

> **VERIFY** — Any required pre-fill calibration or reference data have been saved and
> documented.

## C. Fill with liquid xenon

### 6. Prepare the gas system

> **ACTION** — **Switch off all detector voltages. For the standard direct filling
> route, switch off** **the getter but maintain flow through it for at least 15 minutes
> to cool it, then** **switch off the recirculation pump. Close all gas-board valves,
> including pressure** **regulator V17 by turning it counter-clockwise. Record the
> configuration in LogIt.**

> **VERIFY** — All detector voltages are OFF. For direct filling, getter is cool and
> recirculation pump is OFF. All valves and V17 are closed.

> **STOP** — **Do not change the filling configuration while detector voltages are on.**

### 7. Prepare bottle and flow monitoring

> **ACTION** — **Record the storage-bottle weight. Reset integrated flow in Slow Control
> and** **confirm integration has started. Open the xenon bottle main valve. Open V6
> for** **bottle B or V5 for bottle A.**

> **VERIFY** — Bottle identity and initial mass are in LogIt; integrated flow is active;
> high-pressure side responds normally.

### 8. Choose and establish the filling path

> **ACTION** — **Set V17 so the low-pressure side is approximately 2 bar. Choose one
> approved** **route:** **Direct route: open V8, V9, and V13.** **Hot-getter route: keep
> V13 closed and open V11 and V12 so xenon is filled** **through the hot getter. Confirm
> the getter is at its approved hot operating** **condition before opening this route.**
> **Then open needle valve V7 slowly while continuously observing flow and** **detector
> pressure.**

> **VERIFY** — The selected route is explicitly recorded in LogIt. Flow starts gradually
> and detector pressure responds smoothly. For the hot-getter route, getter status
> remains normal.

> **STOP** — **Never mix the direct and hot-getter valve configurations. If route
> identity is** **uncertain, close V7 and reconstruct the valve state before
> continuing.**

### 9. Use all available cooling power

> **ACTION** — **Lower the LakeShore setpoint sufficiently that the heating band
> switches off.** **Keep Heater Range HIGH. Continue filling while maintaining stable
> pressure and** **temperature.**

> **VERIFY** — Heating power is at or near zero and cooling capacity is available for
> condensation.

> **STOP** — **Someone must remain present throughout filling. Keep alarms enabled. Do
> not** **leave an active fill unattended.**

## C. Fill with liquid xenon - TPC bucket overflow

### 9A. Respond when LXe reaches the top of the TPC bucket

> [!WARNING]
> **Overpressure - liquid xenon overflowing the TPC bucket onto the still-warm
> cryostat wall.**
> Flash evaporation causes a sudden pressure rise and unstable detector pressure
> until the cryostat bottom has cooled, and can rupture a fitting or a window.
> Switch on emergency cooling as soon as TT203/TT204/TT205 drop, keep clear of the
> cryostat, and do not increase the fill rate until pressure is stable again.

> **ACTION** — **Continuously monitor TT203, TT204, and TT205. When their temperatures
> drop,** **indicating that LXe has reached the top of the TPC bucket, switch ON
> emergency** **cooling immediately.**

> **VERIFY** — Emergency cooling is ON. Continue monitoring detector pressure and
> TT203/TT204/TT205 closely. A temporary pressure rise or pressure instability is
> expected while the cryostat bottom cools.

> **STOP** — **Do not leave this transition unattended. If pressure rises beyond safe
> control,** **stop the active fill and follow** SOP-007 - Emergency Xenon Recuperation
> **.**

> [!CUE]
> **OPERATOR CUE**
>
> |  |  |
> | --- | --- |
> | Indication | TT203/TT204/TT205 temperature drop |
> | Immediate response | Switch ON emergency cooling |
> | Expected behaviour | Transient flash evaporation and pressure instability |
> | Continue filling when | Pressure stabilises as the cryostat bottom becomes cold |

## D. Switching storage bottles

### 10. Switch from bottle B to bottle A

> **ACTION** — **As bottle-B pressure drops, fully open V17 and V7 to recover the
> remaining gas.** **Record both bottle weights. Close V6, V7, and V17. Close bottle-B
> main valve.** **Open bottle-A main valve, then open V5. Record the high-pressure
> reading. Open** **V17 and set the low-pressure side to approximately 2 bar.
> Re-establish the** **previously selected filling route and flow with V7.**

> **VERIFY** — Bottle B is isolated, bottle A is connected, low pressure is stable near
> 2 bar, and flow has resumed smoothly through the same documented route.

> **STOP** — **Do not open the new bottle path until the previous bottle and associated
> valves** **are positively isolated.**

## E. Pause filling

### 11. Put the system in a stable paused state

> **ACTION** — **Record bottle weight and integrated flow. Close the bottle main valve.
> Allow** **remaining gas in the high-pressure region to enter the system. Set the**
> **LakeShore setpoint so heating power is high enough to maintain stable** **conditions
> and keep Heater Range HIGH. Close V7, then close all valves** **belonging to the
> selected filling route. Close V6 if bottle B was used, or V5 if** **bottle A was used.
> Pause integrated flow.**

> **VERIFY** — No active bottle connection remains, the selected filling path is fully
> closed, pressure and temperature are stable, and integrated flow is paused.

> **STOP** — **Do not leave the system in a partially isolated or undocumented
> configuration.**

## F. Final safe-state and LogIt record

## FINAL SAFE-STATE CHECK

> [!CHECKLIST]
> - SOP-002 one-week hot-getter purification completed and documented
> - All detector voltages are OFF during filling
> - LakeShore Heater Range HIGH
> - Bottle identity, initial/final mass, and any bottle switch recorded
> - Every valve action, selected route, and configuration change recorded
> - Integrated flow recorded and reconciled with bottle mass change
> - Detector pressure and temperature evolution recorded
> - Alarm coverage and emergency cooling operational
> - TPC-bucket overflow transition and emergency-cooling activation documented
> - If paused, all valves of the selected route closed and system thermally stable
> - Any deviation, unexpected response, or intervention documented and handed over

NEXT PROCEDURE: Continue with SOP-005 - Normal LXe Operation.
