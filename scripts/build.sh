#!/usr/bin/env bash
set -euo pipefail
task_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$task_root"
python3 analysis/analyse.py
python3 scripts/export_diagrams.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd calculations/main.tex
cp calculations/main.pdf calculations/PTRJUN003_Lab2_Calculations.pdf
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd report/main.tex
cp report/main.pdf report/PTRJUN003_Lab2_Report.pdf
python3 scripts/check_report.py
python3 scripts/make_source_listing.py
printf 'Built report and calculation PDFs.\n'
