# Code and calculation guide

Python generates the report figures and numerical results. MATLAB implements independent identification, root-locus and controller checks. Code is separated by task.

## Shared inputs

[config/lab_parameters.json](config/lab_parameters.json) stores the adopted plant, sensor and controller parameters. [Python](analysis/modules/parameters.py) and [MATLAB](matlab/config/lab_parameters.m) read the same file.

Measured inputs are separate: the original CSV in `data/session1` and hardware display in `data/session2`. Screenshot readouts and pixel calibration are in the hardware module because they describe a particular experiment.

Identification uses a 2.5 to 5.0 V actuator step, increment 2.5 V. The nominal controller test is a 0 to 5 m position reference. These signals have different units and roles.

## Python modules

| File | Calculation/output |
| --- | --- |
| [analyse.py](analysis/analyse.py) | Short launcher |
| [pipeline.py](analysis/modules/pipeline.py) | Runs the stages and combines their metrics |
| [parameters.py](analysis/modules/parameters.py) | Loads shared physical parameters |
| [identification.py](analysis/modules/identification.py) | Time resets, position derivative, tail gain, 63.2% interpolation, fitted time constant, sensor calibration and model validation |
| [controller.py](analysis/modules/controller.py) | Characteristic equation, poles, root locus, overshoot, peak time, settling and command |
| [robustness.py](analysis/modules/robustness.py) | Aerodynamic uncertainty, circuit Thevenin calculation, scalar corners, 2,048 resistor/drag corners and gain correction |
| [hardware.py](analysis/modules/hardware.py) | Digitised response, tracking, peak, overshoot and pixel resolution |
| [simulink_evidence.py](analysis/modules/simulink_evidence.py) | Replots the supplied scope and reconstructs its actual 2.5-to-5 m reference sequence |
| [disturbance.py](analysis/modules/disturbance.py) | Defined +2 mV bias prediction and tracking allowance |
| [plot_style.py](analysis/modules/plot_style.py) | Figure styling and PDF/PNG export |

From the project root:

```text
python -m pip install -r requirements.txt
python analysis/analyse.py
```

The launcher calls all modules; they do not need to be run individually. CSV/JSON outputs go to `results`, and plots go to `report/figures`.

## MATLAB modules

| File | Purpose |
| --- | --- |
| [run_all.m](matlab/run_all.m) | Identification, root locus and validation; builds Simulink model if licensed |
| [design/run_root_locus_design.m](matlab/design/run_root_locus_design.m) | Full geometry, angle/magnitude, gain limits, response and scalar uncertainty calculations |
| [identification/identify_session1.m](matlab/identification/identify_session1.m) | Finite-difference identification and sensor fit |
| [validation/verify_nominal_controller.m](matlab/validation/verify_nominal_controller.m) | Independent original controller check |
| [simulink/create_simulink_model.m](matlab/simulink/create_simulink_model.m) | Saves the sensor-scaled, hover-biased nominal model |
| [plots/plot_report_figures.m](matlab/plots/plot_report_figures.m) | MATLAB counterparts of every numerical report figure, with PDF/PNG exports |
| [simulink/run_simulink_tests.m](matlab/simulink/run_simulink_tests.m) | Executes both reference sequences and exports native solver logs |
| [config/lab_parameters.m](matlab/config/lab_parameters.m) | Reads shared parameters |

On Windows:

1. Extract the entire ZIP.
2. Start MATLAB with Control System Toolbox.
3. Set Current Folder to the extracted `matlab` directory.
4. Enter `run_all`, or `addpath(genpath(pwd)); run_root_locus_design(lab_parameters)` for only that method.

Outputs are saved in `results/matlab`. Call the canonical functions in the design, validation and Simulink folders. Simulink is required for native model creation and simulation.

The builder reconstructs the architecture; it is not an uploaded original DAQ model and does not collect experimental data. MATLAB was unavailable here. Its equations were checked independently in Python; a MATLAB execution is not claimed.

## Worked calculations

Read [the calculations PDF](calculations/PTRJUN003_Lab2_Calculations.pdf) and [topic index](calculations/README.md). Corresponding equations also appear in the report's circuit-loading appendix and Appendix C.

The supplement shows formulas, substitutions, units and interpretation for identification, sensor calibration, root-locus geometry, pole/gain selection, response metrics, circuit loading, tolerances, measured tracking, overshoot and disturbance bias.

## Report source and verification

`main.tex` is the root entry point. Files in `report/sections` separate the body, references, appendices and shared supplement calculations. `report/main.tex` defines the appearance, and `report/repository.tex` defines GitHub destinations.

The report has 9 main pages and 3 appendix pages; 15 PDF pages in total. Title, contents, lists, references and appendices are excluded. The complete PDF is limited to 15 pages, including cover, contents, references and appendices. Physical photos and the required controller-tracking screenshot remain in the appendices. The main report includes the supplied Simulink architecture, its Python-replotted results and the enlarged KiCad stage panels. Numerical figures and captions link their GitHub source folders.

The modular Python pipeline reproduces the saved metrics exactly. The PDF check verifies page count, internal destinations, GitHub URI destinations and matching project paths. Run the full build with:

```bash
bash scripts/build.sh
```

Nominal settling remains 54.89 s, and independent component tolerance is not fully met. No repeated experiments or unexecuted MATLAB outputs are presented as measured evidence.

## Reported potentiometer adjustment

`data/session2/test_conditions.json` preserves the student's connected-controller setup and approximately 2.565 V input observation. `report/sections/test_adjustment_calculations.tex` supplies the extended calculation supplement; the essential result appears in Appendix C. It distinguishes that observation from a zero-error hover bias, and compares it with the predicted initial command and reconstructed scope sequence.

The identification module also exports `step_input_transition` and solves the first-order model with the recorded manual transition. MATLAB `plot_report_figures` reproduces this using `ode45`. `hardware/kicad/export_report_panels.py` creates enlarged SVG/PDF views from a native KiCad export. Parameter-check evidence is in `data/session1/evidence`.
