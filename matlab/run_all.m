% Run Session 1 identification and the proportional-controller checks.
% Requires Control System Toolbox. Simulink is optional.
clear; close all; clc;
addpath(genpath(fileparts(mfilename('fullpath'))));
P = lab_parameters();
identification_result = identify_session1(P);
root_locus_result = run_root_locus_design(P);
verify_nominal_controller(P);
plot_report_figures(P);
if license('test','Simulink')
    model = create_simulink_model(P);
    disp('Simulink model built. Run sim(model) when required.');
end
