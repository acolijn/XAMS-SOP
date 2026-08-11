---
sop: Master Index
title: XAMS Operations Manual
subtitle: Quick index
revision: Rev. D
author: Auke-Pieter Colijn
date: 7 August 2026
location: Nikhef - XAMS
status: Added detector operations
---

> [!NOTE]
> This index lists the current revision of every procedure. Always work from the
> individual SOP, not from this summary.

## 0. Read this first

| SOP | Procedure | Use |
| --- | --- | --- |
| SOP-000 | General Hazards | Hazards, PPE, ODH response and emergency contacts for the whole installation |

SOP-000 is not a procedure. It collects the hazards common to every XAMS
operation so that the individual SOPs need only name them and add what is
specific to themselves. Read it before any work on the setup, and keep a copy
posted in the laboratory.

## 1. Normal operating sequence

Run these procedures in the order listed.

| SOP | Procedure | Condition to move on |
| --- | --- | --- |
| SOP-001 | GXe Filling | Detector filled with xenon gas |
| SOP-002 | GXe Circulation Through Hot Getter | Hot getter run for at least 7 effective days |
| SOP-003 | Cooling preparation and PTR start | Cooling systems ready |
| SOP-004 | LXe Filling | Detector filled with liquid xenon |
| SOP-005 | Normal LXe Operation | Steady circulation and measurement |

## 2. Recovery and facility support

| SOP | Procedure | Use |
| --- | --- | --- |
| SOP-006 | Xenon Recovery | Planned recovery |
| SOP-007 | Emergency Xenon Recuperation | Use immediately when required |
| SOP-008 | Main LN2 Supply Dewar Refill | Cryotrans refill procedure |

## 3. Detector operations

| SOP | Procedure | Status |
| --- | --- | --- |
| SOP-101 | PMT Power On and Off | Released |
| SOP-102 | SiPM Bias Power On and Off | Released |
| SOP-103 | TPC Voltages On / Off | DRAFT |
| SOP-104 | PMT Gain Calibration | Released |

> [!DANGER]
> **Unapproved procedure - SOP-103 is a placeholder and its TPC high-voltage
> settings have not been reviewed.**
> Energising the TPC electrodes from an unverified procedure risks a fatal electric
> shock and destruction of the detector.
> Do not use SOP-103 to energise detector hardware until the detector experts have
> approved all settings.

## 4. SOP register

| SOP | Rev. | Procedure | Purpose |
| --- | --- | --- | --- |
| 000 | A | General Hazards | Hazards common to all XAMS operations - read before any procedure |
| 001 | D | GXe Filling | Initial gas fill before purification |
| 002 | C | GXe Circulation Through Hot Getter | Purify xenon before cooling |
| 003 | D | Cooling Preparation and PTR Start | Prepare cooling after GXe purification |
| 004 | E | LXe Filling | Fill the detector with liquid xenon |
| 005 | A | Normal LXe Operation | Normal operation after LXe filling |
| 006 | C | Xenon Recovery | Transfer xenon from detector to storage bottles |
| 007 | B | Emergency Xenon Recuperation | Night-time emergency response |
| 008 | A | Main LN2 Supply Dewar Refill | Schedule and prepare the main LN2 dewar for refill |
| 101 | A | PMT Power On and Off | Safely power the photomultiplier tube on and off |
| 102 | A | SiPM Bias Power On and Off | Safely power the SiPM readout and bias supply |
| 103 | A | TPC Voltages On / Off | Detector operations placeholder |
| 104 | B | PMT Gain Calibration | LED gain calibration of the top and bottom PMTs |

## 5. Before starting any SOP

- Use the current revision and read the complete procedure before starting.
- Confirm an approved measurement plan / operating plan is available for the
  intended activity.
- Confirm Slow Control and alarms are operational where required.
- Record all required valve states, pressures, temperatures, masses, flows and
  deviations in LogIt.
- Do not leave an active xenon transfer unattended.
- Stop and contact an experienced operator if detector response is unexpected.
