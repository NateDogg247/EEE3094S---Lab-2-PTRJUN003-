# EEE3094S Lab 2 — PTRJUN003

Junaid Allan Pieters — Proportional Control of the Kitticopter, University of Cape Town.

- [Report PDF](report/PTRJUN003_Lab2_Report.pdf): exactly **14 main pages**, excluding the title, contents, figure/table lists, references and appendices.
- [Worked calculations PDF](calculations/PTRJUN003_Lab2_Calculations.pdf): identification, root locus, response, circuit loading, robustness and experimental metrics.
- [Code guide](CODE_GUIDE.md): module responsibilities and instructions.

The report follows the supplied previous-year example with numbered chapter headings, a Prepared by / Prepared for cover, a separate conclusion page and a calculation/simulation/experiment comparison. It retains the template's Computer Modern font, 12 pt text, one-inch margins and spacing, with angel-blue accents and the UCT logo. Original photos and screenshots are in the appendices. Internal references and GitHub folder/file links are clickable.

## Project map

| Folder | Contents |
| --- | --- |
| [config](config) | Shared physical parameters read by Python and MATLAB |
| [analysis](analysis) | Python launcher and separate numerical modules |
| [matlab](matlab) | Launchers, identification, design, validation and Simulink code |
| [calculations](calculations) | Worked calculation PDF, equation source and topic index |
| [data/session1](data/session1) | Original identification CSV |
| [data/session2](data/session2) | Supplied experimental and Simulink screenshots |
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

The launcher runs identification, nominal controller analysis, robustness, hardware digitisation and disturbance prediction in order. It writes results and report plots.

## Run MATLAB

Download/extract the entire project. In MATLAB, set Current Folder to `matlab`, then run:

```matlab
run_all
```

For the detailed root locus method alone:

```matlab
root_locus_design
```

Control System Toolbox is required. Simulink is required only for the model builder. MATLAB source is supplied but was not executed in the authoring environment; Python reproduced the saved numerical results.

## Build the PDFs

With Python, Bash and a LaTeX distribution containing `latexmk`, TikZ and Circuitikz:

```bash
bash scripts/build.sh
```

For LaTeX-only compilation, select the root `main.tex` in Overleaf. The calculation supplement compiles from `calculations/main.tex` in that directory with a local LaTeX editor.

## Model and retained evidence

The adopted plant is `14.2748/[s(8.1s+1)]`, sensor gain is 0.93 V/m, and report controller gain is 0.01432 V/V. Identification uses a 2.5 to 5.0 V actuator step, increment 2.5 V. The nominal controller demonstration uses a 0 to 5 m position reference.

Nominal prediction: 25.08% overshoot and 54.89 s settling in the 2% reference band. The retained hardware display gives 97.30% tracking and about 23.77% overshoot about the commanded reference. Independent resistor mismatch and joint drag/gain uncertainty do not establish full robustness. Repeated trials, raw Session 2 logs and a signed demonstration mark were not supplied.

## Repository

[NateDogg247/EEE3094S---Lab-2-PTRJUN003-](https://github.com/NateDogg247/EEE3094S---Lab-2-PTRJUN003-), branch `main`.

The central link settings are in `report/repository.tex`. To regenerate them:

```text
python scripts/set_repository.py https://github.com/NateDogg247/EEE3094S---Lab-2-PTRJUN003-
```

Rebuild the PDF after changing link settings. See [RUBRIC_REVIEW.md](RUBRIC_REVIEW.md) for the available evidence.
