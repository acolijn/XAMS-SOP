---
sop: SOP-101
title: PMT Power On and Off
subtitle: STANDARD OPERATING PROCEDURE - safely power the photomultiplier tube on and off
revision: Rev. A
author: Auke-Pieter Colijn
date: 10 August 2026
location: Nikhef - XAMS
status: Initial release
---

> [!NOTE]
> **Work discipline:** Record every change to the PMT high-voltage state in the
> electronic LogIt logbook.

> [!CAUTION]
> Never apply high voltage to a PMT unless the detector configuration permits
> safe operation and all interlocks are satisfied.

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

> [!TIP]
> - PMT high voltage is 0 V.
> - CAEN high-voltage channel is disabled.
> - CAEN power supply is switched OFF.
> - Power-on and power-off actions have been recorded in LogIt.