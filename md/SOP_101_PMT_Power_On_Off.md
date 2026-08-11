---
sop: SOP-101
doc_id: XAMS-SOP-101
title: PMT Power On and Off
subtitle: Safely power the photomultiplier tube on and off
revision: Rev. A
issue_date: 2026-08-10
supersedes: N/A
author: Auke-Pieter Colijn
prepared_by: Auke-Pieter Colijn
reviewed_by: N/A
approved_by: N/A
audience: Trained XAMS operator authorised for detector high voltage
location: Nikhef - XAMS
status: Initial release
---

> [!NOTE]
> **Work discipline:** Record every change to the PMT high-voltage state in the
> electronic LogIt logbook.

## Scope and competence

|  |  |
| --- | --- |
| **Purpose** | Switch the PMT high voltage on and off in a controlled ramp. |
| **Not for** | Gain calibration, which is SOP-104, and TPC electrode voltages, which are SOP-103. |
| **Competence** | Trained XAMS operator authorised for detector high voltage. |
| **Before you start** | Detector configuration permits high voltage; all interlocks satisfied; CAEN supply serviceable. |

> [!NOTE]
> **General hazards apply:** detector high voltage. Read SOP-000 before starting.

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
> Ramp in 50 V increments and allow the voltage to stabilise after each increment.

## A. Power On

### 1. Switch on the CAEN power supply

> **ACTION** — Switch ON the CAEN high-voltage power supply and verify that the
> required PMT channel is available for operation.

> **VERIFY** — The CAEN power supply is operational, the channel is enabled, and
> no faults or alarms are indicated.

> **STOP** — Do not continue if the power supply reports a fault or the channel
> cannot be enabled.

### 2. Ramp the high voltage

> **ACTION** — Increase the PMT high voltage to the required operating value in
> increments of 50 V. Allow the voltage to stabilise after each increment before
> proceeding to the next step.

> **VERIFY** — The displayed high voltage follows the requested value and no
> unexpected trips or alarms occur during the ramp.

> **STOP** — Stop the ramp immediately if the power supply trips or any abnormal
> behaviour is observed.

### 3. Verify stable operation

> **ACTION** — Observe the PMT current after the target high voltage has been
> reached.

> **VERIFY** — The current remains stable without unexpected fluctuations and no
> alarms are present.

> **STOP** — Do not continue with detector operation if the current is unstable
> or exceeds the expected operating value.

## B. Record the Configuration

### 4. Record the operating conditions

> **ACTION** — Record in the electronic LogIt logbook that the PMT has been
> switched ON and note the operating high voltage.

> **VERIFY** — The logbook entry has been saved and contains the date, time and
> operating high voltage.

> **NOTE** — Include any observations made during the voltage ramp or current
> verification.

## C. Power Off

### 5. Ramp down the high voltage

> **ACTION** — Reduce the PMT high voltage to 0 V in increments of 50 V.

> **VERIFY** — The displayed high voltage decreases to 0 V without trips or
> alarms.

> **STOP** — Stop the procedure if abnormal behaviour or repeated trips are
> observed.

### 6. Switch off the CAEN power supply

> **ACTION** — Disable the PMT channel and switch OFF the CAEN high-voltage power
> supply.

> **VERIFY** — The channel is disabled, the output voltage is 0 V, and the power
> supply is switched OFF.

### 7. Record the shutdown

> **ACTION** — Record in the electronic LogIt logbook that the PMT has been
> switched OFF.

> **VERIFY** — The logbook entry has been saved successfully.

## FINAL SAFE-STATE CHECK

> [!CHECKLIST]
> - PMT high voltage is 0 V.
> - CAEN high-voltage channel is disabled.
> - CAEN power supply is switched OFF.
> - Power-on and power-off actions have been recorded in LogIt.

## Document control

| Revision | Issued | Change |
| --- | --- | --- |
| Rev. A | 2026-08-10 | First issue. |
