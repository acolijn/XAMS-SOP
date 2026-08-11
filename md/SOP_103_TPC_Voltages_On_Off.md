---
sop: SOP-103
title: XAMS TPC Electrode High-Voltage Operation
subtitle: Apply and remove high voltage from the XAMS TPC electrodes in the correct sequence
revision: Rev. A
author: Auke-Pieter Colijn
date: 11 August 2026
location: Nikhef - XAMS
status: Draft placeholder
---

> [!NOTE]
> **Work discipline:** Record all voltage setpoints, achieved voltages and any
> abnormal behaviour in the electronic LogIt logbook.

## Hazards

> [!DANGER]
> **Electric shock - exposed high-voltage equipment.**
> Contact with energised high-voltage components can cause serious injury or
> death.
> Ensure all high-voltage enclosures are closed and interlocks are functional
> before enabling any high-voltage supply.

> [!WARNING]
> **Incorrect electrode energisation sequence.**
> Applying voltages in the wrong order may produce excessive electric fields,
> causing electrical discharges or detector damage.
> Always energise and de-energise the electrodes in the sequence specified in
> this procedure.

> [!NOTICE]
> Incorrect voltage setpoints or ramp rates may damage the detector or
> high-voltage supplies.
> Verify all setpoints before enabling any high-voltage channel.

## A. Preconditions

### 1. Verify detector readiness

> **ACTION** — Confirm that the detector is ready for high-voltage operation,
> all safety interlocks are satisfied and all electrode channels are switched
> OFF.

> **VERIFY** — No active interlocks are present and all electrode voltages read
> 0 V.

> **STOP** — Do not proceed if any interlock is active or any electrode cannot
> be verified at 0 V.

### 2. Enter the required voltage settings

> **ACTION** — Enter the required operating voltages and ramp rates for each
> electrode channel.

> **NOTE** — Operating voltages and ramp rates depend on the detector
> configuration and shall be specified by the detector expert.

| Item | Value |
| --- | --- |
| Bottom screen voltage | TBD - detector operating value |
| Cathode voltage | TBD - detector operating value |
| Gate voltage | TBD - detector operating value |
| Anode voltage | TBD - detector operating value |
| Top screen voltage | TBD - detector operating value |
| Ramp rate | TBD - detector operating value |

## B. Switching ON the electrodes

### 3. Energise the screen electrodes

> **ACTION** — Ramp the bottom and top screen electrodes to the same voltage as
> the corresponding PMT high voltage, within ±50 V.

> **VERIFY** — Both screen electrodes reach their target voltages without trips
> or abnormal current.

> **STOP** — Do not continue if either screen electrode trips or cannot reach
> its setpoint.

### 4. Energise the cathode

> **ACTION** — Ramp the cathode to the required operating voltage.

> **VERIFY** — The cathode reaches the requested voltage and remains stable.

> **STOP** — Do not continue if the cathode trips or exhibits unstable current.

### 5. Energise the gate

> **ACTION** — Ramp the gate to the required operating voltage.

> **VERIFY** — The gate reaches the requested voltage and remains stable.

> **STOP** — Do not continue if the gate trips or exhibits unstable current.

### 6. Energise the anode

> **ACTION** — Ramp the anode to the required operating voltage.

> **VERIFY** — The anode reaches the requested voltage and all electrode
> voltages remain stable.

> **NOTE** — The TPC is ready for operation once all electrode voltages are
> stable and no trips or abnormal leakage currents are observed.

## C. Switching OFF the electrodes

### 7. Ramp down the anode

> **ACTION** — Ramp the anode to 0 V.

> **VERIFY** — The anode voltage reads 0 V.

### 8. Ramp down the gate

> **ACTION** — Ramp the gate to 0 V.

> **VERIFY** — The gate voltage reads 0 V.

### 9. Ramp down the cathode

> **ACTION** — Ramp the cathode to 0 V.

> **VERIFY** — The cathode voltage reads 0 V.

### 10. Ramp down the screen electrodes

> **ACTION** — Ramp the top and bottom screen electrodes to 0 V.

> **VERIFY** — Both screen electrode voltages read 0 V.

> **NOTE** — The shutdown sequence is the reverse of the energisation sequence
> to minimise electric field transients inside the detector.

## FINAL SAFE-STATE CHECK

> [!CHECKLIST]
> - All electrode channels at 0 V
> - All high-voltage channels disabled
> - No active high-voltage alarms or trips
> - Final voltages recorded in LogIt