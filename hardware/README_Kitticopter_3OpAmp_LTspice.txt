Kitticopter 3-op-amp controller - LTspice
=========================================

Main schematic:
  Kitticopter_3OpAmp_Controller.asc

What is reproduced from the supplied diagram
---------------------------------------------
U1 subtract/attenuate stage:
  R1 = 100k
  R2 = 1k
  R3 = 100k
  R4 = 1k
  U1 output = 0.01*(VREF - VSENSE)

U2 non-inverting stage:
  R5 = 4.7k
  R6 = 10k
  Gain = 1 + 4.7k/10k = 1.47

U3 level-shift / command stage:
  R7 = R8 = R9 = R10 = 100k
  Adds the calibrated +2.5 V command bias.

Bias network:
  R11 = 3.9k to ground
  P1 = 10k potentiometer
  R12 = 1.2k shunt across the full potentiometer
  R13 = 22k to -15 V
  The pot is represented in LTspice by two resistors P1_TOP and P1_BOT.

Nominal pot setting:
  .param W=0.7830806

At VREF = VSENSE = 4.650 V, this gives approximately:
  WIPER = -2.500 V
  COMMAND = +2.500 V

The effective small-signal proportional gain is approximately:
  Kp = 0.0143219 V/V

This is slightly below 0.01*1.47 = 0.0147 because the U3 bias-wiper
network is loaded through R9, exactly as in the supplied circuit.

Power and op-amps
-----------------
Three UniversalOpamp2 blocks are configured with approximate 741 dynamics:
  Avol = 200k
  GBW = 1 MHz
  Slew = 0.5 V/us
  Current limit = 25 mA
  Output rail headroom = 2 V

Hardware reminder for a 741:
  pin 7 = +15 V
  pin 4 = -15 V
  pins 1, 5 and 8 left unconnected for this design

There are six 100 nF decoupling capacitors in the schematic:
  one from +15 V to ground and one from -15 V to ground at each op-amp.

How to use
----------
1. Open Kitticopter_3OpAmp_Controller.asc in LTspice.
2. Run the included .op operating-point simulation.
3. Probe COMMAND and WIPER.
4. For calibration, keep VREF_SRC = VSENSE_SRC = 4.65 V.
5. If required, edit .param W slightly until COMMAND is exactly 2.500 V.
6. In hardware, this corresponds to turning P1 while watching ADC-1.

DAQ labels
----------
VREF     : DAC-1 setpoint
VSENSE   : DAC-0 / sensor-feedback signal; ADC-2 can monitor this node
COMMAND  : ADC-1 / controller command output

Plant information from the diagram
----------------------------------
Gpos(s) = 14.2748 / [ s(8.1s + 1) ]
Sensor gain = 0.93 V/m

The plant is not inserted into this controller-only schematic; COMMAND is
left as the output test point so it can be connected to your plant model or DAQ.
