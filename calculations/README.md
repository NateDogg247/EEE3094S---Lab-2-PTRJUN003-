# Worked calculation index

[Calculations PDF](PTRJUN003_Lab2_Calculations.pdf). [LaTeX equation source](main.tex).

| PDF page | Topic | Numerical source |
| --- | --- | --- |
| 1 | Adopted model, voltage/position inputs and governing definitions | `config/lab_parameters.json` |
| 2 | Model derivation, units, final-value theorem and input-bias offset | `report/sections/model_calculations.tex` |
| 3 | Velocity, tail gain, interpolation and sensor calibration | `analysis/modules/identification.py` |
| 4 | Root-locus poles, asymptotes, breakaway and overshoot bound | `matlab/design/run_root_locus_design.m` |
| 5 | Selected gain, pole calculations and angle/magnitude criteria | `matlab/design/run_root_locus_design.m` |
| 6 | Response, peak, overshoot, settling and command headroom | `analysis/modules/controller.py` |
| 7 | Scalar gain bound and independent resistor-ratio tolerance | `analysis/modules/robustness.py` |
| 8 | Matched-resistor correction and bias allowance | `analysis/modules/robustness.py` |
| 9 | Screenshot calibration, tracking, overshoot and uncertainty | `analysis/modules/hardware.py` |
| 10 | Thevenin matrix, hover calibration and loaded circuit gain | `analysis/modules/robustness.py` |
| 11 | Defined actuator-bias prediction | `analysis/modules/disturbance.py` |

The model and root-locus derivations are shared LaTeX fragments under `report/sections`, included by both PDFs. These are retained data and defined model predictions. Metrics are in `results/metrics.json`; processed signals and tolerance corners are saved as CSVs.
