# EEE3094S Lab 2 — PTRJUN003

Junaid Allan Pieters — Proportional Control of the Kitticopter.

The revised report follows the supplied example's section hierarchy and the LaTeX template's Computer Modern font, margins, spacing and ruled title page. It includes the original UCT crest and angel-blue accents. All photos and original screenshots are in appendices. Worked calculations, component values, comparison tables and cross-referenced plots are included.

## Open or compile

- Compiled report: `report/PTRJUN003_Lab2_Report.pdf`.
- Overleaf/root compilation: select `main.tex` at the project root.
- Full numerical regeneration: `python -m pip install -r requirements.txt`, then `bash scripts/build.sh`.
- Compile only: `latexmk -pdf main.tex` from the project root, or from `report/`.

The main report is 15 pages, including references, excluding cover, contents and appendices. Figure, table, equation, contents and appendix references are real internal PDF links. Folder-evidence links jump to the relevant appendix in this edition. External local-file launch links were removed because web PDF viewers commonly block them.

## Supporting files

| Folder | Contents |
| --- | --- |
| `data/session1` | Original identification CSV |
| `data/session2` | Retained experimental and Simulink images |
| `hardware` | Board photo, circuit sources, corrected KiCad copy and design basis |
| `analysis` | Executable Python calculations and plots |
| `results` | Processed data, model traces, metrics and tolerance corners |
| `matlab` | Independent verification and Simulink-building scripts |
| `report` | LaTeX sections, vector figures and PDF |
| `scripts` | Build and central repository-link configuration |

## Git and online folder links

The ZIP includes a complete `repository.bundle`. To recover the repository history:

```bash
git clone repository.bundle eee3094s-lab2-ptrjun003
```

The requested remote `NateDogg247/eee3094s-lab2-ptrjun003` was not accessible when checked. No live URL is asserted. After creating that repository and pushing the project, configure and rebuild:

```bash
git remote add origin https://github.com/NateDogg247/eee3094s-lab2-ptrjun003.git
git push -u origin main
python scripts/set_repository.py https://github.com/NateDogg247/eee3094s-lab2-ptrjun003
bash scripts/build.sh
```

Only use those commands once the remote exists and the user is authenticated. `python scripts/set_repository.py local` restores internal evidence links. For a private repo, grant the marker access.

## Evidence and results

One identification run and one experimental controller display are retained. Repeated trials and raw Session 2 logs are not invented. Nominal gain 0.01432 predicts 25.08% overshoot and 54.89 s 2% settling; the display gives 97.30% tracking and approximately 23.77% overshoot about the commanded reference. Standard overshoot about the displayed terminal value is approximately 27.20%.

The complete bias network yields Kp=0.014321913, correcting the first report's incomplete loading calculation. Independent loop-resistor corners give up to 48.79% DC tracking error and 38.95% overshoot. Recommended matching, gain reduction and hover calibration are proposed improvements, not claimed physical modifications. See `RUBRIC_REVIEW.md` for evidence limits.
