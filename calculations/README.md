# Worked calculation index

[Calculations PDF](PTRJUN003_Lab2_Calculations.pdf). [LaTeX equation source](main.tex).

| PDF page | Topic | Numerical source |
| --- | --- | --- |
| 1 | Model, voltage/position inputs and governing equations | `config/lab_parameters.json` |
| 2 | Velocity, tail gain, interpolation and sensor calibration | `analysis/modules/identification.py` |
| 3 | Root-locus criteria, response, overshoot, settling and command | `analysis/modules/controller.py`; `matlab/design/run_root_locus_design.m` |
| 4 | Scalar bound and independent resistor-ratio tolerance | `analysis/modules/robustness.py` |
| 5 | Matched-resistor correction and bias allowance | `analysis/modules/robustness.py` |
| 6 | Screenshot calibration, tracking, overshoot and uncertainty | `analysis/modules/hardware.py` |
| 7 | Thevenin matrix, hover calibration and loaded circuit gain | `analysis/modules/robustness.py` |
| 8 | Defined actuator-bias prediction | `analysis/modules/disturbance.py` |

These are retained data and defined model predictions. Metrics are in `results/metrics.json`; processed signals and tolerance corners are saved as CSVs.
