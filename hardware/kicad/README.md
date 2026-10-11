# Three-op-amp controller — editable KiCad schematic

Open `Kitticopter_3OpAmp_Controller.kicad_pro` in KiCad 7 or newer, then open
the schematic. You can also open `Kitticopter_3OpAmp_Controller.kicad_sch`
directly. Keep `Controller.kicad_sym` and `sym-lib-table` beside the project.
All symbols are also embedded in the schematic.

The drawing follows the supplied reference's KiCad presentation: green wires,
red US zigzag resistors and op-amp symbols, teal component labels, and physical
pin numbers. The three LM741 symbols are mirrored so that pin 2 (inverting)
is above pin 3 (non-inverting). Their physical pin assignments are unchanged.

This redraw retains the documented three-stage circuit. The single-stage
reference image supplies the drawing style; its 120k/330-ohm values are not
used in this controller.

## Circuit and connections

| Stage | Components | Connection / nominal behaviour |
|---|---|---|
| U1 | R1/R3 100k; R2/R4 1k | DAC-1 -> R1 -> pin 3; DAC-0 -> R3 -> pin 2; V1 = 0.01(VREF - VSENSE) |
| U2 | R5 4.7k; R6 10k | V1 -> pin 3; R5 feedback; R6 to ground; V2 = 1.47 V1 |
| U3 | R7–R10 100k | V2 -> positive divider; P1 wiper -> R9 -> pin 2; output -> ADC-1 |
| Bias | R11 3.9k; P1 10k; R12 1.2k; R13 22k | GND -> R11 -> P1 -> R13 -> -15 V; R12 across P1 |
| Bypass | C1–C6 100nF | One capacitor from each supply rail to ground at each IC |

The bias-source loading is included in the nominal calculation. At zero error,
adjust P1 until the command is +2.500 V. With nominal resistors and ideal
op-amps, P1's fraction from pin 1 to the wiper is approximately 0.78308,
Rth = 5423.00 ohms, and the overall incremental gain is 0.0143219 V/V.
The physical potentiometer must be calibrated; this calculated fraction is
not a measured knob position.

The LM741 supply pins are 4 = -15 V and 7 = +15 V. Pins 1/5 are unused offset
adjustment pins; pin 8 is NC. R11's upper endpoint is ground, following the
documented LTspice source and circuit-reference image.

## Logical interface maps

J1/J2 are convenient schematic mappings, not verified physical connector
part numbers or a claim about the board's terminal ordering.

| Connector pin | Channel / rail |
|---|---|
| J1.1 | DAC-1, reference |
| J1.2 | DAC-0, sensor feedback |
| J1.3 | ADC-1, command |
| J1.4 | ADC-2, monitoring the DAC-0 sensor net |
| J1.5 | Common DAQ / bench ground |
| J2.1 | +15 V |
| J2.2 | Ground |
| J2.3 | -15 V |

## Files and verification

- `.kicad_sch`: native editable schematic; 25 components.
- `.kicad_pro`: project; `.kicad_sym` and `sym-lib-table`: local symbol library.
- `Kitticopter_3OpAmp_preview.svg`: native KiCad vector export.
- `Kitticopter_3OpAmp_preview.png`: 4200-pixel diagram for insertion in a report.
- `Kitticopter_3OpAmp_Controller.net`: KiCad-exported XML netlist.
- `BOM.csv`: resistor, capacitor, op-amp and logical connector list.
- `verify_netlist.py` and `validation.json`: connectivity and ideal DC checks.

KiCad 7.0.11 successfully parsed the schematic and exported SVG and XML.
The verification checks all 16 connected nets, all supply connections, all
feedback paths, and the nine intentionally unused offset/NC pins. This is
not a recorded KiCad ERC run or a physical-board inspection. There is no PCB
layout in this schematic package.

To repeat the checks:

```sh
kicad-cli sch export netlist --format kicadxml --output Kitticopter_3OpAmp_Controller.net Kitticopter_3OpAmp_Controller.kicad_sch
python3 verify_netlist.py
kicad-cli sch export svg --exclude-drawing-sheet --output exports Kitticopter_3OpAmp_Controller.kicad_sch
```

Project repository:
https://github.com/NateDogg247/EEE3094S---Lab-2-PTRJUN003-/tree/main/hardware/kicad

The bundled library symbols come from KiCad's official symbol libraries.
See `KiCad-symbols-COPYRIGHT.txt` for attribution and licence terms.
