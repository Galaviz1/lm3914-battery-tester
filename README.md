# LM3914 Li-ion Battery Tester

A no-microcontroller **18650 Li-ion state-of-charge meter**. An **LM3914** lights a
**2510SR-1 10-segment bargraph** in **bar mode**, mapping the cell voltage from
**3.0 V (empty)** to **4.2 V (full)** across the ten segments — one segment ≈ 10 %.

> A **Paradox Transistor Lab** project. Pure analog: ten comparators and a
> reference, no firmware, no ADC.

## How it works

The LM3914 holds an internal string of ten comparators tapped across a reference
window between **RLO (pin 4)** and **RHI (pin 6)**. Segment *n* turns on when the
signal on **SIG (pin 5)** rises past `RLO + (n/10)·(RHI − RLO)`. Tie **MODE
(pin 9) to V+** and the segments fill cumulatively like a fuel gauge.

Each LED output is a **constant-current sink** (set once by the reference), so the
bargraph needs **no series resistors** — that is the whole point of the chip.

## The one constraint that shapes the design

The LM3914 signal input (pin 5) is only valid from **0 V to (V+ − 1.5 V)**. A
4.2 V cell fed straight in would need V+ ≥ 5.7 V. Instead we run the chip from
**5 V (USB)** and drop the cell voltage with a **÷3.4 input divider** so the
signal lands comfortably in range *and* near the 1.25 V reference:

| Cell voltage | After ÷3.4 divider (→ pin 5) |
|---:|---:|
| 4.20 V (full)  | 1.235 V |
| 3.00 V (empty) | 0.882 V |

Divider: `24 kΩ` (cell+ → SIG) and `10 kΩ` (SIG → GND), 1 % metal film.
Ratio = 10 / 34 = 0.294. (For lower self-drain use `240 kΩ / 100 kΩ` — same
ratio, ~12 µA instead of ~120 µA at 4.2 V.) A `100 nF` cap SIG→GND steadies the
reading.

## Pin wiring (LM3914, 18-pin DIP)

| Pin | Name | Connect to |
|---:|---|---|
| 1 | LED 1 (bottom seg) | bargraph seg 1 cathode |
| 2 | V− | GND |
| 3 | V+ | **+5 V** (USB), 2.2–10 µF + 0.1 µF to GND |
| 4 | **RLO** | wiper of **TRIM-LO** (set ≈ 0.882 V) |
| 5 | **SIG** | input divider tap (cell ÷ 3.4) |
| 6 | **RHI** | wiper of **TRIM-HI** (set ≈ 1.235 V) |
| 7 | REF OUT | top of both trimpots (1.25 V reference) |
| 8 | REF ADJ | `R_prog` 1.2 kΩ → GND (sets LED current ≈ 10 mA) |
| 9 | MODE | **V+** → bar mode |
| 10 | LED 10 (top seg) | bargraph seg 10 cathode |
| 11–18 | LED 9 … LED 2 | bargraph segs 9 … 2 cathodes |

**Segment → output pin** (segment 1 = lowest voltage):

| Seg | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Pin | 1 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 10 |

### Reference / window network
- `R_prog` **1.2 kΩ** from REF ADJ (8) to GND → LED current ≈ 12.5 / 1.2 k ≈ **10 mA** per segment.
- **TRIM-HI** 10 kΩ trimpot: top → REF OUT (7), wiper → RHI (6), bottom → GND.
- **TRIM-LO** 10 kΩ trimpot: top → REF OUT (7), wiper → RLO (4), bottom → GND.

### Bargraph (2510SR-1)
10 LEDs in a DIP package. **Common anodes → V+ (5 V)**; each **cathode → its
LM3914 output** per the table above. No resistors.

## Calibration (bench supply on the input terminals)

1. Set MODE confirmed to V+ (bar mode), power the board from USB 5 V.
2. Feed **4.20 V** into the cell input. Adjust **TRIM-HI** until **segment 10
   just lights**.
3. Feed **3.00 V**. Adjust **TRIM-LO** until **segment 1 just lights** (segments
   2–10 off).
4. Repeat 2–3 once — the two adjustments interact slightly.
5. Optional: tweak `R_prog` for brightness (smaller = brighter, more current).

## Bill of materials

| Qty | Part | Value / notes |
|---:|---|---|
| 1 | LM3914N | dot/bar display driver, 18-pin DIP |
| 1 | 2510SR-1 | 10-segment LED bargraph (red) |
| 1 | R (divider top) | 24 kΩ 1 % (or 240 kΩ) |
| 1 | R (divider bottom) | 10 kΩ 1 % (or 100 kΩ) |
| 1 | R_prog | 1.2 kΩ |
| 2 | Trimpot | 10 kΩ (multiturn preferred) |
| 1 | Cap | 2.2–10 µF electrolytic (V+ bypass) |
| 2 | Cap | 100 nF (V+ and SIG) |
| — | 18650 holder / clip leads | cell under test |

## Why not direct-drive or a 9 V supply?

- **SIG direct at 5 V** breaks the `V+ − 1.5 V` input limit at the top of the
  range (4.2 V > 3.5 V) → upper segments misread. The divider fixes this.
- **9 V supply + SIG direct** is in range but dissipates ~0.7 W in the driver at
  full bar (V+ − V_LED across each sink); you'd then need to run the bargraph
  anodes off a lower rail. The 5 V + divider path avoids all of that.

---

*Part of the **Paradox Transistor Lab** by
[@Galaviz1](https://github.com/Galaviz1). Related: [`tp4056-lcd-gauge`] (the
microcontroller + LCD take on the same idea).*
