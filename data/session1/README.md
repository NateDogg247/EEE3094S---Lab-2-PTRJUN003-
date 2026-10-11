# Source record

`PTRJUN003_raw.csv` is copied byte-for-byte from uploaded `PTRJUN003(1).csv`.

There are 1,634 rows and one clock reset after row 31. The first 31 rows show no motion. The analysis retains the 1,603-row monotonic run starting at 0.1 s. Only one 2.5 V identification step is present. The reset is not counted as a repeated step test.

Use Output(m) for identification. Output(v) clips at 10 V. The speed column is cross-checked but velocity is independently recomputed from position differences. Five empty trailing columns are not used.

The reattached PTRJUN003(2).csv is byte-identical to PTRJUN003_raw.csv, so it is not another trial. `evidence/step_test_circuit_original.png` records the 15 V / 10k series resistor / 10k potentiometer / ADC setup; the report redraws it as a vector. `evidence/parameter_check.png` records submitted A=14.2748, tau=8.1 and sensor=0.93, scored 100%, 96% and 100%. The measured finite input transition is retained, and its effect is checked with an additional first-order integration.
