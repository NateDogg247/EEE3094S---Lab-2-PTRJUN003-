# Controller design basis

This revision uses the supplied LTspice source, KiCad source and circuit-reference image rather than the incomplete bias reconstruction in the first report. The board photograph records physical assembly; the design files do not independently verify its solder-side netlist or actual measured component values.

## Documented circuit

- U1: R1 (reference input) and R3 (sensor input) = 100 kohm; R2 (positive-input shunt) and R4 (feedback) = 1 kohm. Sensor DAC-0 is inverting, reference DAC-1 non-inverting.
- U2: R5 feedback = 4.7 kohm, R6 ground = 10 kohm. Gain 1.47.
- U3: R7-R10 = 100 kohm. U2 enters the positive divider; P1 wiper enters R9 on the negative side. ADC-1 receives U3 output.
- ADC-2 monitors DAC-0 sensor feedback.
- Bias: R11 = 3.9 kohm to ground; P1 = 10 kohm; R12 = 1.2 kohm across the full pot; R13 = 22 kohm to -15 V.
- Three 741-type stages with +15/-15 V rails and common DAQ ground. The design includes six 100 nF decoupling capacitors, one rail-to-ground capacitor per rail per op-amp. Physical device markings and capacitor connections require board verification.

The supplied KiCad file/README labelled R11 at +15 V. The supplied LTspice source and circuit image put R11 at ground. The bundled KiCad copy corrects that endpoint label to ground. The original Library artifact is unchanged.

## Equations

`a_f=R4/R3`, `a_r=(1+a_f)*R2/(R1+R2)`, `V1=a_r*r_v-a_f*y_v`.

`g2=1+R5/R6`, `V2=g2*V1`.

For the unbuffered bias source `Vth`, `Rth`, define `r=R10/(R9+Rth)`. Then `g3=(1+r)*R8/(R7+R8)` and `u=g3*V2-r*Vth`.

Calibration at equal reference/sensor gives W=0.783080594, open-circuit Vth=-2.635575036 V, Rth=5423.001448 ohm and loaded output 2.500 V. Thus g3=0.97427980 and Kp=0.014321913 V/V, consistent with the supplied Simulink value 0.01432.

The full derivation, schematic, bias network and pin/DAQ mapping are in Appendix D. Independent loop-resistor tolerance results hold the bias network nominal and assume hover recalibration. Their failures already rule out an all-component guarantee.
