# Report plot reproduction in MATLAB

From the project root:
```matlab
addpath(genpath("matlab"));
plot_report_figures(lab_parameters());
```
Requires MATLAB R2020a or newer (`exportgraphics`), using standard analytical response formulas for the nominal plots. The separately supplied transfer-function checks require Control System Toolbox. Plots reproduce identification, sensor/velocity/position validation, root locus, nominal response, drag uncertainty, resistor corners, controller comparison, supplied Simulink comparison and the defined 2 mV disturbance. The two screenshot-derived CSVs are approximate evidence and are never labelled raw instrument/solver logs. Outputs are saved in `results/matlab/figures`.
