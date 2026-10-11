# EEE3094S Lab 2 — PTRJUN003

Junaid Allan Pieters — Proportional Control of the Kitticopter, University of Cape Town.

The report follows the four required sections: System Modelling, System Identification, Controller Design and Controller Tests. Full identification calculations remain in the standalone supplement. The supplied Simulink model and enlarged KiCad stages are in the main text, with the original scope retained in the appendix. Numerical plots are rendered by Python and have MATLAB reproduction code. Figures and cross-references link directly to the supporting GitHub folders.

## Project map

| Folder | Contents |
| --- | --- |
| [config](config) | Shared physical parameters read by Python and MATLAB |
| [analysis](analysis) | Python launcher and separate numerical modules |
| [matlab](matlab) | Launchers, identification, design, validation and Simulink code |
| [calculations](calculations) | Worked calculation PDF, equation source and topic index |
| [data/session1](data/session1) | Original identification CSV |
| [data/session2](data/session2) | Supplied experimental and Simulink screenshots |
| [data/rubric](data/rubric) | Original supplied marking rubric images |
| [hardware](hardware) | Circuit sources, component information and board photograph |
| [results](results) | Processed data, numerical traces, uncertainty corners and metrics |
| [report](report) | LaTeX source, figures and compiled report |
| [scripts](scripts) | Build, link configuration, source listing and PDF verification |

## Run Python

From the project root:

```text
python -m pip install -r requirements.txt
python analysis/analyse.py
```

The launcher runs identification, nominal controller analysis, robustness, hardware digitisation, disturbance prediction and the supplied Simulink reference-sequence comparison in order. It writes results and report plots.

## Run MATLAB

Download/extract the entire project. In MATLAB, set Current Folder to `matlab`, then run:

```matlab
run_all
```

For the detailed root locus method alone:

```matlab
addpath(genpath(pwd));
run_root_locus_design(lab_parameters)
```

Control System Toolbox is required. Simulink is required for the model builder and native test runner. The standalone `plot_report_figures` uses analytical formulas without Control System Toolbox. MATLAB source is supplied but was not executed in the authoring environment; Python reproduced the saved numerical results.

## Build the PDFs

With Python, Bash and a LaTeX distribution containing `latexmk`, TikZ and Circuitikz:

```bash
bash scripts/build.sh
```

For LaTeX-only compilation, select the root `main.tex` in Overleaf. The calculation supplement compiles from `calculations/main.tex` in that directory with a local LaTeX editor.

## Model and retained evidence

The adopted plant is `14.2748/[s(8.1s+1)]`, sensor gain is 0.93 V/m, and report controller gain is 0.01432 V/V. Identification uses a 2.5 to 5.0 V actuator step, increment 2.5 V. The nominal controller demonstration uses a 0 to 5 m position reference.

Nominal prediction: 25.08% overshoot and 54.89 s settling in the 2% reference band. The retained hardware display gives 97.30% tracking and about 23.77% overshoot about the commanded reference. Independent resistor mismatch and joint drag/gain uncertainty do not establish full robustness. The student reports a full demo mark. Repeated identification trials and raw Session 2 logs were not supplied.

## Repository

[NateDogg247/EEE3094S---Lab-2-PTRJUN003-](https://github.com/NateDogg247/EEE3094S---Lab-2-PTRJUN003-), branch `main`.

The central link settings are in `report/repository.tex`. To regenerate them:

```text
python scripts/set_repository.py https://github.com/NateDogg247/EEE3094S---Lab-2-PTRJUN003-
```

Rebuild the PDF after changing link settings. See [RUBRIC_REVIEW.md](RUBRIC_REVIEW.md) for the available evidence.

## Clarified controller test

The full three-op-amp circuit remained connected for the physical controller test. The physical potentiometer was adjusted until the input was approximately 2.565 V. This recalled observation is recorded separately from the nominal 2.500 V zero-error hover condition and the terminal 2.498 V display. See `data/session2/test_conditions.json` and the report adjustment calculation.

The current KiCad drawing contains no capacitors, no unused pin-1/pin-5 graphics or crosses, and no opening title/subtitle. Open `hardware/kicad/Kitticopter_3OpAmp_Controller.kicad_pro`.

The first-logging CSV reattached in this revision is byte-identical to the retained data. The manual input reaches 5 V through 2.908 V at 15.8 s and 4.607 V at 15.9 s; the report shows and checks this finite transition. The parameter-check screenshot records A=14.2748 (100%), tau=8.1 (96%) and sensor=0.93 (100%).
