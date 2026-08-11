---
sop: SOP-102
doc_id: XAMS-SOP-102
title: SiPM Bias Power On and Off
subtitle: Safely power the SiPM readout and bias supply
revision: Rev. A
issue_date: 2026-08-10
supersedes: N/A
author: Auke-Pieter Colijn
prepared_by: Auke-Pieter Colijn
reviewed_by: Anna Hurhina
approved_by: Auke-Pieter Colijn
audience: Trained XAMS operator authorised for detector high voltage
location: Nikhef - XAMS
status: Initial release
---

> [!NOTE]
> **Work discipline:** Record all bias voltages, breakdown voltages and any
> anomalies in the electronic LogIt logbook.

## Scope and competence

|  |  |
| --- | --- |
| **Purpose** | Power the SiPM readout and bias supply on and off, and determine the operating bias voltage. |
| **Not for** | PMT high voltage, which is SOP-101, and any work inside the readout box while powered. |
| **Competence** | Trained XAMS operator authorised for detector high voltage. |
| **Before you start** | SiPMs installed in a light-tight environment; multimeter and oscilloscope available; forward-voltage and short checks possible. |

> [!NOTE]
> **General hazards apply:** detector high voltage. Read SOP-000 before starting.

## Hazards specific to this procedure

> [!WARNING]
> **Electric shock and arcing - SiPM bias voltage present on the wiring and
> connectors.**
> Disconnecting or reconnecting a biased channel can arc across the connector and
> injure the hands or eyes.
> Ramp the bias to 0 V and switch off the supply before touching any SiPM cable, and
> never make or break a connection while bias is applied.

> [!NOTICE]
> Biasing a SiPM that is exposed to ambient light permanently damages the sensor.
> Confirm the environment is light-tight before applying any bias voltage.

## A. Pre-power Checks

### 1. Verify the SiPM connections

> **ACTION** — Set the multimeter to diode mode. Connect the COM terminal to the
> expected SiPM cathode and the VΩmA terminal to the expected SiPM anode. Verify
> the forward voltage of each connected SiPM.

> **VERIFY** — The measured forward voltage is between 0.55 V and 0.70 V,
> depending on the SiPM model.

> **STOP** — Do not continue if any measured forward voltage is outside the
> expected range.

### 2. Check for short circuits

> **ACTION** — Verify with the multimeter that there is no short circuit between
> the anode and cathode of each SiPM.

> **VERIFY** — No short circuit is detected.

> **STOP** — Do not power the readout board if any SiPM is shorted.

## B. Power On

### 3. Power the amplifier

> **ACTION** — Switch on the amplifier power supply by applying +6 V, -6 V and
> the common ground.

> **VERIFY** — The amplifier powers up normally without faults or abnormal
> current draw.

> **STOP** — Do not continue if the power supply indicates a fault or reaches
> its current limit.

### 4. Apply the SiPM bias voltage

> **ACTION** — Configure the SiPM bias supply with a current limit of 20 mA
> maximum. Increase the bias voltage at a rate not exceeding 5 V/s until
> 49 V is reached.

> **VERIFY** — The bias voltage increases smoothly and the current remains below
> the configured limit.

> **STOP** — If the current limit is reached, immediately reduce the bias
> voltage to 0 V and inspect the system for a short circuit. Do not continue
> increasing the voltage.

### 5. Determine the breakdown voltage

> **ACTION** — Above 49 V, increase the bias voltage at no more than 0.5 V/s
> while monitoring the SiPM output on an oscilloscope. Identify the breakdown
> voltage as the point where the single-photoelectron peaks become just
> distinguishable.

> **VERIFY** — The breakdown voltage has been identified and recorded.

> **STOP** — For Hamamatsu S13360-6050PE SiPMs, never exceed 56 V.

> **NOTE** — The operating bias voltage is equal to the measured breakdown
> voltage plus 3 V.

> [!CUE]
> **OPERATOR CUE**
>
> | | |
> | --- | --- |
> | **Indication** | Single-photoelectron peaks become visible |
> | **Immediate response** | Record the breakdown voltage and increase the bias by exactly 3 V |

### 6. Verify normal operation

> **ACTION** — Set the operating bias voltage to the measured breakdown voltage
> plus 3 V. Verify the signal quality on the oscilloscope and monitor the bias
> voltage for 30 minutes.

> **VERIFY** — The signal-to-noise ratio is satisfactory and the bias voltage
> remains stable throughout the monitoring period.

> **STOP** — Do not continue operation if the bias voltage drifts significantly
> or the signal quality deteriorates.

## C. Power Off

### 7. Ramp down the bias voltage

> **ACTION** — Reduce the SiPM bias voltage to 0 V at a rate not exceeding
> 5 V/s.

> **VERIFY** — The bias voltage reads 0 V.

### 8. Switch off the amplifier

> **ACTION** — Switch off the ±6 V amplifier power supply.

> **VERIFY** — The amplifier is fully powered down.

> **NOTE** — Never disconnect SiPM cables until both the bias supply and the
> amplifier supply have been switched off.

## D. Emergency Response

### 9. Respond to electrical failure

> **ACTION** — If smoke or a burning smell is observed from the readout box,
> immediately switch off the power supply using the main power switch.

> **VERIFY** — All electrical power to the readout box has been removed.

> **STOP** — Do not continue operation. Follow the laboratory fire safety
> procedure and report the incident.

## FINAL SAFE-STATE CHECK

> [!CHECKLIST]
> - SiPM bias voltage is 0 V.
> - ±6 V amplifier supply is switched OFF.
> - No SiPM cables are connected or disconnected while powered.
> - Breakdown voltage, operating bias voltage and observations have been
>   recorded in LogIt.

## Document control

| Revision | Issued | Change |
| --- | --- | --- |
| Rev. A | 2026-08-10 | First issue. |
