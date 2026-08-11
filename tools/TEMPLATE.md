---
sop: SOP-0XX
title: Short Procedure Name
subtitle: One line saying what the procedure is for
revision: Rev. A
author: Auke-Pieter Colijn
date: 1 January 2026
location: Nikhef - XAMS
status: Initial release
---

> [!NOTE]
> **Work discipline:** Record every valve operation, configuration change,
> bottle mass, pressure, temperature and integrated-flow value in the
> electronic LogIt logbook.

## Hazards

Signal words follow ISO 3864-2 / ANSI Z535.6 and are chosen by the severity of
the consequence: DANGER (imminent, death or serious injury), WARNING (could
cause death or serious injury), CAUTION (minor or moderate injury), NOTICE
(equipment damage only, nobody is hurt). Each message reads hazard and source in
bold, then consequence, then how to avoid it.

> [!DANGER]
> **Hazard and its source, in bold, on the first line.**
> What happens to the person if it is not avoided.
> What the operator must do to avoid it.

> [!WARNING]
> **Cryogenic burn - uninsulated LN2 line.**
> Contact with a cold surface destroys tissue within seconds.
> Wear cryogenic gloves and a face shield before touching any line.

> [!NOTICE]
> Property damage only, so no bold hazard line and no triangle.
> Say what breaks and what prevents it.

## A. Preconditions and preparation

### 1. First thing the operator does

> **ACTION** — What to do, in the imperative. Several sentences are fine.
> Wrap the text across lines; the renderer re-flows it.

> **VERIFY** — The observable state that proves the action succeeded.

> **STOP** — The condition under which the operator must not continue.

### 2. Second thing

> **ACTION** — ...

> **VERIFY** — ...

> [!NOTE]
> A NOTE callout carries background information that is not itself a step.

## B. Main procedure

### 3. A step with a reference table

> **ACTION** — Set the valves to the configuration below.

| Valve / item | Required state |
| --- | --- |
| V1-V14 | CLOSED |
| V17 regulator | FULLY CLOSED - turn counter-clockwise |

### 4. A step with an operator cue

> **ACTION** — Start the transfer and watch the temperatures.

> [!CUE]
> **OPERATOR CUE**
>
> | | |
> | --- | --- |
> | **Indication** | TT203/TT204/TT205 temperature drop |
> | **Immediate response** | Switch ON emergency cooling |

### 5. A step with a figure

> **ACTION** — Compare the reading with the reference trace.

![Reference trace during a nominal fill](figs/example.png){width=70%}

## C. Completion

> **ACTION** — Final safe state.

> **NOTE** — What to record in LogIt before closing the procedure.

> [!CHECKLIST]
> - What must be true before the procedure is closed
> - What must be recorded in LogIt
