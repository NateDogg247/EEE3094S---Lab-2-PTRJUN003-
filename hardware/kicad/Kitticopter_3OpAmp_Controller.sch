EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:Connector_Generic
LIBS:Amplifier_Operational
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 1 1
Title "Kitticopter Three-Op-Amp Controller"
Date "2026-10-10"
Rev "1.0"
Comp "EEE3094S Lab 2"
Comment1 "Kp ≈ 0.0143 V/V | Plant 14.2748/[s(8.1s+1)] | Sensor 0.93 V/m"
Comment2 "741 op-amps, ±15 V supplies, 100 nF decoupling at each op-amp"
Comment3 "Vcommand ≈ 2.5 + 0.0143(Vref - Vsensor)"
Comment4 "Calibrate P1 with Vref = Vsensor = 4.650 V until ADC-1 = +2.500 V"
$EndDescr
Text Notes 900 700 0    120  ~ 24
KITTICOPTER THREE-OP-AMP CONTROLLER — Kp ≈ 0.0143 V/V
Text Notes 900 950 0    60   ~ 12
Plant: 14.2748/[s(8.1s+1)]     Sensor: 0.93 V/m     Nominal overshoot: 25.1%     2% settling: 54.9 s
Text Notes 2500 1250 0    70   ~ 14
U1: SUBTRACT AND ATTENUATE ×0.01
Text Notes 6500 1250 0    70   ~ 14
U2: NON-INVERTING GAIN ×1.47
Text Notes 10300 1250 0    70   ~ 14
U3: ADD CALIBRATED +2.5 V BIAS

$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 1001
P 1250 1950
F 0 "J1" H 1168 2167 50  0000 C CNN
F 1 "DAQ INPUTS" H 1168 2076 50 0000 C CNN
	1    1250 1950
	-1 0 0 -1
$EndComp
Text Label 1500 1950 0    50   ~ 0
VREF
Text Label 1500 2050 0    50   ~ 0
VSENSE
Text Notes 900 1750 0    50   ~ 0
DAC-1: setpoint
Text Notes 900 2150 0    50   ~ 0
DAC-0: sensor feedback
Wire Wire Line
	1450 1950 2050 1950
Wire Wire Line
	1450 2050 2050 2050

$Comp
L Device:R R1
U 1 1 1101
P 2350 1950
F 0 "R1" V 2143 1950 50 0000 C CNN
F 1 "100k" V 2234 1950 50 0000 C CNN
	1    2350 1950
	0 1 1 0
$EndComp
Wire Wire Line
	2050 1950 2200 1950
Wire Wire Line
	2500 1950 2850 1950
$Comp
L Device:R R2
U 1 1 1102
P 2700 1700
F 0 "R2" H 2770 1746 50 0000 L CNN
F 1 "1k" H 2770 1655 50 0000 L CNN
	1    2700 1700
	1 0 0 -1
$EndComp
Wire Wire Line
	2700 1850 2700 1950
Wire Wire Line
	2700 1950 2850 1950
Connection ~ 2700 1950
Text Label 2700 1450 0 50 ~ 0
GND
Wire Wire Line
	2700 1550 2700 1450

$Comp
L Device:R R3
U 1 1 1103
P 2350 2150
F 0 "R3" V 2450 2150 50 0000 C CNN
F 1 "100k" V 2550 2150 50 0000 C CNN
	1    2350 2150
	0 1 1 0
$EndComp
Wire Wire Line
	2050 2050 2050 2150
Wire Wire Line
	2050 2150 2200 2150
Wire Wire Line
	2500 2150 2850 2150

$Comp
L Amplifier_Operational:LM741 U1
U 1 1 1201
P 3150 2050
F 0 "U1" H 3494 2096 50 0000 L CNN
F 1 "LM741" H 3494 2005 50 0000 L CNN
	1    3150 2050
	1 0 0 -1
$EndComp
Wire Wire Line
	3450 2050 3900 2050
Text Label 3550 2050 0 50 ~ 0
U1_OUT
$Comp
L Device:R R4
U 1 1 1104
P 3200 2450
F 0 "R4" V 2993 2450 50 0000 C CNN
F 1 "1k" V 3084 2450 50 0000 C CNN
	1    3200 2450
	0 1 1 0
$EndComp
Wire Wire Line
	2850 2150 2850 2450
Wire Wire Line
	2850 2450 3050 2450
Wire Wire Line
	3350 2450 3700 2450
Wire Wire Line
	3700 2450 3700 2050
Connection ~ 3700 2050
Text Notes 2600 2750 0 50 ~ 0
U1_OUT = 0.01(VREF − VSENSE)

Text Label 3050 1650 0 50 ~ 0
+15V
Text Label 3050 2450 2 50 ~ 0
-15V

Wire Wire Line
	3900 2050 6450 2050

$Comp
L Amplifier_Operational:LM741 U2
U 1 1 1202
P 6750 2050
F 0 "U2" H 7094 2096 50 0000 L CNN
F 1 "LM741" H 7094 2005 50 0000 L CNN
	1    6750 2050
	1 0 0 -1
$EndComp
Wire Wire Line
	7050 2050 7550 2050
Text Label 7150 2050 0 50 ~ 0
U2_OUT
$Comp
L Device:R R5
U 1 1 1301
P 6750 2500
F 0 "R5" V 6543 2500 50 0000 C CNN
F 1 "4.7k" V 6634 2500 50 0000 C CNN
	1    6750 2500
	0 1 1 0
$EndComp
Wire Wire Line
	6450 2150 6250 2150
Wire Wire Line
	6250 2150 6250 2500
Wire Wire Line
	6250 2500 6600 2500
Wire Wire Line
	6900 2500 7350 2500
Wire Wire Line
	7350 2500 7350 2050
Connection ~ 7350 2050
$Comp
L Device:R R6
U 1 1 1302
P 6100 2450
F 0 "R6" H 6170 2496 50 0000 L CNN
F 1 "10k" H 6170 2405 50 0000 L CNN
	1    6100 2450
	1 0 0 -1
$EndComp
Wire Wire Line
	6100 2300 6100 2150
Wire Wire Line
	6100 2150 6250 2150
Connection ~ 6250 2150
Text Label 6100 2750 0 50 ~ 0
GND
Wire Wire Line
	6100 2600 6100 2750
Text Notes 6500 2850 0 50 ~ 0
Gain = 1 + 4.7k/10k = 1.47
Text Label 6650 1650 0 50 ~ 0
+15V
Text Label 6650 2450 2 50 ~ 0
-15V

$Comp
L Device:R R7
U 1 1 1401
P 9000 1950
F 0 "R7" V 8793 1950 50 0000 C CNN
F 1 "100k" V 8884 1950 50 0000 C CNN
	1    9000 1950
	0 1 1 0
$EndComp
Wire Wire Line
	7550 2050 8300 2050
Wire Wire Line
	8300 2050 8300 1950
Wire Wire Line
	8300 1950 8850 1950
Wire Wire Line
	9150 1950 9900 1950
$Comp
L Device:R R8
U 1 1 1402
P 9600 1650
F 0 "R8" H 9670 1696 50 0000 L CNN
F 1 "100k" H 9670 1605 50 0000 L CNN
	1    9600 1650
	1 0 0 -1
$EndComp
Wire Wire Line
	9600 1800 9600 1950
Wire Wire Line
	9600 1950 9900 1950
Connection ~ 9600 1950
Text Label 9600 1400 0 50 ~ 0
GND
Wire Wire Line
	9600 1500 9600 1400

$Comp
L Device:R R9
U 1 1 1403
P 9000 2150
F 0 "R9" V 9100 2150 50 0000 C CNN
F 1 "100k" V 9200 2150 50 0000 C CNN
	1    9000 2150
	0 1 1 0
$EndComp
Text Label 8300 2150 0 50 ~ 0
WIPER
Wire Wire Line
	8300 2150 8850 2150
Wire Wire Line
	9150 2150 9900 2150

$Comp
L Amplifier_Operational:LM741 U3
U 1 1 1203
P 10200 2050
F 0 "U3" H 10544 2096 50 0000 L CNN
F 1 "LM741" H 10544 2005 50 0000 L CNN
	1    10200 2050
	1 0 0 -1
$EndComp
Wire Wire Line
	10500 2050 11250 2050
Text Label 10700 2050 0 50 ~ 0
COMMAND
$Comp
L Device:R R10
U 1 1 1404
P 10200 2500
F 0 "R10" V 9993 2500 50 0000 C CNN
F 1 "100k" V 10084 2500 50 0000 C CNN
	1    10200 2500
	0 1 1 0
$EndComp
Wire Wire Line
	9900 2150 9700 2150
Wire Wire Line
	9700 2150 9700 2500
Wire Wire Line
	9700 2500 10050 2500
Wire Wire Line
	10350 2500 10900 2500
Wire Wire Line
	10900 2500 10900 2050
Connection ~ 10900 2050
Text Label 10100 1650 0 50 ~ 0
+15V
Text Label 10100 2450 2 50 ~ 0
-15V
Text Notes 9900 2850 0 50 ~ 0
VCOMMAND ≈ 2.5 + 0.0143(VREF − VSENSE)

$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 1501
P 12150 2050
F 0 "J2" H 12230 2042 50 0000 L CNN
F 1 "DAQ MONITOR" H 12230 1951 50 0000 L CNN
	1    12150 2050
	1 0 0 -1
$EndComp
Wire Wire Line
	11250 2050 11950 2050
Text Notes 12250 2050 0 50 ~ 0
ADC-1: command output
Text Label 11400 2050 0 50 ~ 0
COMMAND
Text Label 11400 2150 0 50 ~ 0
VSENSE
Wire Wire Line
	11400 2150 11950 2150
Text Notes 12250 2250 0 50 ~ 0
ADC-2: sensor monitor

Text Notes 1750 3550 0 70 ~ 14
BIAS POTENTIOMETER (NO BUFFER)
$Comp
L Device:R R11
U 1 1 1601
P 3000 4050
F 0 "R11" H 3070 4096 50 0000 L CNN
F 1 "3.9k" H 3070 4005 50 0000 L CNN
	1    3000 4050
	1 0 0 -1
$EndComp
Text Label 3000 3750 0 50 ~ 0
GND
Wire Wire Line
	3000 3750 3000 3900
Wire Wire Line
	3000 4200 3000 4400
Text Label 3000 4400 0 50 ~ 0
BIAS_TOP

$Comp
L Device:R_Potentiometer P1
U 1 1 1602
P 3000 4850
F 0 "P1" H 2930 4896 50 0000 R CNN
F 1 "10k" H 2930 4805 50 0000 R CNN
	1    3000 4850
	1 0 0 -1
$EndComp
Wire Wire Line
	3000 4700 3000 4400
Wire Wire Line
	3000 5000 3000 5300
Text Label 3000 5300 0 50 ~ 0
BIAS_BOT
Wire Wire Line
	3150 4850 3900 4850
Text Label 3400 4850 0 50 ~ 0
WIPER

$Comp
L Device:R R12
U 1 1 1603
P 2450 4850
F 0 "R12" H 2520 4896 50 0000 L CNN
F 1 "1.2k" H 2520 4805 50 0000 L CNN
	1    2450 4850
	1 0 0 -1
$EndComp
Wire Wire Line
	2450 4700 2450 4400
Wire Wire Line
	2450 4400 3000 4400
Connection ~ 3000 4400
Wire Wire Line
	2450 5000 2450 5300
Wire Wire Line
	2450 5300 3000 5300
Connection ~ 3000 5300

$Comp
L Device:R R13
U 1 1 1604
P 3000 5650
F 0 "R13" H 3070 5696 50 0000 L CNN
F 1 "22k" H 3070 5605 50 0000 L CNN
	1    3000 5650
	1 0 0 -1
$EndComp
Wire Wire Line
	3000 5300 3000 5500
Text Label 3000 5950 0 50 ~ 0
-15V
Wire Wire Line
	3000 5800 3000 5950

Text Notes 4200 4250 0 60 ~ 12
CALIBRATION
Text Notes 4200 4500 0 50 ~ 0
1. Set DAC-1 = DAC-0 (example: both 4.650 V).
Text Notes 4200 4750 0 50 ~ 0
2. Adjust P1 until ADC-1 reads +2.500 V.
Text Notes 4200 5000 0 50 ~ 0
3. Keep P1 fixed during tracking.
Text Notes 4200 5250 0 50 ~ 0
R12 = 1.2 kΩ is connected across the full 10 kΩ pot.
Text Notes 4200 5500 0 50 ~ 0
Wiper feeds R9 → U3 inverting input.

Text Notes 8100 3650 0 70 ~ 14
POWER AND DECOUPLING
$Comp
L Connector_Generic:Conn_01x03 J3
U 1 1 1701
P 8450 4150
F 0 "J3" H 8368 4467 50 0000 C CNN
F 1 "BENCH SUPPLY" H 8368 4376 50 0000 C CNN
	1    8450 4150
	-1 0 0 -1
$EndComp
Text Label 8750 4050 0 50 ~ 0
+15V
Text Label 8750 4150 0 50 ~ 0
GND
Text Label 8750 4250 0 50 ~ 0
-15V
Wire Wire Line
	8650 4050 9200 4050
Wire Wire Line
	8650 4150 9200 4150
Wire Wire Line
	8650 4250 9200 4250

$Comp
L Device:C C1
U 1 1 1801
P 9850 4150
F 0 "C1" H 9965 4196 50 0000 L CNN
F 1 "100n" H 9965 4105 50 0000 L CNN
	1    9850 4150
	1 0 0 -1
$EndComp
Text Label 9850 3900 0 50 ~ 0
+15V
Text Label 9850 4400 0 50 ~ 0
GND
Wire Wire Line
	9850 3900 9850 4000
Wire Wire Line
	9850 4300 9850 4400
$Comp
L Device:C C2
U 1 1 1802
P 10500 4150
F 0 "C2" H 10615 4196 50 0000 L CNN
F 1 "100n" H 10615 4105 50 0000 L CNN
	1    10500 4150
	1 0 0 -1
$EndComp
Text Label 10500 3900 0 50 ~ 0
-15V
Text Label 10500 4400 0 50 ~ 0
GND
Wire Wire Line
	10500 3900 10500 4000
Wire Wire Line
	10500 4300 10500 4400
Text Notes 9750 4650 0 50 ~ 0
U1 decoupling

$Comp
L Device:C C3
U 1 1 1803
P 11400 4150
F 0 "C3" H 11515 4196 50 0000 L CNN
F 1 "100n" H 11515 4105 50 0000 L CNN
	1    11400 4150
	1 0 0 -1
$EndComp
Text Label 11400 3900 0 50 ~ 0
+15V
Text Label 11400 4400 0 50 ~ 0
GND
Wire Wire Line
	11400 3900 11400 4000
Wire Wire Line
	11400 4300 11400 4400
$Comp
L Device:C C4
U 1 1 1804
P 12050 4150
F 0 "C4" H 12165 4196 50 0000 L CNN
F 1 "100n" H 12165 4105 50 0000 L CNN
	1    12050 4150
	1 0 0 -1
$EndComp
Text Label 12050 3900 0 50 ~ 0
-15V
Text Label 12050 4400 0 50 ~ 0
GND
Wire Wire Line
	12050 3900 12050 4000
Wire Wire Line
	12050 4300 12050 4400
Text Notes 11300 4650 0 50 ~ 0
U2 decoupling

$Comp
L Device:C C5
U 1 1 1805
P 13000 4150
F 0 "C5" H 13115 4196 50 0000 L CNN
F 1 "100n" H 13115 4105 50 0000 L CNN
	1    13000 4150
	1 0 0 -1
$EndComp
Text Label 13000 3900 0 50 ~ 0
+15V
Text Label 13000 4400 0 50 ~ 0
GND
Wire Wire Line
	13000 3900 13000 4000
Wire Wire Line
	13000 4300 13000 4400
$Comp
L Device:C C6
U 1 1 1806
P 13650 4150
F 0 "C6" H 13765 4196 50 0000 L CNN
F 1 "100n" H 13765 4105 50 0000 L CNN
	1    13650 4150
	1 0 0 -1
$EndComp
Text Label 13650 3900 0 50 ~ 0
-15V
Text Label 13650 4400 0 50 ~ 0
GND
Wire Wire Line
	13650 3900 13650 4000
Wire Wire Line
	13650 4300 13650 4400
Text Notes 12900 4650 0 50 ~ 0
U3 decoupling

Text Notes 8100 5200 0 60 ~ 12
741 PIN / WIRING NOTES
Text Notes 8100 5450 0 50 ~ 0
Pin 7 = +15 V; pin 4 = −15 V.
Text Notes 8100 5700 0 50 ~ 0
Pins 1 and 5 (offset null) and pin 8 (NC) are left unconnected.
Text Notes 8100 5950 0 50 ~ 0
Use common ground between bench supply and DAQ.
Text Notes 8100 6200 0 50 ~ 0
Place each 100 nF capacitor physically close to its op-amp supply pin.

Text Notes 1750 6800 0 70 ~ 14
FUNCTIONAL SUMMARY
Text Notes 1750 7100 0 55 ~ 0
U1 forms a difference amplifier with matched 100k/1k ratios: U1_OUT = 0.01(VREF − VSENSE).
Text Notes 1750 7400 0 55 ~ 0
U2 is non-inverting: gain = 1 + R5/R6 = 1.47.
Text Notes 1750 7700 0 55 ~ 0
U3 combines U2 output with the calibrated bias. With P1 set correctly, VCOMMAND ≈ 2.5 + Kp(VREF − VSENSE).
Text Notes 1750 8000 0 55 ~ 0
Nominal component values produce Kp ≈ 0.0143 V/V in the complete loaded circuit.

$EndSCHEMATC
