---
sop: SOP-101
doc_id: XAMS-SOP-101
title: PMT Power On and Off
subtitle: Safely power the photomultiplier tubes on and off, and respond to a trip
revision: Rev. B
issue_date: 2026-09-26
supersedes: Rev. A
author: Auke-Pieter Colijn
prepared_by: Auke-Pieter Colijn
reviewed_by: N/A
approved_by: N/A
audience: Trained XAMS operator authorised for detector high voltage
location: Nikhef - XAMS
status: Draft - not approved for use
---

> [!NOTE]
> **Work discipline:** Record every change to a PMT high voltage, every trip and
> every abnormal observation in the electronic LogIt logbook, with the time.

## Scope and competence

|  |  |
| --- | --- |
| **Purpose** | Switch the PMT high voltage on and off in a controlled ramp with the slow control, and respond to a trip. |
| **Not for** | Gain calibration, which is SOP-104, and TPC electrode voltages, which are SOP-103. |
| **Competence** | Trained XAMS operator authorised for detector high voltage. |
| **Before you start** | Detector closed and dark; all interlocks satisfied; slow control running and the /hv page reachable; approved PMT voltages for this run available. |

> [!NOTE]
> **General hazards apply:** detector high voltage. Read SOP-000 before starting.

> [!NOTE]
> **Supplies and channels.** CAEN DT1470ET hv_1: channel 0 is the bottom PMT,
> channel 1 the top PMT (Hamamatsu R12699, one voltage for its four anodes, DAQ
> channels 1-4). Hard limit 0 to -1100 V. The board ramps at its own rate
> (bottom 1 V/s, top 20 V/s); the enable switch and LOCAL/REMOTE are front-panel
> operations.

## Hazards specific to this procedure

> [!WARNING]
> **Electric shock - high voltage applied to a PMT whose interlocks are not
> satisfied.**
> Energising a channel in the wrong detector configuration can leave an exposed
> conductor live, and contact can be fatal.
> Never apply high voltage unless the detector configuration permits safe operation
> and all interlocks are satisfied.

> [!NOTICE]
> Applying high voltage too quickly, or with the PMT exposed to light, damages the
> photocathode and the dynode chain.
> Ramp in 50 V increments, allow the voltage to stabilise after each increment,
> and never energise a PMT with the detector open.

> [!NOTICE]
> Every change of PMT voltage changes the gain: data taken afterwards need a new
> gain calibration (SOP-104) at the new voltage.
> Do not change PMT voltages during a measurement series.

## A. Power On

### 1. Check the supply

> **ACTION** — Open the /hv page. Check that hv_1 is in REMOTE, that no channel shows
> TRIPPED and that no red VSET banner is shown.

> **VERIFY** — The PMT channels show `disabled`, `enabled` or `ON 0 V` with VSET 0 V.

> **STOP** — Do not continue with a red VSET or a TRIPPED latch; zero the
> setpoints first (`xams-ctl hv-standby`) or follow section D.

### 2. Enable and energise at zero

> **ACTION** — With VSET 0 V, flip the front-panel enable switch of the PMT channel,
> then turn it ON on /hv.

> **VERIFY** — The channel shows `ON 0 V`.

### 3. Ramp the high voltage

> **ACTION** — Raise the setpoint in increments of 50 V up to the approved operating
> value. Wait until VMON has reached each setpoint and IMON is steady before the next.

> **VERIFY** — VMON follows the requested value and no trips or alarms occur.

> **STOP** — Stop the ramp immediately if the supply trips or any abnormal
> behaviour is observed.

### 4. Verify stable operation

> **ACTION** — Observe the PMT current and, with the DAQ running, the pulse rate of
> every PMT channel for at least 15 min after the target voltage has been reached.

> **VERIFY** — The current is steady and the pulse rates are steady and similar to
> earlier runs at the same voltage and threshold.

> **STOP** — Do not start data taking if the current is unstable or a channel
> shows rate bursts.

> [!CUE]
> **OPERATOR CUE**
>
> | | |
> | --- | --- |
> | **Indication** | Pulse rate of one PMT channel rises by a large factor or comes in bursts (on 2026-09-25 the top-PMT channels 3 and 4 rose by a factor 6-50 before the top PMT tripped) |
> | **Immediate response** | Stop the run, lower that PMT by 50 V and watch; if the bursts continue, ramp it down and inform the detector expert |

## B. Record the Configuration

### 5. Record the operating conditions

> **ACTION** — Record in LogIt that the PMT has been switched ON, with the operating
> high voltage, the current and the time. Put the PMT voltages in the DAQ run
> comment.

> **VERIFY** — The logbook entry has been saved and contains the date, time,
> operating high voltage and current.

## C. Power Off

### 6. Ramp down the high voltage

> **ACTION** — Reduce the setpoint to 0 V in increments of 50 V (or set 0 V and turn
> OFF, and let the board ramp down at its own rate).

> **VERIFY** — VMON decreases to 0 V without trips or alarms. The channel reads ON
> while it ramps down; do not re-send the command.

### 7. Disable the channel

> **ACTION** — Turn the channel OFF on /hv and, if the PMT stays off, flip the
> front-panel enable switch off.

> **VERIFY** — The channel shows `disabled` or `enabled` with VSET 0 V and VMON 0 V.

### 8. Record the shutdown

> **ACTION** — Record in LogIt that the PMT has been switched OFF.

> **VERIFY** — The logbook entry has been saved successfully.

## D. Response to a trip

### 9. Record and recover at a lower voltage

> **ACTION** — The slow control has already set VSET 0 V and switched the channel
> OFF. Stop the DAQ run. Record in LogIt: channel, voltage, the highest IMON on the
> banner, the time and the PMT pulse rates before the trip. Press **clear trip**, turn
> the channel ON at 0 V and ramp in 50 V steps to **50 V below** the voltage at which
> it tripped. Wait at least 15 min before data taking.

> **VERIFY** — VMON follows every step; current and pulse rates steady.

> **STOP** — If it trips again, leave it off and inform the detector expert.

> **NOTE** — The new voltage needs a new gain calibration (SOP-104) before physics
> data. Update the run plan and the run comments.

## Troubleshooting

| Fault | Likely cause | Remedy |
| --- | --- | --- |
| Channel TRIPPED | Over-current or discharge in the PMT or its base | Section D; recover 50 V lower |
| Rate bursts on one PMT channel | Micro-discharges or light emission in or near the PMT | Stop the run, lower the voltage by 50 V; inform the detector expert if it persists |
| After clear trip, VMON does not follow | Supply output latched dead after a trip | Ramp the other channels of hv_1 (other PMT, both screens) to 0 V, power-cycle the supply, clear the trip again, restart from step 2 |
| Setpoint refused | Outside -1100..0 V, supply in LOCAL, or channel disabled | Check the value; switch to REMOTE; flip the enable switch with VSET 0 V |
| Gain differs from the previous calibration | Voltage changed, or the PMT was recently switched on | Wait at least 15 min after switching on; recalibrate (SOP-104) |

## FINAL SAFE-STATE CHECK

> [!CHECKLIST]
> - PMT high voltage is 0 V and the channel is OFF with VSET 0 V.
> - No TRIPPED latch and no red VSET on /hv.
> - Power-on, power-off and any trip have been recorded in LogIt.

## Document control

| Revision | Issued | Change |
| --- | --- | --- |
| Rev. B | 2026-09-26 | Operation via the slow-control /hv page; supply channels and ramp rates; rate-burst early warning; trip response at 50 V lower voltage; gain recalibration after a voltage change; troubleshooting. Draft, not yet reviewed or approved. |
| Rev. A | 2026-08-10 | First issue. |
