Kitticopter Three-Op-Amp Controller — KiCad project
=====================================================

Main file:
  Kitticopter_3OpAmp_Controller.sch

This is a KiCad legacy Eeschema schematic. KiCad 6/7/8/9 can open it
directly and will offer to convert/save it as the current .kicad_sch format.

Circuit implemented from the supplied diagram:
- U1: LM741 subtractor/attenuator
    R1 = 100 kΩ
    R2 = 1 kΩ
    R3 = 100 kΩ
    R4 = 1 kΩ
    U1_OUT = 0.01(VREF - VSENSE)
- U2: LM741 non-inverting stage
    R5 = 4.7 kΩ
    R6 = 10 kΩ
    Gain = 1 + R5/R6 = 1.47
- U3: LM741 summing/bias stage
    R7 = R8 = R9 = R10 = 100 kΩ
- Bias network:
    R11 = 3.9 kΩ to GND
    P1 = 10 kΩ
    R12 = 1.2 kΩ shunt across P1
    R13 = 22 kΩ to -15 V
    P1 wiper -> R9
- Six 100 nF decoupling capacitors:
    one +15 V-to-GND and one -15 V-to-GND for each op-amp
- Supply: +15 V / GND / -15 V
- DAQ:
    DAC-1 = VREF / setpoint
    DAC-0 = VSENSE / sensor feedback
    ADC-1 = command output
    ADC-2 = sensor monitor

Calibration:
1. Set DAC-1 = DAC-0, e.g. both 4.650 V.
2. Adjust P1 until ADC-1 reads +2.500 V.
3. Keep P1 fixed during tracking.

741 hardware:
- Pin 7: +15 V
- Pin 4: -15 V
- Pins 1 and 5: offset null, leave unused
- Pin 8: NC
- Bench-supply ground and DAQ ground must be common.

Controller relationship:
    Vcommand ≈ 2.5 + 0.0143(Vref - Vsensor)

NOTE:
The schematic uses symbols from standard KiCad libraries:
Device, Connector_Generic, Amplifier_Operational.
If KiCad asks to remap legacy symbols, select the default global symbol libraries.
