---
sop: SOP-103
doc_id: XAMS-SOP-103
title: XAMS TPC Electrode High-Voltage Operation
subtitle: Apply, change and remove high voltage on the XAMS TPC electrodes, and respond to a trip
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
> **Work discipline:** Record every setpoint, every achieved voltage and current,
> every trip and every abnormal observation in the electronic LogIt logbook,
> with the time. Change one high-voltage channel at a time.

## Scope and competence

|  |  |
| --- | --- |
| **Purpose** | Apply, change and remove high voltage on the TPC electrodes (bottom screen, cathode, gate, anode, top screen) with the slow control, and respond to a trip. |
| **Not for** | PMT and SiPM voltages (SOP-101, SOP-102). Changing the supplies' protection settings (MAXV, ramp rate, trip current) - those are set by the detector expert only. |
| **Competence** | Trained XAMS operator authorised for detector high voltage, working to setpoints approved by the detector expert. |
| **Before you start** | Detector in normal LXe operation (SOP-005); slow control running and the **Controls** page (high-voltage section) reachable; approved setpoints for this run available. |

> [!NOTE]
> **General hazards apply:** detector high voltage. Read SOP-000 before starting.

> [!NOTE]
> **Supplies and channels.** Two CAEN DT1470ET supplies, operated from the
> high-voltage section of the slow-control **Controls** page. hv_2 carries the cathode (ch 0), gate (ch 1), anode
> (ch 2) and the NaI detector (ch 3); hv_1 carries the PMTs (ch 0, 1) and the
> top and bottom screens (ch 2, 3). The front-panel enable switch and the
> LOCAL/REMOTE mode are hand operations; the software sets VSET and switches a
> channel ON or OFF, and the board ramps at its own rate.

## Hazards specific to this procedure

> [!WARNING]
> **Discharge in the TPC - electrode voltages or voltage differences above what
> the detector withstands.**
> A discharge can damage electrodes, the field cage, feedthroughs and PMTs, and
> can put energy into cabling that is handled afterwards.
> Stay inside the limits of Table 1 at every intermediate step, change one
> electrode at a time, and never exceed the highest value run stably before
> without the detector expert.

> [!WARNING]
> **Stored charge - electrode cabling after switch-off.**
> A cable or connector can hold charge after VMON reads 0 V.
> Never disconnect or touch a high-voltage cable or connector with any channel of
> that supply ON; follow SOP-000 for work on detector high voltage.

> [!NOTICE]
> Operating voltages applied to an empty, warm or partly filled TPC (gas only)
> can break down at much lower values than in liquid.
> Apply operating voltages only in normal LXe operation (SOP-005), unless the
> detector expert gives explicit other setpoints.

## A. Preconditions

### 1. Verify the detector state

> **ACTION** — Check on the slow control that the detector is in normal LXe
> operation: pressure, temperatures and liquid level at their normal values.

> **VERIFY** — Pressure, temperatures and level are stable and inside their normal
> range, and no slow-control alarm is active.

> **STOP** — Do not apply high voltage during filling, recovery, warm-up or any
> alarm, or if the level is unknown.

### 2. Verify the high-voltage supplies

> **ACTION** — Open the **Controls** page (high-voltage section). Check that both supplies are in REMOTE, that no
> channel shows TRIPPED, and that no red VSET banner is shown (a disabled channel
> with a non-zero setpoint).

> **VERIFY** — Both supplies REMOTE; every TPC electrode channel `disabled`,
> `enabled` or `ON 0 V` with VSET 0 V; no TRIPPED latch; no red VSET.

> **STOP** — Do not continue with a red VSET: the board ramps to VSET the moment
> the enable switch is flipped. Zero all setpoints first (`xams-ctl hv-standby`).

### 3. Check the setpoints against the limits

> **ACTION** — Press **Load defaults** and compare every box with the approved
> setpoints for this run. Check each setpoint, and each voltage difference, against
> Table 1. Record the setpoints in LogIt.

> **VERIFY** — Every setpoint and every difference is inside Table 1 and matches
> the approved setpoints.

> **STOP** — Do not apply a setpoint that is not approved, or that exceeds a limit
> or the highest value run stably before, without the detector expert.

**Table 1 - limits and operating experience** (update the right-hand column when
the operating point moves; the hard limits are changed only by the detector
expert, on the board and in the slow-control `channels.yaml` together).

| Electrode | Hard limit (board MAXV = slow-control range) | Highest stable / known problems |
| --- | --- | --- |
| Bottom screen | 0 to -2000 V | -1000 V |
| Cathode | 0 to -3500 V | -3250 V (2026-09-25); has tripped before |
| Gate | 0 to -3750 V | -2750 V (2026-09-25) |
| Anode | 0 to +4500 V | +2250 V stable; **broke down at +2400 V and +2500 V (2026-09-23)** |
| Top screen | 0 to -1710 V | -100 V |
| Gate - anode difference | set by the detector expert | 5.0 kV (2026-09-25) |

> [!NOTE]
> The board's own ramp rates are cathode 25 V/s, gate and anode 50 V/s. They are
> protection settings, read by the slow control and never changed by it.

### 4. Start monitoring

> **ACTION** — Keep the PMTs at their operating voltage (SOP-101) and start a
> DAQ monitoring run with the comment 'HV ramp'. Open the Grafana HV panel (VMON
> and IMON of every channel).

> **VERIFY** — PMT pulse rates per channel and electrode currents are visible and
> steady before any electrode is ramped.

> **NOTE** — A discharge usually shows first as a current spike or as a burst in
> the PMT pulse rates, before the supply trips.

## B. Switching ON the electrodes

### 5. Enable the channels

> **ACTION** — With VSET 0 V on every channel, flip the front-panel enable switch
> of each electrode channel that will be used.

> **VERIFY** — The channels show `enabled` (not energised) and VMON 0 V.

### 6. Energise the screen electrodes

> **ACTION** — Apply the top and bottom screen setpoints and turn the channels ON.

> **VERIFY** — Both screens reach their setpoints; IMON returns to its steady value.

> **STOP** — Do not continue if a screen trips or its current does not settle.

### 7. Raise the cathode in steps

> **ACTION** — Raise the cathode in steps of at most 500 V: apply the setpoint,
> turn ON (first step only), wait until VMON has reached it and IMON is steady for
> at least 1 min. Above the highest value run stably before, use steps of at most
> 100 V and hold at least 10 min at each step.

> **VERIFY** — VMON follows every step; IMON returns to a steady value; no PMT rate
> bursts.

> **STOP** — Stop at the current value on a current spike, a creeping current or a
> rate burst; see the trip response in section E if the channel trips.

### 8. Raise the gate in steps

> **ACTION** — Raise the gate in the same way as the cathode (steps of at most
> 500 V, hold until steady).

> **VERIFY** — VMON follows every step; IMON steady; no PMT rate bursts.

> **STOP** — As for the cathode.

### 9. Raise the anode in steps

> **ACTION** — Raise the anode in steps of at most 250 V up to +2000 V, and in steps
> of at most 100 V above +2000 V, holding at least 2 min at each step. The anode and
> gate sit in the gas phase and are the most sensitive to breakdown.

> **VERIFY** — VMON follows every step; IMON steady; no PMT rate bursts.

> **STOP** — Stop and step back 100 V on any current spike or rate burst; never
> exceed the highest stable anode voltage of Table 1 without the detector expert.

### 10. Verify stable operation

> **ACTION** — Hold all electrodes at their setpoints for 15 min before data taking.

> **VERIFY** — All currents flat, PMT rates normal, no trips. Record the final
> VMON and IMON of every channel in LogIt.

## C. Changing an electrode voltage during operation

### 11. Change one electrode, in small steps

> **ACTION** — To change the drift field, change the cathode only; to change the
> extraction field, change the anode (or gate) only. Use steps of at most 125 V and
> hold until IMON is steady. Never change a PMT voltage and an electrode voltage at
> the same time. Note the time of every change in LogIt and in the run comment.

> **VERIFY** — VMON at the new setpoint, IMON steady, PMT rates normal.

## D. Switching OFF the electrodes

### 12. Ramp down in reverse order

> **ACTION** — Set VSET to 0 V and turn OFF, one channel at a time and in this
> order: anode, gate, cathode, top and bottom screen. Wait for each to reach 0 V
> before the next.

> **VERIFY** — Each channel reaches 0 V. A channel keeps reading ON while it ramps
> down at the board's rate; do not re-send the command.

> **NOTE** — The shutdown order is the reverse of the energisation order, to keep
> the field in the gas gap and the drift region controlled.

## E. Response to a trip

### 13. Make the detector safe and record

> [!CUE]
> **OPERATOR CUE**
>
> | | |
> | --- | --- |
> | **Indication** | The **Controls** page shows a red banner and TRIPPED on a channel, or VMON collapses to 0 V while the channel still reads ON |
> | **Immediate response** | Stop every ramp. Do not clear the trip yet. The slow control has already set VSET 0 V and switched the channel OFF |

> **ACTION** — Leave the other electrodes where they are unless the detector
> expert says otherwise. Record in LogIt: channel, setpoint, the highest IMON shown
> on the banner, the time, the other electrode voltages, pressure and level, and
> the DAQ run number. Look at VMON/IMON and the PMT rates in the minutes before the
> trip (Grafana, DAQ).

> **VERIFY** — The tripped channel is OFF at 0 V and the cause has been looked for.

> **NOTE** — A trip sends no alarm: it is expected to happen with people in the lab.

### 14. Clear and recover

> **ACTION** — Press **clear trip** on the **Controls** page. This sets VSET 0 V and switches OFF
> every tripped channel on that supply, and clears the board alarm; the channel
> stays off. Turn it ON at 0 V, then raise it in steps of at most 100 V to one step
> (at least 100 V) below the voltage at which it tripped, holding 5 min per step.
> Hold 15 min there before continuing or taking data.

> **VERIFY** — VMON follows every step and IMON stays steady.

> **STOP** — If VMON does not follow the setpoint, the output is dead: see
> Troubleshooting. If the channel trips a second time at the same value, stop: that
> value is the limit for the day. Run at the highest stable value and inform the
> detector expert.

## Troubleshooting

| Fault | Likely cause | Remedy |
| --- | --- | --- |
| Channel TRIPPED | Discharge or over-current; for the anode, breakdown in the gas gap | Section E. Do not go back to the trip voltage the same day |
| After clear trip, VMON does not follow the setpoint ('needs power cycle' on the **Controls** page) | DT1470ET output latched dead after a trip | Ramp every other channel of that supply to 0 V (hv_2: cathode, gate, anode, NaI), power-cycle the supply, clear the trip again, then restart from step 5 |
| IMON rises slowly at constant voltage | Leakage building up, onset of a discharge | Stop ramping, step back 100 V, hold and watch; inform the detector expert if it does not settle |
| Current spikes or PMT rate bursts without a trip | Micro-discharges | Stop, step back one step, hold 15 min |
| Setpoint refused: outside the permitted range | Value or sign outside channels.yaml | Check the setpoint; ranges are changed only by the detector expert |
| Setpoint refused: LOCAL mode | Supply in front-panel mode | Switch the supply to REMOTE at its front panel |
| Setpoint refused: channel disabled | Enable switch off | Flip the enable switch (VSET must be 0 V first) |
| Channel still reads ON after turn off | Ramping down at the board's rate | Wait and watch VMON; do not re-send |

## FINAL SAFE-STATE CHECK

> [!CHECKLIST]
> - All electrode channels at 0 V and OFF, VSET 0 V
> - No TRIPPED latch and no red VSET on the **Controls** page
> - Trips, their cause and the highest stable voltages recorded in LogIt
> - Table 1 updated if the operating experience changed

## Document control

| Revision | Issued | Change |
| --- | --- | --- |
| Rev. B | 2026-09-26 | Operation via the high-voltage section of the slow-control **Controls** page; limits and operating experience (Table 1); stepwise ramping with holds; changing voltages during operation; trip response and troubleshooting. Draft, not yet reviewed or approved. |
| Rev. A | 2026-08-11 | Drafted; setpoints outstanding, not yet approved for use. |
