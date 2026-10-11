# MATLAB code

Set Current Folder to this directory and run `run_all`, or `addpath(genpath(pwd)); run_root_locus_design(lab_parameters)` for the root-locus method alone.

Implementations are divided into `config`, `identification`, `design`, `validation`, `plots` and `simulink`. Parameters are read from the project root's `config/lab_parameters.json`.

Control System Toolbox is required for `run_all` and the root-locus design. The report-figure function `plot_report_figures` uses analytical expressions and CSV data; it exports vector PDF and PNG figures with MATLAB R2020a or newer. Simulink is required for the model builder and `run_simulink_tests`. Outputs go to `results/matlab`. See [the code guide](../CODE_GUIDE.md).

To run both native Simulink cases and export their logged results, run `run_simulink_tests` after adding these folders to the MATLAB path. MATLAB was not available in the report-generation environment: the supplied Simulink screenshot is retained evidence, and the delivered figures were rendered with Python.
